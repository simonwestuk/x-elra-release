"""Learner state assembly utilities."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from typing import Any, Mapping, Optional, Sequence

try:  # pragma: no cover - optional dependency
    import redis  # type: ignore
except Exception:  # pragma: no cover - redis optional
    redis = None  # type: ignore

from sqlalchemy.orm import Session

from ..config import settings
from ..models.recommender.factory import (
    get_hybrid_recommender,
    get_sequence_recommender,
)
from ..models.llm.config import is_llm_feedback_enabled
from ..olm import service as olm_service
from ..utils.db import Click, Completion, Goal, Impression, LearnerSentimentWindow, LiveCodeEvent
from .schemas import FeatureVector

logger = logging.getLogger(__name__)

_REDIS_CLIENT: Any | None = None


def _normalise_timestamp(value: Any) -> Optional[datetime]:
    if isinstance(value, datetime):
        dt_value = value
    elif isinstance(value, str):
        try:
            dt_value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if dt_value.tzinfo is not None:
        return dt_value.astimezone(timezone.utc)
    return dt_value.replace(tzinfo=timezone.utc)


def _latest_timestamp(entries: Sequence[Mapping[str, Any]]) -> Optional[datetime]:
    latest: Optional[datetime] = None
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        ts = _normalise_timestamp(entry.get("created_at") or entry.get("timestamp"))
        if ts is None:
            continue
        if latest is None or ts > latest:
            latest = ts
    return latest


def _count_recent(entries: Sequence[Mapping[str, Any]], *, days: int) -> int:
    if days <= 0:
        return 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    total = 0
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        ts = _normalise_timestamp(entry.get("created_at") or entry.get("timestamp"))
        if ts is None:
            continue
        if ts >= cutoff:
            total += 1
    return total


def build_feature_metadata(
    mastery: Mapping[str, Any],
    goals: Sequence[Mapping[str, Any]],
    impressions: Sequence[Mapping[str, Any]],
    clicks: Sequence[Mapping[str, Any]],
    completions: Sequence[Mapping[str, Any]],
    recommendations: Sequence[Mapping[str, Any]],
    *,
    strategy: str,
    top_k: int,
    cached: bool,
    error: Optional[str] = None,
    live_code_events: Optional[Sequence[Mapping[str, Any]]] = None,
    sentiment_mean: Optional[float] = None,
) -> Mapping[str, Any]:
    mastery_values = list(mastery.values()) if mastery else []
    has_incomplete_mastery = any(value is None for value in mastery_values)
    # feature_gap counts missing LEARNER data sources only (Table 4: DIAGNOSTIC entry).
    # Runtime artifacts (recommendations, errors) are tracked separately.
    feature_gap = 0
    if not mastery or has_incomplete_mastery:
        feature_gap += 1
    if not goals:
        feature_gap += 1
    if not impressions:
        feature_gap += 1
    if not clicks:
        feature_gap += 1
    if not completions:
        feature_gap += 1

    organic_impressions = [
        entry
        for entry in impressions
        if not str(entry.get("source") or "").lower().startswith("arl_")
    ]
    latest_organic = _latest_timestamp(organic_impressions)
    if latest_organic is None:
        days_since_last_impression = float("inf")
    else:
        delta = datetime.now(timezone.utc) - latest_organic
        days_since_last_impression = max(delta.total_seconds() / 86400.0, 0.0)

    completions_7d = _count_recent(completions, days=7)
    completions_30d = _count_recent(completions, days=30)
    progress_rate = completions_30d / 30.0

    latest_engagement = _latest_timestamp(clicks)
    latest_completion = _latest_timestamp(completions)
    if latest_completion is not None and (
        latest_engagement is None or latest_completion > latest_engagement
    ):
        latest_engagement = latest_completion
    if latest_engagement is None:
        days_since_last_engagement = float("inf")
    else:
        delta = datetime.now(timezone.utc) - latest_engagement
        days_since_last_engagement = max(delta.total_seconds() / 86400.0, 0.0)

    clicks_14d = _count_recent(clicks, days=14)
    impressions_30d = _count_recent(organic_impressions, days=30)
    active_goal_count = len(goals) if goals else 0

    metadata = {
        "strategy": strategy,
        "top_k": int(top_k),
        "cached": cached,
        "feature_gap": feature_gap,
        "days_since_last_impression": days_since_last_impression,
        "days_since_last_engagement": days_since_last_engagement,
        "progress_rate": progress_rate,
        "completions_last_7_days": completions_7d,
        "completions_last_30_days": completions_30d,
        "clicks_last_14_days": clicks_14d,
        "impressions_last_30_days": impressions_30d,
        "active_goal_count": active_goal_count,
    }
    # Compute behavioral features from live code events (actual code execution errors)
    live_code_behavioural: Mapping[str, Any] = {}
    if live_code_events:
        live_code_behavioural = _compute_behavioural_features_from_live_code(live_code_events)
        metadata.update(live_code_behavioural)

    # Derive affect flags from behavioural features + sentiment
    if sentiment_mean is not None:
        metadata["sentiment_mean"] = sentiment_mean
    affect_flags = _compute_affect_flags(live_code_behavioural, sentiment_mean)
    metadata.update(affect_flags)

    latest_any = _latest_timestamp(impressions)
    if latest_any is not None:
        metadata["last_impression_at"] = latest_any.isoformat().replace(
            "+00:00", "Z"
        )
    if error:
        metadata["error"] = error
    return metadata


def get_redis_client(url: Optional[str] = None) -> Any | None:
    """Return a cached Redis client if the dependency and URL are available."""

    global _REDIS_CLIENT
    if _REDIS_CLIENT is not None:
        return _REDIS_CLIENT
    url = url or getattr(settings, "redis_url", None)
    if not url or redis is None:
        return None
    try:
        _REDIS_CLIENT = redis.StrictRedis.from_url(url, decode_responses=True)  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - redis connectivity issues
        logger.exception("failed to initialise redis client", extra={"url": url})
        _REDIS_CLIENT = None
    return _REDIS_CLIENT


def _serialize_goal(goal: Goal, mastery: Mapping[str, float]) -> Mapping[str, Any]:
    due = goal.due_date.isoformat() if getattr(goal, "due_date", None) else None
    return {
        "skill_id": goal.skill_id,
        "target": float(getattr(goal, "target", 1.0) or 1.0),
        "due_date": due,
        "progress": float(mastery.get(goal.skill_id, 0.0)),
    }


def _serialize_event(row: Any) -> Mapping[str, Any]:
    created_at = getattr(row, "created_at", None)
    if isinstance(created_at, datetime):
        created_iso = created_at.isoformat()
    else:
        created_iso = None
    payload = {
        "item_id": getattr(row, "item_id", None),
        "rank": getattr(row, "rank", None),
        "strategy": getattr(row, "strategy", None),
        "arm": getattr(row, "arm", None),
        "arm_key": getattr(row, "arm_key", None),
        "source": getattr(row, "source", None),
        "policy_version": getattr(row, "policy_version", None),
        "schema_version": getattr(row, "schema_version", None),
        "request_id": getattr(row, "request_id", None),
        "created_at": created_iso,
    }
    return payload


def _fetch_recent(session: Session, model: Any, learner_id: str, limit: int = 50) -> Sequence[Mapping[str, Any]]:
    rows = (
        session.query(model)
        .filter(model.learner_id == learner_id)
        .order_by(model.created_at.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_event(row) for row in rows]


def _serialize_live_code_event(row: Any) -> Mapping[str, Any]:
    """Serialize a LiveCodeEvent row to a dict for behavioral feature extraction."""
    event_at = getattr(row, "event_at", None)
    if isinstance(event_at, datetime):
        if event_at.tzinfo is None:
            event_at = event_at.replace(tzinfo=timezone.utc)
        timestamp_iso = event_at.isoformat()
    else:
        timestamp_iso = None

    status = getattr(row, "status", None)
    error_type = getattr(row, "error_type", None)

    # Map status to success/error flags for behavioral feature extraction
    is_success = status == "success" if status else None
    is_error = status == "error" or error_type is not None

    return {
        "id": getattr(row, "id", None),
        "learner_id": getattr(row, "learner_id", None),
        "item_id": getattr(row, "item_id", None),
        "event": getattr(row, "event", None),
        "cell_id": getattr(row, "cell_id", None),
        "status": status,
        "error_type": error_type,
        "error_message": getattr(row, "error_message", None),
        "duration_ms": getattr(row, "duration_ms", None),
        "timestamp": timestamp_iso,
        "created_at": timestamp_iso,
        # Mapped fields for behavioral feature extraction
        "success": is_success,
        "error": is_error,
    }


def _fetch_recent_live_code_events(
    session: Session, learner_id: str, limit: int = 100
) -> Sequence[Mapping[str, Any]]:
    """Fetch recent live code events for a learner (run events only)."""
    rows = (
        session.query(LiveCodeEvent)
        .filter(LiveCodeEvent.learner_id == learner_id)
        .filter(LiveCodeEvent.event == "run")  # Only code run events, not impressions
        .order_by(LiveCodeEvent.event_at.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_live_code_event(row) for row in rows]


def _compute_behavioural_features_from_live_code(
    live_code_events: Sequence[Mapping[str, Any]]
) -> Mapping[str, Any]:
    """
    Compute behavioral features from LiveCodeEvent records.

    This supplements _compute_behavioural_features() which uses Completion records.
    LiveCodeEvent has direct access to error_type and status from code execution.
    """
    # Sort by timestamp (oldest first for burst detection)
    ordered: list[tuple[Optional[datetime], Mapping[str, Any]]] = []
    for entry in live_code_events:
        if not isinstance(entry, Mapping):
            continue
        timestamp = _normalise_timestamp(entry.get("timestamp") or entry.get("created_at"))
        ordered.append((timestamp, entry))
    ordered.sort(key=lambda item: item[0] or datetime.min.replace(tzinfo=timezone.utc))

    max_error_burst = 0
    current_error_burst = 0
    max_success_streak = 0
    current_success_streak = 0
    error_types: set[str] = set()
    total_runs = 0
    error_runs = 0

    for _, entry in ordered:
        status = entry.get("status")
        error_type = entry.get("error_type")
        is_error = status == "error" or error_type is not None
        is_success = status == "success"

        total_runs += 1

        if is_error:
            current_error_burst += 1
            current_success_streak = 0
            error_runs += 1
            if error_type:
                error_types.add(str(error_type))
        else:
            max_error_burst = max(max_error_burst, current_error_burst)
            current_error_burst = 0

        if is_success:
            current_success_streak += 1
            max_success_streak = max(max_success_streak, current_success_streak)
        else:
            current_success_streak = 0

    # Capture final burst if ended on errors
    max_error_burst = max(max_error_burst, current_error_burst)

    # Error rate (similar to hint_rate but for errors)
    error_rate = (error_runs / total_runs) if total_runs > 0 else 0.0

    return {
        "live_code_error_burst": int(max_error_burst),
        "live_code_success_streak": int(max_success_streak),
        "live_code_error_rate": float(error_rate),
        "live_code_error_types": sorted(error_types),
        "live_code_error_type_count": len(error_types),
        "live_code_total_runs": total_runs,
        "live_code_error_runs": error_runs,
    }


def _fetch_learner_sentiment(session: Session, learner_id: str) -> Optional[float]:
    """Return the rolling 7-day mean sentiment polarity for *learner_id*, or ``None``."""
    row = session.get(LearnerSentimentWindow, learner_id)
    if row is None or getattr(row, "n_7d", 0) == 0:
        return None
    return float(row.mean_polarity_7d)


# -- Affect-flag thresholds (module-level so tests can inspect / override) ----
CONFUSION_ERROR_TYPE_COUNT_HIGH = 3
CONFUSION_ERROR_TYPE_COUNT_LOW = 2
CONFUSION_ERROR_RATE_THRESHOLD = 0.5

FRUSTRATION_ERROR_BURST_WITH_SENTIMENT = 3
FRUSTRATION_SENTIMENT_NEGATIVE = 0.0
FRUSTRATION_ERROR_BURST_ALONE = 5
FRUSTRATION_SENTIMENT_VERY_NEGATIVE = -0.3
FRUSTRATION_ERROR_RATE_WITH_SENTIMENT = 0.3


def _compute_affect_flags(
    live_code_features: Mapping[str, Any],
    sentiment_mean: Optional[float],
) -> Mapping[str, bool]:
    """Derive ``confusion_flag`` and ``frustration_flag`` from behavioural + sentiment signals.

    Confusion heuristic (error *diversity* → learner is lost):
      * ``error_type_count >= 3``, **or**
      * ``error_type_count >= 2`` **and** ``error_rate > 0.5``

    Frustration heuristic (persistent failure + negative affect):
      * ``error_burst >= 3`` **and** ``sentiment_mean < 0``, **or**
      * ``error_burst >= 5`` (extreme burst alone), **or**
      * ``sentiment_mean < -0.3`` **and** ``error_rate > 0.3``
    """
    error_type_count = int(live_code_features.get("live_code_error_type_count", 0))
    error_rate = float(live_code_features.get("live_code_error_rate", 0.0))
    error_burst = int(live_code_features.get("live_code_error_burst", 0))

    confusion_flag = (
        error_type_count >= CONFUSION_ERROR_TYPE_COUNT_HIGH
        or (
            error_type_count >= CONFUSION_ERROR_TYPE_COUNT_LOW
            and error_rate > CONFUSION_ERROR_RATE_THRESHOLD
        )
    )

    frustration_flag = False
    if sentiment_mean is not None:
        frustration_flag = (
            (error_burst >= FRUSTRATION_ERROR_BURST_WITH_SENTIMENT
             and sentiment_mean < FRUSTRATION_SENTIMENT_NEGATIVE)
            or (sentiment_mean < FRUSTRATION_SENTIMENT_VERY_NEGATIVE
                and error_rate > FRUSTRATION_ERROR_RATE_WITH_SENTIMENT)
        )
    if not frustration_flag:
        frustration_flag = error_burst >= FRUSTRATION_ERROR_BURST_ALONE

    return {
        "confusion_flag": confusion_flag,
        "frustration_flag": frustration_flag,
    }


def _merge_candidates(
    recommender_items: list,
    llm_candidates: list,
) -> list:
    """Merge hybrid recommender and LLM feedback candidates into a single list.

    Sorting: descending by score, with deterministic tie-breaking by item_id
    (lexicographic ascending).  This guarantees a stable, reproducible ordering
    for the controller's determinism guarantee.
    """
    merged = list(recommender_items) + list(llm_candidates)
    merged.sort(key=lambda c: (-c.get("score", 0.0), c.get("item_id", "")))
    return merged


def build_feature_vector(
    session: Session,
    learner_id: str,
    *,
    redis_client: Any | None = None,
    ttl_seconds: int = 300,
    refresh: bool = False,
    top_k: int = 10,
    strategy: str = "hybrid",
) -> FeatureVector:
    """Build (and cache) a feature vector for ``learner_id``."""

    cache = redis_client or get_redis_client()
    cache_key = f"arl:feature:{learner_id}"
    if cache and not refresh:
        try:
            cached = cache.get(cache_key)
        except Exception:  # pragma: no cover - connectivity issue
            cached = None
        if cached:
            try:
                vector = FeatureVector.from_json(cached)
                missing_keys = {
                    "feature_gap",
                    "days_since_last_impression",
                    "progress_rate",
                } - set(vector.metadata.keys())
                if missing_keys:
                    raise ValueError("cached feature vector missing required metadata")
                logger.debug(
                    "feature vector cache hit", extra={"learner_id": learner_id}
                )
                vector.metadata = dict(vector.metadata)
                vector.metadata["cached"] = True
                return vector
            except Exception:  # pragma: no cover - corrupted payload
                logger.warning(
                    "failed to decode cached feature vector; rebuilding",
                    extra={"learner_id": learner_id},
                )

    mastery_map = olm_service.learner_mastery_map(session, learner_id)
    goals = [
        _serialize_goal(goal, mastery_map)
        for goal in olm_service.goals_for_learner(session, learner_id)
    ]
    impressions = _fetch_recent(session, Impression, learner_id)
    clicks = _fetch_recent(session, Click, learner_id)
    completions = _fetch_recent(session, Completion, learner_id)
    live_code_events = _fetch_recent_live_code_events(session, learner_id)
    sentiment_mean = _fetch_learner_sentiment(session, learner_id)

    recommender_items: Sequence[Mapping[str, Any]] = []
    recommender_error: Optional[str] = None
    try:
        if strategy == "sequence":
            recommender = get_sequence_recommender()
        elif strategy == "content":
            recommender = get_hybrid_recommender(mode="content")
        else:
            recommender = get_hybrid_recommender(mode="hybrid")
        recommender_items = recommender.recommend(
            learner_id,
            top_k=top_k,
            context={"recent_impressions": impressions},
        )
    except Exception:  # pragma: no cover - recommender failure fallback
        logger.exception(
            "failed to fetch recommendations for feature vector",
            extra={"learner_id": learner_id, "strategy": strategy},
        )
        recommender_items = []
        recommender_error = "recommender_error"

    # Tag recommender candidates with source for provenance tracking.
    recommender_items = [
        {**item, "source": item.get("source", "hybrid_recommender")}
        for item in recommender_items
        if isinstance(item, Mapping)
    ]

    # --- LLM feedback candidate merge (additive, never blocks pipeline) ---
    if is_llm_feedback_enabled():
        try:
            from ..models.llm.feedback_generator import LLMFeedbackGenerator

            llm_gen = LLMFeedbackGenerator()
            llm_candidates = llm_gen.generate(
                mastery=mastery_map,
                metadata={
                    "days_since_last_engagement": None,  # placeholder, computed below
                    "confusion_flag": False,
                    "frustration_flag": False,
                },
            )
            # Re-generate with real metadata once we have it (avoid circular
            # dependency: metadata needs recommendations, but LLM needs metadata).
            # Instead, build a lightweight metadata subset for the prompt.
            _llm_meta: dict = {}
            if live_code_events:
                _llm_behavioural = _compute_behavioural_features_from_live_code(live_code_events)
                _llm_meta.update(_llm_behavioural)
            _llm_affect = _compute_affect_flags(
                _llm_meta, sentiment_mean
            )
            _llm_meta.update(_llm_affect)
            # Compute engagement recency for prompt context
            _latest_eng = _latest_timestamp(clicks)
            _latest_comp = _latest_timestamp(completions)
            if _latest_comp is not None and (_latest_eng is None or _latest_comp > _latest_eng):
                _latest_eng = _latest_comp
            if _latest_eng is None:
                _llm_meta["days_since_last_engagement"] = float("inf")
            else:
                _delta = datetime.now(timezone.utc) - _latest_eng
                _llm_meta["days_since_last_engagement"] = max(_delta.total_seconds() / 86400.0, 0.0)

            llm_candidates = llm_gen.generate(
                mastery=mastery_map,
                metadata=_llm_meta,
            )

            if llm_candidates:
                recommender_items = _merge_candidates(recommender_items, llm_candidates)
        except Exception:
            logger.exception(
                "LLM feedback generation failed; continuing with recommender-only candidates",
                extra={"learner_id": learner_id},
            )

    metadata = build_feature_metadata(
        mastery_map,
        goals,
        impressions,
        clicks,
        completions,
        recommender_items,
        strategy=strategy,
        top_k=top_k,
        cached=False,
        error=recommender_error,
        live_code_events=live_code_events,
        sentiment_mean=sentiment_mean,
    )

    feature_vector = FeatureVector(
        learner_id=learner_id,
        mastery=mastery_map,
        goals=goals,
        impressions=impressions,
        clicks=clicks,
        completions=completions,
        recommendations=list(recommender_items),
        metadata=metadata,
        generated_at=datetime.now(timezone.utc),
    )

    if cache:
        try:
            cache.setex(cache_key, ttl_seconds, feature_vector.to_json())
        except Exception:  # pragma: no cover
            logger.exception(
                "failed to cache feature vector", extra={"learner_id": learner_id}
            )

    return feature_vector


__all__ = ["build_feature_metadata", "build_feature_vector", "get_redis_client"]
