"""
Survey router for periodic pilot study surveys.

Handles checking if a survey is due and marking surveys as completed.
Surveys are shown at configured weeks of the pilot study period.
"""

from __future__ import annotations

import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...config import settings
from ...utils.db import SessionLocal, User, SurveyCompletion, SurveyConfig, utc_now

router = APIRouter(prefix="/survey", tags=["survey"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SurveyStatusResponse(BaseModel):
    survey_due: bool
    survey_week: Optional[int] = None
    survey_url: Optional[str] = None
    enabled: bool = True
    code_required: bool = False


class SurveyCompleteRequest(BaseModel):
    learner_id: str
    survey_week: int
    code: Optional[str] = None


class SurveyCompleteResponse(BaseModel):
    ok: bool
    message: str


def parse_survey_weeks() -> list[int]:
    """Parse the comma-separated survey weeks from static config."""
    try:
        return [int(w.strip()) for w in settings.survey_weeks.split(",") if w.strip()]
    except (ValueError, AttributeError):
        return [4, 8, 12]


def parse_survey_codes() -> dict[int, str]:
    """Parse survey completion codes from env config.

    Format: '2:PILOT-W2,4:PILOT-W4'
    Returns dict mapping week number to required code.
    """
    codes = {}
    if not settings.survey_codes:
        return codes
    try:
        for pair in settings.survey_codes.split(","):
            pair = pair.strip()
            if ":" in pair:
                week_str, code = pair.split(":", 1)
                codes[int(week_str.strip())] = code.strip()
    except (ValueError, AttributeError):
        pass
    return codes


def get_survey_config(db: Session) -> Optional[SurveyConfig]:
    """Get survey config from database."""
    return db.query(SurveyConfig).first()


def is_code_required(db: Session) -> bool:
    """Check if completion code verification is required.

    Checks database config first, then falls back to env var.
    """
    config = get_survey_config(db)
    if config is not None and config.code_required:
        return True

    # Fall back to env var (if any codes configured)
    return bool(parse_survey_codes())


def get_expected_code(db: Session, week: int) -> Optional[str]:
    """Get the expected completion code for a given survey week.

    Checks database config first (single code for all weeks),
    then falls back to env var (per-week codes).
    """
    config = get_survey_config(db)
    if config is not None and config.code_required and config.completion_code:
        return config.completion_code

    # Fall back to env var per-week codes
    codes = parse_survey_codes()
    return codes.get(week)


def verify_survey_code(db: Session, week: int, code: Optional[str]) -> tuple[bool, str]:
    """Verify if the provided code matches the expected code for this week.

    Returns (is_valid, error_message).
    """
    if not is_code_required(db):
        return True, ""

    expected = get_expected_code(db, week)
    if not expected:
        # Code required but none configured for this week - allow through
        return True, ""

    if not code:
        return False, "Completion code required"

    if code.strip().upper() != expected.upper():
        return False, "Invalid completion code"

    return True, ""


def get_learner_week(learner_id: str, db: Session) -> int:
    """Calculate which week the learner is in for the study.

    Week 1 starts on day 0 (the pilot start date).
    Week 2 starts on day 7, etc.

    Returns:
        Current week number (1-based), or 0 if user not found or date is before pilot start.
    """
    user = db.query(User).filter(User.learner_id == learner_id).first()
    if not user or not user.created_at:
        return 0

    if settings.pilot_start_date:
        try:
            pilot_start = dt.datetime.strptime(settings.pilot_start_date, "%Y-%m-%d")
            pilot_start = pilot_start.replace(tzinfo=dt.UTC)
        except ValueError:
            pilot_start = user.created_at
    else:
        pilot_start = user.created_at

    if pilot_start.tzinfo is None:
        pilot_start = pilot_start.replace(tzinfo=dt.UTC)

    now = utc_now()
    delta = now - pilot_start
    if delta.days < 0:
        return 0
    weeks = (delta.days // 7) + 1
    return weeks


def get_completed_surveys(learner_id: str, db: Session) -> set[int]:
    """Get the set of survey weeks already completed by this learner."""
    completions = db.query(SurveyCompletion).filter(
        SurveyCompletion.learner_id == learner_id
    ).all()
    return {c.survey_week for c in completions}


def _learner_past_signup_delay(learner_id: str, db: Session) -> bool:
    """Check if learner has been signed up long enough for surveys.

    Returns True if the learner signed up at least
    ``settings.survey_signup_delay_days`` days ago.
    """
    delay = settings.survey_signup_delay_days
    if delay <= 0:
        return True

    user = db.query(User).filter(User.learner_id == learner_id).first()
    if not user or not user.created_at:
        return False

    created = user.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=dt.UTC)

    return (utc_now() - created).days >= delay


@router.get("/status/{learner_id}", response_model=SurveyStatusResponse)
def get_survey_status(learner_id: str, db: Session = Depends(get_db)):
    """Check if a survey is due for this learner.

    Returns survey_due=True if the learner is at or past a survey week
    and hasn't completed that survey yet.  Learners must also have been
    signed up for at least ``survey_signup_delay_days`` before any survey
    is shown, so late signups are not hit with a survey immediately.
    """
    if not settings.survey_enabled:
        return SurveyStatusResponse(survey_due=False, enabled=False)

    # Ensure learner has been signed up long enough
    if not _learner_past_signup_delay(learner_id, db):
        return SurveyStatusResponse(survey_due=False, enabled=True)

    survey_weeks = parse_survey_weeks()
    current_week = get_learner_week(learner_id, db)
    completed = get_completed_surveys(learner_id, db)

    for week in sorted(survey_weeks):
        if current_week >= week and week not in completed:
            return SurveyStatusResponse(
                survey_due=True,
                survey_week=week,
                survey_url=settings.survey_url,
                enabled=True,
                code_required=is_code_required(db),
            )

    return SurveyStatusResponse(survey_due=False, enabled=True)


@router.post("/complete", response_model=SurveyCompleteResponse)
def mark_survey_complete(req: SurveyCompleteRequest, db: Session = Depends(get_db)):
    """Mark a survey as completed for this learner."""
    existing = db.query(SurveyCompletion).filter(
        SurveyCompletion.learner_id == req.learner_id,
        SurveyCompletion.survey_week == req.survey_week,
    ).first()

    if existing:
        return SurveyCompleteResponse(ok=True, message="Survey already completed")

    survey_weeks = parse_survey_weeks()
    if req.survey_week not in survey_weeks:
        raise HTTPException(status_code=400, detail=f"Invalid survey week: {req.survey_week}")

    # Verify completion code if configured
    is_valid, error_msg = verify_survey_code(db, req.survey_week, req.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    completion = SurveyCompletion(
        learner_id=req.learner_id,
        survey_week=req.survey_week,
    )
    db.add(completion)
    db.commit()

    return SurveyCompleteResponse(ok=True, message=f"Week {req.survey_week} survey completed")


@router.get("/completions/{learner_id}")
def get_survey_completions(learner_id: str, db: Session = Depends(get_db)):
    """Get all survey completions for a learner."""
    completions = db.query(SurveyCompletion).filter(
        SurveyCompletion.learner_id == learner_id
    ).all()

    return {
        "learner_id": learner_id,
        "completed_weeks": [c.survey_week for c in completions],
        "current_week": get_learner_week(learner_id, db),
        "survey_weeks": parse_survey_weeks(),
    }


# --- Admin config endpoints ---


class SurveyConfigResponse(BaseModel):
    completion_code: Optional[str] = None
    code_required: bool = False


class SurveyConfigUpdate(BaseModel):
    completion_code: Optional[str] = None
    code_required: Optional[bool] = None


def _get_or_create_config(db: Session) -> SurveyConfig:
    """Get or create the survey config row."""
    cfg = db.query(SurveyConfig).first()
    if cfg is None:
        cfg = SurveyConfig(id=1)
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


class SurveyEnvConfigResponse(BaseModel):
    survey_weeks: list[int] = []
    survey_url: Optional[str] = None
    pilot_start_date: Optional[str] = None


@router.get("/env-config", response_model=SurveyEnvConfigResponse)
def get_env_config():
    """Get survey environment configuration (read-only values from env vars)."""
    return SurveyEnvConfigResponse(
        survey_weeks=parse_survey_weeks(),
        survey_url=settings.survey_url,
        pilot_start_date=settings.pilot_start_date,
    )


@router.get("/config", response_model=SurveyConfigResponse)
def get_config(db: Session = Depends(get_db)):
    """Get current survey configuration."""
    cfg = _get_or_create_config(db)
    return SurveyConfigResponse(
        completion_code=cfg.completion_code,
        code_required=cfg.code_required,
    )


@router.put("/config", response_model=SurveyConfigResponse)
def update_config(update: SurveyConfigUpdate, db: Session = Depends(get_db)):
    """Update survey configuration."""
    cfg = _get_or_create_config(db)

    if update.completion_code is not None:
        cfg.completion_code = update.completion_code.strip() if update.completion_code else None
    if update.code_required is not None:
        cfg.code_required = update.code_required

    cfg.updated_at = utc_now()
    db.commit()
    db.refresh(cfg)

    return SurveyConfigResponse(
        completion_code=cfg.completion_code,
        code_required=cfg.code_required,
    )
