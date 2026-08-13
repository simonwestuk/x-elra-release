# xelra/settings.py (or xelra/config.py if that's your path)
import os
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

import yaml
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_root() -> str:
    # Detect Render; otherwise use a project-local cache dir
    if (
        os.getenv("RENDER")
        or os.getenv("RENDER_SERVICE_ID")
        or os.getenv("RENDER_INSTANCE_ID")
    ):
        return "/var/huggingface"
    return "./.hf_cache"


PERSISTENT_ROOT = _default_root()


def _default_model_dir() -> str:
    # Prefer explicit LOCAL_MODEL_DIR if set, else fall back to persistent root
    return os.getenv("LOCAL_MODEL_DIR", f"{PERSISTENT_ROOT}/models/sentiment")


class Settings(BaseSettings):
    # IMPORTANT: ignore unknown env vars from .env (like HF_HOME etc.)
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # <- stops 'extra_forbidden' errors
        case_sensitive=False,  # env keys often vary in case
    )

    app_name: str = "X-ELRA"

    # Development mode - shows OTP codes in UI when email fails
    dev_mode: bool = Field(
        default=False,
        alias="DEV_MODE",
        description="When true, shows OTP codes in login UI if email delivery fails",
    )

    # Model dirs (both point to the same place by default)
    model_dir: str = Field(default_factory=_default_model_dir)
    sentiment_model_path: str = Field(default_factory=_default_model_dir)

    # SQLite (defaults are local; override on Render to /var/huggingface/app/...)
    feature_store_uri: str = Field(
        default="sqlite:///./data/xelra_fs.db", alias="FEATURE_STORE_URI"
    )
    database_uri: str = Field(
        default="sqlite:///./data/xelra_app.db", alias="DATABASE_URI"
    )

    redis_url: Optional[str] = Field(default=None, alias="REDIS_URL")

    # Control routine version (replaces "policy_version" per ARL terminology alignment)
    routine_version: str = Field(default="v1", alias="ROUTINE_VERSION")
    # Backward compatibility alias
    policy_version: str | None = Field(default=None, alias="POLICY_VERSION")

    telemetry_schema_version: str = Field(
        default="1.1.0", alias="TELEMETRY_SCHEMA_VERSION"
    )

    def model_post_init(self, __context):
        """Ensure routine_version fallback for backward compatibility."""
        super().model_post_init(__context)
        if self.policy_version and not self.routine_version:
            self.routine_version = self.policy_version
        elif not self.policy_version:
            self.policy_version = self.routine_version

        # Warn loudly if JWT secrets are still at their defaults
        _insecure_defaults = {"change-me", "change-me-login"}
        if self.sso_jwt_secret in _insecure_defaults or self.login_jwt_secret in _insecure_defaults:
            import logging
            logging.getLogger(__name__).warning(
                "JWT secrets are still set to defaults — set SSO_JWT_SECRET and "
                "LOGIN_JWT_SECRET environment variables before going live"
            )

    explanation_default_level: str = "auto"
    sso_jwt_secret: str = "change-me"
    sso_expected_issuer: str = "lms"
    sso_expected_audience: str = "xelra"
    login_jwt_secret: str = "change-me-login"
    login_token_ttl_minutes: int = 43200  # 30 days
    login_jwt_issuer: str | None = Field(default=None, alias="JWT_ISSUER")
    login_jwt_audience: str | None = Field(default="xelra-login", alias="JWT_AUDIENCE")
    login_jwt_leeway_seconds: int = Field(
        default=300, alias="LOGIN_JWT_LEEWAY_SECONDS"
    )

    # Email provider settings
    # Resend (recommended for OTP emails)
    resend_api_key: Optional[str] = Field(default=None, alias="RESEND_API_KEY")
    resend_from_email: str = Field(
        default="X-ELRA <auth@xelra-learning.com>",
        alias="RESEND_FROM_EMAIL",
        description="From address for Resend emails (use verified domain in production)",
    )

    # Legacy SMTP settings (fallback if Resend not configured)
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_pass: Optional[str] = None
    smtp_use_tls: bool = True
    smtp_from: str = "xelra@localhost"

    memory_log_on_start: bool = False
    memory_log_interval_secs: Optional[int] = None

    # Registration and demo account controls
    signup_enabled: bool = Field(
        default=True,
        alias="SIGNUP_ENABLED",
        description="Allow new user registrations",
    )
    demo_learners_enabled: bool = Field(
        default=True,
        alias="DEMO_LEARNERS_ENABLED",
        description="Allow @example.com demo accounts to log in",
    )

    explanations: bool = Field(default=True, alias="EXPLANATIONS")
    feature_sentiment: bool = Field(
        default=True,
        alias="FEATURE_SENTIMENT",
        validation_alias=AliasChoices("FEATURE_SENTIMENT", "SENTIMENT"),
    )
    feature_live_code: bool = Field(
        default=False,
        alias="FEATURE_LIVE_CODE",
        validation_alias=AliasChoices("FEATURE_LIVE_CODE", "LIVE_CODE_ENABLED"),
    )
    baseline: bool = Field(default=True, alias="BASELINE")
    infer_sentiment: bool = Field(
        default=True,
        alias="INFER_SENTIMENT",
        validation_alias=AliasChoices(
            "INFER_SENTIMENT", "ENABLE_SENTIMENT_INFERENCE"
        ),
    )

    enable_formal_arl: bool = Field(
        default=True,
        alias="ENABLE_FORMAL_ARL",
        validation_alias=AliasChoices("ENABLE_FORMAL_ARL", "FORMAL_ARL"),
    )

    live_code_engine: str | None = Field(
        default=None,
        alias="LIVE_CODE_ENGINE",
        validation_alias=AliasChoices("LIVE_CODE_ENGINE", "LIVE_CODE_BACKEND"),
    )
    live_code_timeout_ms: int = Field(
        default=10_000,
        alias="LIVE_CODE_TIMEOUT_MS",
    )
    live_code_max_output: int = Field(
        default=8_192,
        alias="LIVE_CODE_MAX_OUTPUT",
    )
    live_code_allow_input: bool = Field(
        default=False,
        alias="LIVE_CODE_ALLOW_INPUT",
    )

    live_code_telemetry_base_url: str = Field(
        default="/v1/telemetry/live",
        alias="LIVE_CODE_TELEMETRY_BASE_URL",
    )

    rate_limit_requests: int = Field(default=600, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: float = Field(
        default=60.0, alias="RATE_LIMIT_WINDOW_SECONDS"
    )

    # Read HF token from env if set
    hugging_face_hub_token: Optional[str] = Field(
        default=None, alias="HUGGING_FACE_HUB_TOKEN"
    )

    # Periodic survey settings for pilot study
    survey_enabled: bool = Field(default=True, alias="SURVEY_ENABLED")
    survey_url: str = Field(
        default="https://app.onlinesurveys.jisc.ac.uk/s/portsmouth/reducing-information-overload-in-e-learning-survey",
        alias="SURVEY_URL",
    )
    survey_weeks: str = Field(
        default="4,8,12",
        alias="SURVEY_WEEKS",
        description="Comma-separated list of weeks when survey should appear",
    )
    survey_codes: str = Field(
        default="",
        alias="SURVEY_CODES",
        description="Completion codes per week, e.g. '2:PILOT-W2,4:PILOT-W4'. Empty = no verification.",
    )
    pilot_start_date: Optional[str] = Field(
        default=None,
        alias="PILOT_START_DATE",
        description="Start date of pilot in YYYY-MM-DD format (uses learner signup if not set)",
    )
    survey_signup_delay_days: int = Field(
        default=5,
        alias="SURVEY_SIGNUP_DELAY_DAYS",
        description="Minimum days since signup before surveys appear. Prevents late signups seeing surveys immediately.",
    )

    # Pilot mode - enables all features (explanations + sentiment) for all users
    # regardless of their arm assignment. Use for end of study or during pilot testing.
    pilot_mode: bool = Field(
        default=False,
        alias="PILOT_MODE",
        description="When true, all users see all features regardless of arm assignment",
    )

    # Post-study feature unlock: after this date, control-group learners get
    # access to the full feature set (explanations, sentiment, etc.).
    study_end_date: Optional[str] = Field(
        default=None,
        alias="STUDY_END_DATE",
        description="End date of study in YYYY-MM-DD format. After this date, all features are unlocked for all arms.",
    )
    study_duration_weeks: int = Field(
        default=12,
        alias="STUDY_DURATION_WEEKS",
        description="Study duration in weeks. Used with pilot_start_date when study_end_date is not set.",
    )


settings = Settings()


# ---------------------------------------------------------------------------
# Experiment arm manifest loader
# ---------------------------------------------------------------------------

ARMS_MANIFEST_ENV = "ARMS_MANIFEST_PATH"


class ManifestError(RuntimeError):
    """Raised when the ARMS manifest cannot be loaded or is malformed."""


@dataclass(frozen=True)
class ArmConfig:
    """Normalised configuration for an experiment arm."""

    name: str
    strategy: str
    explain: bool
    regulatory_mode: bool
    xai_enabled: bool
    xai_level: str | None
    xai_method: str | None
    sentiment_enabled: bool
    sentiment_provider: str | None
    sentiment_model: str | None
    policy_version: str | None
    weight_map: Mapping[str, float]
    raw: Mapping[str, Any]

    @property
    def routine_version(self) -> str:
        """Alias for policy_version to align with ARL terminology."""
        return self.policy_version or settings.routine_version


_manifest_lock = threading.Lock()
_manifest_cache: Mapping[str, Any] | None = None
_manifest_path: Path | None = None


def _default_manifest_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config" / "arms.yaml"


def _resolve_manifest_path() -> Path:
    env_path = os.getenv(ARMS_MANIFEST_ENV)
    if env_path:
        return Path(env_path).expanduser().resolve()
    return _default_manifest_path().resolve()


def _load_manifest_yaml(path: Path) -> Mapping[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except FileNotFoundError as exc:
        raise ManifestError(f"ARMS manifest not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise ManifestError(f"Failed to parse ARMS manifest: {path}") from exc

    if not isinstance(data, dict):
        raise ManifestError("ARMS manifest root must be a mapping")
    return data


def _normalise_arm(name: str, payload: Mapping[str, Any]) -> ArmConfig:
    if not isinstance(payload, Mapping):
        raise ManifestError(f"Arm '{name}' must be a mapping")
    strategy = payload.get("strategy")
    if not isinstance(strategy, str) or not strategy:
        raise ManifestError(f"Arm '{name}' requires a non-empty 'strategy'")
    explain = bool(payload.get("explain", False))
    regulatory_mode = bool(payload.get("regulatory_mode", False))
    policy_version = payload.get("routine_version") or payload.get("policy_version")
    if policy_version is not None and not (
        isinstance(policy_version, str) and policy_version.strip()
    ):
        raise ManifestError(
            f"Arm '{name}' has invalid 'policy_version' (expected non-empty string)"
        )
    if policy_version is None:
        raise ManifestError(f"Arm '{name}' is missing required 'policy_version'")
    weight_map_payload = payload.get("weight_map")
    if not isinstance(weight_map_payload, Mapping):
        raise ManifestError(f"Arm '{name}' must define a 'weight_map' mapping")
    expected_weights = ("content", "cf", "popularity", "sentiment")
    weight_map: dict[str, float] = {}
    for key in expected_weights:
        value = weight_map_payload.get(key)
        if not isinstance(value, (int, float)):
            raise ManifestError(
                f"Arm '{name}' weight_map['{key}'] must be a number"
            )
        weight_map[key] = float(value)
    xai = payload.get("xai", {})
    if isinstance(xai, Mapping):
        xai_enabled = bool(xai.get("enabled", False))
        xai_level = xai.get("level") if isinstance(xai.get("level"), str) else None
        xai_method = xai.get("method") if isinstance(xai.get("method"), str) else None
    else:
        xai_enabled = False
        xai_level = None
        xai_method = None
    if xai_enabled and not xai_method:
        raise ManifestError(
            f"Arm '{name}' requires 'xai.method' when explanations are enabled"
        )
    sentiment = payload.get("sentiment", {})
    sentiment_enabled = bool(sentiment.get("enabled", False)) if isinstance(
        sentiment, Mapping
    ) else False
    if isinstance(sentiment, Mapping):
        sentiment_provider = (
            sentiment.get("provider") if isinstance(sentiment.get("provider"), str) else None
        )
        sentiment_model = (
            sentiment.get("model") if isinstance(sentiment.get("model"), str) else None
        )
    else:
        sentiment_provider = None
        sentiment_model = None
    if sentiment_enabled:
        if not sentiment_provider or not sentiment_model:
            raise ManifestError(
                f"Arm '{name}' requires 'sentiment.provider' and 'sentiment.model' when sentiment is enabled"
            )
    return ArmConfig(
        name=name,
        strategy=strategy,
        explain=explain,
        regulatory_mode=regulatory_mode,
        xai_enabled=xai_enabled,
        xai_level=xai_level,
        xai_method=xai_method,
        sentiment_enabled=sentiment_enabled,
        sentiment_provider=sentiment_provider,
        sentiment_model=sentiment_model,
        policy_version=policy_version,
        weight_map=weight_map,
        raw=payload,
    )


def refresh_arms_manifest(force: bool = False) -> Mapping[str, Any]:
    """Reload the ARMS manifest from disk."""

    global _manifest_cache, _manifest_path
    with _manifest_lock:
        path = _resolve_manifest_path()
        if not force and _manifest_cache is not None and _manifest_path == path:
            return _manifest_cache
        manifest = _load_manifest_yaml(path)
        arms = manifest.get("arms", {})
        if not isinstance(arms, Mapping):
            raise ManifestError("Manifest is missing 'arms' mapping")
        configs = {name: _normalise_arm(name, cfg) for name, cfg in arms.items()}
        manifest = dict(manifest)
        manifest["_arm_objects"] = configs
        _manifest_cache = manifest
        _manifest_path = path
        return manifest


def get_arms_manifest() -> Mapping[str, Any]:
    """Return the cached ARMS manifest, loading it on first access."""

    if _manifest_cache is None:
        return refresh_arms_manifest(force=True)
    return _manifest_cache


def get_arm_config(name: str) -> ArmConfig:
    """Return the configuration for a specific arm."""

    manifest = get_arms_manifest()
    arm_map = manifest.get("_arm_objects")
    if not isinstance(arm_map, Mapping):
        manifest = refresh_arms_manifest(force=True)
        arm_map = manifest.get("_arm_objects")
    if not isinstance(arm_map, Mapping):
        raise ManifestError("ARMS manifest has not been initialised")
    try:
        return arm_map[name]
    except KeyError as exc:
        raise ManifestError(f"Unknown arm '{name}'") from exc


def get_arm_buckets() -> Mapping[str, str]:
    """Return mapping of assignment buckets to arm identifiers."""

    manifest = get_arms_manifest()
    buckets = manifest.get("buckets", {})
    if not isinstance(buckets, Mapping):
        raise ManifestError("Manifest is missing 'buckets' mapping")
    return buckets


def get_arm_weights() -> Mapping[str, float]:
    """Return randomisation weights for each arm."""

    manifest = get_arms_manifest()
    weights = manifest.get("weights", {})
    if not isinstance(weights, Mapping):
        raise ManifestError("Manifest is missing 'weights' mapping")
    return weights


# Load manifest eagerly so configuration problems fail fast.
refresh_arms_manifest(force=True)


__all__ = [
    "settings",
    "Settings",
    "ARMS_MANIFEST_ENV",
    "ArmConfig",
    "ManifestError",
    "refresh_arms_manifest",
    "get_arms_manifest",
    "get_arm_config",
    "get_arm_buckets",
    "get_arm_weights",
]
