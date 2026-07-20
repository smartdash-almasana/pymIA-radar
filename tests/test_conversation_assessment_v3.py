import pytest
from pydantic import ValidationError

from app.schemas.assessment_v3 import (
    AffinityDomain,
    ApparentAffinity,
    ApparentIntention,
    AssessmentStatusV3,
    ConversationAssessmentDraftV3,
    ReviewActionV3,
    RiskLevelV3,
)
from app.semantics.conversation_assessment_v3 import (
    InvalidModelOutputError,
    SemanticProviderError,
    assess_conversation_v3,
    build_v3_runner,
    calculate_review_policy,
    finalize_draft_v3,
    _system_prompt_v3,
    SEMANTIC_HTTP_TIMEOUT_SECONDS,
)


def _draft(**overrides) -> ConversationAssessmentDraftV3:
    data = {
        "real_topic": "Búsqueda de participación en una comunidad regenerativa",
        "contextual_meaning": "La persona solicita información sobre una posibilidad concreta.",
        "apparent_affinity": ApparentAffinity.CLEAR,
        "apparent_affinity_domains": [
            AffinityDomain.COMMUNITY,
            AffinityDomain.REGENERATION,
        ],
        "apparent_intention": ApparentIntention.EXPLORATION,
        "intention_summary": "Explora una comunidad regenerativa en Yucatán.",
        "evidence_fragments": [
            "Busco una comunidad regenerativa en Yucatán y quiero conocer opciones."
        ],
        "contradictions": [],
        "missing_context": [],
        "false_positive_risk": RiskLevelV3.LOW,
        "uncertainty": RiskLevelV3.LOW,
        "human_review_reason": "Existe afinidad aparente con evidencia literal.",
    }
    data.update(overrides)
    return ConversationAssessmentDraftV3(**data)


def test_v3_contract_forbids_legacy_person_inferences() -> None:
    payload = _draft().model_dump(mode="json")
    payload["probable_archetype"] = "SEMBRADOR_PACIENTE"
    with pytest.raises(ValidationError):
        ConversationAssessmentDraftV3.model_validate(payload)


def test_completed_v3_uses_literal_evidence_and_radar_policy() -> None:
    result = finalize_draft_v3(
        conversation_id=7,
        draft=_draft(),
        source_parts=[
            "Busco una comunidad regenerativa en Yucatán y quiero conocer opciones."
        ],
        semantic_engine="llm:test",
        model_name="test-model",
    )
    assert result.assessment_status == AssessmentStatusV3.COMPLETED
    assert result.apparent_affinity == ApparentAffinity.CLEAR
    assert result.recommended_review_action == ReviewActionV3.REVIEW
    assert result.review_priority > 0
    assert result.evidence_fragments


def test_clear_affinity_with_invented_evidence_is_invalid() -> None:
    result = finalize_draft_v3(
        conversation_id=8,
        draft=_draft(evidence_fragments=["Una cita que nunca apareció."]),
        source_parts=["Texto fuente completamente distinto."],
        semantic_engine="llm:test",
        model_name="test-model",
    )
    assert result.assessment_status == AssessmentStatusV3.INVALID_EVIDENCE
    assert result.apparent_affinity is None
    assert result.review_priority == 0
    assert result.recommended_review_action == ReviewActionV3.OBSERVE


def test_action_oriented_requires_specific_action_evidence() -> None:
    result = finalize_draft_v3(
        conversation_id=9,
        draft=_draft(
            apparent_intention=ApparentIntention.ACTION_ORIENTED,
            evidence_fragments=["La comunidad regenerativa parece interesante."],
        ),
        source_parts=["La comunidad regenerativa parece interesante."],
        semantic_engine="llm:test",
        model_name="test-model",
    )
    assert result.assessment_status == AssessmentStatusV3.INVALID_EVIDENCE


def test_provider_failure_is_closed_without_legacy_fallback() -> None:
    def failing_runner(_: str) -> ConversationAssessmentDraftV3:
        raise SemanticProviderError("provider down")

    result = assess_conversation_v3(
        conversation_id=10,
        title=None,
        text="inversión comunidad Yucatán",
        context=None,
        enabled=True,
        model_name="test-model",
        provider_name="agnes",
        base_url="https://example.invalid/v1",
        api_key="secret",
        runner=failing_runner,
    )
    assert result.assessment_status == AssessmentStatusV3.SEMANTIC_ASSESSMENT_UNAVAILABLE
    assert result.apparent_affinity is None
    assert result.review_priority == 0
    assert result.recommended_review_action == ReviewActionV3.OBSERVE


def test_unexpected_runner_error_is_not_misclassified_as_provider_failure() -> None:
    def broken_runner(_: str) -> ConversationAssessmentDraftV3:
        raise RuntimeError("programming error")

    with pytest.raises(RuntimeError, match="programming error"):
        assess_conversation_v3(
            conversation_id=101,
            title=None,
            text="Texto de prueba",
            context=None,
            enabled=True,
            model_name="test-model",
            runner=broken_runner,
        )


def test_disabled_semantic_engine_is_unavailable_not_deterministically_promoted() -> None:
    result = assess_conversation_v3(
        conversation_id=11,
        title=None,
        text="Busco invertir y participar en una comunidad regenerativa.",
        context=None,
        enabled=False,
        model_name="test-model",
    )
    assert result.assessment_status == AssessmentStatusV3.SEMANTIC_ASSESSMENT_UNAVAILABLE
    assert result.apparent_affinity is None


