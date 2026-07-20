from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.workflow import DiscoveryState


def _utc_now() -> datetime:
    return datetime.now(UTC)


class DiscoveryCandidate(Base):
    __tablename__ = "discovery_candidates"
    __table_args__ = (
        UniqueConstraint(
            "origin_conversation_id",
            name="uq_discovery_candidate_origin_conversation",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    origin_conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"), nullable=False, index=True
    )
    public_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    public_identity_reference: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
    public_profile_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    authorized_contact: Mapped[str | None] = mapped_column(String(500), nullable=True)
    discovery_state: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        default=DiscoveryState.DISCOVERY_CANDIDATE.value,
    )
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utc_now, onupdate=_utc_now
    )


class DiscoveryOutcome(Base):
    __tablename__ = "discovery_outcomes"
    __table_args__ = (
        UniqueConstraint(
            "discovery_candidate_id",
            name="uq_discovery_outcome_candidate",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    discovery_candidate_id: Mapped[int] = mapped_column(
        ForeignKey("discovery_candidates.id"), nullable=False, index=True
    )
    sympathy_revealed: Mapped[str] = mapped_column(String(20), nullable=False)
    revealed_affinity_level: Mapped[str] = mapped_column(String(20), nullable=False)
    revealed_affinity_domains: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    motivation_declared: Mapped[str | None] = mapped_column(Text, nullable=True)
    questions_or_interests: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    objections: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    wants_to_continue: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    consent_to_prequalification: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    consent_recorded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    human_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    archetype_hypothesis: Mapped[str | None] = mapped_column(String(100), nullable=True)
    archetype_evidence: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    archetype_confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)
    archetype_human_confirmed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    recorded_by: Mapped[str] = mapped_column(String(255), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utc_now, onupdate=_utc_now
    )
