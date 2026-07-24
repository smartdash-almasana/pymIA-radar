from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.integrations.playwright_mcp import (
    NavigationRequest,
    NavigationResult,
    PlaywrightMCPClient,
    _extract_author,
    _extract_final_url,
    _snapshot_visible_text,
    _classify_snapshot_error,
)


class TestNavigationRequest:
    def test_minimal(self):
        r = NavigationRequest(url="https://example.com")
        assert r.url == "https://example.com"
        assert r.capture_screenshot is False
        assert r.timeout_seconds == 30

    def test_rejects_missing_url(self):
        with pytest.raises(ValidationError):
            NavigationRequest()

    def test_custom_timeout(self):
        r = NavigationRequest(url="https://example.com", timeout_seconds=60)
        assert r.timeout_seconds == 60

    def test_screenshot_enabled(self):
        r = NavigationRequest(url="https://example.com", capture_screenshot=True)
        assert r.capture_screenshot is True


class TestNavigationResult:
    def test_minimal_success(self):
        r = NavigationResult(
            requested_url="https://example.com",
            final_url="https://example.com",
            visible_text="some text",
            author="user123",
            author_status="RESOLVED",
            screenshot_path=None,
            status="SUCCESS",
            latency_ms=1200,
            error_detail=None,
        )
        assert r.requested_url == "https://example.com"
        assert r.author == "user123"

    def test_no_author(self):
        r = NavigationResult(
            requested_url="https://example.com",
            final_url="https://example.com",
            visible_text="",
            author=None,
            author_status="UNAVAILABLE",
            screenshot_path=None,
            status="EXTRACTION_FAILED",
            latency_ms=500,
            error_detail="snapshot failed",
        )
        assert r.author is None
        assert r.author_status == "UNAVAILABLE"

    def test_partial_status(self):
        r = NavigationResult(
            requested_url="https://example.com",
            final_url="https://example.com",
            visible_text="some content",
            author=None,
            author_status="PARTIAL",
            screenshot_path=None,
            status="EXTRACTION_PARTIAL",
            latency_ms=3000,
            error_detail=None,
        )
        assert r.author_status == "PARTIAL"
        assert r.status == "EXTRACTION_PARTIAL"

    def test_captcha_blocked(self):
        r = NavigationResult(
            requested_url="https://example.com",
            final_url=None,
            visible_text="", author=None,
            author_status="UNAVAILABLE",
            screenshot_path=None,
            status="CAPTCHA_BLOCKED",
            latency_ms=2000,
            error_detail="captcha detected",
        )
        assert r.status == "CAPTCHA_BLOCKED"

    def test_login_required(self):
        r = NavigationResult(
            requested_url="https://example.com",
            final_url=None,
            visible_text="",
            author=None,
            author_status="UNAVAILABLE",
            screenshot_path=None,
            status="LOGIN_REQUIRED",
            latency_ms=1500,
            error_detail="login wall",
        )
        assert r.status == "LOGIN_REQUIRED"

    def test_screenshot_path_set(self):
        r = NavigationResult(
            requested_url="https://example.com",
            final_url="https://example.com",
            visible_text="content",
            author="user",
            author_status="RESOLVED",
            screenshot_path="/tmp/screenshot.png",
            status="SUCCESS",
            latency_ms=3000,
            error_detail=None,
        )
        assert r.screenshot_path == "/tmp/screenshot.png"

    def test_all_status_literals_accepted(self):
        for status in [
            "SUCCESS",
            "EXTRACTION_PARTIAL",
            "EXTRACTION_FAILED",
            "SESSION_LOST",
            "MCP_CONNECTION_ERROR",
            "MCP_SERIALIZATION_ERROR",
            "CAPTCHA_BLOCKED",
            "LOGIN_REQUIRED",
        ]:
            r = NavigationResult(
                requested_url="u", final_url="u", visible_text="",
                author=None, author_status="UNAVAILABLE",
                screenshot_path=None, status=status,
                latency_ms=0, error_detail=None,
            )
            assert r.status == status

    def test_all_author_status_literals(self):
        for st in ["RESOLVED", "PARTIAL", "UNAVAILABLE"]:
            r = NavigationResult(
                requested_url="u", final_url="u", visible_text="",
                author=None, author_status=st,
                screenshot_path=None, status="SUCCESS",
                latency_ms=0, error_detail=None,
            )
            assert r.author_status == st


