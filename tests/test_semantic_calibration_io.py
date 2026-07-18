from pathlib import Path

from app.schemas.assessment import AssessmentResult, DecisionStage, DeclaredCapacity, FalsePositiveRisk, ReviewAction
from app.semantics.calibration import run_semantic_calibration
from app.semantics.calibration_io import load_calibration_corpus


def _prediction(_: str) -> AssessmentResult:
    return AssessmentResult(
        thematic_affinity=80,
        values_affinity=80,
        intent_score=80,
        declared_capacity=DeclaredCapacity.UNKNOWN,
        decision_stage=DecisionStage.ACTIVE_EVALUATION,
        evidence_quality=80,
        false_positive_risk=FalsePositiveRisk.LOW,
        review_priority=80,
        recommended_action=ReviewAction.APPROACH_REVIEW,
    )


def test_repository_calibration_corpus_loads_as_draft() -> None:
    corpus = load_calibration_corpus(
        Path("config/semantic_calibration_corpus.v1.json")
    )

    assert corpus.status == "DRAFT"
    assert corpus.human_validated is False
    assert len(corpus.cases) == 4


def test_draft_corpus_cannot_mark_radar_ready_for_pilot() -> None:
    corpus = load_calibration_corpus(
        Path("config/semantic_calibration_corpus.v1.json")
    )
    report = run_semantic_calibration(
        corpus.cases,
        runner=_prediction,
        corpus_human_validated=corpus.human_validated,
    )

    assert report.corpus_human_validated is False
    assert report.ready_for_pilot is False
