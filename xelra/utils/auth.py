"""Authentication helpers for issuing and validating learner login tokens."""

import time
import uuid

import jwt
from jwt import InvalidTokenError

from ..config import settings


def issue_login_token(
    learner_id: str,
    email: str | None = None,
    *,
    arm_key: str | None = None,
    iss: str | None = None,
    aud: str | None = None,
) -> str:
    now = int(time.time())
    exp = now + settings.login_token_ttl_minutes * 60
    issuer = iss if iss is not None else settings.login_jwt_issuer
    audience = aud if aud is not None else settings.login_jwt_audience
    payload: dict[str, object] = {
        "sub": learner_id,
        "iat": now,
        "exp": exp,
    }
    if audience:
        payload["aud"] = audience
    if issuer:
        payload["iss"] = issuer
    if email:
        payload["email"] = email
    if arm_key:
        payload["arm_key"] = arm_key
    return jwt.encode(payload, settings.login_jwt_secret, algorithm="HS256")


def verify_login_token(token: str) -> dict:
    audience = settings.login_jwt_audience
    issuer = settings.login_jwt_issuer
    decode_kwargs = {"algorithms": ["HS256"]}
    options: dict[str, bool] = {}
    if audience:
        decode_kwargs["audience"] = audience
    else:
        options["verify_aud"] = False
    if issuer:
        decode_kwargs["issuer"] = issuer
    else:
        options["verify_iss"] = False
    leeway = settings.login_jwt_leeway_seconds
    if leeway:
        decode_kwargs["leeway"] = leeway
    if options:
        decode_kwargs["options"] = options
    payload = jwt.decode(token, settings.login_jwt_secret, **decode_kwargs)
    arm_key = payload.get("arm_key")
    if not isinstance(arm_key, str) or not arm_key:
        raise InvalidTokenError("Token missing arm_key claim")
    return payload


def new_standalone_learner_id() -> str:
    """Generate a random learner_id for standalone mode."""
    return f"std_{uuid.uuid4()}"
