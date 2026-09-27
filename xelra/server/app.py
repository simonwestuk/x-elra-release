# xelra/server/app.py
import asyncio
import logging
import os
import sys, subprocess, importlib
import time
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict
from uuid import uuid4


# --- Ensure SQLite parents exist BEFORE importing the engine ---
def _ensure_sqlite_parent(uri: str):
    if uri.startswith("sqlite:////"):  # absolute path
        db_path = "/" + uri[len("sqlite:////") :]
    elif uri.startswith("sqlite:///"):  # relative path
        db_path = uri[len("sqlite:///") :]
    else:
        return
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)


# Read the same env vars your Settings uses (works even before Settings import)
FEATURE_STORE_URI = os.getenv("FEATURE_STORE_URI", "sqlite:///./data/xelra_fs.db")
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./data/xelra_app.db")
_ensure_sqlite_parent(FEATURE_STORE_URI)
_ensure_sqlite_parent(DATABASE_URI)

# Now it is safe to import the DB engine (the folders exist)
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from ..utils.db import Base, SessionLocal, engine
from ..utils.sentiment_aggregator import update_sentiment_aggregates

Base.metadata.create_all(bind=engine)

# xelra/server/app.py
from fastapi import FastAPI
from pathlib import Path
import os

# --- Settings & early filesystem preparation ---------------------------------
try:
    # Adjust the import path if your settings live elsewhere
    from ..config import settings
except Exception:
    # Fall back gracefully if settings import fails early
    class _Fallback:  # minimal defaults
        sentiment_model_path = "./local_model"
        feature_store_uri = "sqlite:///./data/xelra_fs.db"
        database_uri = "sqlite:///./data/xelra_app.db"
        explanations = True
        feature_sentiment = True
        baseline = True
        infer_sentiment = True
        rate_limit_requests = 600
        rate_limit_window_seconds = 60.0

    settings = _Fallback()


logger = logging.getLogger(__name__)


def _ensure_request_id(request: Request) -> str:
    request_id = getattr(request.state, "request_id", None)
    if not request_id:
        request_id = str(uuid4())
        request.state.request_id = request_id
    return request_id


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request identifier to each request/response pair."""

    def __init__(self, app, header: str = "X-Request-ID"):
        super().__init__(app)
        self.header = header

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        incoming = request.headers.get(self.header)
        request_id = incoming or getattr(request.state, "request_id", None) or str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers.setdefault(self.header, request_id)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter keyed by client address."""

    def __init__(self, app, *, limit: int, window_seconds: float):
        super().__init__(app)
        self.limit = max(1, int(limit))
        self.window = max(0.1, float(window_seconds))
        self._hits: Dict[str, deque[float]] = {}
        self._lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        now = time.monotonic()
        key = request.client.host if request.client else "global"
        async with self._lock:
            bucket = self._hits.setdefault(key, deque())
            while bucket and now - bucket[0] > self.window:
                bucket.popleft()
            if len(bucket) >= self.limit:
                request_id = _ensure_request_id(request)
                return JSONResponse(
                    {
                        "detail": "We’re getting requests faster than we can respond. Please wait a few seconds and refresh the page.",
                        "request_id": request_id,
                        "reason": "rate_limit",
                        "retry_after_seconds": max(int(self.window), 1),
                    },
                    status_code=429,
                )
            bucket.append(now)
        response = await call_next(request)
        if not bucket:
            self._hits.pop(key, None)
        return response


