"""
Simplified Hybrid Recommender for Research

This is an intentionally simple implementation designed for research purposes.
The goal is to make ARL's regulatory contribution clearly attributable by using
a baseline recommender that is easy to understand, verify, and explain.

DESIGN PRINCIPLES:
1. Transparency: Every step is documented and easy to follow
2. Simplicity: No complex ML models (no SVD, no neural networks)
3. Interpretability: Clear variable names and explicit calculations
4. Reproducibility: Deterministic behavior for research validity

COMPONENTS:
- Content-Based: Jaccard similarity on topics (simple set overlap)
- Collaborative Filtering: Classic item-item similarity (cosine)
- Popularity: Simple engagement counts (clicks + completions)
- Sentiment: Basic reflection polarity only (optional, for ARM E)

FORMULA:
Final Score = w_content × Content + w_cf × CF + w_pop × Popularity + w_sent × Sentiment

Where all components are normalized to [0, 1] and weights sum to 1.0 for transparency.
"""

from typing import Any, Dict, List, Optional, Set
import hashlib

import numpy as np
import pandas as pd

from ...data.loader import load_items, load_events, load_reflections
from ..sentiment.model import SentimentModel


class SimpleHybridRecommender:
    """
    Simple hybrid recommender for research purposes.

    Combines three basic signals with transparent weighting:
    1. Content similarity (topic overlap using Jaccard)
    2. Collaborative filtering (item-item similarity using cosine)
    3. Popularity (engagement counts)
    4. Sentiment (reflection polarity, optional)

    This implementation prioritizes interpretability over performance.
    All operations use simple, explicit calculations rather than
    optimized vectorized operations.
    """

    # Class-level caches (loaded once, shared across instances)
    _items: Optional[pd.DataFrame] = None
    _events: Optional[pd.DataFrame] = None
    _reflections: Optional[pd.DataFrame] = None
    _item_similarity_matrix: Optional[np.ndarray] = None
    _item_index: Optional[Dict[str, int]] = None
    _popularity_scores: Optional[Dict[str, float]] = None
    _item_topics: Optional[Dict[str, Set[str]]] = None

    def __init__(
        self,
        mode: str = "hybrid",
        w_content: float = 0.25,
        w_cf: float = 0.25,
        w_popularity: float = 0.25,
        w_sentiment: float = 0.25,
        # Backward compatibility with old API
        w_base: Optional[float] = None,
        w_sent: Optional[float] = None,
        w_item_sent: float = 0.0,  # Deprecated (was multi-faceted sentiment)
        w_lsw: float = 0.0,  # Deprecated (was learner sentiment window)
    ):
        """
        Initialize the simple hybrid recommender.

        Args:
            mode: Strategy mode - "content", "cf", "popularity", or "hybrid"
            w_content: Weight for content-based component [0, 1]
            w_cf: Weight for collaborative filtering [0, 1]
            w_popularity: Weight for popularity component [0, 1]
            w_sentiment: Weight for sentiment component [0, 1]

            # Backward compatibility (old API)
            w_base: Alias for w_popularity (deprecated)
            w_sent: Alias for w_sentiment (deprecated)
            w_item_sent: Ignored (was item sentiment, now simplified)
            w_lsw: Ignored (was learner sentiment window, now simplified)

        Note: Weights don't need to sum to 1.0 - they're normalized during scoring.
        Default: Equal weighting (0.25 each) for maximum transparency.
        """
        # Backward compatibility: old API parameter mapping
        if w_base is not None:
            w_popularity = w_base
        if w_sent is not None:
            w_sentiment = w_sent

        # Mode-specific weight adjustments (for backward compatibility)
        if mode == "content":
            # Content-only mode: 100% content weight
            w_content = 1.0
            w_cf = 0.0
            w_popularity = 0.0
            w_sentiment = 0.0
        elif mode == "popularity":
            # Popularity-only mode: 100% popularity weight
            w_content = 0.0
            w_cf = 0.0
            w_popularity = 1.0
            w_sentiment = 0.0

        self.mode = mode
        self.w_content = float(w_content)
        self.w_cf = float(w_cf)
        self.w_popularity = float(w_popularity)
        self.w_sentiment = float(w_sentiment)

        cls = type(self)
        if cls._items is None:
            cls._items = load_items()
            cls._prepare_item_topics()
        if cls._events is None:
            cls._events = load_events()
        if cls._reflections is None:
            cls._reflections = load_reflections()

        # Prepare popularity scores (simple counts)
        if cls._popularity_scores is None:
            cls._prepare_popularity_scores()

        # Prepare collaborative filtering (item-item similarity)
        if cls._item_similarity_matrix is None:
            cls._prepare_item_similarity()

        # Bind to instance
        self.items = cls._items
        self.events = cls._events
        self.reflections = cls._reflections
        self.item_topics = cls._item_topics
        self.popularity_scores = cls._popularity_scores
        self.item_similarity_matrix = cls._item_similarity_matrix
        self.item_index = cls._item_index

        # Sentiment model (only loaded if sentiment weight > 0)
        self.sentiment_model = SentimentModel() if w_sentiment > 0 else None

    @classmethod
    def _prepare_item_topics(cls):
        """
        Extract topics from items and store as sets for fast Jaccard calculation.

        Topics are pipe-separated in the database (e.g., "python|data-science|ml").
        We convert them to sets for easy intersection and union operations.
        """
        cls._item_topics = {}
        for _, row in cls._items.iterrows():
            item_id = str(row["item_id"])
            topics_str = str(row.get("topics", ""))
            # Split by pipe and remove empty strings
            topics = {t.strip() for t in topics_str.split("|") if t.strip()}
            cls._item_topics[item_id] = topics

    @classmethod
    def _prepare_popularity_scores(cls):
        """
        Calculate simple popularity scores based on engagement.

        Formula: pop_score = clicks + (2 × completions)

        Rationale: Completions are worth 2× clicks because they indicate
        deeper engagement. This is intentionally simple for interpretability.
        """
        cls._popularity_scores = {}

        # Aggregate events by item
        for item_id in cls._items["item_id"]:
            item_id_str = str(item_id)
            item_events = cls._events[cls._events["item_id"] == item_id]

            # Count clicks and completions
            num_clicks = int(item_events["clicked"].sum() if "clicked" in item_events.columns else 0)
            num_completions = int(item_events["completed"].sum() if "completed" in item_events.columns else 0)

            # Simple formula: clicks + 2 * completions
            pop_score = num_clicks + (2 * num_completions)
            cls._popularity_scores[item_id_str] = float(pop_score)

    @classmethod
    def _prepare_item_similarity(cls):
        """
        Build item-item similarity matrix using cosine similarity.

        This is classic collaborative filtering based on implicit feedback:
        - User-item matrix: rows = users, columns = items
        - Values: 1 for click, 2 for completion (simple implicit ratings)
        - Item similarity: cosine similarity between item column vectors

        Result: A symmetric matrix where entry (i, j) = similarity between items i and j
        """
        users = sorted(cls._events["learner_id"].unique())
        items = sorted(cls._items["item_id"].astype(str).unique())

        user_to_idx = {user: idx for idx, user in enumerate(users)}
        item_to_idx = {item: idx for idx, item in enumerate(items)}
        cls._item_index = item_to_idx

        n_users = len(users)
        n_items = len(items)
        user_item_matrix = np.zeros((n_users, n_items), dtype=float)

        for _, event in cls._events.iterrows():
            user_id = event["learner_id"]
            item_id = str(event["item_id"])

            if user_id not in user_to_idx or item_id not in item_to_idx:
                continue

            user_idx = user_to_idx[user_id]
            item_idx = item_to_idx[item_id]

            # Simple implicit rating: 1 for click, 2 for completion
            clicked = 1.0 if event.get("clicked", 0) else 0.0
            completed = 2.0 if event.get("completed", 0) else 0.0
            user_item_matrix[user_idx, item_idx] += clicked + completed

        # Calculate item-item cosine similarity
        # Transpose to get item-user matrix (items as rows)
        item_user_matrix = user_item_matrix.T

        # Cosine similarity formula: (A · B) / (||A|| × ||B||)
        # Normalize each row (item vector) by its L2 norm
        norms = np.linalg.norm(item_user_matrix, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0  # Avoid division by zero
        normalized_matrix = item_user_matrix / norms

        # Similarity matrix: dot product of normalized vectors
        cls._item_similarity_matrix = normalized_matrix @ normalized_matrix.T

    def _get_user_topics(self, learner_id: str) -> Set[str]:
        """
        Get all topics from items the user has interacted with.

        This builds a "user profile" based on their history.
        Used for content-based filtering.
        """
        user_events = self.events[self.events["learner_id"] == learner_id]
        user_topics = set()

        for item_id in user_events["item_id"]:
            item_id_str = str(item_id)
            item_topics = self.item_topics.get(item_id_str, set())
            user_topics.update(item_topics)

        return user_topics

    def _calculate_content_score(self, user_topics: Set[str], item_topics: Set[str]) -> float:
        """
        Calculate Jaccard similarity between user and item topics.

        Jaccard = |A ∩ B| / |A ∪ B|

        This measures topic overlap:
        - 1.0 = perfect match (all topics overlap)
        - 0.0 = no overlap

        This is one of the simplest and most interpretable similarity measures.
        """
        if not user_topics or not item_topics:
            return 0.0

        intersection = len(user_topics & item_topics)
        union = len(user_topics | item_topics)

        if union == 0:
            return 0.0

        return float(intersection) / float(union)

    def _calculate_cf_score(self, learner_id: str, item_id: str) -> float:
        """
        Calculate collaborative filtering score for an item.

        Formula: Sum of similarities to items the user has already interacted with.

        Intuition: "Users who liked items similar to X also liked X"

        This is the classic item-item CF approach, very interpretable.
        """
        if self.item_similarity_matrix is None or self.item_index is None:
            return 0.0

        user_events = self.events[self.events["learner_id"] == learner_id]
        user_item_ids = set(str(iid) for iid in user_events["item_id"])

        if not user_item_ids:
            return 0.0

        item_id_str = str(item_id)
        if item_id_str not in self.item_index:
            return 0.0

        target_idx = self.item_index[item_id_str]

        # Sum similarities to all items user has seen
        total_similarity = 0.0
        for seen_item_id in user_item_ids:
            if seen_item_id in self.item_index:
                seen_idx = self.item_index[seen_item_id]
                similarity = self.item_similarity_matrix[target_idx, seen_idx]
                total_similarity += similarity

        return float(total_similarity)

    def _get_latest_reflection(self, learner_id: str) -> Optional[str]:
        """Get the most recent reflection text for sentiment analysis."""
        user_reflections = self.reflections[self.reflections["learner_id"] == learner_id]

        if user_reflections.empty:
            return None

        # Sort by timestamp to get latest
        user_reflections = user_reflections.copy()
        user_reflections["timestamp"] = pd.to_datetime(user_reflections["timestamp"], errors="coerce")
        latest = user_reflections.sort_values("timestamp", ascending=False).iloc[0]

        return str(latest["text"])

    def _calculate_sentiment_score(self, learner_id: str) -> float:
        """
        Calculate sentiment score from latest reflection.

        Returns a value in [0, 1] where:
        - 0.0 = very negative sentiment
        - 0.5 = neutral
        - 1.0 = very positive sentiment

        The sentiment model returns values in [-1, 1], so we transform:
        normalized = (raw_score + 1) / 2
        """
        if self.sentiment_model is None:
            return 0.5  # Neutral default

        reflection = self._get_latest_reflection(learner_id)
        if not reflection:
            return 0.5  # Neutral if no reflection

        try:
            # Sentiment model returns value in [-1, 1]
            raw_sentiment = self.sentiment_model.score(reflection)
            # Normalize to [0, 1]
            normalized = (float(raw_sentiment) + 1.0) / 2.0
            return np.clip(normalized, 0.0, 1.0)
        except Exception:
            return 0.5  # Neutral on error

    def _normalize_scores(self, scores: List[float], has_signal: bool = True) -> List[float]:
        """
        Normalize scores to [0, 1] range using min-max scaling.

        Formula: (x - min) / (max - min)

        This ensures all components are on the same scale before weighting.

        IMPORTANT: When all scores are identical (zero variance), we return 0.0
        for all items rather than 0.5. This treats "no signal" as absent rather
        than as "equal preference", allowing other components with actual signal
        to drive the recommendation. This is critical for cold-start learners
        who have no interaction history - they should fall back to popularity
        and sequence order rather than getting artificially uniform scores.
        """
        if not scores:
            return []

        min_score = min(scores)
        max_score = max(scores)

        if max_score == min_score:
            # Zero variance = no signal from this component
            # Return 0.0 to let other components drive the decision
            return [0.0] * len(scores)

        return [(s - min_score) / (max_score - min_score) for s in scores]

    def recommend(
        self,
        learner_id: str,
        top_k: int = 10,
        context: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations using the simple hybrid approach.

        Algorithm:
        1. Get candidate items (exclude already seen)
        2. For each candidate, calculate all component scores
        3. Normalize each component to [0, 1]
        4. Combine using weighted sum
        5. Sort by final score and return top K

        Args:
            learner_id: User to recommend for
            top_k: Number of recommendations to return
            context: Optional filtering context (allowed_item_ids, exclude_item_ids)
            weights: Optional weight overrides for this request

        Returns:
            List of recommendations with scores and component breakdowns
        """
        w_content = float(weights.get("content", self.w_content)) if weights else self.w_content
        w_cf = float(weights.get("cf", self.w_cf)) if weights else self.w_cf
        w_popularity = float(weights.get("popularity", self.w_popularity)) if weights else self.w_popularity
        w_sentiment = float(weights.get("sentiment", self.w_sentiment)) if weights else self.w_sentiment

        allowed_ids = None
        exclude_ids = None
        if context:
            if context.get("allowed_item_ids"):
                allowed_ids = set(str(iid) for iid in context["allowed_item_ids"])
            if context.get("exclude_item_ids"):
                exclude_ids = set(str(iid) for iid in context["exclude_item_ids"])

        user_events = self.events[self.events["learner_id"] == learner_id]
        seen_items = set(str(iid) for iid in user_events["item_id"])

        candidates = []
        for _, item in self.items.iterrows():
            item_id_str = str(item["item_id"])

            # Apply filters
            if allowed_ids and item_id_str not in allowed_ids:
                continue
            if exclude_ids and item_id_str in exclude_ids:
                continue
            if item_id_str in seen_items:
                continue

            # Get sequence_order for curriculum-based tiebreaking
            # Default to a high value if not present
            seq_order = item.get("sequence_order", 999999)
            try:
                seq_order = float(seq_order) if pd.notna(seq_order) else 999999.0
            except (ValueError, TypeError):
                seq_order = 999999.0

            candidates.append({
                "item_id": item_id_str,
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "sequence_order": seq_order,
            })

        if not candidates:
            return []

        # Pre-calculate user profile for content-based
        user_topics = self._get_user_topics(learner_id)

        # Pre-calculate sentiment score (same for all items)
        sentiment_score = self._calculate_sentiment_score(learner_id) if w_sentiment > 0 else 0.5

        # Calculate all component scores for all candidates
        content_scores = []
        cf_scores = []
        popularity_scores_list = []

        for candidate in candidates:
            item_id = candidate["item_id"]
            item_topics = self.item_topics.get(item_id, set())

            # Content score (Jaccard similarity)
            content_score = self._calculate_content_score(user_topics, item_topics)
            content_scores.append(content_score)

            # CF score (item-item similarity)
            cf_score = self._calculate_cf_score(learner_id, item_id)
            cf_scores.append(cf_score)

            # Popularity score
            pop_score = self.popularity_scores.get(item_id, 0.0)
            popularity_scores_list.append(pop_score)

        # Normalize all components to [0, 1]
        content_scores_norm = self._normalize_scores(content_scores)
        cf_scores_norm = self._normalize_scores(cf_scores)
        popularity_scores_norm = self._normalize_scores(popularity_scores_list)

        # Calculate final scores using weighted combination
        results = []
        for idx, candidate in enumerate(candidates):
            # Get normalized component scores
            c = content_scores_norm[idx]
            cf = cf_scores_norm[idx]
            p = popularity_scores_norm[idx]
            s = sentiment_score

            # Weighted combination
            final_score = (w_content * c) + (w_cf * cf) + (w_popularity * p) + (w_sentiment * s)

            # Store result with full transparency
            results.append({
                "item_id": candidate["item_id"],
                "title": candidate["title"],
                "url": candidate["url"],
                "score": final_score,
                "sequence_order": candidate["sequence_order"],
                "components": {
                    "content": c,
                    "cf": cf,
                    "popularity": p,
                    "sentiment": s,
                    "weights": {
                        "content": w_content,
                        "cf": w_cf,
                        "popularity": w_popularity,
                        "sentiment": w_sentiment,
                    },
                    "score_breakdown": {
                        "content": w_content * c,
                        "cf": w_cf * cf,
                        "popularity": w_popularity * p,
                        "sentiment": w_sentiment * s,
                    },
                },
            })

        deterministic_seed = context.get("_deterministic_seed") if context else None

        def sort_key(item: Dict[str, Any]) -> tuple:
            """
            Sort key: (-score, sequence_order, deterministic_hash)

            Priority:
            1. Higher score first (negated for descending)
            2. Earlier in curriculum (lower sequence_order)
            3. Deterministic hash for reproducibility when all else is equal
            """
            item_id = item["item_id"]
            seq_order = item.get("sequence_order", 999999.0)

            # Final tiebreaker: deterministic hash or item_id
            if deterministic_seed is None:
                hash_key = item_id
            else:
                seed_key = f"{deterministic_seed}:{item_id}".encode("utf-8")
                hash_key = hashlib.sha256(seed_key).hexdigest()

            return (-item["score"], seq_order, hash_key)

        results.sort(key=sort_key)

        return results[:top_k]


# Alias for backward compatibility
HybridRecommender = SimpleHybridRecommender
