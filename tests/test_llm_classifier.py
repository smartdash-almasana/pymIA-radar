import json

import httpx
import pytest
from pydantic import ValidationError

from app.schemas.assessment import (
    DecisionStage,
    DeclaredCapacity,
    FalsePositiveRisk,
    ProbableArchetype,
    ReviewAction,
)
from app.semantics.llm_classifier import (
    LLMAssessmentDraft,
    _build_http_json_runner,
    assess_with_optional_llm,
    assess_with_optional_llm_details,
    build_pydantic_ai_runner,
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


def _valid_payload(**overrides: object) -> dict[str, object]:
    payload = _draft().model_dump(mode="json")
    payload.update(overrides)
    return payload


class _Response:
    def __init__(self, status_code: int = 200, *, content: str | None = None, invalid_envelope: bool = False) -> None:
        self.status_code = status_code
        self._content = content
        self._invalid_envelope = invalid_envelope

    def json(self) -> dict[str, object]:
        if self._invalid_envelope:
            return {"unexpected": True}
        return {
            "choices": [
                {"message": {"content": self._content}}
            ]
        }


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


def test_optional_llm_records_fallback_when_runner_fails() -> None:
    def broken_runner(_: str) -> LLMAssessmentDraft:
        raise RuntimeError("provider unavailable")

    execution = assess_with_optional_llm_details(
        "Busco una comunidad regenerativa para invertir a largo plazo.",
        enabled=True,
        model_name="openai:test-model",
        provider_name="agnes",
        runner=broken_runner,
    )

    assert execution.semantic_engine == "deterministic_fallback"
    assert execution.model_name == "openai:test-model"
    assert execution.result.declared_capacity == DeclaredCapacity.UNKNOWN
    assert execution.result.provisional is True
    assert execution.result.human_review_required is True


def test_openai_compatible_provider_requires_base_url() -> None:
    with pytest.raises(ValueError, match="SEMANTIC_LLM_BASE_URL"):
        build_pydantic_ai_runner(
            "free-model",
            provider_name="openai_compatible",
            api_key="test-key",
        )


def test_deepseek_provider_requires_api_key() -> None:
    with pytest.raises(ValueError, match="SEMANTIC_LLM_API_KEY"):
        build_pydantic_ai_runner(
            "deepseek-model",
            provider_name="deepseek",
            base_url="https://example.invalid/v1",
        )


def test_agnes_api_key_alias_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.config import Settings

    monkeypatch.delenv("SEMANTIC_LLM_API_KEY", raising=False)
    monkeypatch.setenv("AGNES_API_KEY", "agnes-secret")

    settings = Settings(_env_file=None)

    assert settings.semantic_llm_api_key == "agnes-secret"


@pytest.mark.parametrize("provider_name", ["openai_compatible", "deepseek", "ollama"])
def test_non_agnes_compatible_providers_keep_structured_runner(
    monkeypatch: pytest.MonkeyPatch,
    provider_name: str,
) -> None:
    sentinel = object()

    def fake_builder(model_name: str, base_url: str, api_key: str) -> object:
        assert model_name == "other-model"
        assert base_url == "https://provider.example/v1"
        assert api_key == ("ollama" if provider_name == "ollama" else "provider-key")
        return sentinel

    monkeypatch.setattr(
        "app.semantics.llm_classifier._build_openai_compatible_structured_runner",
        fake_builder,
    )

    runner = build_pydantic_ai_runner(
        "other-model",
        provider_name=provider_name,
        base_url="https://provider.example/v1",
        api_key=None if provider_name == "ollama" else "provider-key",
    )

    assert runner is sentinel


@pytest.mark.parametrize(
    ("provider_name", "base_url"),
    [
        ("agnes", "https://provider.example/v1"),
        ("openai_compatible", "https://apihub.agnes-ai.com/v1"),
    ],
)
def test_agnes_provider_or_url_uses_http_json_runner(
    monkeypatch: pytest.MonkeyPatch,
    provider_name: str,
    base_url: str,
) -> None:
    sentinel = object()

    def fake_builder(model_name: str, received_base_url: str, api_key: str) -> object:
        assert model_name == "agnes-2.0-flash"
        assert received_base_url == base_url
        assert api_key == "agnes-key"
        return sentinel

    monkeypatch.setattr("app.semantics.llm_classifier._build_http_json_runner", fake_builder)

    runner = build_pydantic_ai_runner(
        "agnes-2.0-flash",
        provider_name=provider_name,
        base_url=base_url,
        api_key="agnes-key",
    )

    assert runner is sentinel


def test_agnes_lookalike_host_does_not_use_http_json_runner(monkeypatch: pytest.MonkeyPatch) -> None:
    sentinel = object()

    def fake_structured_builder(model_name: str, base_url: str, api_key: str) -> object:
        assert model_name == "other-model"
        assert base_url == "https://not-agnes-ai.com/v1"
        assert api_key == "provider-key"
        return sentinel

    def fail_http_builder(*args: object, **kwargs: object) -> object:
        raise AssertionError("Lookalike host must not use Agnes HTTP runner")

    monkeypatch.setattr(
        "app.semantics.llm_classifier._build_openai_compatible_structured_runner",
        fake_structured_builder,
    )
    monkeypatch.setattr("app.semantics.llm_classifier._build_http_json_runner", fail_http_builder)

    runner = build_pydantic_ai_runner(
        "other-model",
        provider_name="openai_compatible",
        base_url="https://not-agnes-ai.com/v1",
        api_key="provider-key",
    )

    assert runner is sentinel


def test_decision_stage_accepts_accented_and_unaccented_values() -> None:
    assert DecisionStage("EXPLORACION") is DecisionStage.EXPLORATION
    assert DecisionStage("EXPLORACIÓN") is DecisionStage.EXPLORATION
    assert DecisionStage("COMPARACION") is DecisionStage.COMPARISON
    assert DecisionStage("COMPARACIÓN") is DecisionStage.COMPARISON
    assert DecisionStage("EVALUACION_ACTIVA") is DecisionStage.ACTIVE_EVALUATION
    assert DecisionStage("EVALUACIÓN_ACTIVA") is DecisionStage.ACTIVE_EVALUATION


def test_decision_stage_rejects_unknown_value() -> None:
    with pytest.raises(ValueError):
        DecisionStage("CASI_LISTO")


def test_agnes_valid_response_is_pydantic_validated(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        httpx,
        "post",
        lambda *args, **kwargs: _Response(content=json.dumps(_valid_payload())),
    )

    runner = _build_http_json_runner(
        "agnes-2.0-flash",
        "https://apihub.agnes-ai.com/v1",
        "secret-key",
    )
    draft = runner("texto real")

    assert draft.declared_capacity is DeclaredCapacity.UNKNOWN
    assert draft.decision_stage is DecisionStage.ACTIVE_EVALUATION


@pytest.mark.parametrize("status_code", [401, 429, 500])
def test_agnes_http_errors_are_sanitized(
    monkeypatch: pytest.MonkeyPatch,
    status_code: int,
) -> None:
    secret = "super-secret-key"
    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: _Response(status_code=status_code))
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", secret)

    with pytest.raises(RuntimeError) as exc_info:
        runner("texto real")

    assert str(status_code) in str(exc_info.value)
    assert secret not in str(exc_info.value)


