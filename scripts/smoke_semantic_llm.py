from __future__ import annotations

from app.core.config import settings
from app.semantics.llm_classifier import assess_with_optional_llm_details


SAMPLE_TEXT = (
    "Estoy evaluando mudarme a Yucatán y participar en una comunidad regenerativa. "
    "Me interesa conocer los costos, el modelo de participación y los plazos antes de decidir."
)


def main() -> int:
    if not settings.semantic_llm_enabled:
        print("AGNES_SMOKE: FAIL")
        print("ERROR: semantic LLM is disabled")
        return 1
    if not settings.semantic_llm_model:
        print("AGNES_SMOKE: FAIL")
        print("ERROR: semantic LLM model is missing")
        return 1
    if not settings.semantic_llm_api_key:
        print("AGNES_SMOKE: FAIL")
        print("ERROR: AGNES_API_KEY is missing")
        return 1

    execution = assess_with_optional_llm_details(
        SAMPLE_TEXT,
        enabled=settings.semantic_llm_enabled,
        model_name=settings.semantic_llm_model,
        provider_name=settings.semantic_llm_provider,
        base_url=settings.semantic_llm_base_url,
        api_key=settings.semantic_llm_api_key,
    )

    fallback = execution.semantic_engine == "deterministic_fallback"
    result = execution.result

    print(f"AGNES_SMOKE: {'FAIL' if fallback else 'PASS'}")
    print(f"MODEL: {execution.model_name}")
    print(f"SEMANTIC_ENGINE: {execution.semantic_engine}")
    print(f"FALLBACK: {str(fallback).lower()}")
    print(f"DECLARED_CAPACITY: {result.declared_capacity.value}")
    print(f"REVIEW_PRIORITY: {result.review_priority}")
    print(f"RECOMMENDED_ACTION: {result.recommended_action.value}")
    print(f"HUMAN_REVIEW_REQUIRED: {str(result.human_review_required).lower()}")
    print(f"PROVISIONAL: {str(result.provisional).lower()}")
    return 1 if fallback else 0


if __name__ == "__main__":
    raise SystemExit(main())
