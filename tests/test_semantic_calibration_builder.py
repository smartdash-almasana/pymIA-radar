from types import SimpleNamespace

from app.semantics.calibration_builder import build_seeded_calibration_corpus


def test_builder_creates_draft_machine_seeded_cases() -> None:
    conversation = SimpleNamespace(
        id=7,
        title="Evaluando comunidad",
        text="Quiero conocer una comunidad regenerativa en Yucatán.",
        context="Conversación pública",
        conversation_url="https://example.com/c/7",
    )
    assessment = SimpleNamespace(
        probable_archetype="SEMBRADOR_PACIENTE",
        recommended_action="REVISAR_O_MADURAR",
        decision_stage="EXPLORACIÓN",
        thematic_affinity=78,
        values_affinity=72,
        intent_score=45,
    )

    corpus = build_seeded_calibration_corpus([(conversation, assessment)])

    assert corpus.status == "DRAFT"
    assert corpus.human_validated is False
    assert len(corpus.cases) == 1
    case = corpus.cases[0]
    assert case.case_id == "conversation-7"
    assert case.source_conversation_id == 7
    assert case.source_url == "https://example.com/c/7"
    assert case.label_provenance == "MACHINE_SEEDED_REQUIRES_HUMAN_REVIEW"
    assert case.expected_thematic_affinity == 78
    assert "Evaluando comunidad" in case.text
    assert "Conversación pública" in case.text


def test_builder_never_marks_empty_corpus_as_validated() -> None:
    corpus = build_seeded_calibration_corpus([])

    assert corpus.status == "DRAFT"
    assert corpus.reviewed_by is None
    assert corpus.cases == []
    assert corpus.human_validated is False
