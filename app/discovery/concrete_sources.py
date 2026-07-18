from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


AccessMode = Literal[
    "PUBLIC_AUTOMATABLE",
    "PUBLIC_ASSISTED",
    "REGISTRATION_REQUIRED",
    "PARTNERSHIP_CHANNEL",
    "PRIVATE_NOT_USABLE",
]
ValueClass = Literal["PRIORIDAD_1", "PRIORIDAD_2", "PRIORIDAD_3", "OBSERVAR", "DESCARTAR"]


class ConcreteSource(BaseModel):
    id: str = Field(pattern=r"^C\d{3}$")
    name: str = Field(min_length=2)
    url: HttpUrl
    family_id: str = Field(pattern=r"^S\d{3}$")
    scope: str = Field(min_length=2)
    languages: list[str] = Field(min_length=1)
    themes: list[str] = Field(min_length=1)
    intent_types: list[str] = Field(min_length=1)
    access_mode: AccessMode
    integration_mode: str = Field(min_length=2)
    value: ValueClass
    evidence_status: str = Field(min_length=2)
    notes: str = Field(min_length=2)


class ConcreteSourceCatalog(BaseModel):
    schema_version: Literal["radar-concrete-sources/v1"]
    client: Literal["Inlak'ech"]
    territorial_center: Literal["Chichen Itza, Yucatan, Mexico"]
    sources: list[ConcreteSource] = Field(min_length=1)


def load_concrete_source_catalog(path: str | Path) -> ConcreteSourceCatalog:
    catalog = ConcreteSourceCatalog.model_validate_json(Path(path).read_text(encoding="utf-8"))
    ids = [source.id for source in catalog.sources]
    if len(ids) != len(set(ids)):
        raise ValueError("concrete source ids must be unique")
    return catalog
