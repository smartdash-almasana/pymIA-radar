from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


SCHEMA_VERSION_APPROVED_OPPORTUNITY_V1 = "radar-approved-opportunity/v1"


class OpportunityStatus(StrEnum):
    READY_FOR_CRM = "READY_FOR_CRM"
    EXPORTED = "EXPORTED"
    TRANSFER_CONFIRMED = "TRANSFER_CONFIRMED"
    TRANSFER_FAILED = "TRANSFER_FAILED"


class ApprovedOpportunityRead(BaseModel):
    id: int
    stable_id: str
    schema_version: str
    conversation_id: int
    assessment_id: int
    presumptive_candidate_id: int
    public_actor_id: int
    source: str
    source_url: str
    public_username: str | None
    apparent_affinity: str
    apparent_intention: str
    evidence_fragments: list[str]
    review_priority: int = Field(ge=0, le=100)
    human_review_id: int
    human_reviewer_identity: str
    approved_at: datetime
    status: OpportunityStatus
    external_crm_id: str | None
    export_count: int = Field(ge=0)
    last_exported_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}