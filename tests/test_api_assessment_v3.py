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
    external_id = f"v3-{uuid4()}"
    return {
        "source": "test_source_v3",
        "external_id": external_id,
        "conversation_url": f"https://example.com/{external_id}",
        "author_name": "Persona V3",
        "title": "Comunidad regenerativa",
        "text": "Busco una comunidad regenerativa en Yucatán y quiero conocer opciones.",
        "context": "Consulta pública sobre alternativas de participación.",
        "query_origin": "comunidad regenerativa yucatan",
        "engagement": {},
    }


def _completed_result(conversation_id: int) -> ConversationAssessmentV3Result:
    return ConversationAssessmentV3Result(
        conversation_id=conversation_id,
        assessment_status=AssessmentStatusV3.COMPLETED,
        real_topic="Búsqueda de comunidad regenerativa",
        contextual_meaning="La persona solicita alternativas concretas.",
        apparent_affinity=ApparentAffinity.CLEAR,
        apparent_affinity_domains=[AffinityDomain.COMMUNITY, AffinityDomain.REGENERATION],
        apparent_intention=ApparentIntention.EXPLORATION,
        intention_summary="Explora opciones de participación.",
        evidence_fragments=[
            "Busco una comunidad regenerativa en Yucatán y quiero conocer opciones."
        ],
        contradictions=[],
        missing_context=[],
        false_positive_risk=RiskLevelV3.LOW,
        uncertainty=RiskLevelV3.LOW,
        human_review_reason="Existe evidencia suficiente para revisión humana.",
        review_priority=92,
        recommended_review_action=ReviewActionV3.REVIEW,
        semantic_engine="llm:test",
        model_name="test-model",
    )


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
        primary_provider_attempted="agnes",
        primary_provider_used="agnes",
        provider_failover=False,
    )


def test_v3_api_persists_history_without_mutating_conversation_status(monkeypatch) -> None:
    with TestClient(app) as client:
        created = client.post("/api/conversations", json=_conversation_payload())
        assert created.status_code == 200
        conversation_id = created.json()["id"]
        initial_status = created.json()["status"]

        monkeypatch.setattr(
            "app.api.routes.assess_conversation_cascade_v1",
            lambda **_: _cascade_result(conversation_id),
        )
        assessed = client.post(
            f"/api/conversations/{conversation_id}/assessments/v3"
        )
        second_assessment = client.post(
            f"/api/conversations/{conversation_id}/assessments/v3"
        )
        assert assessed.status_code == 200
        assert second_assessment.status_code == 200
        body = assessed.json()
        assert body["schema_version"] == "radar-conversation-assessment/v3"
        assert body["assessment_status"] == "COMPLETED"
        assert body["apparent_affinity"] == "CLEAR"
        assert "probable_archetype" not in body
        assert "declared_capacity" not in body

        cascade = client.get(
            f"/api/conversations/{conversation_id}/assessments/v3/{body['id']}/cascade"
        )
        assert cascade.status_code == 200
        assert cascade.json()["deterministic_resolution"] == "GEMMA_NOT_REQUIRED"
        assert cascade.json()["gemma_review_triggered"] is False

        history = client.get(
            f"/api/conversations/{conversation_id}/assessments/v3"
        )
        assert history.status_code == 200
        assert len(history.json()) == 2
        assert all(item["semantic_engine"] == "llm:test" for item in history.json())
        assert client.get(
            f"/api/conversations/{conversation_id}/assessments"
        ).json() == []
        assert client.get(
            f"/api/conversations/{conversation_id}/engagement-events"
        ).json() == []
        assert client.get(
            f"/api/conversations/{conversation_id}/qualifications"
        ).json() == []

        conversations = client.get("/api/conversations").json()
        refreshed = next(item for item in conversations if item["id"] == conversation_id)
        assert refreshed["status"] == initial_status


def test_v3_api_persists_unavailable_attempt(monkeypatch) -> None:
    from app.core.config import settings

    monkeypatch.setattr(settings, "semantic_llm_enabled", False)
    with TestClient(app) as client:
        created = client.post("/api/conversations", json=_conversation_payload())
        conversation_id = created.json()["id"]
        assessed = client.post(
            f"/api/conversations/{conversation_id}/assessments/v3"
        )
        assert assessed.status_code == 200
        body = assessed.json()
        assert body["assessment_status"] == "SEMANTIC_ASSESSMENT_UNAVAILABLE"
        assert body["apparent_affinity"] is None
        assert body["review_priority"] == 0
        assert body["safe_error_code"] == "SEMANTIC_ENGINE_DISABLED_OR_MODEL_MISSING"

        history = client.get(
            f"/api/conversations/{conversation_id}/assessments/v3"
        ).json()
        assert history[-1]["assessment_status"] == "SEMANTIC_ASSESSMENT_UNAVAILABLE"


def test_v3_api_returns_404_for_unknown_conversation() -> None:
    with TestClient(app) as client:
        response = client.post("/api/conversations/999999/assessments/v3")
        assert response.status_code == 404
