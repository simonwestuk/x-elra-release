"""Controller state (S_t) for formal ARL implementation (Paper Section 3.1).

This module implements the explicit controller state required by the formal
ARL definition, maintaining operational context separate from learner perceptions.

Key concepts from the paper:
- S_t represents the controller's internal operational state at time t
- S_t is separate from learner perceptions (I_t) - maintains regulatory context
- S_t includes: current mode, resource budgets, cooldown timers, recent outcomes
- S_t persists across cycles and governs which actions are permitted
- S_{t+1} = transition_state(S_t, A_t, I_t) - deterministic evolution
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional


class ControllerMode(str, Enum):
    """Operational modes that gate available actions."""

    COLD_START = "cold_start"  # New learner, no telemetry
    ORIENTATION = "orientation"  # Initial pathway
    NOMINAL = "nominal"  # Normal operation
    STRUGGLING = "struggling"  # Low mastery + no engagement
    LAPSED = "lapsed"  # >15 days inactive (Table 4)
    ACCELERATING = "accelerating"  # High progress rate
    CONSOLIDATING = "consolidating"  # High mastery, practice mode
    DIAGNOSTIC = "diagnostic"  # Data integrity issues
    COOLDOWN = "cooldown"  # Post-intervention rest


@dataclass
class ControllerBudgets:
    """Resource budgets preventing over-intervention."""

    interventions_remaining: int = 5  # Max interventions per session
    suggestions_remaining: int = 10  # Max suggestions per week

    def consume(self, resource: str, amount: int = 1) -> bool:
        """Attempt to consume budget. Returns True if successful."""
        attr_name = f"{resource}_remaining"
        if not hasattr(self, attr_name):
            return True  # Unknown resource, allow by default
        current = getattr(self, attr_name)
        if current < amount:
            return False
        setattr(self, attr_name, current - amount)
        return True

    def reset(self, resource: str, value: int):
        """Reset a specific budget."""
        setattr(self, f"{resource}_remaining", value)

    def to_dict(self) -> Dict[str, int]:
        """Serialize budgets."""
        return {
            "interventions_remaining": self.interventions_remaining,
            "suggestions_remaining": self.suggestions_remaining,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ControllerBudgets:
        """Deserialize budgets."""
        return cls(
            interventions_remaining=data.get("interventions_remaining", 5),
            suggestions_remaining=data.get("suggestions_remaining", 10),
        )


@dataclass
class ControllerTimers:
    """Cooldown timers preventing oscillation."""

    last_intervention: Optional[datetime] = None
    last_mode_transition: Optional[datetime] = None
    last_routine_executed: Dict[str, datetime] = field(default_factory=dict)
    session_start: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def cooldown_active(
        self,
        routine_name: str,
        cooldown_seconds: int,
        *,
        now: Optional[datetime] = None,
    ) -> bool:
        """Check if routine is in cooldown period."""
        if now is None:
            now = datetime.now(timezone.utc)
        last_exec = self.last_routine_executed.get(routine_name)
        if last_exec is None:
            return False
        elapsed = (now - last_exec).total_seconds()
        return elapsed < cooldown_seconds

    def mark_execution(self, routine_name: str, *, now: Optional[datetime] = None):
        """Record routine execution timestamp."""
        if now is None:
            now = datetime.now(timezone.utc)
        self.last_routine_executed[routine_name] = now
        self.last_intervention = now

    def to_dict(self) -> Dict[str, Any]:
        """Serialize timers."""
        return {
            "last_intervention": self.last_intervention.isoformat()
            if self.last_intervention
            else None,
            "last_mode_transition": self.last_mode_transition.isoformat()
            if self.last_mode_transition
            else None,
            "last_routine_executed": {
                k: v.isoformat() for k, v in self.last_routine_executed.items()
            },
            "session_start": self.session_start.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ControllerTimers:
        """Deserialize timers."""
        return cls(
            last_intervention=datetime.fromisoformat(data["last_intervention"])
            if data.get("last_intervention")
            else None,
            last_mode_transition=datetime.fromisoformat(data["last_mode_transition"])
            if data.get("last_mode_transition")
            else None,
            last_routine_executed={
                k: datetime.fromisoformat(v)
                for k, v in data.get("last_routine_executed", {}).items()
            },
            session_start=datetime.fromisoformat(
                data.get("session_start", datetime.now(timezone.utc).isoformat())
            ),
        )


@dataclass
class RecentOutcomes:
    """Sliding window of recent decisions and mode transitions (Appendix B.2)."""

    decision_history: List[str] = field(default_factory=list)  # Last N routine names
    transition_times: List[float] = field(default_factory=list)  # UTC timestamps of mode transitions (Appendix B.2)
    max_history: int = 10

    def append(self, routine_name: str):
        """Add decision to history, maintaining window size."""
        self.decision_history.append(routine_name)
        if len(self.decision_history) > self.max_history:
            self.decision_history.pop(0)

    def record_transition(self, *, now: Optional[datetime] = None):
        """Record a mode transition timestamp for oscillation detection (Appendix B.2)."""
        if now is None:
            now = datetime.now(timezone.utc)
        self.transition_times.append(now.timestamp())
        # Keep only recent transitions (last 30 minutes worth, with margin)
        if len(self.transition_times) > self.max_history:
            self.transition_times.pop(0)

    def detect_oscillation(self, pattern_length: int = 3) -> bool:
        """Detect A->B->A->B routine name repetition patterns (legacy)."""
        if len(self.decision_history) < pattern_length * 2:
            return False

        recent = self.decision_history[-(pattern_length * 2) :]
        first_half = recent[:pattern_length]
        second_half = recent[pattern_length:]
        return first_half == second_half

    def to_dict(self) -> Dict[str, Any]:
        """Serialize recent outcomes."""
        return {
            "decision_history": self.decision_history,
            "transition_times": self.transition_times,
            "max_history": self.max_history,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> RecentOutcomes:
        """Deserialize recent outcomes."""
        return cls(
            decision_history=list(data.get("decision_history", [])),
            transition_times=list(data.get("transition_times", [])),
            max_history=data.get("max_history", 10),
        )


@dataclass
class ControllerState:
    """
    Explicit controller state S_t maintaining operational context
    separate from learner perceptions.

    This state persists across cycles and governs which actions
    are permitted through modes, budgets, and timers.
    """

    learner_id: str
    mode: ControllerMode = ControllerMode.NOMINAL
    budgets: ControllerBudgets = field(default_factory=ControllerBudgets)
    timers: ControllerTimers = field(default_factory=ControllerTimers)
    recent_outcomes: RecentOutcomes = field(default_factory=RecentOutcomes)
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for persistence."""
        return {
            "learner_id": self.learner_id,
            "mode": self.mode.value,
            "budgets": self.budgets.to_dict(),
            "timers": self.timers.to_dict(),
            "recent_outcomes": self.recent_outcomes.to_dict(),
            "metadata": self.metadata,
            "version": self.version,
            "updated_at": self.updated_at.isoformat(),
        }

    def to_trace_dict(self) -> Dict[str, Any]:
        """Compact serialization for the decision trace (mode + budgets + cooldowns only)."""
        cooldowns: Dict[str, str] = {
            k: v.isoformat() for k, v in self.timers.last_routine_executed.items()
        }
        return {
            "mode": self.mode.value,
            "budgets": self.budgets.to_dict(),
            "cooldowns": cooldowns,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ControllerState:
        """Deserialize from storage."""
        mode = ControllerMode(data.get("mode", "nominal"))
        budgets = ControllerBudgets.from_dict(data.get("budgets", {}))
        timers = ControllerTimers.from_dict(data.get("timers", {}))
        outcomes = RecentOutcomes.from_dict(data.get("recent_outcomes", {}))

        return cls(
            learner_id=data["learner_id"],
            mode=mode,
            budgets=budgets,
            timers=timers,
            recent_outcomes=outcomes,
            metadata=dict(data.get("metadata", {})),
            version=data.get("version", "1.0.0"),
            updated_at=datetime.fromisoformat(data["updated_at"])
            if "updated_at" in data
            else datetime.now(timezone.utc),
        )


def initialize_controller_state(
    learner_id: str, telemetry_available: bool = False
) -> ControllerState:
    """Create initial controller state for a learner."""
    if not telemetry_available:
        mode = ControllerMode.COLD_START
    else:
        mode = ControllerMode.NOMINAL

    return ControllerState(
        learner_id=learner_id,
        mode=mode,
        budgets=ControllerBudgets(),
        timers=ControllerTimers(),
        recent_outcomes=RecentOutcomes(),
    )


__all__ = [
    "ControllerMode",
    "ControllerBudgets",
    "ControllerTimers",
    "RecentOutcomes",
    "ControllerState",
    "initialize_controller_state",
]
