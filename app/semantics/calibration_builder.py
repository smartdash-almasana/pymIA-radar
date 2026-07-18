from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment_v2 import SemanticAssessmentV2
from app.models.conversation import Conversation
from app.schemas.assessment import DecisionStage, ProbableArchetype, ReviewAction
from app.semantics.calibration import HumanAssessmentLabel
from app.semantics.calibration_io import CalibrationCorpus


def _case_text(conversation: Conversation) -> str:
    parts = [conversation.title or "", conversation.text, conversation.context or ""]
    return "\n".join(part.strip() for part in parts if part and part.strip())


def build_seeded_calibration_corpus(
    rows: Iterable[tuple[Conversation, SemanticAssessmentV2]],
) -> CalibrationCorpus:
    """Build a draft corpus from persisted assessments.

    Values are machine-seeded only to reduce manual transcription. The corpus
    remains DRAFT and cannot authorize a pilot until a person validates it.
    """
    cases: list[HumanAssessmentLabel] = []
    for conversation, assessment in rows:
        archetype = (
            ProbableArchetype(assessment.probable_archetype)
            if assessment.probable_archetype
            else None
        )
        cases.append(
            HumanAssessmentLabel(
                case_id=f"conversation-{conversation.id}",
                text=_case_text(conversation),
                source_conversation_id=conversation.id,
                source_url=conversation.conversation_url,
                label_provenance="MACHINE_SEEDED_REQUIRES_HUMAN_REVIEW",
                label_notes=(
                    "Valores copiados de la última evaluación persistida. "
                    "Revisar y corregir antes de marcar HUMAN_VALIDATED."
                ),
                expected_action=ReviewAction(assessment.recommended_action),
                expected_stage=DecisionStage(assessment.decision_stage),
                expected_archetype=archetype,
                expected_thematic_affinity=assessment.thematic_affinity,
                expected_values_affinity=assessment.values_affinity,
                expected_intent_score=assessment.intent_score,
            )
        )
    return CalibrationCorpus(
        status="DRAFT",
        review_notes=(
            "Corpus generado desde evaluaciones persistidas. Todas las etiquetas "
            "requieren revisión humana independiente."
        ),
        cases=cases,
    )


def load_latest_assessment_rows(
    db: Session,
    *,
    limit: int = 100,
) -> list[tuple[Conversation, SemanticAssessmentV2]]:
    conversations = list(
        db.scalars(select(Conversation).order_by(Conversation.id.desc()).limit(limit))
    )
    rows: list[tuple[Conversation, SemanticAssessmentV2]] = []
    for conversation in conversations:
        assessment = db.scalar(
            select(SemanticAssessmentV2)
            .where(SemanticAssessmentV2.conversation_id == conversation.id)
            .order_by(SemanticAssessmentV2.id.desc())
            .limit(1)
        )
        if assessment is not None:
            rows.append((conversation, assessment))
    return rows
