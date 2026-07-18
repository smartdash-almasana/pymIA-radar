from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from pydantic import BaseModel, Field

from app.schemas.assessment import (
    AssessmentResult,
    DecisionStage,
    DeclaredCapacity,
    FalsePositiveRisk,
    ProbableArchetype,
    ReviewAction,
)
from app.semantics.classifier import classify_conversation


class LLMAssessmentDraft(BaseModel):
    """Semantic interpretation produced by an LLM before deterministic policy."""

    thematic_affinity: int = Field(ge=0, le=100)
    values_affinity: int = Field(ge=0, le=100)
    intent_score: int = Field(ge=0, le=100)
    declared_capacity: DeclaredCapacity = DeclaredCapacity.UNKNOWN
    decision_stage: DecisionStage
    evidence_quality: int = Field(ge=0, le=100)
    false_positive_risk: FalsePositiveRisk
    probable_archetype: ProbableArchetype | None = None
    archetype_confidence: int | None = Field(default=None, ge=0, le=100)
    archetype_evidence: list[str] = Field(default_factory=list)
    positive_signals: list[str] = Field(default_factory=list)
    negative_signals: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    evidence_fragments: list[str] = Field(default_factory=list)


class DraftRunner(Protocol):
    def __call__(self, text: str) -> LLMAssessmentDraft: ...


_RISK_PENALTY = {
    FalsePositiveRisk.LOW: 0,
    FalsePositiveRisk.MEDIUM: 10,
    FalsePositiveRisk.HIGH: 25,
}


def _review_action(priority: int) -> ReviewAction:
    if priority >= 80:
        return ReviewAction.APPROACH_REVIEW
    if priority >= 60:
        return ReviewAction.REVIEW_OR_NURTURE
    if priority >= 40:
        return ReviewAction.OBSERVE
    return ReviewAction.DISCARD


def finalize_llm_draft(draft: LLMAssessmentDraft) -> AssessmentResult:
    """Apply RADAR policy to an LLM interpretation.

    The model cannot choose workflow state, final priority, or review action.
    """
    raw_priority = (
        draft.thematic_affinity * 0.25
        + draft.values_affinity * 0.25
        + draft.intent_score * 0.30
        + draft.evidence_quality * 0.20
        - _RISK_PENALTY[draft.false_positive_risk]
    )
    priority = max(0, min(100, round(raw_priority)))

    return AssessmentResult(
        thematic_affinity=draft.thematic_affinity,
        values_affinity=draft.values_affinity,
        intent_score=draft.intent_score,
        declared_capacity=draft.declared_capacity,
        decision_stage=draft.decision_stage,
        evidence_quality=draft.evidence_quality,
        false_positive_risk=draft.false_positive_risk,
        review_priority=priority,
        probable_archetype=draft.probable_archetype,
        archetype_confidence=draft.archetype_confidence,
        archetype_evidence=draft.archetype_evidence,
        positive_signals=draft.positive_signals,
        negative_signals=draft.negative_signals,
        objections=draft.objections,
        missing_information=draft.missing_information,
        evidence_fragments=draft.evidence_fragments,
        recommended_action=_review_action(priority),
    )


def build_pydantic_ai_runner(
    model_name: str,
    *,
    provider_name: str = "default",
    base_url: str | None = None,
    api_key: str | None = None,
) -> DraftRunner:
    """Build a lazy Pydantic AI runner for native or OpenAI-compatible models."""
    try:
        from pydantic_ai import Agent
    except ImportError as exc:  # pragma: no cover - depends on optional package
        raise RuntimeError(
            "Pydantic AI is not installed; install the project with the 'ai' extra"
        ) from exc

    normalized_provider = provider_name.strip().lower()
    model: object = model_name
    if normalized_provider in {"deepseek", "openai_compatible", "ollama"}:
        if not base_url:
            raise ValueError(f"{normalized_provider} requires SEMANTIC_LLM_BASE_URL")
        if normalized_provider != "ollama" and not api_key:
            raise ValueError(f"{normalized_provider} requires SEMANTIC_LLM_API_KEY")
        try:
            from pydantic_ai.models.openai import OpenAIChatModel
            from pydantic_ai.providers.openai import OpenAIProvider
        except ImportError as exc:  # pragma: no cover - optional provider extra
            raise RuntimeError("Pydantic AI OpenAI provider is not installed") from exc
        provider = OpenAIProvider(
            base_url=base_url,
            api_key=api_key or "ollama",
        )
        model = OpenAIChatModel(model_name, provider=provider)
    elif normalized_provider != "default":
        raise ValueError(f"Unsupported semantic LLM provider: {provider_name}")

    agent = Agent(
        model,
        output_type=LLMAssessmentDraft,
        instructions=(
            "Analizá la conversación para RADAR de Inlak'ech. Separá afinidad temática, "
            "afinidad de valores, intención, etapa y calidad de evidencia. No infieras "
            "capacidad económica: usá NO_CONOCIDA salvo declaración explícita. Citá solo "
            "fragmentos presentes en el texto. Diferenciá deseos hipotéticos, curiosidad y "
            "decisión activa. El resultado es provisional y será revisado por una persona."
        ),
    )

    def run(text: str) -> LLMAssessmentDraft:
        result = agent.run_sync(text)
        return result.output

    return run


@dataclass(frozen=True)
class AssessmentExecution:
    result: AssessmentResult
    semantic_engine: str
    model_name: str | None


def assess_with_optional_llm_details(
    text: str,
    *,
    enabled: bool,
    model_name: str | None,
    provider_name: str = "default",
    base_url: str | None = None,
    api_key: str | None = None,
    runner: DraftRunner | None = None,
) -> AssessmentExecution:
    if not enabled or not model_name:
        return AssessmentExecution(
            result=classify_conversation(text),
            semantic_engine="deterministic",
            model_name=None,
        )

    try:
        active_runner = runner or build_pydantic_ai_runner(
            model_name,
            provider_name=provider_name,
            base_url=base_url,
            api_key=api_key,
        )
        return AssessmentExecution(
            result=finalize_llm_draft(active_runner(text)),
            semantic_engine=f"llm:{provider_name}",
            model_name=model_name,
        )
    except Exception:
        return AssessmentExecution(
            result=classify_conversation(text),
            semantic_engine="deterministic_fallback",
            model_name=model_name,
        )


def assess_with_optional_llm(
    text: str,
    *,
    enabled: bool,
    model_name: str | None,
    provider_name: str = "default",
    base_url: str | None = None,
    api_key: str | None = None,
    runner: DraftRunner | None = None,
) -> AssessmentResult:
    """Backward-compatible assessment result without execution metadata."""
    return assess_with_optional_llm_details(
        text,
        enabled=enabled,
        model_name=model_name,
        provider_name=provider_name,
        base_url=base_url,
        api_key=api_key,
        runner=runner,
    ).result
