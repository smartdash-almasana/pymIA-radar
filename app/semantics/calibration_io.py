from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from app.semantics.calibration import HumanAssessmentLabel


class CalibrationCorpus(BaseModel):
    schema_version: Literal["radar-semantic-calibration-corpus/v1"] = (
        "radar-semantic-calibration-corpus/v1"
    )
    status: Literal["DRAFT", "HUMAN_VALIDATED"] = "DRAFT"
    reviewed_by: str | None = None
    review_notes: str | None = None
    cases: list[HumanAssessmentLabel] = Field(default_factory=list)

    @property
    def human_validated(self) -> bool:
        return self.status == "HUMAN_VALIDATED" and bool(self.reviewed_by)


def load_calibration_corpus(path: str | Path) -> CalibrationCorpus:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return CalibrationCorpus.model_validate(payload)


def write_calibration_corpus(path: str | Path, corpus: CalibrationCorpus) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        corpus.model_dump_json(indent=2),
        encoding="utf-8",
    )
