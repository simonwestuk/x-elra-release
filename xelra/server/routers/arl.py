"""Public learner-facing ARL router."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from fastapi import APIRouter, Depends, Header, HTTPException, status
from jwt import InvalidTokenError
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ...utils.auth import verify_login_token
from ...utils.db import GroupAssignment, deterministic_arm, set_arm
from ...arl.dependencies import (
    TelemetryService,
    get_config_service,
    get_persistence_session,
    get_telemetry_service,
)
from ...arl.engine import run_arl_cycle
from ...arl.schemas import (
    ARLCycleResult,
    ActionResult,
    EvaluationJob,
    FeatureVector,
    RoutineResult,
)


router = APIRouter()


class ARLRequest(BaseModel):
    learner_id: str | None = None
    routine_path: str | None = None
    refresh_features: bool = False
    override_arm: str | None = None
    verify_assignment: bool = False


class ARLEventRequest(BaseModel):
    learner_id: str | None = None
    event_type: str
    routine_path: str | None = None
    refresh_features: bool | None = None
    metadata: Mapping[str, Any] | None = None


class ReplayCheck(BaseModel):
    learner_id: str
    expected_arm: str
    stored_arm: str | None = None
    status: str


class ARLCycleResponse(BaseModel):
    """
    Serialised representation of :class:`~xelra.arl.schemas.ARLCycleResult`.

    Includes decision trace fields per ARL formal specification Section 4.4.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            FeatureVector: lambda value: value.to_dict(),
            RoutineResult: lambda value: value.to_dict(),
            ActionResult: lambda value: value.to_dict(),
            EvaluationJob: lambda value: value.to_dict() if value else None,
            ARLCycleResult: lambda value: value.to_dict(),
        },
    )

    learner_id: str
    decision_id: str
    deterministic_hash: str
    routine_version: str
    seed: int | None = None
    feature_vector: FeatureVector
    routine_results: Sequence[RoutineResult]
    explanations: Sequence[Mapping[str, Any]]
    telemetry_events: Sequence[Mapping[str, Any]]
    evaluation_job: EvaluationJob | None = None
    active_routines: Sequence[str] = ()
    replay: ReplayCheck | None = None

    # NEW: Decision trace fields per Section 4.4
    controller_state_before: Mapping[str, Any] | None = None
    controller_state_after: Mapping[str, Any] | None = None
    context_summary: Mapping[str, Any] | None = None
    inputs_used: Mapping[str, Any] | None = None
    decision: Mapping[str, Any] | None = None  # Appendix A.3: {action, source_routine}
    next_transition_conditions: Sequence[Mapping[str, Any]] | None = None
    learner_facing_fields: Mapping[str, Any] | None = None

    # Compact decision trace aligned with the minimal DecisionTrace T_t schema
    decision_trace: Mapping[str, Any] | None = None

    @classmethod
    def from_result(
        cls,
        result: ARLCycleResult,
        replay: ReplayCheck | None = None,
    ) -> "ARLCycleResponse":
        # Extract controller states if present
        state_before = None
        state_after = None
        if result.controller_state_before is not None:
            state_before = result.controller_state_before.to_dict()
        if result.controller_state_after is not None:
            state_after = result.controller_state_after.to_dict()

        return cls(
            learner_id=result.learner_id,
            decision_id=result.decision_id,
            deterministic_hash=result.deterministic_hash,
            routine_version=result.routine_version,
            seed=result.seed,
            feature_vector=result.feature_vector,
            routine_results=result.routine_results,
            explanations=result.explanations,
            telemetry_events=result.telemetry_events,
            evaluation_job=result.evaluation_job,
            active_routines=result.active_routines,
            replay=replay,
            # NEW: Decision trace fields
            controller_state_before=state_before,
            controller_state_after=state_after,
            context_summary=result.context_summary,
            inputs_used=result.inputs_used,
            decision=result.decision,
            next_transition_conditions=result.next_transition_conditions,
            learner_facing_fields=result.learner_facing_fields,
            # Compact decision trace (minimal schema)
            decision_trace=result.decision_trace,
        )


