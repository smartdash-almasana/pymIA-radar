from __future__ import annotations

from app.schemas.assessment import (
    AssessmentResult,
    DecisionStage,
    DeclaredCapacity,
    FalsePositiveRisk,
    ProbableArchetype,
    ReviewAction,
)
from app.semantics.deterministic_filter import deterministic_score


_INTENT_TERMS = (
    "invertir",
    "inversión",
    "participar",
    "mudarse",
    "residir",
    "comparando",
    "evaluando",
    "cuánto cuesta",
    "contacto",
    "plazo",
)
_VALUE_TERMS = (
    "regenerativa",
    "regeneración",
    "comunidad",
    "legado",
    "largo plazo",
    "propósito",
    "territorio",
    "pertenencia",
)
_OBJECTION_TERMS = (
    "seguridad jurídica",
    "rentabilidad",
    "gobernanza",
    "propiedad",
    "liquidez",
    "administración",
    "transparencia",
    "riesgo",
)


def _bounded_score(hit_count: int, weight: int) -> int:
    return min(100, hit_count * weight)


def _review_action(priority: int) -> ReviewAction:
    if priority >= 80:
        return ReviewAction.APPROACH_REVIEW
    if priority >= 60:
        return ReviewAction.REVIEW_OR_NURTURE
    if priority >= 40:
        return ReviewAction.OBSERVE
    return ReviewAction.DISCARD


def classify_conversation(text: str) -> AssessmentResult:
    """Return a provisional, deterministic assessment for human review.

    This function is not a lead qualification decision. It does not infer
    economic capacity and must be recalibrated against a real reviewed corpus.
    """
    normalized = text.lower().strip()
    base = deterministic_score(text)

    value_hits = [term for term in _VALUE_TERMS if term in normalized]
    intent_hits = [term for term in _INTENT_TERMS if term in normalized]
    objections = [term for term in _OBJECTION_TERMS if term in normalized]

    thematic_affinity = base["score"]
    values_affinity = _bounded_score(len(value_hits), 18)
    intent_score = _bounded_score(len(intent_hits), 20)

    evidence_quality = 20
    if len(text) >= 100:
        evidence_quality += 20
    if len(text) >= 240:
        evidence_quality += 20
    if "?" in text:
        evidence_quality += 15
    if objections:
        evidence_quality += 15
    if intent_hits:
        evidence_quality += 10
    evidence_quality = min(100, evidence_quality)

    if len(text) < 60 or not base["positive_hits"]:
        risk = FalsePositiveRisk.HIGH
        risk_penalty = 25
    elif not intent_hits:
        risk = FalsePositiveRisk.MEDIUM
        risk_penalty = 10
    else:
        risk = FalsePositiveRisk.LOW
        risk_penalty = 0

    raw_priority = (
        thematic_affinity * 0.25
        + values_affinity * 0.25
        + intent_score * 0.30
        + evidence_quality * 0.20
        - risk_penalty
    )
    review_priority = max(0, min(100, round(raw_priority)))

    if intent_score >= 60:
        stage = DecisionStage.ACTIVE_EVALUATION
    elif intent_score >= 20:
        stage = DecisionStage.EXPLORATION
    else:
        stage = DecisionStage.DISCOVERY

    archetype = None
    archetype_evidence: list[str] = []
    if any(term in normalized for term in ("patrimonio", "largo plazo", "legado familiar")):
        archetype = ProbableArchetype.PATIENT_SOWER
        archetype_evidence = [
            term for term in ("patrimonio", "largo plazo", "legado familiar") if term in normalized
        ]
    elif any(term in normalized for term in ("gobernanza", "liderar", "construir proyecto")):
        archetype = ProbableArchetype.PIONEER
        archetype_evidence = [
            term for term in ("gobernanza", "liderar", "construir proyecto") if term in normalized
        ]
    elif any(term in normalized for term in ("arquitectura", "materiales", "oficio", "construcción")):
        archetype = ProbableArchetype.REGENERATIVE_ARTISAN
        archetype_evidence = [
            term for term in ("arquitectura", "materiales", "oficio", "construcción") if term in normalized
        ]

    evidence_fragments = list(dict.fromkeys(base["positive_hits"] + value_hits + intent_hits + objections))

    return AssessmentResult(
        thematic_affinity=thematic_affinity,
        values_affinity=values_affinity,
        intent_score=intent_score,
        declared_capacity=DeclaredCapacity.UNKNOWN,
        decision_stage=stage,
        evidence_quality=evidence_quality,
        false_positive_risk=risk,
        review_priority=review_priority,
        probable_archetype=archetype,
        archetype_confidence=min(100, len(archetype_evidence) * 25) if archetype else None,
        archetype_evidence=archetype_evidence,
        positive_signals=list(dict.fromkeys(base["positive_hits"] + value_hits + intent_hits)),
        negative_signals=[f"negative:{item}" for item in base["negative_hits"]],
        objections=objections,
        missing_information=["declared_capacity", "time_horizon", "participation_path"],
        evidence_fragments=evidence_fragments,
        recommended_action=_review_action(review_priority),
    )
