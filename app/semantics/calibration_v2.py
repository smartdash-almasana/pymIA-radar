from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.schemas.assessment_v3 import (
    AffinityDomain,
    ApparentAffinity,
    ApparentIntention,
    ConversationAssessmentV3Result,
    ReviewActionV3,
    RiskLevelV3,
)
from app.semantics.conversation_assessment_v3 import normalize_literal_text


CORPUS_SCHEMA_VERSION_V2 = "radar-conversation-calibration-corpus/v2"


class HumanConversationAssessmentLabelV2(BaseModel):
    case_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source_conversation_id: int | None = None
    source_url: str | None = None
    expected_real_topic: str = Field(min_length=1)
    expected_contextual_meaning: str = Field(min_length=1)
    expected_apparent_affinity: ApparentAffinity
    expected_affinity_domains: list[AffinityDomain] = Field(default_factory=list)
    expected_apparent_intention: ApparentIntention
    expected_false_positive_risk: RiskLevelV3
    expected_review_action: ReviewActionV3
    required_evidence_fragments: list[str] = Field(default_factory=list)
    forbidden_inferences: list[str] = Field(default_factory=list)
    label_provenance: str = "HUMAN"
    reviewed_by: str | None = None


class ConversationCalibrationCorpusV2(BaseModel):
    schema_version: Literal[CORPUS_SCHEMA_VERSION_V2] = CORPUS_SCHEMA_VERSION_V2
    status: Literal["DRAFT", "HUMAN_VALIDATED"] = "DRAFT"
    reviewed_by: str | None = None
    review_notes: str | None = None
    cases: list[HumanConversationAssessmentLabelV2] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_human_status(self) -> "ConversationCalibrationCorpusV2":
        if self.status == "HUMAN_VALIDATED":
            if not self.reviewed_by:
                raise ValueError("reviewed_by is required for HUMAN_VALIDATED corpus")
            invalid = [
                case.case_id
                for case in self.cases
                if case.label_provenance != "HUMAN_VALIDATED" or not case.reviewed_by
            ]
            if invalid:
                raise ValueError(
                    "all cases must be human validated and reviewed: "
                    + ", ".join(invalid)
                )
        return self

    @property
    def human_validated(self) -> bool:
        return self.status == "HUMAN_VALIDATED" and bool(self.reviewed_by)


class ConversationCalibrationCaseResultV2(BaseModel):
    case_id: str
    affinity_match: bool
    intention_match: bool
    review_action_match: bool
    evidence_valid: bool
    false_positive: bool
    human_review_expected: bool
    human_review_recalled: bool
    forbidden_inference_count: int = Field(ge=0)


class ConversationCalibrationReportV2(BaseModel):
    schema_version: Literal["radar-conversation-calibration-report/v2"] = (
        "radar-conversation-calibration-report/v2"
    )
    corpus_human_validated: bool
    case_count: int = Field(ge=1)
    affinity_class_accuracy: float = Field(ge=0, le=1)
    intent_class_accuracy: float = Field(ge=0, le=1)
    false_positive_rate: float = Field(ge=0, le=1)
    evidence_validity_rate: float = Field(ge=0, le=1)
    human_review_recall: float = Field(ge=0, le=1)
    forbidden_inference_rate: float = Field(ge=0, le=1)
    ready_for_pilot: bool
    cases: list[ConversationCalibrationCaseResultV2]


AssessmentRunnerV2 = Callable[[str], ConversationAssessmentV3Result]


def _required_evidence_is_present(
    required: Iterable[str], predicted: Iterable[str]
) -> bool:
    predicted_normalized = {
        normalize_literal_text(fragment) for fragment in predicted if fragment
    }
    return all(
        normalize_literal_text(fragment) in predicted_normalized for fragment in required
    )


def evaluate_calibration_case_v2(
    label: HumanConversationAssessmentLabelV2,
    prediction: ConversationAssessmentV3Result,
) -> ConversationCalibrationCaseResultV2:
    payload_keys = set(prediction.model_dump(mode="json"))
    forbidden_count = sum(item in payload_keys for item in label.forbidden_inferences)
    expected_review = label.expected_review_action == ReviewActionV3.REVIEW
    predicted_review = prediction.recommended_review_action == ReviewActionV3.REVIEW
    false_positive = (
        label.expected_apparent_affinity == ApparentAffinity.NONE
        and prediction.apparent_affinity not in {None, ApparentAffinity.NONE}
    )
    return ConversationCalibrationCaseResultV2(
        case_id=label.case_id,
        affinity_match=(
            prediction.apparent_affinity == label.expected_apparent_affinity
        ),
        intention_match=(
            prediction.apparent_intention == label.expected_apparent_intention
        ),
        review_action_match=(
            prediction.recommended_review_action == label.expected_review_action
        ),
        evidence_valid=_required_evidence_is_present(
            label.required_evidence_fragments, prediction.evidence_fragments
        ),
        false_positive=false_positive,
        human_review_expected=expected_review,
        human_review_recalled=(not expected_review or predicted_review),
        forbidden_inference_count=forbidden_count,
    )


def run_conversation_calibration_v2(
    labels: Iterable[HumanConversationAssessmentLabelV2],
    *,
    runner: AssessmentRunnerV2,
    corpus_human_validated: bool = False,
    minimum_affinity_accuracy: float = 0.80,
    minimum_intent_accuracy: float = 0.80,
    maximum_false_positive_rate: float = 0.15,
) -> ConversationCalibrationReportV2:
    materialized = list(labels)
    if not materialized:
        raise ValueError("At least one V2 calibration case is required")
    cases = [evaluate_calibration_case_v2(label, runner(label.text)) for label in materialized]
    count = len(cases)
    expected_review_count = sum(item.human_review_expected for item in cases)
    human_review_recall = (
        sum(item.human_review_recalled and item.human_review_expected for item in cases)
        / expected_review_count
        if expected_review_count
        else 1.0
    )
    forbidden_total = sum(item.forbidden_inference_count for item in cases)
    forbidden_denominator = sum(
        max(1, len(label.forbidden_inferences)) for label in materialized
    )
    affinity_accuracy = sum(item.affinity_match for item in cases) / count
    intent_accuracy = sum(item.intention_match for item in cases) / count
    false_positive_rate = sum(item.false_positive for item in cases) / count
    evidence_rate = sum(item.evidence_valid for item in cases) / count
    forbidden_rate = forbidden_total / forbidden_denominator
    return ConversationCalibrationReportV2(
        corpus_human_validated=corpus_human_validated,
        case_count=count,
        affinity_class_accuracy=affinity_accuracy,
        intent_class_accuracy=intent_accuracy,
        false_positive_rate=false_positive_rate,
        evidence_validity_rate=evidence_rate,
        human_review_recall=human_review_recall,
        forbidden_inference_rate=forbidden_rate,
        ready_for_pilot=(
            corpus_human_validated
            and affinity_accuracy >= minimum_affinity_accuracy
            and intent_accuracy >= minimum_intent_accuracy
            and false_positive_rate <= maximum_false_positive_rate
            and evidence_rate == 1.0
            and human_review_recall == 1.0
            and forbidden_rate == 0.0
        ),
        cases=cases,
    )


def load_conversation_calibration_corpus_v2(
    path: str | Path,
) -> ConversationCalibrationCorpusV2:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return ConversationCalibrationCorpusV2.model_validate(payload)


def write_conversation_calibration_corpus_v2(
    path: str | Path,
    corpus: ConversationCalibrationCorpusV2,
) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(corpus.model_dump_json(indent=2), encoding="utf-8")
