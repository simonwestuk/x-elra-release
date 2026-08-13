"""Sequence-oriented recommender based on metadata filters and completion history."""

from ...data.loader import load_items
from ...utils.db import SessionLocal, Completion
import pandas as pd
import numpy as np


class SequenceRecommender:
    def __init__(self):
        self.reload_items()

    def reload_items(self) -> None:
        """Reload item metadata from disk into memory."""
        # Store a DataFrame copy so recommend() can work from the cached data
        self.items = load_items().copy()

    def recommend(
        self,
        learner_id: str,
        top_k: int = 5,
        context: dict | None = None,
        weights: dict | None = None,
    ) -> list[dict]:
        df = self.items.copy()
        # Filter by course_id when provided
        cid = (context or {}).get("course_id") if context else None
        if cid:
            try:
                df = df[df["course_id"] == cid]
            except Exception:
                pass
        # NEW: apply upstream allow/exclude filters from context (if present)
        ctx = context or {}
        try:
            allowed_ids = (
                set(map(str, ctx.get("allowed_item_ids", [])))
                if "allowed_item_ids" in ctx
                else None
            )
            exclude_ids = (
                set(map(str, ctx.get("exclude_item_ids", [])))
                if "exclude_item_ids" in ctx
                else None
            )
        except Exception:
            allowed_ids, exclude_ids = None, None
        if allowed_ids is not None:
            df = df[df["item_id"].astype(str).isin(allowed_ids)]
        if exclude_ids is not None:
            df = df[~df["item_id"].astype(str).isin(exclude_ids)]

        if df.empty:
            return []
        # Ensure sequence_order exists and is numeric
        if "sequence_order" not in df.columns:
            df["sequence_order"] = np.arange(1, len(df) + 1)
        df["sequence_order"] = pd.to_numeric(
            df["sequence_order"], errors="coerce"
        ).fillna(1e9)

        # Pull completed items for this learner (skip DB if provided via context)
        completed = set()
        if exclude_ids is not None:
            completed = exclude_ids
        else:
            try:
                db = SessionLocal()
                rows = (
                    db.query(Completion)
                    .filter(Completion.learner_id == learner_id)
                    .all()
                )
                completed = {r.item_id for r in rows}
                db.close()
            except Exception:
                pass

        # Base score: inverse of sequence order (earlier = higher score)
        # Normalise to [0,1]
        max_so = df["sequence_order"].replace([np.inf, 1e9], np.nan).max()
        min_so = df["sequence_order"].replace([np.inf, 1e9], np.nan).min()
        if pd.isna(min_so) or pd.isna(max_so) or max_so == min_so:
            df["seq_score"] = 1.0
        else:
            # earlier gets higher: scale so min_so -> 1.0, max_so -> small
            df["seq_score"] = (max_so - df["sequence_order"]) / (max_so - min_so + 1e-9)
        # Exclude already-completed items
        df["completed"] = df["item_id"].astype(str).isin(completed)
        df = df[~df["completed"]]

        # Sort by score desc, then sequence_order asc as tie-breaker
        df = df.sort_values(["seq_score", "sequence_order"], ascending=[False, True])

        out = []
        for _, r in df.head(top_k).iterrows():
            out.append(
                {
                    "item_id": r.get("item_id"),
                    "title": r.get("title"),
                    "url": r.get("url", ""),
                    "score": float(r.get("seq_score", 0.0)),
                    "components": {"sequence": float(r.get("seq_score", 0.0))},
                }
            )
        return out
