from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

from app.workflow import DiscoveryState


class SympathyRevealed(StrEnum):
    NO = "NO"
    UNCLEAR = "UNCLEAR"
    YES = "YES"


class RevealedAffinityLevel(StrEnum):
    NONE = "NONE"
    PARTIAL = "PARTIAL"
    CLEAR = "CLEAR"


class DiscoveryArchetype(StrEnum):
    PIONEER = "PIONERO_VISIONARIO"
    PATIENT_SOWER = "SEMBRADOR_PACIENTE"
    REGENERATIVE_ARTISAN = "ARTIFICE_REGENERATIVO"


class DiscoveryCandidateCreate(BaseModel):
    origin_conversation_id: int = Field(gt=0)
    public_name: str | None = Field(default=None, max_length=255)
    public_identity_reference: str | None = Field(default=None, max_length=500)
    public_profile_url: str | None = Field(default=None, max_length=2000)
    authorized_contact: str | None = Field(default=None, max_length=500)
    discovery_state: DiscoveryState = DiscoveryState.DISCOVERY_CANDIDATE
    created_by: str = Field(min_length=1, max_length=255)

    @model_validator(mode="after")
    def require_public_reference(self) -> "DiscoveryCandidateCreate":
        if not any(
            value and value.strip()
            for value in (
                self.public_name,
                self.public_identity_reference,
                self.public_profile_url,
            )
        ):
            raise ValueError("at least one public identity reference is required")
        return self


class DiscoveryCandidateRead(BaseModel):
    id: int
    origin_conversation_id: int
    public_name: str | None
    public_identity_reference: str | None
    public_profile_url: str | None
    authorized_contact: str | None
    discovery_state: DiscoveryState
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DiscoveryOutcomeUpsert(BaseModel):
    sympathy_revealed: SympathyRevealed
    revealed_affinity_level: RevealedAffinityLevel
    revealed_affinity_domains: list[str] = Field(default_factory=list)
    motivation_declared: str | None = Field(default=None, max_length=10000)
    questions_or_interests: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    wants_to_continue: bool = False
    consent_to_prequalification: bool = False
    consent_recorded_at: datetime | None = None
    human_notes: str | None = Field(default=None, max_length=10000)
    archetype_hypothesis: DiscoveryArchetype | None = None
    archetype_evidence: list[str] = Field(default_factory=list)
    archetype_confidence: int | None = Field(default=None, ge=0, le=100)
    archetype_human_confirmed: bool = False
    recorded_by: str = Field(min_length=1, max_length=255)

    @model_validator(mode="after")
    def validate_human_outcome(self) -> "DiscoveryOutcomeUpsert":
        if self.consent_to_prequalification:
            if not self.wants_to_continue:
                raise ValueError(
                    "consent_to_prequalification requires wants_to_continue"
                )
            if self.consent_recorded_at is None:
                raise ValueError(
                    "consent_recorded_at is required when consent is true"
                )
            if self.revealed_affinity_level == RevealedAffinityLevel.NONE:
                raise ValueError(
                    "prequalification consent requires PARTIAL or CLEAR affinity"
                )
        elif self.consent_recorded_at is not None:
            raise ValueError(
                "consent_recorded_at must be empty when consent is false"
            )

        if self.archetype_human_confirmed:
            if self.archetype_hypothesis is None:
                raise ValueError(
                    "confirmed archetype requires archetype_hypothesis"
                )
            if not any(item.strip() for item in self.archetype_evidence):
                raise ValueError("confirmed archetype requires evidence")
        if self.archetype_hypothesis is None:
            if self.archetype_confidence is not None or self.archetype_evidence:
                raise ValueError(
                    "archetype evidence and confidence require a hypothesis"
                )
            if self.archetype_human_confirmed:
                raise ValueError("archetype cannot be confirmed without a hypothesis")
        return self


class DiscoveryOutcomeRead(DiscoveryOutcomeUpsert):
    id: int
    discovery_candidate_id: int
    recorded_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
