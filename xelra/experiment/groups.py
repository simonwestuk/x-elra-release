"""Experiment group definitions and utilities.

Groups are sourced from the ARMS manifest and expose the behaviour required by
the recommendation services.  The three-group design evaluates how the **type**
of explanation influences learner experience (Table 8).  All groups use the
same hybrid recommender with identical weights and sentiment-aware
personalisation — only the explanation layer and governance layer differ:

* **treatment** (ARL) – Governed adaptive system with process-level structured
  explanations including regulatory mode semantics (mode/why/next/exit).
  No model-level "How we chose this" card or sentiment panel is shown.
* **control_a** (B1) – Model-driven adaptive with traditional post-hoc SHAP
  feature attribution only (including sentiment as one signal weight).
  No regulatory mode card, no process-level rationale, no sentiment panel.
* **control_b** (B3) – OLM-only transparency: learner state display (mastery,
  progress, goals) without explanations of decision processes.  The same
  sentiment-aware recommender runs underneath but is never surfaced.

This design holds the personalisation mechanism constant across arms and
isolates the effect of explanation type and regulatory structure on
information overload, trust, predictability, and cognitive load.

Examples
--------
>>> from xelra.experiment.groups import ExperimentGroup
>>> group = ExperimentGroup.treatment
>>> group.strategy
'hybrid'
>>> req = group.to_request("learner-123", top_k=5)
>>> req.strategy
'hybrid'
"""

from enum import Enum
from typing import Optional

from xelra.config import ArmConfig, get_arm_config, settings
from xelra.server.routers.recommend import RecRequest, Context


class ExperimentGroup(str, Enum):
    """Enumeration of experiment groups backed by the manifest."""

    treatment = "treatment"
    control_a = "control_a"
    control_b = "control_b"

    def __init__(self, slug: str) -> None:
        cfg = get_arm_config(slug)
        self.slug = slug
        self.config: ArmConfig = cfg
        self.strategy = cfg.strategy
        self.strategy_flag = cfg.raw.get("strategy_flag", slug)
        self.explain = cfg.explain
        self.regulatory_mode = cfg.regulatory_mode
        self.sentiment_enabled = cfg.sentiment_enabled
        self.xai_enabled = cfg.xai_enabled
        self.xai_level = cfg.xai_level
        self.xai_method = cfg.xai_method
        self.sentiment_provider = cfg.sentiment_provider
        self.sentiment_model = cfg.sentiment_model
        self.policy_version = cfg.policy_version
        self.routine_version = cfg.routine_version
        self.weight_map = cfg.weight_map

    def to_request(
        self,
        learner_id: str,
        top_k: int = 10,
        context: Optional[Context] = None,
        explain_level: str = "auto",
    ) -> RecRequest:
        """Create a :class:`RecRequest` for the given learner.

        Parameters
        ----------
        learner_id:
            Identifier of the learner to generate recommendations for.
        top_k:
            Number of recommendations to request. Defaults to ``10``.
        context:
            Optional :class:`~xelra.server.routers.recommend.Context` with
            additional information.
        explain_level:
            Explanation verbosity to request. Defaults to ``"auto"``.

        Returns
        -------
        RecRequest
            A populated request model matching this experiment group.

        Examples
        --------
        >>> ExperimentGroup.control_b.to_request("alice", top_k=3)
        RecRequest(learner_id='alice', context=None, top_k=3, explain=False, explain_level='auto', strategy='hybrid')
        """

        # When pilot_mode is active, override arm restrictions so all
        # learners receive the full feature set (explanations, XAI, etc.).
        explain = self.explain or settings.pilot_mode
        xai_method = self.xai_method if not settings.pilot_mode else (self.xai_method or "shap")

        return RecRequest(
            learner_id=learner_id,
            top_k=top_k,
            context=context,
            explain=explain,
            explain_level=explain_level,
            strategy=self.strategy,
            strategy_flag=self.strategy_flag,
            sentiment_enabled=self.sentiment_enabled,
            weight_map=dict(self.weight_map),
            policy_version=self.policy_version,
            routine_version=self.routine_version,
            xai_method=xai_method,
            sentiment_provider=self.sentiment_provider,
            sentiment_model=self.sentiment_model,
        )
