"""Service-layer operations for OLM skill, mastery, goal, and evidence data."""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from ..utils.db import (
    Skill,
    ItemSkill,
    Mastery,
    Goal,
    Item,
    MasteryEvidence,
    SkillPrerequisite,
)
from collections import defaultdict
from datetime import datetime, timezone
import re
import json


def get_skill_catalogue(db: Session) -> List[Skill]:
    return db.query(Skill).order_by(Skill.level.asc().nullsfirst()).all()


def learner_mastery_map(db: Session, learner_id: str) -> Dict[str, float]:
    rows = db.query(Mastery).filter(Mastery.learner_id == learner_id).all()
    return {r.skill_id: float(r.value) for r in rows}


def learner_mastery_records(db: Session, learner_id: str) -> List[dict]:
    """Return mastery records enriched with skill metadata and evidence links."""

    skills = {s.id: s for s in get_skill_catalogue(db)}
    rows = db.query(Mastery).filter(Mastery.learner_id == learner_id).all()
    records: List[dict] = []
    for row in rows:
        skill = skills.get(row.skill_id)
        records.append(
            {
                "skill_id": row.skill_id,
                "skill_name": skill.name if skill else None,
                "skill_level": skill.level if skill else None,
                "value": float(row.value),
                "updated_at": row.updated_at,
                "evidence_id": row.last_evidence_id,
            }
        )
    return records


def next_unmastered_skill(
    db: Session, learner_id: str, threshold: float = 0.8
) -> Skill | None:
    """Return the next skill in the catalogue whose mastery is below ``threshold``.

    Skills are iterated in catalogue order (ascending ``Skill.level``). If the
    learner has mastered all skills to the given threshold, ``None`` is
    returned.
    """

    skills = get_skill_catalogue(db)
    mastery = learner_mastery_map(db, learner_id)
    for s in skills:
        if mastery.get(s.id, 0.0) < threshold:
            return s
    return None


def goals_for_learner(db: Session, learner_id: str) -> List[Goal]:
    return db.query(Goal).filter(Goal.learner_id == learner_id).all()


def upsert_goal(
    db: Session, learner_id: str, skill_id: str, target: float = 1.0, due_date=None
):
    g = (
        db.query(Goal)
        .filter(Goal.learner_id == learner_id, Goal.skill_id == skill_id)
        .one_or_none()
    )
    if g is None:
        g = Goal(
            learner_id=learner_id, skill_id=skill_id, target=target, due_date=due_date
        )
        db.add(g)
    else:
        g.target = target
        g.due_date = due_date
    db.commit()
    return g


def goal_by_id(db: Session, goal_id: int) -> Goal | None:
    return db.query(Goal).filter(Goal.id == goal_id).one_or_none()


def update_goal(
    db: Session,
    goal_id: int,
    *,
    target: Optional[float] = None,
    due_date=None,
) -> Goal | None:
    goal = goal_by_id(db, goal_id)
    if goal is None:
        return None
    if target is not None:
        goal.target = target
    if due_date is not None:
        goal.due_date = due_date
    db.commit()
    db.refresh(goal)
    return goal


def delete_goal(db: Session, goal_id: int) -> bool:
    goal = goal_by_id(db, goal_id)
    if goal is None:
        return False
    db.delete(goal)
    db.commit()
    return True


def clear_goal(db: Session, learner_id: str, skill_id: str):
    db.query(Goal).filter(
        Goal.learner_id == learner_id, Goal.skill_id == skill_id
    ).delete()
    db.commit()


