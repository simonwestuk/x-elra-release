"""ARL cycle orchestration."""
from __future__ import annotations

import copy
import hashlib
import json
import logging
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence
from uuid import uuid4

from sqlalchemy.orm import Session

from ..config import get_arm_buckets, get_arm_config, settings
from ..utils.db import (
    ARLDecision,
    ARLOutcome,
    FeatureSnapshot,
    SessionLocal,
    get_or_assign_arm,
)
from .evaluation import schedule_evaluation
from .controller_state import ControllerState
from .routines import evaluate_routines, get_routine_bundle
from .schemas import ARLCycleResult, ExecutionContext, FeatureVector, RoutineResult
from .state import build_feature_vector, get_redis_client
from ..olm.regulatory import (
    build_learner_facing_projection,
    build_context_summary,
    build_inputs_used_summary,
    compute_next_transition_conditions,
)

logger = logging.getLogger(__name__)


def _metric_increment(metrics: object, name: str, *, amount: int = 1, **tags: object) -> None:
    if metrics is None:
        return
    if hasattr(metrics, "increment"):
        try:
            metrics.increment(name, amount=amount, tags=tags or None)
            return
        except TypeError:
            metrics.increment(name, amount=amount)
            return
    if hasattr(metrics, "inc"):
        try:
            metrics.inc(name, amount)
        except TypeError:
            metrics.inc(name)


class _SpanContext:
    def __init__(self, span: Any):
        self._span = span

    def __enter__(self):
        if hasattr(self._span, "__enter__"):
            return self._span.__enter__()
        return self._span

    def __exit__(self, exc_type, exc, tb):
        if hasattr(self._span, "__exit__"):
            return self._span.__exit__(exc_type, exc, tb)
        if hasattr(self._span, "end"):
            self._span.end()
        return False


def _start_span(tracer: object, name: str, **attrs: object):
    if tracer is None:
        return nullcontext()
    start_as_current = getattr(tracer, "start_as_current_span", None)
    if callable(start_as_current):
        try:
            return start_as_current(name, attributes=attrs or None)
        except TypeError:
            return start_as_current(name)
    start_span = getattr(tracer, "start_span", None)
    if callable(start_span):
        span = start_span(name, attributes=attrs or None)
        return _SpanContext(span)
    return nullcontext()


def _canonicalize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonicalize_value(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonicalize_value(v) for v in value]
    if isinstance(value, float):
        if value != value:
            return "NaN"
        if value == float("inf"):
            return "Infinity"
        if value == float("-inf"):
            return "-Infinity"
        normalized = float(f"{value:.12g}")
        return 0.0 if normalized == -0.0 else normalized
    if isinstance(value, (int, bool)) or value is None:
        return value
    return str(value)


def _build_canonical_snapshots(items: Sequence[Mapping[str, Any]]) -> Sequence[Mapping[str, Any]]:
    snapshots = []
    for rank, item in enumerate(items):
        if not isinstance(item, Mapping):
            continue
        components = item.get("components")
        if not isinstance(components, Mapping):
            components = {}
        weights = components.get("weights") or components.get("routine_weights") or {}
        if not isinstance(weights, Mapping):
            weights = {}
        features = components.get("features")
        if not isinstance(features, Mapping):
            features = {}
        diversity = item.get("diversity_penalty")
        if diversity is None:
            diversity = components.get("diversity_penalty") or components.get("diversity_penalties")
        snapshot = {
            "item_id": str(item.get("item_id", "")),
            "rank": int(item.get("rank", rank)),
            "score": _canonicalize_value(item.get("score", 0.0)),
            "features": _canonicalize_value(features),
            "weights": _canonicalize_value(weights),
        }
        if diversity is not None:
            snapshot["diversity_penalty"] = _canonicalize_value(diversity)
        snapshots.append(snapshot)
    return snapshots


