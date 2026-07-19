from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field

from app.discovery.contracts import DiscoveryResult


_DECISION_PATTERNS = (
    r"\b(evaluando|comparando|busco|buscando|considerando|interesad[oa]|quiero|quisiera|necesito)\b",
    r"\b(evaluating|comparing|looking for|considering|interested|I want|I need)\b",
)
_OBJECTION_PATTERNS = (
    r"\b(duda|riesgo|rentabilidad|seguridad jurídica|gobernanza|plazo|propiedad|objeción)\b",
    r"\b(concern|risk|return|legal|governance|timeline|ownership|objection)\b",
)
_ACTION_PATTERNS = (
    r"\b(invertir|participar|vivir|colaborar|visitar|contactar|presupuesto|capital)\b",
    r"\b(invest|participate|live|collaborate|visit|contact|budget|capital)\b",
)
_PROMOTIONAL_PATTERNS = (
    r"\b(compra ahora|últimos lugares|oferta limitada|contáctame por dm|promoción)\b",
    r"\b(buy now|limited offer|last spots|dm me|promotion)\b",
)


class ConversationQualityAssessment(BaseModel):
    status: Literal["substantive", "review", "insufficient"]
    score: int = Field(ge=0, le=10)
    positive_signals: list[str] = Field(default_factory=list)
    negative_signals: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _distinct_normalized_parts(*parts: str | None) -> list[str]:
    normalized_parts: list[str] = []
    seen: set[str] = set()
    for part in parts:
        normalized = re.sub(r"\s+", " ", part or "").strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            normalized_parts.append(normalized)
    return normalized_parts


def assess_conversation_quality(result: DiscoveryResult) -> ConversationQualityAssessment:
    text = " ".join(_distinct_normalized_parts(result.title, result.text, result.context))
    score = 0
    positive: list[str] = []
    negative: list[str] = []
    missing: list[str] = []

    if len(text) >= 240:
        score += 3
        positive.append("extended_content")
    elif len(text) >= 100:
        score += 2
        positive.append("sufficient_content")
    else:
        negative.append("thin_content")

    if "?" in text:
        score += 1
        positive.append("explicit_question")
    if _matches(text, _DECISION_PATTERNS):
        score += 2
        positive.append("decision_language")
    if _matches(text, _OBJECTION_PATTERNS):
        score += 2
        positive.append("objection_or_due_diligence")
    if _matches(text, _ACTION_PATTERNS):
        score += 2
        positive.append("action_language")
    if _matches(text, _PROMOTIONAL_PATTERNS):
        score = max(0, score - 4)
        negative.append("promotional_language")

    if result.published_at is None:
        missing.append("published_at")
    if result.author_name is None:
        missing.append("author_name")
    if not result.context:
        missing.append("context")

    status: Literal["substantive", "review", "insufficient"]
    if score >= 5 and "promotional_language" not in negative:
        status = "substantive"
    elif score >= 2:
        status = "review"
    else:
        status = "insufficient"

    return ConversationQualityAssessment(
        status=status,
        score=score,
        positive_signals=positive,
        negative_signals=negative,
        missing_fields=missing,
    )
