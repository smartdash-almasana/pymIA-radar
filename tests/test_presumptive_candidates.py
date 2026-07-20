from __future__ import annotations

import ast
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal, init_db
from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.conversation_participant import ConversationParticipant
from app.models.presumptive_candidate import PresumptiveCandidate
from app.models.public_actor import PublicActor
from app.schemas.assessment_v3 import ApparentAffinity, ApparentIntention, AssessmentStatusV3, ReviewActionV3, RiskLevelV3
from app.schemas.presumptive_candidate import PresumptiveCandidateStatus
from app.services.presumptive_candidates import PublicActorInput, create_or_update_presumptive_candidate


def _conversation(*, source: str = "reddit", author_name: str = "usuario_regenerativo") -> Conversation:
    return Conversation(
        source=source,
        external_id=f"conversation-{uuid4()}",
        conversation_url=f"https://{source}.example.org/conversations/{uuid4()}",
        author_name=author_name,
        title="Busco comunidad regenerativa de largo plazo",
        text="Quiero participar en una comunidad regenerativa en Yucatán con visión de largo plazo.",
        context="Conversación pública capturada por RADAR.",
        published_at=datetime(2026, 7, 20, tzinfo=UTC),
        query_origin="regeneración yucatán",
        status="ASSESSED",
    )


def _assessment(
    conversation: Conversation,
    *,
    status: str = AssessmentStatusV3.COMPLETED.value,
    affinity: str = ApparentAffinity.CLEAR.value,
    intention: str = ApparentIntention.EXPLORATION.value,
    risk: str = RiskLevelV3.LOW.value,
    action: str = ReviewActionV3.REVIEW.value,
    evidence: list[str] | None = None,
) -> ConversationAssessmentV3:
    return ConversationAssessmentV3(
        conversation_id=conversation.id,
        assessment_status=status,
        real_topic="regeneración territorial en Yucatán",
        contextual_meaning="La persona expresa búsqueda compatible con Inlak'ech desde el sentido completo.",
        apparent_affinity=affinity,
        apparent_affinity_domains=["REGENERATION", "COMMUNITY", "LONG_TERM"],
        apparent_intention=intention,
        intention_summary="Busca información y participación.",
        evidence_fragments=evidence if evidence is not None else ["Quiero participar en una comunidad regenerativa en Yucatán"],
        rejected_evidence_fragments=[],
        contradictions=[],
        missing_context=[],
        false_positive_risk=risk,
        uncertainty=RiskLevelV3.LOW.value,
        human_review_reason="Requiere revisión humana antes de cualquier acción externa.",
        review_priority=82,
        recommended_review_action=action,
        semantic_engine="llm:test",
        model_name="MiMo 2.5 Free",
    )


def _persist_candidate(
    *,
    source: str = "reddit",
    username: str = "usuario_regenerativo",
    platform_actor_id: str | None = None,
    action: str = ReviewActionV3.REVIEW.value,
    affinity: str = ApparentAffinity.CLEAR.value,
    status: str = AssessmentStatusV3.COMPLETED.value,
    evidence: list[str] | None = None,
) -> int | None:
    init_db()
    with SessionLocal() as db:
        conversation = _conversation(source=source, author_name=username)
        db.add(conversation)
        db.flush()
        assessment = _assessment(
            conversation,
            status=status,
            affinity=affinity,
            action=action,
            evidence=evidence,
        )
        if affinity == ApparentAffinity.NONE.value:
            assessment.apparent_intention = ApparentIntention.NONE.value
            assessment.false_positive_risk = RiskLevelV3.HIGH.value
            assessment.recommended_review_action = ReviewActionV3.DISCARD.value
            assessment.real_topic = "fútbol internacional"
            assessment.contextual_meaning = "La conversación trata sobre Argentina, Francia, España y Messi."
        db.add(assessment)
        db.flush()
        candidate = create_or_update_presumptive_candidate(
            db,
            conversation=conversation,
            assessment=assessment,
            actor_input=PublicActorInput(
                platform=source,
                platform_actor_id=platform_actor_id or username,
                public_username=username,
                display_name=f"{username} visible",
                public_profile_url=f"https://{source}.example.org/u/{username}",
                platform_comment_id=f"comment-{uuid4()}",
                role="commenter",
            ),
            skill_version="1.0.0",
        )
        db.commit()
        return candidate.id if candidate else None


