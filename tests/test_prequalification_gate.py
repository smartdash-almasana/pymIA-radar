from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.main import app
from test_discovery_candidate import approved_candidate


def qualification_payload() -> dict:
    return {"identity_profile": "INVERSOR", "capital_band": "USD_50000_A_150000", "time_horizon": "ESTE_MES", "motivation_text": "I want to contribute to a long-term regenerative project.", "motivation_coherent": True, "consent_to_continue": True, "requests_next_step": True, "minimum_information_complete": True}


def record_reply(client: TestClient, candidate_id: int) -> None:
    for event in ({"event_type": "CONTACTED", "channel": "email", "message_text": "Approved outreach."}, {"event_type": "REPLIED", "response_text": "Interested in learning more."}):
        event["occurred_at"] = datetime.now(UTC).isoformat()
        assert client.post(f"/api/discovery-candidates/{candidate_id}/engagement-events", json=event).status_code == 200


def test_reply_alone_cannot_open_qualification(monkeypatch) -> None:
    with TestClient(app) as client:
        conversation_id, candidate_id, initial_status = approved_candidate(client, monkeypatch)
        record_reply(client, candidate_id)
        assert client.post(f"/api/conversations/{conversation_id}/qualifications", json=qualification_payload()).status_code == 409


def test_only_explicit_accepted_prequalification_passes_gate(monkeypatch) -> None:
    with TestClient(app) as client:
        conversation_id, candidate_id, initial_status = approved_candidate(client, monkeypatch)
        record_reply(client, candidate_id)
        outcome = {"sympathy_revealed": "YES", "revealed_affinity_level": "CLEAR", "wants_to_continue": True, "consent_to_prequalification": True, "consent_recorded_at": datetime.now(UTC).isoformat(), "recorded_by": "human-reviewer"}
        assert client.put(f"/api/discovery-candidates/{candidate_id}/outcome", json=outcome).status_code == 200
        assert client.post(f"/api/discovery-candidates/{candidate_id}/prequalification-invitation").status_code == 200
        assert client.post(f"/api/discovery-candidates/{candidate_id}/prequalification-acceptance").status_code == 200
        assert client.post(f"/api/conversations/{conversation_id}/qualifications", json=qualification_payload()).status_code == 200
        assert client.get(f"/api/discovery-candidates/{candidate_id}").json()["discovery_state"] == "PREQUALIFICATION_ACCEPTED"
        conversations = client.get("/api/conversations").json()
        assert next(item for item in conversations if item["id"] == conversation_id)["status"] == initial_status
