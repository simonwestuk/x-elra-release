"""Boundedness enforcement for formal ARL compliance (Paper Section 4.2).

This module implements the boundedness constraints that make ARL a "bounded,
deterministic, and inspectable" regulatory controller:

1. **Mode-based action gating**: Routines only execute in permitted modes
2. **Cooldown periods**: Minimum time between routine executions
3. **Resource budgets**: Maximum interventions/suggestions per period
4. **Oscillation detection**: Time-windowed mode transition counting (Appendix B.2)

These constraints ensure:
- Predictable system behaviour
- Prevention of learner fatigue and over-intervention
- Stable regulatory modes (minimum 5-minute mode duration per Appendix B.1)
- Transparent decision-making (all blocks recorded in decision trace)
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Tuple

from .controller_state import ControllerMode, ControllerState
from .schemas import RoutineDefinition


# Default fallbacks used ONLY when a routine has no declared boundedness fields.
# The YAML config is the authoritative source; these exist for backwards compat.
_DEFAULT_MODE_PERMISSIONS: Dict[str, List[ControllerMode]] = {
    "P1": [ControllerMode.COLD_START, ControllerMode.ORIENTATION],
    "P2": [ControllerMode.DIAGNOSTIC],
    "P3": [ControllerMode.STRUGGLING],
    "P4": [ControllerMode.LAPSED],
    "P5": [ControllerMode.ACCELERATING],
    "P6": [ControllerMode.CONSOLIDATING],
    "P7": [ControllerMode.NOMINAL, ControllerMode.COOLDOWN, ControllerMode.ORIENTATION, ControllerMode.DIAGNOSTIC],
    "P8": [ControllerMode.STRUGGLING],
}

_DEFAULT_COOLDOWNS: Dict[str, int] = {
    "P1": 86400,   # 24 hours
    "P2": 3600,    # 1 hour
    "P3": 14400,   # 4 hours
    "P4": 604800,  # 7 days
    "P5": 3600,    # 1 hour
    "P6": 7200,    # 2 hours
    "P7": 0,       # No cooldown
    "P8": 7200,    # 2 hours
}

_DEFAULT_RESOURCE_COSTS: Dict[str, Dict[str, int]] = {
    "P1": {"interventions": 1},
    "P2": {"interventions": 1},
    "P3": {"interventions": 1, "suggestions": 3},
    "P4": {"interventions": 1},
    "P5": {"suggestions": 2},
    "P6": {"suggestions": 2},
    "P7": {},
    "P8": {"interventions": 1, "suggestions": 1},
}

# Public aliases for backwards-compatible test imports
ROUTINE_MODE_PERMISSIONS = _DEFAULT_MODE_PERMISSIONS
ROUTINE_COOLDOWNS = _DEFAULT_COOLDOWNS
ROUTINE_RESOURCE_COSTS = _DEFAULT_RESOURCE_COSTS

# Appendix B.2: Oscillation detection parameters
OSCILLATION_WINDOW_SECONDS = 1800  # τ_window = 30 minutes
OSCILLATION_THRESHOLD = 3          # k = 3 transitions


def _get_permitted_modes(routine: RoutineDefinition) -> list[ControllerMode]:
    """Resolve permitted modes from routine definition, falling back to defaults."""
    if routine.permitted_modes:
        return [ControllerMode(m) for m in routine.permitted_modes]
    return _DEFAULT_MODE_PERMISSIONS.get(routine.name, [])


def _get_cooldown(routine: RoutineDefinition) -> int:
    """Resolve cooldown seconds from routine definition, falling back to defaults."""
    if routine.cooldown_seconds is not None:
        return routine.cooldown_seconds
    return _DEFAULT_COOLDOWNS.get(routine.name, 0)


def _get_resource_costs(routine: RoutineDefinition) -> Dict[str, int]:
    """Resolve resource costs from routine definition, falling back to defaults."""
    if routine.resource_costs:
        return dict(routine.resource_costs)
    return _DEFAULT_RESOURCE_COSTS.get(routine.name, {})


def _detect_oscillation_windowed(
    controller_state: ControllerState,
    *,
    now: Optional[datetime] = None,
    window_seconds: int = OSCILLATION_WINDOW_SECONDS,
    threshold: int = OSCILLATION_THRESHOLD,
) -> bool:
    """Detect oscillation using time-windowed mode transition counting (Appendix B.2).

    Oscillating(S_t) = |S_t.last_transition_times ∩ [t − τ_window, t]| > k
    """
    if now is None:
        now = datetime.now(timezone.utc)

    transition_times = controller_state.recent_outcomes.transition_times
    if not transition_times:
        return False

    cutoff = now.timestamp() - window_seconds
    recent_count = sum(1 for t in transition_times if t >= cutoff)
    return recent_count > threshold


def check_routine_permitted(
    routine: RoutineDefinition,
    controller_state: ControllerState,
    *,
    now: Optional[datetime] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Enforce boundedness constraints on routine execution (Algorithm 1, lines 6-11).

    Checks are ordered per Algorithm 1:
    1. Mode-based gating → SKIPPED (mode mismatch)
    2. Cooldown enforcement → BLOCKED (cooldown_active)
    3. Budget enforcement → BLOCKED (budget_exhausted)
    4. Oscillation prevention → BLOCKED (oscillation_detected)

    Boundedness fields are read from the routine definition (parsed from YAML)
    with fallback to hardcoded defaults for backwards compatibility.

    Args:
        routine: Routine definition to check
        controller_state: Current controller state (S_t)
        now: Current timestamp for cooldown calculations

    Returns:
        (permitted, reason_if_blocked) tuple
    """
    routine_id = routine.name
    if now is None:
        now = datetime.now(timezone.utc)

    # 1. Mode-based gating (Algorithm 1, line 6)
    permitted_modes = _get_permitted_modes(routine)
    if permitted_modes and controller_state.mode not in permitted_modes:
        return False, "mode_mismatch"

    # 2. Cooldown enforcement (Algorithm 1, line 10 — part of CheckBoundedness)
    cooldown = _get_cooldown(routine)
    if controller_state.timers.cooldown_active(routine_id, cooldown, now=now):
        return False, "cooldown_active"

    # 3. Budget enforcement (Algorithm 1, line 10 — part of CheckBoundedness)
    temp_budgets = copy.deepcopy(controller_state.budgets)
    costs = _get_resource_costs(routine)
    for resource, amount in costs.items():
        if not temp_budgets.consume(resource, amount):
            return False, "budget_exhausted"

    # 4. Oscillation prevention (Appendix B.2)
    if _detect_oscillation_windowed(controller_state, now=now):
        return False, "oscillation_detected"

    return True, None


