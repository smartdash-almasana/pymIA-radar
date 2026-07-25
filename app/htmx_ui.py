from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import cos, pi, sin

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.discovery.lightweight_live_search import is_relevant_conversation, run_lightweight_live_search
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.discovery import DiscoveryCandidate
from app.models.engagement import EngagementEvent
from app.models.review import ReviewDecision
from app.schemas.review import ReviewDecisionType
from app.workflow import DiscoveryState

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@dataclass(frozen=True)
class ConversationCard:
    id: int
    title: str
    source: str
    source_key: str
    author: str
    date: str
    url: str
    text: str
    query: str
    status: str
    status_key: str
    affinity: str
    affinity_key: str
    intention: str
    intention_key: str
    risk: str
    risk_key: str
    priority: int
    topic: str
    context: str
    evidence: list[str]
    contradictions: list[str]
    missing: list[str]
    review_reason: str
    initial_evaluation: str
    additional_review: str
    additional_review_reason: str
    final_resolution: str
    human_review_required: str
    x: int
    y: int
    size: int


AFFINITY = {
    "CLEAR": ("Alta", "alta"),
    "POSSIBLE": ("Media", "media"),
    "NONE": ("Nula", "baja"),
    None: ("Sin evaluación", "sin-evaluacion"),
}
INTENTION = {
    "ACTION_ORIENTED": ("Acción declarada", "accion"),
    "EXPLORATION": ("Exploración", "exploracion"),
    "THEMATIC_SYMPATHY": ("Simpatía temática", "simpatia"),
    "NONE": ("Sin intención relacionada", "ninguna"),
    None: ("Sin evaluación", "sin-evaluacion"),
}
RISK = {
    "LOW": ("Bajo", "bajo"),
    "MEDIUM": ("Medio", "medio"),
    "HIGH": ("Alto", "alto"),
    None: ("Sin evaluación", "sin-evaluacion"),
}
STATUS = {
    "detected": ("Para revisar", "revisar"),
    "DETECTED": ("Para revisar", "revisar"),
    "REVIEW_PENDING": ("Para revisar", "revisar"),
    "ASSESSED": ("Para revisar", "revisar"),
    "OBSERVING": ("Observación", "observacion"),
    "DISCARDED": ("Descartada", "descartado"),
    "DO_NOT_CONTACT": ("No contactar", "no_contactar"),
}
SIGNAL_LANES = [
    {"key": "alta", "label": "Alta afinidad", "description": "Señales más claras; requieren revisión humana prioritaria."},
    {"key": "media", "label": "Afinidad media", "description": "Hay indicios, pero falta contexto antes de decidir."},
    {"key": "sin-evaluacion", "label": "Sin evaluación", "description": "Conversaciones reales pendientes de lectura semántica."},
    {"key": "baja", "label": "Baja o ruido", "description": "Coincidencias débiles, ruido o riesgo alto de falso positivo."},
]

DECISIONS = {
    "classify_candidate": ("IDENTIFY_DISCOVERY_CANDIDATE", "Persona candidata identificada"),
    "prepare_public_reply": ("PREPARE_PUBLICATION_REPLY", "Borrador para publicación preparado"),
    "discard": (ReviewDecisionType.DISCARD.value, "Descartada"),
}



def _is_operational_conversation(conversation: Conversation) -> bool:
    source = str(conversation.source or "").lower()
    external_id = str(conversation.external_id or "").lower()
    url = str(conversation.conversation_url or "").lower()
    if source in {"test", "test_source", "fixture", "mock"}:
        return False
    if external_id.startswith("test-") or external_id.startswith("fixture-") or external_id.startswith("mock-"):
        return False
    if "example.com" in url or "iana.org/domains/example" in url:
        return False
    return is_relevant_conversation(conversation)

def _label_source(value: str | None) -> str:
    labels = {"reddit": "Reddit", "facebook": "Facebook", "linkedin": "LinkedIn", "instagram": "Instagram", "x": "X", "github": "GitHub", "youtube": "YouTube", "hackernews": "Hacker News"}
    key = str(value or "").lower()
    return labels.get(key, value or "Fuente pública")


def _date(value: datetime | None) -> str:
    return value.strftime("%d/%m/%Y") if value else "Sin fecha"