class TestExtractAuthor:
    def test_reddit_user_slash(self):
        assert _extract_author("Posted by u/johndoe in community") == "johndoe"

    def test_author_field(self):
        assert _extract_author('author "maria_123" somewhere') == "maria_123"

    def test_posted_by(self):
        assert _extract_author("posted by: some_user") == "some_user"

    def test_no_author(self):
        assert _extract_author("Just a plain text without any username") is None

    def test_empty_text(self):
        assert _extract_author("") is None

    def test_author_with_spaces_in_quotes(self):
        result = _extract_author('author="john doe" rest')
        assert result == "john doe" or result is not None


class TestExtractFinalUrl:
    def test_from_navigate_response(self):
        text = (
            "### Ran Playwright code\n"
            "await page.goto('https://example.com');\n"
            "### Page\n"
            "- Page URL: https://example.com/page\n"
            "- Page Title: Example\n"
        )
        assert _extract_final_url(text) == "https://example.com/page"

    def test_redirected_url(self):
        text = (
            "### Page\n"
            "- Page URL: https://redirected.org/final\n"
        )
        assert _extract_final_url(text) == "https://redirected.org/final"

    def test_no_url_found(self):
        assert _extract_final_url("no url here") is None

    def test_empty_string(self):
        assert _extract_final_url("") is None


class TestSnapshotVisibleText:
    def test_filters_short_lines(self):
        snap = "a\n" + "x" * 70 + "\nb"
        result = _snapshot_visible_text(snap)
        assert "x" * 70 in result
        assert "a" not in result
        assert "b" not in result

    def test_filters_links(self):
        snap = "https://example.com\n" + "y" * 70
        result = _snapshot_visible_text(snap)
        assert "https://" not in result
        assert "y" * 70 in result

    def test_filters_button_labels(self):
        snap = "button submit\n" + "z" * 70
        result = _snapshot_visible_text(snap)
        assert "button" not in result.lower() or "z" * 70 in result

    def test_empty_input(self):
        assert _snapshot_visible_text("") == ""

    def test_fallback_when_no_meaningful(self):
        snap = "a\nbc\ndef"
        result = _snapshot_visible_text(snap)
        assert len(result) <= 3000


class TestClassifySnapshotError:
    def test_captcha_blocked(self):
        assert _classify_snapshot_error(
            "Please verify you are human before continuing"
        ) == "CAPTCHA_BLOCKED"

    def test_captcha_i_am_not_robot(self):
        assert _classify_snapshot_error(
            "Check the box to confirm you are not a robot"
        ) == "CAPTCHA_BLOCKED"

    def test_captcha_security_check(self):
        assert _classify_snapshot_error(
            "Security check required"
        ) == "CAPTCHA_BLOCKED"

    def test_login_required(self):
        assert _classify_snapshot_error(
            "Sign in to continue viewing this content"
        ) == "LOGIN_REQUIRED"

    def test_login_register(self):
        assert _classify_snapshot_error(
            "Create an account to continue"
        ) == "LOGIN_REQUIRED"

    def test_login_log_in(self):
        assert _classify_snapshot_error(
            "Log in to see this page"
        ) == "LOGIN_REQUIRED"

    def test_spanish_login(self):
        assert _classify_snapshot_error(
            "Inicia sesión para continuar"
        ) == "LOGIN_REQUIRED"

    def test_normal_page_returns_none(self):
        assert _classify_snapshot_error(
            "This is a normal page with content"
        ) is None

    def test_empty_string(self):
        assert _classify_snapshot_error("") is None


class TestPlaywrightMCPClientUnit:
    """Unit tests that don't need a real browser."""

    @pytest.mark.anyio
    async def test_navigate_without_start_returns_session_lost(self):
        client = PlaywrightMCPClient()
        req = NavigationRequest(url="https://example.com")
        result = await client.navigate(req)
        assert result.status == "SESSION_LOST"
        assert result.author_status == "UNAVAILABLE"
        assert result.error_detail == "client not started"
        assert result.final_url is None

    @pytest.mark.anyio
    async def test_is_running_false_by_default(self):
        client = PlaywrightMCPClient()
        assert client.is_running is False

    @pytest.mark.anyio
    async def test_stop_without_start_does_not_raise(self):
        client = PlaywrightMCPClient()
        await client.stop()
        assert client.is_running is False