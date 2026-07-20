from __future__ import annotations

from enum import StrEnum


class DiscoveryState(StrEnum):
    DISCOVERY_CANDIDATE = "DISCOVERY_CANDIDATE"
    DISCOVERY_APPROACH_APPROVED = "DISCOVERY_APPROACH_APPROVED"
    DISCOVERY_CONTACTED = "DISCOVERY_CONTACTED"
    DISCOVERY_REPLIED = "DISCOVERY_REPLIED"
    DISCOVERY_DIALOGUE_ACTIVE = "DISCOVERY_DIALOGUE_ACTIVE"
    AFFINITY_REVEALED = "AFFINITY_REVEALED"
    AFFINITY_NOT_CONFIRMED = "AFFINITY_NOT_CONFIRMED"
    DISCOVERY_CLOSED = "DISCOVERY_CLOSED"
    PREQUALIFICATION_INVITED = "PREQUALIFICATION_INVITED"
    PREQUALIFICATION_ACCEPTED = "PREQUALIFICATION_ACCEPTED"
    DO_NOT_CONTACT = "DO_NOT_CONTACT"


class DiscoveryTransitionError(ValueError):
    """Raised when a discovery state transition is not permitted."""


_ALLOWED_DISCOVERY_TRANSITIONS: dict[DiscoveryState, frozenset[DiscoveryState]] = {
    DiscoveryState.DISCOVERY_CANDIDATE: frozenset(
        {
            DiscoveryState.DISCOVERY_APPROACH_APPROVED,
            DiscoveryState.DO_NOT_CONTACT,
        }
    ),
    DiscoveryState.DISCOVERY_APPROACH_APPROVED: frozenset(
        {
            DiscoveryState.DISCOVERY_CONTACTED,
            DiscoveryState.DO_NOT_CONTACT,
        }
    ),
    DiscoveryState.DISCOVERY_CONTACTED: frozenset(
        {
            DiscoveryState.DISCOVERY_REPLIED,
            DiscoveryState.DO_NOT_CONTACT,
        }
    ),
    DiscoveryState.DISCOVERY_REPLIED: frozenset(
        {
            DiscoveryState.DISCOVERY_DIALOGUE_ACTIVE,
            DiscoveryState.AFFINITY_NOT_CONFIRMED,
            DiscoveryState.DO_NOT_CONTACT,
        }
    ),
    DiscoveryState.DISCOVERY_DIALOGUE_ACTIVE: frozenset(
        {
            DiscoveryState.AFFINITY_REVEALED,
            DiscoveryState.AFFINITY_NOT_CONFIRMED,
            DiscoveryState.DO_NOT_CONTACT,
        }
    ),
    DiscoveryState.AFFINITY_REVEALED: frozenset(
        {
            DiscoveryState.PREQUALIFICATION_INVITED,
            DiscoveryState.DISCOVERY_CLOSED,
            DiscoveryState.DO_NOT_CONTACT,
        }
    ),
    DiscoveryState.AFFINITY_NOT_CONFIRMED: frozenset(
        {DiscoveryState.DISCOVERY_CLOSED, DiscoveryState.DO_NOT_CONTACT}
    ),
    DiscoveryState.PREQUALIFICATION_INVITED: frozenset(
        {
            DiscoveryState.PREQUALIFICATION_ACCEPTED,
            DiscoveryState.DISCOVERY_CLOSED,
            DiscoveryState.DO_NOT_CONTACT,
        }
    ),
    DiscoveryState.PREQUALIFICATION_ACCEPTED: frozenset(
        {DiscoveryState.DISCOVERY_CLOSED, DiscoveryState.DO_NOT_CONTACT}
    ),
    DiscoveryState.DISCOVERY_CLOSED: frozenset(),
    DiscoveryState.DO_NOT_CONTACT: frozenset(),
}


def validate_discovery_transition(
    current: DiscoveryState | str,
    target: DiscoveryState | str,
) -> DiscoveryState:
    """Return the canonical target state when a transition is valid.

    Re-applying the current state is idempotent. Evidence-dependent preconditions
    are enforced by the domain service that requests the transition; this module
    owns only the canonical transition graph.
    """
    current_state = DiscoveryState(current)
    target_state = DiscoveryState(target)
    if current_state == target_state:
        return target_state
    if target_state not in _ALLOWED_DISCOVERY_TRANSITIONS[current_state]:
        raise DiscoveryTransitionError(
            f"invalid discovery transition: {current_state.value} -> {target_state.value}"
        )
    return target_state


def allowed_discovery_transitions(
    current: DiscoveryState | str,
) -> frozenset[DiscoveryState]:
    return _ALLOWED_DISCOVERY_TRANSITIONS[DiscoveryState(current)]
