from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class SemanticAssessmentV2(Base):
    __tablename__ = "semantic_assessments_v2"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    thematic_affinity: Mapped[int] = mapped_column(Integer)
    values_affinity: Mapped[int] = mapped_column(Integer)
    intent_score: Mapped[int] = mapped_column(Integer)
    declared_capacity: Mapped[str] = mapped_column(String(50))
    decision_stage: Mapped[str] = mapped_column(String(100))
    evidence_quality: Mapped[int] = mapped_column(Integer)
    false_positive_risk: Mapped[str] = mapped_column(String(50))
    review_priority: Mapped[int] = mapped_column(Integer)
    probable_archetype: Mapped[str | None] = mapped_column(String(100), nullable=True)
    archetype_confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)
    archetype_evidence: Mapped[list] = mapped_column(JSON, default=list)
    positive_signals: Mapped[list] = mapped_column(JSON, default=list)
    negative_signals: Mapped[list] = mapped_column(JSON, default=list)
    objections: Mapped[list] = mapped_column(JSON, default=list)
    missing_information: Mapped[list] = mapped_column(JSON, default=list)
    evidence_fragments: Mapped[list] = mapped_column(JSON, default=list)
    recommended_action: Mapped[str] = mapped_column(String(100))
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    provisional: Mapped[bool] = mapped_column(Boolean, default=True)
    semantic_engine: Mapped[str] = mapped_column(String(50))
    model_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
