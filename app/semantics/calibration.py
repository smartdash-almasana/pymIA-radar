from __future__ import annotations

from collections.abc import Callable, Iterable
from pydantic import BaseModel, Field

from app.schemas.assessment import (
    AssessmentResult,
    DecisionStage,
    ProbableArchetype,
    ReviewAction,
)


class HumanAssessmentLabel(BaseModel):
    case_id: str
    text: str = Field(min_length=1)
    expected_action: ReviewAction
    expected_stage: DecisionStage
    expected_archetype: ProbableArchetype | None = None
    expected_thematic_affinity: int = Field(ge=0, le=100)
    expected_values_affinity: int = Field(ge=0, le=100)
    expected_intent_score: int = Field(ge=0, le=100)


class CalibrationCaseResult(BaseModel):
    case_id: str
    action_match: bool
    stage_match: bool
    archetype_match: bool
    thematic_within_tolerance: bool
    values_within_tolerance: bool
    intent_within_tolerance: bool
    false_positive: bool
    false_negative: bool
    predicted_action: ReviewAction
    expected_action: ReviewAction


class CalibrationReport(BaseModel):
    schema_version: str = "radar-semantic-calibration/v1"
    corpus_human_validated: bool = False
    case_count: int
    action_accuracy: float = Field(ge=0, le=1)
    stage_accuracy: float = Field(ge=0, le=1)
    archetype_accuracy: float = Field(ge=0, le=1)
    score_tolerance_accuracy: float = Field(ge=0, le=1)
    false_positive_rate: float = Field(ge=0, le=1)
    false_negative_rate: float = Field(ge=0, le=1)
    ready_for_pilot: bool
    cases: list[CalibrationCaseResult]


AssessmentRunner = Callable[[str], AssessmentResult]


def _is_positive_action(action: ReviewAction) -> bool:
    return action in {
        ReviewAction.APPROACH_REVIEW,
        ReviewAction.REVIEW_OR_NURTURE,
    }


def evaluate_calibration_case(
    label: HumanAssessmentLabel,
    prediction: AssessmentResult,
    *,
    score_tolerance: int = 20,
) -> CalibrationCaseResult:
    expected_positive = _is_positive_action(label.expected_action)
    predicted_positive = _is_positive_action(prediction.recommended_action)

    return CalibrationCaseResult(
        case_id=label.case_id,
        action_match=prediction.recommended_action == label.expected_action,
        stage_match=prediction.decision_stage == label.expected_stage,
        archetype_match=prediction.probable_archetype == label.expected_archetype,
        thematic_within_tolerance=(
            abs(prediction.thematic_affinity - label.expected_thematic_affinity)
            <= score_tolerance
        ),
        values_within_tolerance=(
            abs(prediction.values_affinity - label.expected_values_affinity)
            <= score_tolerance
        ),
        intent_within_tolerance=(
            abs(prediction.intent_score - label.expected_intent_score)
            <= score_tolerance
        ),
        false_positive=predicted_positive and not expected_positive,
        false_negative=expected_positive and not predicted_positive,
        predicted_action=prediction.recommended_action,
        expected_action=label.expected_action,
    )


def run_semantic_calibration(
    labels: Iterable[HumanAssessmentLabel],
    *,
    runner: AssessmentRunner,
    score_tolerance: int = 20,
    minimum_action_accuracy: float = 0.80,
    maximum_false_positive_rate: float = 0.15,
    corpus_human_validated: bool = False,
) -> CalibrationReport:
    materialized = list(labels)
    if not materialized:
        raise ValueError("At least one human-labeled case is required")

    cases = [
        evaluate_calibration_case(
            label,
            runner(label.text),
            score_tolerance=score_tolerance,
        )
        for label in materialized
    ]
    case_count = len(cases)
    score_checks = sum(
        item.thematic_within_tolerance
        + item.values_within_tolerance
        + item.intent_within_tolerance
        for item in cases
    )

    action_accuracy = sum(item.action_match for item in cases) / case_count
    false_positive_rate = sum(item.false_positive for item in cases) / case_count
    false_negative_rate = sum(item.false_negative for item in cases) / case_count

    return CalibrationReport(
        corpus_human_validated=corpus_human_validated,
        case_count=case_count,
        action_accuracy=action_accuracy,
        stage_accuracy=sum(item.stage_match for item in cases) / case_count,
        archetype_accuracy=sum(item.archetype_match for item in cases) / case_count,
        score_tolerance_accuracy=score_checks / (case_count * 3),
        false_positive_rate=false_positive_rate,
        false_negative_rate=false_negative_rate,
        ready_for_pilot=(
            corpus_human_validated
            and action_accuracy >= minimum_action_accuracy
            and false_positive_rate <= maximum_false_positive_rate
        ),
        cases=cases,
    )
