from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


def _utc_now() -> datetime:
    return datetime.now(UTC)


class PublicActor(Base):
    __tablename__ = "public_actors"
    __table_args__ = (
        UniqueConstraint("platform", "platform_actor_id", name="uq_public_actor_platform_actor"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    platform: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    platform_actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    public_username: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    public_profile_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_utc_now, onupdate=_utc_now)

    @property
    def public_actor_key(self) -> str:
        return f"{self.platform}:{self.platform_actor_id}"
