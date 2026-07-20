from pathlib import Path

from app.schemas.assessment_v3 import (
    AffinityDomain,
    ApparentAffinity,
    ApparentIntention,
    AssessmentStatusV3,
    ConversationAssessmentV3Result,
    ReviewActionV3,
    RiskLevelV3,
)
from app.semantics.calibration_v2 import (
    HumanConversationAssessmentLabelV2,
    load_conversation_calibration_corpus_v2,
    run_conversation_calibration_v2,
)


def _prediction(text: str) -> ConversationAssessmentV3Result:
    if "Messi" in text:
        return ConversationAssessmentV3Result(
            conversation_id=1,
            assessment_status=AssessmentStatusV3.COMPLETED,
            real_topic="Rivalidad futbolística",
            contextual_meaning="Intercambio social sobre jugadores de fútbol.",
            apparent_affinity=ApparentAffinity.NONE,
            apparent_affinity_domains=[],
            apparent_intention=ApparentIntention.NONE,
            intention_summary="No existe intención relacionada con Inlak'ech.",
            evidence_fragments=[text],
            false_positive_risk=RiskLevelV3.HIGH,
            uncertainty=RiskLevelV3.LOW,
            human_review_reason="Control negativo.",
            review_priority=0,
            recommended_review_action=ReviewActionV3.OBSERVE,
            semantic_engine="llm:test",
            model_name="test",
        )
    return ConversationAssessmentV3Result(
        conversation_id=2,
        assessment_status=AssessmentStatusV3.COMPLETED,
        real_topic="Exploración de comunidad regenerativa",
        contextual_meaning="La persona solicita información concreta.",
        apparent_affinity=ApparentAffinity.CLEAR,
        apparent_affinity_domains=[AffinityDomain.COMMUNITY],
        apparent_intention=ApparentIntention.EXPLORATION,
        intention_summary="Explora una posibilidad de participación.",
        evidence_fragments=[text],
        false_positive_risk=RiskLevelV3.LOW,
        uncertainty=RiskLevelV3.LOW,
        human_review_reason="Requiere revisión humana.",
        review_priority=80,
        recommended_review_action=ReviewActionV3.REVIEW,
        semantic_engine="llm:test",
        model_name="test",
    )


def test_repository_calibration_corpus_v2_loads_as_draft() -> None:
    corpus = load_conversation_calibration_corpus_v2(
        Path("config/semantic_calibration_corpus.v2.json")
    )
    assert corpus.status == "DRAFT"
    assert corpus.human_validated is False
    assert len(corpus.cases) == 5
    assert all("probable_archetype" in case.forbidden_inferences for case in corpus.cases)


def test_v2_calibration_metrics_do_not_include_archetype_accuracy() -> None:
    labels = [
        HumanConversationAssessmentLabelV2(
            case_id="football",
            text="No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
            expected_real_topic="Rivalidad futbolística",
            expected_contextual_meaning="Intercambio social sobre fútbol.",
            expected_apparent_affinity=ApparentAffinity.NONE,
            expected_affinity_domains=[],
            expected_apparent_intention=ApparentIntention.NONE,
            expected_false_positive_risk=RiskLevelV3.HIGH,
            expected_review_action=ReviewActionV3.OBSERVE,
            required_evidence_fragments=[
                "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
            ],
            forbidden_inferences=["probable_archetype", "declared_capacity"],
        ),
        HumanConversationAssessmentLabelV2(
            case_id="exploration",
            text="Busco una comunidad regenerativa en Yucatán.",
            expected_real_topic="Exploración de comunidad regenerativa",
            expected_contextual_meaning="Solicitud de información.",
            expected_apparent_affinity=ApparentAffinity.CLEAR,
            expected_affinity_domains=[AffinityDomain.COMMUNITY],
            expected_apparent_intention=ApparentIntention.EXPLORATION,
            expected_false_positive_risk=RiskLevelV3.LOW,
            expected_review_action=ReviewActionV3.REVIEW,
            required_evidence_fragments=["Busco una comunidad regenerativa en Yucatán."],
            forbidden_inferences=["probable_archetype", "declared_capacity"],
        ),
    ]
    report = run_conversation_calibration_v2(
        labels,
        runner=_prediction,
        corpus_human_validated=True,
    )
    payload = report.model_dump(mode="json")
    assert "archetype_accuracy" not in payload
    assert report.affinity_class_accuracy == 1.0
    assert report.intent_class_accuracy == 1.0
    assert report.false_positive_rate == 0.0
    assert report.evidence_validity_rate == 1.0
    assert report.forbidden_inference_rate == 0.0
    assert report.ready_for_pilot is True
