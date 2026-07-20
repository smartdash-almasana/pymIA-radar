from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PublicActorRead(BaseModel):
    id: int
    platform: str
    platform_actor_id: str
    public_username: str
    display_name: str | None
    public_profile_url: str | None
    created_at: datetime
    updated_at: datetime

    @property
    def public_actor_key(self) -> str:
        return f"{self.platform}:{self.platform_actor_id}"

    model_config = {"from_attributes": True}
