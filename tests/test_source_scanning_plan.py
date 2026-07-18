import json
from pathlib import Path

import pytest

from app.discovery.concrete_sources import load_concrete_source_catalog
from app.discovery.source_scanning_plan import (
    load_source_scanning_plan_catalog,
    validate_plan_coverage,
)


def test_source_scanning_plan_v1_covers_all_concrete_sources() -> None:
    sources = load_concrete_source_catalog("config/concrete_sources.v1.json")
    plans = load_source_scanning_plan_catalog("config/source_scanning_plans.v1.json")
    validate_plan_coverage(plans, sources)
    assert len(plans.plans) == len(sources.sources) == 15
    assert {plan.status for plan in plans.plans} >= {
        "ACTIVE",
        "ASSISTED",
        "CONFIG_REQUIRED",
        "DISCOVERY_REQUIRED",
        "INSTITUTIONAL",
    }
    assert all(plan.queries for plan in plans.plans)
    assert all("url" in plan.required_fields or "event_url" in plan.required_fields or "video_url" in plan.required_fields or "public_post_url" in plan.required_fields or "organization" in plan.required_fields or "instance_url" in plan.required_fields for plan in plans.plans)


def test_duplicate_source_plan_is_rejected(tmp_path: Path) -> None:
    raw = json.loads(Path("config/source_scanning_plans.v1.json").read_text(encoding="utf-8"))
    raw["plans"][1]["source_id"] = raw["plans"][0]["source_id"]
    path = tmp_path / "plans.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="only one"):
        load_source_scanning_plan_catalog(path)


def test_unknown_source_reference_is_rejected(tmp_path: Path) -> None:
    raw = json.loads(Path("config/source_scanning_plans.v1.json").read_text(encoding="utf-8"))
    raw["plans"][0]["source_id"] = "C999"
    path = tmp_path / "plans.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    plans = load_source_scanning_plan_catalog(path)
    sources = load_concrete_source_catalog("config/concrete_sources.v1.json")
    with pytest.raises(ValueError, match="unknown concrete sources"):
        validate_plan_coverage(plans, sources)
