import os
from pathlib import Path

TEST_DB_PATH = Path(__file__).parents[1] / ".pytest_cache" / "inlakech_radar.db"
TEST_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# This database is a disposable pytest artifact. Recreate it for every test
# session so Base.metadata.create_all() always builds the current test schema.
if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()

os.environ.setdefault(
    "DATABASE_URL",
    f"sqlite+pysqlite:///{TEST_DB_PATH.as_posix()}",
)
