import sys
from pathlib import Path

from scripts.run_local import (
    DEFAULT_DATABASE,
    DEFAULT_LAST30DAYS,
    build_commands,
    build_local_environment,
)


def test_local_environment_defaults_to_repo_sqlite_and_bundled_last30days(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("LAST30DAYS_PATH", raising=False)

    environment = build_local_environment()

    assert environment["DATABASE_URL"] == (
        f"sqlite+pysqlite:///{DEFAULT_DATABASE.as_posix()}"
    )
    assert Path(environment["LAST30DAYS_PATH"]) == DEFAULT_LAST30DAYS
    assert DEFAULT_LAST30DAYS.is_dir()


def test_local_runtime_applies_migrations_before_starting_server() -> None:
    migration, server = build_commands(host="127.0.0.1", port=8000, reload=True)

    assert migration == [sys.executable, "-m", "alembic", "upgrade", "head"]
    assert server[:4] == [sys.executable, "-m", "uvicorn", "app.main:app"]
    assert server[-1] == "--reload"
