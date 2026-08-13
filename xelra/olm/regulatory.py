"""Learner-facing OLM projection for regulatory transparency.

This module implements the learner-facing fields specified in Table 1 (Section 3.3)
of the ARL paper, providing process-level explainability without exposing model internals.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..arl.controller_state import ControllerMode, ControllerState


# Mode descriptions in learner-facing terms (matches frontend MODE_LABELS)
MODE_LABELS = {
    ControllerMode.COLD_START: "Discovering",
    ControllerMode.ORIENTATION: "Exploring",
    ControllerMode.NOMINAL: "Progressing",
    ControllerMode.STRUGGLING: "Supporting",
    ControllerMode.LAPSED: "Reconnecting",
    ControllerMode.ACCELERATING: "Advancing",
    ControllerMode.CONSOLIDATING: "Reinforcing",
    ControllerMode.DIAGNOSTIC: "Assessing",
    ControllerMode.COOLDOWN: "Resting",
}


# Why each mode was entered (trigger rationale in learner terms)
MODE_ENTRY_RATIONALES = {
    ControllerMode.COLD_START: "You're new here and we're setting up your personalised learning path.",
    ControllerMode.ORIENTATION: "You're in the initial phase of getting familiar with the platform.",
    ControllerMode.NOMINAL: "You're making steady progress through your learning materials.",
    ControllerMode.STRUGGLING: "You may benefit from additional support in areas where you're finding things challenging.",
    ControllerMode.LAPSED: "We noticed you've been away for a while and want to help you get back on track.",
    ControllerMode.ACCELERATING: "You're making excellent progress toward your learning goals.",
    ControllerMode.CONSOLIDATING: "You've mastered core concepts and are ready to reinforce your learning.",
    ControllerMode.DIAGNOSTIC: "We're checking to ensure everything is working properly with your progress tracking.",
    ControllerMode.COOLDOWN: "You've received several recommendations recently. Taking a brief pause helps avoid overload.",
}


# What the system will do while mode is active
MODE_SYSTEM_BEHAVIOURS = {
    ControllerMode.COLD_START: "The system will provide a curated introduction to help you get started.",
    ControllerMode.ORIENTATION: "The system will guide you through foundational materials in a structured sequence.",
    ControllerMode.NOMINAL: "The system will recommend materials based on your progress and learning goals.",
    ControllerMode.STRUGGLING: "The system will offer targeted resources and support to address specific challenges.",
    ControllerMode.LAPSED: "The system will help you reconnect with your learning goals and resume where you left off.",
    ControllerMode.ACCELERATING: "The system will provide advanced materials to maintain your momentum.",
    ControllerMode.CONSOLIDATING: "The system will suggest practice exercises to reinforce what you've learned.",
    ControllerMode.DIAGNOSTIC: "The system will verify your progress data and may adjust recommendations accordingly.",
    ControllerMode.COOLDOWN: "The system will pause additional prompts and recommendations briefly to reduce disruption.",
}


# What learners should do next
MODE_EXPECTED_ACTIONS = {
    ControllerMode.COLD_START: "Start with the recommended introductory materials.",
    ControllerMode.ORIENTATION: "Follow the guided pathway to build your foundational knowledge.",
    ControllerMode.NOMINAL: "Continue with the current materials or explore recommended items.",
    ControllerMode.STRUGGLING: "Review the suggested support resources and practice materials.",
    ControllerMode.LAPSED: "Review your goals and start with a re-engagement activity.",
    ControllerMode.ACCELERATING: "Challenge yourself with the advanced materials provided.",
    ControllerMode.CONSOLIDATING: "Complete practice exercises to solidify your understanding.",
    ControllerMode.DIAGNOSTIC: "Continue your current task. No immediate action needed.",
    ControllerMode.COOLDOWN: "Continue with your current task. Additional support will resume shortly.",
}


# Human-readable exit condition narratives per Section 4.6 worked example
_EXIT_NARRATIVES = {
    ControllerMode.COLD_START: "After engaging with the introductory materials.",
    ControllerMode.ORIENTATION: "After completing several foundational items.",
    ControllerMode.NOMINAL: "System will adapt as needed.",
    ControllerMode.STRUGGLING: "Once you show progress, support will adjust.",
    ControllerMode.LAPSED: "When you return to consistent engagement.",
    ControllerMode.ACCELERATING: "After achieving your current learning targets.",
    ControllerMode.CONSOLIDATING: "After reinforcing your mastery through practice.",
    ControllerMode.DIAGNOSTIC: "Once progress tracking is verified.",
    ControllerMode.COOLDOWN: "After a short period of reduced recommendations.",
}


def _get_struggling_skills(feature_vector: Any, threshold: float = 0.4) -> List[str]:
    """Extract skills where learner has low mastery."""
    if not feature_vector or not hasattr(feature_vector, 'mastery'):
        return []

    struggling = []
    for skill_id, mastery_level in feature_vector.mastery.items():
        if mastery_level < threshold:
            # Extract readable skill name from ID (e.g., "py_loops" -> "loops")
            skill_name = skill_id.replace('_', ' ').replace('py ', '').strip()
            struggling.append(skill_name)

    return struggling[:3]  # Limit to top 3 for readability


def _get_strong_skills(feature_vector: Any, threshold: float = 0.7) -> List[str]:
    """Extract skills where learner has high mastery."""
    if not feature_vector or not hasattr(feature_vector, 'mastery'):
        return []

    strong = []
    for skill_id, mastery_level in feature_vector.mastery.items():
        if mastery_level >= threshold:
            skill_name = skill_id.replace('_', ' ').replace('py ', '').strip()
            strong.append(skill_name)

    return strong[:3]  # Limit to top 3


def _get_activity_summary(feature_metadata: Optional[Mapping[str, Any]]) -> Dict[str, int]:
    """Extract recent activity metrics from feature metadata."""
    if not feature_metadata:
        return {}

    return {
        'completions_7d': feature_metadata.get('completions_last_7_days', 0),
        'clicks_14d': feature_metadata.get('clicks_last_14_days', 0),
        'impressions_30d': feature_metadata.get('impressions_last_30_days', 0),
        'days_since_engagement': feature_metadata.get('days_since_last_engagement', 0),
    }


def _generate_personalized_why(
    mode: ControllerMode,
    feature_vector: Optional[Any] = None,
    feature_metadata: Optional[Mapping[str, Any]] = None,
) -> str:
    """Generate personalised 'why' explanation based on learner's actual data."""

    # Fallback to static explanation if no personalization data available
    default_why = MODE_ENTRY_RATIONALES.get(
        mode, "The system has adjusted to your current learning context."
    )

    if mode == ControllerMode.STRUGGLING:
        struggling_skills = _get_struggling_skills(feature_vector)
        if struggling_skills:
            skill_list = ", ".join(struggling_skills)
            return f"You may benefit from additional support in areas like {skill_list} where progress has been slower."

    elif mode == ControllerMode.ACCELERATING:
        strong_skills = _get_strong_skills(feature_vector)
        activity = _get_activity_summary(feature_metadata)
        completions = activity.get('completions_7d', 0)

        if strong_skills and completions > 0:
            skill_list = ", ".join(strong_skills)
            return f"You're making excellent progress with {completions} completions this week and strong mastery in {skill_list}."
        elif completions > 0:
            return f"You're making excellent progress with {completions} items completed in the past week."

    elif mode == ControllerMode.LAPSED:
        activity = _get_activity_summary(feature_metadata)
        days_away = activity.get('days_since_engagement', 0)
        # Round to integer and only show if meaningful (> 1 day)
        days_away_int = int(round(days_away))
        if days_away_int > 1:
            return f"We noticed you've been away for about {days_away_int} days and want to help you get back on track."

    elif mode == ControllerMode.CONSOLIDATING:
        strong_skills = _get_strong_skills(feature_vector)
        if strong_skills:
            skill_list = ", ".join(strong_skills)
            return f"You've shown strong mastery in {skill_list} and are ready to reinforce your learning."

    return default_why