def _require_token_payload(authorization: str | None = Header(default=None)) -> Mapping[str, Any]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    try:
        return verify_login_token(token)
    except InvalidTokenError as exc:  # pragma: no cover - defensive
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def _resolve_learner_id(requested: str | None, token_payload: Mapping[str, Any]) -> str:
    token_sub = token_payload.get("sub")
    learner_id = requested or token_sub
    if not learner_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="learner_id missing")
    learner_id = str(learner_id)
    if requested and token_sub and str(requested) != str(token_sub):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="learner mismatch")
    return learner_id


def _execute_cycle(
    request: ARLRequest,
    *,
    token_payload: Mapping[str, Any],
    session: Session,
    telemetry: TelemetryService,
    config,
    trigger: str | None = None,
    trigger_metadata: Mapping[str, Any] | None = None,
) -> ARLCycleResponse:
    learner_id = _resolve_learner_id(request.learner_id, token_payload)

    replay_status: ReplayCheck | None = None
    if request.override_arm:
        set_arm(session, learner_id, request.override_arm)
        replay_status = ReplayCheck(
            learner_id=learner_id,
            expected_arm=request.override_arm,
            stored_arm=request.override_arm,
            status="overridden",
        )
    elif request.verify_assignment:
        assignment = (
            session.query(GroupAssignment)
            .filter(GroupAssignment.learner_id == learner_id)
            .one_or_none()
        )
        stored_arm = assignment.arm if assignment else None
        expected_arm = deterministic_arm(learner_id)
        status_value = "match" if stored_arm == expected_arm else "mismatch"
        if stored_arm is None:
            status_value = "not_assigned"
        replay_status = ReplayCheck(
            learner_id=learner_id,
            expected_arm=expected_arm,
            stored_arm=stored_arm,
            status=status_value,
        )

    result = run_arl_cycle(
        learner_id,
        session=session,
        routine_path=request.routine_path,
        refresh_features=request.refresh_features,
    )

    telemetry_events = list(result.telemetry_events)
    if trigger:
        telemetry_events.append(
            {
                "type": "trigger",
                "trigger": trigger,
                "metadata": dict(trigger_metadata or {}),
            }
        )
        result.telemetry_events = telemetry_events

    telemetry.record(
        telemetry_events,
        learner_id=learner_id,
        policy_version=config.routine_version,
    )

    return ARLCycleResponse.from_result(result, replay=replay_status)


@router.post("/arl", response_model=ARLCycleResponse)
def run_cycle(
    request: ARLRequest,
    token_payload: Mapping[str, Any] = Depends(_require_token_payload),
    session: Session = Depends(get_persistence_session),
    telemetry: TelemetryService = Depends(get_telemetry_service),
    config=Depends(get_config_service),
) -> ARLCycleResponse:
    """Run an ARL decision cycle for the authenticated learner.

    Parameters
    ----------
    request:
        Body payload describing the routine bundle, learner identifier, and
        feature refresh behaviour for this cycle.
    token_payload:
        Result of :func:`_require_token_payload`, derived from the
        ``Authorization: Bearer`` header and used to resolve the learner ID.
    session:
        Database session used to fetch or persist group assignments that may
        influence replay checks.
    telemetry:
        Service dependency that receives telemetry events emitted during the
        ARL execution.
    config:
        Configuration object whose ``routine_version`` is echoed in emitted
        telemetry.

    Returns
    -------
    ARLCycleResponse
        Serialised representation of :class:`ARLCycleResponse`, containing
        routine outputs, telemetry events, and optional replay status.

    Raises
    ------
    HTTPException
        ``401`` if the ``Authorization`` header is missing or invalid, ``400``
        if the request does not resolve to a learner, or ``403`` when the
        caller attempts to impersonate another learner.
    """
    return _execute_cycle(
        request,
        token_payload=token_payload,
        session=session,
        telemetry=telemetry,
        config=config,
    )


def _event_to_request(event: ARLEventRequest) -> ARLRequest:
    refresh = event.refresh_features
    if refresh is None:
        refresh = event.event_type.lower() in {"error", "baseline", "time"}
    return ARLRequest(
        learner_id=event.learner_id,
        routine_path=event.routine_path,
        refresh_features=refresh,
    )


