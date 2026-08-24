"""Control routine evaluation pipeline."""
from __future__ import annotations

import hashlib
import logging
import os
import threading
from pathlib import Path
from typing import Iterable, List, Optional

from .actions import execute_action
from .conditions import evaluate_routine_conditions
from .dsl import ARL_ROUTINES_ENV, load_routine_bundle
from .schemas import ExecutionContext, RoutineBundle, RoutineResult

logger = logging.getLogger(__name__)


def _stable_seed(*parts: object) -> int:
    material = "::".join(str(part) for part in parts)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def _metric_increment(metrics: object, name: str, *, amount: int = 1, **tags: object) -> None:
    if metrics is None:
        return
    if hasattr(metrics, "increment"):
        try:
            metrics.increment(name, amount=amount, tags=tags or None)
            return
        except TypeError:
            metrics.increment(name, amount=amount)
            return
    if hasattr(metrics, "inc"):
        try:
            metrics.inc(name, amount)
        except TypeError:
            metrics.inc(name)


def evaluate_routines(
    bundle: RoutineBundle,
    context: ExecutionContext,
    *,
    base_seed: Optional[int] = None,
) -> List[RoutineResult]:
    """Evaluate all enabled control routines in ``bundle`` deterministically."""

    results: List[RoutineResult] = []
    ordered_routines: Iterable = bundle.routines
    for index, routine in enumerate(ordered_routines):
        if not routine.enabled:
            logger.info(
                "routine skipped (disabled)", extra={"routine": routine.name, "learner_id": context.learner_id}
            )
            results.append(
                RoutineResult(
                    routine=routine,
                    seed=None,
                    actions=[],
                    skipped=True,
                    error=None,
                    skip_reason="disabled",
                )
            )
            continue
        if not evaluate_routine_conditions(routine.conditions, context):
            logger.info(
                "routine skipped (conditions)",
                extra={"routine": routine.name, "learner_id": context.learner_id},
            )
            results.append(
                RoutineResult(
                    routine=routine,
                    seed=None,
                    actions=[],
                    skipped=True,
                    error=None,
                    skip_reason="conditions_not_met",
                )
            )
            continue
        routine_seed_material = routine.seed if routine.seed is not None else base_seed
        routine_seed = _stable_seed(
            context.learner_id,
            bundle.version,
            routine.name,
            routine_seed_material or 0,
            index,
        )
        result = RoutineResult(routine=routine, seed=routine_seed)
        _metric_increment(context.metrics, "arl.routine.start", routine=routine.name)
        for action_index, action in enumerate(routine.actions):
            action_seed = _stable_seed(routine_seed, action.name, action_index)
            action_result = execute_action(routine.name, action, context, action_seed)
            result.actions.append(action_result)
            context.shared[f"{routine.name}.{action.name}"] = action_result.payload
            context.shared[action.name] = action_result.payload
            if action.type == "fetch_recommendations" and not action_result.error:
                context.shared["last_recommendations"] = action_result.payload
            if action_result.error:
                logger.warning(
                    "routine action reported error",
                    extra={
                        "routine": routine.name,
                        "action": action.name,
                        "error": action_result.error,
                        "learner_id": context.learner_id,
                    },
                )
                result.error = action_result.error
            _metric_increment(
                context.metrics,
                "arl.action.executed",
                routine=routine.name,
                action=action.name,
                status="error" if action_result.error else "ok",
            )
        results.append(result)
        _metric_increment(context.metrics, "arl.routine.completed", routine=routine.name)
    return results


_routine_registry_lock = threading.Lock()
_routine_registry: RoutineBundle | None = None
_routine_registry_path: Path | None = None
_DEFAULT_ROUTINE_PATH = Path(__file__).resolve().parents[2] / "config" / "arl_routines.yaml"


def _resolve_registry_path(path: Optional[str | Path]) -> Path:
    if path is not None:
        return Path(path).expanduser().resolve()
    env_path = os.getenv(ARL_ROUTINES_ENV)
    if env_path:
        return Path(env_path).expanduser().resolve()
    return _DEFAULT_ROUTINE_PATH


def get_routine_bundle(path: Optional[str | Path] = None) -> RoutineBundle:
    """Return the active control routine bundle, loading it from disk if needed."""

    if path is not None:
        return load_routine_bundle(path)
    with _routine_registry_lock:
        global _routine_registry, _routine_registry_path
        if _routine_registry is None:
            _routine_registry = load_routine_bundle()
            _routine_registry_path = _resolve_registry_path(None)
        return _routine_registry


def reload_routine_registry(path: Optional[str | Path] = None) -> RoutineBundle:
    """Reload the control routine bundle from disk and swap the in-memory registry."""

    bundle = load_routine_bundle(path)
    resolved = _resolve_registry_path(path)
    with _routine_registry_lock:
        global _routine_registry, _routine_registry_path
        _routine_registry = bundle
        _routine_registry_path = resolved
    return bundle


def get_routine_registry_path() -> Path | None:
    """Return the resolved path backing the in-memory control routine registry."""

    with _routine_registry_lock:
        return _routine_registry_path


__all__ = [
    "evaluate_routines",
    "get_routine_bundle",
    "get_routine_registry_path",
    "reload_routine_registry",
]
