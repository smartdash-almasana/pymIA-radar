from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    id: str = Field(pattern=r"^Q\d{3}$")
    language: Literal["es", "en"]
    query: str = Field(min_length=8)


class SearchQueryCatalog(BaseModel):
    schema_version: Literal["radar-search-queries/v1", "radar-search-queries/v2"]
    client: Literal["Inlak'ech"]
    queries: list[SearchQuery] = Field(min_length=1)


def load_search_query_catalog(path: str | Path) -> SearchQueryCatalog:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    catalog = SearchQueryCatalog.model_validate(raw)
    ids = [item.id for item in catalog.queries]
    if len(ids) != len(set(ids)):
        raise ValueError("search query ids must be unique")
    return catalog
