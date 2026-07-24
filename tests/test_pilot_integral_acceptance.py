"""Focal tests for pilot integral acceptance flow."""
from unittest.mock import patch

from sqlalchemy import func, select

from app.db.session import Base, SessionLocal, engine
from app.integrations.playwright_mcp import NavigationResult
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.presumptive_candidate import PresumptiveCandidate
from app.models.review import ReviewDecision
from app.schemas.assessment_v3 import (
    AffinityDomain, ApparentAffinity, ApparentIntention,
    AssessmentStatusV3, ConversationAssessmentV3Result, ReviewActionV3, RiskLevelV3,
)
from app.semantics.semantic_cascade_v1 import CascadeResolutionV1
from app.services.pilot_integral_acceptance import run_pilot_flow


def _nav(*, status="SUCCESS", final_url="https://example.com/pilot/1", visible_text="A" * 300) -> NavigationResult:
    return NavigationResult(
        requested_url=final_url, final_url=final_url,
        visible_text=visible_text, author="pilotuser",
        author_status="RESOLVED", screenshot_path=None,
        status=status, latency_ms=1500, error_detail=None,
    )


def _completed_assessment(**overrides) -> ConversationAssessmentV3Result:
    base = ConversationAssessmentV3Result(
        id=0, conversation_id=0,
        schema_version="radar-conversation-assessment/v3",
        assessment_status=AssessmentStatusV3.COMPLETED,
        real_topic="regeneración",
        contextual_meaning="Interés en proyectos regenerativos.",
        apparent_affinity=ApparentAffinity.POSSIBLE,
        apparent_affinity_domains=[AffinityDomain.REGENERATION],
        apparent_intention=ApparentIntention.EXPLORATION,
        intention_summary="Quiere conocer más.",
        evidence_fragments=["menciona impacto comunitario"],
        rejected_evidence_fragments=[], contradictions=[], missing_context=[],
        false_positive_risk=RiskLevelV3.LOW, uncertainty=RiskLevelV3.LOW,
        human_review_reason="Afinidad aparente detectada.",
        review_priority=50, recommended_review_action=ReviewActionV3.REVIEW,
        semantic_engine="llm:agnes", model_name="agnes-2.0-flash",
        safe_error_code=None, provisional=True, human_review_required=True,
        created_at="2026-07-24T12:00:00Z",
    )
    return base.model_copy(update=overrides)


def _eligible_cascade(assessment: ConversationAssessmentV3Result | None = None) -> CascadeResolutionV1:
    a = assessment or _completed_assessment()
    return CascadeResolutionV1(
        agnes_assessment=a, gemma_review_triggered=False, gemma_trigger_reasons=[],
        gemma_review=None, resolved_affinity=a.apparent_affinity,
        resolved_affinity_domains=a.apparent_affinity_domains,
        resolved_intention=a.apparent_intention,
        resolved_false_positive_risk=a.false_positive_risk,
        resolved_uncertainty=a.uncertainty, accepted_additional_evidence=[],
        disputed_fields=[], primary_provider_attempted="agnes",
        primary_provider_used="agnes", provider_failover=False,
        provider_failure_code=None, provider_failure_detail=None,
        deterministic_resolution="GEMMA_NOT_REQUIRED",
        human_review_required=a.human_review_required,
        resolution_note="Test fixture.",
    )


# ponytail: shared in-memory SQLite across all tests in this module


class TestPilotIntegralFlow:
    def test_happy_path_full_flow(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/pilot/happy")
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                result = run_pilot_flow(db, nav, source="reddit", reviewer_identity="reviewer@inlakech")
        assert result.opportunity is not None
        assert result.opportunity.status == "READY_FOR_CRM"
        assert result.review is not None
        assert result.conversation is not None
        assert result.assessment is not None
        assert result.candidate is not None
        assert result.json_export is not None
        assert result.json_export["status"] == "READY_FOR_CRM"
        assert result.csv_export is not None
        assert "schema_version" in result.csv_export
        assert "READY_FOR_CRM" in result.csv_export
        assert result.error is None

    def test_blocked_navigation_stops_flow(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(status="CAPTCHA_BLOCKED")
        with SessionLocal() as db:
            result = run_pilot_flow(db, nav, source="reddit", reviewer_identity="reviewer@inlakech")
        assert result.conversation is None
        assert result.assessment is None
        assert result.candidate is None
        assert result.review is None
        assert result.opportunity is None
        assert result.error is not None

    def test_not_eligible_assessment_returns_no_candidate(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/pilot/not-eligible")
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
                result = run_pilot_flow(db, nav, source="reddit", reviewer_identity="reviewer@inlakech")
        assert result.conversation is not None
        assert result.assessment is not None
        assert result.candidate is None
        assert result.review is None
        assert result.opportunity is None
        assert result.error is not None

    def test_empty_reviewer_identity_blocks_opportunity(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/pilot/no-reviewer")
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                result = run_pilot_flow(db, nav, source="reddit", reviewer_identity="")
        assert result.conversation is not None
        assert result.review is not None
        assert result.review.created_by == ""
        assert result.opportunity is None
        assert result.error is not None

    def test_conversation_idempotent(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/pilot/idem-conv")
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                a = run_pilot_flow(db, nav, source="reddit", reviewer_identity="r@x", title="first")
                b = run_pilot_flow(db, nav, source="reddit", reviewer_identity="r@x", title="second")
            assert a.conversation is not None and b.conversation is not None
            assert a.conversation.id == b.conversation.id
            conv_count = db.scalar(
                select(func.count()).select_from(Conversation)
                .where(Conversation.external_id == a.conversation.external_id)
            )
            assert conv_count == 1

    def test_opportunity_idempotent_by_review(self):
        Base.metadata.create_all(bind=engine)
        nav = _nav(final_url="https://example.com/pilot/idem-opp")
        with SessionLocal() as db:
            with patch(
                "app.services.semantic_integration.assess_conversation_cascade_v1",
                return_value=_eligible_cascade(),
            ):
                result = run_pilot_flow(db, nav, source="reddit", reviewer_identity="reviewer@x")
            assert result.opportunity is not None
            opp_id = result.opportunity.id
            # Second call with same review idempotency check
            review_id = result.review.id
            from app.services.approved_opportunity import create_opportunity_from_review
            same = create_opportunity_from_review(db, review_id)
            assert same is not None
            assert same.id == opp_id