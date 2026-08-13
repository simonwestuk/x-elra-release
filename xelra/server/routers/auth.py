"""SSO authentication route that validates external JWTs and issues local tokens."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
from jwt import InvalidTokenError
from ...config import settings
from ...utils.auth import issue_login_token
from ...utils.db import SessionLocal, get_or_assign_arm

router = APIRouter()


class SSORequest(BaseModel):
    token: str


@router.post("/auth/sso")
def sso_login(req: SSORequest):
    try:
        payload = jwt.decode(
            req.token,
            settings.sso_jwt_secret,
            algorithms=["HS256"],
            audience=settings.sso_expected_audience,
        )
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid SSO token")
    # Expected claims: sub (user id), iss (issuer), aud (audience), optional course_id
    iss = payload.get("iss")
    if settings.sso_expected_issuer and iss != settings.sso_expected_issuer:
        raise HTTPException(status_code=401, detail="Invalid issuer")
    user_id = payload.get("sub") or payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token missing 'sub' or 'user_id'")
    course_id = payload.get("course_id")
    # Pseudonymous mapping (stable)
    learner_id = f"lms_{user_id}"

    db = SessionLocal()
    try:
        arm = get_or_assign_arm(db, learner_id)
    finally:
        db.close()

    token = issue_login_token(learner_id, arm_key=arm)
    return {"learner_id": learner_id, "course_id": course_id, "arm": arm, "token": token}
