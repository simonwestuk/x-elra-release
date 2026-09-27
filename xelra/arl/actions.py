"""Action executors for ARL control routines."""
from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Mapping, MutableMapping, Optional, Sequence

from ..olm import service as olm_service
from ..utils.db import Impression
from .schemas import ActionDefinition, ActionResult, ExecutionContext

logger = logging.getLogger(__name__)

ActionExecutor = Callable[[str, ActionDefinition, ExecutionContext, Optional[int]], ActionResult]


def _store_payload(
    action: ActionDefinition,
    context: ExecutionContext,
    payload: Mapping[str, Any],
    telemetry_event: Optional[Mapping[str, Any]] = None,
) -> Mapping[str, Any]:
    context.shared[action.name] = payload
    if telemetry_event:
        events = context.shared.setdefault("_telemetry_events", [])
        if isinstance(events, list):
            events.append(dict(telemetry_event))
    return payload


def _canonicalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonicalize(v) for v in value]
    if isinstance(value, float):
        if value != value:  # NaN check
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


def _hash_payload(routine_name: str, action: ActionDefinition, payload: Mapping[str, Any], seed: Optional[int]) -> str:
    body = {
        "routine": routine_name,
        "action": action.name,
        "type": action.type,
        "seed": seed,
        "payload": _canonicalize(payload),
    }
    serialized = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _execute_fetch_recommendations(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    strategy = params.get("strategy") or context.feature_vector.metadata.get("strategy") or "hybrid"
    top_k = params.get("top_k") or context.feature_vector.metadata.get("top_k") or 10
    try:
        top_k = int(top_k)
    except (TypeError, ValueError):
        top_k = 10
    weights = params.get("weights")
    if weights is not None and not isinstance(weights, Mapping):
        weights = None
    rec_context = params.get("context", {})
    if not isinstance(rec_context, Mapping):
        rec_context = {}
    if params.get("include_feature_context", True):
        rec_context = {
            **rec_context,
            "recent_impressions": context.feature_vector.impressions,
            "goals": context.feature_vector.goals,
        }
    items_source = context.feature_vector.recommendations or []
    items = [item for item in items_source if isinstance(item, Mapping)]
    if top_k > 0:
        items = items[:top_k]
    payload = {
        "items": list(items),
        "strategy": strategy,
        "top_k": top_k,
        "weights": dict(weights or {}),
        "context": dict(rec_context),
    }
    return _store_payload(action, context, payload)


def _normalise_items(source: Any) -> Sequence[Mapping[str, Any]]:
    if isinstance(source, Mapping):
        items = source.get("items")
        if isinstance(items, Sequence):
            return [item for item in items if isinstance(item, Mapping)]
        return []
    if isinstance(source, Sequence):
        return [item for item in source if isinstance(item, Mapping)]
    return []


def _execute_log_impressions(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    source_key = params.get("from") or params.get("source")
    if source_key:
        source_payload = context.shared.get(source_key)
    else:
        source_payload = context.shared.get("last_recommendations")
    items = _normalise_items(source_payload)
    if not items:
        items = _normalise_items(context.feature_vector.recommendations)
    strategy = (
        params.get("strategy")
        or (source_payload or {}).get("strategy")
        or context.feature_vector.metadata.get("strategy")
        or "hybrid"
    )
    arm_value = params.get("arm") or context.arm or "NA"
    schema_version = params.get("schema_version") or context.bundle.schema_version
    request_id = params.get("request_id") or context.request_id
    telemetry_source = params.get("telemetry_source", "arl")
    explain_level = params.get("explain_level")
    course_id = params.get("course_id")

    saved = []
    if items:
        records = []
        for idx, item in enumerate(items, start=1):
            item_id = item.get("item_id")
            if not item_id:
                continue
            rank = item.get("rank")
            if rank is None:
                rank = idx - 1
            try:
                rank = int(rank)
            except (TypeError, ValueError):
                rank = idx - 1
            score = item.get("score")
            try:
                score_value = float(score) if score is not None else None
            except (TypeError, ValueError):
                score_value = None
            record = Impression(
                learner_id=context.learner_id,
                item_id=str(item_id),
                rank=rank,
                strategy=str(strategy),
                arm=str(arm_value),
                arm_key=str(arm_value),
                policy_version=context.routine_version,
                schema_version=str(schema_version),
                source=str(telemetry_source),
                explain_level=str(explain_level) if explain_level else None,
                course_id=str(course_id) if course_id else item.get("course_id"),
                request_id=request_id,
                score=score_value,
            )
            saved.append(
                {
                    "item_id": str(item_id),
                    "rank": rank,
                    "score": score_value,
                }
            )
            records.append(record)
        if records:
            context.db.add_all(records)
            context.db.commit()
    payload = {
        "logged": len(saved),
        "strategy": strategy,
        "schema_version": schema_version,
        "request_id": request_id,
        "items": saved,
    }
    return _store_payload(action, context, payload)


def _execute_store_payload(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    payload = dict(action.params)
    context.shared[action.name] = payload
    return payload


def _parse_due_date(raw: Any) -> Optional[datetime]:
    if not raw:
        return None
    if isinstance(raw, datetime):
        if raw.tzinfo is None:
            return raw.replace(tzinfo=timezone.utc)
        return raw.astimezone(timezone.utc)
    if isinstance(raw, str):
        text = raw.strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        else:
            parsed = parsed.astimezone(timezone.utc)
        return parsed
    return None


def _execute_assign_activity(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    skill_id = params.get("skill_id") or params.get("skill")
    if not skill_id:
        payload = {"skipped": True, "reason": "missing_skill"}
        return _store_payload(action, context, payload)
    target = params.get("target", 1.0)
    try:
        target_value = float(target)
    except (TypeError, ValueError):
        target_value = 1.0
    due_date = _parse_due_date(params.get("due_date") or params.get("due"))
    try:
        goal = olm_service.upsert_goal(
            context.db,
            context.learner_id,
            str(skill_id),
            target=target_value,
            due_date=due_date,
        )
        goal_id = getattr(goal, "id", None)
    except Exception as exc:  # pragma: no cover - defensive fallback
        context.logger.error(
            "failed to assign activity",
            extra={"routine": routine_name, "action": action.name, "learner_id": context.learner_id},
        )
        context.db.rollback()
        payload = {"skipped": True, "reason": "assignment_failed", "error": str(exc)}
        telemetry = {
            "type": "assign_activity",
            "status": "failed",
            "skill_id": str(skill_id),
            "target": target_value,
        }
        return _store_payload(action, context, payload, telemetry)

    telemetry = {
        "type": "assign_activity",
        "status": "success",
        "skill_id": str(skill_id),
        "target": target_value,
        "goal_id": goal_id,
    }
    if due_date is not None:
        telemetry["due_date"] = due_date.isoformat()
    payload = {
        "skill_id": str(skill_id),
        "target": target_value,
        "goal_id": goal_id,
        "due_date": due_date.isoformat() if due_date else None,
        "telemetry": telemetry,
    }
    return _store_payload(action, context, payload, telemetry)


def _execute_insert_prereq_review(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    item_payload = params.get("item")
    if not isinstance(item_payload, Mapping):
        item_id = params.get("item_id")
        item_payload = {"item_id": item_id}
    item_id = item_payload.get("item_id")
    if not item_id:
        payload = {"skipped": True, "reason": "missing_item"}
        return _store_payload(action, context, payload)
    reason = params.get("reason") or "prerequisite_review"
    try:
        position = int(params.get("position", 0))
    except (TypeError, ValueError):
        position = 0
    existing_payload = context.shared.get("last_recommendations")
    existing_items = list(_normalise_items(existing_payload))
    new_entry = {
        **{k: v for k, v in item_payload.items() if k != "item_id"},
        "item_id": str(item_id),
        "reason": reason,
        "injected": True,
    }
    if position < 0 or position > len(existing_items):
        position = len(existing_items)
    existing_items.insert(position, new_entry)
    shared_payload = {
        "items": existing_items,
        "strategy": (existing_payload or {}).get("strategy") if isinstance(existing_payload, Mapping) else params.get("strategy", "hybrid"),
    }
    context.shared["last_recommendations"] = shared_payload
    telemetry = {
        "type": "insert_prereq_review",
        "item_id": str(item_id),
        "position": position,
        "reason": reason,
    }
    payload = {
        "items": existing_items,
        "position": position,
        "inserted": new_entry,
        "telemetry": telemetry,
    }
    return _store_payload(action, context, payload, telemetry)


def _execute_adjust_pacing(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    multiplier = params.get("multiplier") or params.get("pace") or 1.0
    try:
        multiplier_value = float(multiplier)
    except (TypeError, ValueError):
        multiplier_value = 1.0
    reason = params.get("reason") or "routine_adjustment"
    horizon = params.get("horizon")
    telemetry = {
        "type": "adjust_pacing",
        "multiplier": multiplier_value,
        "reason": reason,
    }
    if horizon is not None:
        telemetry["horizon"] = horizon
    adjustment_record = {
        "multiplier": multiplier_value,
        "reason": reason,
        "horizon": horizon,
        "telemetry": telemetry,
    }
    pacing_records = context.shared.setdefault("pacing_adjustments", [])
    if isinstance(pacing_records, list):
        pacing_records.append(adjustment_record)
    if hasattr(context, "metadata") and isinstance(context.metadata, MutableMapping):
        history = context.metadata.setdefault("pacing_history", [])  # type: ignore[attr-defined]
        if isinstance(history, list):
            history.append(adjustment_record)
    return _store_payload(action, context, adjustment_record, telemetry)


def _execute_assign_debug_exercise(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    exercise_id = params.get("exercise_id") or params.get("exercise")
    if not exercise_id:
        payload = {"skipped": True, "reason": "missing_exercise"}
        return _store_payload(action, context, payload)

    difficulty = str(params.get("difficulty") or "medium")
    due_date = _parse_due_date(params.get("due_date") or params.get("due"))
    focus = params.get("focus")
    hints = params.get("hints")
    if isinstance(hints, Sequence) and not isinstance(hints, (str, bytes)):
        hint_list = [str(hint) for hint in hints]
    else:
        hint = hints if hints is not None else None
        hint_list = [str(hint)] if hint not in (None, "") else []

    payload = {
        "exercise_id": str(exercise_id),
        "difficulty": difficulty,
        "due_date": due_date.isoformat() if due_date else None,
        "focus": str(focus) if focus not in (None, "") else None,
        "hints": hint_list,
    }
    telemetry = {
        "type": "assign_debug_exercise",
        "status": "assigned",
        "exercise_id": str(exercise_id),
        "difficulty": difficulty,
    }
    if due_date is not None:
        telemetry["due_date"] = due_date.isoformat()
    if payload["focus"]:
        telemetry["focus"] = payload["focus"]
    if hint_list:
        telemetry["hint_count"] = len(hint_list)

    payload["telemetry"] = telemetry
    return _store_payload(action, context, payload, telemetry)


def _execute_suggest_break(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    duration = params.get("duration_minutes") or params.get("duration") or 5
    try:
        duration_minutes = max(1, int(duration))
    except (TypeError, ValueError):
        duration_minutes = 5
    reason = str(params.get("reason") or "wellbeing")
    modality = str(params.get("modality") or "microbreak")
    prompt = params.get("prompt")
    payload = {
        "duration_minutes": duration_minutes,
        "reason": reason,
        "modality": modality,
        "prompt": str(prompt) if prompt not in (None, "") else None,
    }
    telemetry = {
        "type": "suggest_break",
        "duration_minutes": duration_minutes,
        "reason": reason,
        "modality": modality,
    }
    if payload["prompt"]:
        telemetry["prompt_length"] = len(payload["prompt"])
    payload["telemetry"] = telemetry
    return _store_payload(action, context, payload, telemetry)


def _execute_spaced_review(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    raw_items = params.get("items") or params.get("content") or []
    if isinstance(raw_items, Mapping):
        items_source: Sequence[Any] = [raw_items]
    elif isinstance(raw_items, Sequence) and not isinstance(raw_items, (str, bytes)):
        items_source = list(raw_items)
    else:
        items_source = []

    base_interval = params.get("base_interval_minutes") or params.get("interval") or 10
    step_interval = params.get("interval_step_minutes") or params.get("step") or base_interval
    try:
        base_interval_minutes = max(1, int(base_interval))
    except (TypeError, ValueError):
        base_interval_minutes = 10
    try:
        step_interval_minutes = max(1, int(step_interval))
    except (TypeError, ValueError):
        step_interval_minutes = base_interval_minutes

    schedule = []
    for index, item in enumerate(items_source):
        if isinstance(item, Mapping):
            item_id = item.get("item_id") or item.get("id") or item.get("content_id")
            difficulty = item.get("difficulty") or item.get("level") or "medium"
        else:
            item_id = item
            difficulty = "medium"
        if not item_id:
            continue
        entry = {
            "item_id": str(item_id),
            "position": index,
            "review_after_minutes": base_interval_minutes + index * step_interval_minutes,
            "difficulty": str(difficulty),
        }
        schedule.append(entry)

    payload = {
        "base_interval_minutes": base_interval_minutes,
        "interval_step_minutes": step_interval_minutes,
        "schedule": schedule,
    }
    telemetry = {
        "type": "spaced_review",
        "scheduled_items": len(schedule),
        "base_interval_minutes": base_interval_minutes,
        "interval_step_minutes": step_interval_minutes,
    }
    payload["telemetry"] = telemetry
    return _store_payload(action, context, payload, telemetry)


def _execute_show_explanation(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> Mapping[str, Any]:
    params = dict(action.params)
    message = str(params.get("message") or params.get("text") or "")
    tone = str(params.get("tone") or "neutral")
    topics_raw = params.get("topics") or params.get("tags") or []
    if isinstance(topics_raw, Sequence) and not isinstance(topics_raw, (str, bytes)):
        topics = [str(topic) for topic in topics_raw]
    elif topics_raw not in (None, ""):
        topics = [str(topics_raw)]
    else:
        topics = []
    cta = params.get("cta") or params.get("call_to_action")
    payload = {
        "message": message,
        "tone": tone,
        "topics": topics,
        "cta": str(cta) if cta not in (None, "") else None,
    }
    telemetry = {
        "type": "show_explanation",
        "message_length": len(message),
        "tone": tone,
        "topics": topics,
    }
    if payload["cta"]:
        telemetry["cta"] = payload["cta"]
    payload["telemetry"] = telemetry
    return _store_payload(action, context, payload, telemetry)


_EXECUTOR_MAP: Dict[str, Callable[[str, ActionDefinition, ExecutionContext, Optional[int]], Mapping[str, Any]]] = {
    "FETCH_RECOMMENDATIONS": _execute_fetch_recommendations,
    "LOG_IMPRESSIONS": _execute_log_impressions,
    "STORE_PAYLOAD": _execute_store_payload,
    "ASSIGN_ACTIVITY": _execute_assign_activity,
    "INSERT_PREREQ_REVIEW": _execute_insert_prereq_review,
    "ADJUST_PACING": _execute_adjust_pacing,
    "ASSIGN_DEBUG_EXERCISE": _execute_assign_debug_exercise,
    "SUGGEST_BREAK": _execute_suggest_break,
    "SPACED_REVIEW": _execute_spaced_review,
    "SHOW_EXPLANATION": _execute_show_explanation,
}


for _name, _executor in list(_EXECUTOR_MAP.items()):
    lower_name = _name.lower()
    if lower_name not in _EXECUTOR_MAP:
        _EXECUTOR_MAP[lower_name] = _executor


def execute_action(
    routine_name: str,
    action: ActionDefinition,
    context: ExecutionContext,
    seed: Optional[int],
) -> ActionResult:
    executed_at = context.feature_vector.generated_at
    if not action.enabled:
        payload: Mapping[str, Any] = {"skipped": True, "reason": "disabled"}
        deterministic_hash = _hash_payload(routine_name, action, payload, seed)
        return ActionResult(
            routine_name=routine_name,
            action_name=action.name,
            action_type=action.type,
            payload=payload,
            seed=seed,
            deterministic_hash=deterministic_hash,
            executed_at=executed_at,
            error="action_disabled",
        )

    executor = _EXECUTOR_MAP.get(action.type.lower())
    if executor is None:
        payload = {"skipped": True, "reason": "unknown_action"}
        deterministic_hash = _hash_payload(routine_name, action, payload, seed)
        return ActionResult(
            routine_name=routine_name,
            action_name=action.name,
            action_type=action.type,
            payload=payload,
            seed=seed,
            deterministic_hash=deterministic_hash,
            executed_at=executed_at,
            error="unknown_action",
        )

    try:
        payload = executor(routine_name, action, context, seed)
        deterministic_hash = _hash_payload(routine_name, action, payload, seed)
        return ActionResult(
            routine_name=routine_name,
            action_name=action.name,
            action_type=action.type,
            payload=payload,
            seed=seed,
            deterministic_hash=deterministic_hash,
            executed_at=executed_at,
        )
    except Exception as exc:  # pragma: no cover - defensive guard
        context.db.rollback()
        logger.exception(
            "action execution failed",
            extra={"routine": routine_name, "action": action.name},
        )
        payload = {"skipped": True, "reason": "exception"}
        deterministic_hash = _hash_payload(routine_name, action, payload, seed)
        return ActionResult(
            routine_name=routine_name,
            action_name=action.name,
            action_type=action.type,
            payload=payload,
            seed=seed,
            deterministic_hash=deterministic_hash,
            executed_at=executed_at,
            error=str(exc),
        )


__all__ = ["execute_action", "ActionExecutor"]
