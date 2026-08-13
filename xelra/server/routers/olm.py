"""OLM API routes for learner summaries, mastery evidence, and goal management."""

import json
import logging
from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

from ...utils.db import SessionLocal
from ...olm.service import (
    gap_analysis,
    get_skill_catalogue,
    goal_by_id,
    goals_for_learner,
    learner_mastery_map,
    learner_mastery_records,
    mastery_evidence_by_id,
    update_goal,
    upsert_goal,
    delete_goal as delete_goal_service,
)
from ...olm.interface import regulatory_transparency

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MasteryRecordModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_id: str
    skill_name: Optional[str] = None
    skill_level: Optional[int] = None
    value: float = Field(..., ge=0.0, le=1.0)
    updated_at: Optional[datetime] = None
    evidence_id: Optional[int] = None


class GapModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_id: str
    name: Optional[str] = None
    level: Optional[int] = None
    value: float = Field(..., ge=0.0, le=1.0)
    goal_target: float = Field(..., ge=0.0, le=1.0)
    gap: float = Field(..., ge=0.0)
    evidence_id: Optional[int] = None
    updated_at: Optional[datetime] = None


class GoalCreate(BaseModel):
    learner_id: str
    skill_id: str
    target: float = Field(default=1.0, ge=0.0, le=1.0)
    due_date: Optional[datetime] = None


class GoalUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    due_date: Optional[datetime] = None


class GoalModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    learner_id: str
    skill_id: str
    target: float
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class MasteryEvidenceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    learner_id: str
    skill_id: str
    source: str
    delta: Optional[float] = None
    resulting_value: Optional[float] = None
    item_id: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


@router.get("/olm/summary/{learner_id}")
def summary(learner_id: str, db=Depends(get_db)):
    skills = get_skill_catalogue(db)
    mastery = learner_mastery_map(db, learner_id)
    gaps = gap_analysis(db, learner_id)
    cats = [
        {"id": s.id, "name": s.name, "level": s.level, "value": mastery.get(s.id, 0.0)}
        for s in skills
    ]
    top_gaps = gaps[:3]
    goals = goals_for_learner(db, learner_id)
    goal_map = {g.skill_id: float(g.target) for g in goals}
    return {"skills": cats, "top_gaps": top_gaps, "goals": goal_map}


@router.get("/olm/mastery", response_model=List[MasteryRecordModel])
def list_mastery(learner_id: str, db=Depends(get_db)):
    return learner_mastery_records(db, learner_id)


@router.get("/olm/gaps", response_model=List[GapModel])
def list_gaps(learner_id: str, limit: Optional[int] = None, db=Depends(get_db)):
    rows = gap_analysis(db, learner_id)
    if limit is not None and limit >= 0:
        rows = rows[:limit]
    return rows


@router.get("/olm/goal", response_model=List[GoalModel])
def list_goals(learner_id: str, db=Depends(get_db)):
    return goals_for_learner(db, learner_id)


@router.get("/olm/goal/{goal_id}", response_model=GoalModel)
def get_goal(goal_id: int, db=Depends(get_db)):
    goal = goal_by_id(db, goal_id)
    if goal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.post("/olm/goal", response_model=GoalModel, status_code=status.HTTP_201_CREATED)
def create_goal(goal: GoalCreate, db=Depends(get_db)):
    record = upsert_goal(db, goal.learner_id, goal.skill_id, goal.target, goal.due_date)
    db.refresh(record)
    return record


@router.patch("/olm/goal/{goal_id}", response_model=GoalModel)
def patch_goal(goal_id: int, payload: GoalUpdate, db=Depends(get_db)):
    updates = payload.model_dump(exclude_unset=True)
    record = update_goal(
        db,
        goal_id,
        target=updates.get("target"),
        due_date=updates.get("due_date"),
    )
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return record


@router.delete("/olm/goal/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_goal(goal_id: int, db=Depends(get_db)):
    removed = delete_goal_service(db, goal_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/olm/evidence/{evidence_id}", response_model=MasteryEvidenceModel)
def get_evidence(evidence_id: int, db=Depends(get_db)):
    evidence = mastery_evidence_by_id(db, evidence_id)
    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evidence not found"
        )
    metadata = None
    if evidence.metadata_json:
        try:
            metadata = json.loads(evidence.metadata_json)
        except json.JSONDecodeError:
            metadata = None
    return MasteryEvidenceModel(
        id=evidence.id,
        learner_id=evidence.learner_id,
        skill_id=evidence.skill_id,
        source=evidence.source,
        delta=evidence.delta,
        resulting_value=evidence.resulting_value,
        item_id=evidence.item_id,
        notes=evidence.notes,
        metadata=metadata,
        created_at=evidence.created_at,
        updated_at=evidence.updated_at,
    )


@router.get("/olm/regulatory/{learner_id}")
def get_regulatory_transparency(learner_id: str):
    """
    Get learner-facing regulatory transparency information.

    Implements the OLM projection per Table 1 (Section 3.3) of the ARL paper.
    Provides process-level explainability showing:
    - Current regulatory mode
    - Why the system entered this mode
    - What the system will do while in this mode
    - What the learner should do next
    - What conditions will trigger mode exit or transition

    This endpoint provides transparency of regulated system behaviour
    rather than model inference, as specified in Section 3.3.

    Parameters
    ----------
    learner_id:
        The learner identifier

    Returns
    -------
    dict
        Learner-facing projection with the five required fields:
        mode_label, why, system_behaviour, expected_action, exit_conditions
    """
    try:
        return regulatory_transparency(learner_id)
    except Exception:
        logger.exception("regulatory_transparency failed for %s", learner_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve regulatory transparency"
        )
