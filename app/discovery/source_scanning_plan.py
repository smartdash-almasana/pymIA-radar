from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from app.discovery.concrete_sources import ConcreteSourceCatalog

PlanStatus = Literal[
    "ACTIVE",
    "ASSISTED",
    "CONFIG_REQUIRED",
    "DISCOVERY_REQUIRED",
    "INSTITUTIONAL",
    "DEFERRED",
]


class SourceScanningPlan(BaseModel):
    id: str = Field(pattern=r"^P\d{3}$")
    source_id: str = Field(pattern=r"^C\d{3}$")
    status: PlanStatus
    frequency: str = Field(min_length=2)
    capture_mode: str = Field(min_length=2)
    queries: list[str] = Field(min_length=1)
    required_fields: list[str] = Field(min_length=1)
    metrics: list[str] = Field(min_length=1)
    requirements: list[str] = Field(default_factory=list)
    notes: str = Field(min_length=2)


class SourceScanningPlanCatalog(BaseModel):
    schema_version: Literal["radar-source-scanning-plans/v1"]
    client: Literal["Inlak'ech"]
    territorial_center: Literal["Chichen Itza, Yucatan, Mexico"]
    plans: list[SourceScanningPlan] = Field(min_length=1)


def load_source_scanning_plan_catalog(path: str | Path) -> SourceScanningPlanCatalog:
    catalog = SourceScanningPlanCatalog.model_validate_json(Path(path).read_text(encoding="utf-8"))
    plan_ids = [plan.id for plan in catalog.plans]
    source_ids = [plan.source_id for plan in catalog.plans]
    if len(plan_ids) != len(set(plan_ids)):
        raise ValueError("source scanning plan ids must be unique")
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("each concrete source may have only one active plan definition")
    return catalog


def validate_plan_coverage(
    plans: SourceScanningPlanCatalog,
    sources: ConcreteSourceCatalog,
) -> None:
    planned = {plan.source_id for plan in plans.plans}
    available = {source.id for source in sources.sources}
    unknown = planned - available
    missing = available - planned
    if unknown:
        raise ValueError(f"plans reference unknown concrete sources: {sorted(unknown)}")
    if missing:
        raise ValueError(f"concrete sources without scanning plan: {sorted(missing)}")
