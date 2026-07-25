from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation


@dataclass(frozen=True)
class LiveSearchSummary:
    inserted: int
    duplicates: int
    fetched: int
    sources: tuple[str, ...]


DEFAULT_QUERIES = (
    "inversion inmobiliaria yucatan",
    "invertir en mexico turismo sustentable",
    "chichen itza real estate investment",
)


def _parse_epoch(value: Any) -> datetime | None:
    try:
        return datetime.fromtimestamp(float(value), tz=UTC)
    except (TypeError, ValueError, OSError):
        return None


def _search_reddit(client: httpx.Client, query: str, limit: int) -> list[dict[str, Any]]:
    response = client.get(
        "https://www.reddit.com/search.json",
        params={"q": query, "sort": "new", "limit": limit, "type": "link"},
        headers={"User-Agent": "InlakechRadar/1.0 public-conversation-discovery"},
    )
    response.raise_for_status()
    children = response.json().get("data", {}).get("children", [])
    rows: list[dict[str, Any]] = []
    for child in children:
        data = child.get("data", {})
        external_id = str(data.get("name") or data.get("id") or "").strip()
        permalink = str(data.get("permalink") or "").strip()
        title = str(data.get("title") or "").strip()
        body = str(data.get("selftext") or "").strip()
        if not external_id or not permalink or not title:
            continue
        rows.append(
            {
                "source": "reddit",
                "external_id": external_id,
                "conversation_url": f"https://www.reddit.com{permalink}",
                "author_name": data.get("author"),
                "title": title,
                "text": body or title,
                "context": f"r/{data.get('subreddit', 'unknown')}",
                "published_at": _parse_epoch(data.get("created_utc")),
                "query_origin": query,
                "engagement": {
                    "score": data.get("score"),
                    "comments": data.get("num_comments"),
                },
            }
        )
    return rows


def _search_hackernews(client: httpx.Client, query: str, limit: int) -> list[dict[str, Any]]:
    response = client.get(
        "https://hn.algolia.com/api/v1/search_by_date",
        params={"query": query, "tags": "story", "hitsPerPage": limit},
    )
    response.raise_for_status()
    rows: list[dict[str, Any]] = []
    for hit in response.json().get("hits", []):
        external_id = str(hit.get("objectID") or "").strip()
        title = str(hit.get("title") or "").strip()
        if not external_id or not title:
            continue
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={external_id}"
        rows.append(
            {
                "source": "hackernews",
                "external_id": external_id,
                "conversation_url": str(url),
                "author_name": hit.get("author"),
                "title": title,
                "text": str(hit.get("story_text") or title),
                "context": "Hacker News public story",
                "published_at": _parse_epoch(hit.get("created_at_i")),
                "query_origin": query,
                "engagement": {
                    "points": hit.get("points"),
                    "comments": hit.get("num_comments"),
                },
            }
        )
    return rows


def run_lightweight_live_search(
    db: Session,
    *,
    queries: tuple[str, ...] = DEFAULT_QUERIES,
    per_source_limit: int = 4,
    timeout_seconds: float = 12.0,
) -> LiveSearchSummary:
    fetched_rows: list[dict[str, Any]] = []
    successful_sources: list[str] = []
    with httpx.Client(timeout=timeout_seconds, follow_redirects=True) as client:
        for query in queries:
            for source_name, searcher in (
                ("reddit", _search_reddit),
                ("hackernews", _search_hackernews),
            ):
                try:
                    rows = searcher(client, query, per_source_limit)
                except (httpx.HTTPError, ValueError, TypeError):
                    continue
                fetched_rows.extend(rows)
                if rows and source_name not in successful_sources:
                    successful_sources.append(source_name)

    inserted = 0
    duplicates = 0
    seen: set[tuple[str, str]] = set()
    for payload in fetched_rows:
        key = (payload["source"], payload["external_id"])
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        exists = db.scalar(
            select(Conversation.id).where(
                Conversation.source == payload["source"],
                Conversation.external_id == payload["external_id"],
            )
        )
        if exists is not None:
            duplicates += 1
            continue
        db.add(Conversation(**payload, status="detected"))
        inserted += 1
    db.commit()
    return LiveSearchSummary(
        inserted=inserted,
        duplicates=duplicates,
        fetched=len(fetched_rows),
        sources=tuple(successful_sources),
    )
