"""Evaluation helpers for control routine condition expressions."""
from __future__ import annotations

import json
import operator
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Mapping, Sequence


class ConditionEvaluationError(RuntimeError):
    """Raised when a condition expression cannot be evaluated."""


_OPERATORS: Mapping[str, Callable[[Any, Any], bool]] = {
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
}


def _parse_literal(raw: str) -> Any:
    text = raw.strip()
    if not text:
        return None
    if text in {"True", "true"}:
        return True
    if text in {"False", "false"}:
        return False
    if text in {"None", "null", "NULL"}:
        return None
    if (text.startswith("\"") and text.endswith("\"")) or (
        text.startswith("'") and text.endswith("'")
    ):
        return text[1:-1]
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (str, bytes, bytearray)):
        return len(value.strip()) == 0 if isinstance(value, str) else len(value) == 0
    if isinstance(value, Mapping):
        return all(_is_empty(item) for item in value.values()) or len(value) == 0
    if isinstance(value, Sequence):
        return all(_is_empty(item) for item in value) or len(value) == 0
    return False


def _is_incomplete(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(_is_empty(v) for v in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return any(_is_incomplete(item) for item in value)
    return False


def _count_recent(entries: Sequence[Any], *, days: int, now: datetime) -> int:
    cutoff = now - timedelta(days=days)
    total = 0
    for entry in entries:
        if isinstance(entry, Mapping):
            value = entry.get("created_at") or entry.get("timestamp")
        else:
            value = getattr(entry, "created_at", None)
        if value is None:
            continue
        if isinstance(value, str):
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                continue
        elif isinstance(value, datetime):
            parsed = value
        else:
            continue
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        else:
            parsed = parsed.astimezone(timezone.utc)
        if parsed >= cutoff:
            total += 1
    return total


def _lowest(value: Any) -> Any:
    if isinstance(value, Mapping):
        return min((float(v) for v in value.values()), default=None)
    if isinstance(value, Sequence):
        return min((float(v) for v in value), default=None)
    return value


def _highest(value: Any) -> Any:
    if isinstance(value, Mapping):
        return max((float(v) for v in value.values()), default=None)
    if isinstance(value, Sequence):
        return max((float(v) for v in value), default=None)
    return value


def _coerce_float(value: Any, default: float) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _active_count(value: Any) -> int:
    """Count goals that appear to be still in progress."""

    if value is None:
        return 0
    if isinstance(value, Mapping):
        candidates = value.values()
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        candidates = value
    else:
        candidates = (value,)

    total = 0
    epsilon = 1e-6
    for entry in candidates:
        if isinstance(entry, Mapping):
            progress = entry.get("progress")
            target = entry.get("target")
            attained_marker = entry.get("attained") or entry.get("attained_at")
            completed_marker = entry.get("completed") or entry.get("completed_at")
            archived_marker = entry.get("archived_at")
        else:
            progress = getattr(entry, "progress", None)
            target = getattr(entry, "target", None)
            attained_marker = getattr(entry, "attained", None) or getattr(
                entry, "attained_at", None
            )
            completed_marker = getattr(entry, "completed", None) or getattr(
                entry, "completed_at", None
            )
            archived_marker = getattr(entry, "archived_at", None)

        if attained_marker or completed_marker or archived_marker:
            continue

        target_value = _coerce_float(target, 1.0)
        if target_value <= 0:
            target_value = 1.0
        progress_value = _coerce_float(progress, 0.0)
        if progress_value + epsilon < target_value:
            total += 1
    return total


_PIPELINE_FUNCS: Mapping[str, Callable[[Any], Any]] = {
    "count": lambda value: len(value) if isinstance(value, Sequence) else (0 if value is None else 1),
    "lowest": _lowest,
    "highest": _highest,
    "active_count": _active_count,
}


def _apply_pipeline(value: Any, stages: Sequence[str], context: Any) -> Any:
    result = value
    now = getattr(getattr(context, "feature_vector", None), "generated_at", None)
    if now is None:
        now = datetime.fromtimestamp(0, tz=timezone.utc)
    for stage in stages:
        if stage in {"last_7_days", "last_14_days", "last_30_days"}:
            days = int(stage.split("_", 1)[1].split("_", 1)[0])
            result = _count_recent(result or [], days=days, now=now) if isinstance(result, Sequence) else 0
            continue
        func = _PIPELINE_FUNCS.get(stage)
        if func is None:
            raise ConditionEvaluationError(f"unknown pipeline stage '{stage}'")
        result = func(result)
    return result


def _resolve_reference(context: Any, expression: str) -> Any:
    target: Any
    path = expression.strip()
    if path.startswith("context."):
        target = context
        path = path[len("context.") :]
    elif path.startswith("feature_vector."):
        target = getattr(context, "feature_vector")
        path = path[len("feature_vector.") :]
    elif path.startswith("bundle."):
        target = getattr(context, "bundle", None)
        path = path[len("bundle.") :]
    else:
        target = context
    if not path:
        return target
    for segment in path.split("."):
        if not segment:
            continue
        if isinstance(target, Mapping):
            target = target.get(segment)
        else:
            target = getattr(target, segment, None)
        if target is None:
            break
    return target


_RE_IS_PATTERN = re.compile(r"\s+is\s+(not\s+)?(empty|None|null|incomplete)", re.IGNORECASE)


def _evaluate_string(condition: str, context: Any) -> bool:
    expr = condition.strip()
    if not expr:
        return True

    if expr.lower().startswith("not "):
        return not _evaluate_string(expr[4:], context)

    if " is empty or incomplete" in expr:
        prefix = expr.split(" is empty or incomplete", 1)[0].strip()
        value = _evaluate_reference(prefix, context)
        return _is_empty(value) or _is_incomplete(value)

    match = _RE_IS_PATTERN.search(expr)
    if match:
        prefix = expr[: match.start()].strip()
        negated = bool(match.group(1))
        predicate = match.group(2).lower()
        value = _evaluate_reference(prefix, context)
        if predicate == "empty":
            result = _is_empty(value)
        elif predicate == "incomplete":
            result = _is_incomplete(value)
        else:  # None/null
            result = value is None
        return not result if negated else result

    contains_match = re.search(r"(.+?)\s+(not\s+)?contains\s+(.+)", expr, re.IGNORECASE)
    if contains_match:
        left_expr = contains_match.group(1).strip()
        negated = bool(contains_match.group(2))
        right_expr = contains_match.group(3).strip()
        left_value = _evaluate_reference(left_expr, context)
        right_value = _evaluate_operand(right_expr, context)
        result = _contains(left_value, right_value)
        return not result if negated else result

    between_match = re.search(r"(.+?)\s+between\s+(.+?)\s+and\s+(.+)", expr, re.IGNORECASE)
    if between_match:
        left_expr = between_match.group(1).strip()
        lower_expr = between_match.group(2).strip()
        upper_expr = between_match.group(3).strip()
        value = _evaluate_reference(left_expr, context)
        lower = _evaluate_operand(lower_expr, context)
        upper = _evaluate_operand(upper_expr, context)
        try:
            return _compare_between(value, lower, upper)
        except TypeError:
            return False

    in_match = re.search(r"(.+?)\s+(not\s+)?in\s+(.+)", expr, re.IGNORECASE)
    if in_match:
        left_expr = in_match.group(1).strip()
        negated = bool(in_match.group(2))
        right_expr = in_match.group(3).strip()
        left_value = _evaluate_operand(left_expr, context)
        right_value = _evaluate_operand(right_expr, context)
        result = _in_sequence(left_value, right_value)
        return not result if negated else result

    for op_symbol, operator_fn in _OPERATORS.items():
        if op_symbol in expr:
            left, right = expr.split(op_symbol, 1)
            left_value = _evaluate_reference(left.strip(), context)
            right_value = _parse_literal(right)
            try:
                return operator_fn(left_value, right_value)
            except TypeError:
                return False

    raise ConditionEvaluationError(f"unsupported condition expression: {condition}")


def _evaluate_reference(expression: str, context: Any) -> Any:
    if "|" in expression:
        ref, *pipeline = [part.strip() for part in expression.split("|") if part.strip()]
        value = _resolve_reference(context, ref)
        return _apply_pipeline(value, pipeline, context)
    return _resolve_reference(context, expression)


def _evaluate_operand(expression: str, context: Any) -> Any:
    expr = expression.strip()
    if not expr:
        return None
    lower = expr.lower()
    if lower.startswith("context.") or lower.startswith("feature_vector.") or lower.startswith("bundle.") or "|" in expr:
        return _evaluate_reference(expr, context)
    if expr.startswith("[") or expr.startswith("{"):
        try:
            return json.loads(expr)
        except json.JSONDecodeError:
            pass
    literal = _parse_literal(expr)
    return literal


def _contains(container: Any, member: Any) -> bool:
    if container is None:
        return False
    if isinstance(container, Mapping):
        return member in container or member in container.values()
    if isinstance(container, (str, bytes)):
        if member is None:
            return False
        return str(member) in container
    if isinstance(container, Sequence) and not isinstance(container, (str, bytes, bytearray)):
        return any(item == member for item in container)
    return False


def _in_sequence(item: Any, container: Any) -> bool:
    if container is None:
        return False
    if isinstance(container, Mapping):
        return item in container or item in container.values()
    if isinstance(container, (str, bytes)):
        if item is None:
            return False
        return str(item) in container
    if isinstance(container, Sequence) and not isinstance(container, (str, bytes, bytearray)):
        return any(member == item for member in container)
    return False


def _compare_between(value: Any, lower: Any, upper: Any) -> bool:
    if value is None or lower is None or upper is None:
        return False
    try:
        value_f = float(value)
        lower_f = float(lower)
        upper_f = float(upper)
    except (TypeError, ValueError):
        try:
            if isinstance(value, datetime):
                value_ts = value
            else:
                value_ts = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            lower_ts = datetime.fromisoformat(str(lower).replace("Z", "+00:00"))
            upper_ts = datetime.fromisoformat(str(upper).replace("Z", "+00:00"))
        except Exception:
            raise TypeError
        return lower_ts <= value_ts <= upper_ts
    return lower_f <= value_f <= upper_f


def evaluate_condition(condition: Any, context: Any) -> bool:
    """Evaluate a single condition entry against ``context``."""

    if condition is None:
        return True
    if isinstance(condition, str):
        return _evaluate_string(condition, context)
    if isinstance(condition, Mapping):
        nested_all = condition.get("all")
        nested_any = condition.get("any")
        nested_none = condition.get("none")
        if nested_all is not None:
            return all(evaluate_condition(entry, context) for entry in nested_all)
        if nested_any is not None:
            return any(evaluate_condition(entry, context) for entry in nested_any)
        if nested_none is not None:
            return not any(evaluate_condition(entry, context) for entry in nested_none)
        raise ConditionEvaluationError("condition mapping must define all/any/none")
    if isinstance(condition, Sequence):
        return all(evaluate_condition(entry, context) for entry in condition)
    return bool(condition)


def evaluate_routine_conditions(routine_conditions: Mapping[str, Any], context: Any) -> bool:
    """Evaluate the composite condition mapping from a control routine definition."""

    if not routine_conditions:
        return True
    all_entries = routine_conditions.get("all")
    any_entries = routine_conditions.get("any")
    none_entries = routine_conditions.get("none")

    if all_entries is not None and not all(
        evaluate_condition(entry, context) for entry in all_entries
    ):
        return False
    if any_entries is not None and not any(
        evaluate_condition(entry, context) for entry in any_entries
    ):
        return False
    if none_entries is not None and any(
        evaluate_condition(entry, context) for entry in none_entries
    ):
        return False
    return True


__all__ = ["evaluate_routine_conditions", "ConditionEvaluationError"]
