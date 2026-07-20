from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    database = (root / "data/radar-local.db").resolve()
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{database.as_posix()}"

    import httpx
    from pydantic import ValidationError
    from app.core.config import settings
    from app.db.session import SessionLocal
    from app.models.conversation import Conversation
    from app.semantics.conversation_assessment_v3 import (
        _extract_provider_content,
        _system_prompt_v3,
        _validate_provider_draft,
        build_conversation_input,
    )

    report: dict = {"diagnostics": []}
    with SessionLocal() as db:
        for conversation_id in (141, 145):
            conversation = db.get(Conversation, conversation_id)
            if conversation is None:
                continue
            text = build_conversation_input(
                title=conversation.title,
                text=conversation.text,
                context=conversation.context,
            )
            for run in range(1, 4):
                item = {"conversation_id": conversation_id, "run": run}
                response = httpx.post(
                    f"{settings.semantic_llm_base_url.rstrip('/')}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.semantic_llm_api_key or settings.openai_api_key or ''}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.semantic_llm_model or settings.openai_model,
                        "messages": [
                            {"role": "system", "content": _system_prompt_v3()},
                            {"role": "user", "content": text},
                        ],
                        "temperature": 0.1,
                        "max_tokens": 2048,
                    },
                    timeout=30,
                )
                item["http_status"] = response.status_code
                try:
                    envelope = response.json()
                    raw = _extract_provider_content(envelope)
                    item["content_type"] = type(raw).__name__
                    item["content_length"] = len(raw) if isinstance(raw, str) else None
                    item["fenced"] = isinstance(raw, str) and raw.lstrip().startswith("```")
                    draft = _validate_provider_draft(raw)
                    item["valid"] = True
                    item["affinity"] = draft.apparent_affinity.value
                    item["intention"] = draft.apparent_intention.value
                except ValidationError as exc:
                    item["valid"] = False
                    item["error_type"] = "ValidationError"
                    item["errors"] = [
                        {
                            "location": [str(part) for part in error.get("loc", ())],
                            "type": error.get("type"),
                            "message": error.get("msg"),
                        }
                        for error in exc.errors()
                    ]
                except Exception as exc:
                    item["valid"] = False
                    item["error_type"] = type(exc).__name__
                    item["error_message"] = str(exc)[:300]
                report["diagnostics"].append(item)

    target = root / "data/semantic-stability/diagnostic.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
