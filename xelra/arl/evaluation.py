"""Evaluation scheduling utilities."""
from __future__ import annotations

import asyncio
import hashlib
import inspect
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Optional, Sequence

from .schemas import EvaluationJob, RoutineResult


def _collect_items(routine_results: Sequence[RoutineResult]) -> Sequence[Mapping[str, object]]:
    items = []
    for result in routine_results:
        for action in result.actions:
            payload = action.payload or {}
            action_items = payload.get("items") if isinstance(payload, Mapping) else None
            if isinstance(action_items, Sequence):
                for entry in action_items:
                    if isinstance(entry, Mapping):
                        items.append(dict(entry))
    return items


def schedule_evaluation(
    learner_id: str,
    routine_results: Sequence[RoutineResult],
    *,
    delay_seconds: int = 0,
    trigger: str = "routine_execution",
    scheduler: Optional[object] = None,
    decision_id: Optional[str] = None,
    metadata: Optional[Mapping[str, Any]] = None,
    now: Optional[datetime] = None,
) -> EvaluationJob:
    """Create and optionally submit an evaluation job."""

    items = _collect_items(routine_results)
    routine_names = [result.routine.name for result in routine_results if not result.skipped]
    seed_parts = [learner_id, trigger, ",".join(routine_names), str(len(items))]
    if decision_id:
        seed_parts.append(str(decision_id))
    seed_material = "::".join(seed_parts)
    job_id = hashlib.sha256(seed_material.encode("utf-8")).hexdigest()[:16]
    reference_time = now or datetime.fromtimestamp(0, tz=timezone.utc)
    scheduled_for = reference_time + timedelta(seconds=max(delay_seconds, 0))
    payload = {
        "items": items,
        "routine_names": routine_names,
        "trigger": trigger,
    }
    if decision_id:
        payload["decision_id"] = decision_id
    if metadata:
        payload["metadata"] = dict(metadata)
    job = EvaluationJob(
        job_id=job_id,
        learner_id=learner_id,
        routine_names=tuple(routine_names),
        scheduled_for=scheduled_for,
        trigger=trigger,
        payload=payload,
    )
    if scheduler is not None:
        submit = (
            getattr(scheduler, "schedule", None)
            or getattr(scheduler, "enqueue", None)
            or getattr(scheduler, "submit", None)
            or getattr(scheduler, "put", None)
            or getattr(scheduler, "__call__", None)
        )
        if submit is not None:
            result = submit(job)
            if inspect.isawaitable(result):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    asyncio.run(result)
                else:  # pragma: no cover - exercised when running in async app
                    loop.create_task(result)
    return job


__all__ = ["schedule_evaluation"]