def test_positive_case_creates_presumptive_candidate() -> None:
    candidate_id = _persist_candidate()
    assert candidate_id is not None

    with SessionLocal() as db:
        candidate = db.get(PresumptiveCandidate, candidate_id)
        assert candidate is not None
        assert candidate.status == PresumptiveCandidateStatus.INTERPRETATION_PENDING.value
        assert candidate.apparent_affinity == ApparentAffinity.CLEAR.value
        assert candidate.review_priority == 82


def test_ambiguous_case_creates_observed_candidate() -> None:
    candidate_id = _persist_candidate(
        username="usuario_ambiguo",
        action=ReviewActionV3.OBSERVE.value,
        affinity=ApparentAffinity.POSSIBLE.value,
    )

    with SessionLocal() as db:
        candidate = db.get(PresumptiveCandidate, candidate_id)
        assert candidate is not None
        assert candidate.status == PresumptiveCandidateStatus.OBSERVED.value
        assert candidate.apparent_affinity == ApparentAffinity.POSSIBLE.value


def test_football_case_does_not_create_candidate() -> None:
    candidate_id = _persist_candidate(
        username="hincha_messi",
        affinity=ApparentAffinity.NONE.value,
        action=ReviewActionV3.DISCARD.value,
        evidence=["Messi is still the best"],
    )

    assert candidate_id is None


def test_exact_duplicate_does_not_create_second_candidate() -> None:
    init_db()
    actor_input = PublicActorInput(
        platform="reddit",
        platform_actor_id="same-actor",
        public_username="same_user",
    )
    with SessionLocal() as db:
        conversation = _conversation(author_name="same_user")
        db.add(conversation)
        db.flush()
        assessment = _assessment(conversation)
        db.add(assessment)
        db.flush()

        first = create_or_update_presumptive_candidate(db, conversation=conversation, assessment=assessment, actor_input=actor_input, skill_version="1.0.0")
        second = create_or_update_presumptive_candidate(db, conversation=conversation, assessment=assessment, actor_input=actor_input, skill_version="1.0.0")
        db.commit()

        assert first is not None
        assert second is not None
        assert first.id == second.id
        count = db.query(PresumptiveCandidate).filter_by(public_actor_id=first.public_actor_id, conversation_id=conversation.id, assessment_id=assessment.id).count()
        assert count == 1


def test_one_actor_can_have_multiple_conversations() -> None:
    init_db()
    actor_input = PublicActorInput(platform="reddit", platform_actor_id="multi", public_username="multi_user")
    with SessionLocal() as db:
        ids = []
        for _ in range(2):
            conversation = _conversation(author_name="multi_user")
            db.add(conversation)
            db.flush()
            assessment = _assessment(conversation)
            db.add(assessment)
            db.flush()
            candidate = create_or_update_presumptive_candidate(db, conversation=conversation, assessment=assessment, actor_input=actor_input, skill_version="1.0.0")
            assert candidate is not None
            ids.append(candidate.id)
        db.commit()

        actor = db.query(PublicActor).filter_by(platform="reddit", platform_actor_id="multi").one()
        candidates = db.query(PresumptiveCandidate).filter_by(public_actor_id=actor.id).all()
        assert len(ids) == 2
        assert len(candidates) == 2


def test_public_identity_is_not_mixed_between_platforms() -> None:
    reddit_id = _persist_candidate(source="reddit", username="same_name", platform_actor_id="same-name")
    twitter_id = _persist_candidate(source="twitter", username="same_name", platform_actor_id="same-name")

    with SessionLocal() as db:
        reddit_candidate = db.get(PresumptiveCandidate, reddit_id)
        twitter_candidate = db.get(PresumptiveCandidate, twitter_id)
        assert reddit_candidate is not None
        assert twitter_candidate is not None
        assert reddit_candidate.public_actor_id != twitter_candidate.public_actor_id
        assert db.query(PublicActor).filter_by(public_username="same_name").count() == 2


