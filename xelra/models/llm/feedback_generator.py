"""LLM Feedback Generator — upstream candidate producer for the ARL pipeline.

Generates personalised natural-language learning feedback using a local LLM
(via Ollama) based on current learner state.  Outputs are serialised as
candidate actions in the same schema used by the hybrid recommender, enabling
governance through the existing ARL controller without modification.
"""
from __future__ import annotations

import hashlib
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence

from .config import LLM_CONFIG
from .prompts import build_feedback_prompt

logger = logging.getLogger(__name__)

# Default score assigned to LLM feedback candidates.  This positions them
# within the merged candidate list alongside hybrid recommender items.
# Kept moderate (0.5) so that governance (routines/boundedness) is the
# primary selection mechanism, not a hard-coded score advantage.
DEFAULT_FEEDBACK_SCORE = 0.5


class LLMFeedbackGenerator:
    """Generates personalised natural-language learning feedback
    using a local LLM (via Ollama) based on current learner state.

    Outputs are serialised as candidate actions in the same schema
    used by the hybrid recommender, enabling governance through
    the existing ARL controller without modification.
    """

    def __init__(self, config: Optional[Mapping[str, Any]] = None) -> None:
        cfg = dict(LLM_CONFIG)
        if config:
            cfg.update(config)
        self.model: str = cfg["model"]
        self.base_url: str = cfg["base_url"].rstrip("/")
        self.temperature: float = cfg["temperature"]
        self.max_tokens: int = cfg["max_tokens"]
        self.timeout_seconds: int = cfg["timeout_seconds"]
        self.fallback_on_failure: bool = cfg.get("fallback_on_failure", True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        mastery: Mapping[str, float],
        metadata: Mapping[str, Any],
        *,
        topic: Optional[str] = None,
        score: float = DEFAULT_FEEDBACK_SCORE,
    ) -> List[Dict[str, Any]]:
        """Generate LLM feedback candidates from learner state.

        Parameters
        ----------
        mastery:
            Mastery estimates per skill (from FeatureVector.mastery).
        metadata:
            FeatureVector.metadata containing engagement/affect fields.
        topic:
            Override the active topic.  If *None*, the weakest skill is used.
        score:
            Confidence/relevance score assigned to the generated candidate.

        Returns
        -------
        A list of candidate dicts compatible with the hybrid recommender
        output schema.  Returns an empty list if generation fails (graceful
        degradation — the pipeline continues with recommender-only candidates).
        """
        active_topic, mastery_level = self._resolve_topic(mastery, topic)
        prompt = build_feedback_prompt(active_topic, mastery_level, metadata)

        try:
            feedback_text = self._call_llm(prompt)
        except Exception:
            logger.exception("LLM feedback generation failed; returning empty candidates")
            return []

        if not feedback_text or not feedback_text.strip():
            logger.warning("LLM returned empty feedback; returning empty candidates")
            return []

        timestamp = datetime.now(timezone.utc).isoformat()
        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]

        candidate: Dict[str, Any] = {
            "item_id": f"llm_feedback_{int(time.time())}",
            "action_type": "generated_feedback",
            "title": "Personalised Learning Feedback",
            "content": feedback_text.strip(),
            "score": score,
            "source": "llm_feedback_generator",
            "url": "",
            "sequence_order": 999999.0,
            "components": {
                "content": 0.0,
                "cf": 0.0,
                "popularity": 0.0,
                "sentiment": 0.0,
                "weights": {},
                "score_breakdown": {},
            },
            "metadata": {
                "model": self.model,
                "prompt_hash": prompt_hash,
                "generation_timestamp": timestamp,
            },
        }
        return [candidate]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_topic(
        mastery: Mapping[str, float],
        topic_override: Optional[str],
    ) -> tuple[str, float]:
        """Pick the active topic and its mastery level."""
        if topic_override and topic_override in mastery:
            return topic_override, mastery[topic_override]
        if topic_override:
            return topic_override, 0.0
        if mastery:
            weakest = min(mastery.items(), key=lambda kv: kv[1])
            return weakest
        return "general Python programming", 0.0

    def _call_llm(self, prompt: str) -> str:
        """Call Ollama's generate endpoint and return the response text.

        Raises on any failure so the caller can handle gracefully.
        """
        import urllib.request
        import json as _json

        url = f"{self.base_url}/api/generate"
        body = _json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
            data = _json.loads(resp.read().decode("utf-8"))
        return data.get("response", "")