def _generate_personalized_system_behavior(
    mode: ControllerMode,
    feature_vector: Optional[Any] = None,
    feature_metadata: Optional[Mapping[str, Any]] = None,
) -> str:
    """Generate personalized system behavior description."""

    default_behavior = MODE_SYSTEM_BEHAVIOURS.get(
        mode, "The system will provide recommendations based on your progress."
    )

    if mode == ControllerMode.STRUGGLING:
        struggling_skills = _get_struggling_skills(feature_vector)
        if struggling_skills:
            skill_list = ", ".join(struggling_skills)
            return f"The system will offer targeted resources to help with {skill_list} and similar areas."

    elif mode == ControllerMode.ACCELERATING:
        strong_skills = _get_strong_skills(feature_vector)
        if strong_skills:
            return "The system will provide advanced materials and new challenges to maintain your momentum."

    elif mode == ControllerMode.CONSOLIDATING:
        strong_skills = _get_strong_skills(feature_vector)
        if strong_skills:
            skill_list = ", ".join(strong_skills)
            return f"The system will suggest practice exercises focused on {skill_list} to reinforce what you've learned."

    return default_behavior


def _generate_personalized_next_action(
    mode: ControllerMode,
    feature_vector: Optional[Any] = None,
    feature_metadata: Optional[Mapping[str, Any]] = None,
) -> str:
    """Generate personalized next action recommendation."""

    default_action = MODE_EXPECTED_ACTIONS.get(
        mode, "Continue with your current learning activities."
    )

    if mode == ControllerMode.STRUGGLING:
        struggling_skills = _get_struggling_skills(feature_vector)
        if struggling_skills:
            return "Review the suggested support resources focusing on areas where you need more practice."

    elif mode == ControllerMode.ACCELERATING:
        return "Challenge yourself with the advanced materials and explore new topics."

    elif mode == ControllerMode.CONSOLIDATING:
        strong_skills = _get_strong_skills(feature_vector)
        if strong_skills:
            return "Complete practice exercises to solidify your understanding and mastery."

    return default_action


