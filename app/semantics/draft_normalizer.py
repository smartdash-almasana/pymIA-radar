from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import Any

from app.schemas.assessment_v3 import (
    AffinityDomain,
    ApparentAffinity,
    ApparentIntention,
    ReviewActionV3,
    RiskLevelV3,
    SCHEMA_VERSION_V3,
)

_KNOWN_FIELDS = frozenset({
    "schema_version",
    "real_topic",
    "contextual_meaning",
    "apparent_affinity",
    "apparent_affinity_domains",
    "apparent_intention",
    "intention_summary",
    "evidence_fragments",
    "contradictions",
    "missing_context",
    "false_positive_risk",
    "uncertainty",
    "human_review_reason",
    "review_priority",
    "recommended_review_action",
})


def _coerce_str(value: object) -> str | None:
    if isinstance(value, str):
        return value
    if value is not None:
        return str(value)
    return None


def _coerce_str_list(value: object) -> list[str] | None:
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            s = _coerce_str(item)
            if s is not None:
                result.append(s)
        return result if result else None
    return None


def _normalize_enum(
    value: object, enum_cls: type, default: object | None = None
) -> object | None:
    raw = _coerce_str(value)
    if raw is None:
        return default
    upper = raw.strip().upper()
    for member in enum_cls:
        if member.value.upper() == upper:
            return member
    return default


def _normalize_enum_list(
    values: object, enum_cls: type,
) -> list[object] | None:
    if not isinstance(values, list):
        return None
    result: list[object] = []
    for item in values:
        s = _coerce_str(item)
        if s is None:
            continue
        upper = s.strip().upper()
        for member in enum_cls:
            if member.value.upper() == upper:
                result.append(member)
                break
    return result if result else None


def _strip_unknown_fields(raw: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in raw.items() if k in _KNOWN_FIELDS}


def normalize_draft(raw: object) -> dict[str, Any]:
    if isinstance(raw, str):
        parsed = _extract_json(raw)
        if parsed is None:
            raise ValueError("response content does not contain valid JSON")
    elif isinstance(raw, dict):
        parsed = raw
    else:
        raise TypeError(f"unsupported raw type: {type(raw).__name__}")

    clean = _strip_unknown_fields(parsed)

    clean["schema_version"] = SCHEMA_VERSION_V3

    for field in ("real_topic", "contextual_meaning", "intention_summary", "human_review_reason"):
        val = _coerce_str(clean.get(field))
        if val and val.strip():
            clean[field] = val.strip()
        else:
            clean.pop(field, None)

    affinity = _normalize_enum(clean.get("apparent_affinity"), ApparentAffinity)
    if affinity is not None:
        clean["apparent_affinity"] = affinity.value if isinstance(affinity, ApparentAffinity) else affinity
    else:
        clean.pop("apparent_affinity", None)

    intention = _normalize_enum(clean.get("apparent_intention"), ApparentIntention)
    if intention is not None:
        clean["apparent_intention"] = intention.value if isinstance(intention, ApparentIntention) else intention
    else:
        clean.pop("apparent_intention", None)

    fp_risk = _normalize_enum(clean.get("false_positive_risk"), RiskLevelV3)
    if fp_risk is not None:
        clean["false_positive_risk"] = fp_risk.value if isinstance(fp_risk, RiskLevelV3) else fp_risk
    else:
        clean.pop("false_positive_risk", None)

    uncertainty = _normalize_enum(clean.get("uncertainty"), RiskLevelV3)
    if uncertainty is not None:
        clean["uncertainty"] = uncertainty.value if isinstance(uncertainty, RiskLevelV3) else uncertainty
    else:
        clean.pop("uncertainty", None)

    action = _normalize_enum(clean.get("recommended_review_action"), ReviewActionV3)
    if action is not None:
        clean["recommended_review_action"] = action.value if isinstance(action, ReviewActionV3) else action
    else:
        clean.pop("recommended_review_action", None)

    domains = _normalize_enum_list(clean.get("apparent_affinity_domains", []), AffinityDomain)
    if domains is not None:
        clean["apparent_affinity_domains"] = [d.value for d in domains]
    else:
        clean["apparent_affinity_domains"] = []

    for field in ("evidence_fragments", "contradictions", "missing_context"):
        vals = _coerce_str_list(clean.get(field))
        if vals is not None:
            clean[field] = vals
        else:
            clean[field] = []

    return clean


class _JSONExtractError(ValueError):
    pass


def _extract_json(raw: str) -> dict[str, Any] | None:
    payload = raw.strip()
    if not payload:
        return None

    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", payload, flags=re.DOTALL)
    if fenced:
        payload = fenced.group(1).strip()

    try:
        decoded = json.loads(payload)
        if isinstance(decoded, dict):
            return decoded
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    for index, character in enumerate(payload):
        if character != "{":
            continue
        try:
            candidate, _ = decoder.raw_decode(payload[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            return candidate
    return None


def extract_provider_raw(envelope: object) -> object:
    if not isinstance(envelope, dict):
        raise TypeError("response envelope must be an object")
    choices = envelope.get("choices")
    if not isinstance(choices, list) or not choices:
        raise KeyError("response choices are missing")
    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        raise TypeError("response choice must be an object")
    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise KeyError("response message is missing")
    content = message.get("content")
    if isinstance(content, list):
        text_parts = [
            part.get("text")
            for part in content
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        ]
        if not text_parts:
            raise ValueError("response content parts contain no text")
        return "".join(text_parts)
    if isinstance(content, (str, dict)):
        return content
    raise TypeError("response content has unsupported shape")
