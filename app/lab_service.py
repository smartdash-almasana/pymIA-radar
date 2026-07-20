from __future__ import annotations

import json
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.assessment_v3 import AssessmentStatusV3, SCHEMA_VERSION_V3
from app.semantics.conversation_assessment_v3 import (
    InvalidModelOutputError,
    SemanticProviderError,
    _extract_provider_content,
    SEMANTIC_HTTP_TIMEOUT_SECONDS,
    _system_prompt_v3,
    _validate_provider_draft,
    build_conversation_input,
    distinct_conversation_parts,
    finalize_draft_v3,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
LAB_DIR = ROOT_DIR / "lab"
LAB_CORPUS_PATH = LAB_DIR / "corpus" / "semantic_lab_corpus.v1.json"
DEFAULT_EXPERIMENT_ID = "experimento1"
PROMPT_VERSION = SCHEMA_VERSION_V3
PROVIDERS = ("agnes", "gemma")


@dataclass(frozen=True)
class LabCase:
    case_id: str
    text: str
    context: str | None = None


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    provider_name: str
    model: str | None
    base_url: str | None
    api_key: str | None


def _experiment_path(experiment_id: str = DEFAULT_EXPERIMENT_ID) -> Path:
    safe_id = experiment_id.strip() or DEFAULT_EXPERIMENT_ID
    if not safe_id.startswith("experimento") or any(ch in safe_id for ch in "\\/:"):
        raise ValueError("experiment_id inválido")
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    return LAB_DIR / f"{safe_id}.md"


def list_experiments() -> list[dict[str, str]]:
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for path in sorted(LAB_DIR.glob("experimento*.md"), reverse=True):
        items.append({"name": path.name, "content": path.read_text(encoding="utf-8")})
    return items


def load_lab_cases() -> list[LabCase]:
    if not LAB_CORPUS_PATH.exists():
        raise ValueError(f"Corpus de laboratorio no encontrado: {LAB_CORPUS_PATH}")
    payload = json.loads(LAB_CORPUS_PATH.read_text(encoding="utf-8"))
    cases: list[LabCase] = []
    for item in payload.get("cases", []):
        case_id = str(item.get("case_id", "")).strip()
        text = str(item.get("text", "")).strip()
        context = item.get("context")
        if not case_id.startswith("CASE_") or not text:
            raise ValueError("Corpus de laboratorio inválido")
        cases.append(LabCase(case_id=case_id, text=text, context=context))
    if not cases:
        raise ValueError("Corpus de laboratorio vacío")
    return cases


def list_lab_case_options() -> list[dict[str, str]]:
    return [{"case_id": item.case_id} for item in load_lab_cases()]


def get_lab_case(case_id: str) -> dict[str, str | None]:
    for item in load_lab_cases():
        if item.case_id == case_id:
            return {"case_id": item.case_id, "text": item.text, "context": item.context}
    raise ValueError(f"Caso de laboratorio desconocido: {case_id}")


def _provider_config(provider: str) -> ProviderConfig:
    if provider == "agnes":
        return ProviderConfig(
            provider="agnes",
            provider_name="agnes",
            model=settings.semantic_llm_model or settings.openai_model,
            base_url=settings.semantic_llm_base_url,
            api_key=settings.semantic_llm_api_key or settings.openai_api_key,
        )
    if provider == "gemma":
        return ProviderConfig(
            provider="gemma",
            provider_name="openai_compatible",
            model=settings.gemini_model,
            base_url=settings.gemini_base_url,
            api_key=settings.gemini_api_key,
        )
    raise ValueError(f"Proveedor desconocido: {provider}")


def _failure_parsed_output(
    *, case_index: int, config: ProviderConfig, safe_error_code: str
) -> dict[str, Any]:
    return {
        "conversation_id": case_index,
        "schema_version": SCHEMA_VERSION_V3,
        "assessment_status": AssessmentStatusV3.SEMANTIC_ASSESSMENT_UNAVAILABLE.value,
        "semantic_engine": f"llm:{config.provider_name}",
        "model_name": config.model,
        "safe_error_code": safe_error_code,
        "review_priority": 0,
        "recommended_review_action": "OBSERVE",
        "human_review_required": True,
        "provisional": True,
    }


def _execute_provider(
    *,
    experiment_id: str,
    lab_case: LabCase,
    case_index: int,
    config: ProviderConfig,
    repetition: int,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    start = time.perf_counter()
    raw_output: Any = None
    parsed_output: dict[str, Any] | None = None
    error: str | None = None
    status = AssessmentStatusV3.SEMANTIC_ASSESSMENT_UNAVAILABLE.value

    try:
        if not config.model or not config.base_url or not config.api_key:
            raise SemanticProviderError("semantic provider configuration is incomplete")

        import httpx

        try:
            response = httpx.post(
                f"{config.base_url.rstrip('/')}/chat/completions",
                headers={
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": config.model,
                    "messages": [
                        {"role": "system", "content": _system_prompt_v3()},
                        {
                            "role": "user",
                            "content": build_conversation_input(
                                title=lab_case.case_id,
                                text=lab_case.text,
                                context=lab_case.context,
                            ),
                        },
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2048,
                },
                timeout=SEMANTIC_HTTP_TIMEOUT_SECONDS,
            )
        except httpx.RequestError as exc:
            raise SemanticProviderError("semantic provider request failed") from exc
        if response.status_code < 200 or response.status_code >= 300:
            raw_output = response.text
            raise SemanticProviderError(
                f"semantic provider HTTP error: {response.status_code}"
            )
        envelope = response.json()
        raw_output = _extract_provider_content(envelope)
        draft = _validate_provider_draft(raw_output)
        result = finalize_draft_v3(
            conversation_id=case_index,
            draft=draft,
            source_parts=distinct_conversation_parts(
                title=lab_case.case_id, text=lab_case.text, context=lab_case.context
            ),
            semantic_engine=f"llm:{config.provider_name}",
            model_name=config.model,
        )
        parsed_output = result.model_dump(mode="json")
        status = result.assessment_status.value
        error = result.safe_error_code
    except (InvalidModelOutputError, json.JSONDecodeError, ValueError, TypeError) as exc:
        error = "INVALID_MODEL_OUTPUT"
        parsed_output = _failure_parsed_output(
            case_index=case_index, config=config, safe_error_code=error
        )
        parsed_output["assessment_status"] = AssessmentStatusV3.INVALID_MODEL_OUTPUT.value
        status = AssessmentStatusV3.INVALID_MODEL_OUTPUT.value
        raw_output = raw_output if raw_output is not None else str(exc)
    except SemanticProviderError as exc:
        error = "SEMANTIC_PROVIDER_UNAVAILABLE"
        parsed_output = _failure_parsed_output(
            case_index=case_index, config=config, safe_error_code=error
        )
        status = AssessmentStatusV3.SEMANTIC_ASSESSMENT_UNAVAILABLE.value
        raw_output = raw_output if raw_output is not None else str(exc)

    finished = datetime.now(timezone.utc)
    latency_ms = int((time.perf_counter() - start) * 1000)
    return {
        "experiment_id": experiment_id,
        "case_id": lab_case.case_id,
        "input_text": lab_case.text,
        "provider": config.provider,
        "model": config.model,
        "repetition": repetition,
        "prompt_version": PROMPT_VERSION,
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "latency_ms": latency_ms,
        "raw_output": raw_output,
        "parsed_output": parsed_output,
        "error": error,
        "fallback_used": False,
        "status": status,
    }


def _select_cases(*, source: str, case_ids: list[str] | None, input_text: str | None) -> list[LabCase]:
    if source == "free_text":
        text = (input_text or "").strip()
        if not text:
            raise ValueError("El texto libre es obligatorio")
        return [LabCase(case_id="FREE_TEXT", text=text)]
    if source != "corpus":
        raise ValueError("La fuente del laboratorio debe ser corpus o free_text")

    available = {item.case_id: item for item in load_lab_cases()}
    selected_ids = case_ids or list(available)
    missing = [case_id for case_id in selected_ids if case_id not in available]
    if missing:
        raise ValueError("Casos de laboratorio desconocidos: " + ", ".join(missing))
    return [available[case_id] for case_id in selected_ids]


def _stability(values: list[str | None]) -> str:
    if not values:
        return "sin datos"
    count = Counter(str(value) for value in values)
    value, occurrences = count.most_common(1)[0]
    return f"{value} ({occurrences}/{len(values)})"


def _write_report(
    *,
    path: Path,
    experiment_id: str,
    source: str,
    cases: list[LabCase],
    providers: list[str],
    repetitions: int,
    records: list[dict[str, Any]],
) -> None:
    created_at = datetime.now(timezone.utc).isoformat()
    lines = [
        f"# {experiment_id}",
        "",
        f"- Fecha UTC: `{created_at}`",
        f"- Fuente: `{source}`",
        f"- Corpus: `{LAB_CORPUS_PATH.relative_to(ROOT_DIR).as_posix()}`",
        f"- Casos: `{', '.join(item.case_id for item in cases)}`",
        f"- Providers: `{', '.join(providers)}`",
        f"- Repeticiones por provider: `{repetitions}`",
        f"- Total llamadas: `{len(records)}`",
        f"- Prompt version: `{PROMPT_VERSION}`",
        "- Fallback silencioso: `false`",
        "",
        "## Resumen",
        "",
    ]
    for provider in providers:
        provider_records = [item for item in records if item["provider"] == provider]
        lines.extend(
            [
                f"- {provider}: status dominante `{_stability([item['status'] for item in provider_records])}`, errores `{_stability([item['error'] for item in provider_records])}`",
            ]
        )
    lines.extend(["", "## Registros trazables", ""])
    for record in records:
        lines.extend(
            [
                f"### {record['case_id']} · {record['provider']} · repetición {record['repetition']}",
                "",
                "```json",
                json.dumps(record, ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_comparison_experiment(
    db: Session | None = None,
    *,
    source: str = "corpus",
    case_ids: list[str] | None = None,
    input_text: str | None = None,
    providers: list[str] | None = None,
    repetitions: int = 1,
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
) -> dict[str, Any]:
    del db
    if repetitions < 1:
        raise ValueError("Las repeticiones deben ser mayores a cero")
    selected_providers = providers or list(PROVIDERS)
    unknown = [provider for provider in selected_providers if provider not in PROVIDERS]
    if unknown:
        raise ValueError("Proveedores desconocidos: " + ", ".join(unknown))

    cases = _select_cases(source=source, case_ids=case_ids, input_text=input_text)
    path = _experiment_path(experiment_id)
    records: list[dict[str, Any]] = []
    for case_index, lab_case in enumerate(cases, start=1):
        for provider in selected_providers:
            config = _provider_config(provider)
            for repetition in range(1, repetitions + 1):
                records.append(
                    _execute_provider(
                        experiment_id=experiment_id,
                        lab_case=lab_case,
                        case_index=case_index,
                        config=config,
                        repetition=repetition,
                    )
                )

    _write_report(
        path=path,
        experiment_id=experiment_id,
        source=source,
        cases=cases,
        providers=selected_providers,
        repetitions=repetitions,
        records=records,
    )
    return {
        "experiment": path.name,
        "experiment_id": experiment_id,
        "report_path": str(path.relative_to(ROOT_DIR).as_posix()),
        "source": source,
        "corpus_path": str(LAB_CORPUS_PATH.relative_to(ROOT_DIR).as_posix()),
        "case_count": len(cases),
        "providers": selected_providers,
        "repetitions": repetitions,
        "total_calls": len(records),
        "records": records,
    }
