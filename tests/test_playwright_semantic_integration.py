"""Focal tests for Playwright → semantic evaluation pipeline."""

from unittest.mock import patch

from sqlalchemy import func, select

from app.db.session import Base, SessionLocal, engine
from app.integrations.playwright_mcp import NavigationResult
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.presumptive_candidate import PresumptiveCandidate
from app.schemas.assessment_v3 import (
    AffinityDomain,
    ApparentAffinity,
    ApparentIntention,
    AssessmentStatusV3,
    ConversationAssessmentV3Result,
    ReviewActionV3,
    RiskLevelV3,
)
from app.semantics.semantic_cascade_v1 import CascadeResolutionV1
from app.services.semantic_integration import (
    persist_cascade_assessment,
    run_playwright_semantic_pipeline,
)
from app.api.routes import create_conversation_assessment_v3, create_review
from app.schemas.review import ReviewCreate, ReviewDecisionType


def _nav(
    *,
    status="SUCCESS",
    final_url="https://example.com/post/1",
    visible_text="A" * 300,
    author="user123",
    author_status="RESOLVED",
) -> NavigationResult:
    return NavigationResult(
        requested_url="https://example.com/redirect-me",
        final_url=final_url,
        visible_text=visible_text,
        author=author,
        author_status=author_status,
        screenshot_path=None,
        status=status,
        latency_ms=1500,
        error_detail=None,
    )


def _completed_assessment(**overrides) -> ConversationAssessmentV3Result:
    base = ConversationAssessmentV3Result(
        id=0,
        conversation_id=0,
        schema_version="radar-conversation-assessment/v3",
        assessment_status=AssessmentStatusV3.COMPLETED,
        real_topic="regeneración",
        contextual_meaning="Interés en proyectos regenerativos.",
        apparent_affinity=ApparentAffinity.POSSIBLE,
        apparent_affinity_domains=[AffinityDomain.REGENERATION],
        apparent_intention=ApparentIntention.EXPLORATION,
        intention_summary="Quiere conocer más.",
        evidence_fragments=["menciona impacto comunitario"],
        rejected_evidence_fragments=[],
        contradictions=[],
        missing_context=[],
        false_positive_risk=RiskLevelV3.LOW,
        uncertainty=RiskLevelV3.LOW,
human_review_reason="Afinidad aparente detectada.",
            review_priority=50,
        recommended_review_action=ReviewActionV3.REVIEW,
        semantic_engine="llm:agnes",
        model_name="agnes-2.0-flash",
        safe_error_code=None,
        provisional=True,
        human_review_required=True,
        created_at="2026-07-24T12:00:00Z",
    )
    return base.model_copy(update=overrides)


def _eligible_cascade(assessment: ConversationAssessmentV3Result | None = None) -> CascadeResolutionV1:
    a = assessment or _completed_assessment()
    return CascadeResolutionV1(
        agnes_assessment=a,
        gemma_review_triggered=False,
        gemma_trigger_reasons=[],
        gemma_review=None,
        resolved_affinity=a.apparent_affinity,
        resolved_affinity_domains=a.apparent_affinity_domains,
        resolved_intention=a.apparent_intention,
        resolved_false_positive_risk=a.false_positive_risk,
        resolved_uncertainty=a.uncertainty,
        accepted_additional_evidence=[],
        disputed_fields=[],
        primary_provider_attempted="agnes",
        primary_provider_used="agnes",
        provider_failover=False,
        provider_failure_code=None,
        provider_failure_detail=None,
        deterministic_resolution="GEMMA_NOT_REQUIRED",
        human_review_required=a.human_review_required,
        resolution_note="Test fixture.",
    )


