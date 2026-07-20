from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.schemas.assessment_v3 import SCHEMA_VERSION_V3


class ConversationAssessmentV3(Base):
    __tablename__ = "conversation_assessments_v3"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"), index=True
    )
    schema_version: Mapped[str] = mapped_column(
        String(100), default=SCHEMA_VERSION_V3
    )
    assessment_status: Mapped[str] = mapped_column(String(60), index=True)
    real_topic: Mapped[str | None] = mapped_column(String(500), nullable=True)
    contextual_meaning: Mapped[str | None] = mapped_column(Text, nullable=True)
    apparent_affinity: Mapped[str | None] = mapped_column(String(30), nullable=True)
    apparent_affinity_domains: Mapped[list] = mapped_column(JSON, default=list)
    apparent_intention: Mapped[str | None] = mapped_column(String(40), nullable=True)
    intention_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_fragments: Mapped[list] = mapped_column(JSON, default=list)
    rejected_evidence_fragments: Mapped[list] = mapped_column(JSON, default=list)
    contradictions: Mapped[list] = mapped_column(JSON, default=list)
    missing_context: Mapped[list] = mapped_column(JSON, default=list)
    false_positive_risk: Mapped[str | None] = mapped_column(String(20), nullable=True)
    uncertainty: Mapped[str | None] = mapped_column(String(20), nullable=True)
    human_review_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_priority: Mapped[int] = mapped_column(Integer, default=0)
    recommended_review_action: Mapped[str] = mapped_column(
        String(30), default="OBSERVE"
    )
    semantic_engine: Mapped[str] = mapped_column(String(100))
    model_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    safe_error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    provisional: Mapped[bool] = mapped_column(Boolean, default=True)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    cascade_schema_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gemma_review_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    gemma_trigger_reasons: Mapped[list] = mapped_column(JSON, default=list)
    gemma_review: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    deterministic_resolution: Mapped[str | None] = mapped_column(String(60), nullable=True)
    resolution_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_provider_attempted: Mapped[str] = mapped_column(String(30), default="agnes")
    primary_provider_used: Mapped[str | None] = mapped_column(String(30), nullable=True)
    provider_failover: Mapped[bool] = mapped_column(Boolean, default=False)
    provider_failure_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    provider_failure_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
