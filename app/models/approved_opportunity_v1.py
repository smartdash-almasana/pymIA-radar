from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _new_stable_id() -> str:
    return str(uuid4())


class ApprovedOpportunityV1(Base):
    __tablename__ = "approved_opportunities_v1"
    __table_args__ = (
        UniqueConstraint("human_review_id", name="uq_opportunity_human_review"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    stable_id: Mapped[str] = mapped_column(String(36), nullable=False, default=_new_stable_id, index=True)
    schema_version: Mapped[str] = mapped_column(String(50), nullable=False)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("conversation_assessments_v3.id"), nullable=False)
    presumptive_candidate_id: Mapped[int] = mapped_column(ForeignKey("presumptive_candidates.id"), nullable=False)
    public_actor_id: Mapped[int] = mapped_column(ForeignKey("public_actors.id"), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    public_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    apparent_affinity: Mapped[str] = mapped_column(String(30), nullable=False)
    apparent_intention: Mapped[str] = mapped_column(String(40), nullable=False)
    evidence_fragments: Mapped[list] = mapped_column(JSON, default=list)
    review_priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    human_review_id: Mapped[int] = mapped_column(ForeignKey("review_decisions.id"), nullable=False, unique=True)
    human_reviewer_identity: Mapped[str] = mapped_column(String(255), nullable=False)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="READY_FOR_CRM", index=True)
    external_crm_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    export_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_exported_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now, onupdate=_utc_now)