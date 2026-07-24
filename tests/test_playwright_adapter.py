import hashlib

from sqlalchemy import func, select

from app.db.session import Base, SessionLocal, engine
from app.discovery.playwright_adapter import _canonicalize_url, navigation_to_discovery, process_and_persist
from app.integrations.playwright_mcp import NavigationResult
from app.models.conversation import Conversation


def _nav(
    *,
    status="SUCCESS",
    final_url="https://example.com/post/1",
    visible_text="A" * 300,
    author="user123",
    author_status="RESOLVED",
    screenshot_path=None,
    latency_ms=1500,
    error_detail=None,
) -> NavigationResult:
    return NavigationResult(
        requested_url="https://example.com/redirect-me",
        final_url=final_url,
        visible_text=visible_text,
        author=author,
        author_status=author_status,
        screenshot_path=screenshot_path,
        status=status,
        latency_ms=latency_ms,
        error_detail=error_detail,
    )


def _expected_id(source: str, final_url: str) -> str:
    canonical = _canonicalize_url(final_url)
    raw = f"{source.strip().lower()}:{canonical}"
    return f"pw:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


class TestCanonicalizeUrl:
    def test_lowercases_scheme_and_host(self):
        assert _canonicalize_url("HTTP://ExAmPlE.COM/Path") == "http://example.com/Path"

    def test_removes_fragment(self):
        result = _canonicalize_url("https://example.com/page#section-a")
        assert "section-a" not in result
        assert result == "https://example.com/page"

    def test_removes_trailing_slash(self):
        assert _canonicalize_url("https://example.com/page/") == "https://example.com/page"

    def test_preserves_root_trailing_slash(self):
        assert _canonicalize_url("https://example.com/") == "https://example.com/"

    def test_strips_utm_params(self):
        url = "https://example.com/page?utm_source=twitter&utm_medium=social&a=1"
        assert "utm_source" not in _canonicalize_url(url)
        assert "utm_medium" not in _canonicalize_url(url)
        assert "a=1" in _canonicalize_url(url)

    def test_strips_fbclid(self):
        url = "https://example.com/page?fbclid=abc123&id=42"
        result = _canonicalize_url(url)
        assert "fbclid" not in result
        assert "id=42" in result

    def test_strips_gclid(self):
        url = "https://example.com/page?gclid=xyz789&ref=home"
        result = _canonicalize_url(url)
        assert "gclid" not in result
        assert "ref=home" in result

    def test_preserves_functional_params(self):
        url = "https://example.com/post?id=123&ref=sidebar"
        result = _canonicalize_url(url)
        assert "id=123" in result
        assert "ref=sidebar" in result

    def test_preserves_only_tracking_params(self):
        url = "https://example.com/page?q=search&sort=asc&utm_campaign=test"
        result = _canonicalize_url(url)
        assert "q=search" in result
        assert "sort=asc" in result
        assert "utm_campaign" not in result


