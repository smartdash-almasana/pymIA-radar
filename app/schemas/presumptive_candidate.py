from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class PresumptiveCandidateStatus(StrEnum):
    DISCOVERED = "DISCOVERED"
    INTERPRETATION_PENDING = "INTERPRETATION_PENDING"
    PRESUMPTIVE_CANDIDATE = "PRESUMPTIVE_CANDIDATE"
    OBSERVED = "OBSERVED"
    DISCARDED = "DISCARDED"
    INTERPRETATION_FAILED = "INTERPRETATION_FAILED"


ACTIVE_PRESUMPTIVE_CANDIDATE_STATUSES = {
    PresumptiveCandidateStatus.DISCOVERED,
    PresumptiveCandidateStatus.INTERPRETATION_PENDING,
    PresumptiveCandidateStatus.PRESUMPTIVE_CANDIDATE,
    PresumptiveCandidateStatus.OBSERVED,
}


class PresumptiveCandidateRead(BaseModel):
    id: int
    public_actor_id: int
    conversation_id: int
    assessment_id: int
    status: PresumptiveCandidateStatus
    apparent_affinity: str
    apparent_intention: str
    false_positive_risk: str
    review_priority: int = Field(ge=0, le=100)
    skill_version: str
    model_name: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