class FeatureFlagMiddleware(BaseHTTPMiddleware):
    """Block flagged endpoints and expose feature flags via request state."""

    def __init__(self, app, *, flags: Dict[str, bool]):
        super().__init__(app)
        self.flags = {name: bool(value) for name, value in flags.items()}
        self.routes: Dict[str, tuple[str, ...]] = {
            "explanations": (
                "/v1/telemetry/explanation",
                "/v1/feedback/latest_explain",
            ),
            "feature_sentiment": ("/v1/feedback",),
            "baseline": ("/v1/baseline",),
            "infer_sentiment": ("/v1/sentiment",),
            "feature_live_code": (
                "/v1/live-code",
                "/v1/content/live-code",
            ),
        }

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        request.state.feature_flags = self.flags
        path = request.url.path
        for flag_name, prefixes in self.routes.items():
            if self.flags.get(flag_name, True):
                continue
            if any(path.startswith(prefix) for prefix in prefixes):
                request_id = _ensure_request_id(request)
                return JSONResponse(
                    {
                        "detail": f"Feature '{flag_name}' is disabled",
                        "request_id": request_id,
                    },
                    status_code=404,
                )
        return await call_next(request)


def _ensure_dir(p: str | os.PathLike):
    Path(p).mkdir(parents=True, exist_ok=True)


def _ensure_sqlite_parent(uri: str):
    """
    Create parent directory for sqlite:///relative.db and sqlite:////absolute.db
    """
    path = None
    if uri.startswith("sqlite:////"):  # absolute
        path = Path("/" + uri[len("sqlite:////") :])
    elif uri.startswith("sqlite:///"):  # relative to CWD
        path = Path(uri[len("sqlite:///") :])
    if path is not None:
        _ensure_dir(path.parent)


# Create directories needed by the app before anything imports/uses them
try:
    # Sentiment model directory (local or /var/huggingface/... on Render)
    _ensure_dir(Path(settings.sentiment_model_path).parent)

    # SQLite stores
    _ensure_sqlite_parent(settings.feature_store_uri)
    _ensure_sqlite_parent(settings.database_uri)

    # Optional: Hugging Face caches if env vars are set
    for env_key in ("HF_HOME", "TRANSFORMERS_CACHE", "HF_HUB_CACHE"):
        v = os.getenv(env_key)
        if v:
            _ensure_dir(v)
except Exception as _e:
    # Keep startup resilient; router import below will print detailed errors if needed
    print(f"[startup-warn] Pre-flight directory setup warning: {_e}")

# --- DB schema creation -------------------------------------------------------
from ..utils.db import Base, engine

Base.metadata.create_all(bind=engine)

# --- Lifespan context manager for startup/shutdown ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle."""
    # Startup logic
    sentiment_agg_task = None
    engagement_task = None

    try:
        # 1a. Always ensure learning materials exist
        try:
            _seed_learning_materials()
        except Exception as e:
            print(f"[seed] Learning materials seeding encountered an error: {e}")

        # 1b. Auto-seed demo data (learners, telemetry, etc.)
        try:
            if _should_seed_demo():
                print("[seed] Seeding demo data...")
                _run_seed_script()
                _mark_seeded()
            else:
                print("[seed] Skipping demo seeding (disabled or already seeded).")
        except Exception as e:
            print(f"[seed] Seeding encountered an error: {e}")

        # 2. Load ARL routines
        try:
            from xelra.arl import routines as routines_module
            bundle = routines_module.reload_routine_registry()
            logger.info(
                "ARL routine bundle loaded",
                extra={"routine_version": getattr(bundle, "version", None)},
            )
        except Exception as exc:
            logger.critical(
                "Failed to load ARL routine bundle during startup",
                exc_info=exc,
            )
            raise RuntimeError("Failed to load ARL routine bundle") from exc

        # 3. Start sentiment aggregator
        if (getattr(settings, "feature_sentiment", True) and
            getattr(settings, "infer_sentiment", True)):
            sentiment_agg_task = asyncio.create_task(_sentiment_aggregate_loop())

        # 4. Start engagement reminder loop (daily check)
        engagement_task = asyncio.create_task(_engagement_reminder_loop())

        yield  # Application runs here

    finally:
        # Shutdown logic
        for task in (sentiment_agg_task, engagement_task):
            if task is not None:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

