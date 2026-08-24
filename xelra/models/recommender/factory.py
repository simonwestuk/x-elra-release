"""Factory helpers for recommender models.

These functions return shared instances of recommenders. They also ensure that
heavy data preparation inside the recommenders is performed only once and
reused across different callers.
"""

from __future__ import annotations

from typing import Dict, Tuple

_hybrid_cache: Dict[Tuple[str, float, float, float, float, float], object] = {}
_sequence_instance: object | None = None


def get_hybrid_recommender(
    mode: str = "popularity",
    w_base: float = 0.6,
    w_sent: float = 0.2,
    w_cf: float = 0.2,
    w_item_sent: float = 0.0,
    w_lsw: float = 0.0,
):
    """
    Return a cached ``SimpleHybridRecommender`` instance for the given settings.

    Uses the simplified hybrid recommender designed for research transparency.
    See hybrid_simple.py for algorithm details.
    """
    from .hybrid_simple import SimpleHybridRecommender

    key = (mode, w_base, w_sent, w_cf, w_item_sent, w_lsw)
    instance = _hybrid_cache.get(key)
    if instance is None:
        instance = SimpleHybridRecommender(
            mode=mode,
            w_base=w_base,
            w_sent=w_sent,
            w_cf=w_cf,
            w_item_sent=w_item_sent,
            w_lsw=w_lsw,
        )
        _hybrid_cache[key] = instance
    return instance


def get_sequence_recommender():
    """Return a shared ``SequenceRecommender`` instance."""

    global _sequence_instance
    if _sequence_instance is None:
        from .sequence import SequenceRecommender

        _sequence_instance = SequenceRecommender()
    return _sequence_instance


__all__ = [
    "get_hybrid_recommender",
    "get_sequence_recommender",
]
