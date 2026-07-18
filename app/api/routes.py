from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.assessment import SemanticAssessment
from app.models.conversation import Conversation
from app.models.engagement import EngagementEvent
from app.models.qualification import QualificationRecord
from app.models.review import ReviewDecision
from app.qualification import qualify_contact
from app.schemas.assessment import AssessmentResult
from app.schemas.conversation import (
    ConversationCreate,
    ConversationRead,
    conversation_orm_payload,
)
from app.schemas.qualification import QualificationInput, QualificationResult
from app.schemas.review import (
    EngagementCreate,
    EngagementEventType,
    EngagementRead,
    ReviewCreate,
    ReviewDecisionType,
    ReviewRead,
)
from app.semantics.llm_classifier import assess_with_optional_llm

router = APIRouter(prefix="/api")


@router.post("/conversations", response_model=ConversationRead)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    existing = db.scalar(
        select(Conversation).where(
            Conversation.source == payload.source,
            Conversation.external_id == payload.external_id,
        )
    )
    if existing:
        return existing

    item = Conversation(**conversation_orm_payload(payload))
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/conversations", response_model=list[ConversationRead])
def list_conversations(db: Session = Depends(get_db)):
    return list(db.scalars(select(Conversation).order_by(Conversation.id.desc())))


@router.post("/conversations/{conversation_id}/assess", response_model=AssessmentResult)
def assess_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    result = assess_with_optional_llm(
        f"{conversation.title or ''}\n{conversation.text}\n{conversation.context or ''}",
        enabled=settings.semantic_llm_enabled,
        model_name=settings.semantic_llm_model or settings.openai_model,
        provider_name=settings.semantic_llm_provider,
        base_url=settings.semantic_llm_base_url,
        api_key=settings.semantic_llm_api_key or settings.openai_api_key,
    )
    record = SemanticAssessment(
        conversation_id=conversation.id,
        relevant=result.recommended_action.value != "DESCARTAR",
        affinity_score=result.thematic_affinity,
        investment_intent=result.intent_score,
        probable_archetype=(
            result.probable_archetype.value if result.probable_archetype else None
        ),
        conversation_stage=result.decision_stage.value,
        recommended_action=result.recommended_action.value,
        evidence=result.evidence_fragments,
        missing_data=result.missing_information,
        risk_flags=[result.false_positive_risk.value, *result.negative_signals],
        reasoning_summary=(
            "Evaluación determinística provisional; requiere revisión humana."
        ),
    )
    db.add(record)
    conversation.status = (
        "REVIEW_PENDING"
        if result.recommended_action.value != "DESCARTAR"
        else "DISCARDED"
    )
    db.commit()
    return result


@router.post(
    "/conversations/{conversation_id}/reviews",
    response_model=ReviewRead,
)
def create_review(
    conversation_id: int,
    payload: ReviewCreate,
    db: Session = Depends(get_db),
):
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    status_by_decision = {
        ReviewDecisionType.APPROVE_APPROACH: "APPROACH_APPROVED",
        ReviewDecisionType.KEEP_OBSERVING: "OBSERVING",
        ReviewDecisionType.DISCARD: "DISCARDED",
        ReviewDecisionType.DO_NOT_CONTACT: "DO_NOT_CONTACT",
    }
    review = ReviewDecision(
        conversation_id=conversation_id,
        decision=payload.decision.value,
        edited_response=payload.edited_response,
        reviewer_notes=payload.reviewer_notes,
    )
    db.add(review)
    conversation.status = status_by_decision[payload.decision]
    db.commit()
    db.refresh(review)
    return review