def _short(text: str | None, length: int = 92) -> str:
    clean = " ".join((text or "").split())
    return clean if len(clean) <= length else clean[: length - 1].rstrip() + "…"


def _latest_assessments(db: Session) -> dict[int, ConversationAssessmentV3]:
    out: dict[int, ConversationAssessmentV3] = {}
    try:
        rows = db.scalars(select(ConversationAssessmentV3).order_by(ConversationAssessmentV3.conversation_id, ConversationAssessmentV3.id.desc()))
        for row in rows:
            out.setdefault(row.conversation_id, row)
    except SQLAlchemyError:
        db.rollback()
        return {}
    return out


def _latest_reviews(db: Session) -> dict[int, ReviewDecision]:
    out: dict[int, ReviewDecision] = {}
    rows = db.scalars(select(ReviewDecision).order_by(ReviewDecision.conversation_id, ReviewDecision.id.desc()))
    for row in rows:
        out.setdefault(row.conversation_id, row)
    return out


def _candidates(db: Session) -> dict[int, DiscoveryCandidate]:
    return {row.origin_conversation_id: row for row in db.scalars(select(DiscoveryCandidate))}


def _position(conversation_id: int, assessment: ConversationAssessmentV3 | None) -> tuple[int, int, int]:
    affinity = assessment.apparent_affinity if assessment else None
    risk = assessment.false_positive_risk if assessment else None
    radius = {"CLEAR": 18, "POSSIBLE": 30, "NONE": 42, None: 36}.get(affinity, 36)
    radius += {"LOW": -4, "MEDIUM": 4, "HIGH": 9, None: 0}.get(risk, 0)
    angle = ((conversation_id * 137) % 360) * pi / 180
    return round(50 + cos(angle) * radius), round(50 + sin(angle) * radius * 0.72), max(74, min(132, 72 + (assessment.review_priority if assessment else 20)))


def _to_card(conversation: Conversation, assessment: ConversationAssessmentV3 | None, candidate: DiscoveryCandidate | None, review: ReviewDecision | None) -> ConversationCard:
    if candidate and candidate.discovery_state == DiscoveryState.DISCOVERY_CANDIDATE.value:
        status, status_key, final = "Persona candidata", "aprobado", "Identificada para seguimiento humano"
    elif candidate and candidate.discovery_state == DiscoveryState.DISCOVERY_APPROACH_APPROVED.value:
        status, status_key, final = "Acercamiento aprobado", "aprobado", "Resolución humana: acercamiento aprobado"
    elif candidate and candidate.discovery_state == DiscoveryState.DO_NOT_CONTACT.value:
        status, status_key, final = "No contactar", "no_contactar", "Resolución humana: no contactar"
    elif review and review.decision == ReviewDecisionType.KEEP_OBSERVING.value:
        status, status_key, final = "Observación", "observacion", "Resolución humana: observar"
    elif review and review.decision == ReviewDecisionType.DISCARD.value:
        status, status_key, final = "Descartada", "descartado", "Resolución humana: descartar"
    elif review and review.decision == ReviewDecisionType.DO_NOT_CONTACT.value:
        status, status_key, final = "No contactar", "no_contactar", "Resolución humana: no contactar"
    else:
        status, status_key = STATUS.get(conversation.status, ("Para revisar", "revisar"))
        final = assessment.resolution_note if assessment and assessment.resolution_note else "Revisión humana pendiente"
    affinity, affinity_key = AFFINITY.get(assessment.apparent_affinity if assessment else None, AFFINITY[None])
    intention, intention_key = INTENTION.get(assessment.apparent_intention if assessment else None, INTENTION[None])
    risk, risk_key = RISK.get(assessment.false_positive_risk if assessment else None, RISK[None])
    x, y, size = _position(conversation.id, assessment)
    return ConversationCard(
        id=conversation.id,
        title=conversation.title or _short(conversation.text) or "Conversación sin título",
        source=_label_source(conversation.source),
        source_key=str(conversation.source or "").lower(),
        author=conversation.author_name or "Autor público no identificado",
        date=_date(conversation.published_at),
        url=conversation.conversation_url,
        text=conversation.text,
        query=conversation.query_origin or "Consulta no registrada",
        status=status,
        status_key=status_key,
        affinity=affinity,
        affinity_key=affinity_key,
        intention=intention,
        intention_key=intention_key,
        risk=risk,
        risk_key=risk_key,
        priority=assessment.review_priority if assessment else 0,
        topic=assessment.real_topic if assessment and assessment.real_topic else "Pendiente de evaluación",
        context=assessment.contextual_meaning if assessment and assessment.contextual_meaning else conversation.context or "Pendiente de evaluación",
        evidence=list(assessment.evidence_fragments if assessment else []),
        contradictions=list(assessment.contradictions if assessment else []),
        missing=list(assessment.missing_context if assessment else []),
        review_reason=assessment.human_review_reason if assessment and assessment.human_review_reason else "Pendiente de revisión humana.",
        initial_evaluation="Evaluación semántica con IA",
        additional_review="Revisión semántica adicional" if assessment and assessment.gemma_review_triggered else "Revisión adicional no requerida",
        additional_review_reason="; ".join(assessment.gemma_trigger_reasons) if assessment and assessment.gemma_trigger_reasons else "Sin motivo adicional registrado",
        final_resolution=final,
        human_review_required="Sí" if not assessment or assessment.human_review_required else "No",
        x=x,
        y=y,
        size=size,
    )