# --- FastAPI app & static files ----------------------------------------------
app = FastAPI(title="X-ELRA API", lifespan=lifespan)

_feature_flags = {
    "explanations": bool(getattr(settings, "explanations", True)),
    "feature_sentiment": bool(getattr(settings, "feature_sentiment", True)),
    "baseline": bool(getattr(settings, "baseline", True)),
    "infer_sentiment": bool(getattr(settings, "infer_sentiment", True)),
    "feature_live_code": bool(getattr(settings, "feature_live_code", False)),
}
app.state.feature_flags = _feature_flags

app.add_middleware(
    RateLimitMiddleware,
    limit=getattr(settings, "rate_limit_requests", 120),
    window_seconds=getattr(settings, "rate_limit_window_seconds", 60.0),
)
app.add_middleware(FeatureFlagMiddleware, flags=_feature_flags)
_cors_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "*")
_cors_origins = [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)


@app.exception_handler(HTTPException)
async def _handle_http_exception(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", None)
    content = {"detail": exc.detail}
    if request_id:
        content["request_id"] = request_id
    return JSONResponse(status_code=exc.status_code, content=content)


@app.exception_handler(Exception)
async def _handle_unexpected_exception(request: Request, exc: Exception):
    request_id = _ensure_request_id(request)
    logger.exception("Unhandled error", exc_info=exc, extra={"request_id": request_id})
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "request_id": request_id},
    )

ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = ROOT / "static"

# Seed marker path (can override with env XELRA_SEEDED_MARK)
SEED_MARK_PATH = Path(
    os.getenv("XELRA_SEEDED_MARK", str(ROOT / "data" / ".seeded.demo"))
)


def _should_seed_demo() -> bool:
    v = os.getenv("XELRA_AUTO_SEED", "1").lower()
    if v in ("0", "false", "no", "off"):
        return False
    if SEED_MARK_PATH.exists():
        return False
    return True


def _mark_seeded():
    try:
        SEED_MARK_PATH.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        SEED_MARK_PATH.write_text(f"seeded@{timestamp}\n")
    except Exception as e:
        print(f"[seed] Could not write seed marker: {e}")


def _seed_learning_materials():
    """Ensure learning materials (skills, items, item-skill mappings) exist.

    Called on every startup. The underlying function is idempotent — it
    only inserts when the items table is empty.
    """
    try:
        if str(ROOT) not in sys.path:
            sys.path.append(str(ROOT))
    except Exception:
        pass

    try:
        mod = importlib.import_module("scripts.seed_demo_data")
        fn = getattr(mod, "seed_learning_materials", None)
        if callable(fn):
            fn()
        else:
            print("[seed] seed_learning_materials not found in seed module — skipping.")
    except Exception as e:
        print(f"[seed] Learning materials seeding failed: {e}")


def _run_seed_script():
    # Ensure project root is importable
    try:
        if str(ROOT) not in sys.path:
            sys.path.append(str(ROOT))
    except Exception:
        pass

    # Try import-first
    try:
        mod = importlib.import_module("scripts.seed_demo_data")
        for name in ("seed", "main", "run", "cli"):
            fn = getattr(mod, name, None)
            if callable(fn):
                fn()
                print("[seed] Demo data seeded via import.")
                return
        # If no callable found, fall back
        print(
            "[seed] No callable entry in scripts.seed_demo_data; falling back to subprocess."
        )
    except Exception as e:
        print(f"[seed] Import seeding failed: {e}")

    # Fallback to subprocess module invocation
    try:
        cmd = [sys.executable, "-m", "scripts.seed_demo_data"]
        subprocess.run(cmd, check=True, cwd=str(ROOT))
        print("[seed] Demo data seeded via subprocess.")
    except Exception as e:
        print(f"[seed] Subprocess seeding failed: {e}")


try:
    from fastapi.staticfiles import StaticFiles

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
        app.mount("/app", StaticFiles(directory=str(STATIC_DIR)), name="app")
