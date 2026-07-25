from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import re
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
    'Yucatan real estate investment risk',
    'Chichen Itza property investment',
    'Mexico sustainable tourism investment',
    'Yucatan legal security real estate',
    'Mexico community impact investment',
)

_TERRITORY = re.compile(r'\b(yucatan|chichen itza|riviera maya|quintana roo|mexico|m[eé]xico)\b', re.I)
_INVESTMENT = re.compile(r'\b(invest|investment|investor|invertir|inversi[oó]n|real estate|property|propiedad|inmobiliari[oa]|capital|return|rentabilidad|roi)\b', re.I)
_DUE_DILIGENCE = re.compile(r'\b(risk|legal|ownership|title|governance|timeline|return|security|riesgo|legal|propiedad|t[ií]tulo|gobernanza|plazo|rentabilidad|seguridad jur[ií]dica|compar|evaluat|consider|duda|pregunta|worth it|conviene)\b', re.I)
_NOISE = re.compile(r'\b(programming|software|api|bug|javascript|python|developer|job|hiring|football|soccer|recipe|weather|gaming|crypto token|nft)\b', re.I)


def relevance_score_payload(payload: dict[str, Any]) -> int:
    text = ' '.join(str(payload.get(k) or '') for k in ('title', 'text', 'context', 'query_origin'))
    if _NOISE.search(text):
        return -10
    score = 0
    if _TERRITORY.search(text):
        score += 3
    if _INVESTMENT.search(text):
        score += 3
    if _DUE_DILIGENCE.search(text):
        score += 3
    if '?' in text:
        score += 1
    if len(text) >= 140:
        score += 1
    return score


def is_relevant_payload(payload: dict[str, Any]) -> bool:
    return relevance_score_payload(payload) >= 7


def is_relevant_conversation(conversation: Conversation) -> bool:
    return is_relevant_payload({
        'title': conversation.title,
        'text': conversation.text,
        'context': conversation.context,
        'query_origin': conversation.query_origin,
    })


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


def _search_github(client: httpx.Client, query: str, limit: int) -> list[dict[str, Any]]:
    response = client.get(
        "https://api.github.com/search/issues",
        params={"q": f"{query} in:title,body is:issue", "sort": "created", "order": "desc", "per_page": limit},
        headers={"Accept": "application/vnd.github+json", "User-Agent": "InlakechRadar/1.0"},
    )
    response.raise_for_status()
    rows: list[dict[str, Any]] = []
    for item in response.json().get("items", []):
        external_id = str(item.get("id") or "").strip()
        title = str(item.get("title") or "").strip()
        url = str(item.get("html_url") or "").strip()
        if not external_id or not title or not url:
            continue
        user = item.get("user") or {}
        repo_url = str(item.get("repository_url") or "")
        rows.append(
            {
                "source": "github",
                "external_id": external_id,
                "conversation_url": url,
                "author_name": user.get("login"),
                "title": title,
                "text": str(item.get("body") or title),
                "context": repo_url.rsplit("/", 1)[-1] if repo_url else "GitHub public issue",
                "published_at": datetime.fromisoformat(str(item.get("created_at")).replace("Z", "+00:00")) if item.get("created_at") else None,
                "query_origin": query,
                "engagement": {"comments": item.get("comments")},
            }
        )
    return rows


def _search_stackexchange(client: httpx.Client, query: str, limit: int) -> list[dict[str, Any]]:
    response = client.get(
        "https://api.stackexchange.com/2.3/search/advanced",
        params={"q": query, "site": "travel", "sort": "creation", "order": "desc", "pagesize": limit, "filter": "withbody"},
    )
    response.raise_for_status()
    rows: list[dict[str, Any]] = []
    for item in response.json().get("items", []):
        external_id = str(item.get("question_id") or "").strip()
        title = str(item.get("title") or "").strip()
        url = str(item.get("link") or "").strip()
        if not external_id or not title or not url:
            continue
        owner = item.get("owner") or {}
        rows.append(
            {
                "source": "stackexchange",
                "external_id": external_id,
                "conversation_url": url,
                "author_name": owner.get("display_name"),
                "title": title,
                "text": str(item.get("body") or title),
                "context": "Stack Exchange public question",
                "published_at": _parse_epoch(item.get("creation_date")),
                "query_origin": query,
                "engagement": {"score": item.get("score"), "answers": item.get("answer_count"), "views": item.get("view_count")},
            }
        )
    return rows


def _search_bluesky(client: httpx.Client, query: str, limit: int) -> list[dict[str, Any]]:
    response = client.get(
        "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts",
        params={"q": query, "limit": limit, "sort": "latest"},
        headers={"User-Agent": "InlakechRadar/1.0"},
    )
    response.raise_for_status()
    rows: list[dict[str, Any]] = []
    for post in response.json().get("posts", []):
        uri = str(post.get("uri") or "").strip()
        record = post.get("record") or {}
        author = post.get("author") or {}
        text = str(record.get("text") or "").strip()
        handle = str(author.get("handle") or "").strip()
        if not uri or not text or not handle:
            continue
        rkey = uri.rsplit("/", 1)[-1]
        indexed_at = post.get("indexedAt") or record.get("createdAt")
        published_at = None
        if indexed_at:
            try:
                published_at = datetime.fromisoformat(str(indexed_at).replace("Z", "+00:00"))
            except ValueError:
                published_at = None
        rows.append(
            {
                "source": "bluesky",
                "external_id": uri,
                "conversation_url": f"https://bsky.app/profile/{handle}/post/{rkey}",
                "author_name": author.get("displayName") or handle,
                "title": text[:120],
                "text": text,
                "context": "Bluesky public post",
                "published_at": published_at,
                "query_origin": query,
                "engagement": {
                    "likes": post.get("likeCount"),
                    "replies": post.get("replyCount"),
                    "reposts": post.get("repostCount"),
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
                ("github", _search_github),
                ("stackexchange", _search_stackexchange),
                ("bluesky", _search_bluesky),
            ):
                try:
                    rows = searcher(client, query, per_source_limit)
                except (httpx.HTTPError, ValueError, TypeError):
                    continue
                fetched_rows.extend(rows)
                if rows and source_name not in successful_sources:
                    successful_sources.append(source_name)

    relevant_rows = [payload for payload in fetched_rows if is_relevant_payload(payload)]
    relevant_rows.sort(key=relevance_score_payload, reverse=True)

    inserted = 0
    duplicates = 0
    seen: set[tuple[str, str]] = set()
    for payload in relevant_rows[:10]:
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
