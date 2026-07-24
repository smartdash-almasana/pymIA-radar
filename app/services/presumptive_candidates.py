from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment_v3 import ConversationAssessmentV3
from app.models.conversation import Conversation
from app.models.conversation_participant import ConversationParticipant
from app.models.presumptive_candidate import PresumptiveCandidate
from app.models.public_actor import PublicActor
from app.schemas.assessment_v3 import ApparentAffinity, AssessmentStatusV3, ReviewActionV3
from app.schemas.presumptive_candidate import PresumptiveCandidateStatus

SKILL_PATH = Path(__file__).resolve().parents[2] / "config" / "semantic_skills" / "inlakech_affinity_v1.yaml"


class PublicActorInput(NamedTuple):
    platform: str
    platform_actor_id: str
    public_username: str
    display_name: str | None = None
    public_profile_url: str | None = None
    platform_comment_id: str | None = None
    role: str = "author"


def public_actor_key(platform: str, platform_actor_id: str) -> str:
    return f"{platform}:{platform_actor_id}"


def semantic_skill_version() -> str:
    with SKILL_PATH.open(encoding="utf-8") as file:
        payload = yaml.safe_load(file)
    return str(payload["version"])


def is_candidate_eligible(assessment: ConversationAssessmentV3) -> bool:
    return (
        assessment.assessment_status == AssessmentStatusV3.COMPLETED.value
        and assessment.apparent_affinity in {ApparentAffinity.POSSIBLE.value, ApparentAffinity.CLEAR.value}
        and bool(assessment.evidence_fragments)
        and assessment.recommended_review_action in {ReviewActionV3.OBSERVE.value, ReviewActionV3.REVIEW.value}
    )


def _initial_status(assessment: ConversationAssessmentV3) -> PresumptiveCandidateStatus:
    if assessment.recommended_review_action == ReviewActionV3.OBSERVE.value:
        return PresumptiveCandidateStatus.OBSERVED
    return PresumptiveCandidateStatus.INTERPRETATION_PENDING


def _default_actor_input(conversation: Conversation) -> PublicActorInput:
    username = (conversation.author_name or "autor_publico_no_identificado").strip()
    platform_actor_id = username if username != "autor_publico_no_identificado" else f"conversation:{conversation.external_id}"
    return PublicActorInput(
        platform=conversation.source,
        platform_actor_id=platform_actor_id,
        public_username=username,
        display_name=conversation.author_name,
        public_profile_url=None,
        role="author",
    )


def upsert_public_actor(db: Session, actor_input: PublicActorInput) -> PublicActor:
    actor = db.scalar(
        select(PublicActor).where(
            PublicActor.platform == actor_input.platform,
            PublicActor.platform_actor_id == actor_input.platform_actor_id,
        )
    )
    if actor is None:
        actor = PublicActor(
            platform=actor_input.platform,
            platform_actor_id=actor_input.platform_actor_id,
            public_username=actor_input.public_username,
            display_name=actor_input.display_name,
            public_profile_url=actor_input.public_profile_url,
        )
        db.add(actor)
        db.flush()
        return actor

    actor.public_username = actor_input.public_username
    actor.display_name = actor_input.display_name
    actor.public_profile_url = actor_input.public_profile_url
    db.flush()
    return actor


def upsert_conversation_participant(
    db: Session,
    *,
    conversation: Conversation,
    actor: PublicActor,
    actor_input: PublicActorInput,
) -> ConversationParticipant:
    participant = db.scalar(
        select(ConversationParticipant).where(
            ConversationParticipant.conversation_id == conversation.id,
            ConversationParticipant.public_actor_id == actor.id,
        )
    )
    if participant is None:
        participant = ConversationParticipant(
            conversation_id=conversation.id,
            public_actor_id=actor.id,
            platform_comment_id=actor_input.platform_comment_id,
            role=actor_input.role,
        )
        db.add(participant)
        db.flush()
        return participant

    participant.platform_comment_id = actor_input.platform_comment_id
    participant.role = actor_input.role
    db.flush()
    return participant


def create_or_update_presumptive_candidate(
    db: Session,
    *,
    conversation: Conversation,
    assessment: ConversationAssessmentV3,
    actor_input: PublicActorInput | None = None,
    skill_version: str | None = None,
) -> PresumptiveCandidate | None:
    if not is_candidate_eligible(assessment):
        return None
    if assessment.conversation_id != conversation.id:
        return None

    resolved_actor_input = actor_input or _default_actor_input(conversation)
    actor = upsert_public_actor(db, resolved_actor_input)
    upsert_conversation_participant(
        db,
        conversation=conversation,
        actor=actor,
        actor_input=resolved_actor_input,
    )

    candidate = db.scalar(
        select(PresumptiveCandidate).where(
            PresumptiveCandidate.public_actor_id == actor.id,
            PresumptiveCandidate.conversation_id == conversation.id,
        )
    )
    if candidate is None:
        candidate = PresumptiveCandidate(
            public_actor_id=actor.id,
            conversation_id=conversation.id,
            assessment_id=assessment.id,
            status=_initial_status(assessment).value,
            apparent_affinity=assessment.apparent_affinity or "",
            apparent_intention=assessment.apparent_intention or "",
            false_positive_risk=assessment.false_positive_risk or "",
            review_priority=assessment.review_priority,
            skill_version=skill_version or semantic_skill_version(),
            model_name=assessment.model_name,
        )
        db.add(candidate)
    else:
        candidate.assessment_id = assessment.id
        candidate.apparent_affinity = assessment.apparent_affinity or candidate.apparent_affinity
        candidate.apparent_intention = assessment.apparent_intention or candidate.apparent_intention
        candidate.false_positive_risk = assessment.false_positive_risk or candidate.false_positive_risk
        candidate.review_priority = assessment.review_priority
        candidate.skill_version = skill_version or candidate.skill_version
        candidate.model_name = assessment.model_name
    db.flush()
    return candidate


def observe_presumptive_candidate(db: Session, candidate_id: int) -> PresumptiveCandidate | None:
    candidate = db.get(PresumptiveCandidate, candidate_id)
    if candidate is None:
        return None
    if candidate.status == PresumptiveCandidateStatus.INTERPRETATION_PENDING.value:
        candidate.status = PresumptiveCandidateStatus.OBSERVED.value
        db.flush()
    return candidate


def discard_presumptive_candidate(db: Session, candidate_id: int) -> PresumptiveCandidate | None:
    candidate = db.get(PresumptiveCandidate, candidate_id)
    if candidate is None:
        return None
    if candidate.status in {
        PresumptiveCandidateStatus.INTERPRETATION_PENDING.value,
        PresumptiveCandidateStatus.OBSERVED.value,
    }:
        candidate.status = PresumptiveCandidateStatus.DISCARDED.value
        db.flush()
    return candidate
