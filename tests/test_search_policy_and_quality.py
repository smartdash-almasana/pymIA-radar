import json
from pathlib import Path

import pytest

from app.discovery.contracts import DiscoveryResult
from app.discovery.conversation_quality import assess_conversation_quality
from app.discovery.search_policy import load_search_query_catalog


def test_canonical_search_catalog_loads() -> None:
    catalog = load_search_query_catalog(Path("config/search_queries.v1.json"))
    assert catalog.schema_version == "radar-search-queries/v1"
    assert catalog.client == "Inlak'ech"
    assert len(catalog.queries) == 10
    assert len({query.id for query in catalog.queries}) == 10
    assert {query.language for query in catalog.queries} == {"es", "en"}


def test_duplicate_query_ids_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "queries.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "radar-search-queries/v1",
                "client": "Inlak'ech",
                "queries": [
                    {"id": "Q001", "language": "es", "query": "consulta suficientemente larga"},
                    {"id": "Q001", "language": "en", "query": "another sufficiently long query"},
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unique"):
        load_search_query_catalog(path)


def test_substantive_conversation_is_not_confused_with_affinity() -> None:
    result = DiscoveryResult(
        source="reddit",
        external_id="quality-001",
        conversation_url="https://example.com/quality-001",
        title="Estoy evaluando una inversión de largo plazo",
        text=(
            "Estoy comparando alternativas para invertir y participar en un proyecto. "
            "Tengo dudas sobre gobernanza, propiedad, riesgos y plazos. "
            "¿Qué referencias debería revisar antes de contactar al equipo?"
        ),
        context="Conversación pública con respuestas argumentadas.",
        query_origin="inversión regenerativa México experiencias recomendaciones",
        engagement={"comments": 7},
    )
    assessment = assess_conversation_quality(result)
    assert assessment.status == "substantive"
    assert assessment.score >= 5
    assert "decision_language" in assessment.positive_signals
    assert "objection_or_due_diligence" in assessment.positive_signals
    assert "author_name" in assessment.missing_fields


def test_promotional_fragment_is_not_substantive() -> None:
    result = DiscoveryResult(
        source="web",
        external_id="quality-002",
        conversation_url="https://example.com/quality-002",
        text="Oferta limitada. Compra ahora. Últimos lugares. Contáctame por DM.",
        query_origin="ecoaldea México invertir participar dudas",
    )
    assessment = assess_conversation_quality(result)
    assert assessment.status == "insufficient"
    assert "promotional_language" in assessment.negative_signals


def test_short_contextless_mention_is_insufficient() -> None:
    result = DiscoveryResult(
        source="reddit",
        external_id="quality-003",
        conversation_url="https://example.com/quality-003",
        text="Me gustan las ecoaldeas.",
    )
    assessment = assess_conversation_quality(result)
    assert assessment.status == "insufficient"
    assert "thin_content" in assessment.negative_signals
    assert "context" in assessment.missing_fields
