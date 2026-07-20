from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.discovery import DiscoveryCandidate, DiscoveryOutcome
from app.schemas.discovery import DiscoveryOutcomeUpsert, RevealedAffinityLevel
from app.workflow import DiscoveryState, DiscoveryTransitionError, validate_discovery_transition


class DiscoveryPreconditionError(ValueError):
    """Raised when a human discovery operation lacks its required evidence."""


def move_candidate(candidate: DiscoveryCandidate, target: DiscoveryState) -> None:
    candidate.discovery_state = validate_discovery_transition(
        candidate.discovery_state, target
    ).value


def upsert_outcome(
    db: Session,
    candidate: DiscoveryCandidate,
    payload: DiscoveryOutcomeUpsert,
) -> DiscoveryOutcome:
    target = (
        DiscoveryState.AFFINITY_REVEALED
        if payload.revealed_affinity_level
        in {RevealedAffinityLevel.PARTIAL, RevealedAffinityLevel.CLEAR}
        else DiscoveryState.AFFINITY_NOT_CONFIRMED
    )
    current = DiscoveryState(candidate.discovery_state)
    if current == DiscoveryState.DISCOVERY_REPLIED and target == DiscoveryState.AFFINITY_REVEALED:
        move_candidate(candidate, DiscoveryState.DISCOVERY_DIALOGUE_ACTIVE)
    try:
        move_candidate(candidate, target)
    except DiscoveryTransitionError as exc:
        raise DiscoveryPreconditionError(
            "A human discovery outcome requires a recorded reply and valid discovery state"
        ) from exc

    outcome = db.scalar(
        select(DiscoveryOutcome).where(
            DiscoveryOutcome.discovery_candidate_id == candidate.id
        )
    )
    values = payload.model_dump(mode="python")
    if outcome is None:
        outcome = DiscoveryOutcome(discovery_candidate_id=candidate.id, **values)
        db.add(outcome)
    else:
        for name, value in values.items():
            setattr(outcome, name, value)
    return outcome


def require_prequalification_eligibility(
    candidate: DiscoveryCandidate | None,
    outcome: DiscoveryOutcome | None,
) -> None:
    if candidate is None or outcome is None:
        raise DiscoveryPreconditionError(
            "Qualification requires a discovery candidate and human outcome"
        )
    if DiscoveryState(candidate.discovery_state) != DiscoveryState.PREQUALIFICATION_ACCEPTED:
        raise DiscoveryPreconditionError(
            "Qualification requires PREQUALIFICATION_ACCEPTED"
        )
    if outcome.revealed_affinity_level not in {
        RevealedAffinityLevel.PARTIAL.value,
        RevealedAffinityLevel.CLEAR.value,
    }:
        raise DiscoveryPreconditionError(
            "Qualification requires PARTIAL or CLEAR revealed affinity"
        )
    if not outcome.wants_to_continue or not outcome.consent_to_prequalification:
        raise DiscoveryPreconditionError(
            "Qualification requires continuing intent and prequalification consent"
        )
    if outcome.consent_recorded_at is None:
        raise DiscoveryPreconditionError(
            "Qualification requires recorded consent date"
        )