def _cards(db: Session) -> list[ConversationCard]:
    assessments = _latest_assessments(db)
    candidates = _candidates(db)
    reviews = _latest_reviews(db)
    rows = db.scalars(select(Conversation).order_by(Conversation.id.desc()))
    return [
        _to_card(row, assessments.get(row.id), candidates.get(row.id), reviews.get(row.id))
        for row in rows
        if _is_operational_conversation(row)
    ]


def _filter(cards: list[ConversationCard], status: str, source: str, affinity: str, intent: str, risk: str) -> list[ConversationCard]:
    out = [c for c in cards if c.status_key != "descartado"]
    if status == "descartado":
        return []
    if status != "todos":
        out = [c for c in out if (c.affinity_key == "alta" if status == "alta" else c.status_key == status)]
    if source != "todas":
        out = [c for c in out if c.source_key == source]
    if affinity != "todas":
        out = [c for c in out if c.affinity_key == affinity]
    if intent != "todas":
        out = [c for c in out if c.intention_key == intent]
    if risk != "todos":
        out = [c for c in out if c.risk_key == risk]
    return out


def _counts(cards: list[ConversationCard]) -> dict[str, int]:
    visible = [c for c in cards if c.status_key != "descartado"]
    return {
        "found": len(visible),
        "review": len([c for c in visible if c.status_key == "revisar"]),
        "high": len([c for c in visible if c.affinity_key == "alta"]),
        "watch": len([c for c in visible if c.status_key == "observacion"]),
        "do_not_contact": len([c for c in visible if c.status_key == "no_contactar"]),
    }


