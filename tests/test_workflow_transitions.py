import pytest

from app.workflow import (
    DiscoveryState,
    DiscoveryTransitionError,
    allowed_discovery_transitions,
    validate_discovery_transition,
)


def test_discovery_transition_graph_allows_canonical_progression() -> None:
    progression = [
        DiscoveryState.DISCOVERY_CANDIDATE,
        DiscoveryState.DISCOVERY_APPROACH_APPROVED,
        DiscoveryState.DISCOVERY_CONTACTED,
        DiscoveryState.DISCOVERY_REPLIED,
        DiscoveryState.DISCOVERY_DIALOGUE_ACTIVE,
        DiscoveryState.AFFINITY_REVEALED,
        DiscoveryState.PREQUALIFICATION_INVITED,
        DiscoveryState.PREQUALIFICATION_ACCEPTED,
    ]
    for current, target in zip(progression, progression[1:]):
        assert validate_discovery_transition(current, target) == target


def test_transition_is_idempotent() -> None:
    state = DiscoveryState.DISCOVERY_CONTACTED
    assert validate_discovery_transition(state, state) == state


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (
            DiscoveryState.DISCOVERY_CANDIDATE,
            DiscoveryState.DISCOVERY_REPLIED,
        ),
        (
            DiscoveryState.DISCOVERY_REPLIED,
            DiscoveryState.PREQUALIFICATION_ACCEPTED,
        ),
        (
            DiscoveryState.AFFINITY_NOT_CONFIRMED,
            DiscoveryState.PREQUALIFICATION_INVITED,
        ),
        (
            DiscoveryState.DO_NOT_CONTACT,
            DiscoveryState.DISCOVERY_CONTACTED,
        ),
        (
            DiscoveryState.DISCOVERY_CLOSED,
            DiscoveryState.DISCOVERY_DIALOGUE_ACTIVE,
        ),
    ],
)
def test_invalid_discovery_transitions_are_blocked(
    current: DiscoveryState,
    target: DiscoveryState,
) -> None:
    with pytest.raises(DiscoveryTransitionError):
        validate_discovery_transition(current, target)


def test_terminal_states_have_no_outgoing_transitions() -> None:
    assert not allowed_discovery_transitions(DiscoveryState.DO_NOT_CONTACT)
    assert not allowed_discovery_transitions(DiscoveryState.DISCOVERY_CLOSED)
