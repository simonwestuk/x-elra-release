"""Explanation builder for hybrid recommender contribution and rationale payloads."""

from typing import Any, Dict, List, Optional

# Friendly labels for contribution components
COMPONENT_LABELS: Dict[str, str] = {
    "C": "Content relevance",
    "CF": "Similar learners",
    "P": "Community popularity",
    "S": "Sentiment alignment",
    "D": "Diversity balance",
}

COMPONENT_ORDER: List[str] = ["C", "CF", "P", "S", "D"]

# The hybrid recommender uses long lowercase names while the XAI layer uses
# short uppercase keys.  This mapping normalises incoming data so both
# conventions resolve correctly.
_LONG_TO_SHORT: Dict[str, str] = {
    "content": "C",
    "cf": "CF",
    "popularity": "P",
    "sentiment": "S",
    "diversity": "D",
}


def _normalise_keys(src: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of *src* with long recommender names mapped to short keys.

    Keys already in short form are kept as-is.  Nested dicts (like
    ``score_breakdown``) are normalised recursively one level deep.
    """
    out: Dict[str, Any] = {}
    for key, value in src.items():
        short = _LONG_TO_SHORT.get(key, key)
        # If both "content" and "C" are present, prefer the short key
        if short in out:
            continue
        if isinstance(value, dict) and key in ("score_breakdown", "weights"):
            value = {_LONG_TO_SHORT.get(k, k): v for k, v in value.items()}
        out[short] = value
    return out

FRIENDLY_REASON_SNIPPETS: Dict[str, str] = {
    "C": "it focuses on the skills you're practising right now",
    "CF": "learners on a similar path said it helped",
    "P": "many people in this course found it useful",
    "S": "it matches the pace and tone you've responded well to",
    "D": "it keeps some variety in your study plan",
}

# Short labels used when building weight-aware summaries
COMPONENT_SHORT_LABELS: Dict[str, str] = {
    "C": "skill relevance",
    "CF": "similar-learner patterns",
    "P": "community popularity",
    "S": "sentiment alignment",
    "D": "variety balance",
}

DEFAULT_SHORT_SUMMARY = "We chose this to keep you moving without adding extra load."


class ExplanationService:
    """Generates deterministic explanation payloads for recommendation items."""

    def __init__(self, use_shap: bool = False):
        self.use_shap = use_shap
        self._shap_ready = False
        if use_shap:
            try:  # pragma: no cover - optional dependency
                import shap  # type: ignore

                self.shap = shap
                self._shap_ready = True
            except Exception:
                self._shap_ready = False

    def _friendly_label(self, key: str) -> str:
        return COMPONENT_LABELS.get(key, key)

    @staticmethod
    def _build_short_summary(
        top_positive: List[Dict[str, Any]],
        friendly_factors: List[str],
        raw_weights: Dict[str, float],
    ) -> str:
        """Build a data-driven short summary referencing actual signal strengths.

        Produces sentences like:
          "Skill relevance was the strongest signal (45%), supported by
           similar-learner patterns (25%). We chose this because it focuses
           on the skills you're practising right now."
        """
        if not top_positive:
            return DEFAULT_SHORT_SUMMARY

        # Compute normalised percentages from raw weights for the positive
        # contributors so the learner sees how much each signal mattered.
        weight_total = sum(
            abs(raw_weights.get(k, 0.0)) for k in COMPONENT_ORDER
        )

        def _pct(component_key: str) -> int:
            if weight_total <= 0:
                return 0
            return round(abs(raw_weights.get(component_key, 0.0)) / weight_total * 100)

        leader = top_positive[0]
        leader_label = COMPONENT_SHORT_LABELS.get(
            leader["component"], leader["feature"]
        )
        leader_pct = _pct(leader["component"])

        parts: List[str] = []
        if len(top_positive) >= 2:
            second = top_positive[1]
            second_label = COMPONENT_SHORT_LABELS.get(
                second["component"], second["feature"]
            )
            second_pct = _pct(second["component"])
            parts.append(
                f"{leader_label.capitalize()} was the strongest signal ({leader_pct}%), "
                f"supported by {second_label} ({second_pct}%)."
            )
        else:
            parts.append(
                f"{leader_label.capitalize()} was the main signal ({leader_pct}%)."
            )

        # Append the friendly reason for the top contributor.
        if friendly_factors:
            parts.append(f"We chose this because {friendly_factors[0]}.")

        return " ".join(parts)

    def _normalize_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        total = sum(abs(weights.get(k, 0.0)) for k in COMPONENT_ORDER)
        normalized: Dict[str, float] = {}
        for key in COMPONENT_ORDER:
            label = self._friendly_label(key)
            value = abs(weights.get(key, 0.0))
            normalized[label] = value / total if total else 0.0
        return normalized

    def _extract_components(
        self,
        item: Dict[str, Any],
        snapshot: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        snapshot = snapshot or {}
        features_src = snapshot.get("features")
        if not isinstance(features_src, dict):
            features_src = item.get("components", {}) or {}
        # Normalise long recommender names (content/cf/…) → short keys (C/CF/…)
        features_src = _normalise_keys(features_src)

        weights_src: Any = snapshot.get("weights")
        if not isinstance(weights_src, dict):
            weights_src = item.get("components", {}).get("weights", {})
        if isinstance(weights_src, dict):
            weights_src = _normalise_keys(weights_src)
        policy_weights: Dict[str, float] = {}
        component_weights: Dict[str, float] = {}
        if isinstance(weights_src, dict):
            for w_key, w_val in weights_src.items():
                if w_key == "policy_weights" and isinstance(w_val, dict):
                    policy_weights = {str(k): float(v) for k, v in w_val.items()}
                    continue
                if isinstance(w_val, (int, float)):
                    component_weights[w_key] = float(w_val)
        elif isinstance(weights_src, (int, float)):
            component_weights["value"] = float(weights_src)

        feature_values: Dict[str, float] = {}
        for key in COMPONENT_ORDER:
            raw = features_src.get(key) if isinstance(features_src, dict) else None
            try:
                feature_values[key] = float(raw)
            except (TypeError, ValueError):
                feature_values[key] = 0.0

        score_breakdown_src = (
            features_src.get("score_breakdown")
            if isinstance(features_src, dict)
            else None
        )
        contributions: Dict[str, float] = {}
        if isinstance(score_breakdown_src, dict):
            for key in COMPONENT_ORDER:
                try:
                    contributions[key] = float(score_breakdown_src.get(key, 0.0))
                except (TypeError, ValueError):
                    contributions[key] = 0.0
        else:
            for key in COMPONENT_ORDER:
                weight = component_weights.get(key, 0.0)
                value = feature_values.get(key, 0.0)
                if key == "D":
                    contributions[key] = -value * weight
                else:
                    contributions[key] = value * weight

        model_versions: Dict[str, Any] = {}
        if isinstance(features_src, dict):
            mv = features_src.get("model_versions") or features_src.get("model_version")
            if isinstance(mv, dict):
                model_versions = {str(k): str(v) for k, v in mv.items()}

        score = snapshot.get("score")
        if score is None:
            score = item.get("score")
        try:
            score_value = float(score) if score is not None else None
        except (TypeError, ValueError):
            score_value = None

        return {
            "features": feature_values,
            "weights": component_weights,
            "policy_weights": policy_weights,
            "contributions": contributions,
            "model_versions": model_versions,
            "score": score_value,
        }

    def _shap_explain(
        self,
        features: Dict[str, float],
        weights: Dict[str, float],
    ) -> Optional[Dict[str, float]]:
        if not self._shap_ready:
            return None
        try:  # pragma: no cover - optional dependency path
            import numpy as np
            from sklearn.linear_model import LinearRegression

            names = [key for key in COMPONENT_ORDER if key in features]
            if not names:
                return None
            X = np.eye(len(names))
            y = np.array([weights.get(name, 0.0) for name in names], dtype=float)
            model = LinearRegression(fit_intercept=False).fit(X, y)
            explainer = self.shap.Explainer(model.predict, X)
            x = np.array([[features.get(name, 0.0) for name in names]])
            shap_values = explainer(x)
            vals = shap_values.values[0].tolist()
            shap_map = {
                self._friendly_label(name): float(val)
                for name, val in zip(names, vals)
            }
            return shap_map
        except Exception:
            return None

    def explain_item(
        self,
        item: Dict[str, Any],
        level: str = "auto",
        snapshot: Optional[Dict[str, Any]] = None,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        snapshot = snapshot or {}
        provenance = provenance or {}
        components = self._extract_components(item, snapshot)

        normalized_weights = self._normalize_weights(components["weights"])
        friendly_contributions = {
            self._friendly_label(key): components["contributions"].get(key, 0.0)
            for key in COMPONENT_ORDER
        }
        feature_values = {
            self._friendly_label(key): components["features"].get(key, 0.0)
            for key in COMPONENT_ORDER
        }

        top_positive = [
            {
                "feature": self._friendly_label(key),
                "component": key,
                "contribution": components["contributions"].get(key, 0.0),
                "weight": components["weights"].get(key, 0.0),
                "normalized_weight": normalized_weights.get(
                    self._friendly_label(key), 0.0
                ),
            }
            for key in COMPONENT_ORDER
            if components["contributions"].get(key, 0.0) > 0
        ]
        top_positive.sort(key=lambda entry: entry["contribution"], reverse=True)
        top_features = top_positive[:3]

        # --- short summary: data-driven sentence with signal strengths ---
        friendly_factors: List[str] = []
        for entry in top_positive:
            snippet = FRIENDLY_REASON_SNIPPETS.get(entry["component"])
            if snippet and snippet not in friendly_factors:
                friendly_factors.append(snippet)

        short_summary = self._build_short_summary(
            top_positive, friendly_factors, components["weights"]
        )

        # --- detailed summary: numeric contribution breakdown ---
        ordered_parts = []
        for key in COMPONENT_ORDER:
            label = self._friendly_label(key)
            value = components["contributions"].get(key, 0.0)
            ordered_parts.append(f"{label} {'+' if value >= 0 else ''}{value:.3f}")
        detailed_summary = "Contribution breakdown: " + ", ".join(ordered_parts)
        if components.get("score") is not None:
            detailed_summary += f". Total score {components['score']:.3f}."

        summaries = {
            "short": short_summary,
            "detailed": detailed_summary,
        }
        if level == "detailed":
            selected_level = "detailed"
        else:
            selected_level = "short"
        summary_value = summaries[selected_level]

        model_versions = components.get("model_versions") or {}
        if not model_versions and isinstance(provenance.get("model_versions"), dict):
            model_versions = {
                str(k): str(v) for k, v in provenance.get("model_versions", {}).items()
            }

        provenance_payload = {
            "strategy": provenance.get("strategy"),
            "policy_version": provenance.get("policy_version"),
            "routine_version": provenance.get("routine_version") or provenance.get("policy_version"),
            "decision_id": provenance.get("decision_id"),
            "deterministic_hash": provenance.get("deterministic_hash"),
            "seed": provenance.get("seed"),
            "model_versions": model_versions,
        }
        evidence_refs = provenance.get("evidence")
        if isinstance(evidence_refs, dict):
            provenance_payload["evidence"] = evidence_refs

        diagnostics: Dict[str, Any] = {}
        if self.use_shap:
            shap_bits = self._shap_explain(components["features"], components["weights"])
            if shap_bits:
                diagnostics["shap"] = shap_bits

        item_id = item.get("item_id") or snapshot.get("item_id") or ""

        explanation = {
            "method": "transparent-combiner",
            "item_id": str(item_id),
            "summary": summary_value,
            "selected_level": selected_level,
            "summaries": summaries,
            "story": short_summary,
            "friendly_factors": friendly_factors,
            "closing_note": "We'll see how this goes and adjust your next step.",
            "top_features": top_features,
            "weights": normalized_weights,
            "contributions": friendly_contributions,
            "features": feature_values,
            "score": components.get("score"),
            "provenance": provenance_payload,
            "raw": {
                "weights": components.get("weights"),
                "policy_weights": components.get("policy_weights"),
                "score_breakdown": components.get("contributions"),
            },
        }
        if diagnostics:
            explanation["diagnostics"] = diagnostics
        return explanation