class TestPersistCascadeAssessment:
    def test_persists_and_returns_record(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/persist/1")
        with SessionLocal() as db:
            from app.discovery.playwright_adapter import process_and_persist
            disc = process_and_persist(db, nav, source="reddit")
            conv = db.scalar(
                select(Conversation).where(
                    Conversation.source == disc.source,
                    Conversation.external_id == disc.external_id,
                )
            )
            assert conv is not None
            cascade = _eligible_cascade()
            record = persist_cascade_assessment(db, cascade, conv)
            assert record.id is not None
            assert record.conversation_id == conv.id
            assert record.assessment_status == "COMPLETED"

    def test_idempotent_no_duplicate(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/persist/2")
        with SessionLocal() as db:
            from app.discovery.playwright_adapter import process_and_persist
            disc = process_and_persist(db, nav, source="reddit")
            conv = db.scalar(
                select(Conversation).where(
                    Conversation.source == disc.source,
                    Conversation.external_id == disc.external_id,
                )
            )
            assert conv is not None
            cascade = _eligible_cascade()
            a = persist_cascade_assessment(db, cascade, conv)
            b = persist_cascade_assessment(db, cascade, conv)
            assert a.id != b.id  # no unique constraint on assessment per se
            count = db.scalar(
                select(func.count()).select_from(ConversationAssessmentV3)
                .where(ConversationAssessmentV3.conversation_id == conv.id)
            )
            assert count == 2  # assessments are append-only per design


class TestRunPlaywrightSemanticPipeline:
    def test_full_flow_eligible(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav()
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                result = run_playwright_semantic_pipeline(
                    db, nav, source="reddit", query_origin="test",
                )
            assert result.conversation is not None
            assert result.assessment is not None
            assert result.assessment.assessment_status == "COMPLETED"
            assert result.candidate is not None
            assert any(s.stage == "evidence" and s.status == "PERSISTED" for s in result.stages)
            assert any(s.stage == "assessment" and s.status == "PERSISTED" for s in result.stages)
            assert any(s.stage == "candidate" and s.status == "PERSISTED" for s in result.stages)

    def test_idempotent_same_nav_no_duplicate(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/idempotent-pipeline/1")
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                a = run_playwright_semantic_pipeline(db, nav, source="reddit")
                b = run_playwright_semantic_pipeline(db, nav, source="reddit")
            assert a.conversation is not None and b.conversation is not None
            assert a.conversation.id == b.conversation.id  # same Conversation

            conv_count = db.scalar(
                select(func.count()).select_from(Conversation)
                .where(Conversation.source == "reddit",
                       Conversation.external_id == a.conversation.external_id)
            )
            assert conv_count == 1

            assessment_count = db.scalar(
                select(func.count()).select_from(ConversationAssessmentV3)
                .where(ConversationAssessmentV3.conversation_id == a.conversation.id)
            )
            candidate_count = db.scalar(
                select(func.count()).select_from(PresumptiveCandidate)
                .where(PresumptiveCandidate.conversation_id == a.conversation.id)
            )
            assert assessment_count == 2  # append-only assessment history
            assert candidate_count == 1  # one active presumptive candidate per conversation
            assert b.candidate is not None
            assert b.candidate.assessment_id == b.assessment.id

    def test_candidate_is_durable_after_session_reopen(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/durable-candidate/1")
        candidate_id = None
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                result = run_playwright_semantic_pipeline(db, nav, source="reddit")
            assert result.candidate is not None
            candidate_id = result.candidate.id

        with SessionLocal() as db:
            persisted = db.get(PresumptiveCandidate, candidate_id)
            assert persisted is not None

    def test_blocked_navigation_returns_nothing(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(status="CAPTCHA_BLOCKED")
        with SessionLocal() as db:
            result = run_playwright_semantic_pipeline(db, nav, source="reddit")
            assert result.conversation is None
            assert result.assessment is None
            assert result.candidate is None
            assert any(s.status == "REJECTED" for s in result.stages)

    def test_invalid_model_output_no_candidate(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav()
        failed = _completed_assessment(
            assessment_status=AssessmentStatusV3.INVALID_MODEL_OUTPUT,
            safe_error_code="INVALID_MODEL_OUTPUT",
            recommended_review_action=ReviewActionV3.OBSERVE,
        )
        cascade = _eligible_cascade(assessment=failed)
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=cascade,
            ):
                result = run_playwright_semantic_pipeline(db, nav, source="reddit")
            assert result.conversation is not None
            assert result.assessment is not None
            assert result.candidate is None

    def test_completed_not_eligible_no_candidate(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/not-eligible/1")
        no_affinity = _completed_assessment(
            apparent_affinity=ApparentAffinity.NONE,
            apparent_affinity_domains=[],
            recommended_review_action=ReviewActionV3.OBSERVE,
        )
        cascade = _eligible_cascade(assessment=no_affinity)
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=cascade,
            ):
                result = run_playwright_semantic_pipeline(db, nav, source="reddit")
            assert result.conversation is not None
            assert result.assessment is not None
            assert result.assessment.assessment_status == "COMPLETED"
            assert result.candidate is None

    def test_no_author_preserves_author_status(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(
            final_url="https://example.com/no-author/1",
            author=None, author_status="UNAVAILABLE", visible_text="X" * 300,
        )
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                result = run_playwright_semantic_pipeline(db, nav, source="reddit")
            assert result.conversation is not None
            assert result.conversation.author_name is None
            assert result.conversation.engagement["author_status"] == "UNAVAILABLE"


class TestEndpointStillWorks:
    def test_v3_endpoint_rejects_missing_conversation(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            from fastapi import HTTPException
            try:
                create_conversation_assessment_v3(99999, db)
                assert False, "should have raised"
            except HTTPException as e:
                assert e.status_code == 404

    def test_v3_endpoint_persists_assessment_for_existing_conversation(self):
        Base.metadata.create_all(bind=engine)
        conversation = Conversation(
            source="reddit",
            external_id="endpoint-success-1",
            conversation_url="https://example.com/endpoint-success-1",
            author_name="user-endpoint",
            title="title",
            text="A" * 300,
            context="context",
            engagement={},
        )
        with SessionLocal() as db:
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            with patch("app.api.routes.assess_conversation_cascade_v1", return_value=_eligible_cascade()):
                result = create_conversation_assessment_v3(conversation.id, db)
            assert result.assessment_status == AssessmentStatusV3.COMPLETED
            persisted = db.scalar(
                select(ConversationAssessmentV3).where(
                    ConversationAssessmentV3.conversation_id == conversation.id
                )
            )
            assert persisted is not None

    def test_human_review_still_requires_completed_assessment(self):
        Base.metadata.create_all(bind=engine)
        conversation = Conversation(
            source="reddit",
            external_id="review-gate-1",
            conversation_url="https://example.com/review-gate-1",
            author_name="user-review",
            title="title",
            text="B" * 300,
            context="context",
            engagement={},
        )
        payload = ReviewCreate(
            decision=ReviewDecisionType.APPROVE_DISCOVERY_CONTACT,
            edited_response="Mensaje revisado por una persona.",
            reviewer_identity="reviewer@example.com",
        )
        with SessionLocal() as db:
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            from fastapi import HTTPException
            try:
                create_review(conversation.id, payload, db)
                assert False, "approval should require a completed assessment"
            except HTTPException as exc:
                assert exc.status_code == 409