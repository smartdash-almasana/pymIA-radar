from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.discovery import (
    DiscoveryArchetype,
    DiscoveryCandidateCreate,
    DiscoveryOutcomeUpsert,
    RevealedAffinityLevel,
    SympathyRevealed,
)


def test_candidate_requires_public_identity_reference() -> None:
    with pytest.raises(ValidationError):
        DiscoveryCandidateCreate(
            origin_conversation_id=1,
            created_by="reviewer@example.com",
        )


def test_candidate_accepts_public_name_without_contact() -> None:
    candidate = DiscoveryCandidateCreate(
        origin_conversation_id=1,
        public_name="Persona pública",
        created_by="reviewer@example.com",
    )
    assert candidate.authorized_contact is None


def test_consent_requires_willingness_date_and_affinity() -> None:
    with pytest.raises(ValidationError):
        DiscoveryOutcomeUpsert(
            sympathy_revealed=SympathyRevealed.YES,
            revealed_affinity_level=RevealedAffinityLevel.CLEAR,
            wants_to_continue=False,
            consent_to_prequalification=True,
            consent_recorded_at=datetime.now(UTC),
            recorded_by="reviewer@example.com",
        )

    with pytest.raises(ValidationError):
        DiscoveryOutcomeUpsert(
            sympathy_revealed=SympathyRevealed.YES,
            revealed_affinity_level=RevealedAffinityLevel.PARTIAL,
            wants_to_continue=True,
            consent_to_prequalification=True,
            recorded_by="reviewer@example.com",
        )

    with pytest.raises(ValidationError):
        DiscoveryOutcomeUpsert(
            sympathy_revealed=SympathyRevealed.UNCLEAR,
            revealed_affinity_level=RevealedAffinityLevel.NONE,
            wants_to_continue=True,
            consent_to_prequalification=True,
            consent_recorded_at=datetime.now(UTC),
            recorded_by="reviewer@example.com",
        )


def test_confirmed_archetype_requires_hypothesis_and_evidence() -> None:
    with pytest.raises(ValidationError):
        DiscoveryOutcomeUpsert(
            sympathy_revealed=SympathyRevealed.YES,
            revealed_affinity_level=RevealedAffinityLevel.CLEAR,
            archetype_hypothesis=DiscoveryArchetype.PIONEER,
            archetype_human_confirmed=True,
            recorded_by="reviewer@example.com",
        )


def test_valid_human_outcome_preserves_separate_truths() -> None:
    recorded_at = datetime.now(UTC)
    outcome = DiscoveryOutcomeUpsert(
        sympathy_revealed=SympathyRevealed.YES,
        revealed_affinity_level=RevealedAffinityLevel.PARTIAL,
        revealed_affinity_domains=["COMMUNITY", "REGENERATION"],
        motivation_declared="Quiere conocer el proyecto y su forma de participación.",
        wants_to_continue=True,
        consent_to_prequalification=True,
        consent_recorded_at=recorded_at,
        archetype_hypothesis=DiscoveryArchetype.PATIENT_SOWER,
        archetype_evidence=["Expresó interés por legado y largo plazo."],
        archetype_confidence=70,
        archetype_human_confirmed=True,
        recorded_by="reviewer@example.com",
    )
    assert outcome.consent_to_prequalification is True
    assert outcome.revealed_affinity_level == RevealedAffinityLevel.PARTIAL
    assert outcome.archetype_human_confirmed is True
