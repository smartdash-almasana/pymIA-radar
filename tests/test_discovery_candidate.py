from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
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


def _conversation_payload() -> dict:
    external_id = f"candidate-{uuid4()}"
    return {"source": "discovery_test", "external_id": external_id, "conversation_url": f"https://example.test/{external_id}", "author_name": "Public Person", "title": "Regenerative community", "text": "I want to learn about a regenerative community in Yucatan.", "context": None, "engagement": {}}


def _completed_result(conversation_id: int) -> ConversationAssessmentV3Result:
    return ConversationAssessmentV3Result(conversation_id=conversation_id, assessment_status=AssessmentStatusV3.COMPLETED, real_topic="Regenerative community", contextual_meaning="The person requests information about a community.", apparent_affinity=ApparentAffinity.CLEAR, apparent_affinity_domains=[AffinityDomain.COMMUNITY], apparent_intention=ApparentIntention.EXPLORATION, intention_summary="The person wants to learn more.", evidence_fragments=["I want to learn about a regenerative community in Yucatan."], contradictions=[], missing_context=[], false_positive_risk=RiskLevelV3.LOW, uncertainty=RiskLevelV3.LOW, human_review_reason="Literal public evidence requires human review.", review_priority=70, recommended_review_action=ReviewActionV3.REVIEW, semantic_engine="llm:test", model_name="test")


def _cascade_result(conversation_id: int) -> CascadeResolutionV1:
    result = _completed_result(conversation_id)
    return CascadeResolutionV1(
        agnes_assessment=result,
        gemma_review_triggered=False,
        resolved_affinity=result.apparent_affinity,
        resolved_affinity_domains=result.apparent_affinity_domains,
        resolved_intention=result.apparent_intention,
        resolved_false_positive_risk=result.false_positive_risk,
        resolved_uncertainty=result.uncertainty,
        deterministic_resolution="GEMMA_NOT_REQUIRED",
        human_review_required=result.human_review_required,
        resolution_note="Gemma review not required.",
    )


def approved_candidate(client: TestClient, monkeypatch) -> tuple[int, int, str]:
    created = client.post("/api/conversations", json=_conversation_payload()).json()
    conversation_id, initial_status = created["id"], created["status"]
    monkeypatch.setattr("app.api.routes.assess_conversation_cascade_v1", lambda **_: _cascade_result(conversation_id))
    assert client.post(f"/api/conversations/{conversation_id}/assessments/v3").status_code == 200
    approval = client.post(f"/api/conversations/{conversation_id}/reviews", json={"decision": "APPROVE_DISCOVERY_CONTACT", "edited_response": "Hello, I would like to share more about Inlak'ech.", "reviewer_identity": "human-reviewer"})
    assert approval.status_code == 200
    return conversation_id, approval.json()["discovery_candidate_id"], initial_status


def test_discovery_approval_creates_one_candidate_and_preserves_conversation_state(monkeypatch) -> None:
    with TestClient(app) as client:
        conversation_id, candidate_id, initial_status = approved_candidate(client, monkeypatch)
        repeated = client.post(f"/api/conversations/{conversation_id}/reviews", json={"decision": "APPROVE_DISCOVERY_CONTACT", "edited_response": "Hello, I would like to share more about Inlak'ech.", "reviewer_identity": "human-reviewer"})
        assert repeated.status_code == 200
        assert repeated.json()["discovery_candidate_id"] == candidate_id
        candidate = client.get(f"/api/discovery-candidates/{candidate_id}").json()
        assert candidate["origin_conversation_id"] == conversation_id
        assert candidate["discovery_state"] == "DISCOVERY_APPROACH_APPROVED"
        conversations = client.get("/api/conversations").json()
        assert next(item for item in conversations if item["id"] == conversation_id)["status"] == initial_status


def test_candidate_events_and_human_outcome_follow_discovery_workflow(monkeypatch) -> None:
    with TestClient(app) as client:
        _, candidate_id, _ = approved_candidate(client, monkeypatch)
        for event in ({"event_type": "CONTACTED", "channel": "email", "message_text": "Approved human outreach."}, {"event_type": "REPLIED", "response_text": "Yes, I would like to continue."}):
            event["occurred_at"] = datetime.now(UTC).isoformat()
            assert client.post(f"/api/discovery-candidates/{candidate_id}/engagement-events", json=event).status_code == 200
        outcome = client.put(f"/api/discovery-candidates/{candidate_id}/outcome", json={"sympathy_revealed": "YES", "revealed_affinity_level": "PARTIAL", "revealed_affinity_domains": ["COMMUNITY"], "wants_to_continue": True, "consent_to_prequalification": True, "consent_recorded_at": datetime.now(UTC).isoformat(), "recorded_by": "human-reviewer"})
        assert outcome.status_code == 200
        events = client.get(f"/api/discovery-candidates/{candidate_id}/engagement-events").json()
        assert all(item["discovery_candidate_id"] == candidate_id for item in events)
