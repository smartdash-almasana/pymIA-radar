from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api import routes
from app.db.session import Base
from app.discovery.contracts import DiscoveryResult
from app.discovery.last30days_adapter import Last30DaysExecutionError
from app.discovery.last30days_contracts import (
    Last30DaysAgentExport,
    Last30DaysExecutionTrace,
    Last30DaysSearchResult,
)
from app.discovery.operational_scan import load_operational_queries, run_operational_scan
from app.main import app
from app.models.conversation import Conversation
from app.schemas.discovery_scan import OperationalScanRequest, OperationalScanResult


class FakeAdapter:
    def __init__(self, conversations: list[DiscoveryResult]) -> None:
        self.conversations = conversations

    def search(self, query: str, **_: object) -> Last30DaysSearchResult:
        return Last30DaysSearchResult(
            export=Last30DaysAgentExport(
                schema_version="1.2",
                query=query,
                generated_at=datetime.now(UTC),
                window_days=30,
                results=[],
            ),
            conversations=self.conversations,
            trace=Last30DaysExecutionTrace(
                command=["fake"],
                return_code=0,
                duration_seconds=1.25,
            ),
        )


def _conversation(external_id: str, text: str) -> DiscoveryResult:
    return DiscoveryResult(
        source="reddit",
        external_id=external_id,
        conversation_url=f"https://example.test/{external_id}",
        author_name="Public author",
        title="Conversation about Mexico",
        text=text,
        context="Public discussion captured for operational RADAR review.",
        published_at=datetime.now(UTC),
        query_origin="inversión de impacto México",
        engagement={},
    )


def _engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine


def test_operational_scan_admits_only_substantive_and_is_idempotent() -> None:
    substantive = _conversation(
        "substantive-1",
        "Estoy evaluando invertir y participar en un proyecto regenerativo en México. "
        "Quiero entender la gobernanza, los riesgos, la propiedad y el horizonte de largo plazo. "
        "¿Qué experiencias existen y cómo se compara con otras comunidades intencionales?",
    )
    review = _conversation(
        "review-1",
        "Crónica descriptiva sobre comunidades en México, sus paisajes, costumbres y experiencias. "
        "El texto comparte información general y recuerdos de viaje sin plantear un paso posterior.",
    )
    insufficient = DiscoveryResult(
        source="reddit",
        external_id="thin-1",
        conversation_url="https://example.test/thin-1",
        author_name=None,
        title=None,
        text="Comunidad México.",
        context=None,
        published_at=None,
        query_origin="inversión de impacto México",
        engagement={},
    )
    adapter = FakeAdapter([substantive, review, insufficient])
    engine = _engine()
    try:
        with Session(engine) as db:
            first = run_operational_scan(
                db,
                OperationalScanRequest(query_id="Q101"),
                adapter=adapter,
            )
            second = run_operational_scan(
                db,
                OperationalScanRequest(query_id="Q101"),
                adapter=adapter,
            )
            stored = list(db.scalars(select(Conversation)))

        assert first.total_results == 3
        assert first.substantive_results == 1
        assert first.review_results == 1
        assert first.insufficient_results == 1
        assert first.admitted_results == 1
        assert first.new_conversations == 1
        assert first.existing_conversations == 0
        assert second.new_conversations == 0
        assert second.existing_conversations == 1
        assert [item.external_id for item in stored] == ["substantive-1"]
    finally:
        engine.dispose()


def test_operational_query_catalog_is_exposed() -> None:
    queries = load_operational_queries()
    assert len(queries) == 20
    assert queries[0].id == "Q101"

    with TestClient(app) as client:
        response = client.get("/api/discovery/search-queries")
        assert response.status_code == 200
        assert response.json()[0]["id"] == "Q101"


def test_operational_scan_route_returns_result(monkeypatch) -> None:
    expected = OperationalScanResult(
        query_id="Q101",
        query="inversión de impacto México",
        total_results=4,
        substantive_results=2,
        review_results=1,
        insufficient_results=1,
        admitted_results=2,
        new_conversations=1,
        existing_conversations=1,
        duration_seconds=2.5,
    )
    monkeypatch.setattr(routes, "run_operational_scan", lambda db, payload: expected)

    with TestClient(app) as client:
        response = client.post("/api/discovery/scan", json={"query_id": "Q101"})
        assert response.status_code == 200
        assert response.json()["new_conversations"] == 1


def test_operational_scan_route_sanitizes_source_failure(monkeypatch) -> None:
    def fail(db, payload):
        raise Last30DaysExecutionError("secret provider stderr")

    monkeypatch.setattr(routes, "run_operational_scan", fail)
    with TestClient(app) as client:
        response = client.post("/api/discovery/scan", json={"query_id": "Q101"})
        assert response.status_code == 503
        assert "secret provider stderr" not in response.text
        assert "last30days configuration" in response.json()["detail"]
