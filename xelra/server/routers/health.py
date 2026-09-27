"""Operational health endpoint that verifies API and database responsiveness."""

from fastapi import APIRouter
from sqlalchemy import text
from ...utils.db import SessionLocal

router = APIRouter()


@router.get("/health")
def health():
    # Try a quick DB connection + trivial query
    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
        finally:
            db.close()
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "degraded", "db": f"error: {type(e).__name__}"}
