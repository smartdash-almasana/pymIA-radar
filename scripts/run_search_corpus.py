from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.db.session import SessionLocal, init_db
from app.discovery.corpus_runner import run_catalog_evaluation
from app.discovery.last30days_adapter import Last30DaysAdapter
from app.discovery.search_policy import load_search_query_catalog


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run and evaluate the RADAR search query catalog.")
    parser.add_argument("--catalog", default="config/search_queries.v1.json")
    parser.add_argument("--last30days-repo", default="last30days-skill-main")
    parser.add_argument("--python", default="python")
    parser.add_argument("--runs-root", default="data/last30days-runs/corpus-v1")
    parser.add_argument("--report", default="data/last30days-runs/corpus-v1/report.json")
    parser.add_argument("--sources", default="reddit,hackernews,github,polymarket")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--no-quick", action="store_true")
    parser.add_argument("--persist", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    catalog = load_search_query_catalog(args.catalog)
    adapter = Last30DaysAdapter(
        repo_path=args.last30days_repo,
        python_executable=args.python,
        timeout_seconds=args.timeout,
    )
    sources = [item.strip() for item in args.sources.split(",") if item.strip()]

    db = None
    try:
        if args.persist:
            init_db()
            db = SessionLocal()
        report = run_catalog_evaluation(
            catalog,
            adapter=adapter,
            runs_root=args.runs_root,
            db=db,
            search_sources=sources,
            quick=not args.no_quick,
        )
    finally:
        if db is not None:
            db.close()

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(report_path)
    print(
        f"queries={report.query_count} completed={report.completed_count} "
        f"failed={report.failed_count} results={report.total_results} "
        f"substantive={report.total_substantive} review={report.total_review} "
        f"insufficient={report.total_insufficient}"
    )
    return 1 if report.failed_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
