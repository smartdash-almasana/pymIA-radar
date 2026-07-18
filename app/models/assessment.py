from datetime import UTC, datetime
from sqlalchemy import ForeignKey, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class SemanticAssessment(Base):
    __tablename__ = "semantic_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    relevant: Mapped[bool] = mapped_column(Boolean, default=False)
    affinity_score: Mapped[int] = mapped_column(Integer, default=0)
    investment_intent: Mapped[int] = mapped_column(Integer, default=0)
    probable_archetype: Mapped[str | None] = mapped_column(String(100), nullable=True)
    conversation_stage: Mapped[str | None] = mapped_column(String(100), nullable=True)
    recommended_action: Mapped[str | None] = mapped_column(String(100), nullable=True)
    evidence: Mapped[list] = mapped_column(JSON, default=list)
    missing_data: Mapped[list] = mapped_column(JSON, default=list)
    risk_flags: Mapped[list] = mapped_column(JSON, default=list)
    reasoning_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
