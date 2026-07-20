from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


SCHEMA_VERSION_V3 = "radar-conversation-assessment/v3"


class AssessmentStatusV3(StrEnum):
    COMPLETED = "COMPLETED"
    SEMANTIC_ASSESSMENT_UNAVAILABLE = "SEMANTIC_ASSESSMENT_UNAVAILABLE"
    INVALID_MODEL_OUTPUT = "INVALID_MODEL_OUTPUT"
    INVALID_EVIDENCE = "INVALID_EVIDENCE"


class ApparentAffinity(StrEnum):
    NONE = "NONE"
    POSSIBLE = "POSSIBLE"
    CLEAR = "CLEAR"


class ApparentIntention(StrEnum):
    NONE = "NONE"
    THEMATIC_SYMPATHY = "THEMATIC_SYMPATHY"
    EXPLORATION = "EXPLORATION"
    ACTION_ORIENTED = "ACTION_ORIENTED"


class RiskLevelV3(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ReviewActionV3(StrEnum):
    DISCARD = "DISCARD"
    OBSERVE = "OBSERVE"
    REVIEW = "REVIEW"


class AffinityDomain(StrEnum):
    CONSCIOUS_INVESTMENT = "CONSCIOUS_INVESTMENT"
    LEGACY = "LEGACY"
    COMMUNITY = "COMMUNITY"
    REGENERATION = "REGENERATION"
    TERRITORY = "TERRITORY"
    USEFUL_BEAUTY = "USEFUL_BEAUTY"
    STRATEGIC_PATIENCE = "STRATEGIC_PATIENCE"
    PURPOSEFUL_BUILDING = "PURPOSEFUL_BUILDING"
    BELONGING = "BELONGING"
    LONG_TERM = "LONG_TERM"
    SUSTAINABLE_HOSPITALITY = "SUSTAINABLE_HOSPITALITY"
    NON_SPECULATIVE_DEVELOPMENT = "NON_SPECULATIVE_DEVELOPMENT"
    ACTIVE_PARTICIPATION = "ACTIVE_PARTICIPATION"
    CULTURAL_RESPECT = "CULTURAL_RESPECT"
    MEXICO_YUCATAN_CONNECTION = "MEXICO_YUCATAN_CONNECTION"


class ConversationAssessmentDraftV3(BaseModel):
    """Untrusted semantic interpretation before deterministic RADAR policy."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[SCHEMA_VERSION_V3] = SCHEMA_VERSION_V3
    real_topic: str = Field(min_length=1, max_length=500)
    contextual_meaning: str = Field(min_length=1, max_length=3000)
    apparent_affinity: ApparentAffinity
    apparent_affinity_domains: list[AffinityDomain] = Field(default_factory=list)
    apparent_intention: ApparentIntention
    intention_summary: str = Field(min_length=1, max_length=2000)
    evidence_fragments: list[str] = Field(default_factory=list, max_length=20)
    contradictions: list[str] = Field(default_factory=list, max_length=20)
    missing_context: list[str] = Field(default_factory=list, max_length=20)
    false_positive_risk: RiskLevelV3
    uncertainty: RiskLevelV3
    human_review_reason: str = Field(min_length=1, max_length=2000)


class ConversationAssessmentV3Result(BaseModel):
    """Versioned public contract returned and persisted by RADAR."""

    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int | None = None
    conversation_id: int
    schema_version: Literal[SCHEMA_VERSION_V3] = SCHEMA_VERSION_V3
    assessment_status: AssessmentStatusV3
    real_topic: str | None = Field(default=None, max_length=500)
    contextual_meaning: str | None = Field(default=None, max_length=3000)
    apparent_affinity: ApparentAffinity | None = None
    apparent_affinity_domains: list[AffinityDomain] = Field(default_factory=list)
    apparent_intention: ApparentIntention | None = None
    intention_summary: str | None = Field(default=None, max_length=2000)
    evidence_fragments: list[str] = Field(default_factory=list)
    rejected_evidence_fragments: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    missing_context: list[str] = Field(default_factory=list)
    false_positive_risk: RiskLevelV3 | None = None
    uncertainty: RiskLevelV3 | None = None
    human_review_reason: str | None = Field(default=None, max_length=2000)
    review_priority: int = Field(default=0, ge=0, le=100)
    recommended_review_action: ReviewActionV3 = ReviewActionV3.OBSERVE
    semantic_engine: str = Field(min_length=1, max_length=100)
    model_name: str | None = Field(default=None, max_length=200)
    safe_error_code: str | None = Field(default=None, max_length=100)
    provisional: Literal[True] = True
    human_review_required: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def validate_completed_contract(self) -> "ConversationAssessmentV3Result":
        if self.assessment_status != AssessmentStatusV3.COMPLETED:
            return self

        required = {
            "real_topic": self.real_topic,
            "contextual_meaning": self.contextual_meaning,
            "apparent_affinity": self.apparent_affinity,
            "apparent_intention": self.apparent_intention,
            "intention_summary": self.intention_summary,
            "false_positive_risk": self.false_positive_risk,
            "uncertainty": self.uncertainty,
            "human_review_reason": self.human_review_reason,
        }
        missing = [name for name, value in required.items() if value is None or value == ""]
        if missing:
            raise ValueError("completed assessment is missing: " + ", ".join(missing))
        if not self.evidence_fragments:
            raise ValueError("completed assessment requires literal evidence")
        if (
            self.apparent_affinity in {ApparentAffinity.POSSIBLE, ApparentAffinity.CLEAR}
            and not self.human_review_required
        ):
            raise ValueError("possible or clear affinity requires human review")
        return self
