"""Configuration for the LLM feedback generator."""
from __future__ import annotations

import os
from typing import Any, Mapping


def is_llm_feedback_enabled() -> bool:
    """Check whether the LLM feedback generator feature flag is active."""
    return os.environ.get("XELRA_LLM_FEEDBACK", "false").lower() == "true"


LLM_CONFIG: Mapping[str, Any] = {
    "provider": "ollama",
    "model": os.environ.get("XELRA_LLM_MODEL", "llama3"),
    "base_url": os.environ.get("XELRA_LLM_BASE_URL", "http://localhost:11434"),
    "temperature": float(os.environ.get("XELRA_LLM_TEMPERATURE", "0.7")),
    "max_tokens": int(os.environ.get("XELRA_LLM_MAX_TOKENS", "200")),
    "timeout_seconds": int(os.environ.get("XELRA_LLM_TIMEOUT", "10")),
    "fallback_on_failure": True,
}
