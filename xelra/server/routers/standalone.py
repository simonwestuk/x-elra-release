"""Standalone email-code authentication routes for non-SSO learner access."""

import datetime as dt
import secrets

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, constr

from ...config import settings
from ...utils.auth import (
    issue_login_token,
    new_standalone_learner_id,
    verify_login_token,
)
from ...utils.db import SessionLocal, User, LoginCode, ConsentConfig, get_or_assign_arm, utc_now
from ...utils.email import send_otp_email

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CodeRequest(BaseModel):
    email: EmailStr


@router.post("/standalone/request_code")
def request_code(req: CodeRequest, db=Depends(get_db)):
    # Guard: demo learners
    if req.email.endswith("@example.com"):
        if not settings.demo_learners_enabled:
            raise HTTPException(
                status_code=403,
                detail="Demo accounts are currently disabled.",
            )

    # Guard: signup for unknown users
    u = db.query(User).filter_by(email=req.email).first()
    if not u:
        if not settings.signup_enabled:
            raise HTTPException(
                status_code=403,
                detail="New registrations are currently closed. Only existing users can sign in.",
            )

    code = f"{secrets.randbelow(1_000_000):06d}"
    expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
    rec = LoginCode(email=req.email, code=code, expires_at=expires)
    db.add(rec)
    # Ensure user exists with learner_id mapping
    if not u:
        learner_id = new_standalone_learner_id()
        u = User(email=req.email, learner_id=learner_id)
        db.add(u)
    db.commit()

    # Example learners (@example.com) can't receive real email;
    # always surface the code so demo users can log in directly.
    if req.email.endswith("@example.com"):
        return {
            "ok": True,
            "delivery": "dev",
            "note": "Example learner — code shown for demo login",
            "code": code,
        }

    # Send email via configured provider (Resend or SMTP)
    email_result = send_otp_email(req.email, code)

    if email_result["success"]:
        return {
            "ok": True,
            "delivery": "email",
            "provider": email_result.get("provider"),
        }
    else:
        # Email failed
        print(f"[standalone] Email send failed: {email_result.get('error')}")

        if settings.dev_mode:
            # Dev mode: return code in response for testing
            return {
                "ok": True,
                "delivery": "dev",
                "note": f"DEV MODE: Email failed ({email_result.get('error')})",
                "code": code,
            }
        else:
            # Production: don't reveal code, but still allow login attempt
            return {
                "ok": True,
                "delivery": "failed",
                "error": "Email delivery failed. Please try again or contact support.",
            }


class VerifyRequest(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6)


@router.post("/standalone/verify_code")
def verify_code(req: VerifyRequest, db=Depends(get_db)):
    rec = (
        db.query(LoginCode)
        .filter_by(email=req.email, code=req.code)
        .order_by(LoginCode.created_at.desc())
        .first()
    )
    now = dt.datetime.now(dt.timezone.utc)
    if not rec:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    expires_at = rec.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=dt.timezone.utc)
    if expires_at < now:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    # Invalidate the code so it cannot be reused
    db.delete(rec)
    db.flush()
    # Get/create user
    u = db.query(User).filter_by(email=req.email).first()
    if not u:
        raise HTTPException(
            status_code=400, detail="User not found after code creation"
        )
    u.last_login = dt.datetime.now(dt.timezone.utc)
    db.commit()
    arm = get_or_assign_arm(db, u.learner_id)
    token = issue_login_token(u.learner_id, arm_key=arm)
    return {"ok": True, "token": token, "learner_id": u.learner_id, "arm": arm}


class TokenRequest(BaseModel):
    token: str


@router.post("/standalone/me")
def me(req: TokenRequest):
    try:
        payload = verify_login_token(req.token)
        safe_fields = {"sub", "arm_key", "exp", "iss", "aud", "iat"}
        filtered_payload = {
            key: value for key, value in payload.items() if key in safe_fields
        }
        return {
            "ok": True,
            "learner_id": payload.get("sub"),
            "claims": filtered_payload,
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# --- Consent config endpoints ---


class ConsentConfigResponse(BaseModel):
    completion_code: str | None = None
    code_required: bool = False


class ConsentConfigUpdate(BaseModel):
    completion_code: str | None = None
    code_required: bool | None = None


class ConsentVerifyRequest(BaseModel):
    code: str


class ConsentVerifyResponse(BaseModel):
    valid: bool
    message: str


def _get_or_create_consent_config(db) -> ConsentConfig:
    """Get or create the consent config row."""
    cfg = db.query(ConsentConfig).first()
    if cfg is None:
        cfg = ConsentConfig(id=1)
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


@router.get("/standalone/consent/config", response_model=ConsentConfigResponse)
def get_consent_config(db=Depends(get_db)):
    """Get current consent configuration (public - returns if code required)."""
    cfg = _get_or_create_consent_config(db)
    return ConsentConfigResponse(
        completion_code=None,  # Don't expose the actual code to public endpoint
        code_required=cfg.code_required,
    )


@router.get("/standalone/consent/admin-config", response_model=ConsentConfigResponse)
def get_consent_admin_config(db=Depends(get_db)):
    """Get full consent configuration (admin only - includes actual code)."""
    cfg = _get_or_create_consent_config(db)
    return ConsentConfigResponse(
        completion_code=cfg.completion_code,
        code_required=cfg.code_required,
    )


@router.put("/standalone/consent/config", response_model=ConsentConfigResponse)
def update_consent_config(update: ConsentConfigUpdate, db=Depends(get_db)):
    """Update consent configuration."""
    cfg = _get_or_create_consent_config(db)

    if update.completion_code is not None:
        cfg.completion_code = update.completion_code.strip() if update.completion_code else None
    if update.code_required is not None:
        cfg.code_required = update.code_required

    cfg.updated_at = utc_now()
    db.commit()
    db.refresh(cfg)

    return ConsentConfigResponse(
        completion_code=cfg.completion_code,
        code_required=cfg.code_required,
    )


@router.post("/standalone/consent/verify", response_model=ConsentVerifyResponse)
def verify_consent_code(req: ConsentVerifyRequest, db=Depends(get_db)):
    """Verify a consent completion code."""
    cfg = _get_or_create_consent_config(db)

    if not cfg.code_required:
        return ConsentVerifyResponse(valid=True, message="Code verification not required")

    if not cfg.completion_code:
        # Code required but none configured - allow through
        return ConsentVerifyResponse(valid=True, message="No code configured")

    if not req.code:
        return ConsentVerifyResponse(valid=False, message="Completion code required")

    if req.code.strip().upper() != cfg.completion_code.upper():
        return ConsentVerifyResponse(valid=False, message="Invalid completion code")

    return ConsentVerifyResponse(valid=True, message="Code verified")
