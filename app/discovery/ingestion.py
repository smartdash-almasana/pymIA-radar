from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.discovery.contracts import DiscoveryResult
from app.models.conversation import Conversation
from app.schemas.conversation import conversation_orm_payload


def persist_discovery_results(
    db: Session,
    results: list[DiscoveryResult],
) -> list[Conversation]:
    """Persist normalized discovery results idempotently.

    Existing rows are returned unchanged. New rows are inserted once using the
    product identity boundary: source + external_id.
    """
    persisted: list[Conversation] = []
    seen: set[tuple[str, str]] = set()

    for result in results:
        key = (result.source, result.external_id)
        if key in seen:
            continue
        seen.add(key)

        existing = db.scalar(
            select(Conversation).where(
                Conversation.source == result.source,
                Conversation.external_id == result.external_id,
            )
        )
        if existing is not None:
            persisted.append(existing)
            continue

        conversation = Conversation(**conversation_orm_payload(result))
        db.add(conversation)
        db.flush()
        persisted.append(conversation)

    db.commit()
    for conversation in persisted:
        db.refresh(conversation)
    return persisted