def _serialize_for_hash(snapshots: Sequence[Mapping[str, Any]], seed_value: Optional[int]) -> str:
    payload = {
        "seed": _canonicalize_value(seed_value),
        "items": [snapshot for snapshot in snapshots],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _build_trace_id(
    *,
    routine_version: str,
    controller_state_before: Any,
    feature_vector: FeatureVector,
    routine_results: Sequence[RoutineResult],
) -> str:
    trace_payload = {
        "routine_version": routine_version,
        "state_before": controller_state_before.to_dict()
        if controller_state_before is not None
        else None,
        "inputs": feature_vector.to_dict(),
        "routine_path": [result.to_dict() for result in routine_results],
    }
    canonical = _canonicalize_value(trace_payload)
    serialized = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _collect_items(context_shared: Mapping[str, Any], routine_results) -> Sequence[Mapping[str, Any]]:
    payload = context_shared.get("last_recommendations")
    if isinstance(payload, Mapping):
        items = payload.get("items")
        if isinstance(items, Sequence):
            return [item for item in items if isinstance(item, Mapping)]
    items = []
    for result in routine_results:
        for action in result.actions:
            if action.action_type == "fetch_recommendations" and isinstance(action.payload, Mapping):
                raw = action.payload.get("items")
                if isinstance(raw, Sequence):
                    items.extend([item for item in raw if isinstance(item, Mapping)])
    return items


def _collect_telemetry(routine_results) -> Sequence[Mapping[str, Any]]:
    events = []
    for result in routine_results:
        for action in result.actions:
            if action.action_type == "log_impressions" and isinstance(action.payload, Mapping):
                events.append({"type": "impression", **action.payload})
            payload = action.payload
            if isinstance(payload, Mapping) and "telemetry" in payload:
                telemetry_payload = payload["telemetry"]
                if isinstance(telemetry_payload, Mapping):
                    events.append(
                        {
                            **telemetry_payload,
                            "routine": result.routine.name,
                            "action": action.action_name,
                        }
                    )
                elif isinstance(telemetry_payload, Sequence):
                    for entry in telemetry_payload:
                        if isinstance(entry, Mapping):
                            events.append(
                                {
                                    **entry,
                                    "routine": result.routine.name,
                                    "action": action.action_name,
                                }
                            )
    return events


def _inject_elapsed_times(controller_state: Any, *, now: datetime) -> None:
    if controller_state is None:
        return
    metadata = controller_state.metadata
    if not isinstance(metadata, dict):
        return
    last_intervention = controller_state.timers.last_intervention
    if last_intervention is not None:
        metadata["time_since_last_intervention_seconds"] = (now - last_intervention).total_seconds()
    last_transition = controller_state.timers.last_mode_transition
    if last_transition is not None:
        metadata["time_since_last_mode_transition_seconds"] = (now - last_transition).total_seconds()
    elapsed_since_routine = {}
    for routine_name, last_exec in controller_state.timers.last_routine_executed.items():
        elapsed_since_routine[routine_name] = (now - last_exec).total_seconds()
    if elapsed_since_routine:
        metadata["elapsed_since_routine_seconds"] = elapsed_since_routine


def _assemble_explanations(feature_vector: FeatureVector, items: Sequence[Mapping[str, Any]]):
    mastery_sorted = sorted(feature_vector.mastery.items(), key=lambda kv: kv[1])
    gaps = [skill for skill, value in mastery_sorted if value < 0.8][:3]
    explanations = []
    for rank, item in enumerate(items):
        explanations.append(
            {
                "item_id": item.get("item_id"),
                "rank": rank,
                "summary": "Recommended to strengthen skills: " + ", ".join(gaps)
                if gaps
                else "Recommended based on engagement patterns.",
                "score": item.get("score"),
            }
        )
    return explanations


def _persist_decision(
    session: Session,
    *,
    learner_id: str,
    decision_id: str,
    deterministic_hash: str,
    seed_value: Optional[int],
    routine_version: str,
    strategy: str,
    items: Sequence[Mapping[str, Any]],
    snapshots: Sequence[Mapping[str, Any]],
    feature_vector: FeatureVector,
    routine_results,
    explanations,
    telemetry,
    decision_trace: Mapping[str, Any],
    request_id: str,
) -> None:
    request_payload = {
        "learner_id": learner_id,
        "feature_vector": feature_vector.to_dict(),
        "routine_version": routine_version,
        "request_id": request_id,
    }
    canonical_items = [_canonicalize_value(item) for item in items]
    response_payload = {
        "items": canonical_items,
        "explanations": [_canonicalize_value(exp) for exp in explanations],
        "telemetry": [_canonicalize_value(event) for event in telemetry],
        "routine_results": [result.to_dict() for result in routine_results],
        "decision_trace": _canonicalize_value(decision_trace),
        "decision_id": decision_id,
        "deterministic_hash": deterministic_hash,
        "routine_version": routine_version,
    }
    request_payload = _canonicalize_value(request_payload)
    response_payload = _canonicalize_value(response_payload)
    existing = session.query(ARLDecision).filter_by(decision_id=decision_id).one_or_none()
    if existing is not None:
        return
    decision = ARLDecision(
        decision_id=decision_id,
        learner_id=learner_id,
        policy_name=strategy,
        deterministic_hash=deterministic_hash,
        policy_version=routine_version,
        seed=str(seed_value) if seed_value is not None else None,
        request_id=request_id,
        request_payload=json.dumps(request_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
        response_payload=json.dumps(response_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
    )
    session.add(decision)
    session.flush()
    outcome_models = []
    feature_snapshot_models = []
    for snapshot in snapshots:
        diversity = snapshot.get("diversity_penalty")
        diversity_json = (
            json.dumps(diversity, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            if diversity is not None
            else None
        )
        features_json = (
            json.dumps(
                snapshot.get("features", {}),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            if snapshot.get("features") is not None
            else None
        )
        weights_json = (
            json.dumps(
                snapshot.get("weights", {}),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            if snapshot.get("weights") is not None
            else None
        )
        outcome_models.append(
            ARLOutcome(
                decision_id=decision.decision_id,
                item_id=str(snapshot.get("item_id", "")),
                rank=int(snapshot.get("rank", 0)),
                score=_canonicalize_value(snapshot.get("score")),
                features_json=features_json,
                weights_json=weights_json,
                metadata_json=diversity_json,
            )
        )
        feature_snapshot_models.append(
            FeatureSnapshot(
                decision_id=decision.decision_id,
                item_id=str(snapshot.get("item_id", "")),
                rank=int(snapshot.get("rank", 0)),
                features_json=features_json,
                weights_json=weights_json,
            )
        )
    if outcome_models:
        session.add_all(outcome_models)
    if feature_snapshot_models:
        session.add_all(feature_snapshot_models)
    session.commit()


def _stable_seed(*parts: object) -> int:
    material = "::".join(str(part) for part in parts)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def _evaluate_routines_bounded(bundle, context, *, base_seed=None):
    """
    Evaluate control routines with boundedness enforcement (formal ARL).

    This implements Algorithm Step 4 from the ARL paper:
    FOR each routine r ∈ R_t (in priority order):
      a. CHECK mode_permitted(r, S_t.mode)
      b. CHECK cooldown_active(r, S_t.timers)
      c. CHECK budget_available(r, S_t.budgets)
      d. EVALUATE conditions(r, I_t)
      e. EXECUTE actions(r) → A_t
      f. CONSUME resources(r, S_t.budgets)
      g. BREAK (single-action selection)

    This wraps standard control routine evaluation with mode gating, cooldown checks,
    budget enforcement, and oscillation prevention.
    """
    from .boundedness import check_routine_permitted, consume_routine_resources
    from .routines import _stable_seed, execute_action, evaluate_routine_conditions

    results = []

    from .boundedness import _get_permitted_modes

    for index, routine in enumerate(bundle.routines):
        if not routine.enabled:
            results.append(
                RoutineResult(
                    routine=routine,
                    seed=None,
                    actions=[],
                    skipped=True,
                    error=None,
                    skip_reason="disabled",
                    outcome="SKIPPED",
                )
            )
            continue

        # Algorithm 1, line 6: Mode mismatch check → SKIPPED
        permitted_modes = _get_permitted_modes(routine)
        if permitted_modes and context.controller_state.mode not in permitted_modes:
            context.logger.info(
                "arl.routine_skipped",
                extra={
                    "routine": routine.name,
                    "reason": "mode_mismatch",
                    "mode": context.controller_state.mode.value,
                    "permitted": [m.value for m in permitted_modes],
                },
            )
            results.append(
                RoutineResult(
                    routine=routine,
                    seed=None,
                    actions=[],
                    skipped=True,
                    skip_reason="mode_mismatch",
                    outcome="SKIPPED",
                )
            )
            continue

        # Algorithm 1, line 8: Trigger conditions check → SKIPPED
        if not evaluate_routine_conditions(routine.conditions, context):
            results.append(
                RoutineResult(
                    routine=routine,
                    seed=None,
                    actions=[],
                    skipped=True,
                    skip_reason="conditions_not_met",
                    outcome="SKIPPED",
                )
            )
            continue

        # Algorithm 1, line 10: Boundedness check (cooldown, budget, oscillation) → BLOCKED
        permitted, block_reason = check_routine_permitted(
            routine,
            context.controller_state,
            now=context.feature_vector.generated_at,
        )
        if not permitted:
            context.logger.info(
                "arl.routine_blocked",
                extra={"routine": routine.name, "reason": block_reason, "mode": context.controller_state.mode.value},
            )
            results.append(
                RoutineResult(
                    routine=routine,
                    seed=None,
                    actions=[],
                    skipped=True,
                    error=f"blocked: {block_reason}",
                    skip_reason=block_reason,
                    outcome="BLOCKED",
                )
            )
            continue

        # Algorithm 1, line 13: Execute routine
        routine_seed = _stable_seed(
            context.learner_id,
            bundle.version,
            routine.name,
            base_seed or 0,
            index,
        )

        result = RoutineResult(routine=routine, seed=routine_seed)

        for action_index, action in enumerate(routine.actions):
            action_seed = _stable_seed(routine_seed, action.name, action_index)
            action_result = execute_action(routine.name, action, context, action_seed)
            result.actions.append(action_result)

            context.shared[f"{routine.name}.{action.name}"] = action_result.payload
            context.shared[action.name] = action_result.payload

        # Section 4.3: EXECUTED_ACTION if actions produced results, EXECUTED_NO_ACTION if all empty
        has_action = any(a.payload for a in result.actions)
        result.outcome = "EXECUTED_ACTION" if has_action else "EXECUTED_NO_ACTION"
        result.stop_evaluation = True

        consume_routine_resources(routine, context.controller_state)
        context.controller_state.timers.mark_execution(
            routine.name,
            now=context.feature_vector.generated_at,
        )

        _metric_increment(context.metrics, "arl.routine.completed", routine=routine.name)
        results.append(result)

        # Algorithm 1, line 16: BREAK if routine terminates evaluation
        break

    return results


def run_arl_cycle(
    learner_id: str,
    *,
    session: Optional[Session] = None,
    routine_path: Optional[str | Path] = None,
    redis_client: Any | None = None,
    metrics: Any = None,
    tracer: Any = None,
    logger_override: Optional[logging.Logger] = None,
    evaluation_scheduler: Any = None,
    refresh_features: bool = False,
) -> ARLCycleResult:
    """
    Execute one ARL cycle for learner_id.

    This implements the complete ARL decision cycle algorithm from the paper:

    ALGORITHM: ARL Decision Cycle at time t

    INPUT:  learner_id, session context
    OUTPUT: ARLCycleResult (decision trace T_t)

    1. LOAD I_t ← build_feature_vector(learner_id)
    2. LOAD S_t ← get_controller_state(learner_id)
    3. LOAD R_t ← get_routine_bundle()
    4. FOR each routine r ∈ R_t: [evaluate with boundedness]
    5. IF no routine executed: A_t ← ∅ (deliberate non-intervention)
    6. COMPUTE S_{t+1} ← transition_state(S_t, A_t, I_t)
    7. EMIT T_t ← build_decision_trace(...)
    8. PERSIST decision(T_t, deterministic_hash)
    9. RETURN ARLCycleResult(T_t)
    """

    log = logger_override or logger
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True
    request_id = str(uuid4())
    redis_client = redis_client or get_redis_client()

    try:
        with _start_span(tracer, "arl.cycle", learner_id=learner_id):
            _metric_increment(metrics, "arl.cycle.start", learner_id=learner_id)

            # === ALGORITHM STEP 1: Load I_t (Perception Inputs) ===
            feature_vector = build_feature_vector(
                session,
                learner_id,
                redis_client=redis_client,
                refresh=refresh_features,
            )

            # === Resolve arm assignment before controller state ===
            # The arm determines whether bounded ARL applies (Table 8).
            arm_value = get_or_assign_arm(session, learner_id)
            _arm_slug = get_arm_buckets().get(arm_value, arm_value)
            try:
                _arm_cfg = get_arm_config(_arm_slug)
            except Exception:
                _arm_cfg = None

            # Bounded ARL controller state is only needed for the treatment
            # arm (regulatory_mode=True).  B1 (model-driven) and B3 (OLM-only)
            # must not be governed by ARL mode gating / budgets / cooldowns.
            _arm_needs_governance = (
                settings.enable_formal_arl
                and (_arm_cfg is not None and _arm_cfg.regulatory_mode)
            )

            # === ALGORITHM STEP 2: Load S_t (Controller State) ===
            if _arm_needs_governance:
                from ..utils.db import get_controller_state
                controller_state = get_controller_state(session, learner_id)
                _inject_elapsed_times(controller_state, now=feature_vector.generated_at)

                # Infer mode from current perceptions I_t before routine evaluation.
                # The persisted mode may be stale (e.g. COLD_START for a learner who
                # now has mastery). Mode inference is part of the reasoning step and
                # must precede routine gating.
                from .mode_inference import infer_mode as _infer_mode_early
                from .boundedness import check_transition_allowed as _check_early
                inferred_mode = _infer_mode_early(feature_vector, controller_state)
                if inferred_mode != controller_state.mode:
                    allowed, _reason = _check_early(
                        controller_state.mode,
                        inferred_mode,
                        controller_state.timers,
                        now=feature_vector.generated_at,
                    )
                    if allowed:
                        controller_state.mode = inferred_mode
                        controller_state.timers.last_mode_transition = feature_vector.generated_at
                        controller_state.recent_outcomes.record_transition(now=feature_vector.generated_at)
                        controller_state.metadata["mode_transition_count"] = (
                            controller_state.metadata.get("mode_transition_count", 0) + 1
                        )

                log.info(
                    "arl.state_loaded",
                    extra={
                        "learner_id": learner_id,
                        "mode": controller_state.mode.value,
                        "budgets": controller_state.budgets.to_dict(),
                    }
                )

                # Snapshot S_t before routine evaluation mutates budgets/timers.
                # _evaluate_routines_bounded() consumes budgets and marks timers
                # in-place on controller_state, so without this snapshot the
                # trace would record identical before/after budgets.
                controller_state_before = copy.deepcopy(controller_state)
            else:
                controller_state = None
                controller_state_before = None

            # === ALGORITHM STEP 3: Load R_t (Ordered Control Routine Set) ===
            bundle = get_routine_bundle(routine_path)

            cycle_seed = _stable_seed(
                learner_id,
                bundle.version,
                feature_vector.generated_at.isoformat(),
            )
            context = ExecutionContext(
                learner_id=learner_id,
                feature_vector=feature_vector,
                db=session,
                logger=log,
                metrics=metrics,
                tracer=tracer,
                shared={},
                request_id=request_id,
                routine_version=settings.routine_version,
                bundle=bundle,
                cycle_seed=cycle_seed,
                controller_state=controller_state,
                arm=arm_value,
            )

            # === ALGORITHM STEP 4: Evaluate R_t with Boundedness ===
            # Iterate through routines in priority order.
            # The evaluation mode depends on the learner's assigned arm
            # (Table 8 – Cognitive Load row):
            #   Treatment:  bounded ARL (mode gating, cooldowns, budgets)
            #   B1 control: unbounded model-driven (no governance constraints)
            #   B3 control: no intervention at all (OLM-only transparency)
            _arm_skips_intervention = (
                _arm_cfg is not None and not _arm_cfg.explain
            )

            if _arm_skips_intervention:
                # B3 (OLM-only): deliberate non-intervention — no routines fire.
                routine_results = []
                log.info(
                    "arl.arm_skips_intervention",
                    extra={"learner_id": learner_id, "arm": arm_value},
                )
            elif _arm_needs_governance:
                routine_results = _evaluate_routines_bounded(bundle, context, base_seed=cycle_seed)
            else:
                routine_results = evaluate_routines(bundle, context, base_seed=cycle_seed)
            # === ALGORITHM STEP 5: Determine A_t (Selected Action) ===
            # First successful routine = A_t, or ∅ if all blocked/skipped
            executed_routine = next(
                (r.routine.name for r in routine_results if not r.skipped and not r.error),
                "NO_ACTION"
            )

            # === ALGORITHM STEP 6: Compute S_{t+1} (State Transition) ===
            # Deterministic state update: mode inference, budget updates, timers
            controller_state_after = controller_state or ControllerState(
                learner_id=learner_id
            )
            if _arm_needs_governance and controller_state is not None:
                from .mode_inference import transition_state, get_mode_inference_reason
                from .boundedness import check_transition_allowed

                controller_state_after = transition_state(controller_state, executed_routine, feature_vector)

                # Check if mode transition is allowed
                transition_ok, transition_reason = check_transition_allowed(
                    controller_state.mode,
                    controller_state_after.mode,
                    controller_state.timers,
                    now=feature_vector.generated_at,
                )
                if not transition_ok:
                    exploit_reason = get_mode_inference_reason(feature_vector, controller_state)
                    log.warning(
                        "arl.mode_transition_blocked: %s -> %s blocked (%s), exploit_reason=%s, routine=%s, learner=%s",
                        controller_state.mode.value,
                        controller_state_after.mode.value,
                        transition_reason,
                        exploit_reason,
                        executed_routine,
                        learner_id,
                    )
                    controller_state_after.mode = controller_state.mode  # Revert mode

                # Persist new state
                from ..utils.db import save_controller_state
                save_controller_state(session, controller_state_after)
                _metric_increment(
                    metrics, "arl.state_transition",
                    old_mode=controller_state.mode.value,
                    new_mode=controller_state_after.mode.value
                )
            else:
                from .mode_inference import infer_mode
                controller_state_after.mode = infer_mode(feature_vector, controller_state_after)

            # === ALGORITHM STEP 7: Emit T_t (Decision Trace) ===
            items = _collect_items(context.shared, routine_results)
            explanations = _assemble_explanations(feature_vector, items)
            telemetry_events = _collect_telemetry(routine_results)
            evaluation_job = None
            snapshots = _build_canonical_snapshots(items)
            serialized = _serialize_for_hash(snapshots, cycle_seed)
            deterministic_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
            strategy = executed_routine if _arm_needs_governance else (
                context.shared.get("last_recommendations", {}).get("strategy")
                if isinstance(context.shared.get("last_recommendations"), Mapping)
                else None
            ) or "arl"

            # Build decision trace fields per Paper Section 4.4
            executed_routine = next(
                (r for r in routine_results if not r.skipped and not r.error),
                None
            )

            if executed_routine:
                action_name = None
                if executed_routine.actions:
                    action_name = executed_routine.actions[0].action_name

                # Appendix A.3 decision schema: {action, source_routine}
                decision_object = {
                    "action": action_name,
                    "source_routine": executed_routine.routine.name,
                }
            else:
                # Deliberate non-intervention (∅) per Appendix A.3
                decision_object = {
                    "action": None,
                    "source_routine": None,
                }

            evaluation_terminated = False
            terminated_by = None
            for result in routine_results:
                if result.stop_evaluation:
                    evaluation_terminated = True
                    terminated_by = result.routine.name
                    break

            context_summary = build_context_summary(feature_vector)
            inputs_used = build_inputs_used_summary(feature_vector, routine_results)

            next_transition_conditions = compute_next_transition_conditions(
                controller_state_after,
                feature_vector.metadata
            )

            learner_facing_fields = build_learner_facing_projection(
                controller_state_after,
                feature_vector.metadata,
                feature_vector
            )
            if decision_object["action"] is None:
                suppression_reasons = []
                for result in routine_results:
                    if result.skipped:
                        suppression_reasons.append(result.skip_reason or result.error or "skipped")
                if suppression_reasons:
                    learner_facing_fields = {
                        **learner_facing_fields,
                        "suppression_reasons": list(dict.fromkeys(suppression_reasons)),
                    }

            decision_id = _build_trace_id(
                routine_version=settings.routine_version,
                controller_state_before=controller_state_before,
                feature_vector=feature_vector,
                routine_results=routine_results,
            )
            decision_trace = {
                "trace_id": decision_id,
                "timestamp": feature_vector.generated_at.isoformat(),  # Appendix A.3
                "routines_version": settings.routine_version,  # Appendix A.3
                "context_summary": context_summary,
                "inputs_used": inputs_used,
                "state_before": controller_state_before.to_dict() if controller_state_before else None,
                "routine_path": [result.to_dict() for result in routine_results],
                "decision": decision_object,
                "state_after": controller_state_after.to_dict() if controller_state_after else None,
                "next_transition_conditions": next_transition_conditions,
                "olm_projection": learner_facing_fields,  # Appendix A.3 field name
            }
            # Build compact decision trace per Appendix A.3 schema:
            #   trace_id, timestamp, routines_version, state_before,
            #   inputs_summary, routine_path, decision, state_after,
            #   exit_conditions, olm_projection.
            compact_decision_trace = {
                "trace_id": decision_id,
                "timestamp": feature_vector.generated_at.isoformat(),
                "routines_version": settings.routine_version,
                "state_before": controller_state_before.to_trace_dict() if controller_state_before else None,
                "inputs_summary": inputs_used,  # Appendix A.3
                "routine_path": [
                    r.to_trace_dict()
                    for r in routine_results
                ],
                "decision": decision_object,
                "state_after": controller_state_after.to_trace_dict() if controller_state_after else None,
                "exit_conditions": next_transition_conditions,
                "olm_projection": learner_facing_fields,
            }

            # === ALGORITHM STEP 8: Persist Decision Trace ===
            # Store T_t for audit, replay, and learner-facing explanation
            _persist_decision(
                session,
                learner_id=learner_id,
                decision_id=decision_id,
                deterministic_hash=deterministic_hash,
                seed_value=cycle_seed,
                routine_version=settings.routine_version,
                strategy=strategy,
                items=items,
                snapshots=snapshots,
                feature_vector=feature_vector,
                routine_results=routine_results,
                explanations=explanations,
                telemetry=telemetry_events,
                decision_trace=decision_trace,
                request_id=request_id,
            )
            evaluation_job = schedule_evaluation(
                learner_id,
                routine_results,
                scheduler=evaluation_scheduler,
                decision_id=decision_id,
                metadata={"deterministic_hash": deterministic_hash},
                now=feature_vector.generated_at,
            )
            log.info(
                "arl decision generated",
                extra={
                    "learner_id": learner_id,
                    "decision_id": decision_id,
                    "deterministic_hash": deterministic_hash,
                    "routine_version": settings.routine_version,
                    "item_count": len(items),
                },
            )
            _metric_increment(metrics, "arl.cycle.completed", learner_id=learner_id)

            active_routines = [
                (result.routine.description or result.routine.name)
                for result in routine_results
                if not result.skipped
            ]

            # === ALGORITHM STEP 9: Return Decision Trace T_t ===
            # ARLCycleResult contains complete trace for API response
            return ARLCycleResult(
                learner_id=learner_id,
                decision_id=decision_id,
                deterministic_hash=deterministic_hash,
                routine_version=settings.routine_version,
                seed=cycle_seed,
                feature_vector=feature_vector,
                routine_results=routine_results,
                explanations=explanations,
                telemetry_events=telemetry_events,
                evaluation_job=evaluation_job,
                active_routines=tuple(active_routines),
                controller_state_before=controller_state_before,
                controller_state_after=controller_state_after,
                # NEW: Decision trace fields per Section 4.4
                context_summary=context_summary,
                inputs_used=inputs_used,
                decision=decision_object,  # Appendix A.3: {action, source_routine}
                evaluation_terminated=evaluation_terminated,
                terminated_by=terminated_by,
                next_transition_conditions=next_transition_conditions,
                learner_facing_fields=learner_facing_fields,
                # Compact decision trace (minimal schema)
                decision_trace=compact_decision_trace,
            )
    except Exception:
        session.rollback()
        _metric_increment(metrics, "arl.cycle.error", learner_id=learner_id)
        log.exception("arl cycle failed", extra={"learner_id": learner_id})
        raise
    finally:
        if close_session:
            session.close()


__all__ = ["run_arl_cycle"]
