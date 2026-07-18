import json
from pathlib import Path

import pytest

from app.discovery.scanning_matrix import load_conversational_scanning_matrix


def test_scanning_matrix_v1_loads() -> None:
    matrix = load_conversational_scanning_matrix("config/conversational_scanning_matrix.v1.json")
    assert matrix.client == "Inlak'ech"
    assert matrix.territorial_center == "Chichen Itza, Yucatan, Mexico"
    assert len(matrix.source_families) == 10
    assert [source.priority for source in matrix.source_families] == list(range(1, 11))
    assert matrix.source_families[0].name == "Reddit"
    assert matrix.source_families[1].name == "YouTube comments and replies"
    assert "affinity" in matrix.mandatory_dimensions
    assert "intent" in matrix.mandatory_dimensions
    assert "human_review" in matrix.mandatory_dimensions


def test_duplicate_source_priority_is_rejected(tmp_path: Path) -> None:
    raw = json.loads(Path("config/conversational_scanning_matrix.v1.json").read_text(encoding="utf-8"))
    raw["source_families"][1]["priority"] = raw["source_families"][0]["priority"]
    path = tmp_path / "matrix.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="priorities must be unique"):
        load_conversational_scanning_matrix(path)
