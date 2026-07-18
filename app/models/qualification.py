from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class QualificationRecord(Base):
    __tablename__ = "qualification_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"), index=True
    )
    input_payload: Mapped[dict] = mapped_column(JSON)
    traffic_light: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(50), index=True)
    action: Mapped[str] = mapped_column(String(50))
    radar_state: Mapped[str] = mapped_column(String(50), index=True)
    recommended_path: Mapped[str] = mapped_column(String(100))
    path_requires_human_confirmation: Mapped[bool] = mapped_column(Boolean)
    crm_transfer_allowed: Mapped[bool] = mapped_column(Boolean)
    calendar_access_allowed: Mapped[bool] = mapped_column(Boolean)
    reasons: Mapped[list] = mapped_column(JSON)
    missing_information: Mapped[list] = mapped_column(JSON)
    reviewer_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
