from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


def _utc_now() -> datetime:
    return datetime.now(UTC)


class PresumptiveCandidate(Base):
    __tablename__ = "presumptive_candidates"
    __table_args__ = (
        UniqueConstraint(
            "public_actor_id",
            "conversation_id",
            "assessment_id",
            name="uq_presumptive_candidate_actor_conversation_assessment",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    public_actor_id: Mapped[int] = mapped_column(ForeignKey("public_actors.id"), nullable=False, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("conversation_assessments_v3.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    apparent_affinity: Mapped[str] = mapped_column(String(30), nullable=False)
    apparent_intention: Mapped[str] = mapped_column(String(40), nullable=False)
    false_positive_risk: Mapped[str] = mapped_column(String(20), nullable=False)
    review_priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    skill_version: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now, onupdate=_utc_now)
