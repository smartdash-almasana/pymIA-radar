import os
from pathlib import Path

import pytest

from scripts.diagnose_v3_output import main


LIVE_FLAG = Path("data/run-live-probe.txt")
LIVE_TESTS_ENABLED = os.getenv("RADAR_RUN_LIVE_LLM_TESTS") == "1"

pytestmark = pytest.mark.skipif(
    not (LIVE_FLAG.exists() and LIVE_TESTS_ENABLED),
    reason="live semantic diagnostic requires data/run-live-probe.txt and RADAR_RUN_LIVE_LLM_TESTS=1",
)


def test_live_semantic_diagnostic() -> None:
    assert main() == 0
