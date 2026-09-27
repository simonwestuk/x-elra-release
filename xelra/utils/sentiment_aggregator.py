"""Utilities for maintaining learner/topic sentiment aggregates."""

from __future__ import annotations

import datetime as dt
from collections import defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
from sqlalchemy.orm import Session

from .db import Reflection, SentimentAggregate


def _linear_regression(x: Sequence[float], y: Sequence[float]) -> Tuple[float, float]:
    """Return (slope, intercept) for the best-fit line using least squares."""

    if len(x) < 2:
        value = float(y[0]) if y else 0.0
        return 0.0, value

    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    if np.allclose(x_arr, x_arr[0]):
        value = float(np.mean(y_arr)) if y_arr.size else 0.0
        return 0.0, value

    A = np.vstack([x_arr, np.ones_like(x_arr)]).T
    slope, intercept = np.linalg.lstsq(A, y_arr, rcond=None)[0]
    return float(slope), float(intercept)


def update_sentiment_aggregates(session: Session, window_days: int = 7) -> int:
    """Recompute learner/topic aggregates over the trailing ``window_days``.

    The function groups reflections by ``(learner_id, topic)`` where a topic is
    provided and sentiment has been scored.  For each group we compute the
    arithmetic mean of sentiment and a least-squares slope (per day) of the
    sentiment trend.  Existing aggregates that fall outside the window are
    removed.  Returns the number of aggregate rows touched (created/updated/
    deleted).
    """

    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=window_days)

    reflections: Iterable[Reflection] = (
        session.query(Reflection)
        .filter(
            Reflection.created_at >= cutoff,
            Reflection.sentiment.isnot(None),
            Reflection.topic.isnot(None),
        )
        .all()
    )

    grouped: Dict[Tuple[str, str], List[Reflection]] = defaultdict(list)
    for ref in reflections:
        topic = (ref.topic or "").strip()
        if not topic:
            continue
        grouped[(ref.learner_id, topic)].append(ref)

    touched = 0

    existing: Dict[Tuple[str, str], SentimentAggregate] = {
        (agg.learner_id, agg.topic): agg
        for agg in session.query(SentimentAggregate)
        .filter(SentimentAggregate.window_days == window_days)
        .all()
    }

    for key, rows in grouped.items():
        rows.sort(key=lambda r: r.created_at or cutoff)
        sentiments = [float(r.sentiment or 0.0) for r in rows]
        base_time = rows[0].created_at or cutoff
        x_vals = [
            ((r.created_at or base_time) - base_time).total_seconds() / 86400.0
            for r in rows
        ]
        slope, intercept = _linear_regression(x_vals, sentiments)
        mean_val = float(np.mean(sentiments)) if sentiments else 0.0
        last_sample = max((r.created_at for r in rows if r.created_at), default=None)

        agg = existing.pop(key, None)
        if agg is None:
            agg = SentimentAggregate(learner_id=key[0], topic=key[1])
            session.add(agg)

        agg.mean_polarity = mean_val
        agg.slope = slope
        agg.intercept = intercept
        agg.sample_size = len(rows)
        agg.window_days = window_days
        agg.last_sample_at = last_sample
        agg.updated_at = now
        touched += 1

    for agg in existing.values():
        session.delete(agg)
        touched += 1

    session.commit()
    return touched
