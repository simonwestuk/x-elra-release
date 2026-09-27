"""Prompt templates for the LLM feedback generator.

Prompts deliberately exclude any governance information (modes, budgets,
cooldowns).  The LLM should produce pedagogical feedback only; governance
decisions are the exclusive responsibility of the ARL controller.
"""
from __future__ import annotations

from typing import Any, Mapping, Optional


FEEDBACK_PROMPT_TEMPLATE = """\
You are a supportive learning assistant for a Python programming course.

A learner is currently working on {topic}. Their mastery level is {mastery_level} \
(on a scale of 0 to 1). They have been {engagement_description} recently.
{affect_context}
Generate a short piece of personalised learning feedback (2-3 sentences) that:
- Acknowledges their current position
- Suggests a specific next step
- Is encouraging but honest

Respond with only the feedback text, no preamble or formatting."""


def _describe_engagement(metadata: Mapping[str, Any]) -> str:
    """Return a human-readable engagement description from feature metadata."""
    days = metadata.get("days_since_last_engagement")
    if days is None or days == float("inf"):
        return "inactive (no recent engagement recorded)"
    if days <= 1:
        return "actively engaged"
    if days <= 7:
        return "moderately active"
    if days <= 14:
        return "showing declining engagement"
    return "lapsed (inactive for over two weeks)"


def _describe_affect(metadata: Mapping[str, Any]) -> str:
    """Return affect context string from confusion/frustration flags."""
    confusion = metadata.get("confusion_flag", False)
    frustration = metadata.get("frustration_flag", False)
    if confusion and frustration:
        return "The learner appears to be both confused and frustrated."
    if confusion:
        return "The learner appears to be confused."
    if frustration:
        return "The learner appears to be frustrated."
    return ""


def build_feedback_prompt(
    topic: str,
    mastery_level: float,
    metadata: Mapping[str, Any],
) -> str:
    """Construct a feedback prompt from learner state.

    Parameters
    ----------
    topic:
        The current topic or module the learner is working on.
    mastery_level:
        The learner's mastery estimate for the active topic (0-1).
    metadata:
        The FeatureVector metadata dict containing engagement and affect fields.
    """
    engagement_description = _describe_engagement(metadata)
    affect_context = _describe_affect(metadata)
    return FEEDBACK_PROMPT_TEMPLATE.format(
        topic=topic,
        mastery_level=f"{mastery_level:.2f}",
        engagement_description=engagement_description,
        affect_context=affect_context,
    )
