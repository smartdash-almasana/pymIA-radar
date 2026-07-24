"""Adapt NavigationResult to DiscoveryResult and persist via existing pipeline."""

from __future__ import annotations

import hashlib
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from pydantic import HttpUrl, TypeAdapter

from app.discovery.contracts import DiscoveryResult
from app.discovery.ingestion import persist_discovery_results
from app.integrations.playwright_mcp import NavigationResult

ADMITTED_STATUSES = frozenset({"SUCCESS", "EXTRACTION_PARTIAL"})
_TRACKING_PARAMS = frozenset({
    "utm_source", "utm_medium", "utm_campaign", "utm_term",
    "utm_content", "fbclid", "gclid",
})
_http_url = TypeAdapter(HttpUrl)


def _canonicalize_url(raw_url: str) -> str:
    """Normalize URL for identity purposes only.

    Lowercases scheme and host, removes fragment and trailing slash,
    strips known tracking params, preserves everything else in order.
    """
    parsed = urlparse(raw_url)
    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or parsed.netloc).lower()
    netloc = f"{hostname}:{parsed.port}" if parsed.port else hostname
    path = parsed.path.rstrip("/") or "/"
    params = parse_qsl(parsed.query, keep_blank_values=True)
    filtered = [(k, v) for k, v in params if k not in _TRACKING_PARAMS]
    query = urlencode(filtered) if filtered else ""
    return urlunparse((scheme, netloc, path, parsed.params, query, ""))


def navigation_to_discovery(
    navigation: NavigationResult,
    *,
    source: str,
    query_origin: str | None = None,
    title: str | None = None,
    context: str | None = None,
) -> DiscoveryResult | None:
    if navigation.status not in ADMITTED_STATUSES:
        return None
    if navigation.final_url is None:
        return None
    try:
        _http_url.validate_strings(navigation.final_url)
    except (ValueError, TypeError):
        return None
    text = navigation.visible_text.strip()
    if len(text) < 50:
        return None

    normalized_source = source.strip().lower()
    canonical = _canonicalize_url(navigation.final_url)
    raw_identity = f"{normalized_source}:{canonical}"
    external_id = f"pw:{hashlib.sha256(raw_identity.encode()).hexdigest()[:16]}"

    return DiscoveryResult(
        source=normalized_source,
        external_id=external_id,
        conversation_url=navigation.final_url,
        author_name=navigation.author,
        title=title,
        text=text,
        context=context,
        published_at=None,
        query_origin=query_origin,
        engagement={
            "requested_url": navigation.requested_url,
            "final_url": navigation.final_url,
            "author_status": navigation.author_status,
            "navigation_status": navigation.status,
            "screenshot_path": navigation.screenshot_path,
            "latency_ms": navigation.latency_ms,
        },
    )


def process_and_persist(
    db,
    navigation: NavigationResult,
    *,
    source: str,
    query_origin: str | None = None,
    title: str | None = None,
    context: str | None = None,
) -> DiscoveryResult | None:
    """Convert and persist in one call. Returns None when rejected."""
    result = navigation_to_discovery(
        navigation=navigation,
        source=source,
        query_origin=query_origin,
        title=title,
        context=context,
    )
    if result is None:
        return None
    persist_discovery_results(db, [result])
    return result