def _compute_exit_conditions(
    controller_state: ControllerState, feature_metadata: Optional[Mapping[str, Any]] = None
) -> List[Dict[str, str]]:
    """
    Compute explicit exit/transition conditions in learner-facing terms.

    Returns a list of conditions that will trigger mode exit or transition.
    """
    mode = controller_state.mode
    conditions = []

    if mode == ControllerMode.COLD_START:
        conditions.append({
            "condition": "Complete initial activities",
            "monitored_field": "impressions",
        })

    elif mode == ControllerMode.ORIENTATION:
        conditions.append({
            "condition": "Establish baseline progress",
            "monitored_field": "mastery",
        })

    elif mode == ControllerMode.STRUGGLING:
        conditions.append({
            "condition": "mastery_min > 0.5",
            "monitored_field": "mastery",
        })
        conditions.append({
            "condition": "clicks_14d >= 3",
            "monitored_field": "engagement",
        })

    elif mode == ControllerMode.LAPSED:
        conditions.append({
            "condition": "Resume regular activity",
            "monitored_field": "engagement",
        })

    elif mode == ControllerMode.ACCELERATING:
        conditions.append({
            "condition": "Reach goal milestones",
            "monitored_field": "goals",
        })
        conditions.append({
            "condition": "Maintain pace",
            "monitored_field": "progress_rate",
        })

    elif mode == ControllerMode.CONSOLIDATING:
        conditions.append({
            "condition": "Complete practice exercises",
            "monitored_field": "completions",
        })

    elif mode == ControllerMode.DIAGNOSTIC:
        conditions.append({
            "condition": "feature_gap <= 2",
            "monitored_field": "feature_gap",
        })

    elif mode == ControllerMode.COOLDOWN:
        conditions.append({
            "condition": "cooldown_elapsed",
            "monitored_field": "timers",
        })
        conditions.append({
            "condition": "stable_progress_observed",
            "monitored_field": "engagement",
        })

    else:  # NOMINAL or unknown
        conditions.append({
            "condition": "Continue as you are",
            "monitored_field": "adaptive",
        })

    return conditions