class TestNavigationToDiscovery:
    def test_success_maps_all_fields(self):
        nav = _nav(screenshot_path=".tmp/screenshots/nav-123.png")
        result = navigation_to_discovery(nav, source="reddit", query_origin="test query")
        assert result is not None
        assert result.source == "reddit"
        assert result.external_id == _expected_id("reddit", nav.final_url)
        assert str(result.conversation_url) == "https://example.com/post/1"
        assert result.author_name == "user123"
        assert result.text == "A" * 300
        assert result.query_origin == "test query"
        assert result.published_at is None
        assert result.engagement["screenshot_path"] == ".tmp/screenshots/nav-123.png"
        assert result.engagement["latency_ms"] == 1500
        assert result.engagement["navigation_status"] == "SUCCESS"

    def test_external_id_is_deterministic(self):
        nav = _nav()
        a = navigation_to_discovery(nav, source="reddit")
        b = navigation_to_discovery(nav, source="reddit")
        assert a is not None and b is not None
        assert a.external_id == b.external_id
        assert a.external_id.startswith("pw:")
        assert len(a.external_id) == 19

    def test_same_url_different_text_same_id(self):
        nav_a = _nav(visible_text="A" * 300)
        nav_b = _nav(visible_text="B" * 300)
        a = navigation_to_discovery(nav_a, source="reddit")
        b = navigation_to_discovery(nav_b, source="reddit")
        assert a is not None and b is not None
        assert a.external_id == b.external_id

    def test_trailing_slash_same_id(self):
        nav_a = _nav(final_url="https://example.com/post")
        nav_b = _nav(final_url="https://example.com/post/")
        a = navigation_to_discovery(nav_a, source="reddit")
        b = navigation_to_discovery(nav_b, source="reddit")
        assert a is not None and b is not None
        assert a.external_id == b.external_id

    def test_different_fragments_same_id(self):
        nav_a = _nav(final_url="https://example.com/post#section-a")
        nav_b = _nav(final_url="https://example.com/post#section-b")
        a = navigation_to_discovery(nav_a, source="reddit")
        b = navigation_to_discovery(nav_b, source="reddit")
        assert a is not None and b is not None
        assert a.external_id == b.external_id

    def test_tracking_params_same_id(self):
        nav_a = _nav(final_url="https://example.com/post?id=1")
        nav_b = _nav(final_url="https://example.com/post?id=1&utm_source=twitter&fbclid=abc")
        a = navigation_to_discovery(nav_a, source="reddit")
        b = navigation_to_discovery(nav_b, source="reddit")
        assert a is not None and b is not None
        assert a.external_id == b.external_id

    def test_functional_params_different_id(self):
        nav_a = _nav(final_url="https://example.com/post?id=1")
        nav_b = _nav(final_url="https://example.com/post?id=2")
        a = navigation_to_discovery(nav_a, source="reddit")
        b = navigation_to_discovery(nav_b, source="reddit")
        assert a is not None and b is not None
        assert a.external_id != b.external_id

    def test_host_case_different_same_id(self):
        nav_a = _nav(final_url="https://Example.com/Post")
        nav_b = _nav(final_url="https://example.com/Post")
        a = navigation_to_discovery(nav_a, source="reddit")
        b = navigation_to_discovery(nav_b, source="reddit")
        assert a is not None and b is not None
        assert a.external_id == b.external_id

    def test_source_is_normalized_for_identity_and_persistence(self):
        nav = _nav()
        a = navigation_to_discovery(nav, source="Reddit")
        b = navigation_to_discovery(nav, source=" reddit ")
        assert a is not None and b is not None
        assert a.source == b.source == "reddit"
        assert a.external_id == b.external_id

    def test_different_source_different_id(self):
        nav = _nav()
        a = navigation_to_discovery(nav, source="reddit")
        b = navigation_to_discovery(nav, source="twitter")
        assert a is not None and b is not None
        assert a.external_id != b.external_id

    def test_truly_different_url_different_id(self):
        nav_a = _nav(final_url="https://example.com/post/a")
        nav_b = _nav(final_url="https://example.com/post/b")
        a = navigation_to_discovery(nav_a, source="reddit")
        b = navigation_to_discovery(nav_b, source="reddit")
        assert a is not None and b is not None
        assert a.external_id != b.external_id

    def test_extraction_partial_without_author(self):
        nav = _nav(status="EXTRACTION_PARTIAL", author=None, author_status="PARTIAL", visible_text="B" * 100)
        result = navigation_to_discovery(nav, source="reddit")
        assert result is not None
        assert result.author_name is None

    def test_blocked_status_rejected(self):
        for status in ("EXTRACTION_FAILED", "SESSION_LOST", "MCP_CONNECTION_ERROR",
                       "MCP_SERIALIZATION_ERROR", "CAPTCHA_BLOCKED", "LOGIN_REQUIRED"):
            nav = _nav(status=status)
            assert navigation_to_discovery(nav, source="reddit") is None, f"{status} should be rejected"

    def test_no_final_url_rejected(self):
        nav = _nav(final_url=None)
        assert navigation_to_discovery(nav, source="reddit") is None

    def test_short_text_rejected(self):
        nav = _nav(visible_text="Short", status="EXTRACTION_PARTIAL")
        assert navigation_to_discovery(nav, source="reddit") is None

    def test_invalid_url_rejected(self):
        nav = _nav(final_url="not-a-url")
        assert navigation_to_discovery(nav, source="reddit") is None

    def test_engagement_preserves_all_traceability(self):
        nav = _nav(screenshot_path=".tmp/screenshots/nav-456.png")
        result = navigation_to_discovery(nav, source="reddit")
        assert result is not None
        assert result.engagement == {
            "requested_url": "https://example.com/redirect-me",
            "final_url": "https://example.com/post/1",
            "author_status": "RESOLVED",
            "navigation_status": "SUCCESS",
            "screenshot_path": ".tmp/screenshots/nav-456.png",
            "latency_ms": 1500,
        }

    def test_title_and_context(self):
        nav = _nav()
        result = navigation_to_discovery(nav, source="reddit", title="Some Title", context="Some Context")
        assert result is not None
        assert result.title == "Some Title"
        assert result.context == "Some Context"


class TestProcessAndPersist:
    def test_persists_success(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav()
        with SessionLocal() as db:
            result = process_and_persist(db, nav, source="reddit", query_origin="pw test")
            assert result is not None

            count = db.scalar(
                select(func.count()).select_from(Conversation).where(
                    Conversation.source == "reddit",
                    Conversation.external_id == result.external_id,
                )
            )
            assert count == 1

    def test_idempotent_same_url_different_text(self):
        Base.metadata.create_all(bind=engine)
        nav_a = _nav(visible_text="A" * 300)
        nav_b = _nav(visible_text="B" * 300)
        with SessionLocal() as db:
            first = process_and_persist(db, nav_a, source="reddit")
            second = process_and_persist(db, nav_b, source="reddit")
            assert first is not None and second is not None
            assert first.external_id == second.external_id == _expected_id("reddit", nav_a.final_url)

            count = db.scalar(
                select(func.count()).select_from(Conversation).where(
                    Conversation.source == "reddit",
                    Conversation.external_id == _expected_id("reddit", nav_a.final_url),
                )
            )
            assert count == 1

    def test_idempotent_source_variants(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav()
        with SessionLocal() as db:
            first = process_and_persist(db, nav, source="Reddit")
            second = process_and_persist(db, nav, source=" reddit ")
            assert first is not None and second is not None
            assert first.source == second.source == "reddit"
            assert first.external_id == second.external_id

            count = db.scalar(
                select(func.count()).select_from(Conversation).where(
                    Conversation.source == "reddit",
                    Conversation.external_id == first.external_id,
                )
            )
            assert count == 1

    def test_blocked_not_persisted(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(status="CAPTCHA_BLOCKED")
        with SessionLocal() as db:
            result = process_and_persist(db, nav, source="reddit")
            assert result is None