def _context(
    request: Request,
    db: Session,
    status: str = "todos",
    source: str = "todas",
    affinity: str = "todas",
    intent: str = "todas",
    risk: str = "todos",
    page: int = 1,
) -> dict:
    cards = _cards(db)
    filtered = _filter(cards, status, source, affinity, intent, risk)
    page_size = 20
    total = len(filtered)
    page_count = max(1, (total + page_size - 1) // page_size)
    current_page = min(max(page, 1), page_count)
    start = (current_page - 1) * page_size
    return {
        "request": request,
        "conversations": filtered[start : start + page_size],
        "board_conversations": filtered[:12],
        "total_filtered": total,
        "page": current_page,
        "page_count": page_count,
        "has_previous": current_page > 1,
        "has_next": current_page < page_count,
        "signal_lanes": SIGNAL_LANES,
        "counts": _counts(cards),
        "filters": {"status": status, "source": source, "affinity": affinity, "intent": intent, "risk": risk},
    }


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    return templates.TemplateResponse(request, "radar/index.html", _context(request, db))


@router.get("/htmx/results", response_class=HTMLResponse)
def htmx_results(
    request: Request,
    status: str = Query("todos"),
    source: str = Query("todas"),
    affinity: str = Query("todas"),
    intent: str = Query("todas"),
    risk: str = Query("todos"),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "radar/partials/workspace.html",
        _context(request, db, status, source, affinity, intent, risk, page),
    )


@router.post("/htmx/search", response_class=HTMLResponse)
def htmx_search(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    summary = run_lightweight_live_search(db)
    context = _context(request, db)
    context["search_message"] = (
        f"{summary.inserted} conversaciones nuevas incorporadas"
        if summary.inserted
        else "No se encontraron conversaciones nuevas en esta ejecución"
    )
    context["search_sources"] = ", ".join(summary.sources) if summary.sources else "sin fuentes disponibles"
    return templates.TemplateResponse(request, "radar/partials/workspace.html", context)


@router.get("/htmx/indicators", response_class=HTMLResponse)
def htmx_indicators(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    cards = _cards(db)
    return templates.TemplateResponse(request, "radar/partials/indicators.html", {"request": request, "counts": _counts(cards)})


@router.get("/htmx/conversations/{conversation_id}/modal", response_class=HTMLResponse)
def modal(request: Request, conversation_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    return templates.TemplateResponse(request, "radar/partials/modal.html", {"request": request, "conversation": _one(db, conversation_id)})


@router.get("/analysis/{conversation_id}", response_class=HTMLResponse)
def analysis(request: Request, conversation_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    return templates.TemplateResponse(request, "radar/analysis.html", {"request": request, "conversation": _one(db, conversation_id)})


@router.post("/htmx/conversations/{conversation_id}/decision", response_class=HTMLResponse)
def decision(
    request: Request,
    conversation_id: int,
    decision: str = Form(...),
    lead_identity: str = Form(""),
    publication_reply: str = Form(""),
    internal_note: str = Form(""),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    error = None
    label = DECISIONS.get(decision, (None, "Decisión registrada"))[1]
    conversation = db.get(Conversation, conversation_id)
    if conversation is None or not _is_operational_conversation(conversation):
        raise HTTPException(status_code=404, detail="Conversation not found")
    lead_identity = lead_identity.strip()
    publication_reply = publication_reply.strip()
    if decision == "classify_candidate" and not lead_identity:
        error = "Para identificar una persona candidata tenés que registrar su identidad pública."
    elif decision == "prepare_public_reply" and not publication_reply:
        error = "Para preparar un mensaje tenés que escribir el borrador para la publicación."
    elif decision not in DECISIONS:
        error = "Decisión inválida."
    else:
        try:
            review_type = DECISIONS[decision][0]
            if decision == "classify_candidate":
                candidate = db.scalar(
                    select(DiscoveryCandidate).where(
                        DiscoveryCandidate.origin_conversation_id == conversation_id
                    )
                )
                if candidate is None:
                    candidate = DiscoveryCandidate(
                        origin_conversation_id=conversation.id,
                        public_name=lead_identity,
                        public_identity_reference=f"{conversation.source}:{conversation.external_id}",
                        public_profile_url=conversation.conversation_url,
                        created_by="interfaz_htmx",
                    )
                    db.add(candidate)
                    db.flush()
                else:
                    candidate.public_name = lead_identity
                conversation.status = "REVIEW_PENDING"
            elif decision == "prepare_public_reply":
                conversation.status = "REVIEW_PENDING"
            elif decision == "discard":
                conversation.status = "DISCARDED"
            notes = internal_note.strip() or None
            db.add(
                ReviewDecision(
                    conversation_id=conversation_id,
                    decision=review_type,
                    edited_response=publication_reply or None,
                    reviewer_notes=notes,
                )
            )
            db.commit()
        except ValueError as exc:
            db.rollback()
            error = str(exc)
    sent_contact = db.scalar(
        select(EngagementEvent.id).where(
            EngagementEvent.conversation_id == conversation_id,
            EngagementEvent.event_type == "CONTACTED",
        )
    ) is not None
    return templates.TemplateResponse(
        request,
        "radar/partials/decision_result.html",
        {
            "request": request,
            "error": error,
            "decision_label": label,
            "reviewer": lead_identity,
            "automatic_contact_sent": sent_contact,
        },
    )


def _one(db: Session, conversation_id: int) -> ConversationCard:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None or not _is_operational_conversation(conversation):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return _to_card(conversation, _latest_assessments(db).get(conversation_id), _candidates(db).get(conversation_id), _latest_reviews(db).get(conversation_id))
