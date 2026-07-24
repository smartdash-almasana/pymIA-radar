from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.assessment_v2 import SemanticAssessmentV2
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.discovery import DiscoveryCandidate, DiscoveryOutcome
from app.models.engagement import EngagementEvent
from app.models.qualification import QualificationRecord
from app.models.review import ReviewDecision
from app.discovery_service import (
    DiscoveryPreconditionError,
    move_candidate,
    require_prequalification_eligibility,
    upsert_outcome,
)
from app.discovery.last30days_adapter import Last30DaysAdapterError
from app.discovery.operational_scan import (
    OperationalScanError,
    load_operational_queries,
    run_operational_scan,
)
from app.qualification import qualify_contact
from app.lab_service import list_experiments, list_lab_case_options, run_comparison_experiment
from app.schemas.assessment import AssessmentResult
from app.schemas.assessment_v3 import ConversationAssessmentV3Result
from app.schemas.conversation import (
    ConversationCreate,
    ConversationRead,
    conversation_orm_payload,
)
from app.schemas.discovery import (
    DiscoveryCandidateRead,
    DiscoveryOutcomeRead,
    DiscoveryOutcomeUpsert,
    RevealedAffinityLevel,
)
from app.schemas.discovery_scan import (
    OperationalScanRequest,
    OperationalScanResult,
    SearchQueryRead,
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
from app.semantics.semantic_cascade_v1 import assess_conversation_cascade_v1
from app.services.semantic_integration import persist_cascade_assessment
from app.services.approved_opportunity import (
    create_opportunity_from_review,
    get_opportunity,
    list_opportunities,
    opportunity_to_json,
    opportunities_to_csv,
)
from app.schemas.approved_opportunity_v1 import ApprovedOpportunityRead, OpportunityStatus
from app.semantics.llm_classifier import assess_with_optional_llm_details
from app.workflow import DiscoveryState, DiscoveryTransitionError

router = APIRouter(prefix="/api")


class LabExperimentRequest(BaseModel):
    source: str = "corpus"
    case_ids: list[str] | None = None
    input_text: str | None = None
    providers: list[str] = Field(default_factory=lambda: ["agnes", "gemma"])
    repetitions: int = 1
    experiment_id: str = "experimento1"


@router.get("/lab/cases")
def get_lab_cases() -> list[dict[str, str]]:
    return list_lab_case_options()


@router.get("/lab/experiments")
def get_lab_experiments() -> list[dict[str, str]]:
    return list_experiments()


@router.post("/lab/experiments")
def create_lab_experiment(
    payload: LabExperimentRequest, db: Session = Depends(get_db)
) -> dict:
    try:
        return run_comparison_experiment(
            db,
            source=payload.source,
            case_ids=payload.case_ids,
            input_text=payload.input_text,
            providers=payload.providers,
            repetitions=payload.repetitions,
            experiment_id=payload.experiment_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/discovery/search-queries", response_model=list[SearchQueryRead])
def list_operational_search_queries() -> list[SearchQueryRead]:
    return [SearchQueryRead.model_validate(item.model_dump()) for item in load_operational_queries()]


@router.post("/discovery/scan", response_model=OperationalScanResult)
def execute_operational_scan(
    payload: OperationalScanRequest,
    db: Session = Depends(get_db),
) -> OperationalScanResult:
    try:
        return run_operational_scan(db, payload)
    except OperationalScanError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Last30DaysAdapterError as exc:
        raise HTTPException(
            status_code=503,
            detail="Discovery search is unavailable; verify last30days configuration",
        ) from exc


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

    execution = assess_with_optional_llm_details(
        f"{conversation.title or ''}\n{conversation.text}\n{conversation.context or ''}",
        enabled=settings.semantic_llm_enabled,
        model_name=settings.semantic_llm_model or settings.openai_model,
        provider_name=settings.semantic_llm_provider,
        base_url=settings.semantic_llm_base_url,
        api_key=settings.semantic_llm_api_key or settings.openai_api_key,
    )
    result = execution.result
    record = SemanticAssessmentV2(
        conversation_id=conversation.id,
        thematic_affinity=result.thematic_affinity,
        values_affinity=result.values_affinity,
        intent_score=result.intent_score,
        declared_capacity=result.declared_capacity.value,
        decision_stage=result.decision_stage.value,
        evidence_quality=result.evidence_quality,
        false_positive_risk=result.false_positive_risk.value,
        review_priority=result.review_priority,
        probable_archetype=(
            result.probable_archetype.value if result.probable_archetype else None
        ),
        archetype_confidence=result.archetype_confidence,
        archetype_evidence=result.archetype_evidence,
        positive_signals=result.positive_signals,
        negative_signals=result.negative_signals,
        objections=result.objections,
        missing_information=result.missing_information,
        evidence_fragments=result.evidence_fragments,
        recommended_action=result.recommended_action.value,
        human_review_required=result.human_review_required,
        provisional=result.provisional,
        semantic_engine=execution.semantic_engine,
        model_name=execution.model_name,
    )
    db.add(record)
    conversation.status = (
        "REVIEW_PENDING"
        if result.recommended_action.value != "DESCARTAR"
        else "DISCARDED"
    )
    db.commit()
    return result


@router.get("/conversations/{conversation_id}/assessments")
def list_assessments(conversation_id: int, db: Session = Depends(get_db)):
    if not db.get(Conversation, conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    records = list(
        db.scalars(
            select(SemanticAssessmentV2)
            .where(SemanticAssessmentV2.conversation_id == conversation_id)
            .order_by(SemanticAssessmentV2.id.asc())
        )
    )
    return [
        {
            "id": item.id,
            "conversation_id": item.conversation_id,
            "thematic_affinity": item.thematic_affinity,
            "values_affinity": item.values_affinity,
            "intent_score": item.intent_score,
            "declared_capacity": item.declared_capacity,
            "decision_stage": item.decision_stage,
            "evidence_quality": item.evidence_quality,
            "false_positive_risk": item.false_positive_risk,
            "review_priority": item.review_priority,
            "probable_archetype": item.probable_archetype,
            "archetype_confidence": item.archetype_confidence,
            "archetype_evidence": item.archetype_evidence,
            "positive_signals": item.positive_signals,
            "negative_signals": item.negative_signals,
            "objections": item.objections,
            "missing_information": item.missing_information,
            "evidence_fragments": item.evidence_fragments,
            "recommended_action": item.recommended_action,
            "human_review_required": item.human_review_required,
            "provisional": item.provisional,
            "semantic_engine": item.semantic_engine,
            "model_name": item.model_name,
            "created_at": item.created_at,
        }
        for item in records
    ]


@router.post(
    "/conversations/{conversation_id}/assessments/v3",
    response_model=ConversationAssessmentV3Result,
)
def create_conversation_assessment_v3(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationAssessmentV3Result:
    conversation = db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    cascade = assess_conversation_cascade_v1(
        conversation_id=conversation.id,
        title=conversation.title,
        text=conversation.text,
        context=conversation.context,
        agnes_enabled=settings.semantic_llm_enabled,
        agnes_model_name=settings.semantic_llm_model or settings.openai_model,
        agnes_base_url=settings.semantic_llm_base_url,
        agnes_api_key=settings.semantic_llm_api_key or settings.openai_api_key,
        gemma_enabled=bool(settings.gemini_api_key),
        gemma_model_name=settings.gemini_model,
        gemma_base_url=settings.gemini_base_url,
        gemma_api_key=settings.gemini_api_key,
    )
    record = persist_cascade_assessment(db, cascade, conversation)
    return ConversationAssessmentV3Result.model_validate(record)


@router.get(
    "/conversations/{conversation_id}/assessments/v3",
    response_model=list[ConversationAssessmentV3Result],
)
def list_conversation_assessments_v3(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> list[ConversationAssessmentV3Result]:
    if not db.get(Conversation, conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    records = list(
        db.scalars(
            select(ConversationAssessmentV3)
            .where(ConversationAssessmentV3.conversation_id == conversation_id)
            .order_by(ConversationAssessmentV3.id.asc())
        )
    )
    return [ConversationAssessmentV3Result.model_validate(item) for item in records]


@router.get("/conversations/{conversation_id}/assessments/v3/{assessment_id}/cascade")
def get_conversation_assessment_v3_cascade(
    conversation_id: int,
    assessment_id: int,
    db: Session = Depends(get_db),
) -> dict:
    record = db.get(ConversationAssessmentV3, assessment_id)
    if record is None or record.conversation_id != conversation_id:
        raise HTTPException(status_code=404, detail="V3 assessment not found")
    return {
        "assessment_id": record.id,
        "conversation_id": record.conversation_id,
        "cascade_schema_version": record.cascade_schema_version,
        "gemma_review_triggered": record.gemma_review_triggered,
        "gemma_trigger_reasons": record.gemma_trigger_reasons,
        "gemma_review": record.gemma_review,
        "deterministic_resolution": record.deterministic_resolution,
        "resolution_note": record.resolution_note,
        "primary_provider_attempted": record.primary_provider_attempted,
        "primary_provider_used": record.primary_provider_used,
        "provider_failover": record.provider_failover,
        "provider_failure_code": record.provider_failure_code,
        "provider_failure_detail": record.provider_failure_detail,
    }


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

    if payload.decision == ReviewDecisionType.APPROVE_DISCOVERY_CONTACT:
        completed_v3 = db.scalar(
            select(ConversationAssessmentV3.id).where(
                ConversationAssessmentV3.conversation_id == conversation_id,
                ConversationAssessmentV3.assessment_status == "COMPLETED",
            )
        )
        if completed_v3 is None:
            raise HTTPException(
                status_code=409,
                detail="Discovery approval requires a completed V3 assessment",
            )
        candidate = db.scalar(
            select(DiscoveryCandidate).where(
                DiscoveryCandidate.origin_conversation_id == conversation_id
            )
        )
        if candidate is None:
            candidate = DiscoveryCandidate(
                origin_conversation_id=conversation.id,
                public_name=conversation.author_name,
                public_identity_reference=f"{conversation.source}:{conversation.external_id}",
                public_profile_url=conversation.conversation_url,
                created_by=payload.reviewer_identity or "",
            )
            db.add(candidate)
            db.flush()
        move_candidate(candidate, DiscoveryState.DISCOVERY_APPROACH_APPROVED)
        review = ReviewDecision(
            conversation_id=conversation_id,
            decision=payload.decision.value,
            edited_response=payload.edited_response,
            reviewer_notes=payload.reviewer_notes,
            created_by=payload.reviewer_identity or None,
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return ReviewRead.model_validate(review).model_copy(
            update={"discovery_candidate_id": candidate.id}
        )

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
        created_by=payload.reviewer_identity or None,
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
    if not db.get(Conversation, conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    raise HTTPException(
        status_code=409,
        detail="New engagement events require a discovery_candidate_id endpoint",
    )


@router.get("/discovery-candidates", response_model=list[DiscoveryCandidateRead])
def list_discovery_candidates(db: Session = Depends(get_db)) -> list[DiscoveryCandidate]:
    return list(db.scalars(select(DiscoveryCandidate).order_by(DiscoveryCandidate.id.desc())))


@router.get(
    "/discovery-candidates/{candidate_id}", response_model=DiscoveryCandidateRead
)
def get_discovery_candidate(candidate_id: int, db: Session = Depends(get_db)) -> DiscoveryCandidate:
    candidate = db.get(DiscoveryCandidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Discovery candidate not found")
    return candidate


@router.post(
    "/discovery-candidates/{candidate_id}/engagement-events",
    response_model=EngagementRead,
)
def create_candidate_engagement_event(
    candidate_id: int,
    payload: EngagementCreate,
    db: Session = Depends(get_db),
) -> EngagementEvent:
    candidate = db.get(DiscoveryCandidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Discovery candidate not found")
    try:
        event_target = {
            EngagementEventType.CONTACTED: DiscoveryState.DISCOVERY_CONTACTED,
            EngagementEventType.REPLIED: DiscoveryState.DISCOVERY_REPLIED,
            EngagementEventType.DO_NOT_CONTACT: DiscoveryState.DO_NOT_CONTACT,
        }.get(payload.event_type)
        if event_target is not None:
            move_candidate(candidate, event_target)
    except DiscoveryTransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    event = EngagementEvent(
        conversation_id=candidate.origin_conversation_id,
        discovery_candidate_id=candidate.id,
        event_type=payload.event_type.value,
        channel=payload.channel,
        message_text=payload.message_text,
        response_text=payload.response_text,
        notes=payload.notes,
        occurred_at=payload.occurred_at,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get(
    "/discovery-candidates/{candidate_id}/engagement-events",
    response_model=list[EngagementRead],
)
def list_candidate_engagement_events(candidate_id: int, db: Session = Depends(get_db)) -> list[EngagementEvent]:
    if db.get(DiscoveryCandidate, candidate_id) is None:
        raise HTTPException(status_code=404, detail="Discovery candidate not found")
    return list(
        db.scalars(
            select(EngagementEvent)
            .where(EngagementEvent.discovery_candidate_id == candidate_id)
            .order_by(EngagementEvent.occurred_at.asc(), EngagementEvent.id.asc())
        )
    )


@router.put(
    "/discovery-candidates/{candidate_id}/outcome",
    response_model=DiscoveryOutcomeRead,
)
def put_discovery_outcome(
    candidate_id: int,
    payload: DiscoveryOutcomeUpsert,
    db: Session = Depends(get_db),
) -> DiscoveryOutcome:
    candidate = db.get(DiscoveryCandidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Discovery candidate not found")
    try:
        outcome = upsert_outcome(db, candidate, payload)
    except DiscoveryPreconditionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    db.commit()
    db.refresh(outcome)
    return outcome


@router.get(
    "/discovery-candidates/{candidate_id}/outcome",
    response_model=DiscoveryOutcomeRead,
)
def get_discovery_outcome(candidate_id: int, db: Session = Depends(get_db)) -> DiscoveryOutcome:
    outcome = db.scalar(
        select(DiscoveryOutcome).where(DiscoveryOutcome.discovery_candidate_id == candidate_id)
    )
    if outcome is None:
        raise HTTPException(status_code=404, detail="Discovery outcome not found")
    return outcome


@router.post("/discovery-candidates/{candidate_id}/prequalification-invitation", response_model=DiscoveryCandidateRead)
def invite_to_prequalification(candidate_id: int, db: Session = Depends(get_db)) -> DiscoveryCandidate:
    candidate = db.get(DiscoveryCandidate, candidate_id)
    outcome = db.scalar(select(DiscoveryOutcome).where(DiscoveryOutcome.discovery_candidate_id == candidate_id))
    if candidate is None:
        raise HTTPException(status_code=404, detail="Discovery candidate not found")
    if outcome is None or outcome.revealed_affinity_level not in {RevealedAffinityLevel.PARTIAL.value, RevealedAffinityLevel.CLEAR.value} or not outcome.wants_to_continue:
        raise HTTPException(status_code=409, detail="Prequalification invitation requires revealed affinity and continuing intent")
    try:
        move_candidate(candidate, DiscoveryState.PREQUALIFICATION_INVITED)
    except DiscoveryTransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    db.commit()
    db.refresh(candidate)
    return candidate


@router.post("/discovery-candidates/{candidate_id}/prequalification-acceptance", response_model=DiscoveryCandidateRead)
def accept_prequalification(candidate_id: int, db: Session = Depends(get_db)) -> DiscoveryCandidate:
    candidate = db.get(DiscoveryCandidate, candidate_id)
    outcome = db.scalar(select(DiscoveryOutcome).where(DiscoveryOutcome.discovery_candidate_id == candidate_id))
    if candidate is None:
        raise HTTPException(status_code=404, detail="Discovery candidate not found")
    if outcome is None or not outcome.consent_to_prequalification or outcome.consent_recorded_at is None or not outcome.wants_to_continue or outcome.revealed_affinity_level not in {RevealedAffinityLevel.PARTIAL.value, RevealedAffinityLevel.CLEAR.value}:
        raise HTTPException(status_code=409, detail="Prequalification acceptance requires recorded consent, affinity, and continuing intent")
    try:
        move_candidate(candidate, DiscoveryState.PREQUALIFICATION_ACCEPTED)
    except DiscoveryTransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    db.commit()
    db.refresh(candidate)
    return candidate


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
    candidate = db.scalar(
        select(DiscoveryCandidate).where(
            DiscoveryCandidate.origin_conversation_id == conversation_id
        )
    )
    outcome = (
        db.scalar(
            select(DiscoveryOutcome).where(
                DiscoveryOutcome.discovery_candidate_id == candidate.id
            )
        )
        if candidate is not None
        else None
    )
    try:
        require_prequalification_eligibility(candidate, outcome)
    except DiscoveryPreconditionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _create_qualification_record(db, conversation_id, candidate, outcome, payload)


@router.post(
    "/discovery-candidates/{candidate_id}/qualifications",
    response_model=QualificationResult,
)
def create_candidate_qualification(
    candidate_id: int,
    payload: QualificationInput,
    db: Session = Depends(get_db),
) -> QualificationResult:
    candidate = db.get(DiscoveryCandidate, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Discovery candidate not found")
    outcome = db.scalar(
        select(DiscoveryOutcome).where(
            DiscoveryOutcome.discovery_candidate_id == candidate.id
        )
    )
    try:
        require_prequalification_eligibility(candidate, outcome)
    except DiscoveryPreconditionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _create_qualification_record(
        db, candidate.origin_conversation_id, candidate, outcome, payload
    )


def _create_qualification_record(
    db: Session,
    conversation_id: int,
    candidate: DiscoveryCandidate,
    outcome: DiscoveryOutcome,
    payload: QualificationInput,
) -> QualificationResult:
    result = qualify_contact(payload)
    record = QualificationRecord(
        conversation_id=conversation_id,
        discovery_candidate_id=candidate.id,
        discovery_outcome_id=outcome.id,
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


@router.post("/opportunities/from-review/{review_id}", response_model=ApprovedOpportunityRead)
def create_opportunity(review_id: int, db: Session = Depends(get_db)):
    opportunity = create_opportunity_from_review(db, review_id)
    if opportunity is None:
        raise HTTPException(status_code=400, detail="Cannot create opportunity from this review")
    return ApprovedOpportunityRead.model_validate(opportunity)


@router.get("/opportunities/export/json")
def export_opportunities_json(db: Session = Depends(get_db)):
    from fastapi.responses import JSONResponse

    opportunities = list_opportunities(db)
    data = [opportunity_to_json(o) for o in opportunities]
    return JSONResponse(content=data)


@router.get("/opportunities/export/csv")
def export_opportunities_csv(db: Session = Depends(get_db)):
    from fastapi.responses import PlainTextResponse

    opportunities = list_opportunities(db)
    content = opportunities_to_csv(opportunities)
    return PlainTextResponse(content=content, media_type="text/csv")


@router.get("/opportunities/{opportunity_id}", response_model=ApprovedOpportunityRead)
def read_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = get_opportunity(db, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return ApprovedOpportunityRead.model_validate(opportunity)


@router.get("/opportunities", response_model=list[ApprovedOpportunityRead])
def list_opportunities_endpoint(
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return [
        ApprovedOpportunityRead.model_validate(o)
        for o in list_opportunities(db, status=status, limit=limit, offset=offset)
    ]
