"""Telemetry routes for consent, event logging, and GDPR deletion workflows."""

import copy
import datetime as dt
import json
import logging
from typing import Optional, Literal, List, Any, Dict

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field, ConfigDict, model_validator
from ...utils.db import (
    SessionLocal,
    LearnerConsent,
    Impression,
    ExplanationInteraction,
    Click,
    Completion,
    get_or_assign_arm,
    set_arm,
    OLMEvent,
    User,
    Reflection,
    LiveCodeEvent,
    purge_sentiment_for_learner,
)
from ...olm.service import record_progress_on_completion
from ...config import get_arm_buckets, get_arm_config, get_arms_manifest, settings
from ...arl.state import get_redis_client

router = APIRouter()

logger = logging.getLogger(__name__)


def _gdpr_api_key_guard(authorization: str = Header(None)):
    """Protect GDPR delete with a simple API key (set via GDPR_API_KEY env var)."""
    import hmac
    import os
    expected = os.getenv("GDPR_API_KEY", "")
    if not expected:
        raise HTTPException(status_code=403, detail="GDPR_API_KEY not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    token = authorization.split(" ", 1)[1]
    if not hmac.compare_digest(token, expected):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


LIVE_CODE_EVENT_TYPES = {
    "impression",
    "run",
    "success",
    "hint",
    "reflection",
    "arl_nudge",
}


class ConsentRequest(BaseModel):
    learner_id: str
    consent_given: bool


class GdprDeleteRequest(BaseModel):
    learner_id: str


@router.post("/telemetry/consent")
def set_consent(req: ConsentRequest, db=Depends(get_db)):
    rc = LearnerConsent(learner_id=req.learner_id, consent_given=req.consent_given)
    db.add(rc)
    purge_stats: Dict[str, int] = {}
    if not req.consent_given:
        purge_stats = purge_sentiment_for_learner(db, req.learner_id)
    db.commit()
    return {"ok": True, "purged": purge_stats}


@router.post("/telemetry/gdpr_delete", dependencies=[Depends(_gdpr_api_key_guard)])
def gdpr_delete(req: GdprDeleteRequest, db=Depends(get_db)):
    user = db.query(User).filter_by(learner_id=req.learner_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Learner not found")

    purge_stats = purge_sentiment_for_learner(db, req.learner_id)
    user_id = user.id

    db.delete(user)
    db.commit()

    logger.info(
        "GDPR delete executed",
        extra={
            "event": "telemetry.gdpr_delete",
            "learner_id": req.learner_id,
            "user_id": user_id,
            "purge_stats": purge_stats,
        },
    )

    return {"ok": True, "learner_id": req.learner_id, "purged": purge_stats}


@router.get("/telemetry/arm/{learner_id}")
def get_arm(learner_id: str, db=Depends(get_db)):
    arm = get_or_assign_arm(db, learner_id)
    return {"learner_id": learner_id, "arm": arm}


class TelemetryMetadata(BaseModel):
    user_id: int
    arm_key: str
    schema_version: str
    routine_version: Optional[str] = None
    policy_version: Optional[str] = None

    @model_validator(mode="after")
    def _sync_versions(self):
        resolved = self.routine_version or self.policy_version or settings.routine_version
        self.routine_version = resolved
        self.policy_version = resolved
        return self


class ExplainEvent(TelemetryMetadata):
    learner_id: str
    item_id: str
    action: Literal["expand", "collapse", "view"] = "view"
    source: Optional[str] = None
    rank: Optional[int] = None
    strategy: Optional[str] = None
    arm: Optional[str] = None
    course_id: Optional[str] = None
    level: Optional[Literal["short", "detailed"]] = None
    dwell_ms: Optional[int] = None


def _require_user(db, learner_id: str, user_id: int) -> User:
    user = db.query(User).filter_by(learner_id=learner_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Learner not found")
    if user.id != user_id:
        raise HTTPException(status_code=400, detail="user_id does not match learner")
    return user


@router.post("/telemetry/explanation")
def log_explanation(ev: ExplainEvent, db=Depends(get_db)):
    user = _require_user(db, ev.learner_id, ev.user_id)
    e = ExplanationInteraction(
        user_id=user.id,
        learner_id=ev.learner_id,
        item_id=ev.item_id,
        action=ev.action,
        source=ev.source,
        rank=ev.rank,
        strategy=ev.strategy,
        arm=ev.arm or ev.arm_key,
        arm_key=ev.arm_key,
        policy_version=ev.policy_version,
        schema_version=ev.schema_version,
        course_id=ev.course_id,
        level=ev.level,
        dwell_ms=ev.dwell_ms,
    )
    db.add(e)
    db.commit()
    return {"ok": True}


class ClickEvent(TelemetryMetadata):
    learner_id: str
    item_id: str
    action: Literal["click", "complete", "code_run"] = "click"
    source: Optional[str] = None
    rank: Optional[int] = None
    strategy: Optional[str] = None
    arm: Optional[str] = None
    course_id: Optional[str] = None
    request_id: Optional[str] = None


def _persist_completion(
    db,
    *,
    learner_id: str,
    item_id: str,
    user_id: int,
    arm_value: Optional[str],
    arm_key: str,
    routine_version: str,
    schema_version: str,
    source: Optional[str] = None,
    rank: Optional[int] = None,
    strategy: Optional[str] = None,
    course_id: Optional[str] = None,
    request_id: Optional[str] = None,
):
    comp = Completion(
        user_id=user_id,
        learner_id=learner_id,
        item_id=item_id,
        source=source,
        rank=rank,
        strategy=strategy,
        arm=arm_value,
        arm_key=arm_key,
        policy_version=routine_version,
        schema_version=schema_version,
        course_id=course_id,
        request_id=request_id,
    )
    db.add(comp)
    db.commit()
    record_progress_on_completion(db, learner_id, item_id)

    # Invalidate feature vector cache so next request reflects the new completion
    cache = get_redis_client()
    if cache:
        try:
            cache.delete(f"arl:feature:{learner_id}")
        except Exception:
            logger.warning(
                "Failed to invalidate feature cache after completion",
                extra={"learner_id": learner_id, "item_id": item_id},
            )

    return comp


@router.post("/telemetry/click")
def log_click(ev: ClickEvent, db=Depends(get_db)):
    user = _require_user(db, ev.learner_id, ev.user_id)
    if ev.action in ("click", "code_run"):
        c = Click(
            user_id=user.id,
            learner_id=ev.learner_id,
            item_id=ev.item_id,
            action=ev.action,
            source=ev.source,
            rank=ev.rank,
            strategy=ev.strategy,
            arm=ev.arm or ev.arm_key,
            arm_key=ev.arm_key,
            policy_version=ev.routine_version,
            schema_version=ev.schema_version,
            course_id=ev.course_id,
        )
        db.add(c)
        db.commit()
    else:
        _persist_completion(
            db,
            learner_id=ev.learner_id,
            item_id=ev.item_id,
            user_id=user.id,
            arm_value=ev.arm or ev.arm_key,
            arm_key=ev.arm_key,
            routine_version=ev.routine_version,
            schema_version=ev.schema_version,
            source=ev.source,
            rank=ev.rank,
            strategy=ev.strategy,
            course_id=ev.course_id,
            request_id=ev.request_id,
        )
    return {"ok": True}


class ArmOverride(BaseModel):
    learner_id: str
    arm: str  # 'T' (Treatment), 'A' (Control A), 'B' (Control B)


@router.post("/telemetry/arm")
def override_arm(req: ArmOverride, db=Depends(get_db), _auth=Depends(_gdpr_api_key_guard)):
    arm = req.arm.upper()
    if arm not in ["T", "A", "B"]:
        raise HTTPException(status_code=400, detail="Invalid arm. Use T (Treatment), A (Control A), or B (Control B).")
    set_arm(db, req.learner_id, arm)
    return {"ok": True, "learner_id": req.learner_id, "arm": arm}


@router.get("/telemetry/arms")
def list_arms(db=Depends(get_db), _auth=Depends(_gdpr_api_key_guard)):
    from ...utils.db import GroupAssignment

    rows = db.query(GroupAssignment).all()
    return [
        {"learner_id": r.learner_id, "arm": r.arm, "assigned_at": str(r.assigned_at)}
        for r in rows
    ]


@router.get("/telemetry/consent/{learner_id}")
def get_consent(learner_id: str, db=Depends(get_db)):
    row = (
        db.query(LearnerConsent)
        .filter_by(learner_id=learner_id, consent_given=True)
        .order_by(LearnerConsent.timestamp.desc())
        .first()
    )
    return {
        "learner_id": learner_id,
        "consent_given": bool(row is not None),
        "timestamp": str(row.timestamp) if row else None,
    }


class ImpressionItem(BaseModel):
    item_id: str
    rank: Optional[int] = None
    source: Optional[str] = None
    strategy: Optional[str] = None
    arm: Optional[str] = None
    course_id: Optional[str] = None
    request_id: Optional[str] = None


class ImpressionEvent(TelemetryMetadata):
    learner_id: str
    items: List[ImpressionItem]


@router.post("/telemetry/impression")
def impression(body: ImpressionEvent, db=Depends(get_db)):
    user = _require_user(db, body.learner_id, body.user_id)
    stored = 0
    for it in body.items:
        try:
            impr = Impression(
                user_id=user.id,
                learner_id=body.learner_id,
                item_id=it.item_id,
                source=it.source,
                rank=it.rank,
                strategy=it.strategy,
                arm=it.arm or body.arm_key,
                arm_key=body.arm_key,
                policy_version=body.routine_version,
                schema_version=body.schema_version,
                course_id=it.course_id,
                request_id=it.request_id,
            )
            db.add(impr)
            stored += 1
        except Exception:
            continue
    db.commit()
    return {"ok": True, "count": stored}


class CompletionEvent(TelemetryMetadata):
    learner_id: str
    item_id: str
    source: Optional[str] = None
    rank: Optional[int] = None
    strategy: Optional[str] = None
    arm: Optional[str] = None
    course_id: Optional[str] = None
    request_id: Optional[str] = None


@router.post("/telemetry/completion")
def completion(body: CompletionEvent, db=Depends(get_db)):
    user = _require_user(db, body.learner_id, body.user_id)
    _persist_completion(
        db,
        learner_id=body.learner_id,
        item_id=body.item_id,
        user_id=user.id,
        arm_value=body.arm or body.arm_key,
        arm_key=body.arm_key,
        routine_version=body.routine_version,
        schema_version=body.schema_version,
        source=body.source,
        rank=body.rank,
        strategy=body.strategy,
        course_id=body.course_id,
        request_id=body.request_id,
    )
    return {"ok": True}


class ReflectionEvent(TelemetryMetadata):
    learner_id: str
    text: str
    topic: Optional[str] = None
    item_id: Optional[str] = None
    prompt: Optional[str] = None
    sentiment: Optional[float] = None
    metadata: Optional[Any] = None


@router.post("/telemetry/reflection")
def log_reflection(body: ReflectionEvent, db=Depends(get_db)):
    user = _require_user(db, body.learner_id, body.user_id)
    metadata_json = None
    if body.metadata is not None:
        try:
            metadata_json = json.dumps(body.metadata)
        except TypeError:
            metadata_json = None
    reflection = Reflection(
        user_id=user.id,
        learner_id=body.learner_id,
        item_id=body.item_id,
        topic=body.topic,
        prompt=body.prompt,
        text=body.text,
        sentiment=body.sentiment,
        metadata_json=metadata_json,
        arm_key=body.arm_key,
        policy_version=body.routine_version,
        schema_version=body.schema_version,
    )
    db.add(reflection)
    db.commit()
    return {"ok": True, "reflection_id": reflection.id}


class LiveCodeEventPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    event: Optional[str] = None
    timestamp: Optional[dt.datetime] = None
    learner_id: Optional[str] = None
    item_id: Optional[str] = None
    attempt_id: Optional[str] = None
    session_id: Optional[str] = None
    engine: Optional[str] = None
    cell_id: Optional[str] = None
    code_size: Optional[int] = None
    status: Optional[str] = None
    duration_ms: Optional[int] = Field(default=None, ge=0)
    output_preview: Optional[str] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    response: Optional[str] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def _clip_preview(preview: Optional[str]) -> Optional[str]:
    if not preview:
        return None
    limit = int(getattr(settings, "live_code_max_output", 0) or 0)
    if limit > 0 and len(preview) > limit:
        return preview[:limit]
    return preview


@router.post("/telemetry/live/{event_name}")
def log_live_code_event(
    event_name: str, body: LiveCodeEventPayload, db=Depends(get_db)
):
    canonical = event_name.strip().lower()
    if canonical not in LIVE_CODE_EVENT_TYPES:
        raise HTTPException(status_code=404, detail="Unknown live code event")
    body_event = (body.event or "").strip().lower()
    if body.event and body_event != canonical:
        raise HTTPException(status_code=400, detail="Event name mismatch")

    learner_id = body.learner_id
    user_id = None
    if learner_id:
        user = db.query(User).filter_by(learner_id=learner_id).one_or_none()
        user_id = user.id if user else None

    event_at = body.timestamp or dt.datetime.now(dt.UTC)
    preview = _clip_preview(body.output_preview)

    record = LiveCodeEvent(
        user_id=user_id,
        learner_id=learner_id,
        item_id=body.item_id,
        attempt_id=body.attempt_id,
        session_id=body.session_id,
        event=canonical,
        cell_id=body.cell_id,
        engine=body.engine,
        status=body.status,
        code_size=body.code_size,
        duration_ms=body.duration_ms,
        output_preview=preview,
        error_type=body.error_type,
        error_message=body.error_message,
        response_text=body.response,
        message_text=body.message,
        event_at=event_at,
    )

    extra_payload: Dict[str, Any] = {}
    if body.metadata is not None:
        extra_payload["metadata"] = body.metadata
    model_extra = getattr(body, "model_extra", None)
    if model_extra:
        extras = {k: v for k, v in model_extra.items() if v is not None}
        if extras:
            extra_payload["extras"] = extras
    if extra_payload:
        try:
            record.extra_json = json.dumps(extra_payload)
        except TypeError:
            record.extra_json = json.dumps({"metadata": str(extra_payload)})

    db.add(record)
    db.commit()
    db.refresh(record)

    logger.info(
        "telemetry.live_code",
        extra={
            "event": canonical,
            "learner_id": learner_id,
            "item_id": body.item_id,
            "status": body.status,
        },
    )

    return {"ok": True, "event": canonical, "id": record.id}


class ArmReplayRequest(BaseModel):
    """Request payload for replaying deterministic arm assignments."""

    learner_ids: List[str]

    class Config:
        extra = "forbid"


class ArmSentimentSettings(BaseModel):
    """Sentiment analysis configuration for an experiment arm."""

    enabled: bool
    provider: Optional[str] = None
    model: Optional[str] = None

    class Config:
        extra = "forbid"


class ArmWeightMap(BaseModel):
    """Weighted contribution of the recommenders powering an arm."""

    content: float
    cf: float
    popularity: float
    sentiment: float

    class Config:
        extra = "forbid"


class ArmConfigSnapshot(BaseModel):
    """Normalised view of an experiment arm configuration."""

    name: str
    strategy: str
    explain: bool
    policy_version: str
    routine_version: str
    weight_map: ArmWeightMap
    sentiment: ArmSentimentSettings

    class Config:
        extra = "forbid"


class ArmReplayAssignment(BaseModel):
    """Replay payload for a single learner."""

    learner_id: str
    bucket: str
    arm: str
    config: ArmConfigSnapshot

    class Config:
        extra = "forbid"


class ArmsManifestSnapshot(BaseModel):
    """Serializable snapshot of the ARMS manifest served to clients."""

    policy: Dict[str, Any]
    buckets: Dict[str, str]
    weights: Dict[str, float]
    arms: Dict[str, Any]

    class Config:
        extra = "forbid"


class ArmReplayResponse(BaseModel):
    """Response envelope for arm replay requests."""

    manifest: ArmsManifestSnapshot
    assignments: List[ArmReplayAssignment]
    arms: List[ArmReplayAssignment] = Field(default_factory=list)

    class Config:
        extra = "forbid"


@router.post("/telemetry/arm/replay")
def replay_arms(body: ArmReplayRequest, db=Depends(get_db)) -> ArmReplayResponse:
    buckets = get_arm_buckets()
    manifest = get_arms_manifest()
    manifest_snapshot = {
        key: copy.deepcopy(value)
        for key, value in manifest.items()
        if key != "_arm_objects"
    }

    assignments: List[ArmReplayAssignment] = []
    for learner_id in body.learner_ids:
        bucket = get_or_assign_arm(db, learner_id)
        arm_slug = buckets.get(bucket)
        if not arm_slug:
            logger.error("No manifest arm mapped for bucket '%s'", bucket)
            raise HTTPException(
                status_code=422,
                detail="Arm configuration error for this learner",
            )
        cfg = get_arm_config(arm_slug)
        if not cfg.routine_version:
            logger.error("Arm '%s' missing routine_version", arm_slug)
            raise HTTPException(
                status_code=422,
                detail="Arm configuration error for this learner",
            )
        weight_map = ArmWeightMap(**dict(cfg.weight_map))
        sentiment = ArmSentimentSettings(
            enabled=cfg.sentiment_enabled,
            provider=cfg.sentiment_provider,
            model=cfg.sentiment_model,
        )
        config_snapshot = ArmConfigSnapshot(
            name=cfg.name,
            strategy=cfg.strategy,
            explain=cfg.explain,
            policy_version=cfg.policy_version,
            routine_version=cfg.routine_version,
            weight_map=weight_map,
            sentiment=sentiment,
        )
        assignments.append(
            ArmReplayAssignment(
                learner_id=learner_id,
                bucket=bucket,
                arm=arm_slug,
                config=config_snapshot,
            )
        )

    response = ArmReplayResponse(
        manifest=ArmsManifestSnapshot(**manifest_snapshot),
        assignments=assignments,
        arms=assignments,
    )
    return response


class OlmEvent(BaseModel):
    learner_id: str
    skill_id: str
    action: str = "goal_set"  # goal_set | goal_clear
    target: Optional[float] = None


@router.post("/telemetry/olm_event")
def olm_event(body: OlmEvent, db=Depends(get_db)):
    # Store in dedicated OLMEvent table (avoid FK to items)
    ev = OLMEvent(
        learner_id=body.learner_id,
        skill_id=body.skill_id,
        action=body.action,
        target=body.target,
    )
    db.add(ev)
    db.commit()
    return {"ok": True}
