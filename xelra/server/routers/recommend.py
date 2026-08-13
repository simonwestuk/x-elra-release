"""Recommendation API routes, filtering logic, and explanation payload assembly."""

import hashlib
import json
import logging
import math
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator, model_validator
from typing import Any, Dict, List, Literal, Optional
from functools import lru_cache
from sqlalchemy.orm import selectinload
from ...config import settings
from ...models.recommender.factory import (
    get_hybrid_recommender,
    get_sequence_recommender,
)
from ...models.xai.explain import ExplanationService
from ...olm.service import (
    explain_with_olm,
    get_skill_catalogue,
    learner_mastery_map,
)
from ...utils.db import (
    SessionLocal,
    Impression,
    get_or_assign_arm,
    Click,
    Completion,
    Feedback,
    Item,
    ItemSkill,
    ARLDecision,
    ARLOutcome,
    FeatureSnapshot,
    User,
)
from ...data.loader import load_items

logger = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache(maxsize=None)
def get_recommender_instance(strategy: str):
    # Builds and caches a recommender per strategy on first use
    if strategy == "content":
        return get_hybrid_recommender(mode="content")
    if strategy in {"hybrid", "hybrid_plus"}:
        return get_hybrid_recommender(mode="hybrid", w_base=0.6, w_sent=0.2, w_cf=0.2)
    if strategy == "hybrid_nosent":
        return get_hybrid_recommender(mode="hybrid", w_base=0.8, w_sent=0.0, w_cf=0.2)
    if strategy == "sequence":
        return get_sequence_recommender()
    # default
    return get_hybrid_recommender(mode="popularity")


# Single explanation service instance reused for all requests
xai_service = ExplanationService(use_shap=True)

# Progression configuration flags
MASTERY_TOL = 1e-6
LEVEL_FALLBACK_ENABLED = True
LEVEL_FALLBACK_RADIUS = 1
RELAX_COMPLETION_IF_EMPTY = True
FAIL_OPEN_ON_FILTER_ERROR = True
MAX_TOP_K = 500


def _parse_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            loaded = json.loads(text)
        except Exception:
            loaded = None
        if isinstance(loaded, (list, tuple, set)):
            return [str(v).strip() for v in loaded if str(v).strip()]
        if "," in text:
            parts = text.split(",")
        else:
            parts = text.split()
        return [part.strip() for part in parts if part.strip()]
    return [str(value).strip()]


def _normalize_tags(value: Any) -> List[str]:
    tags = [tag.lower() for tag in _parse_str_list(value) if tag]
    # Preserve deterministic ordering
    return sorted({tag for tag in tags if tag})


def _prereqs_satisfied(prereq_value: Any, completed_ids: set[str]) -> bool:
    prereqs = [pr for pr in _parse_str_list(prereq_value) if pr]
    if not prereqs:
        return True
    if not completed_ids and RELAX_COMPLETION_IF_EMPTY:
        return True
    return set(prereqs).issubset(completed_ids)


def _max_skill_level(item) -> Optional[int]:
    levels: List[int] = []
    for rel in getattr(item, "item_skills", []) or []:
        skill = getattr(rel, "skill", None)
        if skill is None:
            continue
        level = getattr(skill, "level", None)
        if level is None:
            continue
        try:
            levels.append(int(level))
        except Exception:
            continue
    if not levels:
        return None
    return max(levels)