def consume_routine_resources(
    routine: RoutineDefinition,
    controller_state: ControllerState,
) -> None:
    """
    Consume resources for routine execution.

    Reads resource costs from the routine definition (parsed from YAML)
    with fallback to hardcoded defaults.
    """
    costs = _get_resource_costs(routine)
    for resource, amount in costs.items():
        controller_state.budgets.consume(resource, amount)


def check_transition_allowed(
    old_mode: ControllerMode,
    new_mode: ControllerMode,
    timers: Any,
    *,
    now: Optional[datetime] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Prevent rapid mode oscillation (Appendix B.1: Dwell time constraint).

    TransitionAllowed(S_t) = (t − S_t.mode_entered_at) ≥ τ_dwell
    Default τ_dwell = 5 minutes (300 seconds).
    """
    MIN_MODE_DURATION_SECONDS = 300  # τ_dwell = 5 minutes (Appendix B.1)

    if now is None:
        now = datetime.now(timezone.utc)

    if old_mode == new_mode:
        return True, None

    if timers.last_mode_transition is None:
        return True, None

    elapsed = (now - timers.last_mode_transition).total_seconds()

    if elapsed < MIN_MODE_DURATION_SECONDS:
        return (
            False,
            f"mode_transition_too_soon: {elapsed:.0f}s < {MIN_MODE_DURATION_SECONDS}s",
        )

    return True, None


def get_permitted_routines(
    routines: List[RoutineDefinition],
    controller_state: ControllerState,
    *,
    now: Optional[datetime] = None,
) -> List[Tuple[RoutineDefinition, Optional[str]]]:
    """Filter routines by boundedness constraints."""
    if now is None:
        now = datetime.now(timezone.utc)
    results = []
    for routine in routines:
        permitted, reason = check_routine_permitted(routine, controller_state, now=now)
        results.append((routine, reason if not permitted else None))
    return results


__all__ = [
    "ROUTINE_MODE_PERMISSIONS",
    "ROUTINE_COOLDOWNS",
    "ROUTINE_RESOURCE_COSTS",
    "check_routine_permitted",
    "consume_routine_resources",
    "check_transition_allowed",
    "get_permitted_routines",
]
