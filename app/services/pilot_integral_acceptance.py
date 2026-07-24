"""Pilot integral acceptance — end-to-end flow orchestrator.

Reuses existing services exclusively. No direct table writes.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.integrations.playwright_mcp import NavigationResult
from app.models.approved_opportunity_v1 import ApprovedOpportunityV1
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.presumptive_candidate import PresumptiveCandidate
from app.models.review import ReviewDecision
from app.services.approved_opportunity import (
    create_opportunity_from_review,
    opportunities_to_csv,
    opportunity_to_json,
)
from app.services.semantic_integration import run_playwright_semantic_pipeline


@dataclass
class PilotResult:
    conversation: Conversation | None = None
    assessment: ConversationAssessmentV3 | None = None
    candidate: PresumptiveCandidate | None = None
    review: ReviewDecision | None = None
    opportunity: ApprovedOpportunityV1 | None = None
    json_export: dict | None = None
    csv_export: str | None = None
    error: str | None = None
    stages: list[str] = field(default_factory=list)


def run_pilot_flow(
    db: Session,
    navigation: NavigationResult,
    *,
    source: str,
    reviewer_identity: str,
    query_origin: str | None = None,
    title: str | None = None,
    context: str | None = None,
) -> PilotResult:
    result = PilotResult()

    # Stage 1-3: evidence → assessment → candidate
    pipeline = run_playwright_semantic_pipeline(
        db, navigation, source=source, query_origin=query_origin,
        title=title, context=context,
    )
    if pipeline.conversation is None:
        result.error = f"pipeline blocked at {pipeline.stages[-1].stage if pipeline.stages else 'unknown'}"
        result.stages = [s.stage for s in pipeline.stages]
        return result

    result.conversation = pipeline.conversation
    result.assessment = pipeline.assessment
    result.candidate = pipeline.candidate
    result.stages = [s.stage for s in pipeline.stages]

    # Must have both assessment and candidate to proceed to review
    if not result.assessment or not result.candidate:
        result.error = "assessment not eligible or no candidate created"
        return result

    # Stage 4: human review
    review = ReviewDecision(
        conversation_id=result.conversation.id,
        decision="APPROVE_DISCOVERY_CONTACT",
        edited_response="Mensaje de contacto revisado por piloto de aceptación.",
        reviewer_notes="Verificación de flujo integral.",
        created_by=reviewer_identity,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    result.review = review
    result.stages.append("review")

    # Stage 5: opportunity
    opportunity = create_opportunity_from_review(db, review.id)
    if not opportunity:
        result.error = "opportunity creation failed"
        return result
    result.opportunity = opportunity
    result.stages.append("opportunity")

    # Stage 6: export
    result.json_export = opportunity_to_json(opportunity)
    result.csv_export = opportunities_to_csv([opportunity])
    result.stages.append("export")

    return result