def build_learner_facing_projection(
    controller_state: ControllerState,
    feature_metadata: Optional[Mapping[str, Any]] = None,
    feature_vector: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Build learner-facing OLM projection per Section 4.4 and Example 4.6.

    Provides regulatory transparency without exposing model internals:
    - mode_label: Which regulatory mode is active (Section 4.6)
    - why: Trigger rationale in learner terms (Section 4.6)
    - what_system_will_do: What the system will do while mode is active
    - what_next: What the learner should do next (Section 4.6: "what you should do next")
    - exit_conditions: What will cause transition ("what will change this", Section 4.6)

    Args:
        controller_state: Current controller state S_t
        feature_metadata: Optional feature vector metadata for context
        feature_vector: Optional full feature vector for personalised explanations

    Returns:
        Learner-facing projection dict with the five required fields per Section 4.6
    """
    mode = controller_state.mode

    # Compute exit conditions (Appendix A.3 exit_conditions schema)
    exit_conds = _compute_exit_conditions(controller_state, feature_metadata)

    # Format exit conditions as a human-readable narrative per Section 4.6
    exit_narrative = _EXIT_NARRATIVES.get(mode, "System will adapt as needed.")

    # Generate personalized explanations based on learner's actual data
    why = _generate_personalized_why(mode, feature_vector, feature_metadata)
    what_system_will_do = _generate_personalized_system_behavior(mode, feature_vector, feature_metadata)
    what_next = _generate_personalized_next_action(mode, feature_vector, feature_metadata)

    return {
        # Appendix A.3 olm_projection schema (5 fields)
        "mode_label": MODE_LABELS.get(mode, mode.value),
        "why": why,
        "system_behaviour": what_system_will_do,
        "expected_action": what_next,
        "exit_conditions": exit_narrative,
    }


def _infer_session_phase(metadata: Mapping[str, Any]) -> str:
    """Derive session phase label per Appendix A.1 enum.

    Returns ``"orientation"`` | ``"practice"`` | ``"review"``.
    """
    impressions = metadata.get("impressions_last_30_days", 0)
    clicks_14d = metadata.get("clicks_last_14_days", 0)
    completions_7d = metadata.get("completions_last_7_days", 0)

    if impressions == 0 and clicks_14d == 0:
        return "orientation"
    if completions_7d > 0:
        return "review"
    return "practice"


def build_context_summary(
    feature_vector,  # FeatureVector type (avoid circular import)
    session_metadata: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build context_summary for decision trace per Section 4.4.

    Summarizes task/topic/session phase without full feature vector details.
    """
    metadata = feature_vector.metadata or {}

    summary: Dict[str, Any] = {
        "learner_id": feature_vector.learner_id,
        "timestamp": feature_vector.generated_at.isoformat(),
    }

    # Topic: derive from mastery skill names
    if feature_vector.mastery:
        summary["topic"] = list(feature_vector.mastery.keys())

    # Session phase: inferred from activity indicators
    summary["session_phase"] = _infer_session_phase(metadata)

    # Session phase indicators
    if "impressions_last_30_days" in metadata:
        summary["impressions_30d"] = metadata["impressions_last_30_days"]
    if "clicks_last_14_days" in metadata:
        summary["clicks_14d"] = metadata["clicks_last_14_days"]
    if "completions_last_7_days" in metadata:
        summary["completions_7d"] = metadata["completions_last_7_days"]

    # Task/topic context
    if "active_goal_count" in metadata:
        summary["active_goals"] = metadata["active_goal_count"]
    if "mastery_count" in metadata:
        summary["skill_coverage"] = metadata["mastery_count"]

    # Engagement phase
    if "days_since_last_engagement" in metadata:
        summary["days_since_engagement"] = metadata["days_since_last_engagement"]

    # Optional session metadata
    if session_metadata:
        summary["session"] = dict(session_metadata)

    return summary


def build_inputs_used_summary(
    feature_vector,  # FeatureVector type
    routine_results: Sequence[Any],  # Sequence[RoutineResult]
) -> Dict[str, Any]:
    """
    Build inputs_summary per Appendix A.3.

    Structure: {mastery_range, engagement_level, candidates_count}
    """
    metadata = feature_vector.metadata or {}

    # mastery_range: [min, max] per Appendix A.3
    mastery_range = [0.0, 0.0]
    if feature_vector.mastery:
        vals = list(feature_vector.mastery.values())
        mastery_range = [min(vals), max(vals)]

    # engagement_level: enum per Appendix A.3
    clicks_14d = metadata.get("clicks_last_14_days", 0)
    days_since = metadata.get("days_since_last_engagement", 0)
    if days_since > 15:
        engagement_level = "lapsed"
    elif clicks_14d == 0:
        engagement_level = "declining"
    else:
        engagement_level = "active"

    # candidates_count per Appendix A.3
    candidates_count = len(feature_vector.recommendations) if feature_vector.recommendations else 0

    return {
        "mastery_range": mastery_range,
        "engagement_level": engagement_level,
        "candidates_count": candidates_count,
    }


def compute_next_transition_conditions(
    controller_state: ControllerState,
    feature_metadata: Optional[Mapping[str, Any]] = None,
) -> List[Dict[str, str]]:
    """
    Compute exit_conditions per Appendix A.3.

    Returns ``[{condition, monitored_field}, ...]`` — the explicit conditions
    the controller monitors to trigger a mode exit or transition.
    """
    return _compute_exit_conditions(controller_state, feature_metadata)


__all__ = [
    "build_learner_facing_projection",
    "build_context_summary",
    "build_inputs_used_summary",
    "compute_next_transition_conditions",
    "MODE_LABELS",
    "MODE_ENTRY_RATIONALES",
    "MODE_SYSTEM_BEHAVIOURS",
    "MODE_EXPECTED_ACTIONS",
]
