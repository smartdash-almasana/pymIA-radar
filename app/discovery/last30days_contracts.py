from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from app.discovery.contracts import DiscoveryResult


SUPPORTED_SCHEMA_VERSION = "1.2"


class Last30DaysCluster(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    summary: str = ""
    sources: list[str] = Field(default_factory=list)
    engagement_total: float | int = 0


class Last30DaysResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    candidate_id: str
    title: str | None = None
    source: str
    url: HttpUrl
    published_at: datetime | None = None
    summary: str
    engagement: dict[str, Any] = Field(default_factory=dict)
    relevance_score: float | None = None
    cluster: int | None = None

    @field_validator("candidate_id", "source", "summary")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("must not be empty")
        return normalized


class Last30DaysAgentExport(BaseModel):
    model_config = ConfigDict(extra="ignore")

    schema_version: str
    query: str
    generated_at: datetime
    window_days: int
    source_status: dict[str, str] = Field(default_factory=dict)
    freshness_verdicts: list[dict[str, Any]] = Field(default_factory=list)
    clusters: list[Last30DaysCluster] = Field(default_factory=list)
    results: list[Last30DaysResult] = Field(default_factory=list)

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        if value != SUPPORTED_SCHEMA_VERSION:
            raise ValueError(
                f"unsupported schema_version {value!r}; expected {SUPPORTED_SCHEMA_VERSION!r}"
            )
        return value

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("query must not be empty")
        return normalized


class Last30DaysExecutionTrace(BaseModel):
    command: list[str]
    return_code: int
    stderr: str = ""
    duration_seconds: float


class Last30DaysSearchResult(BaseModel):
    export: Last30DaysAgentExport
    conversations: list[DiscoveryResult]
    trace: Last30DaysExecutionTrace