@router.post("/arl/event", response_model=ARLCycleResponse)
def dispatch_event(
    event: ARLEventRequest,
    token_payload: Mapping[str, Any] = Depends(_require_token_payload),
    session: Session = Depends(get_persistence_session),
    telemetry: TelemetryService = Depends(get_telemetry_service),
    config=Depends(get_config_service),
) -> ARLCycleResponse:
    """Execute an ARL cycle in response to an external learner event.

    Parameters
    ----------
    event:
        Event payload describing the learner, originating event type, routine
        bundle, and optional metadata captured with the cycle.
    token_payload:
        Verified token payload sourced from the ``Authorization: Bearer``
        header, ensuring that the caller controls the referenced learner.
    session:
        Persistence session used to manage replay checks and group
        assignments.
    telemetry:
        Service dependency that records telemetry emitted by
        :func:`run_arl_cycle` along with the event metadata.
    config:
        Active configuration used to annotate telemetry with the routine
        version.

    Returns
    -------
    ARLCycleResponse
        See :class:`ARLCycleResponse`; additionally includes a ``trigger``
        telemetry event summarising the supplied learner event.

    Raises
    ------
    HTTPException
        Propagated from :func:`_require_token_payload` when the caller is not
        authenticated (``401``) and from :func:`_resolve_learner_id` when the
        learner cannot be determined (``400``) or does not match the token
        subject (``403``).
    """
    request = _event_to_request(event)
    return _execute_cycle(
        request,
        token_payload=token_payload,
        session=session,
        telemetry=telemetry,
        config=config,
        trigger=event.event_type,
        trigger_metadata=event.metadata or {},
    )


@router.post("/arl/trigger", response_model=ARLCycleResponse)
def trigger_cycle(
    request: ARLRequest,
    token_payload: Mapping[str, Any] = Depends(_require_token_payload),
    session: Session = Depends(get_persistence_session),
    telemetry: TelemetryService = Depends(get_telemetry_service),
    config=Depends(get_config_service),
) -> ARLCycleResponse:
    """Manually trigger an ARL cycle without recording an external event.

    Parameters
    ----------
    request:
        Same payload accepted by :func:`run_cycle`, allowing the caller to
        override the learner's stored arm or refresh features.
    token_payload:
        Authentication context derived from the ``Authorization: Bearer``
        header.
    session:
        Persistence session that tracks group assignments.
    telemetry:
        Telemetry service invoked with the ARL cycle's emitted events.
    config:
        Configuration dependency whose ``routine_version`` is used in telemetry
        records.

    Returns
    -------
    ARLCycleResponse
        See :class:`ARLCycleResponse` for the response schema containing routine
        results, telemetry events, and optional replay information.

    Raises
    ------
    HTTPException
        Mirrors the authentication and learner validation errors raised by
        :func:`run_cycle`.
    """
    return _execute_cycle(
        request,
        token_payload=token_payload,
        session=session,
        telemetry=telemetry,
        config=config,
    )


class ArmOverrideRequest(BaseModel):
    learner_id: str | None = None
    arm: str


class ArmOverrideResponse(BaseModel):
    learner_id: str
    arm: str
    status: str


@router.post("/arl/override", response_model=ArmOverrideResponse)
def override_arm_assignment(
    request: ArmOverrideRequest,
    token_payload: Mapping[str, Any] = Depends(_require_token_payload),
    session: Session = Depends(get_persistence_session),
) -> ArmOverrideResponse:
    """Override the stored experimental arm for the authenticated learner.

    Parameters
    ----------
    request:
        Payload identifying the learner and target arm to persist.
    token_payload:
        Authentication context produced by :func:`_require_token_payload`,
        ensuring that the caller can only override their own assignment unless
        they specify a matching learner identifier.
    session:
        Database session used to persist the override assignment.

    Returns
    -------
    ArmOverrideResponse
        Confirmation that the requested arm override was stored, including the
        resolved learner identifier.

    Raises
    ------
    HTTPException
        ``401`` when authentication fails, ``403`` when the learner identifier
        conflicts with the authenticated subject, or ``400`` if the ``arm``
        field is blank.
    """
    learner_id = _resolve_learner_id(request.learner_id, token_payload)
    arm = request.arm.strip().upper()
    if not arm:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="arm missing")
    set_arm(session, learner_id, arm)
    return ArmOverrideResponse(learner_id=learner_id, arm=arm, status="overridden")


__all__ = ["router"]