def test_high_false_positive_risk_caps_priority() -> None:
    priority, action = calculate_review_policy(
        status=AssessmentStatusV3.COMPLETED,
        affinity=ApparentAffinity.CLEAR,
        intention=ApparentIntention.ACTION_ORIENTED,
        false_positive_risk=RiskLevelV3.HIGH,
        uncertainty=RiskLevelV3.LOW,
        valid_evidence_count=4,
    )
    assert priority <= 60
    assert action == ReviewActionV3.REVIEW


def test_football_context_can_be_explicitly_classified_as_no_affinity() -> None:
    text = "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    result = finalize_draft_v3(
        conversation_id=12,
        draft=_draft(
            real_topic="Rivalidad futbolística",
            contextual_meaning="Intercambio social sobre Messi y Cristiano.",
            apparent_affinity=ApparentAffinity.NONE,
            apparent_affinity_domains=[],
            apparent_intention=ApparentIntention.NONE,
            intention_summary="No existe búsqueda relacionada con Inlak'ech.",
            evidence_fragments=[text],
            false_positive_risk=RiskLevelV3.HIGH,
            uncertainty=RiskLevelV3.LOW,
        ),
        source_parts=[text],
        semantic_engine="llm:test",
        model_name="test-model",
    )
    assert result.assessment_status == AssessmentStatusV3.COMPLETED
    assert result.apparent_affinity == ApparentAffinity.NONE
    assert result.recommended_review_action == ReviewActionV3.OBSERVE


def test_invalid_runner_payload_is_classified_as_invalid_model_output() -> None:
    def invalid_runner(_: str) -> dict:
        return {"real_topic": "incompleto"}

    result = assess_conversation_v3(
        conversation_id=13,
        title=None,
        text="Texto de prueba",
        context=None,
        enabled=True,
        model_name="test-model",
        provider_name="agnes",
        base_url="https://example.invalid/v1",
        api_key="secret",
        runner=invalid_runner,
    )
    assert result.assessment_status == AssessmentStatusV3.INVALID_MODEL_OUTPUT
    assert result.safe_error_code == "INVALID_MODEL_OUTPUT"


def test_http_json_runner_accepts_valid_v3_response(monkeypatch) -> None:
    import httpx

    payload = _draft().model_dump_json()

    class Response:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {"choices": [{"message": {"content": payload}}]}

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: Response())
    runner = build_v3_runner(
        "test-model",
        provider_name="agnes",
        base_url="https://apihub.agnes-ai.com/v1",
        api_key="secret",
    )
    assert runner("texto").apparent_affinity == ApparentAffinity.CLEAR


def test_http_json_runner_rejects_invalid_assessment(monkeypatch) -> None:
    import httpx

    class Response:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {"choices": [{"message": {"content": '{"real_topic":"x"}'}}]}

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: Response())
    runner = build_v3_runner(
        "test-model",
        provider_name="agnes",
        base_url="https://apihub.agnes-ai.com/v1",
        api_key="secret",
    )
    with pytest.raises(InvalidModelOutputError):
        runner("texto")


@pytest.mark.parametrize(
    "content",
    [
        lambda payload: f"```json\n{payload}\n```",
        lambda payload: f"Here is the assessment:\n{payload}\nEnd.",
        lambda payload: [{"type": "text", "text": payload}],
    ],
)
def test_http_json_runner_accepts_safe_openai_compatible_json_wrappers(
    monkeypatch, content
) -> None:
    import httpx

    payload = _draft().model_dump_json()

    class Response:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {"choices": [{"message": {"content": content(payload)}}]}

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: Response())
    runner = build_v3_runner(
        "test-model",
        provider_name="agnes",
        base_url="https://apihub.agnes-ai.com/v1",
        api_key="secret",
    )
    assert runner("texto").schema_version == "radar-conversation-assessment/v3"


def test_http_json_runner_sanitizes_http_error(monkeypatch) -> None:
    import httpx

    class Response:
        status_code = 500

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: Response())
    runner = build_v3_runner(
        "test-model",
        provider_name="agnes",
        base_url="https://apihub.agnes-ai.com/v1",
        api_key="secret",
    )
    with pytest.raises(SemanticProviderError, match="500"):
        runner("texto")


def test_v3_prompt_requires_exact_enums_and_array_fields() -> None:
    prompt = _system_prompt_v3()
    assert "apparent_affinity=NONE|POSSIBLE|CLEAR" in prompt
    assert "apparent_intention=NONE|THEMATIC_SYMPATHY|EXPLORATION|ACTION_ORIENTED" in prompt
    assert "missing_context must always be JSON arrays" in prompt


def test_v3_prompt_prevents_gemma_schema_and_reason_regressions() -> None:
    prompt = _system_prompt_v3()
    assert "Return a single valid JSON object only" in prompt
    assert "Do not include markdown fences" in prompt
    assert "<thought> tags" in prompt
    assert 'schema_version value MUST be exactly "radar-conversation-assessment/v3"' in prompt
    assert 'never shorten it to "v3"' in prompt
    assert "human_review_reason must always be a non-empty JSON string" in prompt
    assert "never an array" in prompt


def test_http_json_runner_uses_extended_timeout(monkeypatch) -> None:
    import httpx

    captured: dict[str, object] = {}
    payload = _draft().model_dump_json()

    class Response:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {"choices": [{"message": {"content": payload}}]}

    def fake_post(*args, **kwargs):
        captured.update(kwargs)
        return Response()

    monkeypatch.setattr(httpx, "post", fake_post)
    runner = build_v3_runner(
        "test-model",
        provider_name="openai_compatible",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        api_key="secret",
    )

    assert runner("texto").schema_version == "radar-conversation-assessment/v3"
    assert captured["timeout"] == SEMANTIC_HTTP_TIMEOUT_SECONDS