def _apply_catalog_filters(
    db,
    candidate_ids: Optional[set[str]],
    *,
    required_tags: Optional[List[str]] = None,
    max_difficulty: Optional[int] = None,
    completed_ids: Optional[set[str]] = None,
):
    if db is None:
        return candidate_ids
    completed_ids = completed_ids or set()
    require_prereq_check = bool(completed_ids) or not RELAX_COMPLETION_IF_EMPTY
    if (
        candidate_ids is None
        and not required_tags
        and max_difficulty is None
        and not require_prereq_check
    ):
        return candidate_ids
    try:
        query = db.query(Item)
        if candidate_ids is not None:
            if not candidate_ids:
                return set()
            query = query.filter(Item.item_id.in_(candidate_ids))
        items = query.options(
            selectinload(Item.item_skills).selectinload(ItemSkill.skill)
        ).all()
    except Exception:
        logger.exception("failed to materialize catalogue items for filtering")
        if FAIL_OPEN_ON_FILTER_ERROR:
            return candidate_ids
        return set()

    filtered: set[str] = set()
    required_tags_set = set(required_tags or [])

    for item in items:
        iid = getattr(item, "item_id", None)
        if not iid:
            continue
        if not _prereqs_satisfied(getattr(item, "prereqs", None), completed_ids):
            continue
        if required_tags_set:
            item_tags = set(_normalize_tags(getattr(item, "topics", None)))
            if not required_tags_set.issubset(item_tags):
                continue
        if max_difficulty is not None:
            max_level = _max_skill_level(item)
            if max_level is not None and max_level > max_difficulty:
                continue
        filtered.add(str(iid))

    if candidate_ids is None:
        return filtered
    return filtered


def _canonicalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _canonicalize_value(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonicalize_value(v) for v in value]
    if isinstance(value, set):
        return sorted(_canonicalize_value(v) for v in value)
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return str(value)
        normalized = float(f"{value:.12g}")
        return 0.0 if normalized == -0.0 else normalized
    if isinstance(value, (int, bool)) or value is None:
        return value
    if isinstance(value, str):
        return value
    try:
        converted = float(value)
    except Exception:
        return str(value)
    normalized = float(f"{converted:.12g}")
    return 0.0 if normalized == -0.0 else normalized


def _extract_diversity_payload(
    item: Dict[str, Any], components: Dict[str, Any]
) -> Any:
    for key in ("diversity_penalty", "diversity_penalties"):
        if key in item and item[key] is not None:
            return item[key]
        if key in components and components[key] is not None:
            return components[key]
    return None


# The hybrid recommender uses long lowercase names (content, cf, …) while
# the explanation layer and reasons builder expect short uppercase keys
# (C, CF, …).  This mapping bridges the two conventions.
_LONG_TO_SHORT: Dict[str, str] = {
    "content": "C",
    "cf": "CF",
    "popularity": "P",
    "sentiment": "S",
    "diversity": "D",
}


def _normalise_component_keys(d: Dict[str, Any]) -> Dict[str, Any]:
    """Copy *d* mapping long recommender names to short component keys."""
    out: Dict[str, Any] = {}
    for key, value in d.items():
        short = _LONG_TO_SHORT.get(key, key)
        if short not in out:
            out[short] = value
    return out


