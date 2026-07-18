from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.discovery.conversation_quality import assess_conversation_quality
from app.discovery.ingestion import persist_discovery_results
from app.discovery.last30days_adapter import Last30DaysAdapter, Last30DaysAdapterError
from app.discovery.search_policy import SearchQuery, SearchQueryCatalog
from app.models.conversation import Conversation


class QueryEvaluation(BaseModel):
    query_id: str
    query: str
    language: Literal["es", "en"]
    status: Literal["completed", "failed"]
    total_results: int = 0
    substantive: int = 0
    review: int = 0
    insufficient: int = 0
    substantive_rate: float = Field(ge=0, le=1)
    sources: dict[str, int] = Field(default_factory=dict)
    created_count: int = 0
    persisted_count: int = 0
    recommendation: Literal["KEEP", "REFINE", "REJECT", "ERROR"]
    error: str | None = None


class CorpusEvaluationReport(BaseModel):
    schema_version: Literal["radar-corpus-evaluation/v1"] = "radar-corpus-evaluation/v1"
    client: Literal["Inlak'ech"] = "Inlak'ech"
    query_count: int
    completed_count: int
    failed_count: int
    total_results: int
    total_substantive: int
    total_review: int
    total_insufficient: int
    evaluations: list[QueryEvaluation]


def _recommendation(total: int, substantive: int, review: int) -> Literal["KEEP", "REFINE", "REJECT"]:
    if total == 0:
        return "REJECT"
    substantive_rate = substantive / total
    if substantive >= 2 and substantive_rate >= 0.35:
        return "KEEP"
    if substantive > 0 or review > 0:
        return "REFINE"
    return "REJECT"


def evaluate_query(
    query: SearchQuery,
    *,
    adapter: Last30DaysAdapter,
    runs_root: str | Path,
    db: Session | None = None,
    search_sources: list[str] | None = None,
    quick: bool = True,
) -> QueryEvaluation:
    run_dir = Path(runs_root) / query.id
    run_dir.mkdir(parents=True, exist_ok=True)

    try:
        search_result = adapter.search(
            query.query,
            save_dir=run_dir,
            search_sources=search_sources,
            quick=quick,
        )
    except Last30DaysAdapterError as exc:
        return QueryEvaluation(
            query_id=query.id,
            query=query.query,
            language=query.language,
            status="failed",
            substantive_rate=0,
            recommendation="ERROR",
            error=str(exc),
        )

    counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    for result in search_result.conversations:
        assessment = assess_conversation_quality(result)
        counts[assessment.status] += 1
        source_counts[result.source] += 1

    persisted_count = 0
    created_count = 0
    if db is not None:
        before_count = db.scalar(select(func.count()).select_from(Conversation)) or 0
        persisted = persist_discovery_results(db, search_result.conversations)
        after_count = db.scalar(select(func.count()).select_from(Conversation)) or 0
        persisted_count = len(persisted)
        created_count = max(0, after_count - before_count)

    total = len(search_result.conversations)
    substantive = counts["substantive"]
    review = counts["review"]
    insufficient = counts["insufficient"]

    return QueryEvaluation(
        query_id=query.id,
        query=query.query,
        language=query.language,
        status="completed",
        total_results=total,
        substantive=substantive,
        review=review,
        insufficient=insufficient,
        substantive_rate=(substantive / total) if total else 0,
        sources=dict(sorted(source_counts.items())),
        created_count=created_count,
        persisted_count=persisted_count,
        recommendation=_recommendation(total, substantive, review),
    )


def run_catalog_evaluation(
    catalog: SearchQueryCatalog,
    *,
    adapter: Last30DaysAdapter,
    runs_root: str | Path,
    db: Session | None = None,
    search_sources: list[str] | None = None,
    quick: bool = True,
) -> CorpusEvaluationReport:
    evaluations = [
        evaluate_query(
            query,
            adapter=adapter,
            runs_root=runs_root,
            db=db,
            search_sources=search_sources,
            quick=quick,
        )
        for query in catalog.queries
    ]
    return CorpusEvaluationReport(
        query_count=len(evaluations),
        completed_count=sum(item.status == "completed" for item in evaluations),
        failed_count=sum(item.status == "failed" for item in evaluations),
        total_results=sum(item.total_results for item in evaluations),
        total_substantive=sum(item.substantive for item in evaluations),
        total_review=sum(item.review for item in evaluations),
        total_insufficient=sum(item.insufficient for item in evaluations),
        evaluations=evaluations,
    )