@pytest.mark.parametrize(
    ("status", "evidence", "action"),
    [
        (AssessmentStatusV3.SEMANTIC_ASSESSMENT_UNAVAILABLE.value, ["evidencia"], ReviewActionV3.REVIEW.value),
        (AssessmentStatusV3.INVALID_MODEL_OUTPUT.value, ["evidencia"], ReviewActionV3.REVIEW.value),
        (AssessmentStatusV3.INVALID_EVIDENCE.value, ["evidencia"], ReviewActionV3.REVIEW.value),
        (AssessmentStatusV3.COMPLETED.value, [], ReviewActionV3.REVIEW.value),
        (AssessmentStatusV3.COMPLETED.value, ["evidencia"], ReviewActionV3.DISCARD.value),
    ],
)
def test_pending_failed_empty_evidence_and_discard_do_not_create_candidates(status: str, evidence: list[str], action: str) -> None:
    candidate_id = _persist_candidate(
        username=f"excluded_{uuid4()}",
        status=status,
        evidence=evidence,
        action=action,
    )

    assert candidate_id is None


def test_creation_does_not_create_lead_or_message_side_effects() -> None:
    init_db()
    with SessionLocal() as db:
        before_discovery = db.execute(text("SELECT COUNT(*) FROM discovery_candidates")).scalar_one()
        before_engagement = db.execute(text("SELECT COUNT(*) FROM engagement_events")).scalar_one()
        before_qualification = db.execute(text("SELECT COUNT(*) FROM qualification_records")).scalar_one()

    candidate_id = _persist_candidate(username="sin_side_effects")
    assert candidate_id is not None

    with SessionLocal() as db:
        assert db.execute(text("SELECT COUNT(*) FROM discovery_candidates")).scalar_one() == before_discovery
        assert db.execute(text("SELECT COUNT(*) FROM engagement_events")).scalar_one() == before_engagement
        assert db.execute(text("SELECT COUNT(*) FROM qualification_records")).scalar_one() == before_qualification


def test_database_unique_constraints_reject_exact_duplicates() -> None:
    init_db()
    with SessionLocal() as db:
        actor = PublicActor(platform="reddit", platform_actor_id="unique", public_username="unique")
        db.add(actor)
        db.commit()
        db.add(PublicActor(platform="reddit", platform_actor_id="unique", public_username="unique2"))
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()

        conversation = _conversation(author_name="unique")
        db.add(conversation)
        db.flush()
        assessment = _assessment(conversation)
        db.add(assessment)
        db.flush()
        participant = ConversationParticipant(conversation_id=conversation.id, public_actor_id=actor.id, role="author")
        db.add(participant)
        db.commit()
        db.add(ConversationParticipant(conversation_id=conversation.id, public_actor_id=actor.id, role="author"))
        with pytest.raises(IntegrityError):
            db.commit()


def test_migration_upgrades_fresh_database_to_presumptive_candidate_tables(tmp_path: Path) -> None:
    database_path = tmp_path / "presumptive-candidates.db"
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", f"sqlite+pysqlite:///{database_path.as_posix()}")

    command.upgrade(config, "head")

    engine = create_engine(f"sqlite+pysqlite:///{database_path.as_posix()}")
    try:
        inspector = inspect(engine)
        tables = set(inspector.get_table_names())
        assert {"public_actors", "conversation_participants", "presumptive_candidates"}.issubset(tables)
        candidate_columns = {column["name"] for column in inspector.get_columns("presumptive_candidates")}
        assert {"public_actor_id", "conversation_id", "assessment_id", "status", "skill_version"}.issubset(candidate_columns)
    finally:
        engine.dispose()


def test_candidate_modules_do_not_import_forbidden_phase_two_dependencies() -> None:
    forbidden_modules = {"app.qualification", "app.engagement", "app.crm_transfer", "app.integrations.relaticle"}
    files = [
        Path("app/services/presumptive_candidates.py"),
        Path("app/models/public_actor.py"),
        Path("app/models/conversation_participant.py"),
        Path("app/models/presumptive_candidate.py"),
        Path("app/presumptive_candidate_ui.py"),
    ]
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
        assert imports.isdisjoint(forbidden_modules)