def _build_canonical_snapshots(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    snapshots: List[Dict[str, Any]] = []
    for rank, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        components = item.get("components")
        if not isinstance(components, dict):
            components = {}
        weights = components.get("weights")
        policy_weights = components.get("policy_weights")
        routine_weights = components.get("routine_weights")
        if isinstance(weights, dict):
            weights_payload: Dict[str, Any] = dict(weights)
        elif weights is None:
            weights_payload = {}
        else:
            weights_payload = {"value": weights}
        if isinstance(policy_weights, dict):
            weights_payload["policy_weights"] = dict(policy_weights)
        if isinstance(routine_weights, dict):
            weights_payload["routine_weights"] = dict(routine_weights)
        feature_payload = {
            k: v
            for k, v in components.items()
            if k not in {"weights", "policy_weights"}
        }
        diversity = _extract_diversity_payload(item, components)
        snapshots.append(
            {
                "rank": rank,
                "item_id": str(item.get("item_id", "")),
                "score": _canonicalize_value(item.get("score", 0.0)),
                "features": _canonicalize_value(feature_payload),
                "weights": _canonicalize_value(weights_payload),
                "diversity_penalty": _canonicalize_value(diversity),
            }
        )
    return snapshots


def _extract_model_versions(
    item: Dict[str, Any], snapshot: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    snapshot = snapshot or {}
    sources: List[Dict[str, Any]] = []
    features = snapshot.get("features")
    if isinstance(features, dict):
        sources.append(features)
    components = item.get("components")
    if isinstance(components, dict):
        sources.append(components)
    for src in sources:
        mv = src.get("model_versions") or src.get("model_version")
        if isinstance(mv, dict):
            return {str(k): str(v) for k, v in mv.items()}
    return {}


def _serialize_for_hash(
    snapshots: List[Dict[str, Any]], seed_value: Optional[int]
) -> str:
    payload = {
        "seed": _canonicalize_value(seed_value),
        "items": snapshots,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _build_telemetry_metadata(
    db,
    learner_id: str,
    routine_version: str,
    *,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    user_id: Optional[int] = None
    arm_key: Optional[str] = None

    if db is not None:
        try:
            arm_key = get_or_assign_arm(db, learner_id)
        except Exception:
            logger.exception(
                "failed to resolve arm assignment", extra={"learner_id": learner_id}
            )
        try:
            user = db.query(User).filter_by(learner_id=learner_id).one_or_none()
        except Exception:
            logger.exception(
                "failed to resolve user metadata", extra={"learner_id": learner_id}
            )
            user = None
        if user is not None:
            user_id = user.id

    metadata: Dict[str, Any] = {
        "user_id": user_id,
        "arm_key": arm_key,
        "policy_version": routine_version,
        "routine_version": routine_version,
        "schema_version": settings.telemetry_schema_version,
    }
    if request_id is not None:
        metadata["request_id"] = request_id
    return metadata


def _persist_decision(
    db,
    req: "RecRequest",
    decision_id: str,
    deterministic_hash: str,
    seed_value: Optional[int],
    response_payload: Dict[str, Any],
    snapshots: List[Dict[str, Any]],
    routine_version: str,
    request_id: Optional[str],
) -> None:
    try:
        request_dump = req.model_dump(mode="json", exclude_none=True)
    except AttributeError:  # pragma: no cover - backwards compatibility
        request_dump = req.dict()
    decision = ARLDecision(
        decision_id=decision_id,
        learner_id=req.learner_id,
        policy_name=req.strategy,
        policy_version=routine_version,
        deterministic_hash=deterministic_hash,
        seed=str(seed_value) if seed_value is not None else None,
        request_id=request_id,
        request_payload=json.dumps(
            request_dump, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ),
        response_payload=json.dumps(
            response_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ),
    )
    db.add(decision)
    db.flush()

    outcome_models: List[ARLOutcome] = []
    feature_snapshot_models: List[FeatureSnapshot] = []
    for snapshot in snapshots:
        diversity_json = (
            json.dumps(
                snapshot["diversity_penalty"],
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            if snapshot.get("diversity_penalty") is not None
            else None
        )
        features_json = (
            json.dumps(
                snapshot.get("features", {}),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            if snapshot.get("features") is not None
            else None
        )
        weights_json = (
            json.dumps(
                snapshot.get("weights", {}),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            if snapshot.get("weights") is not None
            else None
        )
        outcome_models.append(
            ARLOutcome(
                decision_id=decision.decision_id,
                item_id=snapshot.get("item_id", ""),
                rank=int(snapshot.get("rank", 0)),
                score=_canonicalize_value(snapshot.get("score")),
                features_json=features_json,
                weights_json=weights_json,
                metadata_json=diversity_json,
            )
        )
        feature_snapshot_models.append(
            FeatureSnapshot(
                decision_id=decision.decision_id,
                item_id=snapshot.get("item_id", ""),
                rank=int(snapshot.get("rank", 0)),
                features_json=features_json,
                weights_json=weights_json,
            )
        )
    if outcome_models:
        db.add_all(outcome_models)
    if feature_snapshot_models:
        db.add_all(feature_snapshot_models)
    db.commit()

class Context(BaseModel):
    course_id: Optional[str] = None
    time: Optional[str] = None


class RecRequest(BaseModel):
    learner_id: str
    context: Optional[Context] = None
    top_k: int = 10
    explain: bool = True
    explain_level: Literal["short", "detailed", "auto"] = "auto"
    strategy: Literal[
        "popularity",
        "content",
        "hybrid",
        "hybrid_nosent",
        "hybrid_plus",
        "sequence",
    ] = "popularity"
    strategy_flag: Optional[str] = None
    # NEW: allow client to request filtering of completed items
    exclude_completed: bool = False
    seed: Optional[int] = None
    sentiment_enabled: Optional[bool] = None
    weight_map: Optional[Dict[str, float]] = None
    policy_version: Optional[str] = None
    routine_version: Optional[str] = None
    xai_method: Optional[str] = None
    sentiment_provider: Optional[str] = None
    sentiment_model: Optional[str] = None
    required_tags: Optional[List[str]] = None
    max_difficulty: Optional[int] = None

    @field_validator("required_tags")
    @classmethod
    def _validate_required_tags(cls, value: Optional[List[str]]):
        if value is None:
            return None
        tags = [str(tag).strip().lower() for tag in value if str(tag).strip()]
        if not tags:
            raise ValueError("required_tags must contain at least one tag")
        return sorted(set(tags))

    @field_validator("max_difficulty")
    @classmethod
    def _validate_max_difficulty(cls, value: Optional[int]):
        if value is None:
            return None
        try:
            difficulty = int(value)
        except Exception as exc:  # pragma: no cover - defensive
            raise ValueError("max_difficulty must be an integer") from exc
        if difficulty < 0:
            raise ValueError("max_difficulty must be non-negative")
        return difficulty

    @model_validator(mode="after")
    def _sync_versions(self):
        resolved = self.routine_version or self.policy_version or settings.routine_version
        self.routine_version = resolved
        self.policy_version = resolved
        return self


class GroupRecRequest(BaseModel):
    learner_id: str
    group: str
    context: Optional[Context] = None
    top_k: int = 10
    explain_level: Literal["short", "detailed", "auto"] = "auto"


@router.post("/recommend/recommendations")
def recommend(req: RecRequest, db=Depends(get_db)):
    top_k = max(min(req.top_k, MAX_TOP_K), 0)
    fetch_k = top_k
    if req.exclude_completed and top_k > 0:
        fetch_k = min(top_k * 3, 200)

    # Compute progress and allowed items up front
    progress = {"active_level": None, "skills_at_level": []}
    allowed_ids: Optional[set[str]] = None
    if db is not None:
        try:
            skills = get_skill_catalogue(db)
            mastery = learner_mastery_map(db, req.learner_id)
        except Exception:
            logger.exception(
                "progress computation failed", extra={"learner_id": req.learner_id}
            )
            skills, mastery = [], {}
        by_level = {}
        for s in skills:
            if s.level is None:
                continue
            by_level.setdefault(s.level, []).append(s)
        active_level = None
        for lvl in sorted(by_level):
            lvl_skills = by_level[lvl]
            if any(mastery.get(s.id, 0.0) < 1.0 - MASTERY_TOL for s in lvl_skills):
                active_level = lvl
                break
        progress["active_level"] = active_level
        progress["skills_at_level"] = [s.id for s in by_level.get(active_level, [])]
        if progress["skills_at_level"]:
            try:
                item_rows = (
                    db.query(ItemSkill)
                    .filter(ItemSkill.skill_id.in_(progress["skills_at_level"]))
                    .all()
                )
                allowed_ids = {str(r.item_id) for r in item_rows}
                # Fail-open if mapping produced no items
                if not allowed_ids and FAIL_OPEN_ON_FILTER_ERROR:
                    allowed_ids = None
            except Exception:
                logger.exception(
                    "skill-to-item mapping failed", extra={"learner_id": req.learner_id}
                )
                allowed_ids = None if FAIL_OPEN_ON_FILTER_ERROR else set()

    # Completed set used for filtering and optional exclusion
    completed_ids: set[str] = set()
    if db is not None:
        try:
            comps = (
                db.query(Completion)
                .filter(Completion.learner_id == req.learner_id)
                .all()
            )
            completed_ids = {str(r.item_id) for r in comps if r.item_id}
        except Exception:
            logger.exception(
                "completion fetch failed", extra={"learner_id": req.learner_id}
            )
            completed_ids = set()

    allowed_ids = _apply_catalog_filters(
        db,
        allowed_ids,
        required_tags=req.required_tags,
        max_difficulty=req.max_difficulty,
        completed_ids=completed_ids,
    )

    seed_value = req.seed
    routine_version = req.routine_version or settings.routine_version

    # Build context for upstream filtering inside the recommender
    ctx = req.context.model_dump(exclude_none=True) if req.context else {}
    if allowed_ids is not None:
        ctx["allowed_item_ids"] = sorted(str(i) for i in allowed_ids)
    if req.exclude_completed and completed_ids:
        ctx["exclude_item_ids"] = sorted(str(i) for i in completed_ids)
    if req.required_tags:
        ctx["required_tags"] = list(req.required_tags)
    if req.max_difficulty is not None:
        ctx["max_difficulty"] = req.max_difficulty
    if seed_value is not None:
        ctx["_deterministic_seed"] = seed_value

    rec_engine = get_recommender_instance(req.strategy)

    global_sentiment_enabled = bool(
        getattr(settings, "feature_sentiment", True)
    ) and bool(getattr(settings, "infer_sentiment", True))
    request_sentiment_enabled = (
        req.sentiment_enabled
        if req.sentiment_enabled is not None
        else True
    )
    sentiment_allowed = global_sentiment_enabled and request_sentiment_enabled

    effective_weights: Optional[Dict[str, float]]
    if req.weight_map:
        effective_weights = dict(req.weight_map)
    else:
        effective_weights = None

    if not sentiment_allowed:
        disabled_weights = dict(effective_weights or {})
        disabled_weights["sentiment"] = 0.0
        effective_weights = disabled_weights

    items: List[Dict[str, Any]] = []
    # If progress is unavailable (e.g., no DB), fall back to recommending
    if progress["active_level"] is None:
        if db is not None and progress["skills_at_level"]:
            items = []
        else:
            items = rec_engine.recommend(
                req.learner_id, fetch_k, context=ctx, weights=effective_weights
            )
    else:
        items = rec_engine.recommend(
            req.learner_id, fetch_k, context=ctx, weights=effective_weights
        )

    raw_items = list((items or [])[:top_k])

    fb_map = {}
    if db is not None and raw_items:
        try:
            item_ids = [it.get("item_id") for it in raw_items if it.get("item_id")]
            rows = (
                db.query(Feedback)
                .filter(Feedback.learner_id == req.learner_id)
                .filter(Feedback.item_id.in_(item_ids))
                .all()
            )
            fb_map = {r.item_id: {"comment": r.text, "rating": r.rating} for r in rows}
        except Exception:
            fb_map = {}

    snapshots = _build_canonical_snapshots(raw_items)

    out_items: List[Dict[str, Any]] = []
    explanations_out: List[Dict[str, Any]] = []
    for rank, it in enumerate(raw_items):
        iid = it.get("item_id")
        if not iid:
            continue
        reasons = []
        raw_components = it.get("components", {}) or {}
        # Normalise long recommender names (content/cf/…) → short keys (C/CF/…)
        # for the reasons / explanation layer.  routine_weights keeps original
        # names since it documents the recommender's own effective weights.
        components = _normalise_component_keys(raw_components)
        weights_map = _normalise_component_keys(components.get("weights", {}) or {})
        breakdown = _normalise_component_keys(components.get("score_breakdown", {}) or {})
        routine_weights = raw_components.get("routine_weights", {}) or {}
        for key in ("C", "CF", "P", "S"):
            if key in components or key in breakdown:
                reasons.append(
                    {
                        "type": "component",
                        "component": key,
                        "value": float(components.get(key, 0.0)),
                        "weight": float(weights_map.get(key, 0.0)),
                        "contribution": float(
                            breakdown.get(
                                key,
                                float(components.get(key, 0.0))
                                * float(weights_map.get(key, 0.0)),
                            )
                        ),
                    }
                )
        if float(components.get("D", 0.0) or 0.0):
            reasons.append(
                {
                    "type": "penalty",
                    "component": "D",
                    "value": float(components.get("D", 0.0)),
                    "weight": float(weights_map.get("D", 0.0)),
                    "contribution": float(
                        breakdown.get(
                            "D",
                            -float(components.get("D", 0.0))
                            * float(weights_map.get("D", 0.0)),
                        )
                    ),
                }
            )

        snapshot = snapshots[rank] if rank < len(snapshots) else None
        xai = None
        if req.explain:
            try:
                provenance = {
                    "policy_version": routine_version,
                    "routine_version": routine_version,
                    "strategy": req.strategy,
                    "seed": seed_value,
                    "model_versions": _extract_model_versions(it, snapshot),
                }
                xai = xai_service.explain_item(
                    it,
                    level=req.explain_level,
                    snapshot=snapshot,
                    provenance=provenance,
                )
                if db is not None:
                    try:
                        olm_payload = explain_with_olm(
                            it.get("components", {}), iid, db, req.learner_id
                        )
                        if isinstance(olm_payload, dict):
                            provenance_bits = olm_payload.pop("provenance", None)
                            if isinstance(provenance_bits, dict):
                                prov = xai.setdefault("provenance", {})
                                for key, value in provenance_bits.items():
                                    if (
                                        isinstance(value, dict)
                                        and isinstance(prov.get(key), dict)
                                    ):
                                        prov[key].update(value)
                                    else:
                                        prov[key] = value
                            xai.update(olm_payload)
                    except Exception:
                        logger.warning("olm explanation failed", exc_info=True)
            except Exception:
                logger.exception("xai generation failed", extra={"item_id": iid})
                xai = None
        fb = fb_map.get(iid, {})
        out_items.append(
            {
                "item_id": iid,
                "title": it.get("title", ""),
                "url": it.get("url", ""),
                "score": it.get("score", 0.0),
            }
        )
        explanations_out.append(
            {
                "item_id": iid,
                "rank": len(out_items) - 1,
                "reasons": reasons,
                "components": components,
                "weights": weights_map,
                "policy_weights": components.get("policy_weights", {}),
                "routine_weights": routine_weights,
                "score_breakdown": breakdown,
                "xai": xai,
                "feedback": {
                    "comment": fb.get("comment", ""),
                    "rating": fb.get("rating"),
                },
            }
        )
    serialized = _serialize_for_hash(snapshots, seed_value)
    deterministic_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    decision_id = str(uuid4())
    request_id = str(uuid4())

    telemetry_metadata = _build_telemetry_metadata(
        db, req.learner_id, routine_version, request_id=request_id
    )
    arm_key = telemetry_metadata.get("arm_key")

    if req.explain:
        for entry in explanations_out:
            xai_payload = entry.get("xai")
            if isinstance(xai_payload, dict):
                prov = xai_payload.setdefault("provenance", {})
                prov["decision_id"] = decision_id
                prov["deterministic_hash"] = deterministic_hash

    response_body = {
        "learner_id": req.learner_id,
        "strategy": req.strategy,
        "items": out_items,
        "explanations": explanations_out,
        "progress": progress,
        "decision_id": decision_id,
        "deterministic_hash": deterministic_hash,
        "policy_version": routine_version,
        "routine_version": routine_version,
        "arm": arm_key,
        "request_id": request_id,
        "telemetry": telemetry_metadata,
    }

    if db is not None:
        try:
            _persist_decision(
                db=db,
                req=req,
                decision_id=decision_id,
                deterministic_hash=deterministic_hash,
                seed_value=seed_value,
                response_payload=response_body,
                snapshots=snapshots,
                routine_version=routine_version,
                request_id=request_id,
            )
        except Exception:
            db.rollback()
            logger.exception(
                "failed to log recommendation decision",
                extra={"learner_id": req.learner_id, "decision_id": decision_id},
            )

    logger.info(
        "recommendation decision generated",
        extra={
            "decision_id": decision_id,
            "deterministic_hash": deterministic_hash,
            "policy_version": routine_version,
            "learner_id": req.learner_id,
            "strategy": req.strategy,
            "item_count": len(out_items),
            "request_id": request_id,
        },
    )

    return response_body


@router.post("/recommend/recommendations/by_group")
def recommend_by_group(req: GroupRecRequest, db=Depends(get_db)):
    from ...experiment.groups import ExperimentGroup
    from ...config import get_arm_buckets

    identifier = req.group
    group = None
    if isinstance(identifier, str):
        try:
            group = ExperimentGroup[identifier]
        except KeyError:
            try:
                group = ExperimentGroup(identifier)
            except ValueError:
                buckets = get_arm_buckets()
                slug = buckets.get(identifier.upper()) if identifier else None
                if slug:
                    group = ExperimentGroup(slug)
    if group is None:
        raise HTTPException(status_code=400, detail=f"Unknown experiment group '{req.group}'")
    rec_req = group.to_request(
        learner_id=req.learner_id,
        top_k=req.top_k,
        context=req.context,
        explain_level=req.explain_level,
    )
    return recommend(rec_req, db)


class NextUpRequest(BaseModel):
    learner_id: str
    course_id: str | None = None
    top_k: int = 1  # keep interface symmetric, though we return 1


@router.post("/recommend/next_up")
def next_up(req: NextUpRequest, db=Depends(get_db)):
    # compute the next uncompleted item by sequence_order (optionally course-scoped)
    df = load_items().copy()
    if req.course_id:
        try:
            df = df[df["course_id"] == req.course_id]
        except Exception:
            pass
    if df.empty:
        return {"item": None}
    # Ensure sequence column
    import pandas as pd, numpy as np

    if "sequence_order" not in df.columns:
        df["sequence_order"] = np.arange(1, len(df) + 1)
    df["sequence_order"] = pd.to_numeric(df["sequence_order"], errors="coerce").fillna(
        1e9
    )
    # Completed set
    comps = (
        db.query(Completion)
        .filter(Completion.learner_id == req.learner_id)
        .all()
    )
    completed = {r.item_id for r in comps}
    # pick first item not completed, with lowest sequence_order
    df_nc = df[~df["item_id"].astype(str).isin(completed)].copy()
    if df_nc.empty:
        # all done; fall back to the first item (or None)
        df_nc = df.sort_values("sequence_order", ascending=True)
    row = (
        df_nc.sort_values("sequence_order", ascending=True)
        .head(1)
        .to_dict(orient="records")[0]
    )
    item = {
        "item_id": row.get("item_id"),
        "title": row.get("title"),
        "url": row.get("url", ""),
        "sequence_order": (
            int(row.get("sequence_order"))
            if pd.notna(row.get("sequence_order"))
            else None
        ),
    }
    routine_version = settings.routine_version
    request_id = str(uuid4())
    telemetry_metadata = _build_telemetry_metadata(
        db, req.learner_id, routine_version, request_id=request_id
    )
    return {
        "item": item,
        "request_id": request_id,
        "telemetry": telemetry_metadata,
        "arm": telemetry_metadata.get("arm_key"),
    }


@router.get("/recommend/completed/{learner_id}")
def completed_items(learner_id: str, db=Depends(get_db), limit: int = 200):
    # fetch clicks marked as complete
    rows = (
        db.query(Completion)
        .filter(Completion.learner_id == learner_id)
        .all()
    )

    # de-duplicate by item_id, keep latest if possible
    def get_when(r):
        for attr in ("created_at", "timestamp", "ts"):
            if hasattr(r, attr):
                return getattr(r, attr)
        return None

    latest_by_item = {}
    for r in rows:
        key = r.item_id
        t = get_when(r)
        if key not in latest_by_item or (
            t and get_when(latest_by_item[key]) and t > get_when(latest_by_item[key])
        ):
            latest_by_item[key] = r
        elif key not in latest_by_item:
            latest_by_item[key] = r

    item_ids = list(latest_by_item.keys())[:limit]
    # map item metadata
    df = load_items().copy()
    meta = {}
    try:
        df["item_id"] = df["item_id"].astype(str)
        meta = df.set_index("item_id")[["title", "url"]].to_dict(orient="index")
    except Exception:
        pass

    items_out = []
    for iid in item_ids:
        m = meta.get(str(iid), {})
        when = get_when(latest_by_item[iid])
        items_out.append(
            {
                "item_id": str(iid),
                "title": m.get("title", ""),
                "url": m.get("url", ""),
                "completed_at": when.isoformat() if when else None,
            }
        )
    return {"learner_id": learner_id, "items": items_out}
