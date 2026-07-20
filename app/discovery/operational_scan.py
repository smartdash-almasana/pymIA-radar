from __future__ import annotations

from collections import Counter
from pathlib import Path
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.discovery.conversation_quality import assess_conversation_quality
from app.discovery.ingestion import persist_discovery_results
from app.discovery.last30days_adapter import Last30DaysAdapter
from app.discovery.search_policy import SearchQuery, load_search_query_catalog
from app.models.conversation import Conversation
from app.schemas.discovery_scan import OperationalScanRequest, OperationalScanResult


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG_PATH = REPO_ROOT / "config" / "search_queries.v2.json"
DEFAULT_RUNS_ROOT = REPO_ROOT / "data" / "last30days-runs" / "operational"
LOCAL_LAST30DAYS_PATH = REPO_ROOT / "last30days-skill-main"


class OperationalScanError(RuntimeError):
    pass


def load_operational_queries() -> list[SearchQuery]:
    return load_search_query_catalog(DEFAULT_CATALOG_PATH).queries


def build_operational_adapter() -> Last30DaysAdapter:
    configured_path = Path(settings.last30days_path)
    repo_path = configured_path if configured_path.exists() else LOCAL_LAST30DAYS_PATH
    return Last30DaysAdapter(repo_path=repo_path)


def run_operational_scan(
    db: Session,
    payload: OperationalScanRequest,
    *,
    adapter: Last30DaysAdapter | None = None,
) -> OperationalScanResult:
    queries = {item.id: item for item in load_operational_queries()}
    query = queries.get(payload.query_id)
    if query is None:
        raise OperationalScanError(f"Unknown operational query: {payload.query_id}")

    active_adapter = adapter or build_operational_adapter()
    run_dir = DEFAULT_RUNS_ROOT / query.id / uuid4().hex
    search_result = active_adapter.search(
        query.query,
        save_dir=run_dir,
        search_sources=payload.sources,
        quick=payload.quick,
    )

    counts: Counter[str] = Counter()
    admitted = []
    for result in search_result.conversations:
        quality = assess_conversation_quality(result)
        counts[quality.status] += 1
        if quality.status == "substantive":
            admitted.append(result)

    existing_count = 0
    for result in admitted:
        existing = db.scalar(
            select(Conversation.id).where(
                Conversation.source == result.source,
                Conversation.external_id == result.external_id,
            )
        )
        if existing is not None:
            existing_count += 1

    persist_discovery_results(db, admitted)
    return OperationalScanResult(
        query_id=query.id,
        query=query.query,
        total_results=len(search_result.conversations),
        substantive_results=counts["substantive"],
        review_results=counts["review"],
        insufficient_results=counts["insufficient"],
        admitted_results=len(admitted),
        new_conversations=len(admitted) - existing_count,
        existing_conversations=existing_count,
        duration_seconds=search_result.trace.duration_seconds,
    )
