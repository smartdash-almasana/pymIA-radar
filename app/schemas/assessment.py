from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class DeclaredCapacity(StrEnum):
    UNKNOWN = "NO_CONOCIDA"
    LOW = "BAJA_DECLARADA"
    MEDIUM = "MEDIA_DECLARADA"
    HIGH = "ALTA_DECLARADA"


class DecisionStage(StrEnum):
    DISCOVERY = "DESCUBRIMIENTO"
    EXPLORATION = "EXPLORACIÓN"
    COMPARISON = "COMPARACIÓN"
    ACTIVE_EVALUATION = "EVALUACIÓN_ACTIVA"
    READY_TO_TALK = "LISTO_PARA_CONVERSAR"
    READY_TO_QUALIFY = "LISTO_PARA_PRECALIFICAR"


class FalsePositiveRisk(StrEnum):
    LOW = "BAJO"
    MEDIUM = "MEDIO"
    HIGH = "ALTO"


class ReviewAction(StrEnum):
    APPROACH_REVIEW = "REVISAR_PARA_ACERCAMIENTO"
    REVIEW_OR_NURTURE = "REVISAR_O_MADURAR"
    OBSERVE = "OBSERVAR"
    DISCARD = "DESCARTAR"


class ProbableArchetype(StrEnum):
    PIONEER = "PIONERO_VISIONARIO"
    PATIENT_SOWER = "SEMBRADOR_PACIENTE"
    REGENERATIVE_ARTISAN = "ARTIFICE_REGENERATIVO"


class AssessmentResult(BaseModel):
    thematic_affinity: int = Field(ge=0, le=100)
    values_affinity: int = Field(ge=0, le=100)
    intent_score: int = Field(ge=0, le=100)
    declared_capacity: DeclaredCapacity = DeclaredCapacity.UNKNOWN
    decision_stage: DecisionStage
    evidence_quality: int = Field(ge=0, le=100)
    false_positive_risk: FalsePositiveRisk
    review_priority: int = Field(ge=0, le=100)
    probable_archetype: ProbableArchetype | None = None
    archetype_confidence: int | None = Field(default=None, ge=0, le=100)
    archetype_evidence: list[str] = Field(default_factory=list)
    positive_signals: list[str] = Field(default_factory=list)
    negative_signals: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    evidence_fragments: list[str] = Field(default_factory=list)
    recommended_action: ReviewAction
    human_review_required: bool = True
    provisional: bool = True
