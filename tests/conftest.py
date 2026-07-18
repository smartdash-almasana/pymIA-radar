import os
from pathlib import Path

TEST_DB_PATH = Path(__file__).parents[1] / ".pytest_cache" / "inlakech_radar.db"
TEST_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

os.environ.setdefault(
    "DATABASE_URL",
    f"sqlite+pysqlite:///{TEST_DB_PATH.as_posix()}",
)