def create_mastery_evidence(
    db: Session,
    learner_id: str,
    skill_id: str,
    *,
    source: str,
    delta: Optional[float] = None,
    resulting_value: Optional[float] = None,
    item_id: Optional[str] = None,
    notes: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> MasteryEvidence:
    evidence = MasteryEvidence(
        learner_id=learner_id,
        skill_id=skill_id,
        source=source,
        delta=delta,
        resulting_value=resulting_value,
        item_id=item_id,
        notes=notes,
        metadata_json=json.dumps(metadata) if metadata is not None else None,
    )
    db.add(evidence)
    db.flush()
    return evidence


def record_progress_on_completion(
    db: Session, learner_id: str, item_id: str, delta: float = 0.1
):
    # When an item is completed, credit associated skills
    links = db.query(ItemSkill).filter(ItemSkill.item_id == item_id).all()

    def _ensure_skill(skill_id: str, *, fallback_name: Optional[str] = None) -> Skill:
        skill = db.query(Skill).filter(Skill.id == skill_id).one_or_none()
        if skill is None:
            skill = Skill(id=skill_id, name=fallback_name or skill_id)
            db.add(skill)
            db.flush()
        return skill

    def _apply_update(skill_id: str, increment: float, weight: Optional[float] = None):
        _ensure_skill(skill_id)
        mastery_row = (
            db.query(Mastery)
            .filter(Mastery.learner_id == learner_id, Mastery.skill_id == skill_id)
            .one_or_none()
        )
        current_value = mastery_row.value if mastery_row else 0.0
        new_value = min(1.0, current_value + increment)
        actual_delta = new_value - current_value
        if mastery_row:
            mastery_row.value = new_value
            mastery_row.p = new_value
            prev_sigma = mastery_row.sigma if mastery_row.sigma is not None else 1.0
            mastery_row.sigma = max(0.0, prev_sigma - abs(actual_delta))
            mastery_row.updated_at = datetime.now(timezone.utc)
        else:
            mastery_row = Mastery(
                learner_id=learner_id,
                skill_id=skill_id,
                value=new_value,
                p=new_value,
                sigma=max(0.0, 1.0 - new_value),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(mastery_row)
            db.flush()
        evidence = create_mastery_evidence(
            db,
            learner_id,
            skill_id,
            source="completion",
            delta=actual_delta,
            resulting_value=new_value,
            item_id=item_id,
            metadata={"weight": weight} if weight is not None else None,
            notes=f"Completion credit from item {item_id}",
        )
        mastery_row.last_evidence_id = evidence.id

    if not links:
        item = db.query(Item).filter(Item.item_id == item_id).one_or_none()
        topics: List[str] = []
        if item and item.topics:
            topics = [t.strip() for t in re.split(r"[|,]", item.topics) if t.strip()]
        for topic in topics:
            _ensure_skill(topic, fallback_name=topic)
            _apply_update(topic, delta)
        db.commit()
        return

    for link in links:
        weight = link.weight if link.weight is not None else 1.0
        increment = delta * weight
        _apply_update(link.skill_id, increment, weight=link.weight)

    db.commit()


def mastery_evidence_by_id(db: Session, evidence_id: int) -> MasteryEvidence | None:
    return (
        db.query(MasteryEvidence)
        .filter(MasteryEvidence.id == evidence_id)
        .one_or_none()
    )


def gap_analysis(db: Session, learner_id: str, default_target: float = 1.0) -> List[dict]:
    skills = get_skill_catalogue(db)
    masteries = {
        row.skill_id: row
        for row in db.query(Mastery).filter(Mastery.learner_id == learner_id).all()
    }
    goal_map = {g.skill_id: float(g.target) for g in goals_for_learner(db, learner_id)}
    prereq_edges = (
        db.query(SkillPrerequisite)
        .filter(SkillPrerequisite.skill_id.in_([s.id for s in skills]))
        .all()
    )
    prereq_map: dict[str, set[str]] = defaultdict(set)
    for edge in prereq_edges:
        prereq_map[edge.skill_id].add(edge.prerequisite_skill_id)

    rows: List[dict] = []
    for s in skills:
        mastery_row = masteries.get(s.id)
        value = float(mastery_row.value) if mastery_row else 0.0
        target = goal_map.get(s.id, default_target)
        gap_value = max(target - value, 0.0)
        rows.append(
            {
                "skill_id": s.id,
                "name": s.name,
                "level": s.level,
                "value": value,
                "goal_target": target,
                "gap": gap_value,
                "evidence_id": mastery_row.last_evidence_id if mastery_row else None,
                "updated_at": mastery_row.updated_at if mastery_row else None,
            }
        )
    gap_by_skill = {row["skill_id"]: row["gap"] for row in rows}
    prereq_tolerance = 0.05
    blocking_counts = {}
    epsilon = 1e-6
    for row in rows:
        blockers = 0
        for prereq in prereq_map.get(row["skill_id"], set()):
            gap = gap_by_skill.get(prereq, 0.0)
            if gap > prereq_tolerance + epsilon:
                blockers += 1
        blocking_counts[row["skill_id"]] = blockers
    rows.sort(
        key=lambda r: (
            blocking_counts.get(r["skill_id"], 0),
            r["value"],
            r["level"] if r["level"] is not None else 99,
            r["skill_id"],
        )
    )
    return rows


def gaps_sorted(db: Session, learner_id: str) -> List[dict]:
    """Backwards compatible alias for :func:`gap_analysis`."""

    return gap_analysis(db, learner_id)


def explain_with_olm(components: dict, item_id: str, db: Session, learner_id: str):
    # If item maps to low-mastery skills, add an OLM reason
    links = db.query(ItemSkill).filter(ItemSkill.item_id == item_id).all()
    mastery_rows = (
        db.query(Mastery)
        .filter(Mastery.learner_id == learner_id)
        .all()
    )
    mastery_values = {row.skill_id: float(row.value) for row in mastery_rows}
    evidence_ids = {row.skill_id: row.last_evidence_id for row in mastery_rows}

    lows = []
    for l in links:
        v = mastery_values.get(l.skill_id, 0.0)
        if v < 0.7:  # threshold
            lows.append((l.skill_id, v, l.weight or 1.0, evidence_ids.get(l.skill_id)))
    if lows:
        lows.sort(key=lambda t: (t[1], -t[2]))
        targets = []
        evidence_refs: Dict[str, Dict[str, Optional[int]]] = {}
        for sid, mv, w, evidence_id in lows[:2]:
            targets.append({"skill_id": sid, "mastery": mv, "evidence_id": evidence_id})
            if evidence_id is not None:
                evidence_refs[sid] = {"evidence_id": evidence_id}

        payload: Dict[str, Any] = {
            "olm": {
                "targets": targets,
                "summary": "Addresses skills where your mastery is currently lower.",
            }
        }
        if evidence_refs:
            payload["provenance"] = {"evidence": evidence_refs}
        return payload
    return {}
