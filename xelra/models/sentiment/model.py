"""Transformer-backed sentiment scoring utilities for learner text inputs."""

import logging
import os
import re
from typing import List, Optional, Sequence, Tuple

# ---------- environment & backend sanity ----------
# Avoid tokenizers thread deadlocks / oversubscription (common on macOS)
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# Optional: cap CPU threads to avoid MKL/OpenMP thrash on first call
try:
    import torch
    if torch.get_num_threads() > 8:
        torch.set_num_threads(8)
except Exception:
    pass

import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from ...config import settings

# Optional: bump Transformers logging while debugging initialisation/downloads
try:
    from transformers.utils.logging import set_verbosity_info  # type: ignore
except Exception:
    pass

try:
    from lime.lime_text import LimeTextExplainer
except Exception:  # optional dependency
    LimeTextExplainer = None

try:
    import shap  # type: ignore
except Exception:  # optional dependency
    shap = None

try:
    from huggingface_hub import InferenceClient  # type: ignore
except Exception:  # optional dependency
    InferenceClient = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------- lightweight text chunkers ----------

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def to_sentences(text: str, min_len: int = 3) -> List[str]:
    """Dependency-free sentence splitter for long documents.

    Filters out ultra-short fragments that are often punctuation or headers.
    """
    if not text:
        return []
    sents = [s.strip() for s in _SENT_SPLIT.split(text)]
    return [s for s in sents if len(s) >= min_len]


def to_token_chunks(text: str, tokenizer, max_tokens: int = 128, stride: int = 32) -> List[str]:
    """Chunk long text by token count to stay within model max length.

    Uses the model's tokenizer to create overlapping windows (via stride) and
    decodes them back to plain text for downstream use.
    """
    if not text:
        return []
    enc = tokenizer(
        text,
        return_overflowing_tokens=True,
        truncation=True,
        max_length=max_tokens,
        stride=stride,
    )
    input_ids = enc.get("input_ids", [])
    return [tokenizer.decode(ids, skip_special_tokens=True) for ids in input_ids]


