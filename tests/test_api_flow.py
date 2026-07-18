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
        assert assessment_body["relevant"] is True
        assert assessment_body["recommended_action"] == "human_review"
        assert assessment_body["evidence"]

        reviewed = client.post(
            f"/api/conversations/{conversation_id}/review",
            params={
                "decision": "approved",
                "reviewer_notes": "Aprobado durante la validación local de M0",
            },
        )
        assert reviewed.status_code == 200
        assert reviewed.json() == {"status": "ok", "decision": "approved"}

        refreshed = client.get("/api/conversations")
        assert refreshed.status_code == 200
        reviewed_item = next(
            item for item in refreshed.json() if item["id"] == conversation_id
        )
        assert reviewed_item["status"] == "approved"
