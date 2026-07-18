from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

class ConversationCreate(BaseModel):
    source: str
    external_id: str
    conversation_url: HttpUrl
    author_name: str | None = None
    title: str | None = None
    text: str
    context: str | None = None
    published_at: datetime | None = None
    query_origin: str | None = None
    engagement: dict = Field(default_factory=dict)

class ConversationRead(ConversationCreate):
    id: int
    status: str

    model_config = {"from_attributes": True}
