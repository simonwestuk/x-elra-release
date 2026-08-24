"""Control Routine DSL loader, validator, and registry helpers."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableSet, Optional, Sequence

import yaml

try:  # pragma: no cover - optional dependency fallback
    from jsonschema import Draft7Validator
except Exception:  # pragma: no cover - fallback when jsonschema missing
    class Draft7Validator:  # type: ignore[override]
        def __init__(self, schema):
            self.schema = schema

        def iter_errors(self, _payload):
            return []

from .schemas import ActionDefinition, RoutineBundle, RoutineDefinition


class DSLValidationError(RuntimeError):
    """Raised when the ARL control routine manifest is invalid."""


@dataclass(frozen=True)
class DSLSource:
    path: Path
    payload: Mapping[str, Any]


ARL_ROUTINES_ENV = "ARL_ROUTINES_PATH"

_DEFAULT_PATH = Path(__file__).resolve().parents[2] / "config" / "arl_routines.yaml"

_CONDITION_ENTRY_SCHEMA: Mapping[str, Any] = {
    "oneOf": [
        {"type": "string", "minLength": 1},
        {"type": "object"},
    ]
}

_ROUTINE_SCHEMA: Mapping[str, Any] = {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["version", "schema_version", "routines"],
    "additionalProperties": False,
    "properties": {
        "version": {"type": "string", "minLength": 1},
        "schema_version": {"type": "string", "minLength": 1},
        "metadata": {"type": "object"},
        "routines": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": [
                    "id",
                    "priority",
                    "conditions",
                    "actions",
                    "explanation",
                ],
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "title": {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "priority": {"type": "integer"},
                    "conditions": {
                        "oneOf": [
                            {
                                "type": "object",
                                "additionalProperties": True,
                                "properties": {
                                    "all": {
                                        "type": "array",
                                        "items": _CONDITION_ENTRY_SCHEMA,
                                    },
                                    "any": {
                                        "type": "array",
                                        "items": _CONDITION_ENTRY_SCHEMA,
                                    },
                                    "none": {
                                        "type": "array",
                                        "items": _CONDITION_ENTRY_SCHEMA,
                                    },
                                    "description": {"type": "string"},
                                },
                            },
                            {
                                "type": "array",
                                "items": _CONDITION_ENTRY_SCHEMA,
                            },
                        ]
                    },
                    "actions": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["name", "type"],
                            "additionalProperties": False,
                            "properties": {
                                "name": {"type": "string", "minLength": 1},
                                "type": {"type": "string", "minLength": 1},
                                "params": {"type": "object"},
                                "enabled": {"type": "boolean"},
                            },
                        },
                    },
                    "explanation": {"type": "string", "minLength": 1},
                    "enabled": {"type": "boolean"},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "seed": {
                        "oneOf": [
                            {"type": "integer"},
                            {"type": "string", "pattern": "^-?\\d+$"},
                            {"type": "null"},
                        ]
                    },
                    "metadata": {"type": "object"},
                    "permitted_modes": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "cooldown_seconds": {"type": "integer", "minimum": 0},
                    "resource_costs": {"type": "object"},
                },
            },
        },
    },
}

_VALIDATOR = Draft7Validator(_ROUTINE_SCHEMA)


def _resolve_routine_path(path: Optional[str | Path]) -> Path:
    if path:
        return Path(path).expanduser().resolve()
    env_path = os.getenv(ARL_ROUTINES_ENV)
    if env_path:
        return Path(env_path).expanduser().resolve()
    return _DEFAULT_PATH


def _ensure_mapping(node: Any, message: str) -> Mapping[str, Any]:
    if not isinstance(node, Mapping):
        raise DSLValidationError(message)
    return node


def _ensure_sequence(node: Any, message: str) -> Sequence[Any]:
    if not isinstance(node, Sequence) or isinstance(node, (str, bytes, bytearray)):
        raise DSLValidationError(message)
    return node


def _load_yaml(path: Path) -> Mapping[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle) or {}
    except FileNotFoundError as exc:
        raise DSLValidationError(f"control routine manifest not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise DSLValidationError(f"failed to parse control routine manifest: {path}") from exc
    return _ensure_mapping(payload, "control routine manifest root must be a mapping")


def _validate_schema(payload: Mapping[str, Any], *, path: Path) -> None:
    errors = sorted(_VALIDATOR.iter_errors(payload), key=lambda error: error.path)
    if errors:
        error = errors[0]
        location = " → ".join(str(part) for part in error.absolute_path)
        prefix = f" ({location})" if location else ""
        raise DSLValidationError(f"control routine manifest validation error{prefix}: {error.message}")


def _normalise_conditions(raw: Any, *, routine_name: str) -> Mapping[str, Any]:
    if raw is None:
        return {"all": tuple()}
    if isinstance(raw, Mapping):
        normalised: dict[str, Any] = {}
        for key, value in raw.items():
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
                normalised[key] = tuple(
                    _normalise_condition_entry(routine_name, idx, entry)
                    for idx, entry in enumerate(value)
                )
            else:
                normalised[key] = value
        return normalised
    if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes, bytearray)):
        return {
            "all": tuple(
                _normalise_condition_entry(routine_name, idx, entry)
                for idx, entry in enumerate(raw)
            )
        }
    raise DSLValidationError(
        f"control routine '{routine_name}' conditions must be a mapping or list of entries"
    )


def _normalise_condition_entry(routine_name: str, index: int, entry: Any) -> Any:
    if isinstance(entry, Mapping):
        return dict(entry)
    if isinstance(entry, str):
        value = entry.strip()
        if not value:
            raise DSLValidationError(
                f"control routine '{routine_name}' condition #{index} must be a non-empty string"
            )
        return value
    raise DSLValidationError(
        f"control routine '{routine_name}' condition #{index} must be a string or mapping"
    )


def _normalise_action(entry: Mapping[str, Any], *, index: int, routine_name: str) -> ActionDefinition:
    name = entry.get("name") or f"action_{index}"
    if not isinstance(name, str) or not name.strip():
        raise DSLValidationError(f"control routine '{routine_name}' action #{index} requires a name")
    action_type = entry.get("type")
    if not isinstance(action_type, str) or not action_type.strip():
        raise DSLValidationError(
            f"control routine '{routine_name}' action '{name}' requires a non-empty type"
        )
    params = entry.get("params", {})
    if not isinstance(params, Mapping):
        raise DSLValidationError(
            f"control routine '{routine_name}' action '{name}' params must be a mapping"
        )
    enabled = entry.get("enabled", True)
    return ActionDefinition(
        name=name.strip(),
        type=action_type.strip(),
        params=dict(params),
        enabled=bool(enabled),
    )


def _normalise_routine(entry: Mapping[str, Any], *, index: int) -> RoutineDefinition:
    routine_id = entry.get("id") or entry.get("name") or f"routine_{index}"
    if not isinstance(routine_id, str) or not routine_id.strip():
        raise DSLValidationError(f"control routine #{index} requires a non-empty id or name")
    title = entry.get("title") or entry.get("description")
    if title is not None and not isinstance(title, str):
        raise DSLValidationError(f"control routine '{routine_id}' title must be a string if provided")
    priority_raw = entry.get("priority")
    try:
        priority = int(priority_raw)
    except (TypeError, ValueError) as exc:
        raise DSLValidationError(f"control routine '{routine_id}' priority must be an integer") from exc
    conditions = _normalise_conditions(entry.get("conditions"), routine_name=routine_id)
    explanation = entry.get("explanation")
    if not isinstance(explanation, str) or not explanation.strip():
        raise DSLValidationError(f"control routine '{routine_id}' requires a non-empty explanation")
    seed_raw = entry.get("seed")
    seed: Optional[int]
    if seed_raw is None:
        seed = None
    else:
        try:
            seed = int(seed_raw)
        except (TypeError, ValueError) as exc:
            raise DSLValidationError(f"control routine '{routine_id}' seed must be coercible to int") from exc
    enabled = bool(entry.get("enabled", True))
    tags_payload = entry.get("tags", [])
    tag_list: list[str] = []
    if tags_payload:
        if not isinstance(tags_payload, Sequence) or isinstance(
            tags_payload, (str, bytes, bytearray)
        ):
            raise DSLValidationError(f"control routine '{routine_id}' tags must be a list of strings")
        for tag in tags_payload:
            if not isinstance(tag, str) or not tag.strip():
                raise DSLValidationError(f"control routine '{routine_id}' tags must be strings")
            tag_list.append(tag.strip())
    metadata_payload = entry.get("metadata", {})
    if metadata_payload and not isinstance(metadata_payload, Mapping):
        raise DSLValidationError(f"control routine '{routine_id}' metadata must be a mapping if provided")
    actions_payload = _ensure_sequence(
        entry.get("actions", []), f"control routine '{routine_id}' actions must be a list"
    )
    actions = [
        _normalise_action(action_entry, index=idx, routine_name=routine_id)
        for idx, action_entry in enumerate(actions_payload)
    ]
    if not actions:
        raise DSLValidationError(f"control routine '{routine_id}' must define at least one action")
    # Parse boundedness constraints (Section 4.3, Table 3)
    permitted_modes_raw = entry.get("permitted_modes", [])
    if not isinstance(permitted_modes_raw, Sequence) or isinstance(permitted_modes_raw, (str, bytes)):
        permitted_modes_raw = []
    permitted_modes = tuple(str(m).strip() for m in permitted_modes_raw if m)

    cooldown_seconds_raw = entry.get("cooldown_seconds")
    cooldown_seconds: Optional[int] = None
    if cooldown_seconds_raw is not None:
        try:
            cooldown_seconds = int(cooldown_seconds_raw)
        except (TypeError, ValueError):
            pass

    resource_costs_raw = entry.get("resource_costs", {})
    if not isinstance(resource_costs_raw, Mapping):
        resource_costs_raw = {}
    resource_costs = {str(k): int(v) for k, v in resource_costs_raw.items() if v is not None}

    return RoutineDefinition(
        name=routine_id.strip(),
        priority=priority,
        conditions=conditions,
        actions=tuple(actions),
        explanation=explanation.strip(),
        seed=seed,
        description=title.strip() if isinstance(title, str) else None,
        enabled=enabled,
        tags=tuple(tag_list),
        metadata=dict(metadata_payload) if isinstance(metadata_payload, Mapping) else {},
        permitted_modes=permitted_modes,
        cooldown_seconds=cooldown_seconds,
        resource_costs=resource_costs,
    )


def _validate_unique_routine_names(routines: Sequence[RoutineDefinition]) -> None:
    seen: MutableSet[str] = set()
    for routine in routines:
        if routine.name in seen:
            raise DSLValidationError(f"duplicate control routine name '{routine.name}' detected")
        seen.add(routine.name)


def _validate_unique_action_names(routines: Sequence[RoutineDefinition]) -> None:
    for routine in routines:
        seen: MutableSet[str] = set()
        for action in routine.actions:
            if action.name in seen:
                raise DSLValidationError(
                    f"duplicate action name '{action.name}' in control routine '{routine.name}'"
                )
            seen.add(action.name)


def load_routine_source(path: Optional[str | Path] = None) -> DSLSource:
    resolved = _resolve_routine_path(path)
    payload = _load_yaml(resolved)
    _validate_schema(payload, path=resolved)
    return DSLSource(path=resolved, payload=payload)


def load_routine_bundle(path: Optional[str | Path] = None) -> RoutineBundle:
    source = load_routine_source(path)
    payload = source.payload
    routines_payload = _ensure_sequence(
        payload.get("routines", []), "control routine manifest must define a routines list"
    )
    routines = [
        _normalise_routine(routine_entry, index=idx)
        for idx, routine_entry in enumerate(routines_payload)
    ]
    _validate_unique_routine_names(routines)
    _validate_unique_action_names(routines)
    metadata = payload.get("metadata", {})
    if metadata and not isinstance(metadata, Mapping):
        raise DSLValidationError("control routine bundle metadata must be a mapping if provided")
    version_raw = payload.get("version", "")
    schema_raw = payload.get("schema_version", "")
    if not isinstance(version_raw, str) or not version_raw.strip():
        raise DSLValidationError("control routine bundle requires a non-empty version string")
    if not isinstance(schema_raw, str) or not schema_raw.strip():
        raise DSLValidationError("control routine bundle requires a non-empty schema_version")
    return RoutineBundle(
        version=version_raw.strip(),
        schema_version=schema_raw.strip(),
        routines=tuple(sorted(routines, key=lambda routine: (-routine.priority, routine.name))),
        metadata=dict(metadata) if isinstance(metadata, Mapping) else {},
    )


__all__ = [
    "ARL_ROUTINES_ENV",
    "DSLSource",
    "DSLValidationError",
    "load_routine_bundle",
    "load_routine_source",
]
