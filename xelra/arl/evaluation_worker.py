"""Background worker that enriches ARL outcomes with telemetry metrics."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, Iterable, Mapping, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from .schemas import EvaluationJob
from ..utils import db as db_models


def _as_utc(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


@dataclass
class EvaluationWorker:
    """Consume :class:`EvaluationJob` instances and write telemetry outcomes."""

    session_factory: Callable[[], Session] = db_models.SessionLocal
    window: timedelta = timedelta(days=7)
    logger: logging.Logger = field(
        default_factory=lambda: logging.getLogger("xelra.arl.evaluation")
    )

    # Public API -----------------------------------------------------
    def schedule(self, job: EvaluationJob) -> None:
        """Compatibility hook so the worker can be passed to ``schedule_evaluation``."""

        self.process(job)

    def __call__(self, job: EvaluationJob) -> None:
        self.process(job)

    def process(self, job: EvaluationJob) -> Dict[int, Mapping[str, float]]:
        """Process a job immediately and return the computed metrics."""

        decision_id = str(job.payload.get("decision_id") or "")
        if not decision_id:
            self.logger.debug("evaluation job skipped (no decision_id)", extra={"job_id": job.job_id})
            return {}
        scheduled_for = _as_utc(job.scheduled_for)
        window_start = scheduled_for - self.window
        with self.session_factory() as session:
            outcomes: Iterable[db_models.ARLOutcome] = (
                session.query(db_models.ARLOutcome)
                .filter(db_models.ARLOutcome.decision_id == decision_id)
                .all()
            )
            metrics_by_outcome: Dict[int, Mapping[str, float]] = {}
            for outcome in outcomes:
                metrics = self._collect_metrics(
                    session,
                    learner_id=job.learner_id,
                    item_id=outcome.item_id,
                    window_start=window_start,
                    window_end=scheduled_for,
                )
                metrics_by_outcome[outcome.id] = metrics
                self._persist_metrics(session, outcome, metrics)
            session.commit()
            return metrics_by_outcome

    # Internal helpers ----------------------------------------------
    def _collect_metrics(
        self,
        session: Session,
        *,
        learner_id: str,
        item_id: Optional[str],
        window_start: datetime,
        window_end: datetime,
    ) -> Mapping[str, float]:
        if not item_id:
            return {
                "mastery_delta": 0.0,
                "error_delta": 0.0,
                "latency_recovery": 0.0,
                "hint_change": 0.0,
                "retention": 0.0,
            }
        skill_ids = [
            row[0]
            for row in session.query(db_models.ItemSkill.skill_id)
            .filter(db_models.ItemSkill.item_id == item_id)
            .all()
        ]
        mastery_query = session.query(
            func.coalesce(func.sum(db_models.MasteryEvidence.delta), 0.0)
        ).filter(db_models.MasteryEvidence.learner_id == learner_id)
        if skill_ids:
            mastery_query = mastery_query.filter(
                db_models.MasteryEvidence.skill_id.in_(skill_ids)
            )
        mastery_delta = float(
            mastery_query.filter(db_models.MasteryEvidence.created_at >= window_start)
            .filter(db_models.MasteryEvidence.created_at <= window_end)
            .scalar()
            or 0.0
        )
        click_count = (
            session.query(func.count(db_models.Click.id))
            .filter(db_models.Click.learner_id == learner_id)
            .filter(db_models.Click.item_id == item_id)
            .filter(db_models.Click.created_at >= window_start)
            .filter(db_models.Click.created_at <= window_end)
            .scalar()
            or 0
        )
        completion_count = (
            session.query(func.count(db_models.Completion.id))
            .filter(db_models.Completion.learner_id == learner_id)
            .filter(db_models.Completion.item_id == item_id)
            .filter(db_models.Completion.created_at >= window_start)
            .filter(db_models.Completion.created_at <= window_end)
            .scalar()
            or 0
        )
        impressions = (
            session.query(db_models.Impression)
            .filter(db_models.Impression.learner_id == learner_id)
            .filter(db_models.Impression.item_id == item_id)
            .filter(db_models.Impression.created_at <= window_end)
            .filter(db_models.Impression.created_at >= window_start)
            .order_by(db_models.Impression.created_at.desc())
            .all()
        )
        completions = (
            session.query(db_models.Completion)
            .filter(db_models.Completion.learner_id == learner_id)
            .filter(db_models.Completion.item_id == item_id)
            .filter(db_models.Completion.created_at >= window_start)
            .filter(db_models.Completion.created_at <= window_end)
            .order_by(db_models.Completion.created_at.asc())
            .all()
        )
        latencies = []
        for completion in completions:
            impression = next(
                (imp for imp in impressions if imp.created_at <= completion.created_at),
                None,
            )
            if impression is not None:
                delta = completion.created_at - impression.created_at
                latencies.append(max(delta.total_seconds(), 0.0))
        latency_recovery = sum(latencies) / len(latencies) if latencies else 0.0
        hint_change = (
            session.query(func.count(db_models.ExplanationInteraction.id))
            .filter(db_models.ExplanationInteraction.learner_id == learner_id)
            .filter(db_models.ExplanationInteraction.item_id == item_id)
            .filter(db_models.ExplanationInteraction.created_at >= window_start)
            .filter(db_models.ExplanationInteraction.created_at <= window_end)
            .scalar()
            or 0
        )
        impression_count = len(impressions)
        retention = (
            float(completion_count) / float(impression_count)
            if impression_count
            else float(completion_count)
        )
        return {
            "mastery_delta": mastery_delta,
            "error_delta": float(completion_count - click_count),
            "latency_recovery": float(latency_recovery),
            "hint_change": float(hint_change),
            "retention": float(retention),
        }

    def _persist_metrics(
        self,
        session: Session,
        outcome: db_models.ARLOutcome,
        metrics: Mapping[str, float],
    ) -> None:
        metadata = {}
        if outcome.metadata_json:
            try:
                metadata = json.loads(outcome.metadata_json)
            except json.JSONDecodeError:  # pragma: no cover - defensive
                metadata = {}
        metadata["evaluation"] = {
            key: float(value) for key, value in metrics.items()
        }
        outcome.metadata_json = json.dumps(
            metadata,
            sort_keys=True,
            separators=(",", ":"),
        )
        session.add(outcome)


__all__ = ["EvaluationWorker"]

