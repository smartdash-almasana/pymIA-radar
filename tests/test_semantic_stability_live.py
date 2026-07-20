import os
from pathlib import Path
import sys

import pytest

from scripts.run_semantic_stability_probe import main


LIVE_FLAG = Path("data/run-live-probe.txt")
LIVE_TESTS_ENABLED = os.getenv("RADAR_RUN_LIVE_LLM_TESTS") == "1"

pytestmark = pytest.mark.skipif(
    not (LIVE_FLAG.exists() and LIVE_TESTS_ENABLED),
    reason="live semantic stability probe requires data/run-live-probe.txt and RADAR_RUN_LIVE_LLM_TESTS=1",
)


def test_live_semantic_stability_probe(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["run_semantic_stability_probe.py"])
    assert main() == 0
