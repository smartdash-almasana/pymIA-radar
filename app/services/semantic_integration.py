"""Playwright → semantic evaluation → Lista 1 pipeline.

Controlled campaign mode: evaluation runs inside this pipeline only,
never automatically for all Conversations.
"""

from __future__ import annotations

from typing import NamedTuple

from sqlalchemy.orm import Session

from app.discovery.playwright_adapter import navigation_to_discovery
from app.discovery.ingestion import persist_discovery_results
from app.integrations.playwright_mcp import NavigationResult
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.semantics.conversation_assessment_v3 import DraftRunnerV3
from app.semantics.semantic_cascade_v1 import (
    CascadeResolutionV1,
    assess_conversation_cascade_v1,
)
from app.services.presumptive_candidates import (
    create_or_update_presumptive_candidate,
)
from app.models.presumptive_candidate import PresumptiveCandidate


class PipelineStage(NamedTuple):
    stage: str
    status: str
    detail: str | None = None


class PlaywrightSemanticPipelineResult(NamedTuple):
    conversation: Conversation | None
    assessment: ConversationAssessmentV3 | None
    candidate: PresumptiveCandidate | None
    stages: list[PipelineStage]


def persist_cascade_assessment(
    db: Session,
    cascade: CascadeResolutionV1,
    conversation: Conversation,
) -> ConversationAssessmentV3:
    """Map CascadeResolutionV1 → ConversationAssessmentV3 ORM and persist.

    Extracted from POST /conversations/{id}/assessments/v3 to avoid
    duplicating the mapping between the endpoint and the pipeline.
    """
    result = cascade.agnes_assessment
    record = ConversationAssessmentV3(
        conversation_id=conversation.id,
        schema_version=result.schema_version,
        assessment_status=result.assessment_status.value,
        real_topic=result.real_topic,
        contextual_meaning=result.contextual_meaning,
        apparent_affinity=(
            cascade.resolved_affinity.value if cascade.resolved_affinity else None
        ),
        apparent_affinity_domains=[item.value for item in cascade.resolved_affinity_domains],
        apparent_intention=(
            cascade.resolved_intention.value if cascade.resolved_intention else None
        ),
        intention_summary=result.intention_summary,
        evidence_fragments=list(
            dict.fromkeys(result.evidence_fragments + cascade.accepted_additional_evidence)
        ),
        rejected_evidence_fragments=result.rejected_evidence_fragments,
        contradictions=result.contradictions,
        missing_context=result.missing_context,
        false_positive_risk=(
            cascade.resolved_false_positive_risk.value
            if cascade.resolved_false_positive_risk
            else None
        ),
        uncertainty=(
            cascade.resolved_uncertainty.value if cascade.resolved_uncertainty else None
        ),
        human_review_reason=result.human_review_reason,
        review_priority=result.review_priority,
        recommended_review_action=result.recommended_review_action.value,
        semantic_engine=result.semantic_engine,
        model_name=result.model_name,
        safe_error_code=result.safe_error_code,
        provisional=result.provisional,
        human_review_required=cascade.human_review_required,
        cascade_schema_version=cascade.schema_version,
        gemma_review_triggered=cascade.gemma_review_triggered,
        gemma_trigger_reasons=cascade.gemma_trigger_reasons,
        gemma_review=(
            cascade.gemma_review.model_dump(mode="json") if cascade.gemma_review else None
        ),
        deterministic_resolution=cascade.deterministic_resolution,
        resolution_note=cascade.resolution_note,
        primary_provider_attempted=cascade.primary_provider_attempted,
        primary_provider_used=cascade.primary_provider_used,
        provider_failover=cascade.provider_failover,
        provider_failure_code=cascade.provider_failure_code,
        provider_failure_detail=cascade.provider_failure_detail,
        created_at=result.created_at,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def run_playwright_semantic_pipeline(
    db: Session,
    navigation: NavigationResult,
    *,
    source: str,
    query_origin: str | None = None,
    title: str | None = None,
    context: str | None = None,
    agnes_enabled: bool = True,
    agnes_model_name: str | None = None,
    agnes_base_url: str | None = None,
    agnes_api_key: str | None = None,
    gemma_enabled: bool = False,
    gemma_model_name: str | None = None,
    gemma_base_url: str | None = None,
    gemma_api_key: str | None = None,
    agnes_runner: DraftRunnerV3 | None = None,
) -> PlaywrightSemanticPipelineResult:
    stages: list[PipelineStage] = []

    # Stage 1: persist evidence
    discovery = navigation_to_discovery(
        navigation=navigation,
        source=source,
        query_origin=query_origin,
        title=title,
        context=context,
    )
    if discovery is None:
        stages.append(PipelineStage("evidence", "REJECTED", navigation.status))
        return PlaywrightSemanticPipelineResult(None, None, None, stages)

    persisted = persist_discovery_results(db, [discovery])
    conversation = persisted[0]
    stages.append(
        PipelineStage("evidence", "PERSISTED", f"conversation_id={conversation.id}")
    )

    # Stage 2: semantic evaluation
    cascade = assess_conversation_cascade_v1(
        conversation_id=conversation.id,
        title=conversation.title,
        text=conversation.text,
        context=conversation.context,
        agnes_enabled=agnes_enabled,
        agnes_model_name=agnes_model_name,
        agnes_base_url=agnes_base_url,
        agnes_api_key=agnes_api_key,
        gemma_enabled=gemma_enabled,
        gemma_model_name=gemma_model_name,
        gemma_base_url=gemma_base_url,
        gemma_api_key=gemma_api_key,
        agnes_runner=agnes_runner,
    )
    assessment = persist_cascade_assessment(db, cascade, conversation)
    stages.append(
        PipelineStage(
            "assessment",
            "PERSISTED",
            f"assessment_id={assessment.id} status={assessment.assessment_status}",
        )
    )

    # Stage 3: presumptive candidate (only if assessment is eligible)
    candidate = create_or_update_presumptive_candidate(
        db,
        conversation=conversation,
        assessment=assessment,
    )
    if candidate:
        db.commit()
        db.refresh(candidate)
        stages.append(
            PipelineStage("candidate", "PERSISTED", f"candidate_id={candidate.id}")
        )
    else:
        stages.append(
            PipelineStage(
                "candidate",
                "SKIPPED",
                "assessment not eligible",
            )
        )

    return PlaywrightSemanticPipelineResult(conversation, assessment, candidate, stages)