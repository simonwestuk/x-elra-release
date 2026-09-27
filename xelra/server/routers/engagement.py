"""Engagement monitoring and reminder router.

Provides:
- Attrition risk endpoint (identifies inactive learners)
- Background task for sending weekly engagement reminders
- Admin endpoint to view engagement stats
"""

import datetime as dt
import logging
from typing import Optional

import hmac
import os

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from ...config import settings
from ...utils.db import (
    Completion,
    Click,
    ReminderConfig,
    ReminderLog,
    SessionLocal,
    User,
    utc_now,
)

logger = logging.getLogger(__name__)

router = APIRouter()
router_prefix = "/v1"


def _get_reminder_config(db: Session) -> ReminderConfig:
    """Return the singleton ReminderConfig row, creating defaults if needed."""
    cfg = db.query(ReminderConfig).first()
    if cfg is None:
        cfg = ReminderConfig(id=1)
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


def _admin_api_key_guard(authorization: str = Header(None)):
    """Require GDPR_API_KEY for admin endpoints."""
    expected = os.getenv("GDPR_API_KEY", "")
    if not expected:
        raise HTTPException(status_code=403, detail="Admin API key not configured")
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

# Fallback thresholds (used only if DB config not yet created)
_DEFAULT_WARNING_DAYS = 7
_DEFAULT_CRITICAL_DAYS = 14


class EngagementStatus(BaseModel):
    learner_id: str
    last_activity: Optional[str] = None
    days_inactive: int = 0
    risk_level: str = "active"  # active | warning | critical | lost
    total_completions: int = 0
    reminders_sent: int = 0


class EngagementSummary(BaseModel):
    total_learners: int = 0
    active: int = 0
    warning: int = 0
    critical: int = 0
    lost: int = 0


@router.get("/engagement/status/{learner_id}", response_model=EngagementStatus)
def get_engagement_status(learner_id: str, db: Session = Depends(get_db)):
    """Check engagement status for a single learner."""
    user = db.query(User).filter(User.learner_id == learner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")

    cfg = _get_reminder_config(db)
    return _compute_status(db, learner_id, cfg.warning_days, cfg.critical_days)


@router.get("/engagement/summary", response_model=EngagementSummary)
def get_engagement_summary(db: Session = Depends(get_db), _auth=Depends(_admin_api_key_guard)):
    """Admin endpoint: get attrition summary across all learners."""
    cfg = _get_reminder_config(db)
    users = db.query(User.learner_id).all()
    summary = EngagementSummary(total_learners=len(users))

    for (lid,) in users:
        status = _compute_status(db, lid, cfg.warning_days, cfg.critical_days)
        if status.risk_level == "active":
            summary.active += 1
        elif status.risk_level == "warning":
            summary.warning += 1
        elif status.risk_level == "critical":
            summary.critical += 1
        else:
            summary.lost += 1

    return summary


@router.post("/engagement/send_reminder/{learner_id}")
def send_reminder(learner_id: str, db: Session = Depends(get_db), _auth=Depends(_admin_api_key_guard)):
    """Manually trigger an engagement reminder for a learner."""
    user = db.query(User).filter(User.learner_id == learner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")

    cfg = _get_reminder_config(db)
    status = _compute_status(db, learner_id, cfg.warning_days, cfg.critical_days)
    if status.risk_level == "active":
        return {"sent": False, "reason": "Learner is currently active."}

    result = _send_engagement_email(user.email, learner_id, status, cfg)
    if result["success"]:
        log = ReminderLog(
            learner_id=learner_id,
            reminder_type=f"inactive_{status.days_inactive}d",
        )
        db.add(log)
        db.commit()

    return {"sent": result["success"], "provider": result.get("provider"), "error": result.get("error")}


def _compute_status(
    db: Session,
    learner_id: str,
    warning_days: int = _DEFAULT_WARNING_DAYS,
    critical_days: int = _DEFAULT_CRITICAL_DAYS,
) -> EngagementStatus:
    """Compute engagement status for a learner."""
    now = utc_now()

    # Find most recent activity across completions and clicks
    last_completion = db.query(func.max(Completion.created_at)).filter(
        Completion.learner_id == learner_id
    ).scalar()

    last_click = db.query(func.max(Click.created_at)).filter(
        Click.learner_id == learner_id
    ).scalar()

    dates = [d for d in [last_completion, last_click] if d is not None]
    last_activity = max(dates) if dates else None

    # Fall back to the user's sign-up date when there is no activity yet,
    # so new users show realistic days since registration instead of 999.
    if last_activity is None:
        user = db.query(User).filter(User.learner_id == learner_id).first()
        if user and user.created_at:
            last_activity = user.created_at

    if last_activity and last_activity.tzinfo is None:
        last_activity = last_activity.replace(tzinfo=dt.timezone.utc)

    days_inactive = (now - last_activity).days if last_activity else 0

    if days_inactive <= 3:
        risk = "active"
    elif days_inactive <= warning_days:
        risk = "warning"
    elif days_inactive <= critical_days:
        risk = "critical"
    else:
        risk = "lost"

    total_completions = db.query(func.count(Completion.id)).filter(
        Completion.learner_id == learner_id
    ).scalar() or 0

    reminders_sent = db.query(func.count(ReminderLog.id)).filter(
        ReminderLog.learner_id == learner_id
    ).scalar() or 0

    return EngagementStatus(
        learner_id=learner_id,
        last_activity=last_activity.isoformat() if last_activity else None,
        days_inactive=days_inactive,
        risk_level=risk,
        total_completions=total_completions,
        reminders_sent=reminders_sent,
    )


def _send_engagement_email(
    to_email: str,
    learner_id: str,
    status: EngagementStatus,
    cfg: Optional[ReminderConfig] = None,
) -> dict:
    """Send an engagement reminder email."""
    import httpx

    if not settings.resend_api_key:
        # Fall back to logging if no email provider
        logger.info(
            "Engagement reminder (no email provider): learner=%s days_inactive=%d",
            learner_id,
            status.days_inactive,
        )
        return {"success": True, "provider": "log_only"}

    # Use admin-configured content when available, otherwise defaults
    subject = cfg.email_subject if cfg else "We miss you on X-ELRA!"
    heading = cfg.email_heading if cfg else "Keep your learning momentum going"
    body_text = (cfg.email_body if cfg else "").format(
        days_inactive=status.days_inactive,
        total_completions=status.total_completions,
    ) if cfg else (
        f"It's been {status.days_inactive} days since your last activity on X-ELRA. "
        f"You've completed {status.total_completions} item(s) so far — great work!\n\n"
        "New recommendations are waiting for you. Pop in for just a few minutes to "
        "continue building your skills."
    )
    cta_text = cfg.email_cta_text if cfg else "Continue Learning"

    # Convert newlines in body to HTML paragraphs
    body_paragraphs = "".join(
        f'<p style="color:#666;margin-bottom:16px;">{p.strip()}</p>'
        for p in body_text.split("\n\n") if p.strip()
    )

    html = f"""
    <div style="font-family:system-ui,sans-serif;max-width:480px;margin:0 auto;padding:24px;">
        <h2 style="color:#111;margin-bottom:8px;">{heading}</h2>
        {body_paragraphs}
        <div style="text-align:center;margin-bottom:24px;">
            <a href="{_app_url()}" style="display:inline-block;padding:12px 28px;background:#4c6ef5;color:#fff;text-decoration:none;border-radius:8px;font-weight:600;">
                {cta_text}
            </a>
        </div>
        <p style="color:#999;font-size:13px;">
            You're receiving this because you signed up for X-ELRA. If you'd like to stop
            these reminders, withdraw your consent in the app or email us at
            <a href="mailto:Simon.West@port.ac.uk" style="color:#2563eb;">Simon.West@port.ac.uk</a>.
        </p>
    </div>
    """

    text = (
        f"{body_text}\n\n"
        f"{cta_text}: {_app_url()}\n\n"
        "To stop reminders, withdraw consent or email Simon.West@port.ac.uk."
    )

    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.resend_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": settings.resend_from_email,
                "to": [to_email],
                "subject": subject,
                "html": html,
                "text": text,
            },
            timeout=10.0,
        )
        if response.status_code == 200:
            return {"success": True, "provider": "resend"}
        return {"success": False, "provider": "resend", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "provider": "resend", "error": str(e)}


