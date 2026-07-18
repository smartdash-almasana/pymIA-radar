from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.discovery.contracts import DiscoveryResult
from app.discovery.corpus_runner import _recommendation, run_catalog_evaluation
from app.discovery.last30days_contracts import (
    Last30DaysAgentExport,
    Last30DaysExecutionTrace,
    Last30DaysSearchResult,
)
from app.discovery.search_policy import SearchQuery, SearchQueryCatalog


class FakeAdapter:
    def __init__(self, by_query: dict[str, list[DiscoveryResult]]) -> None:
        self.by_query = by_query

    def search(self, query: str, **_: object) -> Last30DaysSearchResult:
        conversations = self.by_query.get(query, [])
        export = Last30DaysAgentExport.model_validate(
            {
                "schema_version": "1.2",
                "query": query,
                "generated_at": datetime.now(UTC).isoformat(),
                "window_days": 30,
                "source_status": {},
                "freshness_verdicts": [],
                "clusters": [],
                "results": [],
            }
        )
        return Last30DaysSearchResult(
            export=export,
            conversations=conversations,
            trace=Last30DaysExecutionTrace(
                command=["python", "last30days.py", query],
                return_code=0,
                stderr="",
                duration_seconds=0.1,
            ),
        )


def _result(identifier: str, text: str) -> DiscoveryResult:
    return DiscoveryResult(
        source="reddit",
        external_id=identifier,
        conversation_url=f"https://example.com/{identifier}",
        title="Investment discussion",
        text=text,
        context="Public discussion with several replies",
        published_at=datetime.now(UTC),
        query_origin="query",
    )


def test_recommendation_rules() -> None:
    assert _recommendation(0, 0, 0) == "REJECT"
    assert _recommendation(5, 2, 0) == "KEEP"
    assert _recommendation(5, 1, 1) == "REFINE"
    assert _recommendation(3, 0, 0) == "REJECT"


def test_run_catalog_evaluation_aggregates_quality(tmp_path: Path) -> None:
    catalog = SearchQueryCatalog(
        schema_version="radar-search-queries/v1",
        client="Inlak'ech",
        queries=[
            SearchQuery(id="Q001", language="es", query="consulta regenerativa uno"),
            SearchQuery(id="Q002", language="en", query="regenerative query two"),
        ],
    )
    substantive_text = (
        "Estoy evaluando invertir y participar en un proyecto de largo plazo. "
        "¿Cómo funciona la gobernanza, la propiedad y la seguridad jurídica? "
        "Tengo presupuesto y quiero comparar alternativas antes de contactar al equipo. "
    ) * 2
    adapter = FakeAdapter(
        {
            "consulta regenerativa uno": [
                _result("a", substantive_text),
                _result("b", "Interesante."),
            ],
            "regenerative query two": [],
        }
    )

    report = run_catalog_evaluation(catalog, adapter=adapter, runs_root=tmp_path)

    assert report.query_count == 2
    assert report.completed_count == 2
    assert report.failed_count == 0
    assert report.total_results == 2
    assert report.total_substantive == 1
    assert report.total_insufficient == 1
    assert report.evaluations[0].recommendation == "REFINE"
    assert report.evaluations[1].recommendation == "REJECT"
