"""Core dataclasses shared across the ARL runtime."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence
import json

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


@dataclass(frozen=True)
class FeatureVector:
    """
    Snapshot of learner state used for control routine evaluation.

    Represents perception inputs I_t from heterogeneous ML models and telemetry.
    This is distinct from controller state S_t - FeatureVector captures WHAT the
    learner is doing, while ControllerState captures HOW the system is regulating.
    """

    learner_id: str
    mastery: Mapping[str, float]
    goals: Sequence[Mapping[str, Any]]
    impressions: Sequence[Mapping[str, Any]]
    clicks: Sequence[Mapping[str, Any]]
    completions: Sequence[Mapping[str, Any]]
    recommendations: Sequence[Mapping[str, Any]]
    metadata: Mapping[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["generated_at"] = self.generated_at.strftime(ISO_FORMAT)
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "FeatureVector":
        generated = payload.get("generated_at")
        if isinstance(generated, str):
            try:
                generated_at = datetime.strptime(generated, ISO_FORMAT).replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                generated_at = datetime.fromisoformat(
                    generated.replace("Z", "+00:00")
                ).astimezone(timezone.utc)
        elif isinstance(generated, datetime):
            generated_at = (
                generated.replace(tzinfo=timezone.utc)
                if generated.tzinfo is None
                else generated.astimezone(timezone.utc)
            )
        else:
            generated_at = datetime.now(timezone.utc)
        return cls(
            learner_id=str(payload.get("learner_id", "")),
            mastery=dict(payload.get("mastery", {})),
            goals=list(payload.get("goals", [])),
            impressions=list(payload.get("impressions", [])),
            clicks=list(payload.get("clicks", [])),
            completions=list(payload.get("completions", [])),
            recommendations=list(payload.get("recommendations", [])),
            metadata=dict(payload.get("metadata", {})),
            generated_at=generated_at,
        )

    @classmethod
    def from_json(cls, raw: str) -> "FeatureVector":
        return cls.from_dict(json.loads(raw))


@dataclass(frozen=True)
class ActionDefinition:
    name: str
    type: str
    params: Mapping[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass(frozen=True)
class RoutineDefinition:
    """
    Control routine specification (element of R_t).

    Represents an explicit, inspectable decision module with:
    - Trigger conditions: When the routine should activate
    - Priority: Conflict resolution order (higher = evaluated first)
    - Actions: What to do if conditions are met
    - Boundedness: Mode permissions, cooldowns, resource costs
    - Explanation: Learner-facing rationale

    Control routines are declarative - they don't execute directly.
    The controller evaluates them and may execute, skip, or block them.
    """
    name: str
    priority: int
    conditions: Mapping[str, Any]
    actions: Sequence[ActionDefinition]
    explanation: str
    seed: Optional[int] = None
    description: Optional[str] = None
    enabled: bool = True
    tags: Sequence[str] = field(default_factory=list)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    # Boundedness constraints (Section 4.3, Table 3)
    permitted_modes: Sequence[str] = field(default_factory=tuple)
    cooldown_seconds: Optional[int] = None
    resource_costs: Mapping[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class RoutineBundle:
    version: str
    schema_version: str
    routines: Sequence[RoutineDefinition]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def enabled_routines(self) -> Iterable[RoutineDefinition]:
        return (routine for routine in self.routines if routine.enabled)


@dataclass
class ActionResult:
    routine_name: str
    action_name: str
    action_type: str
    payload: Mapping[str, Any]
    seed: Optional[int]
    deterministic_hash: str
    executed_at: datetime
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "routine_name": self.routine_name,
            "action_name": self.action_name,
            "action_type": self.action_type,
            "payload": self.payload,
            "seed": self.seed,
            "deterministic_hash": self.deterministic_hash,
            "executed_at": self.executed_at.strftime(ISO_FORMAT),
            "error": self.error,
        }


@dataclass
class RoutineResult:
    """
    Routine evaluation outcome per Section 4.3.

    Outcome values (Section 4.3):
    - SKIPPED: ineligible (unmet triggers, mode mismatch)
    - BLOCKED: eligible but prevented by boundedness (budget, cooldown, stability, quotas)
    - EXECUTED_ACTION: routine executes and selects action A_t
    - EXECUTED_NO_ACTION: routine executes and selects deliberate non-intervention (∅)

    Convention: effect = NONE when outcome ∈ {SKIPPED, BLOCKED}
    """
    routine: RoutineDefinition
    seed: Optional[int]
    actions: List[ActionResult] = field(default_factory=list)
    skipped: bool = False
    error: Optional[str] = None
    skip_reason: Optional[str] = None
    # NEW: Explicit outcome field per Section 4.3
    outcome: Optional[str] = None  # SKIPPED | BLOCKED | EXECUTED_ACTION | EXECUTED_NO_ACTION
    mode_transition: Optional[str] = None  # Mode change if routine executed
    stop_evaluation: bool = False  # Whether routine terminated further evaluation

    def to_dict(self) -> Dict[str, Any]:
        routine_payload: Dict[str, Any] = {
            "id": self.routine.name,
            "name": self.routine.name,
            "title": self.routine.description or self.routine.name,
            "priority": self.routine.priority,
            "enabled": self.routine.enabled,
            "tags": list(self.routine.tags),
            "metadata": dict(self.routine.metadata),
            "explanation": self.routine.explanation,
        }
        if self.routine.description:
            routine_payload["description"] = self.routine.description

        result_dict = {
            "routine": routine_payload,
            "routine_name": self.routine.name,
            "seed": self.seed,
            "skipped": self.skipped,
            "error": self.error,
            "skip_reason": self.skip_reason,
            "actions": [action.to_dict() for action in self.actions],
        }

        # Add Section 4.4 trace fields for routine_path
        if self.outcome:
            result_dict["outcome"] = self.outcome
            result_dict["reason"] = self.skip_reason or self.error or "triggers_met_and_bounded"
        if self.mode_transition:
            result_dict["mode_transition"] = self.mode_transition
        if self.stop_evaluation:
            result_dict["stop_evaluation"] = self.stop_evaluation

        return result_dict

    def to_trace_dict(self) -> Dict[str, Any]:
        """Compact serialization for the decision trace routine_path (Appendix A.3).

        Returns ``{routine_id, outcome, reason, mode_transition, action_selected,
        terminated_evaluation}`` per the formal schema.  The routine version is
        captured at the trace level in ``routines_version``, not per-entry.
        """
        entry: Dict[str, Any] = {
            "routine_id": self.routine.name,
            "outcome": self.outcome or ("SKIPPED" if self.skipped else "EXECUTED_ACTION"),
            "reason": self.skip_reason or self.error or "triggers_met_and_bounded",
            "mode_transition": self.mode_transition,
            "action_selected": self.actions[0].action_name if self.actions else None,
            "terminated_evaluation": self.stop_evaluation,
        }
        return entry


@dataclass
class EvaluationJob:
    job_id: str
    learner_id: str
    routine_names: Sequence[str]
    scheduled_for: datetime
    trigger: str
    payload: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "learner_id": self.learner_id,
            "routine_names": list(self.routine_names),
            "scheduled_for": self.scheduled_for.strftime(ISO_FORMAT),
            "trigger": self.trigger,
            "payload": self.payload,
        }


@dataclass
class ARLCycleResult:
    """
    Decision trace T_t for ARL cycle.

    Follows the formal DecisionTrace schema from Section 4.4:
    - trace_id (decision_id): deterministic identifier
    - context_summary: task/topic/session phase
    - inputs_used: references to O_t and C_t fields used by routines
    - state_before (controller_state_before): mode, budgets, cooldowns, stability counters
    - routine_path: ordered routine evaluation outcomes, including skip reasons
    - decision: selected action A_t or deliberate non-intervention ∅
    - state_after (controller_state_after): updated mode, budgets, cooldowns
    - next_transition_conditions: explicit conditions monitored for exit/transition
    - learner_facing_fields: mode label, "why", "what next", exit conditions
    - routine_versions (routine_version): routine set version identifiers for replay
    """
    learner_id: str
    decision_id: str  # trace_id
    deterministic_hash: str
    routine_version: str  # routine_versions
    seed: Optional[int]
    feature_vector: FeatureVector  # I_t
    routine_results: Sequence[RoutineResult]  # routine_path
    explanations: Sequence[Mapping[str, Any]]
    telemetry_events: Sequence[Mapping[str, Any]]
    evaluation_job: Optional[EvaluationJob] = None
    active_routines: Sequence[str] = field(default_factory=tuple)
    controller_state_before: Any = None  # state_before: S_t
    controller_state_after: Any = None  # state_after: S_{t+1}

    # NEW: Additional trace fields per Section 4.4
    context_summary: Optional[Mapping[str, Any]] = None  # task/topic/session phase
    inputs_used: Optional[Mapping[str, Any]] = None  # references to O_t and C_t fields
    decision: Optional[Mapping[str, Any]] = None  # Appendix A.3: {action, source_routine} or {null, null} (∅)
    evaluation_terminated: bool = False  # Whether routine evaluation was stopped early
    terminated_by: Optional[str] = None  # routine_id that stopped evaluation
    next_transition_conditions: Optional[Sequence[Mapping[str, Any]]] = None  # exit conditions
    learner_facing_fields: Optional[Mapping[str, Any]] = None  # OLM projection

    # Compact decision trace aligned with the minimal DecisionTrace T_t schema
    decision_trace: Optional[Mapping[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "learner_id": self.learner_id,
            "decision_id": self.decision_id,
            "deterministic_hash": self.deterministic_hash,
            "routine_version": self.routine_version,
            "seed": self.seed,
            "feature_vector": self.feature_vector.to_dict(),
            "routine_results": [r.to_dict() for r in self.routine_results],
            "explanations": list(self.explanations),
            "telemetry_events": list(self.telemetry_events),
            "evaluation_job": self.evaluation_job.to_dict()
            if self.evaluation_job
            else None,
            "active_routines": list(self.active_routines),
        }
        if self.controller_state_before is not None:
            result["controller_state_before"] = self.controller_state_before.to_dict()
        if self.controller_state_after is not None:
            result["controller_state_after"] = self.controller_state_after.to_dict()
        # NEW: Add trace fields per Section 4.4
        if self.context_summary is not None:
            result["context_summary"] = dict(self.context_summary)
        if self.inputs_used is not None:
            result["inputs_used"] = dict(self.inputs_used)
        if self.decision is not None:
            result["decision"] = dict(self.decision) if isinstance(self.decision, Mapping) else self.decision
        result["evaluation_terminated"] = self.evaluation_terminated
        if self.terminated_by is not None:
            result["terminated_by"] = self.terminated_by
        if self.next_transition_conditions is not None:
            result["next_transition_conditions"] = [dict(c) for c in self.next_transition_conditions]
        if self.learner_facing_fields is not None:
            result["learner_facing_fields"] = dict(self.learner_facing_fields)
        if self.decision_trace is not None:
            result["decision_trace"] = dict(self.decision_trace)
        return result


@dataclass
class ExecutionContext:
    learner_id: str
    feature_vector: FeatureVector
    db: Any
    logger: Any
    metrics: Any
    tracer: Any
    shared: MutableMapping[str, Any]
    request_id: str
    routine_version: str
    bundle: RoutineBundle
    cycle_seed: Optional[int]
    controller_state: Any = None  # ControllerState from controller_state module
    arm: Optional[str] = None
    metadata: MutableMapping[str, Any] = field(default_factory=dict)
