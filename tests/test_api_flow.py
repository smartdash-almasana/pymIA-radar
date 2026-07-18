from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_local_conversation_flow_persists_deduplicates_assesses_and_reviews() -> None:
    external_id = f"test-{uuid4()}"
    payload = {
        "source": "test_source",
        "external_id": external_id,
        "conversation_url": f"https://example.com/conversations/{external_id}",
        "author_name": "Persona de prueba",
        "title": "Inversión regenerativa",
        "text": (
            "Busco una inversión regenerativa de largo plazo, "
            "con comunidad, patrimonio y propósito."
        ),
        "context": "Corpus local de validación M0",
        "query_origin": "inversión consciente",
        "engagement": {"likes": 3},
    }

    with TestClient(app) as client:
        created = client.post("/api/conversations", json=payload)
        assert created.status_code == 200
        created_body = created.json()
        conversation_id = created_body["id"]
        assert created_body["external_id"] == external_id
        assert created_body["status"] == "detected"

        duplicate = client.post("/api/conversations", json=payload)
        assert duplicate.status_code == 200
        assert duplicate.json()["id"] == conversation_id

        listed = client.get("/api/conversations")
        assert listed.status_code == 200
        matching = [
            item for item in listed.json()
            if item["source"] == payload["source"]
            and item["external_id"] == external_id
        ]
        assert len(matching) == 1

        assessment = client.post(f"/api/conversations/{conversation_id}/assess")
        assert assessment.status_code == 200
        assessment_body = assessment.json()
        assert assessment_body["thematic_affinity"] > 0
        assert assessment_body["values_affinity"] > 0
        assert assessment_body["intent_score"] > 0
        assert assessment_body["declared_capacity"] == "NO_CONOCIDA"
        assert assessment_body["human_review_required"] is True
        assert assessment_body["provisional"] is True
        assert assessment_body["evidence_fragments"]

        assessment_history = client.get(
            f"/api/conversations/{conversation_id}/assessments"
        )
        assert assessment_history.status_code == 200
        stored_assessment = assessment_history.json()[-1]
        assert stored_assessment["thematic_affinity"] == assessment_body["thematic_affinity"]
        assert stored_assessment["values_affinity"] == assessment_body["values_affinity"]
        assert stored_assessment["intent_score"] == assessment_body["intent_score"]
        assert stored_assessment["declared_capacity"] == "NO_CONOCIDA"
        assert stored_assessment["semantic_engine"] == "deterministic"
        assert stored_assessment["human_review_required"] is True

        blocked_contact = client.post(
            f"/api/conversations/{conversation_id}/engagement-events",
            json={
                "event_type": "CONTACTED",
                "channel": "public_forum",
                "message_text": "Mensaje todavía no aprobado",
                "occurred_at": "2026-07-18T12:00:00Z",
            },
        )
        assert blocked_contact.status_code == 409

        reviewed = client.post(
            f"/api/conversations/{conversation_id}/reviews",
            json={
                "decision": "APPROVE_APPROACH",
                "edited_response": "Hola. Leí tu reflexión y quisiera compartirte Inlak'ech.",
                "reviewer_notes": "Aprobado durante la validación local",
            },
        )
        assert reviewed.status_code == 200
        assert reviewed.json()["decision"] == "APPROVE_APPROACH"

        contacted = client.post(
            f"/api/conversations/{conversation_id}/engagement-events",
            json={
                "event_type": "CONTACTED",
                "channel": "public_forum",
                "message_text": "Hola. Leí tu reflexión y quisiera compartirte Inlak'ech.",
                "occurred_at": "2026-07-18T12:00:00Z",
            },
        )
        assert contacted.status_code == 200
        assert contacted.json()["event_type"] == "CONTACTED"

        replied = client.post(
            f"/api/conversations/{conversation_id}/engagement-events",
            json={
                "event_type": "REPLIED",
                "channel": "public_forum",
                "response_text": "Gracias, me interesa conocer el proyecto.",
                "occurred_at": "2026-07-18T13:00:00Z",
            },
        )
        assert replied.status_code == 200

        review_history = client.get(
            f"/api/conversations/{conversation_id}/reviews"
        )
        assert review_history.status_code == 200
        assert len(review_history.json()) == 1

        engagement_history = client.get(
            f"/api/conversations/{conversation_id}/engagement-events"
        )
        assert engagement_history.status_code == 200
        assert [item["event_type"] for item in engagement_history.json()] == [
            "CONTACTED",
            "REPLIED",
        ]

        refreshed = client.get("/api/conversations")
        assert refreshed.status_code == 200
        reviewed_item = next(
            item for item in refreshed.json() if item["id"] == conversation_id
        )
        assert reviewed_item["status"] == "REPLIED"