def test_agnes_timeout_is_sanitized(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "super-secret-key"

    def timeout(*args: object, **kwargs: object) -> object:
        raise httpx.ReadTimeout("timed out")

    monkeypatch.setattr(httpx, "post", timeout)
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", secret)

    with pytest.raises(RuntimeError, match="timed out") as exc_info:
        runner("texto real")

    assert secret not in str(exc_info.value)


def test_agnes_rejects_invalid_json_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    class InvalidJsonResponse(_Response):
        def json(self) -> dict[str, object]:
            raise ValueError("invalid json")

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: InvalidJsonResponse())
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", "key")

    with pytest.raises(RuntimeError, match="invalid JSON envelope"):
        runner("texto real")


def test_agnes_rejects_invalid_json_assessment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: _Response(content="not-json"))
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", "key")

    with pytest.raises(ValidationError):
        runner("texto real")


def test_agnes_rejects_empty_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: _Response(content=""))
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", "key")

    with pytest.raises(RuntimeError, match="empty assessment"):
        runner("texto real")


def test_agnes_rejects_invalid_envelope(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: _Response(invalid_envelope=True))
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", "key")

    with pytest.raises(RuntimeError, match="invalid response envelope"):
        runner("texto real")


def test_agnes_rejects_unknown_enum(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _valid_payload(decision_stage="CASI_LISTO")
    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: _Response(content=json.dumps(payload)))
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", "key")

    with pytest.raises(ValidationError):
        runner("texto real")


def test_agnes_does_not_infer_capacity_when_unknown(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _valid_payload(declared_capacity="NO_CONOCIDA")
    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: _Response(content=json.dumps(payload)))
    runner = _build_http_json_runner("agnes-2.0-flash", "https://apihub.agnes-ai.com/v1", "key")

    result = finalize_llm_draft(runner("texto real"))

    assert result.declared_capacity is DeclaredCapacity.UNKNOWN
    assert result.human_review_required is True
    assert result.provisional is True
