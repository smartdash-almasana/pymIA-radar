from app.schemas.assessment import (
    DecisionStage,
    DeclaredCapacity,
    FalsePositiveRisk,
    ProbableArchetype,
    ReviewAction,
)
from app.semantics.llm_classifier import (
    LLMAssessmentDraft,
    assess_with_optional_llm,
    finalize_llm_draft,
)


def _draft() -> LLMAssessmentDraft:
    return LLMAssessmentDraft(
        thematic_affinity=90,
        values_affinity=80,
        intent_score=70,
        declared_capacity=DeclaredCapacity.UNKNOWN,
        decision_stage=DecisionStage.ACTIVE_EVALUATION,
        evidence_quality=80,
        false_positive_risk=FalsePositiveRisk.LOW,
        probable_archetype=ProbableArchetype.PATIENT_SOWER,
        archetype_confidence=75,
        archetype_evidence=["largo plazo"],
        positive_signals=["comunidad regenerativa", "evaluando invertir"],
        negative_signals=[],
        objections=["seguridad jurídica"],
        missing_information=["declared_capacity"],
        evidence_fragments=["Estoy evaluando invertir en una comunidad regenerativa"],
    )


def test_finalize_llm_draft_recalculates_priority_and_action() -> None:
    result = finalize_llm_draft(_draft())

    assert result.review_priority == 80
    assert result.recommended_action == ReviewAction.APPROACH_REVIEW
    assert result.human_review_required is True
    assert result.provisional is True


def test_optional_llm_uses_injected_runner_without_external_call() -> None:
    calls: list[str] = []

    def runner(text: str) -> LLMAssessmentDraft:
        calls.append(text)
        return _draft()

    result = assess_with_optional_llm(
        "Conversación real",
        enabled=True,
        model_name="openai:test-model",
        runner=runner,
    )

    assert calls == ["Conversación real"]
    assert result.intent_score == 70
    assert result.recommended_action == ReviewAction.APPROACH_REVIEW


def test_optional_llm_falls_back_when_disabled() -> None:
    result = assess_with_optional_llm(
        "Busco una comunidad regenerativa para invertir a largo plazo.",
        enabled=False,
        model_name="openai:test-model",
    )

    assert result.provisional is True
    assert result.human_review_required is True


def test_optional_llm_falls_back_when_runner_fails() -> None:
    def broken_runner(_: str) -> LLMAssessmentDraft:
        raise RuntimeError("provider unavailable")

    result = assess_with_optional_llm(
        "Busco una comunidad regenerativa para invertir a largo plazo.",
        enabled=True,
        model_name="openai:test-model",
        runner=broken_runner,
    )

    assert result.provisional is True
    assert result.human_review_required is True
    assert result.declared_capacity == DeclaredCapacity.UNKNOWN