except Exception:
    # Static is optional
    pass

from fastapi.responses import RedirectResponse


@app.get("/")
def home():
    candidates = [
        STATIC_DIR / "standalone.html",
        STATIC_DIR / "web" / "standalone.html",
        STATIC_DIR / "index.html",
        STATIC_DIR / "web" / "index.html",
    ]
    for path in candidates:
        if path.exists():
            rel = path.relative_to(STATIC_DIR).as_posix()
            return RedirectResponse(url=f"/app/{rel}")
    return RedirectResponse(url="/docs")


# Note: Startup logic for seeding and ARL policy loading
# has been moved to the lifespan context manager above


# --- Auto-discover and mount routers -----------------------------------------
from importlib import import_module
import pkgutil
from . import routers as routers_pkg


def _include_all_routers():
    for _, module_name, _ in pkgutil.iter_modules(routers_pkg.__path__):
        mod_qual = f"{routers_pkg.__name__}.{module_name}"
        try:
            module = import_module(mod_qual)
        except Exception as e:
            print(f"[router-skip] Failed to import {mod_qual}: {e}")
            continue

        router = getattr(module, "router", None)
        if router is None:
            continue

        prefix = getattr(module, "router_prefix", "/v1")
        try:
            app.include_router(router, prefix=prefix)
            print(f"[router] Mounted {mod_qual} at prefix '{prefix}'")
        except Exception as e:
            print(f"[router-skip] Could not include {mod_qual}: {e}")


_include_all_routers()

# Create any tables defined by routers (e.g., survey models)
Base.metadata.create_all(bind=engine)


async def _sentiment_aggregate_loop(interval_seconds: int = 1800) -> None:
    """Background task that periodically updates sentiment aggregates."""
    while True:
        try:
            session = SessionLocal()
            try:
                update_sentiment_aggregates(session, window_days=7)
            finally:
                session.close()
        except asyncio.CancelledError:
            break
        except Exception as exc:  # pragma: no cover - safety net
            print(f"[sentiment-agg] update failed: {exc}")
        try:
            await asyncio.sleep(interval_seconds)
        except asyncio.CancelledError:
            break


async def _engagement_reminder_loop(interval_seconds: int = 86400) -> None:
    """Background task that checks for inactive learners and sends reminders.

    The interval adapts to the admin-configured check_interval_hours stored
    in the ReminderConfig table.  Falls back to *interval_seconds* if the
    config cannot be read.
    """
    # Wait 60s after startup before first check
    try:
        await asyncio.sleep(60)
    except asyncio.CancelledError:
        return
    while True:
        next_interval = interval_seconds
        try:
            from .routers.engagement import run_engagement_check_once
            interval_hours = await run_engagement_check_once()
            if interval_hours:
                next_interval = interval_hours * 3600
        except asyncio.CancelledError:
            break
        except Exception as exc:
            print(f"[engagement] check failed: {exc}")
        try:
            await asyncio.sleep(next_interval)
        except asyncio.CancelledError:
            break


# Note: Sentiment aggregator startup/shutdown logic
# has been moved to the lifespan context manager above


# --- Mount admin-tools FastAPI sub-app at /admin-tools -----------------------
def _mount_admin_tools():
    """Import and mount the admin-tools FastAPI app as a sub-application."""
    admin_tools_dir = str(ROOT / "admin-tools")
    if admin_tools_dir not in sys.path:
        sys.path.insert(0, admin_tools_dir)

    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "admin_tools_app", str(ROOT / "admin-tools" / "app.py")
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["admin_tools_app"] = mod
    spec.loader.exec_module(mod)
    app.mount("/admin-tools", mod.app)
    print("[admin-tools] Mounted at /admin-tools")


try:
    _mount_admin_tools()
except Exception as e:
    print(f"[admin-tools] Could not mount admin tools: {e}")