class SentimentModel:
    def __init__(
        self,
        model_name: str = os.getenv("SENTIMENT_MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english"),
        local_dir: Optional[str] = None,
        tokenizer=None,
        model=None,
        enable_shap: bool = False,
        device: Optional[int] = -1,  # default CPU to avoid slow GPU/MPS init stalls; set 0 for first GPU
        batch_size: int = 32,         # larger default for speed; tune per hardware
        chunk_size: int = 32,         # retained for back-compat; no longer used in _predict_proba
    ):
        """
        Initialise the SentimentModel.

        If tokenizer/model are provided, they are used directly.
        Otherwise we try to load from local_dir; if that fails we download model_name
        into local_dir and load from there.
        """
        # Allow env to override the model selection
        resolved_local_dir = local_dir or os.getenv("LOCAL_MODEL_DIR") or settings.sentiment_model_path
        self.local_dir = resolved_local_dir
        self.model_name = model_name
        # Optional: log chosen model
        logger.info("Using sentiment model: %s", self.model_name)
        self._lime = None
        self._shap = None
        self._positive_label, self._negative_label = "POSITIVE", "NEGATIVE"
        self._chunk_size = max(1, int(chunk_size))
        self._device = device
        self._batch_size = batch_size
        # Batch size for remote HF API calls (tunable via env). Helps avoid N HTTP calls for N texts.
        self._remote_max_batch = int(os.getenv("HF_REMOTE_MAX_BATCH", "64"))

        # Mode selection
        self.use_hf_api = os.getenv("USE_HF_API", "").lower() not in ("", "0", "false")
        self.use_default_pipeline = os.getenv("SENTIMENT_USE_DEFAULT_PIPELINE", "1").lower() not in ("", "0", "false")
        self.sentiment_analyzer = None
        self._remote_client = None

        # Decide and initialise the chosen mode
        if self.use_hf_api and not self.use_default_pipeline:
            # REMOTE: Hugging Face Inference API with SENTIMENT_MODEL_NAME
            print(f"Sentiment mode: REMOTE (Inference API) - model={self.model_name}")
            if InferenceClient is not None and self.model_name:
                try:
                    hf_token = os.getenv("HUGGING_FACE_HUB_TOKEN") or os.getenv("HF_TOKEN")
                    self._remote_client = InferenceClient(self.model_name, token=hf_token)
                    # Warm-up to infer labels if possible
                    try:
                        warm = self._remote_client.text_classification("ok", top_k=None)
                        scores = self._normalise_single(warm)
                        labels = [d.get("label", "").upper() for d in scores]
                        if any("POS" in l for l in labels) and any("NEG" in l for l in labels):
                            self._positive_label = next(l for l in labels if "POS" in l)
                            self._negative_label = next(l for l in labels if "NEG" in l)
                    except Exception as e:  # pragma: no cover - best effort
                        msg = str(e).lower()
                        if "401" in msg or "unauthorized" in msg:
                            logger.warning("Remote warm-up unauthorized. Falling back to LOCAL.")
                            self.use_hf_api = False
                            self._remote_client = None
                        else:
                            logger.warning("Remote warm-up failed (continuing): %s", e)
                except Exception as e:
                    logger.warning("Failed to init InferenceClient (%s). Falling back to LOCAL.", e)
                    self.use_hf_api = False
                    self._remote_client = None
            else:
                logger.warning("InferenceClient unavailable. Falling back to LOCAL.")
                self.use_hf_api = False

            if not self.use_hf_api or self._remote_client is None:
                # Fall back to LOCAL init below
                print(f"Sentiment mode: LOCAL (fallback) - local_dir={resolved_local_dir}")

        elif self.use_hf_api and self.use_default_pipeline:
            # REMOTE DEFAULT: transformers pipeline default model (no Inference API)
            print("Sentiment mode: REMOTE DEFAULT (transformers pipeline default model)")
            try:
                self.sentiment_analyzer = pipeline(
                    task="sentiment-analysis",
                    device=device,
                    batch_size=batch_size,
                )
                try:
                    _ = self.sentiment_analyzer(["ok", "fine"], top_k=None)
                    logger.info("Pipeline warm-up completed.")
                except Exception as e:
                    logger.warning("Warm-up failed (continuing): %s", e)
                try:
                    mdl = getattr(self.sentiment_analyzer, "model", None)
                    if mdl is not None:
                        self._positive_label, self._negative_label = self._infer_label_names(mdl)
                except Exception:
                    pass
            except Exception as e:
                logger.warning(
                    "Failed to create default sentiment pipeline (%s). "
                    "Falling back to LOCAL.",
                    e,
                )
                self.use_hf_api = False
                self.sentiment_analyzer = None

        if not self.use_hf_api or (self.use_hf_api and not self.use_default_pipeline and self._remote_client is None):
            # LOCAL: load/download model into LOCAL_MODEL_DIR and build pipeline with model+tokenizer
            print(f"Sentiment mode: LOCAL - local_dir={resolved_local_dir}")
            if tokenizer is not None and model is not None:
                tok, mdl = tokenizer, model
            else:
                tok, mdl = self._load_or_download(resolved_local_dir, self.model_name)
            self.sentiment_analyzer = pipeline(
                task="sentiment-analysis",
                model=mdl,
                tokenizer=tok,
                device=device,
                batch_size=batch_size,
            )
            try:
                _ = self.sentiment_analyzer(["ok", "fine"], top_k=None)
                logger.info("Pipeline warm-up completed.")
            except Exception as e:
                logger.warning("Warm-up failed (continuing): %s", e)
            self._positive_label, self._negative_label = self._infer_label_names(mdl)

        # Optional SHAP support
        self._enable_shap = enable_shap and shap is not None
        if self._enable_shap:
            try:
                self._shap = shap.Explainer(self._predict_proba)  # type: ignore
            except Exception as e:
                logger.warning("SHAP initialisation failed: %s", e)
                self._shap = None
                self._enable_shap = False

        # LIME samples
        try:
            default_lime_samples = 1000 if (self.use_hf_api and not self.use_default_pipeline) else 5000
            self._lime_samples = int(os.getenv("LIME_NUM_SAMPLES", str(default_lime_samples)))
        except Exception:
            self._lime_samples = 1000 if (self.use_hf_api and not self.use_default_pipeline) else 5000

    # ---------- setup helpers ----------

    def _load_or_download(
        self, local_dir: str, model_name: str
    ) -> Tuple[AutoTokenizer, AutoModelForSequenceClassification]:
        """
        Try loading from local_dir; if that fails, download model_name and save there.
        This avoids guessing which files must exist.
        """
        try:
            tok = AutoTokenizer.from_pretrained(local_dir, local_files_only=True)
            mdl = AutoModelForSequenceClassification.from_pretrained(
                local_dir, local_files_only=True
            )
            logger.info("Loaded model from local_dir '%s'.", local_dir)
            return tok, mdl
        except Exception:
            logger.info("Local model not found/invalid at '%s'. Downloading…", local_dir)
            os.makedirs(local_dir, exist_ok=True)
            tok = AutoTokenizer.from_pretrained(model_name)
            mdl = AutoModelForSequenceClassification.from_pretrained(model_name)
            tok.save_pretrained(local_dir)
            mdl.save_pretrained(local_dir)
            logger.info("Model downloaded to '%s'.", local_dir)
            return tok, mdl

    @staticmethod
    def _infer_label_names(model) -> Tuple[str, str]:
        """
        Determine which label is positive/negative from config, falling back gracefully.
        """
        cfg = getattr(model, "config", None)
        id2label = getattr(cfg, "id2label", None) or {}
        labels = {k: v.upper() for k, v in id2label.items()}
        # Common cases
        if any("POS" in v for v in labels.values()) and any("NEG" in v for v in labels.values()):
            pos = next(v for v in labels.values() if "POS" in v)
            neg = next(v for v in labels.values() if "NEG" in v)
            return pos, neg
        # Heuristic fallback for binary classifiers: assume id 1 is positive
        if 1 in labels and 0 in labels:
            return labels[1], labels[0]
        # Absolute fallback used by SST-2
        return "POSITIVE", "NEGATIVE"

    def _ensure_local_pipeline(self) -> None:
        """Initialise the local transformers pipeline on demand."""
        if self.sentiment_analyzer is not None:
            return
        # LOCAL on-demand initialisation
        tok, mdl = self._load_or_download(self.local_dir, self.model_name)
        self.sentiment_analyzer = pipeline(
            task="sentiment-analysis",
            model=mdl,
            tokenizer=tok,
            device=self._device,
            batch_size=self._batch_size,
        )
        try:
            _ = self.sentiment_analyzer(["ok", "fine"], top_k=None)
            logger.info("Pipeline warm-up completed.")
        except Exception as e:
            logger.warning("Warm-up failed (continuing): %s", e)
        self._positive_label, self._negative_label = self._infer_label_names(mdl)

    # ---------- output equalisers ----------

    def _normalise_single(self, output):
        """
        For a single input, pipeline(..., top_k=None) can return:
          - List[Dict]          (new style for single input)
          - List[List[Dict]]    (older behaviour or other tasks)
          - Dict                (if top_k=1 or other edge cases)
        Return a List[Dict].
        """
        if isinstance(output, dict):
            return [output]
        if isinstance(output, list):
            if output and isinstance(output[0], dict):
                return output                      # List[Dict]
            if output and isinstance(output[0], list):
                return output[0]                   # List[List[Dict]] -> first sample
            return []
        return []

    def _normalise_batch(self, outputs):
        """
        For batch inputs, ensure we always have List[List[Dict]].
        """
        normalised = []
        for item in outputs:
            if isinstance(item, dict):
                normalised.append([item])
            elif isinstance(item, list) and item and isinstance(item[0], dict):
                normalised.append(item)            # List[Dict]
            elif isinstance(item, list) and item and isinstance(item[0], list):
                normalised.append(item)            # List[List[Dict]]
            else:
                normalised.append([])
        return normalised

    # ---------- public API ----------

    def score(self, text: Optional[str]) -> float:
        """
        Return sentiment in [-1, 1]. Uses top_k=None (replacement for return_all_scores=True).
        """
        if not text:
            return 0.0
        if self.use_hf_api and self._remote_client is not None:
            try:
                raw = self._remote_client.text_classification(text, top_k=None)
                scores = self._normalise_single(raw)
                by_label = {d["label"].upper(): float(d["score"]) for d in scores}
                pos = by_label.get(self._positive_label, by_label.get("LABEL_1", 0.5))
                neg = by_label.get(self._negative_label, by_label.get("LABEL_0", 0.5))
                s = (pos - neg) / max(pos + neg, 1e-9)
                return float(np.clip(s, -1.0, 1.0))
            except Exception as exc:
                logger.warning("Remote inference failed, trying local: %s", exc)

        try:
            self._ensure_local_pipeline()
            raw = self.sentiment_analyzer(text, top_k=None)
            scores = self._normalise_single(raw)
            by_label = {d["label"].upper(): float(d["score"]) for d in scores}
            pos = by_label.get(self._positive_label, by_label.get("LABEL_1", 0.5))
            neg = by_label.get(self._negative_label, by_label.get("LABEL_0", 0.5))
            s = (pos - neg) / max(pos + neg, 1e-9)
            return float(np.clip(s, -1.0, 1.0))
        except Exception as exc:
            logger.exception("Error during sentiment analysis: %s", exc)
            return 0.0

    # New: return (polarity, confidence) using model probabilities
    def score_confidence(self, text: Optional[str]) -> Tuple[float, float]:
        """
        Compute sentiment polarity in [-1,1] and confidence as max(prob_pos, prob_neg).
        Returns (0.0, 0.0) on empty input.  Raises on model failure so callers
        can decide how to handle it.
        """
        if not text:
            return 0.0, 0.0
        probs = self._predict_proba([text])  # shape (1,2): [neg, pos]
        if probs.shape[0] == 0:
            raise RuntimeError("sentiment model returned empty predictions")
        neg, pos = float(probs[0, 0]), float(probs[0, 1])
        ssum = max(neg + pos, 1e-12)
        polarity = float(np.clip((pos - neg) / ssum, -1.0, 1.0))
        confidence = float(max(pos, neg))
        return polarity, confidence

    def batch_predict(self, texts: Sequence[Optional[str]]) -> List[dict]:
        """Return sentiment polarity/label/confidence for a batch of texts.

        Each result dict contains:

        * ``polarity``   – value in ``[-1, 1]`` derived from positive/negative probs
        * ``confidence`` – ``max(prob_pos, prob_neg)``
        * ``label``      – positive/negative label chosen via the max probability
        * ``probabilities`` – mapping with ``{"negative": ..., "positive": ...}``
        """

        probs = self._predict_proba(["" if t is None else str(t) for t in texts])
        results: List[dict] = []
        for row in probs:
            if len(row) != 2:
                neg_prob, pos_prob = 0.5, 0.5
            else:
                neg_prob, pos_prob = float(row[0]), float(row[1])
            total = neg_prob + pos_prob if (neg_prob + pos_prob) > 1e-12 else 1e-12
            polarity = float(np.clip((pos_prob - neg_prob) / total, -1.0, 1.0))
            confidence = float(max(neg_prob, pos_prob))
            label = self._positive_label if pos_prob >= neg_prob else self._negative_label
            results.append(
                {
                    "polarity": polarity,
                    "confidence": confidence,
                    "label": label,
                    "probabilities": {
                        "negative": float(neg_prob),
                        "positive": float(pos_prob),
                    },
                }
            )
        return results

    def topic_affinity(self, text: Optional[str], topics: List[str]) -> float:
        """
        Return a graded affinity score in [0,1] based on token overlap (Jaccard).
        """
        if not text or not topics:
            return 0.0
        toks = set(self.tokenize(text))
        cues = set()
        for tp in topics:
            cues |= set(re.findall(r"[A-Za-z']+", str(tp).lower()))
        if not cues:
            return 0.0
        inter = len(toks & cues)
        union = len(toks | cues)
        return inter / union

    def explain_tokens(self, text: str) -> dict:
        """Return token attributions for LIME (reliable) and SHAP (best-effort).

        The structure mirrors the front-end contract and always returns
        ``{"lime": {...}, "shap": {...}}`` where each inner mapping has:

        * ``tokens`` – list of token strings
        * ``weightsPos`` – ``[[index, weight], ...]`` for positive class
        * ``weightsNeg`` – ``[[index, weight], ...]`` for negative class

        Missing explainers or failures produce empty structures so callers can
        fall back gracefully.
        """

        lime = {"tokens": [], "weightsPos": [], "weightsNeg": []}
        shap_res = {"tokens": [], "weightsPos": [], "weightsNeg": []}

        if LimeTextExplainer is not None:
            try:
                if self._lime is None:
                    self._lime = LimeTextExplainer(
                        class_names=[self._negative_label.lower(), self._positive_label.lower()]
                    )
                exp = self._lime.explain_instance(
                    text,
                    self._predict_proba,
                    labels=[0, 1],
                    num_features=1000,
                    # Reduce calls when remote; configurable via self._lime_samples
                    num_samples=self._lime_samples,
                )

                # Get LIME's view of the text (preserving spaces) if available.
                idx_str = getattr(exp.domain_mapper, "indexed_string", None)
                toks_attr = getattr(idx_str, "as_list", None)
                toks = toks_attr() if callable(toks_attr) else toks_attr
                if not toks:
                    # Fallback: split preserving spaces so the UI can retain shape
                    toks = re.findall(r"\S+|\s+", text)

                # Build non-space token sequence and normalised forms
                nonspace_abs = []
                nonspace_norm = []
                for i, tok in enumerate(toks):
                    if tok and not tok.isspace():
                        nonspace_abs.append(i)
                        # Normalise to word-ish for matching LIME features
                        nonspace_norm.append(re.sub(r"[^A-Za-z']+", "", tok).lower())

                from collections import defaultdict

                def accumulate_by_nonspace_index(label: int):
                    acc = defaultdict(float)
                    as_list = getattr(exp, "as_list", None)
                    pairs = as_list(label=label) if callable(as_list) else []
                    for feat, w in pairs:
                        # LIME features are words (bag-of-words). Match against our non-space tokens.
                        wnorm = re.sub(r"[^A-Za-z']+", "", str(feat)).lower()
                        # Find all non-space token indices (in non-space coordinate j = 0..N-1) that match
                        matches = [j for j, n in enumerate(nonspace_norm) if n == wnorm]
                        if not matches:
                            continue
                        share = float(w) / len(matches)
                        for j in matches:
                            acc[j] += share
                    return acc

                neg_acc = accumulate_by_nonspace_index(0)
                pos_acc = accumulate_by_nonspace_index(1)

                # Important: indices are over non-space tokens (j), which the UI expects
                lime = {
                    "tokens": list(toks),
                    "weightsNeg": [[int(j), float(w)] for j, w in neg_acc.items()],
                    "weightsPos": [[int(j), float(w)] for j, w in pos_acc.items()],
                }
            except Exception as e: 
                logger.warning("LIME explanation failed: %s", e)

        if self._enable_shap and self._shap is not None:
            try:
                sv = self._shap([text])  # type: ignore
                exp = sv[0]
                toks = list(getattr(exp, "data", []))
                vals = np.array(getattr(exp, "values", []), dtype=float)
                neg_vals: np.ndarray
                pos_vals: np.ndarray
                if vals.ndim == 1:
                    neg_vals = np.zeros_like(vals)
                    pos_vals = vals
                elif vals.ndim == 2:
                    if vals.shape[0] == len(toks):
                        neg_vals = vals[:, 0] if vals.shape[1] > 0 else np.zeros(len(toks))
                        pos_vals = vals[:, 1] if vals.shape[1] > 1 else np.zeros(len(toks))
                    else:
                        neg_vals = vals[0] if vals.shape[0] > 0 else np.zeros(vals.shape[1])
                        pos_vals = vals[1] if vals.shape[0] > 1 else np.zeros(vals.shape[1])
                else:
                    neg_vals = np.zeros(len(toks))
                    pos_vals = np.zeros(len(toks))
                shap_res = {
                    "tokens": toks,
                    "weightsNeg": [[i, float(v)] for i, v in enumerate(neg_vals.tolist())],
                    "weightsPos": [[i, float(v)] for i, v in enumerate(pos_vals.tolist())],
                }
            except Exception as e:  # pragma: no cover - best effort
                logger.warning("SHAP explanation failed: %s", e)

        return {"lime": lime, "shap": shap_res}

    # ---------- internal helpers ----------

    def _predict_proba(self, texts: List[str]) -> np.ndarray:
        """Return [[neg, pos], ...] probabilities for a list of texts."""
        # Accept any sequence-like and coerce to strings while preserving order
        try:
            texts = list(texts)  # type: ignore
        except Exception:
            raise AssertionError("texts must be a sequence of strings")

        # Flatten nested singletons (e.g., ['text'] or array(['text'], dtype='<U...'))
        flat_texts: List[str] = []
        for t in texts:
            if isinstance(t, (list, tuple, np.ndarray)) and not isinstance(t, (str, bytes)):
                t = t[0] if len(t) > 0 else ""
            flat_texts.append("" if t is None else str(t))
        texts = flat_texts

        n = len(texts)
        if n == 0:
            return np.zeros((0, 2), dtype=float)

        # Keep alignment: neutral probs for empty/whitespace entries
        probs = np.full((n, 2), 0.5, dtype=float)
        mask = [bool(t.strip()) for t in texts]

        if any(mask):
            nonempty_texts = [t for t, m in zip(texts, mask) if m]
            outs = None
            if self.use_hf_api and self._remote_client is not None:
                try:
                    # Batch remote requests to reduce HTTP round-trips.
                    outs_all = []
                    bs = max(1, int(self._remote_max_batch))
                    for start in range(0, len(nonempty_texts), bs):
                        batch = nonempty_texts[start : start + bs]
                        raw = self._remote_client.text_classification(batch, top_k=None)
                        outs_all.extend(self._normalise_batch(raw))
                    outs = outs_all
                except Exception as exc:
                    logger.warning("Remote inference failed, trying local: %s", exc)
                    outs = None

            if outs is None:
                self._ensure_local_pipeline()
                outs = self.sentiment_analyzer(nonempty_texts, top_k=None)
                outs = self._normalise_batch(outs)

            pos_lab, neg_lab = self._positive_label, self._negative_label
            fill_idx = (i for i, m in enumerate(mask) if m)
            for scores in outs:
                i = next(fill_idx)
                by_label = {d["label"].upper(): float(d["score"]) for d in scores}
                pos = by_label.get(pos_lab, by_label.get("LABEL_1", 0.5))
                neg = by_label.get(neg_lab, by_label.get("LABEL_0", 0.5))
                ssum = pos + neg if (pos + neg) > 1e-12 else 1e-12
                probs[i] = [neg / ssum, pos / ssum]

        return probs

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """
        Tokenise the input text into words.
        """
        return re.findall(r"[A-Za-z']+", text.lower())
