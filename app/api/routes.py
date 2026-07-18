from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.assessment import SemanticAssessment
from app.models.review import ReviewDecision
from app.schemas.conversation import ConversationCreate, ConversationRead
from app.schemas.assessment import AssessmentResult
from app.semantics.classifier import classify_conversation

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

    item = Conversation(**payload.model_dump(mode="json"))
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

    result = classify_conversation(
        f"{conversation.title or ''}\n{conversation.text}\n{conversation.context or ''}"
    )
    record = SemanticAssessment(
        conversation_id=conversation.id,
        relevant=result.relevant,
        affinity_score=result.affinity_score,
        investment_intent=result.investment_intent,
        probable_archetype=result.probable_archetype,
        conversation_stage=result.conversation_stage,
        recommended_action=result.recommended_action,
        evidence=result.evidence,
        missing_data=result.missing_data,
        risk_flags=result.risk_flags,
        reasoning_summary=result.reasoning_summary,
    )
    db.add(record)
    conversation.status = "review" if result.relevant else "discarded"
    db.commit()
    return result

@router.post("/conversations/{conversation_id}/review")
def review_conversation(
    conversation_id: int,
    decision: str,
    edited_response: str | None = None,
    reviewer_notes: str | None = None,
    db: Session = Depends(get_db),
):
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    review = ReviewDecision(
        conversation_id=conversation_id,
        decision=decision,
        edited_response=edited_response,
        reviewer_notes=reviewer_notes,
    )
    db.add(review)
    conversation.status = decision
    db.commit()
    return {"status": "ok", "decision": decision}
