"""Shared dependency factories for the ARL API routers."""

from __future__ import annotations

import logging
from collections.abc import Iterator, Mapping, Sequence
from typing import Optional

from sqlalchemy.orm import Session

from ..config import Settings, settings
from ..utils.db import SessionLocal


class TelemetryService:
    """Best-effort recorder for telemetry payloads emitted by the ARL runtime."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger or logging.getLogger("xelra.telemetry")

    def record(
        self,
        events: Sequence[Mapping[str, object]],
        *,
        learner_id: Optional[str] = None,
        policy_version: Optional[str] = None,
    ) -> None:
        """Persist telemetry events in a non-blocking, logging-friendly manner."""

        if not events:
            return
        for event in events:
            self._logger.info(
                "telemetry.event",
                extra={
                    "learner_id": learner_id,
                    "policy_version": policy_version,
                    "event": event,
                },
            )


def get_telemetry_service() -> TelemetryService:
    """Provide a telemetry service instance for request handlers."""

    return TelemetryService()


def get_persistence_session() -> Iterator[Session]:
    """Yield a SQLAlchemy session tied to the application's primary database."""

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_config_service() -> Settings:
    """Expose the configured :class:`~xelra.config.Settings` instance."""

    return settings


__all__ = [
    "TelemetryService",
    "get_config_service",
    "get_persistence_session",
    "get_telemetry_service",
]

