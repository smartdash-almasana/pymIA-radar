"""Focal tests for ApprovedOpportunityV1 — CRM-neutral opportunity contract."""

from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.models.approved_opportunity_v1 import ApprovedOpportunityV1
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.presumptive_candidate import PresumptiveCandidate
from app.models.public_actor import PublicActor
from app.models.review import ReviewDecision
from app.schemas.approved_opportunity_v1 import OpportunityStatus
from app.services.approved_opportunity import (
    create_opportunity_from_review,
    get_opportunity,
    list_opportunities,
    opportunity_to_json,
    opportunities_to_csv,
)

# ponytail: reuse in-memory SQLite across all tests in this module


def _seed_review(db, *, decision="APPROVE_DISCOVERY_CONTACT", reviewer="reviewer@inlakech", suffix=""):
    eid = f"opp:test:{suffix or '1'}"
    conversation = Conversation(
        source="reddit",
        external_id=eid,
        conversation_url="https://reddit.com/r/test/1",
        author_name="testuser",
        text="Test conversation for opportunity creation.",
    )
    db.add(conversation)
    db.flush()

    assessment = ConversationAssessmentV3(
        conversation_id=conversation.id,
        schema_version="radar-conversation-assessment/v3",
        assessment_status="COMPLETED",
        apparent_affinity="POSSIBLE",
        apparent_intention="EXPLORATION",
        evidence_fragments=["menciona intereses regenerativos"],
        review_priority=50,
        recommended_review_action="REVIEW",
        semantic_engine="llm:agnes",
    )
    db.add(assessment)
    db.flush()

    actor = PublicActor(
        platform="reddit",
        platform_actor_id=f"reddit:testuser:{suffix}" if suffix else "reddit:testuser",
        public_username=f"testuser_{suffix}" if suffix else "testuser",
    )
    db.add(actor)
    db.flush()

    candidate = PresumptiveCandidate(
        public_actor_id=actor.id,
        conversation_id=conversation.id,
        assessment_id=assessment.id,
        status="INTERPRETATION_PENDING",
        apparent_affinity="POSSIBLE",
        apparent_intention="EXPLORATION",
        false_positive_risk="LOW",
        review_priority=50,
        skill_version="1.0",
    )
    db.add(candidate)
    db.flush()

    review = ReviewDecision(
        conversation_id=conversation.id,
        decision=decision,
        edited_response="Hola, soy de Inlak'ech...",
        reviewer_notes="Parece genuino.",
        created_by=reviewer,
    )
    db.add(review)
    db.flush()

    db.commit()
    return review


class TestCreateFromReview:
    def test_valid_approval_creates_opportunity(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db)
            opp = create_opportunity_from_review(db, review.id)
            assert opp is not None
            assert opp.status == OpportunityStatus.READY_FOR_CRM.value
            assert opp.external_crm_id is None
            assert opp.human_reviewer_identity == "reviewer@inlakech"
            assert opp.schema_version == "radar-approved-opportunity/v1"
            assert opp.stable_id is not None

    def test_same_review_returns_same_opportunity(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="idem")
            a = create_opportunity_from_review(db, review.id)
            b = create_opportunity_from_review(db, review.id)
            assert a is not None and b is not None
            assert a.id == b.id

    def test_observe_decision_returns_none(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, decision="KEEP_OBSERVING", suffix="observe")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is None

    def test_discard_decision_returns_none(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, decision="DISCARD", suffix="discard")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is None

    def test_review_not_found_returns_none(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            opp = create_opportunity_from_review(db, 99999)
            assert opp is None

    def test_missing_reviewer_identity_returns_none(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, reviewer=None, suffix="missing-reviewer")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is None


class TestPreconditions:
    def test_assessment_not_completed_rejected(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="not-completed")
            db.query(ConversationAssessmentV3).update({"assessment_status": "INVALID_MODEL_OUTPUT"})
            db.commit()
            opp = create_opportunity_from_review(db, review.id)
            assert opp is None

    def test_conversation_deleted_rejected(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="conv-deleted")
            db.query(Conversation).delete()
            db.commit()
            opp = create_opportunity_from_review(db, review.id)
            assert opp is None


class TestGetAndList:
    def test_get_opportunity_by_id(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="get-by-id")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is not None
            fetched = get_opportunity(db, opp.id)
            assert fetched is not None
            assert fetched.id == opp.id

    def test_get_nonexistent_returns_none(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            assert get_opportunity(db, 99999) is None

    def test_list_by_status(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="list-status")
            create_opportunity_from_review(db, review.id)
            ready = list_opportunities(db, status="READY_FOR_CRM")
            assert len(ready) == 1
            exported = list_opportunities(db, status="EXPORTED")
            assert len(exported) == 0


class TestExport:
    def test_json_export_has_schema_version(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="json")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is not None
            data = opportunity_to_json(opp)
            assert data["schema_version"] == "radar-approved-opportunity/v1"
            assert data["stable_id"] == opp.stable_id
            assert data["status"] == "READY_FOR_CRM"
            assert data["external_crm_id"] is None

    def test_csv_has_stable_headers(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="csv")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is not None
            csv_content = opportunities_to_csv([opp])
            lines = csv_content.strip().split("\n")
            headers = lines[0].split(",")
            assert "schema_version" in headers
            assert "stable_id" in headers
            assert "status" in headers
            assert "external_crm_id" in headers
            assert len(lines) == 2  # header + 1 row

    def test_csv_empty_list_has_only_headers(self):
        csv_content = opportunities_to_csv([])
        lines = csv_content.strip().split("\n")
        assert len(lines) == 1  # only header

    def test_json_initial_status_ready_for_crm(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="status")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is not None
            assert opp.status == "READY_FOR_CRM"

    def test_external_crm_id_null(self):
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            review = _seed_review(db, suffix="crm-null")
            opp = create_opportunity_from_review(db, review.id)
            assert opp is not None
            assert opp.external_crm_id is None

class TestHttpExports:
    def test_json_export_route_is_not_captured_by_dynamic_id_route(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        with TestClient(app) as client:
            response = client.get("/api/opportunities/export/json")
        assert response.status_code == 200
        assert response.json() == []

    def test_csv_export_route_is_not_captured_by_dynamic_id_route(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        with TestClient(app) as client:
            response = client.get("/api/opportunities/export/csv")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/csv")
        assert response.text.startswith("schema_version,stable_id,")
