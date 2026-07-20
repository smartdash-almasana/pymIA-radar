from __future__ import annotations

from pydantic import BaseModel, Field


class SearchQueryRead(BaseModel):
    id: str
    language: str
    query: str


class OperationalScanRequest(BaseModel):
    query_id: str = Field(pattern=r"^Q\d{3}$")
    sources: list[str] = Field(
        default_factory=lambda: ["reddit", "hackernews", "github", "polymarket"]
    )
    quick: bool = True


class OperationalScanResult(BaseModel):
    query_id: str
    query: str
    total_results: int
    substantive_results: int
    review_results: int
    insufficient_results: int
    admitted_results: int
    new_conversations: int
    existing_conversations: int
    duration_seconds: float = Field(ge=0)
