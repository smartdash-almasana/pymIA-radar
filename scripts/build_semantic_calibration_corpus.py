from __future__ import annotations

import argparse

from app.db.session import SessionLocal, init_db
from app.semantics.calibration_builder import (
    build_seeded_calibration_corpus,
    load_latest_assessment_rows,
)
from app.semantics.calibration_io import write_calibration_corpus


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export persisted RADAR assessments into a draft calibration corpus."
    )
    parser.add_argument(
        "--output",
        default="data/calibration/semantic_calibration_corpus.real.v1.json",
    )
    parser.add_argument("--limit", type=int, default=100)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    init_db()
    with SessionLocal() as db:
        rows = load_latest_assessment_rows(db, limit=args.limit)
    corpus = build_seeded_calibration_corpus(rows)
    write_calibration_corpus(args.output, corpus)
    print(args.output)
    print(f"cases={len(corpus.cases)} status={corpus.status}")
    return 0 if corpus.cases else 2


if __name__ == "__main__":
    raise SystemExit(main())
