from __future__ import annotations

import csv
import io

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.approved_opportunity_v1 import ApprovedOpportunityV1
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.presumptive_candidate import PresumptiveCandidate
from app.models.review import ReviewDecision
from app.schemas.approved_opportunity_v1 import (
    SCHEMA_VERSION_APPROVED_OPPORTUNITY_V1,
    OpportunityStatus,
)


def create_opportunity_from_review(
    db: Session,
    review_id: int,
) -> ApprovedOpportunityV1 | None:
    review = db.get(ReviewDecision, review_id)
    if not review:
        return None
    if review.decision != "APPROVE_DISCOVERY_CONTACT":
        return None
    if not review.created_by:
        return None

    conversation = db.get(Conversation, review.conversation_id)
    if not conversation:
        return None

    assessment = db.scalar(
        select(ConversationAssessmentV3).where(
            ConversationAssessmentV3.conversation_id == review.conversation_id,
            ConversationAssessmentV3.assessment_status == "COMPLETED",
        ).order_by(ConversationAssessmentV3.id.desc()).limit(1)
    )
    if not assessment:
        return None

    candidate = db.scalar(
        select(PresumptiveCandidate).where(
            PresumptiveCandidate.conversation_id == review.conversation_id,
        ).order_by(PresumptiveCandidate.id.desc()).limit(1)
    )
    if not candidate:
        return None

    existing = db.scalar(
        select(ApprovedOpportunityV1).where(
            ApprovedOpportunityV1.human_review_id == review_id,
        )
    )
    if existing:
        return existing

    opportunity = ApprovedOpportunityV1(
        schema_version=SCHEMA_VERSION_APPROVED_OPPORTUNITY_V1,
        conversation_id=conversation.id,
        assessment_id=assessment.id,
        presumptive_candidate_id=candidate.id,
        public_actor_id=candidate.public_actor_id,
        source=conversation.source,
        source_url=conversation.conversation_url,
        public_username=conversation.author_name,
        apparent_affinity=assessment.apparent_affinity or "",
        apparent_intention=assessment.apparent_intention or "",
        evidence_fragments=assessment.evidence_fragments,
        review_priority=assessment.review_priority,
        human_review_id=review.id,
        human_reviewer_identity=review.created_by or "",
        approved_at=review.created_at,
        status=OpportunityStatus.READY_FOR_CRM.value,
    )
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity


def get_opportunity(db: Session, opportunity_id: int) -> ApprovedOpportunityV1 | None:
    return db.get(ApprovedOpportunityV1, opportunity_id)


def list_opportunities(
    db: Session,
    *,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[ApprovedOpportunityV1]:
    query = select(ApprovedOpportunityV1).order_by(ApprovedOpportunityV1.created_at.desc())
    if status:
        query = query.where(ApprovedOpportunityV1.status == status)
    return list(db.scalars(query.offset(offset).limit(limit)))


def opportunity_to_json(opportunity: ApprovedOpportunityV1) -> dict:
    return {
        "schema_version": opportunity.schema_version,
        "stable_id": opportunity.stable_id,
        "id": opportunity.id,
        "conversation_id": opportunity.conversation_id,
        "assessment_id": opportunity.assessment_id,
        "presumptive_candidate_id": opportunity.presumptive_candidate_id,
        "public_actor_id": opportunity.public_actor_id,
        "source": opportunity.source,
        "source_url": opportunity.source_url,
        "public_username": opportunity.public_username,
        "apparent_affinity": opportunity.apparent_affinity,
        "apparent_intention": opportunity.apparent_intention,
        "evidence_fragments": opportunity.evidence_fragments,
        "review_priority": opportunity.review_priority,
        "human_review_id": opportunity.human_review_id,
        "human_reviewer_identity": opportunity.human_reviewer_identity,
        "approved_at": opportunity.approved_at.isoformat() if opportunity.approved_at else None,
        "status": opportunity.status,
        "external_crm_id": opportunity.external_crm_id,
        "export_count": opportunity.export_count,
        "last_exported_at": opportunity.last_exported_at.isoformat() if opportunity.last_exported_at else None,
        "created_at": opportunity.created_at.isoformat() if opportunity.created_at else None,
        "updated_at": opportunity.updated_at.isoformat() if opportunity.updated_at else None,
    }


CSV_HEADERS = [
    "schema_version", "stable_id", "id", "conversation_id", "assessment_id",
    "presumptive_candidate_id", "public_actor_id", "source", "source_url",
    "public_username", "apparent_affinity", "apparent_intention",
    "evidence_fragments", "review_priority", "human_review_id",
    "human_reviewer_identity", "approved_at", "status", "external_crm_id",
    "export_count", "last_exported_at", "created_at", "updated_at",
]


def opportunities_to_csv(opportunities: list[ApprovedOpportunityV1]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(CSV_HEADERS)
    for opp in opportunities:
        writer.writerow([
            opp.schema_version,
            opp.stable_id,
            opp.id,
            opp.conversation_id,
            opp.assessment_id,
            opp.presumptive_candidate_id,
            opp.public_actor_id,
            opp.source,
            opp.source_url,
            opp.public_username or "",
            opp.apparent_affinity,
            opp.apparent_intention,
            _fragments_str(opp.evidence_fragments),
            opp.review_priority,
            opp.human_review_id,
            opp.human_reviewer_identity,
            opp.approved_at.isoformat() if opp.approved_at else "",
            opp.status,
            opp.external_crm_id or "",
            opp.export_count,
            opp.last_exported_at.isoformat() if opp.last_exported_at else "",
            opp.created_at.isoformat() if opp.created_at else "",
            opp.updated_at.isoformat() if opp.updated_at else "",
        ])
    return buf.getvalue()


def _fragments_str(fragments: list) -> str:
    return "; ".join(str(f) for f in fragments) if fragments else ""