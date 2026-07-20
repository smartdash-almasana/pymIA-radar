from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = REPO_ROOT / "data" / "radar-local.db"
DEFAULT_LAST30DAYS = REPO_ROOT / "last30days-skill-main"


def build_local_environment() -> dict[str, str]:
    DEFAULT_DATABASE.parent.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment.setdefault(
        "DATABASE_URL",
        f"sqlite+pysqlite:///{DEFAULT_DATABASE.as_posix()}",
    )
    environment.setdefault("LAST30DAYS_PATH", str(DEFAULT_LAST30DAYS))
    return environment


def build_commands(*, host: str, port: int, reload: bool) -> list[list[str]]:
    server = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        host,
        "--port",
        str(port),
    ]
    if reload:
        server.append("--reload")
    return [
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        server,
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Start Inlak'ech RADAR locally.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    environment = build_local_environment()
    migration_command, server_command = build_commands(
        host=args.host,
        port=args.port,
        reload=args.reload,
    )

    print(f"RADAR database: {environment['DATABASE_URL']}")
    print(f"last30days: {environment['LAST30DAYS_PATH']}")
    subprocess.run(
        migration_command,
        cwd=REPO_ROOT,
        env=environment,
        check=True,
    )
    print(f"RADAR: http://{args.host}:{args.port}")
    return subprocess.run(
        server_command,
        cwd=REPO_ROOT,
        env=environment,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
