"""OLM-facing integration helpers for learner profile and transparency views."""

from typing import Dict, Any, List, Optional
import pandas as pd
from ..data.loader import load_items, load_events
from ..utils.db import SessionLocal, LearnerPreference, get_controller_state, save_controller_state
from ..arl.controller_state import ControllerMode, ControllerState
from ..arl.mode_inference import infer_mode
from ..arl.state import build_feature_vector
from .regulatory import build_learner_facing_projection


def set_preferences(learner_id: str, explain_level: str = "auto") -> Dict[str, Any]:
    db = SessionLocal()
    pref = db.query(LearnerPreference).filter_by(learner_id=learner_id).first()
    if pref:
        pref.explain_level = explain_level
    else:
        pref = LearnerPreference(learner_id=learner_id, explain_level=explain_level)
        db.add(pref)
    db.commit()
    db.close()
    return {"learner_id": learner_id, "explain_level": explain_level}


def get_preferences(learner_id: str) -> Dict[str, Any]:
    db = SessionLocal()
    pref = db.query(LearnerPreference).filter_by(learner_id=learner_id).first()
    level = pref.explain_level if pref else "auto"
    db.close()
    return {"explain_level": level}


def _topic_from_row(row) -> List[str]:
    topics = str(row.get("topics", "") or "").split("|")
    return [t.strip() for t in topics if t.strip()]


def learner_profile(learner_id: str) -> Dict[str, Any]:
    items = load_items()
    events = load_events()
    df = events.merge(items, on="item_id", how="left")
    df = df[df["learner_id"] == learner_id].copy()
    mastery: Dict[str, float] = {}
    recent = []
    if not df.empty:
        df["weight"] = df["clicked"].fillna(0) * 1.0 + df["completed"].fillna(0) * 2.0
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp", ascending=False)
        for r in df.itertuples():
            ts = getattr(r, "timestamp", None)
            recent.append(
                {
                    "item_id": r.item_id,
                    "title": r.title,
                    "completed": int(r.completed),
                    "timestamp": str(ts) if pd.notnull(ts) else None,
                }
            )
            for t in _topic_from_row(
                r._asdict() if hasattr(r, "_asdict") else {"topics": r.topics}
            ):
                mastery[t] = mastery.get(t, 0.0) + float(r.weight)
    if mastery:
        mmax = max(mastery.values())
        if mmax > 0:
            for k in list(mastery.keys()):
                mastery[k] = round(mastery[k] / mmax, 3)
    all_topics = set()
    for r in items.itertuples():
        for t in _topic_from_row(
            r._asdict() if hasattr(r, "_asdict") else {"topics": r.topics}
        ):
            all_topics.add(t)
    mastered = {k for k, v in mastery.items() if v >= 0.7}
    weak = sorted(list(all_topics - mastered), key=lambda t: mastery.get(t, 0.0))
    next_topics = weak[:3]
    seen = set(df["item_id"].tolist()) if not df.empty else set()
    recs = []
    for r in items.itertuples():
        if r.item_id in seen:
            continue
        its = _topic_from_row(
            r._asdict() if hasattr(r, "_asdict") else {"topics": r.topics}
        )
        if any(t in its for t in next_topics):
            recs.append({"item_id": r.item_id, "title": r.title, "topics": its})
    recs = recs[:5]
    prefs = get_preferences(learner_id)
    profile = {
        "learner_id": learner_id,
        "preferences": prefs,
        "mastery": mastery,
        "recent_activity": recent[:10],
        "next_topics": next_topics,
        "suggested_items": recs,
    }
    return profile


def compute_mode_from_features(feature_vector, controller_state: ControllerState = None) -> ControllerMode:
    """
    Compute the correct controller mode based on the learner's feature vector.

    Delegates to mode_inference.infer_mode() to ensure a single source of truth
    for mode determination across the ARL engine and OLM projection.

    Args:
        feature_vector: The learner's FeatureVector
        controller_state: Optional current controller state for budget/transition checks

    Returns:
        The appropriate ControllerMode
    """
    if controller_state is None:
        controller_state = ControllerState(learner_id=feature_vector.learner_id)
    return infer_mode(feature_vector, controller_state)


def regulatory_transparency(learner_id: str) -> Dict[str, Any]:
    """
    Get learner-facing regulatory transparency information.

    Implements the OLM projection per Table 1 (Section 3.3) of the ARL paper:
    - Current mode: Which regulatory mode is active
    - Why entered: Trigger rationale in learner terms
    - System behaviour: What the system will do while mode is active
    - Expected learner action: What to do next
    - Exit conditions: What will cause transition or exit

    This provides process-level explainability without exposing model internals.

    Args:
        learner_id: The learner identifier

    Returns:
        Dict with learner-facing regulatory transparency fields
    """
    db = SessionLocal()
    try:
        # Build feature vector to get current learner state
        feature_vector = build_feature_vector(db, learner_id)

        # Load controller state S_t
        controller_state = get_controller_state(db, learner_id)

        # Compute the correct mode based on the feature vector
        computed_mode = compute_mode_from_features(feature_vector, controller_state)

        # Update controller state if mode has changed
        if controller_state.mode != computed_mode:
            controller_state.mode = computed_mode
            save_controller_state(db, controller_state)
            db.commit()

        # Build feature metadata for personalization
        feature_metadata = dict(feature_vector.metadata) if feature_vector.metadata else {}

        # Add goal count for context
        feature_metadata["active_goal_count"] = len(feature_vector.goals) if feature_vector.goals else 0

        # Build learner-facing projection with full personalization
        projection = build_learner_facing_projection(
            controller_state,
            feature_metadata=feature_metadata,
            feature_vector=feature_vector,
        )

        # Add additional context
        projection["learner_id"] = learner_id
        projection["mode_internal"] = controller_state.mode.value  # For debugging
        projection["budgets_remaining"] = {
            "interventions": controller_state.budgets.interventions_remaining,
            "suggestions": controller_state.budgets.suggestions_remaining,
        }

        return projection
    finally:
        db.close()
