import json
from pathlib import Path

import pytest

from app.discovery.concrete_sources import load_concrete_source_catalog


def test_concrete_source_catalog_v1_loads() -> None:
    catalog = load_concrete_source_catalog("config/concrete_sources.v1.json")
    assert catalog.client == "Inlak'ech"
    assert catalog.territorial_center == "Chichen Itza, Yucatan, Mexico"
    assert len(catalog.sources) == 15
    assert len({source.id for source in catalog.sources}) == 15
    assert {source.value for source in catalog.sources} >= {"PRIORIDAD_1", "PRIORIDAD_2"}
    assert any(source.access_mode == "PARTNERSHIP_CHANNEL" for source in catalog.sources)
    assert any("learning" in source.intent_types for source in catalog.sources)


def test_duplicate_concrete_source_ids_are_rejected(tmp_path: Path) -> None:
    raw = json.loads(Path("config/concrete_sources.v1.json").read_text(encoding="utf-8"))
    raw["sources"][1]["id"] = raw["sources"][0]["id"]
    path = tmp_path / "sources.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="unique"):
        load_concrete_source_catalog(path)