@router.get(
    "/conversations/{conversation_id}/reviews",
    response_model=list[ReviewRead],
)
def list_reviews(conversation_id: int, db: Session = Depends(get_db)):
    if not db.get(Conversation, conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return list(
        db.scalars(
            select(ReviewDecision)
            .where(ReviewDecision.conversation_id == conversation_id)
            .order_by(ReviewDecision.id.asc())
        )
    )


@router.post(
    "/conversations/{conversation_id}/engagement-events",
    response_model=EngagementRead,
)
def create_engagement_event(
    conversation_id: int,
    payload: EngagementCreate,
    db: Session = Depends(get_db),
):
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if payload.event_type == EngagementEventType.CONTACTED:
        approved = db.scalar(
            select(ReviewDecision.id)
            .where(
                ReviewDecision.conversation_id == conversation_id,
                ReviewDecision.decision == ReviewDecisionType.APPROVE_APPROACH.value,
            )
            .order_by(ReviewDecision.id.desc())
        )
        if approved is None:
            raise HTTPException(
                status_code=409,
                detail="Human approval is required before recording contact",
            )

    status_by_event = {
        EngagementEventType.CONTACTED: "CONTACTED",
        EngagementEventType.REPLIED: "REPLIED",
        EngagementEventType.NO_RESPONSE: "OBSERVING",
        EngagementEventType.DO_NOT_CONTACT: "DO_NOT_CONTACT",
    }
    event = EngagementEvent(
        conversation_id=conversation_id,
        event_type=payload.event_type.value,
        channel=payload.channel,
        message_text=payload.message_text,
        response_text=payload.response_text,
        notes=payload.notes,
        occurred_at=payload.occurred_at,
    )
    db.add(event)
    conversation.status = status_by_event[payload.event_type]
    db.commit()
    db.refresh(event)
    return event


@router.get(
    "/conversations/{conversation_id}/engagement-events",
    response_model=list[EngagementRead],
)
def list_engagement_events(conversation_id: int, db: Session = Depends(get_db)):
    if not db.get(Conversation, conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return list(
        db.scalars(
            select(EngagementEvent)
            .where(EngagementEvent.conversation_id == conversation_id)
            .order_by(EngagementEvent.occurred_at.asc(), EngagementEvent.id.asc())
        )
    )


@router.post(
    "/conversations/{conversation_id}/qualifications",
    response_model=QualificationResult,
)
def create_qualification(
    conversation_id: int,
    payload: QualificationInput,
    db: Session = Depends(get_db),
) -> QualificationResult:
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.status not in {"REPLIED", "QUALIFICATION_STARTED", "NURTURING"}:
        raise HTTPException(
            status_code=409,
            detail="Qualification requires a recorded reply or an active qualification",
        )

    result = qualify_contact(payload)
    record = QualificationRecord(
        conversation_id=conversation_id,
        input_payload=payload.model_dump(mode="json"),
        traffic_light=result.traffic_light.value,
        status=result.status.value,
        action=result.action.value,
        radar_state=result.radar_state.value,
        recommended_path=result.recommended_path.value,
        path_requires_human_confirmation=result.path_requires_human_confirmation,
        crm_transfer_allowed=result.crm_transfer_allowed,
        calendar_access_allowed=result.calendar_access_allowed,
        reasons=result.reasons,
        missing_information=result.missing_information,
    )
    db.add(record)
    conversation.status = result.radar_state.value
    db.commit()
    return result


@router.get("/conversations/{conversation_id}/qualifications")
def list_qualifications(conversation_id: int, db: Session = Depends(get_db)):
    if not db.get(Conversation, conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    records = list(
        db.scalars(
            select(QualificationRecord)
            .where(QualificationRecord.conversation_id == conversation_id)
            .order_by(QualificationRecord.id.asc())
        )
    )
    return [
        {
            "id": item.id,
            "conversation_id": item.conversation_id,
            "input_payload": item.input_payload,
            "traffic_light": item.traffic_light,
            "status": item.status,
            "action": item.action,
            "radar_state": item.radar_state,
            "recommended_path": item.recommended_path,
            "path_requires_human_confirmation": item.path_requires_human_confirmation,
            "crm_transfer_allowed": item.crm_transfer_allowed,
            "calendar_access_allowed": item.calendar_access_allowed,
            "reasons": item.reasons,
            "missing_information": item.missing_information,
            "created_at": item.created_at,
        }
        for item in records
    ]


@router.post("/qualification/evaluate", response_model=QualificationResult)
def evaluate_qualification(payload: QualificationInput) -> QualificationResult:
    return qualify_contact(payload)
