import json

from sqlalchemy import func, select

from app.db.session import Base, SessionLocal, engine
from app.discovery.ingestion import persist_discovery_results
from app.discovery.last30days_adapter import Last30DaysAdapter
from app.models.conversation import Conversation


def test_fixture_normalization_persists_idempotently_and_is_queryable(tmp_path):
    Base.metadata.create_all(bind=engine)
    payload = {
        "schema_version": "1.2",
        "query": "patrimonio regenerativo",
        "generated_at": "2026-07-18T12:00:00Z",
        "window_days": 30,
        "source_status": {"reddit": "ok"},
        "freshness_verdicts": [],
        "clusters": [],
        "results": [
            {
                "candidate_id": "reddit:integration-001",
                "title": "Patrimonio con impacto",
                "source": "reddit",
                "url": "https://reddit.com/r/example/comments/integration001",
                "published_at": "2026-07-17T10:00:00Z",
                "summary": "Busco construir patrimonio con impacto comunitario.",
                "engagement": {"score": 18},
                "relevance_score": 0.82,
            }
        ],
    }
    adapter = Last30DaysAdapter(repo_path=tmp_path)
    export = adapter.parse_output(
        json.dumps(payload),
        requested_query="patrimonio regenerativo",
    )
    normalized = adapter.normalize(export)

    with SessionLocal() as db:
        first = persist_discovery_results(db, normalized)
        second = persist_discovery_results(db, normalized)

        assert len(first) == 1
        assert len(second) == 1
        assert first[0].id == second[0].id

        count = db.scalar(
            select(func.count()).select_from(Conversation).where(
                Conversation.source == "reddit",
                Conversation.external_id == "reddit:integration-001",
            )
        )
        stored = db.scalar(
            select(Conversation).where(
                Conversation.source == "reddit",
                Conversation.external_id == "reddit:integration-001",
            )
        )

        assert count == 1
        assert stored is not None
        assert stored.query_origin == "patrimonio regenerativo"
        assert stored.text == "Busco construir patrimonio con impacto comunitario."
