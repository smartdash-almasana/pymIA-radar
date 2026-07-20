from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.session import SessionLocal, init_db
from app.main import app
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.presumptive_candidate import PresumptiveCandidate
from app.schemas.assessment_v3 import ApparentAffinity, ApparentIntention, AssessmentStatusV3, ReviewActionV3, RiskLevelV3
from app.schemas.presumptive_candidate import PresumptiveCandidateStatus
from app.services.presumptive_candidates import PublicActorInput, create_or_update_presumptive_candidate


def _seed_ui_candidate(*, username: str = "actor_publico_lista") -> int:
    init_db()
    with SessionLocal() as db:
        conversation = Conversation(
            source="reddit",
            external_id=f"ui-{uuid4()}",
            conversation_url=f"https://www.reddit.com/r/inlakech/comments/{uuid4()}",
            author_name=username,
            title="Participar en una comunidad regenerativa en Yucatán",
            text="Quiero participar en una comunidad regenerativa en Yucatán con visión de largo plazo.",
            context="Comentario público con búsqueda explícita de comunidad y participación.",
            published_at=datetime(2026, 7, 20, tzinfo=UTC),
            query_origin="comunidad regenerativa yucatán",
            status="ASSESSED",
        )
        db.add(conversation)
        db.flush()
        assessment = ConversationAssessmentV3(
            conversation_id=conversation.id,
            assessment_status=AssessmentStatusV3.COMPLETED.value,
            real_topic="comunidad regenerativa en Yucatán",
            contextual_meaning="La conversación expresa exploración compatible con Inlak'ech.",
            apparent_affinity=ApparentAffinity.CLEAR.value,
            apparent_affinity_domains=["COMMUNITY", "REGENERATION", "LONG_TERM"],
            apparent_intention=ApparentIntention.EXPLORATION.value,
            intention_summary="La persona busca participar.",
            evidence_fragments=["Quiero participar en una comunidad regenerativa en Yucatán"],
            rejected_evidence_fragments=[],
            contradictions=[],
            missing_context=[],
            false_positive_risk=RiskLevelV3.LOW.value,
            uncertainty=RiskLevelV3.LOW.value,
            human_review_reason="Revisión humana requerida.",
            review_priority=91,
            recommended_review_action=ReviewActionV3.REVIEW.value,
            semantic_engine="llm:test",
            model_name="MiMo 2.5 Free",
        )
        db.add(assessment)
        db.flush()
        candidate = create_or_update_presumptive_candidate(
            db,
            conversation=conversation,
            assessment=assessment,
            actor_input=PublicActorInput(
                platform="reddit",
                platform_actor_id=f"actor-{username}",
                public_username=username,
                display_name="Actor público visible",
                public_profile_url=f"https://www.reddit.com/user/{username}",
                platform_comment_id="comment-visible-1",
                role="commenter",
            ),
            skill_version="1.0.0",
        )
        assert candidate is not None
        db.commit()
        return candidate.id


def test_presumptive_candidate_list_uses_persisted_data_and_allowed_actions_only() -> None:
    _seed_ui_candidate(username="actor_lista_real")

    with TestClient(app) as client:
        response = client.get("/radar/presumptive-candidates")

    assert response.status_code == 200
    assert "LISTA DE CANDIDATOS POR AFINIDAD SEMÁNTICA PRESUNTIVA" in response.text
    assert "actor_lista_real" in response.text
    assert "comunidad regenerativa en Yucatán" in response.text
    assert "Quiero participar en una comunidad regenerativa en Yucatán" in response.text
    assert "Abrir detalle" in response.text
    assert "Abrir fuente original" in response.text
    assert "Observar" in response.text
    assert "Descartar" in response.text
    assert "Contactar" not in response.text
    assert "Precalificar" not in response.text
    assert "Transferir" not in response.text
    assert "Relaticle" not in response.text


def test_presumptive_candidate_detail_shows_traceability_without_messages() -> None:
    candidate_id = _seed_ui_candidate(username="actor_detalle_real")

    with TestClient(app) as client:
        response = client.get(f"/radar/presumptive-candidates/{candidate_id}")

    assert response.status_code == 200
    assert "reddit:actor-actor_detalle_real" in response.text
    assert "Abrir perfil público" in response.text
    assert "Participar en una comunidad regenerativa en Yucatán" in response.text
    assert "Comentario público con búsqueda explícita" in response.text
    assert "Evaluación semántica" in response.text
    assert "Skill version" in response.text
    assert "MiMo 2.5 Free" in response.text
    assert "Abrir fuente original" in response.text
    assert "Mensaje" not in response.text
    assert "Contactar" not in response.text


def test_observe_and_discard_actions_change_only_candidate_status() -> None:
    candidate_id = _seed_ui_candidate(username="actor_estado_real")

    with SessionLocal() as db:
        before = db.get(PresumptiveCandidate, candidate_id)
        assert before is not None
        unchanged = {
            "public_actor_id": before.public_actor_id,
            "conversation_id": before.conversation_id,
            "assessment_id": before.assessment_id,
            "apparent_affinity": before.apparent_affinity,
            "apparent_intention": before.apparent_intention,
            "false_positive_risk": before.false_positive_risk,
            "review_priority": before.review_priority,
            "skill_version": before.skill_version,
            "model_name": before.model_name,
        }

    with TestClient(app) as client:
        observed = client.post(f"/htmx/presumptive-candidates/{candidate_id}/observe")
        discarded = client.post(f"/htmx/presumptive-candidates/{candidate_id}/discard")

    assert observed.status_code == 200
    assert PresumptiveCandidateStatus.OBSERVED.value in observed.text
    assert discarded.status_code == 200
    assert PresumptiveCandidateStatus.DISCARDED.value in discarded.text

    with SessionLocal() as db:
        after = db.get(PresumptiveCandidate, candidate_id)
        assert after is not None
        assert after.status == PresumptiveCandidateStatus.DISCARDED.value
        for field, value in unchanged.items():
            assert getattr(after, field) == value
