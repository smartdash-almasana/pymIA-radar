from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ConversationParticipantRead(BaseModel):
    id: int
    conversation_id: int
    public_actor_id: int
    platform_comment_id: str | None
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
