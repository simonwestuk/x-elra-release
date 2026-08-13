"""Mode inference and state transition logic for formal ARL.

This module implements the S_t → S_{t+1} transition function (Algorithm Step 6)
and mode inference based on learner perceptions (feature vector).

Key concepts from the paper:
- Controller modes represent discrete regulatory stances
- Mode inference is deterministic and based on perception thresholds
- Mode transitions follow priority order matching routine priorities
- Modes gate which control routines are eligible for execution
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from .controller_state import ControllerBudgets, ControllerMode, ControllerState
from .schemas import FeatureVector


def get_mode_inference_reason(
    feature_vector: FeatureVector,
    current_state: ControllerState,
) -> str:
    """
    Get the reason why a particular mode would be inferred.

    Returns a human-readable string explaining which condition triggered
    the mode inference. Useful for debugging mode transition blocks.

    Args:
        feature_vector: Learner perceptions (I_t) from ML models and telemetry
        current_state: Current controller state (S_t)

    Returns:
        String explaining why the mode was inferred
    """
    metadata = feature_vector.metadata

    # COOLDOWN check (budget exhaustion + frequent transitions, or oscillation)
    interventions_remaining = current_state.budgets.interventions_remaining
    mode_transition_count = current_state.metadata.get("mode_transition_count", 0)
    if interventions_remaining <= 1 and mode_transition_count >= 3:
        return f"COOLDOWN: interventions_remaining={interventions_remaining}, mode_transition_count={mode_transition_count}"

    # Oscillation → COOLDOWN (Appendix B.2)
    from .boundedness import _detect_oscillation_windowed
    if _detect_oscillation_windowed(current_state):
        return "COOLDOWN: oscillation_detected (Appendix B.2)"

    mastery_empty = not feature_vector.mastery or all(
        v == 0 for v in feature_vector.mastery.values()
    )
    impressions_count = metadata.get("impressions_last_30_days", 0)

    # COLD_START check
    if mastery_empty and impressions_count == 0:
        return f"COLD_START: mastery_empty={mastery_empty}, impressions_count={impressions_count}"

    # ORIENTATION check
    if mastery_empty and impressions_count > 0 and impressions_count < 10:
        return f"ORIENTATION: mastery_empty={mastery_empty}, impressions_count={impressions_count}"

    # DIAGNOSTIC check
    feature_gap = metadata.get("feature_gap", 0)
    if feature_gap > 2:
        return f"DIAGNOSTIC: feature_gap={feature_gap}"

    # LAPSED check (Table 4: >15 days inactive, active goals)
    days_since_engagement = metadata.get("days_since_last_engagement", 0)
    active_goals = metadata.get("active_goal_count", 0)
    if days_since_engagement > 15 and active_goals > 0:
        return f"LAPSED: days_since_engagement={days_since_engagement}, active_goals={active_goals}"

    # STRUGGLING check (Table 4: lowest mastery < 0.4, no clicks in 14 days)
    mastery_values = list(feature_vector.mastery.values())
    lowest_mastery = min(mastery_values) if mastery_values else 0.0
    clicks_14d = metadata.get("clicks_last_14_days", 0)
    if lowest_mastery < 0.4 and clicks_14d == 0:
        return f"STRUGGLING: lowest_mastery={lowest_mastery}, clicks_14d={clicks_14d}"

    # STRUGGLING via affect flags (confusion or frustration from live code + sentiment)
    confusion = metadata.get("confusion_flag", False)
    frustration = metadata.get("frustration_flag", False)
    if confusion or frustration:
        return f"STRUGGLING: confusion_flag={confusion}, frustration_flag={frustration}"

    # CONSOLIDATING check
    highest_mastery = max(mastery_values) if mastery_values else 0.0
    completions_7d = metadata.get("completions_last_7_days", 0)
    if highest_mastery >= 0.85 and completions_7d > 0:
        return f"CONSOLIDATING: highest_mastery={highest_mastery}, completions_7d={completions_7d}"

    # ACCELERATING check
    progress_rate = metadata.get("progress_rate", 0.0)
    if active_goals > 0 and progress_rate >= 0.05:
        return f"ACCELERATING: active_goals={active_goals}, progress_rate={progress_rate}"

    # Default
    return "NOMINAL: no special conditions met"


def infer_mode(
    feature_vector: FeatureVector,
    current_state: ControllerState,
) -> ControllerMode:
    """
    Infer appropriate controller mode from learner perceptions (I_t → mode).

    Mode inference is deterministic and based on explicit perception thresholds.
    Modes represent discrete regulatory stances that gate available control routines.

    Mode inference priority order:
    1. COOLDOWN - budget exhaustion + frequent transitions, or oscillation (Appendix B.2)
    2. COLD_START (P1) - no mastery signals, zero impressions
    3. ORIENTATION (P1) - no mastery, 1-9 impressions
    4. DIAGNOSTIC (P2) - feature gap > 2 (missing data sources)
    5. LAPSED (P4) - >15 days inactive, active goals
    6. STRUGGLING (P3) - lowest mastery < 0.4, no clicks in 14 days
    7. CONSOLIDATING (P6) - highest mastery >= 0.85, recent completions
    8. ACCELERATING (P5) - active goals, progress rate >= 0.05/day
    9. NOMINAL (P7) - default fallback

    Args:
        feature_vector: Learner perceptions (I_t) from ML models and telemetry
        current_state: Current controller state (S_t)

    Returns:
        Inferred controller mode for S_{t+1}
    """
    metadata = feature_vector.metadata

    # COOLDOWN: Budget exhaustion + frequent transitions (Table 4)
    interventions_remaining = current_state.budgets.interventions_remaining
    mode_transition_count = current_state.metadata.get("mode_transition_count", 0)
    if interventions_remaining <= 1 and mode_transition_count >= 3:
        return ControllerMode.COOLDOWN

    # COOLDOWN: Oscillation detected → transition to COOLDOWN (Appendix B.2)
    from .boundedness import _detect_oscillation_windowed
    if _detect_oscillation_windowed(current_state):
        return ControllerMode.COOLDOWN

    # Check for empty/zero mastery (used in multiple conditions)
    mastery_empty = not feature_vector.mastery or all(
        v == 0 for v in feature_vector.mastery.values()
    )
    impressions_count = metadata.get("impressions_last_30_days", 0)

    # COLD_START: No mastery signals, zero impressions (Table 4)
    if mastery_empty and impressions_count == 0:
        return ControllerMode.COLD_START

    # ORIENTATION: No mastery, 1-9 impressions (Table 4)
    if mastery_empty and impressions_count > 0 and impressions_count < 10:
        return ControllerMode.ORIENTATION

    # DIAGNOSTIC: Feature gap > 2 (Table 4)
    feature_gap = metadata.get("feature_gap", 0)
    if feature_gap > 2:
        return ControllerMode.DIAGNOSTIC

    # LAPSED: >15 days inactive, active goals (Table 4)
    days_since_engagement = metadata.get("days_since_last_engagement", 0)
    active_goals = metadata.get("active_goal_count", 0)
    if days_since_engagement > 15 and active_goals > 0:
        return ControllerMode.LAPSED

    # STRUGGLING: Lowest mastery < 0.4, no clicks in 14 days (Table 4)
    mastery_values = list(feature_vector.mastery.values())
    lowest_mastery = min(mastery_values) if mastery_values else 0.0
    clicks_14d = metadata.get("clicks_last_14_days", 0)
    if lowest_mastery < 0.4 and clicks_14d == 0:
        return ControllerMode.STRUGGLING

    # STRUGGLING via affect flags (confusion or frustration from live code + sentiment)
    if metadata.get("confusion_flag") or metadata.get("frustration_flag"):
        return ControllerMode.STRUGGLING

    # CONSOLIDATING: Highest mastery >= 0.85, recent completions (Table 4)
    highest_mastery = max(mastery_values) if mastery_values else 0.0
    completions_7d = metadata.get("completions_last_7_days", 0)
    if highest_mastery >= 0.85 and completions_7d > 0:
        return ControllerMode.CONSOLIDATING

    # ACCELERATING: Active goals, progress rate >= 0.05/day (Table 4)
    progress_rate = metadata.get("progress_rate", 0.0)
    if active_goals > 0 and progress_rate >= 0.05:
        return ControllerMode.ACCELERATING

    # NOMINAL: Default (Table 4)
    return ControllerMode.NOMINAL


def transition_state(
    old_state: ControllerState,
    action_taken: str,
    feature_vector: FeatureVector,
) -> ControllerState:
    """
    Compute S_{t+1} from S_t, A_t, and I_t (Algorithm Step 6).

    This is the core state transition function ensuring deterministic
    controller evolution. The function:
    1. Infers new mode from perceptions (I_t)
    2. Updates budgets (reset on mode transition, session expiry)
    3. Updates timers (last_intervention, last_mode_transition)
    4. Appends decision to recent outcomes history
    5. Records mode transition timestamps for oscillation detection (Appendix B.2)

    The state transition is deterministic and reproducible given the same inputs.
    Creates a new state object (immutable semantics) rather than mutating in place.

    Args:
        old_state: Current controller state (S_t)
        action_taken: Control routine executed in this cycle (A_t or ∅)
        feature_vector: Current learner perceptions (I_t)

    Returns:
        New controller state (S_{t+1}) with updated mode, budgets, timers
    """
    # Infer new mode from perceptions
    new_mode = infer_mode(feature_vector, old_state)

    # Create new state (immutable update pattern)
    import copy

    now = feature_vector.generated_at
    new_state = ControllerState(
        learner_id=old_state.learner_id,
        mode=new_mode,
        budgets=copy.deepcopy(old_state.budgets),
        timers=copy.deepcopy(old_state.timers),
        recent_outcomes=copy.deepcopy(old_state.recent_outcomes),
        metadata=dict(old_state.metadata),
        version=old_state.version,
        updated_at=now,
    )

    # Update recent outcomes history
    new_state.recent_outcomes.append(action_taken)

    # Reset budgets on mode transition and record transition time (Appendix B.2)
    if new_mode != old_state.mode:
        new_state.timers.last_mode_transition = now
        new_state.budgets = ControllerBudgets()  # Fresh budgets
        new_state.metadata["mode_transition_count"] = (
            old_state.metadata.get("mode_transition_count", 0) + 1
        )
        new_state.metadata["previous_mode"] = old_state.mode.value
        # Record transition timestamp for time-windowed oscillation detection
        new_state.recent_outcomes.record_transition(now=now)

    # Reset session budgets if new session (>4 hours since last intervention)
    if old_state.timers.last_intervention:
        hours_elapsed = (now - old_state.timers.last_intervention).total_seconds() / 3600
        if hours_elapsed > 4:
            new_state.budgets.reset("interventions", 5)
            new_state.metadata["session_resets"] = (
                old_state.metadata.get("session_resets", 0) + 1
            )

    return new_state


__all__ = ["infer_mode", "transition_state", "get_mode_inference_reason"]
