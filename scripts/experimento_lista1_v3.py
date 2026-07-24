"""Experimento v3: max_tokens=4096 con los 3 casos reales de Lista 1.

Ejecuta assess_conversation_v3 para cada caso con el pipeline corregido
(skill v1.1.0 + normalizer + retry + max_tokens=4096 + truncation detection).
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.schemas.assessment_v3 import AssessmentStatusV3
from app.semantics.conversation_assessment_v3 import assess_conversation_v3, build_v3_runner

CASOS = [
    {
        "id": "A",
        "title": "Seeking co-creators to build an ecovillage in Mexico",
        "text": (
            "I'm looking for like-minded people to help create a regenerative community "
            "in Mexico, preferably in Yucatán or neighboring states. We already have a "
            "piece of land and we need people with skills in permaculture, natural building, "
            "water management, and community governance. The vision is a self-sustaining "
            "village that respects the local ecosystem and culture. We're not a business, "
            "we're a community project."
        ),
        "context": "Posted in r/intentionalcommunity",
        "expected": {
            "status": AssessmentStatusV3.COMPLETED,
            "affinity": "CLEAR",
            "intention": "ACTION_ORIENTED",
            "min_evidence": 3,
        },
    },
    {
        "id": "B",
        "title": "Curious about life in Yucatán",
        "text": (
            "I've been reading about Yucatán and it seems like a nice place. "
            "Has anyone here moved there? What's it like? I'm just curious, "
            "not planning anything yet."
        ),
        "context": "Posted in r/mexico",
        "expected": {
            "status": AssessmentStatusV3.COMPLETED,
            "affinity": "NONE",
            "intention": "NONE",
            "max_evidence": 1,
        },
    },
    {
        "id": "C",
        "title": "Real estate investment in Yucatán",
        "text": (
            "I want to invest in real estate in Yucatán. Looking for good deals "
            "on beachfront properties. I have capital ready and want to see returns "
            "within 2-3 years. Any recommendations for agents or developments?"
        ),
        "context": "Posted in r/Yucatan",
        "expected": {
            "status": AssessmentStatusV3.COMPLETED,
            "affinity": "NONE",
            "intention": "NONE",
            "max_evidence": 1,
        },
    },
]


def _summarize(result, caso, elapsed) -> dict:
    """Build a human-readable summary row."""
    is_ok = (
        result.assessment_status == caso["expected"]["status"]
        and result.apparent_affinity == caso["expected"]["affinity"]
    )
    evidence_count = len(result.evidence_fragments)
    return {
        "caso": caso["id"],
        "title_preview": caso["title"][:50],
        "status": result.assessment_status.value,
        "affinity": (result.apparent_affinity or "N/A"),
        "intention": (result.apparent_intention or "N/A"),
        "evidence": evidence_count,
        "action": result.recommended_review_action.value,
        "human_review": result.human_review_required,
        "safe_error": result.safe_error_code or "-",
        "elapsed_s": round(elapsed, 2),
        "expected_affinity": caso["expected"]["affinity"],
        "expected_status": caso["expected"]["status"].value,
        "PASS": "PASS" if is_ok else "FAIL",
        "details": "",
    }


def run():
    print("# Experimento v3 — max_tokens=4096")
    print(f"Modelo: {settings.semantic_llm_model}")
    print(f"Proveedor: agnes")
    print(f"max_tokens: {settings.semantic_max_tokens}")
    print(f"Fecha: {datetime.now(timezone.utc).isoformat()}")
    print()

    results = []
    runner = build_v3_runner(
        settings.semantic_llm_model,
        provider_name="agnes",
        base_url=settings.semantic_llm_base_url,
        api_key=settings.semantic_llm_api_key or settings.openai_api_key,
    )

    for caso in CASOS:
        print(f"--- Caso {caso['id']}: {caso['title'][:60]} ---")
        import time

        t0 = time.perf_counter()
        result = assess_conversation_v3(
            conversation_id=ord(caso["id"]),
            title=caso["title"],
            text=caso["text"],
            context=caso["context"],
            enabled=True,
            model_name=settings.semantic_llm_model,
            provider_name="agnes",
            base_url=settings.semantic_llm_base_url,
            api_key=settings.semantic_llm_api_key or settings.openai_api_key,
            runner=runner,
        )
        elapsed = time.perf_counter() - t0
        results.append(_summarize(result, caso, elapsed))
        print()

    # Summary table
    header = f"{'Caso':<6} {'Status':<28} {'Afinidad':<12} {'Intención':<20} {'Evid':<5} {'Acción':<10} {'Error':<16} {'Resultado':<5}"
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in results:
        print(
            f"{r['caso']:<6} {r['status']:<28} {r['affinity']:<12} {r['intention']:<20} "
            f"{r['evidence']:<5} {r['action']:<10} {r['safe_error']:<16} {r['PASS']:<5}"
        )
    print(sep)

    passed = sum(1 for r in results if r["PASS"] == "✅")
    print(f"\n{passed}/{len(results)} pasaron")

    # Write report file
    report_path = Path(__file__).resolve().parents[1] / ".tmp"
    report_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report_file = report_path / f"reporte-experimento-lista1-v3-{timestamp}.json"
    report_file.write_text(
        json.dumps(results, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"\nReporte: {report_file}")


if __name__ == "__main__":
    run()