def _app_url() -> str:
    """Return the application URL (best-effort)."""
    base = getattr(settings, "app_base_url", None) or "https://xelra-learning.com"
    return f"{base}/static/web/standalone.html"


# ---------------------------------------------------------------------------
# Background task: run_engagement_check
# Called from app.py lifespan alongside the sentiment aggregator.
# ---------------------------------------------------------------------------

async def run_engagement_check_once():
    """Check all learners and send reminders to inactive ones.

    Called periodically from the background loop in app.py.
    Returns the configured check_interval_hours so the loop can adapt.
    """
    from ...utils.db import SessionLocal

    interval_hours = 24  # fallback
    session = SessionLocal()
    try:
        cfg = _get_reminder_config(session)
        interval_hours = cfg.check_interval_hours

        if not cfg.enabled:
            logger.info("Engagement reminders disabled by admin config")
            return interval_hours

        users = session.query(User).all()
        sent = 0
        for user in users:
            status = _compute_status(
                session, user.learner_id, cfg.warning_days, cfg.critical_days
            )
            if status.risk_level in ("warning", "critical"):
                # Check cooldown
                recent = session.query(ReminderLog).filter(
                    ReminderLog.learner_id == user.learner_id,
                    ReminderLog.sent_at >= utc_now() - dt.timedelta(days=cfg.cooldown_days),
                ).first()
                if recent:
                    continue

                result = _send_engagement_email(user.email, user.learner_id, status, cfg)
                if result["success"]:
                    log = ReminderLog(
                        learner_id=user.learner_id,
                        reminder_type=f"auto_{status.risk_level}",
                    )
                    session.add(log)
                    sent += 1

        session.commit()
        if sent:
            logger.info("Engagement check: sent %d reminder(s)", sent)
    except Exception as e:
        logger.error("Engagement check failed: %s", e)
        session.rollback()
    finally:
        session.close()

    return interval_hours
