from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


AccessMode = Literal[
    "PUBLIC_AUTOMATABLE",
    "PUBLIC_ASSISTED",
    "REGISTRATION_REQUIRED",
    "PARTNERSHIP_CHANNEL",
    "PRIVATE_NOT_USABLE",
    "IRRELEVANT",
]
ValueLevel = Literal["PRIORIDAD_1", "PRIORIDAD_2", "PRIORIDAD_3", "OBSERVAR", "DESCARTAR"]


class SourceFamily(BaseModel):
    id: str = Field(pattern=r"^S\d{3}$")
    priority: int = Field(ge=1)
    name: str = Field(min_length=2)
    access_mode: AccessMode
    integration_mode: str = Field(min_length=2)
    value: ValueLevel
    conversation_types: list[str] = Field(min_length=1)
    intent_types: list[str] = Field(min_length=1)
    territorial_terms: list[str] = Field(min_length=1)
    restrictions: list[str] = Field(default_factory=list)


class ConversationalScanningMatrix(BaseModel):
    schema_version: Literal["radar-conversational-scanning-matrix/v1"]
    client: Literal["Inlak'ech"]
    territorial_center: str
    source_families: list[SourceFamily] = Field(min_length=1)
    shared_positive_signals: list[str] = Field(min_length=1)
    shared_exclusion_signals: list[str] = Field(min_length=1)
    mandatory_dimensions: list[str] = Field(min_length=1)


def load_conversational_scanning_matrix(path: str | Path) -> ConversationalScanningMatrix:
    matrix = ConversationalScanningMatrix.model_validate_json(Path(path).read_text(encoding="utf-8"))
    ids = [source.id for source in matrix.source_families]
    priorities = [source.priority for source in matrix.source_families]
    if len(ids) != len(set(ids)):
        raise ValueError("source family ids must be unique")
    if len(priorities) != len(set(priorities)):
        raise ValueError("source family priorities must be unique")
    return matrix
