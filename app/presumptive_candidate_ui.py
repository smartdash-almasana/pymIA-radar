from __future__ import annotations

from dataclasses import dataclass

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.conversation_participant import ConversationParticipant
from app.models.presumptive_candidate import PresumptiveCandidate
from app.models.public_actor import PublicActor
from app.schemas.presumptive_candidate import PresumptiveCandidateStatus
from app.services.presumptive_candidates import (
    discard_presumptive_candidate,
    observe_presumptive_candidate,
    public_actor_key,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@dataclass(frozen=True)
class PresumptiveCandidateView:
    id: int
    actor_key: str
    public_username: str
    display_name: str | None
    platform: str
    public_profile_url: str | None
    conversation_title: str
    conversation_text: str
    conversation_context: str | None
    source_url: str
    platform_comment_id: str | None
    role: str
    real_topic: str
    contextual_meaning: str
    apparent_affinity: str
    apparent_intention: str
    evidence_fragments: list[str]
    false_positive_risk: str
    review_priority: int
    status: str
    skill_version: str
    model_name: str | None

    @property
    def primary_evidence(self) -> str:
        if not self.evidence_fragments:
            return "Sin evidencia literal registrada."
        return self.evidence_fragments[0]


def _candidate_rows(db: Session, *, include_discarded: bool = False) -> list[PresumptiveCandidateView]:
    statement = (
        select(
            PresumptiveCandidate,
            PublicActor,
            Conversation,
            ConversationAssessmentV3,
            ConversationParticipant,
        )
        .join(PublicActor, PublicActor.id == PresumptiveCandidate.public_actor_id)
        .join(Conversation, Conversation.id == PresumptiveCandidate.conversation_id)
        .join(ConversationAssessmentV3, ConversationAssessmentV3.id == PresumptiveCandidate.assessment_id)
        .join(
            ConversationParticipant,
            and_(
                ConversationParticipant.conversation_id == PresumptiveCandidate.conversation_id,
                ConversationParticipant.public_actor_id == PresumptiveCandidate.public_actor_id,
            ),
        )
        .order_by(PresumptiveCandidate.review_priority.desc(), PresumptiveCandidate.id.desc())
    )
    if not include_discarded:
        statement = statement.where(PresumptiveCandidate.status != PresumptiveCandidateStatus.DISCARDED.value)
    rows = db.execute(statement).all()
    return [_to_view(candidate, actor, conversation, assessment, participant) for candidate, actor, conversation, assessment, participant in rows]


def _candidate_row(db: Session, candidate_id: int) -> PresumptiveCandidateView:
    statement = (
        select(
            PresumptiveCandidate,
            PublicActor,
            Conversation,
            ConversationAssessmentV3,
            ConversationParticipant,
        )
        .join(PublicActor, PublicActor.id == PresumptiveCandidate.public_actor_id)
        .join(Conversation, Conversation.id == PresumptiveCandidate.conversation_id)
        .join(ConversationAssessmentV3, ConversationAssessmentV3.id == PresumptiveCandidate.assessment_id)
        .join(
            ConversationParticipant,
            and_(
                ConversationParticipant.conversation_id == PresumptiveCandidate.conversation_id,
                ConversationParticipant.public_actor_id == PresumptiveCandidate.public_actor_id,
            ),
        )
        .where(PresumptiveCandidate.id == candidate_id)
    )
    row = db.execute(statement).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Presumptive candidate not found")
    candidate, actor, conversation, assessment, participant = row
    return _to_view(candidate, actor, conversation, assessment, participant)


def _to_view(
    candidate: PresumptiveCandidate,
    actor: PublicActor,
    conversation: Conversation,
    assessment: ConversationAssessmentV3,
    participant: ConversationParticipant,
) -> PresumptiveCandidateView:
    return PresumptiveCandidateView(
        id=candidate.id,
        actor_key=public_actor_key(actor.platform, actor.platform_actor_id),
        public_username=actor.public_username,
        display_name=actor.display_name,
        platform=actor.platform,
        public_profile_url=actor.public_profile_url,
        conversation_title=conversation.title or "Conversación sin título",
        conversation_text=conversation.text,
        conversation_context=conversation.context,
        source_url=conversation.conversation_url,
        platform_comment_id=participant.platform_comment_id,
        role=participant.role,
        real_topic=assessment.real_topic or "Sin tema registrado",
        contextual_meaning=assessment.contextual_meaning or "Sin contexto semántico registrado",
        apparent_affinity=candidate.apparent_affinity,
        apparent_intention=candidate.apparent_intention,
        evidence_fragments=list(assessment.evidence_fragments or []),
        false_positive_risk=candidate.false_positive_risk,
        review_priority=candidate.review_priority,
        status=candidate.status,
        skill_version=candidate.skill_version,
        model_name=candidate.model_name,
    )


@router.get("/radar/presumptive-candidates", response_class=HTMLResponse)
def presumptive_candidate_list(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "radar/presumptive_candidates.html",
        {"request": request, "candidates": _candidate_rows(db)},
    )


@router.get("/radar/presumptive-candidates/{candidate_id}", response_class=HTMLResponse)
def presumptive_candidate_detail(
    request: Request,
    candidate_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "radar/presumptive_candidate_detail.html",
        {"request": request, "candidate": _candidate_row(db, candidate_id)},
    )


@router.post("/htmx/presumptive-candidates/{candidate_id}/observe", response_class=HTMLResponse)
def observe_candidate_status(
    request: Request,
    candidate_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    candidate = observe_presumptive_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Presumptive candidate not found")
    db.commit()
    return templates.TemplateResponse(
        request,
        "radar/partials/presumptive_candidate_status.html",
        {"request": request, "candidate": candidate},
    )


@router.post("/htmx/presumptive-candidates/{candidate_id}/discard", response_class=HTMLResponse)
def discard_candidate_status(
    request: Request,
    candidate_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    candidate = discard_presumptive_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Presumptive candidate not found")
    db.commit()
    return templates.TemplateResponse(
        request,
        "radar/partials/presumptive_candidate_status.html",
        {"request": request, "candidate": candidate},
    )
