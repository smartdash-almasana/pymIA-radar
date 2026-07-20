from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--database", default="data/radar-local.db")
    value.add_argument("--limit", type=int, default=10)
    value.add_argument("--runs", type=int, default=3)
    value.add_argument("--ids", default="")
    value.add_argument("--report", default="data/semantic-stability/latest.json")
    value.add_argument("--list-only", action="store_true")
    return value


def enum_value(value: object) -> object:
    return getattr(value, "value", value)


def main() -> int:
    args = parser().parse_args()
    root = Path(__file__).resolve().parents[1]
    database = (root / args.database).resolve()
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{database.as_posix()}"

    from sqlalchemy import desc, func, select
    from app.core.config import settings
    from app.db.session import SessionLocal
    from app.models.assessment_v3 import ConversationAssessmentV3
    from app.models.conversation import Conversation
    from app.models.discovery import DiscoveryCandidate
    from app.semantics.conversation_assessment_v3 import assess_conversation_v3

    ids = [int(item) for item in args.ids.split(",") if item.strip()]
    with SessionLocal() as db:
        before = db.scalar(select(func.count()).select_from(DiscoveryCandidate)) or 0
        query = select(Conversation)
        if ids:
            query = query.where(Conversation.id.in_(ids)).order_by(Conversation.id)
        else:
            query = (
                query.where(Conversation.query_origin.is_not(None))
                .where(Conversation.source.not_in(("discovery_test", "api_test")))
                .order_by(desc(Conversation.id))
                .limit(args.limit)
            )
        conversations = list(db.scalars(query))
        if not conversations:
            raise SystemExit("no persisted conversations available")

        if args.list_only:
            print(json.dumps([
                {
                    "id": item.id,
                    "source": item.source,
                    "query_origin": item.query_origin,
                    "title": (item.title or "")[:120],
                    "status": item.status,
                }
                for item in conversations
            ], ensure_ascii=False, indent=2))
            return 0

        rows = []
        for conversation in conversations:
            latest = db.scalar(
                select(ConversationAssessmentV3)
                .where(ConversationAssessmentV3.conversation_id == conversation.id)
                .order_by(desc(ConversationAssessmentV3.id)).limit(1)
            )
            runs = []
            for number in range(1, args.runs + 1):
                result = assess_conversation_v3(
                    conversation_id=conversation.id,
                    title=conversation.title,
                    text=conversation.text,
                    context=conversation.context,
                    enabled=settings.semantic_llm_enabled,
                    model_name=settings.semantic_llm_model or settings.openai_model,
                    provider_name=settings.semantic_llm_provider,
                    base_url=settings.semantic_llm_base_url,
                    api_key=settings.semantic_llm_api_key or settings.openai_api_key,
                )
                runs.append({
                    "run": number,
                    "status": enum_value(result.assessment_status),
                    "action": enum_value(result.recommended_review_action),
                    "priority": result.review_priority,
                    "affinity": enum_value(result.apparent_affinity),
                    "intention": enum_value(result.apparent_intention),
                    "risk": enum_value(result.false_positive_risk),
                    "uncertainty": enum_value(result.uncertainty),
                    "evidence": len(result.evidence_fragments),
                    "rejected_evidence": len(result.rejected_evidence_fragments),
                    "error": result.safe_error_code,
                })
            actions = [item["action"] for item in runs]
            priorities = [item["priority"] for item in runs]
            rows.append({
                "conversation_id": conversation.id,
                "source": conversation.source,
                "query_origin": conversation.query_origin,
                "title": (conversation.title or "")[:160],
                "conversation_status": conversation.status,
                "baseline_action": latest.recommended_review_action if latest else None,
                "runs": runs,
                "action_stable": len(set(actions)) == 1,
                "action_counts": dict(Counter(actions)),
                "priority_min": min(priorities),
                "priority_max": max(priorities),
                "priority_mean": round(mean(priorities), 2),
                "discarded_promoted": conversation.status in {"DISCARDED", "DO_NOT_CONTACT"} and "REVIEW" in actions,
            })
            print(f"conversation={conversation.id} actions={actions} priorities={priorities}")

        after = db.scalar(select(func.count()).select_from(DiscoveryCandidate)) or 0

    total = len(rows) * args.runs
    completed = sum(run["status"] == "COMPLETED" for row in rows for run in row["runs"])
    stable = sum(row["action_stable"] for row in rows)
    report = {
        "schema_version": "radar-semantic-stability/v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "provider": settings.semantic_llm_provider,
        "model": settings.semantic_llm_model,
        "conversation_count": len(rows),
        "runs_per_conversation": args.runs,
        "total_runs": total,
        "completed_runs": completed,
        "stable_action_count": stable,
        "discarded_promoted_count": sum(row["discarded_promoted"] for row in rows),
        "candidate_count_before": before,
        "candidate_count_after": after,
        "candidate_count_unchanged": before == after,
        "assessments": rows,
    }
    target = (root / args.report).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"completed={completed}/{total} stable={stable}/{len(rows)} candidates_unchanged={before == after}")
    print(target)
    return 0 if completed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
