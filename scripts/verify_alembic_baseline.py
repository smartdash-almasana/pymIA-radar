from __future__ import annotations

import argparse
from dataclasses import dataclass

from sqlalchemy import create_engine, inspect

from app.core.config import settings


EXPECTED_BASELINE_TABLES = {
    "conversations",
    "semantic_assessments",
    "semantic_assessments_v2",
    "review_decisions",
    "engagement_events",
    "qualification_records",
}
V3_TABLE = "conversation_assessments_v3"


@dataclass(frozen=True)
class BaselineVerification:
    status: str
    missing_tables: tuple[str, ...]
    unexpected_v3_present: bool
    alembic_version_present: bool

    @property
    def safe_to_stamp_baseline(self) -> bool:
        return (
            self.status == "BASELINE_MATCH"
            and not self.missing_tables
            and not self.unexpected_v3_present
            and not self.alembic_version_present
        )


def verify_existing_schema(database_url: str) -> BaselineVerification:
    engine = create_engine(database_url, future=True)
    try:
        tables = set(inspect(engine).get_table_names())
    finally:
        engine.dispose()

    missing = tuple(sorted(EXPECTED_BASELINE_TABLES - tables))
    v3_present = V3_TABLE in tables
    version_present = "alembic_version" in tables

    if missing:
        status = "BASELINE_MISMATCH"
    elif v3_present or version_present:
        status = "ALREADY_VERSIONED_OR_V3_PRESENT"
    else:
        status = "BASELINE_MATCH"

    return BaselineVerification(
        status=status,
        missing_tables=missing,
        unexpected_v3_present=v3_present,
        alembic_version_present=version_present,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify an existing RADAR database before stamping the Alembic baseline."
    )
    parser.add_argument("--database-url", default=settings.database_url)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = verify_existing_schema(args.database_url)
    print(f"STATUS={result.status}")
    print(f"SAFE_TO_STAMP_BASELINE={str(result.safe_to_stamp_baseline).lower()}")
    print("MISSING_TABLES=" + ",".join(result.missing_tables))
    print(f"V3_PRESENT={str(result.unexpected_v3_present).lower()}")
    print(f"ALEMBIC_VERSION_PRESENT={str(result.alembic_version_present).lower()}")
    return 0 if result.safe_to_stamp_baseline else 2


if __name__ == "__main__":
    raise SystemExit(main())
