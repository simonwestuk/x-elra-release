"""Version/manifest endpoint exposing build, config, and migration metadata."""

import ast
import copy
import os
import json
import datetime as dt
import re
from pathlib import Path
from typing import Mapping, Optional

from fastapi import APIRouter

from ...config import ArmConfig, get_arms_manifest, settings

router = APIRouter()


def _manifest_snapshot() -> Mapping[str, object]:
    manifest = get_arms_manifest()
    arm_objects = manifest.get("_arm_objects")
    snapshot = {k: v for k, v in manifest.items() if k != "_arm_objects"}
    if isinstance(arm_objects, Mapping):
        snapshot["arms"] = {
            name: _arm_to_payload(cfg)
            for name, cfg in arm_objects.items()
            if isinstance(cfg, ArmConfig)
        }
    return snapshot


def _arm_to_payload(cfg: ArmConfig) -> Mapping[str, object]:
    base = copy.deepcopy(cfg.raw)
    base.setdefault("strategy", cfg.strategy)
    base.setdefault("explain", cfg.explain)
    base.setdefault("xai", {})
    if isinstance(base["xai"], dict):
        base["xai"].setdefault("enabled", cfg.xai_enabled)
        if cfg.xai_level is not None:
            base["xai"].setdefault("level", cfg.xai_level)
    else:
        base["xai"] = {"enabled": cfg.xai_enabled, "level": cfg.xai_level}
    base.setdefault("sentiment", {})
    if isinstance(base["sentiment"], dict):
        base["sentiment"].setdefault("enabled", cfg.sentiment_enabled)
    else:
        base["sentiment"] = {"enabled": cfg.sentiment_enabled}
    return base


def load_cfg():
    config_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "..",
        "config",
    )
    for filename in ("production_lock.json", "pilot_lock.json"):
        p = os.path.abspath(os.path.join(config_dir, filename))
        try:
            with open(p, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            continue
        except Exception:
            return {}
    return {}


@router.get("/version")
def version():
    cfg = load_cfg()
    manifest = _manifest_snapshot()
    schema_version = _get_alembic_head_revision() or "unknown"
    commit = (
        os.environ.get("GIT_COMMIT") or os.environ.get("RENDER_GIT_COMMIT") or "unknown"
    )
    build_time = os.environ.get("BUILD_TIME") or dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    payload = {
        "git_commit": commit,
        "build_time": build_time,
        "app_env": os.environ.get("APP_ENV", "unknown"),
        "config_locked": cfg.get("config_locked", "no"),
        "tag": cfg.get("tag", ""),
        "lms_enabled": cfg.get("lms_enabled", False),
        "schema_version": schema_version,
        **manifest,
    }
    feature_flags = {
        "explanations": bool(getattr(settings, "explanations", True)),
        "feature_sentiment": bool(getattr(settings, "feature_sentiment", True)),
        "baseline": bool(getattr(settings, "baseline", True)),
        "infer_sentiment": bool(getattr(settings, "infer_sentiment", True)),
        "feature_live_code": bool(getattr(settings, "feature_live_code", False)),
        "pilot_mode": bool(getattr(settings, "pilot_mode", False)),
    }
    payload["feature_flags"] = feature_flags
    payload["live_code"] = {
        "enabled": feature_flags["feature_live_code"],
        "engine": getattr(settings, "live_code_engine", None),
        "timeout_ms": int(getattr(settings, "live_code_timeout_ms", 0)),
        "max_output": int(getattr(settings, "live_code_max_output", 0)),
        "allow_input": bool(getattr(settings, "live_code_allow_input", False)),
        "telemetry_base_url": getattr(
            settings, "live_code_telemetry_base_url", "/v1/telemetry/live"
        ),
    }
    # Persist snapshot (idempotent-ish)
    try:
        from ...utils.db import engine
        import sqlalchemy as sa

        with engine.begin() as conn:
            # Use database-agnostic DDL via SQLAlchemy
            # Check if table exists first using inspector
            inspector = sa.inspect(conn)
            if "app_versions" not in inspector.get_table_names():
                # Create table using SQLAlchemy DDL (works with SQLite, PostgreSQL, etc.)
                metadata = sa.MetaData()
                app_versions = sa.Table(
                    "app_versions",
                    metadata,
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("created_at", sa.Text),
                    sa.Column("payload", sa.Text),
                )
                metadata.create_all(conn)

            # only insert if latest row differs
            rs = conn.execute(
                sa.text("SELECT payload FROM app_versions ORDER BY id DESC LIMIT 1")
            ).fetchone()
            last = rs[0] if rs else None
            cur = json.dumps(payload, sort_keys=True)
            if cur != last:
                conn.execute(
                    sa.text(
                        "INSERT INTO app_versions (created_at, payload) VALUES (:t, :p)"
                    ),
                    {"t": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"), "p": cur},
                )
    except Exception:
        pass
    return payload
_ROOT_DIR = Path(__file__).resolve().parents[3]
_ALEMBIC_DIR = _ROOT_DIR / "alembic"


def _extract_assignment(source: str, name: str) -> Optional[object]:
    pattern = re.compile(rf"^{name}\\s*=\\s*(.+)$", re.MULTILINE)
    match = pattern.search(source)
    if not match:
        return None
    value_src = match.group(1).strip()
    try:
        return ast.literal_eval(value_src)
    except Exception:
        return None


def _scan_head_revision() -> Optional[str]:
    versions_dir = _ALEMBIC_DIR / "versions"
    if not versions_dir.is_dir():
        return None

    revisions = set()
    down_revisions = set()

    for path in versions_dir.glob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue

        revision = _extract_assignment(content, "revision")
        if isinstance(revision, str):
            revisions.add(revision)

        down_revision = _extract_assignment(content, "down_revision")
        if isinstance(down_revision, str):
            down_revisions.add(down_revision)
        elif isinstance(down_revision, (list, tuple)):
            down_revisions.update(filter(lambda x: isinstance(x, str), down_revision))

    candidates = [rev for rev in revisions if rev not in down_revisions]
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    return sorted(candidates)[-1]


def _get_alembic_head_revision() -> Optional[str]:
    try:
        from alembic.script import ScriptDirectory

        script_dir = ScriptDirectory(str(_ALEMBIC_DIR))
        head = script_dir.get_current_head()
        if isinstance(head, str):
            return head
    except Exception:
        pass

    return _scan_head_revision()
