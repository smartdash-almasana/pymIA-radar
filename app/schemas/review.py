from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class ReviewDecisionType(StrEnum):
    APPROVE_APPROACH = "APPROVE_APPROACH"
    KEEP_OBSERVING = "KEEP_OBSERVING"
    DISCARD = "DISCARD"
    DO_NOT_CONTACT = "DO_NOT_CONTACT"


class ReviewCreate(BaseModel):
    decision: ReviewDecisionType
    edited_response: str | None = Field(default=None, max_length=5000)
    reviewer_notes: str | None = Field(default=None, max_length=5000)

    @model_validator(mode="after")
    def require_message_for_approval(self) -> "ReviewCreate":
        if self.decision == ReviewDecisionType.APPROVE_APPROACH and not self.edited_response:
            raise ValueError("edited_response is required when approving an approach")
        return self


class ReviewRead(BaseModel):
    id: int
    conversation_id: int
    decision: str
    edited_response: str | None
    reviewer_notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class EngagementEventType(StrEnum):
    CONTACTED = "CONTACTED"
    REPLIED = "REPLIED"
    NO_RESPONSE = "NO_RESPONSE"
    DO_NOT_CONTACT = "DO_NOT_CONTACT"


class EngagementCreate(BaseModel):
    event_type: EngagementEventType
    channel: str | None = Field(default=None, max_length=100)
    message_text: str | None = Field(default=None, max_length=10000)
    response_text: str | None = Field(default=None, max_length=10000)
    notes: str | None = Field(default=None, max_length=5000)
    occurred_at: datetime

    @model_validator(mode="after")
    def validate_event_payload(self) -> "EngagementCreate":
        if self.event_type == EngagementEventType.CONTACTED:
            if not self.channel or not self.message_text:
                raise ValueError("CONTACTED requires channel and message_text")
        if self.event_type == EngagementEventType.REPLIED and not self.response_text:
            raise ValueError("REPLIED requires response_text")
        return self


class EngagementRead(BaseModel):
    id: int
    conversation_id: int
    event_type: str
    channel: str | None
    message_text: str | None
    response_text: str | None
    notes: str | None
    occurred_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
