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
    """Build a lazy semantic runner without broadening provider-specific workarounds."""
    normalized_provider = provider_name.strip().lower()

    if normalized_provider in {"deepseek", "openai_compatible", "ollama", "agnes"}:
        if not base_url:
            raise ValueError(f"{normalized_provider} requires SEMANTIC_LLM_BASE_URL")
        if normalized_provider != "ollama" and not api_key:
            raise ValueError(f"{normalized_provider} requires SEMANTIC_LLM_API_KEY")

        is_agnes = normalized_provider == "agnes" or _is_agnes_base_url(base_url)
        if is_agnes:
            return _build_http_json_runner(model_name, base_url, api_key or "")
        return _build_openai_compatible_structured_runner(
            model_name,
            base_url,
            api_key or "ollama",
        )

    if normalized_provider != "default":
        raise ValueError(f"Unsupported semantic LLM provider: {provider_name}")

    return _build_pydantic_structured_runner(model_name)


def _is_agnes_base_url(base_url: str) -> bool:
    """Return true only for Agnes' exact host or real subdomains."""
    from urllib.parse import urlparse

    try:
        hostname = urlparse(base_url).hostname or ""
    except ValueError:
        return False
    hostname = hostname.lower().rstrip(".")
    return hostname == "agnes-ai.com" or hostname.endswith(".agnes-ai.com")


def _build_http_json_runner(
    model_name: str,
    base_url: str,
    api_key: str,
) -> DraftRunner:
    """Direct HTTP runner — sends a system prompt asking for JSON, parses manually.

    Avoids pydantic-ai's tool-calling path, which many providers don't support correctly.
    """
    import httpx

    schema_description = (
        '{\n'
        '  "thematic_affinity": int 0-100 (qué tanto se alinea con regeneración, '
        'permacultura, soberanía, propósito colectivo),\n'
        '  "values_affinity": int 0-100 (qué tanto resuena con valores como comunidad, '
        'largo plazo, ética, arraigo),\n'
        '  "intent_score": int 0-100 (qué tan concreta es la intención de acción),\n'
        '  "declared_capacity": "NO_CONOCIDA" | "BAJA_DECLARADA" | "MEDIA_DECLARADA" | '
        '"ALTA_DECLARADA" (usá NO_CONOCIDA salvo que haya declaración explícita de '
        'capacidad económica o patrimonial),\n'
        '  "decision_stage": "DESCUBRIMIENTO" | "EXPLORACION" | "COMPARACION" | '
        '"EVALUACION_ACTIVA" | "LISTO_PARA_CONVERSAR" | "LISTO_PARA_PRECALIFICAR",\n'
        '  "evidence_quality": int 0-100 (calidad de las citas textuales disponibles),\n'
        '  "false_positive_risk": "BAJO" | "MEDIO" | "ALTO",\n'
        '  "probable_archetype": "PIONERO_VISIONARIO" | "SEMBRADOR_PACIENTE" | '
        '"ARTIFICE_REGENERATIVO" | null,\n'
        '  "archetype_confidence": int 0-100 | null,\n'
        '  "archetype_evidence": [string],\n'
        '  "positive_signals": [string] (señales de alineación con Inlak\'ech),\n'
        '  "negative_signals": [string] (señales de desalineación),\n'
        '  "objections": [string] (objeciones o dudas explícitas),\n'
        '  "missing_information": [string] (qué falta para decidir),\n'
        '  "evidence_fragments": [string] (citas textuales literales del texto original)\n'
        '}'
    )

    system_prompt = (
        "Analizá la conversación para RADAR de Inlak'ech. "
        "Devolvé ÚNICAMENTE un objeto JSON válido (sin texto adicional, sin markdown) "
        "con esta estructura exacta:\n\n"
        f"{schema_description}\n\n"
        "Reglas:\n"
        "- NO infieras capacidad económica. Usá NO_CONOCIDA.\n"
        "- Diferenciá deseos hipotéticos de decisión activa.\n"
        "- Citá solo fragmentos literales presentes en el texto.\n"
        "- El resultado es provisional y será revisado por humanos."
    )

    def run(text: str) -> LLMAssessmentDraft:
        try:
            resp = httpx.post(
                f"{base_url.rstrip('/')}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text},
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2048,
                },
                timeout=30,
            )
        except httpx.TimeoutException as exc:
            raise RuntimeError("Agnes request timed out") from exc
        except httpx.RequestError as exc:
            raise RuntimeError("Agnes request failed") from exc

        if resp.status_code < 200 or resp.status_code >= 300:
            raise RuntimeError(f"Agnes HTTP error: {resp.status_code}")

        try:
            body = resp.json()
        except ValueError as exc:
            raise RuntimeError("Agnes returned invalid JSON envelope") from exc

        try:
            raw = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Agnes returned an invalid response envelope") from exc

        if not isinstance(raw, str) or not raw.strip():
            raise RuntimeError("Agnes returned an empty assessment")

        return LLMAssessmentDraft.model_validate_json(raw)

    return run


def _build_openai_compatible_structured_runner(
    model_name: str,
    base_url: str,
    api_key: str,
) -> DraftRunner:
    """Pydantic AI runner for compatible providers with working structured output."""
    try:
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.openai import OpenAIProvider
    except ImportError as exc:
        raise RuntimeError("Pydantic AI OpenAI provider is not installed") from exc

    provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    model = OpenAIChatModel(model_name, provider=provider)
    return _build_pydantic_structured_runner(model)


def _build_pydantic_structured_runner(model_name: object) -> DraftRunner:
    """Pydantic AI structured-output runner for providers with proper tool-calling support."""
    try:
        from pydantic_ai import Agent
    except ImportError as exc:
        raise RuntimeError(
            "Pydantic AI is not installed; install the project with the 'ai' extra"
        ) from exc

    agent = Agent(
        model_name,
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
