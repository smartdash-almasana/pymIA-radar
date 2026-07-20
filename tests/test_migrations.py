from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text

from scripts.verify_alembic_baseline import verify_existing_schema


BASELINE = "20260719_0001"
ASSESSMENT_V3 = "20260719_0002"
HEAD = "20260719_0003"


def _config(database_path: Path) -> Config:
    config = Config("alembic.ini")
    config.set_main_option(
        "sqlalchemy.url",
        f"sqlite+pysqlite:///{database_path.as_posix()}",
    )
    return config


def _tables(database_path: Path) -> set[str]:
    engine = create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}")
    try:
        return set(inspect(engine).get_table_names())
    finally:
        engine.dispose()


def _columns(database_path: Path, table_name: str) -> set[str]:
    engine = create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}")
    try:
        return {item["name"] for item in inspect(engine).get_columns(table_name)}
    finally:
        engine.dispose()


def test_fresh_database_upgrades_to_v3(tmp_path: Path) -> None:
    database_path = tmp_path / "fresh.db"
    command.upgrade(_config(database_path), "head")
    tables = _tables(database_path)
    assert "conversations" in tables
    assert "semantic_assessments_v2" in tables
    assert "conversation_assessments_v3" in tables
    assert "discovery_candidates" in tables
    assert "discovery_outcomes" in tables
    assert "alembic_version" in tables


def test_existing_baseline_database_upgrades_without_recreation(tmp_path: Path) -> None:
    database_path = tmp_path / "baseline.db"
    config = _config(database_path)
    command.upgrade(config, BASELINE)
    before = _tables(database_path)
    assert "conversations" in before
    assert "conversation_assessments_v3" not in before

    command.upgrade(config, HEAD)
    after = _tables(database_path)
    assert before.issubset(after)
    assert "conversation_assessments_v3" in after
    assert "discovery_candidates" in after
    assert "discovery_outcomes" in after
    assert "discovery_candidate_id" in _columns(database_path, "engagement_events")
    assert {
        "discovery_candidate_id",
        "discovery_outcome_id",
    }.issubset(_columns(database_path, "qualification_records"))


def test_v3_revision_downgrade_preserves_baseline_tables(tmp_path: Path) -> None:
    database_path = tmp_path / "downgrade.db"
    config = _config(database_path)
    command.upgrade(config, HEAD)
    command.downgrade(config, BASELINE)
    tables = _tables(database_path)
    assert "conversation_assessments_v3" not in tables
    assert "conversations" in tables
    assert "semantic_assessments_v2" in tables


def test_discovery_revision_downgrade_preserves_assessment_v3(tmp_path: Path) -> None:
    database_path = tmp_path / "discovery-downgrade.db"
    config = _config(database_path)
    command.upgrade(config, HEAD)
    command.downgrade(config, ASSESSMENT_V3)
    tables = _tables(database_path)
    assert "conversation_assessments_v3" in tables
    assert "discovery_candidates" not in tables
    assert "discovery_outcomes" not in tables
    assert "discovery_candidate_id" not in _columns(database_path, "engagement_events")
    assert "discovery_candidate_id" not in _columns(database_path, "qualification_records")
    assert "discovery_outcome_id" not in _columns(database_path, "qualification_records")


def test_existing_unversioned_schema_can_be_verified_before_stamp(tmp_path: Path) -> None:
    database_path = tmp_path / "unversioned-baseline.db"
    config = _config(database_path)
    command.upgrade(config, BASELINE)
    engine = create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}")
    try:
        with engine.begin() as connection:
            connection.execute(text("DROP TABLE alembic_version"))
    finally:
        engine.dispose()

    result = verify_existing_schema(
        f"sqlite+pysqlite:///{database_path.as_posix()}"
    )
    assert result.status == "BASELINE_MATCH"
    assert result.safe_to_stamp_baseline is True


def test_baseline_verification_rejects_missing_schema(tmp_path: Path) -> None:
    database_path = tmp_path / "empty.db"
    create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}").dispose()
    result = verify_existing_schema(
        f"sqlite+pysqlite:///{database_path.as_posix()}"
    )
    assert result.status == "BASELINE_MISMATCH"
    assert result.safe_to_stamp_baseline is False
    assert "conversations" in result.missing_tables
