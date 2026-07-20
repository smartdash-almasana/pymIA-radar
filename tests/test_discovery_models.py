from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import Base
from app.models.conversation import Conversation
from app.models.discovery import DiscoveryCandidate, DiscoveryOutcome
from app.models.engagement import EngagementEvent
from app.models.qualification import QualificationRecord
from app.workflow import DiscoveryState


def _engine():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def _conversation() -> Conversation:
    return Conversation(
        source="test",
        external_id="candidate-origin",
        conversation_url="https://example.com/thread/1",
        author_name="Persona pública",
        text="Conversación de prueba",
        engagement={},
    )


def test_candidate_is_unique_per_origin_conversation() -> None:
    engine = _engine()
    try:
        with Session(engine) as session:
            conversation = _conversation()
            session.add(conversation)
            session.flush()
            session.add(
                DiscoveryCandidate(
                    origin_conversation_id=conversation.id,
                    public_name=conversation.author_name,
                    discovery_state=DiscoveryState.DISCOVERY_CANDIDATE.value,
                    created_by="reviewer",
                )
            )
            session.commit()

            session.add(
                DiscoveryCandidate(
                    origin_conversation_id=conversation.id,
                    public_name=conversation.author_name,
                    discovery_state=DiscoveryState.DISCOVERY_CANDIDATE.value,
                    created_by="another-reviewer",
                )
            )
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
            else:
                raise AssertionError("duplicate discovery candidate was accepted")
    finally:
        engine.dispose()


def test_outcome_is_unique_per_candidate() -> None:
    engine = _engine()
    try:
        with Session(engine) as session:
            conversation = _conversation()
            session.add(conversation)
            session.flush()
            candidate = DiscoveryCandidate(
                origin_conversation_id=conversation.id,
                public_name=conversation.author_name,
                discovery_state=DiscoveryState.DISCOVERY_CANDIDATE.value,
                created_by="reviewer",
            )
            session.add(candidate)
            session.flush()
            session.add(
                DiscoveryOutcome(
                    discovery_candidate_id=candidate.id,
                    sympathy_revealed="YES",
                    revealed_affinity_level="PARTIAL",
                    revealed_affinity_domains=["COMMUNITY"],
                    questions_or_interests=[],
                    objections=[],
                    wants_to_continue=True,
                    consent_to_prequalification=False,
                    archetype_evidence=[],
                    archetype_human_confirmed=False,
                    recorded_by="reviewer",
                )
            )
            session.commit()

            session.add(
                DiscoveryOutcome(
                    discovery_candidate_id=candidate.id,
                    sympathy_revealed="UNCLEAR",
                    revealed_affinity_level="NONE",
                    revealed_affinity_domains=[],
                    questions_or_interests=[],
                    objections=[],
                    wants_to_continue=False,
                    consent_to_prequalification=False,
                    archetype_evidence=[],
                    archetype_human_confirmed=False,
                    recorded_by="reviewer",
                )
            )
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
            else:
                raise AssertionError("duplicate discovery outcome was accepted")
    finally:
        engine.dispose()


def test_historical_references_are_nullable() -> None:
    engine = _engine()
    try:
        inspector = inspect(engine)
        engagement_columns = {
            item["name"]: item for item in inspector.get_columns(EngagementEvent.__tablename__)
        }
        qualification_columns = {
            item["name"]: item
            for item in inspector.get_columns(QualificationRecord.__tablename__)
        }
        assert engagement_columns["discovery_candidate_id"]["nullable"] is True
        assert qualification_columns["discovery_candidate_id"]["nullable"] is True
        assert qualification_columns["discovery_outcome_id"]["nullable"] is True
    finally:
        engine.dispose()
