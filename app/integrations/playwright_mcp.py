"""Persistent Playwright MCP runner for RADAR.

Single Chromium instance, session reuse, text/URL extraction via
browser_snapshot. No browser_evaluate.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import re
import time
from typing import Literal

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel

NavigationStatus = Literal[
    "SUCCESS",
    "EXTRACTION_PARTIAL",
    "EXTRACTION_FAILED",
    "SESSION_LOST",
    "MCP_CONNECTION_ERROR",
    "MCP_SERIALIZATION_ERROR",
    "CAPTCHA_BLOCKED",
    "LOGIN_REQUIRED",
]

AuthorStatus = Literal["RESOLVED", "PARTIAL", "UNAVAILABLE"]


class NavigationRequest(BaseModel):
    url: str
    capture_screenshot: bool = False
    timeout_seconds: int = 30


class NavigationResult(BaseModel):
    requested_url: str
    final_url: str | None
    visible_text: str
    author: str | None
    author_status: AuthorStatus
    screenshot_path: str | None
    status: NavigationStatus
    latency_ms: int
    error_detail: str | None


_AUTHOR_PATTERNS = [
    re.compile(r"(?:u|user)/([A-Za-z0-9_-]+)", re.IGNORECASE),
    re.compile(r"author[\":=\s]+([A-Za-z0-9_ -]+?)(?:[\s,\"}])", re.IGNORECASE),
    re.compile(r"posted by\s*:?\s*([A-Za-z0-9_-]+)", re.IGNORECASE),
]

_URL_PATTERN = re.compile(r"- Page URL:\s*(\S+)")

_CAPTCHA_KEYWORDS = [
    "captcha", "verify you are human", "security check",
    "i am not a robot", "please verify", "not a robot",
]

_LOGIN_KEYWORDS = [
    "log in", "sign in", "login", "sign in to continue",
    "log in to continue", "inicia sesi", "iniciar sesi",
    "register", "create an account to continue",
]

_SCREENSHOT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", ".tmp", "screenshots"
)

# ponytail: MCP saves files relative to cwd (project root)
_SCREENSHOT_REL_DIR = os.path.join(".tmp", "screenshots")


def _extract_author(text: str) -> str | None:
    for pat in _AUTHOR_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1).strip()
    return None


def _extract_final_url(nav_text: str) -> str | None:
    m = _URL_PATTERN.search(nav_text)
    return m.group(1) if m else None


def _snapshot_visible_text(snap_text: str) -> str:
    lines = [l.strip() for l in snap_text.split("\n") if l.strip()]
    meaningful = [
        l for l in lines
        if len(l) > 60
        and not l.startswith(("http", "/", "www"))
        and "button" not in l.lower()
    ]
    return "\n".join(meaningful[:10]) if meaningful else snap_text[:3000]


def _classify_snapshot_error(snap_text: str) -> NavigationStatus | None:
    lower = snap_text.lower()
    if any(kw in lower for kw in _CAPTCHA_KEYWORDS):
        return "CAPTCHA_BLOCKED"
    if any(kw in lower for kw in _LOGIN_KEYWORDS):
        return "LOGIN_REQUIRED"
    return None


class PlaywrightMCPClient:
    """Single persistent Chromium via Playwright MCP over stdio.

    One instance, session survives across navigations. Extraction uses
    browser_snapshot (no browser_evaluate).
    """

    def __init__(self) -> None:
        self._session: ClientSession | None = None
        self._stdio_ctx: object = None

    async def start(self) -> None:
        params = StdioServerParameters(command="npx", args=["@playwright/mcp"])
        self._stdio_ctx = stdio_client(params)
        read, write = await self._stdio_ctx.__aenter__()
        self._session = await ClientSession(read, write).__aenter__()
        await self._session.initialize()

    async def stop(self) -> None:
        if self._session:
            await self._session.__aexit__(None, None, None)
            self._session = None
        if self._stdio_ctx:
            with contextlib.suppress(BaseExceptionGroup, RuntimeError):
                await self._stdio_ctx.__aexit__(None, None, None)
            self._stdio_ctx = None

    @property
    def is_running(self) -> bool:
        return self._session is not None

    async def navigate(self, request: NavigationRequest) -> NavigationResult:
        t0 = time.perf_counter()
        url = request.url

        if not self._session:
            return NavigationResult(
                requested_url=url, final_url=None, visible_text="",
                author=None, author_status="UNAVAILABLE",
                screenshot_path=None, status="SESSION_LOST",
                latency_ms=round((time.perf_counter() - t0) * 1000),
                error_detail="client not started",
            )

        try:
            nav = await self._session.call_tool(
                "browser_navigate", arguments={"url": url}
            )

            nav_text = "".join(c.text or "" for c in (nav.content or []))
            final_url = _extract_final_url(nav_text) if nav.content else None

            if nav.isError:
                detail = nav_text[:500] or "navigate failed"
                return NavigationResult(
                    requested_url=url, final_url=final_url, visible_text="",
                    author=None, author_status="UNAVAILABLE",
                    screenshot_path=None, status="MCP_CONNECTION_ERROR",
                    latency_ms=round((time.perf_counter() - t0) * 1000),
                    error_detail=detail,
                )

            await asyncio.sleep(2)

            snap = await self._session.call_tool("browser_snapshot", arguments={})
            if snap.isError or not snap.content:
                return NavigationResult(
                    requested_url=url, final_url=final_url, visible_text="",
                    author=None, author_status="UNAVAILABLE",
                    screenshot_path=None, status="EXTRACTION_FAILED",
                    latency_ms=round((time.perf_counter() - t0) * 1000),
                    error_detail="snapshot failed",
                )

            snap_text = "".join(c.text or "" for c in snap.content)

            blocked_status = _classify_snapshot_error(snap_text)
            if blocked_status:
                return NavigationResult(
                    requested_url=url, final_url=final_url, visible_text=snap_text[:500],
                    author=None, author_status="UNAVAILABLE",
                    screenshot_path=None, status=blocked_status,
                    latency_ms=round((time.perf_counter() - t0) * 1000),
                    error_detail=f"page blocked: {blocked_status} detected in content",
                )

            author = _extract_author(snap_text)
            visible_text = _snapshot_visible_text(snap_text)

            screenshot_path: str | None = None
            if request.capture_screenshot:
                os.makedirs(_SCREENSHOT_DIR, exist_ok=True)
                ts = time.strftime("%Y%m%d-%H%M%S")
                filename = f"nav-{ts}.png"
                rel = os.path.join(_SCREENSHOT_REL_DIR, filename)
                ss = await self._session.call_tool(
                    "browser_take_screenshot",
                    arguments={"type": "png", "scale": "css", "filename": rel},
                )
                if not ss.isError:
                    screenshot_path = os.path.join(_SCREENSHOT_DIR, filename)

            if author and len(visible_text) > 200:
                nav_status: NavigationStatus = "SUCCESS"
                author_status: AuthorStatus = "RESOLVED"
            elif len(visible_text) > 50:
                nav_status = "EXTRACTION_PARTIAL"
                author_status = "PARTIAL" if author is None else "RESOLVED"
            else:
                nav_status = "EXTRACTION_FAILED"
                author_status = "PARTIAL" if author else "UNAVAILABLE"

            return NavigationResult(
                requested_url=url,
                final_url=final_url,
                visible_text=visible_text,
                author=author,
                author_status=author_status,
                screenshot_path=screenshot_path,
                status=nav_status,
                latency_ms=round((time.perf_counter() - t0) * 1000),
                error_detail=None,
            )

        except Exception as e:
            err_name = type(e).__name__
            if "Connection" in err_name:
                nav_status: NavigationStatus = "MCP_CONNECTION_ERROR"
            elif "Serialization" in err_name:
                nav_status = "MCP_SERIALIZATION_ERROR"
            else:
                nav_status = "SESSION_LOST"
            return NavigationResult(
                requested_url=url, final_url=None, visible_text="",
                author=None, author_status="UNAVAILABLE",
                screenshot_path=None, status=nav_status,
                latency_ms=round((time.perf_counter() - t0) * 1000),
                error_detail=f"{err_name}: {e}"[:500],
            )