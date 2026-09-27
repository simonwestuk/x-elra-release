"""Post-study feature unlock router.

After the study period ends, control-group learners (arms A, B) are offered
access to the full feature set (explanations, sentiment analysis, etc.)
that was previously restricted to the treatment arm.

The unlock check considers:
1. Global study_end_date from config
2. Per-learner study duration (pilot_start_date + study_duration_weeks)
3. Manual pilot_mode override
"""

import datetime as dt
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...config import settings
from ...utils.db import (
    GroupAssignment,
    SessionLocal,
    User,
    utc_now,
)

logger = logging.getLogger(__name__)

router = APIRouter()
router_prefix = "/v1"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UnlockStatus(BaseModel):
    learner_id: str
    arm: Optional[str] = None
    study_ended: bool = False
    features_unlocked: bool = False
    unlock_reason: Optional[str] = None
    days_until_unlock: Optional[int] = None


@router.get("/study/unlock/{learner_id}", response_model=UnlockStatus)
def get_unlock_status(learner_id: str, db: Session = Depends(get_db)):
    """Check whether post-study features are unlocked for this learner."""
    user = db.query(User).filter(User.learner_id == learner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")

    ga = db.query(GroupAssignment).filter(GroupAssignment.learner_id == learner_id).first()
    arm = ga.arm if ga else None

    # 1. If pilot_mode is on, everything is unlocked
    if settings.pilot_mode:
        return UnlockStatus(
            learner_id=learner_id,
            arm=arm,
            study_ended=True,
            features_unlocked=True,
            unlock_reason="pilot_mode",
        )

    # 2. Treatment arm always has full features
    if arm == "T":
        return UnlockStatus(
            learner_id=learner_id,
            arm=arm,
            study_ended=False,
            features_unlocked=True,
            unlock_reason="treatment_arm",
        )

    # 3. Check if study has ended
    now = utc_now()
    end_date = _resolve_study_end(user)

    if end_date and now >= end_date:
        return UnlockStatus(
            learner_id=learner_id,
            arm=arm,
            study_ended=True,
            features_unlocked=True,
            unlock_reason="study_completed",
        )

    # Still in study period
    days_left = (end_date - now).days if end_date else None
    return UnlockStatus(
        learner_id=learner_id,
        arm=arm,
        study_ended=False,
        features_unlocked=False,
        days_until_unlock=days_left,
    )


def is_study_ended_for_learner(db: Session, learner_id: str) -> bool:
    """Utility: check if the study period is over for a learner.

    Can be called from other routers (e.g., recommend) to decide
    whether to override arm-based feature restrictions.
    """
    if settings.pilot_mode:
        return True

    user = db.query(User).filter(User.learner_id == learner_id).first()
    if not user:
        return False

    end_date = _resolve_study_end(user)
    if end_date is None:
        return False

    return utc_now() >= end_date


def _resolve_study_end(user) -> Optional[dt.datetime]:
    """Determine when the study ends for a given user."""
    # Explicit end date takes priority
    if settings.study_end_date:
        try:
            d = dt.datetime.strptime(settings.study_end_date, "%Y-%m-%d")
            return d.replace(tzinfo=dt.timezone.utc)
        except ValueError:
            logger.warning("Invalid STUDY_END_DATE: %s", settings.study_end_date)

    # Derive from pilot start + duration
    if settings.pilot_start_date:
        try:
            start = dt.datetime.strptime(settings.pilot_start_date, "%Y-%m-%d")
            start = start.replace(tzinfo=dt.timezone.utc)
            return start + dt.timedelta(weeks=settings.study_duration_weeks)
        except ValueError:
            pass

    # Derive from user signup + duration
    if user and user.created_at:
        signup = user.created_at
        if signup.tzinfo is None:
            signup = signup.replace(tzinfo=dt.timezone.utc)
        return signup + dt.timedelta(weeks=settings.study_duration_weeks)

    return None
