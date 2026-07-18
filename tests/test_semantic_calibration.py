import pytest

from app.schemas.assessment import (
    AssessmentResult,
    DecisionStage,
    DeclaredCapacity,
    FalsePositiveRisk,
    ReviewAction,
)
from app.semantics.calibration import (
    HumanAssessmentLabel,
    run_semantic_calibration,
)


def _prediction(
    *,
    action: ReviewAction,
    stage: DecisionStage,
    thematic: int,
    values: int,
    intent: int,
) -> AssessmentResult:
    return AssessmentResult(
        thematic_affinity=thematic,
        values_affinity=values,
        intent_score=intent,
        declared_capacity=DeclaredCapacity.UNKNOWN,
        decision_stage=stage,
        evidence_quality=80,
        false_positive_risk=FalsePositiveRisk.LOW,
        review_priority=75,
        recommended_action=action,
    )


def test_calibration_report_marks_ready_when_thresholds_pass() -> None:
    labels = [
        HumanAssessmentLabel(
            case_id="positive",
            text="Estoy evaluando participar en una comunidad regenerativa.",
            expected_action=ReviewAction.REVIEW_OR_NURTURE,
            expected_stage=DecisionStage.ACTIVE_EVALUATION,
            expected_thematic_affinity=80,
            expected_values_affinity=80,
            expected_intent_score=70,
        ),
        HumanAssessmentLabel(
            case_id="negative",
            text="Necesito información turística general.",
            expected_action=ReviewAction.DISCARD,
            expected_stage=DecisionStage.DISCOVERY,
            expected_thematic_affinity=10,
            expected_values_affinity=5,
            expected_intent_score=5,
        ),
    ]
    predictions = {
        labels[0].text: _prediction(
            action=ReviewAction.REVIEW_OR_NURTURE,
            stage=DecisionStage.ACTIVE_EVALUATION,
            thematic=75,
            values=70,
            intent=65,
        ),
        labels[1].text: _prediction(
            action=ReviewAction.DISCARD,
            stage=DecisionStage.DISCOVERY,
            thematic=10,
            values=0,
            intent=0,
        ),
    }

    report = run_semantic_calibration(labels, runner=predictions.__getitem__)

    assert report.case_count == 2
    assert report.action_accuracy == 1
    assert report.false_positive_rate == 0
    assert report.score_tolerance_accuracy == 1
    assert report.ready_for_pilot is True


def test_calibration_report_detects_false_positive() -> None:
    label = HumanAssessmentLabel(
        case_id="noise",
        text="Artículo académico sin intención personal.",
        expected_action=ReviewAction.DISCARD,
        expected_stage=DecisionStage.DISCOVERY,
        expected_thematic_affinity=20,
        expected_values_affinity=20,
        expected_intent_score=0,
    )

    report = run_semantic_calibration(
        [label],
        runner=lambda _: _prediction(
            action=ReviewAction.APPROACH_REVIEW,
            stage=DecisionStage.ACTIVE_EVALUATION,
            thematic=90,
            values=90,
            intent=90,
        ),
    )

    assert report.false_positive_rate == 1
    assert report.ready_for_pilot is False
    assert report.cases[0].false_positive is True


def test_calibration_requires_human_labeled_cases() -> None:
    with pytest.raises(ValueError, match="At least one"):
        run_semantic_calibration([], runner=lambda _: None)  # type: ignore[arg-type]
