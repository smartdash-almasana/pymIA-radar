import os
from pathlib import Path

TEST_DB_PATH = Path(__file__).parent / ".test_inlakech_radar.db"

os.environ.setdefault(
    "DATABASE_URL",
    f"sqlite+pysqlite:///{TEST_DB_PATH.as_posix()}",
)
