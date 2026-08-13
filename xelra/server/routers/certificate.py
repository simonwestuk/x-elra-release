"""Certificate of participation router.

Issues certificates when a learner has completed all items in a course
(or all items globally if no course_id is specified).
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...utils.db import (
    Certificate,
    Completion,
    Item,
    SessionLocal,
    User,
    utc_now,
)

router = APIRouter()
router_prefix = "/v1"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CertificateRequest(BaseModel):
    learner_id: str
    course_id: Optional[str] = None
    holder_name: Optional[str] = None


class CertificateResponse(BaseModel):
    eligible: bool
    issued: bool = False
    certificate_id: Optional[int] = None
    learner_id: str
    course_id: Optional[str] = None
    holder_name: Optional[str] = None
    total_items: int = 0
    completed_items: int = 0
    issued_at: Optional[str] = None
    message: str = ""


@router.post("/certificate/check", response_model=CertificateResponse)
def check_certificate(req: CertificateRequest, db: Session = Depends(get_db)):
    """Check if a learner is eligible for a participation certificate.

    Returns eligibility status without issuing.
    """
    user = db.query(User).filter(User.learner_id == req.learner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")

    total, completed = _get_progress(db, req.learner_id, req.course_id)

    # Check if already issued
    existing = _get_existing(db, req.learner_id, req.course_id)
    if existing:
        return CertificateResponse(
            eligible=True,
            issued=True,
            certificate_id=existing.id,
            learner_id=req.learner_id,
            course_id=req.course_id,
            holder_name=existing.holder_name,
            total_items=total,
            completed_items=completed,
            issued_at=existing.issued_at.isoformat() if existing.issued_at else None,
            message="Certificate already issued.",
        )

    eligible = total > 0 and completed >= total
    return CertificateResponse(
        eligible=eligible,
        learner_id=req.learner_id,
        course_id=req.course_id,
        total_items=total,
        completed_items=completed,
        message="Eligible for certificate." if eligible else f"Complete {total - completed} more item(s) to earn your certificate.",
    )


@router.post("/certificate/issue", response_model=CertificateResponse)
def issue_certificate(req: CertificateRequest, db: Session = Depends(get_db)):
    """Issue a participation certificate if the learner is eligible."""
    user = db.query(User).filter(User.learner_id == req.learner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")

    # Check if already issued
    existing = _get_existing(db, req.learner_id, req.course_id)
    if existing:
        return CertificateResponse(
            eligible=True,
            issued=True,
            certificate_id=existing.id,
            learner_id=req.learner_id,
            course_id=req.course_id,
            holder_name=existing.holder_name,
            total_items=existing.total_items,
            completed_items=existing.total_completions,
            issued_at=existing.issued_at.isoformat() if existing.issued_at else None,
            message="Certificate already issued.",
        )

    total, completed = _get_progress(db, req.learner_id, req.course_id)
    if total == 0 or completed < total:
        raise HTTPException(
            status_code=400,
            detail=f"Not eligible: {completed}/{total} items completed.",
        )

    cert = Certificate(
        learner_id=req.learner_id,
        course_id=req.course_id,
        holder_name=req.holder_name,
        total_items=total,
        total_completions=completed,
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    return CertificateResponse(
        eligible=True,
        issued=True,
        certificate_id=cert.id,
        learner_id=req.learner_id,
        course_id=req.course_id,
        holder_name=cert.holder_name,
        total_items=total,
        completed_items=completed,
        issued_at=cert.issued_at.isoformat() if cert.issued_at else None,
        message="Certificate issued successfully.",
    )


@router.get("/certificate/{learner_id}")
def get_certificate(learner_id: str, course_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve an existing certificate for a learner."""
    cert = _get_existing(db, learner_id, course_id)
    if not cert:
        total, completed = _get_progress(db, learner_id, course_id)
        return CertificateResponse(
            eligible=total > 0 and completed >= total,
            learner_id=learner_id,
            course_id=course_id,
            total_items=total,
            completed_items=completed,
            message="No certificate issued yet.",
        )
    return CertificateResponse(
        eligible=True,
        issued=True,
        certificate_id=cert.id,
        learner_id=learner_id,
        course_id=course_id,
        holder_name=cert.holder_name,
        total_items=cert.total_items,
        completed_items=cert.total_completions,
        issued_at=cert.issued_at.isoformat() if cert.issued_at else None,
        message="Certificate issued.",
    )


def _get_progress(db: Session, learner_id: str, course_id: Optional[str]):
    """Return (total_items, completed_items) for a course or globally."""
    item_q = db.query(Item.item_id)
    if course_id:
        item_q = item_q.filter(Item.course_id == course_id)
    all_items = {r[0] for r in item_q.all()}
    total = len(all_items)

    comp_q = db.query(Completion.item_id).filter(
        Completion.learner_id == learner_id
    )
    if course_id:
        comp_q = comp_q.filter(Completion.course_id == course_id)
    completed_ids = {r[0] for r in comp_q.distinct().all()}

    return total, len(completed_ids & all_items)


def _get_existing(db: Session, learner_id: str, course_id: Optional[str]):
    q = db.query(Certificate).filter(Certificate.learner_id == learner_id)
    if course_id:
        q = q.filter(Certificate.course_id == course_id)
    else:
        q = q.filter(Certificate.course_id.is_(None))
    return q.first()
