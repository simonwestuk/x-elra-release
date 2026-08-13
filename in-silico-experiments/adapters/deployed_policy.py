#!/usr/bin/env python3
"""Deployed X-ELRA controller as an in-silico study policy (Route 2, Option 2).

Runs the *deployed* governance code (deployed/xelra/arl + olm/regulatory,
loaded verbatim from the enclosing x-elra-base repository) inside the verification harness's experiment
protocol, so Studies 1-4, 6 and 7 evaluate the reference implementation itself
rather than the harness re-encoding.

Provenance of the invocation pattern:
  * module loading = analysis_pipeline/scripts/11b_functional_replay.py
    (pure-module technique; that pattern reproduced 349/349 live decisions);
  * cycle order line-validated against xelra/arl/engine.py::run_arl_cycle:
    inject elapsed times -> gated early mode inference (no budget reset)
    -> bounded priority-ordered routine evaluation (first execution wins)
    -> transition_state (mode-change budget reset, 4h idle reset)
    -> check_transition_allowed with mode-only revert;
  * trace fields built by the deployed OLM builders (olm/regulatory.py) and
    the engine's own hash construction (_stable_seed, canonical snapshots),
    replicated verbatim below because engine.py itself imports service-layer
    dependencies (SQLAlchemy/FastAPI) that the studies do not use.

Configuration variants for Study 6 sensitivity never modify deployed/ files:
cooldown scaling rewrites a temporary copy of arl_routines.yaml; budget and
dwell variants parameterise the adapter's faithful re-statement of the
corresponding deployed constant (defaults reproduce deployed behaviour
bit-for-bit; the deployed code path is used whenever no override is set).
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import time
import types
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # in-silico-experiments/
DEPLOYED_ROOT = ROOT.parent             # the enclosing x-elra-base repository

_PURE_ARL = ("schemas", "conditions", "boundedness", "mode_inference",
             "controller_state", "dsl")


def load_deployed(root: Path = DEPLOYED_ROOT):
    """Copy the dependency-free deployed modules into package `dxelra`.

    Renamed package avoids colliding with the harness package `xelra`;
    olm/regulatory.py is included so the deployed trace-field builders
    (context summary, inputs-used, exit conditions, OLM projection) run
    verbatim.
    """
    if "dxelra.arl.mode_inference" in sys.modules:
        return
    pkg = Path(tempfile.mkdtemp(prefix="dxelra_")) / "pkg"
    (pkg / "dxelra" / "arl").mkdir(parents=True)
    (pkg / "dxelra" / "olm").mkdir(parents=True)
    (pkg / "dxelra" / "__init__.py").write_text("")
    (pkg / "dxelra" / "arl" / "__init__.py").write_text("")
    (pkg / "dxelra" / "olm" / "__init__.py").write_text("")
    for m in _PURE_ARL:
        shutil.copy(root / "xelra" / "arl" / f"{m}.py", pkg / "dxelra" / "arl" / f"{m}.py")
    shutil.copy(root / "xelra" / "olm" / "regulatory.py", pkg / "dxelra" / "olm" / "regulatory.py")
    sys.path.insert(0, str(pkg))


load_deployed()

from dxelra.arl import dsl as ddsl                                   # noqa: E402
from dxelra.arl.controller_state import (ControllerState,            # noqa: E402
                                         ControllerMode)
from dxelra.arl.boundedness import (_get_permitted_modes,            # noqa: E402
                                    _get_resource_costs,
                                    check_routine_permitted,
                                    consume_routine_resources,
                                    check_transition_allowed)
from dxelra.arl.conditions import evaluate_routine_conditions        # noqa: E402
from dxelra.arl.mode_inference import infer_mode, transition_state   # noqa: E402
from dxelra.olm.regulatory import (build_learner_facing_projection,  # noqa: E402
                                   build_context_summary,
                                   build_inputs_used_summary,
                                   compute_next_transition_conditions)

DEPLOYED_YAML = DEPLOYED_ROOT / "config" / "arl_routines.yaml"
T0 = datetime(2026, 3, 10, 9, 0, 0, tzinfo=timezone.utc)

# ---------------------------------------------------------------------------
# Engine hash helpers, replicated verbatim from xelra/arl/engine.py
# (_canonicalize_value, _build_canonical_snapshots, _serialize_for_hash,
#  _stable_seed, _build_trace_id). engine.py cannot be imported pure.
# ---------------------------------------------------------------------------


def _canonicalize_value(value):
    if isinstance(value, dict):
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


def _build_canonical_snapshots(items):
    snapshots = []
    for rank, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        snapshots.append({
            "item_id": str(item.get("item_id", "")),
            "rank": int(item.get("rank", rank)),
            "score": _canonicalize_value(item.get("score", 0.0)),
            "features": {},
            "weights": {},
        })
    return snapshots


def _serialize_for_hash(snapshots, seed_value):
    payload = {"seed": _canonicalize_value(seed_value),
               "items": [s for s in snapshots]}
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _stable_seed(*parts):
    material = "::".join(str(part) for part in parts)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def _sha256_canonical(payload) -> str:
    canonical = _canonicalize_value(payload)
    serialized = json.dumps(canonical, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Harness perception -> deployed FeatureVector
# ---------------------------------------------------------------------------


def fv_from_step(perc, cands, t_minutes, learner_id="L"):
    md = {
        "clicks_last_14_days": int(perc.get("clicks_14d", 0)),
        "completions_last_7_days": int(perc.get("recent_completions", 0)),
        "days_since_last_engagement": float(perc.get("days_since_engagement", 0.0)),
        "impressions_last_30_days": int(perc.get("impressions", 0)),
        "active_goal_count": 1 if perc.get("active_goals") else 0,
        "progress_rate": float(perc.get("progress_rate", 0.0)),
        "feature_gap": int(perc.get("feature_gap", 0)),
        "confusion_flag": bool(perc.get("confusion_flag", False)),
        "frustration_flag": bool(perc.get("frustration_flag", False)),
        "mastery_count": int(perc.get("mastery_count", 0)),
    }
    mastery = {"s_low": float(perc.get("lowest_mastery", 0.0)),
               "s_high": float(perc.get("highest_mastery", 0.0)),
               "s_mean": float(perc.get("mean_mastery", 0.0))}
    if not perc.get("has_mastery", True):
        mastery = {}
    recs = [{"item_id": c.get("action_id", f"r{k}"), "score": float(c.get("score", 0.0)),
             "source": c.get("source", "hybrid_recommender"), "action_type": "recommend"}
            for k, c in enumerate(cands)]
    return types.SimpleNamespace(
        learner_id=learner_id, mastery=mastery,
        goals=([{"id": "g1"}] if perc.get("active_goals") else []),
        impressions=[], clicks=[], completions=[], recommendations=recs,
        metadata=md, generated_at=T0 + timedelta(minutes=float(t_minutes)))


def fv_to_dict(fv):
    """Canonical serialisation of the adapter FeatureVector (replay inputs)."""
    return {
        "learner_id": fv.learner_id,
        "mastery": dict(fv.mastery),
        "goals": list(fv.goals),
        "recommendations": list(fv.recommendations),
        "metadata": dict(fv.metadata),
        "generated_at": fv.generated_at.isoformat(),
    }


# ---------------------------------------------------------------------------
# Configuration variants (Study 6 / Study 4) - deployed/ files never modified
# ---------------------------------------------------------------------------


def make_scaled_bundle_path(cooldown_scale: float) -> str:
    """Temp copy of the deployed YAML with cooldown_seconds scaled."""
    raw = yaml.safe_load(open(DEPLOYED_YAML, encoding="utf-8"))
    for r in raw.get("routines", []):
        r["cooldown_seconds"] = int(round(float(r.get("cooldown_seconds", 0))
                                          * cooldown_scale))
    tmp = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                      prefix=f"arl_cd{cooldown_scale}_")
    yaml.safe_dump(raw, tmp)
    tmp.close()
    return tmp.name


def make_padded_bundle_path(n_routines: int) -> str:
    """Temp copy of the deployed YAML inflated with inert routines.

    Padding routines are permitted only in cold_start (SKIPPED on mode
    mismatch in the active mode), mirroring the harness Study-4 padding
    method: the per-routine evaluation loop and trace-path construction are
    exercised without changing any decision.
    """
    raw = yaml.safe_load(open(DEPLOYED_YAML, encoding="utf-8"))
    extra = max(0, n_routines - len(raw.get("routines", [])))
    for i in range(extra):
        # High priority so every padding routine is traversed (and SKIPPED on
        # mode mismatch) before the first executing routine terminates the loop.
        raw["routines"].append({
            "id": f"PAD{i:03d}", "title": f"pad {i}", "priority": 1000 - i,
            "enabled": True, "permitted_modes": ["cold_start"],
            "conditions": {"all": ["feature_vector.metadata.impressions_last_30_days >= 0"]},
            "actions": [{"name": f"pad_log_{i}", "type": "log_impressions",
                         "params": {}}],
            "explanation": "inert latency padding (cold_start only)",
            "resource_costs": {}, "cooldown_seconds": 0,
        })
    tmp = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False,
                                      prefix=f"arl_pad{n_routines}_")
    yaml.safe_dump(raw, tmp)
    tmp.close()
    return tmp.name


# ---------------------------------------------------------------------------
# The policy
# ---------------------------------------------------------------------------


class DeployedARLPolicy:
    """Deployed governance cycle over the harness stream protocol.

    Defaults reproduce the deployed controller exactly (deployed functions and
    deployed constants on every code path). Overrides exist solely for the
    Study-6 sensitivity sweep and are faithful parameterisations of the
    corresponding deployed constant:
      budget_interventions/_suggestions: capacity applied wherever the deployed
        cycle installs fresh budgets (init, mode-change reset, 4h idle reset);
      dwell_seconds: tau_dwell in the transition check (deployed constant 300);
      bundle_path: alternative routine YAML (e.g. cooldown-scaled temp copy).
    """

    name = "ARL_dep"

    def __init__(self, bundle_path=None, budget_interventions=None,
                 budget_suggestions=None, dwell_seconds=None,
                 dwell_anchor="deployed", emit_traces=False):
        self.bundle = ddsl.load_routine_bundle(str(bundle_path or DEPLOYED_YAML))
        self.bi = budget_interventions
        self.bs = budget_suggestions
        self.dwell = dwell_seconds
        self.dwell_anchor = dwell_anchor   # "deployed" | "entry" (counterfactual)
        self.emit_traces = emit_traces
        self.last_decide_us = None       # wall-clock of last decide() core
        self.last_trace_bytes = None

    # -- deployed constants, parameterised only when an override is set -----
    #
    # dwell_anchor="deployed" (default): the deployed check compares against
    # timers.last_mode_transition, which transition_state refreshes even when
    # the transition is subsequently blocked -- under persistently
    # contradictory inference at sub-dwell cadence the mode therefore
    # latches. dwell_anchor="entry" is a mechanism-isolation COUNTERFACTUAL
    # (not deployed behaviour): dwell measured from when the current mode was
    # entered, the anchoring the harness uses.

    def _transition_allowed(self, old_mode, new_mode, cs, now):
        if self.dwell_anchor == "entry":
            if old_mode == new_mode:
                return True, None
            iso = cs.metadata.get("mode_entered_at_sim")
            if iso is None:
                return True, None
            elapsed = (now - datetime.fromisoformat(iso)).total_seconds()
            tau = self.dwell if self.dwell is not None else 300
            if elapsed < tau:
                return False, f"mode_entry_too_recent: {elapsed:.0f}s < {tau:.0f}s"
            return True, None
        if self.dwell is None:
            return check_transition_allowed(old_mode, new_mode, cs.timers, now=now)
        # verbatim restatement of boundedness.check_transition_allowed with
        # MIN_MODE_DURATION_SECONDS parameterised (deployed value 300)
        if old_mode == new_mode:
            return True, None
        if cs.timers.last_mode_transition is None:
            return True, None
        elapsed = (now - cs.timers.last_mode_transition).total_seconds()
        if elapsed < self.dwell:
            return False, f"mode_transition_too_soon: {elapsed:.0f}s < {self.dwell:.0f}s"
        return True, None

    def _apply_budget_capacity(self, new_cs, old_cs, mode_changed):
        if self.bi is None and self.bs is None:
            return
        bi = self.bi if self.bi is not None else 5
        bs = self.bs if self.bs is not None else 10
        if mode_changed:
            # transition_state installed ControllerBudgets() (full capacity)
            new_cs.budgets.interventions_remaining = bi
            new_cs.budgets.suggestions_remaining = bs
        elif (new_cs.metadata.get("session_resets", 0)
              != old_cs.metadata.get("session_resets", 0)):
            # 4h idle reset restored interventions to deployed capacity 5
            new_cs.budgets.interventions_remaining = bi

    # -- state ---------------------------------------------------------------

    def init_state(self, stream, learner_id="L"):
        t0, perc0, cands0 = stream[0]
        fv0 = fv_from_step(perc0, cands0, t0, learner_id)
        cs = ControllerState(learner_id=learner_id)
        cs.timers.session_start = fv0.generated_at   # pin simulated clock
        cs.updated_at = fv0.generated_at
        cs.mode = infer_mode(fv0, cs)
        if self.dwell_anchor == "entry":
            cs.metadata["mode_entered_at_sim"] = fv0.generated_at.isoformat()
        if self.bi is not None:
            cs.budgets.interventions_remaining = self.bi
        if self.bs is not None:
            cs.budgets.suggestions_remaining = self.bs
        return cs

    # -- one decision cycle (engine.run_arl_cycle order) --------------------

    def decide(self, cs, fv, learner_id="L"):
        """Run one governance cycle; returns (record, new_cs).

        record keys: mode, executed, intervened, action, mode_transition,
        trace (None unless emit_traces), path.
        """
        now = fv.generated_at
        prev_mode = cs.mode
        t_start = time.perf_counter()

        # engine._inject_elapsed_times (before inference)
        if cs.timers.last_intervention is not None:
            cs.metadata["time_since_last_intervention_seconds"] = \
                (now - cs.timers.last_intervention).total_seconds()
        if cs.timers.last_mode_transition is not None:
            cs.metadata["time_since_last_mode_transition_seconds"] = \
                (now - cs.timers.last_mode_transition).total_seconds()
        esr = {rn: (now - te).total_seconds()
               for rn, te in cs.timers.last_routine_executed.items()}
        if esr:
            cs.metadata["elapsed_since_routine_seconds"] = esr

        # Phase 1: early inference with dwell/oscillation gating (no budget reset)
        inferred = infer_mode(fv, cs)
        if inferred != cs.mode:
            ok, _ = self._transition_allowed(cs.mode, inferred, cs, now)
            if ok:
                cs.mode = inferred
                cs.timers.last_mode_transition = now
                cs.recent_outcomes.record_transition(now=now)
                cs.metadata["mode_transition_count"] = \
                    cs.metadata.get("mode_transition_count", 0) + 1
                if self.dwell_anchor == "entry":
                    cs.metadata["mode_entered_at_sim"] = now.isoformat()

        # engine snapshots S_t after early inference, before routine evaluation
        state_before = copy.deepcopy(cs) if self.emit_traces else None

        # Phase 2: bounded priority-ordered evaluation, first execution wins
        executed = None
        path = []
        for routine in self.bundle.routines:
            if not routine.enabled:
                continue
            pm = _get_permitted_modes(routine)
            if pm and cs.mode not in pm:
                path.append({"routine_name": routine.name, "outcome": "SKIPPED",
                             "reason": "mode_mismatch"})
                continue
            ctx = types.SimpleNamespace(feature_vector=fv, controller_state=cs,
                                        learner_id=learner_id, shared={},
                                        bundle=self.bundle, logger=None, metrics=None)
            if not evaluate_routine_conditions(routine.conditions, ctx):
                path.append({"routine_name": routine.name, "outcome": "SKIPPED",
                             "reason": "conditions_not_met"})
                continue
            ok, reason = check_routine_permitted(routine, cs, now=now)
            if not ok:
                path.append({"routine_name": routine.name, "outcome": "SKIPPED",
                             "reason": reason or "bounded"})
                continue
            consume_routine_resources(routine, cs)
            cs.timers.mark_execution(routine.name, now=now)
            path.append({"routine_name": routine.name, "outcome": "EXECUTED_ACTION",
                         "reason": "triggers_met_and_bounded"})
            executed = routine
            break

        exec_name = executed.name if executed else "NO_ACTION"
        costs = _get_resource_costs(executed) if executed else {}
        intervened = bool(costs.get("interventions", 0) > 0)

        # Phase 4/6: deployed transition_state + gated adoption (mode-only revert)
        new_cs = transition_state(cs, exec_name, fv)
        mode_changed = new_cs.mode != cs.mode
        if mode_changed:
            ok, _ = self._transition_allowed(cs.mode, new_cs.mode, cs, now)
            if not ok:
                new_cs.mode = cs.mode
                mode_changed = False
            elif self.dwell_anchor == "entry":
                new_cs.metadata["mode_entered_at_sim"] = now.isoformat()
        self._apply_budget_capacity(new_cs, cs, mode_changed)

        self.last_decide_us = (time.perf_counter() - t_start) * 1e6

        trace = None
        if self.emit_traces:
            trace = self._build_trace(state_before, new_cs, fv, path, executed,
                                      exec_name, learner_id)
        return ({"mode": new_cs.mode.value.upper(), "executed": exec_name,
                 "intervened": intervened,
                 "action": (executed.actions[0].name
                            if executed and executed.actions else None),
                 "mode_transition": (f"{prev_mode.value.upper()}->{new_cs.mode.value.upper()}"
                                     if new_cs.mode != prev_mode else None),
                 "path": path, "trace": trace},
                new_cs)

    # -- decision trace (deployed record shape; fields built by deployed code)

    def _build_trace(self, state_before, state_after, fv, path, executed,
                     exec_name, learner_id):
        cycle_seed = _stable_seed(learner_id, self.bundle.version,
                                  fv.generated_at.isoformat())
        # Emulated action-selection ordering: the deployed merge sorts
        # candidates by (-score, item_id) before selection (state.py); items
        # appear only when the executed routine fetches recommendations.
        items = []
        if executed and any("fetch" in (a.type or "") for a in executed.actions):
            ordered = sorted(fv.recommendations,
                             key=lambda c: (-float(c.get("score", 0.0)),
                                            str(c.get("item_id", ""))))
            items = [{"item_id": c["item_id"], "rank": i, "score": c["score"]}
                     for i, c in enumerate(ordered)]
        deterministic_hash = hashlib.sha256(
            _serialize_for_hash(_build_canonical_snapshots(items),
                                cycle_seed).encode("utf-8")).hexdigest()
        fvd = fv_to_dict(fv)
        trace_id = _sha256_canonical({
            "routine_version": self.bundle.version,
            "state_before": state_before.to_dict(),
            "inputs": fvd,
            "routine_path": path,
        })
        return {
            "trace_id": trace_id,
            "deterministic_hash": deterministic_hash,
            "seed": cycle_seed,
            "timestamp": fv.generated_at.isoformat(),
            "routines_version": self.bundle.version,
            "context_summary": build_context_summary(fv),
            "state_before": state_before.to_trace_dict(),
            "inputs_used": build_inputs_used_summary(fv, []),
            "routine_path": path,
            "decision": {"action": (executed.actions[0].name
                                    if executed and executed.actions else None),
                         "source_routine": (executed.name if executed else None),
                         "executed": exec_name},
            "state_after": state_after.to_trace_dict(),
            "next_transition_conditions":
                compute_next_transition_conditions(state_after, fv.metadata),
            "olm_projection": build_learner_facing_projection(
                state_after, fv.metadata, fv),
            "replay_inputs": fvd,
            "state_before_full": state_before.to_dict(),
        }

    # -- harness protocol ----------------------------------------------------

    def run(self, stream, learner_id="L"):
        from sim.baselines import StepResult
        cs = self.init_state(stream, learner_id)
        out = []
        for (t, perc, cands) in stream:
            fv = fv_from_step(perc, cands, t, learner_id)
            prev = cs.mode
            rec, cs = self.decide(cs, fv, learner_id)
            out.append(StepResult(
                t=t, stance=rec["mode"], intervened=rec["intervened"],
                is_bounded=rec["intervened"], action=rec["action"],
                log_record=(rec["trace"] if self.emit_traces else {}),
                trace=rec["trace"],
                mode_transition=rec["mode_transition"]))
        return out
