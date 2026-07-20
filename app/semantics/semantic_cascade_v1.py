from __future__ import annotations

import json
from collections.abc import Callable
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.schemas.assessment_v3 import (
    AffinityDomain, ApparentAffinity, ApparentIntention, AssessmentStatusV3,
    ConversationAssessmentV3Result, ReviewActionV3, RiskLevelV3,
)
from app.semantics.conversation_assessment_v3 import (
    InvalidModelOutputError, SEMANTIC_HTTP_TIMEOUT_SECONDS, SemanticProviderError,
    assess_conversation_v3, build_conversation_input, validate_evidence_fragments,
)

CASCADE_SCHEMA_VERSION = "radar-semantic-cascade/v1"
GEMMA_REVIEW_SCHEMA_VERSION = "radar-semantic-review/v1"


class GemmaSemanticReviewV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[GEMMA_REVIEW_SCHEMA_VERSION] = GEMMA_REVIEW_SCHEMA_VERSION
    agrees_with_agnes: bool
    disputed_fields: list[str] = Field(default_factory=list, max_length=20)
    proposed_affinity: ApparentAffinity | None = None
    proposed_affinity_domains: list[AffinityDomain] | None = None
    proposed_intention: ApparentIntention | None = None
    proposed_false_positive_risk: RiskLevelV3 | None = None
    proposed_uncertainty: RiskLevelV3 | None = None
    additional_evidence: list[str] = Field(default_factory=list, max_length=20)
    semantic_corrections: list[str] = Field(default_factory=list, max_length=20)
    ambiguities: list[str] = Field(default_factory=list, max_length=20)
    review_note: str = Field(min_length=1, max_length=3000)


class CascadeResolutionV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[CASCADE_SCHEMA_VERSION] = CASCADE_SCHEMA_VERSION
    agnes_assessment: ConversationAssessmentV3Result
    gemma_review_triggered: bool
    gemma_trigger_reasons: list[str] = Field(default_factory=list)
    gemma_review: GemmaSemanticReviewV1 | None = None
    resolved_affinity: ApparentAffinity | None = None
    resolved_affinity_domains: list[AffinityDomain] = Field(default_factory=list)
    resolved_intention: ApparentIntention | None = None
    resolved_false_positive_risk: RiskLevelV3 | None = None
    resolved_uncertainty: RiskLevelV3 | None = None
    accepted_additional_evidence: list[str] = Field(default_factory=list)
    disputed_fields: list[str] = Field(default_factory=list)
    deterministic_resolution: Literal[
        "AGNES_ACCEPTED", "GEMMA_NOT_REQUIRED", "GEMMA_CORRECTIONS_ACCEPTED",
        "HUMAN_REVIEW_REQUIRED", "GEMMA_UNAVAILABLE",
    ]
    human_review_required: bool
    resolution_note: str


GemmaReviewRunner = Callable[[str], GemmaSemanticReviewV1]


def gemma_trigger_reasons(assessment: ConversationAssessmentV3Result) -> list[str]:
    if assessment.assessment_status != AssessmentStatusV3.COMPLETED:
        return []
    reasons: list[str] = []
    if assessment.apparent_affinity == ApparentAffinity.POSSIBLE:
        reasons.append("AFFINITY_POSSIBLE")
    if assessment.uncertainty in {RiskLevelV3.MEDIUM, RiskLevelV3.HIGH}:
        reasons.append("UNCERTAINTY_ELEVATED")
    if assessment.false_positive_risk in {RiskLevelV3.MEDIUM, RiskLevelV3.HIGH}:
        reasons.append("FALSE_POSITIVE_RISK_ELEVATED")
    if assessment.recommended_review_action == ReviewActionV3.REVIEW:
        reasons.append("REVIEW_ACTION")
    if 40 <= assessment.review_priority <= 65:
        reasons.append("PRIORITY_NEAR_THRESHOLD")
    if assessment.contradictions:
        reasons.append("CONTRADICTIONS_PRESENT")
    if AffinityDomain.MEXICO_YUCATAN_CONNECTION in assessment.apparent_affinity_domains:
        reasons.append("YUCATAN_STRATEGIC_CASE")
    return reasons


def _gemma_review_prompt(agnes: ConversationAssessmentV3Result) -> str:
    domains = " | ".join(item.value for item in AffinityDomain)
    return (
        "Review the Agnes V3 assessment for Inlak'ech RADAR. Return one JSON object only, "
        "without markdown or thought tags. Review meaning, intention, contradictions, "
        "omitted domains, uncertainty, false-positive risk and literal evidence. Do not "
        "classify capacity, qualification, lead status, contact permission or workflow. "
        f"schema_version must be {GEMMA_REVIEW_SCHEMA_VERSION}. disputed_fields may only "
        "name apparent_affinity, apparent_affinity_domains, apparent_intention, "
        "false_positive_risk, uncertainty, evidence_fragments. Proposed fields must be null "
        "unless disputed. additional_evidence must be literal. Allowed domains: "
        f"{domains}.\nAGNES_ASSESSMENT:\n"
        + json.dumps(agnes.model_dump(mode="json"), ensure_ascii=False)
    )


def _parse_gemma_review(raw: str) -> GemmaSemanticReviewV1:
    payload = raw.strip()
    try:
        return GemmaSemanticReviewV1.model_validate_json(payload)
    except ValidationError as direct_error:
        decoder = json.JSONDecoder()
        for index, character in enumerate(payload):
            if character != "{":
                continue
            try:
                candidate, _ = decoder.raw_decode(payload[index:])
            except json.JSONDecodeError:
                continue
            if isinstance(candidate, dict):
                return GemmaSemanticReviewV1.model_validate(candidate)
        raise direct_error


def build_gemma_review_runner(*, model_name: str, base_url: str, api_key: str) -> GemmaReviewRunner:
    import httpx

    def run(text: str) -> GemmaSemanticReviewV1:
        try:
            response = httpx.post(
                f"{base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model_name,
                    "messages": [{"role": "system", "content": text}],
                    "temperature": 0.1,
                    "max_tokens": 1536,
                },
                timeout=SEMANTIC_HTTP_TIMEOUT_SECONDS,
            )
        except httpx.RequestError as exc:
            raise SemanticProviderError("Gemma semantic review request failed") from exc
        if not 200 <= response.status_code < 300:
            raise SemanticProviderError(f"Gemma semantic review HTTP error: {response.status_code}")
        try:
            raw = response.json()["choices"][0]["message"]["content"]
            if not isinstance(raw, str):
                raise TypeError("Gemma review content must be text")
            return _parse_gemma_review(raw)
        except (KeyError, IndexError, TypeError, ValueError, ValidationError) as exc:
            raise InvalidModelOutputError("invalid Gemma semantic review") from exc

    return run


def _base_resolution(agnes: ConversationAssessmentV3Result, **updates) -> CascadeResolutionV1:
    payload = dict(
        agnes_assessment=agnes,
        gemma_review_triggered=False,
        resolved_affinity=agnes.apparent_affinity,
        resolved_affinity_domains=agnes.apparent_affinity_domains,
        resolved_intention=agnes.apparent_intention,
        resolved_false_positive_risk=agnes.false_positive_risk,
        resolved_uncertainty=agnes.uncertainty,
        deterministic_resolution="GEMMA_NOT_REQUIRED",
        human_review_required=agnes.human_review_required,
        resolution_note="Agnes assessment did not meet any Gemma review trigger.",
    )
    payload.update(updates)
    return CascadeResolutionV1(**payload)


def _resolve_review(
    *, agnes: ConversationAssessmentV3Result, review: GemmaSemanticReviewV1,
    title: str | None, text: str, context: str | None,
) -> CascadeResolutionV1:
    source_parts = [part for part in (title, text, context) if part]
    valid_additional, _ = validate_evidence_fragments(source_parts, review.additional_evidence)
    disputed = sorted(set(review.disputed_fields))
    hard_conflict = (
        "apparent_affinity" in disputed and review.proposed_affinity is not None
        and review.proposed_affinity != agnes.apparent_affinity
    ) or (
        "apparent_intention" in disputed and review.proposed_intention is not None
        and review.proposed_intention != agnes.apparent_intention
    )
    if hard_conflict:
        return _base_resolution(
            agnes, gemma_review_triggered=True,
            gemma_trigger_reasons=gemma_trigger_reasons(agnes), gemma_review=review,
            accepted_additional_evidence=valid_additional, disputed_fields=disputed,
            deterministic_resolution="HUMAN_REVIEW_REQUIRED", human_review_required=True,
            resolution_note="Gemma disputes a core semantic field; no automatic overwrite is allowed.",
        )
    domains = list(agnes.apparent_affinity_domains)
    fp_risk = agnes.false_positive_risk
    uncertainty = agnes.uncertainty
    if "apparent_affinity_domains" in disputed and review.proposed_affinity_domains is not None:
        domains = sorted(set(domains) | set(review.proposed_affinity_domains), key=lambda item: item.value)
    if "false_positive_risk" in disputed and review.proposed_false_positive_risk is not None:
        fp_risk = review.proposed_false_positive_risk
    if "uncertainty" in disputed and review.proposed_uncertainty is not None:
        uncertainty = review.proposed_uncertainty
    resolution = "AGNES_ACCEPTED" if review.agrees_with_agnes and not disputed else "GEMMA_CORRECTIONS_ACCEPTED"
    return _base_resolution(
        agnes, gemma_review_triggered=True,
        gemma_trigger_reasons=gemma_trigger_reasons(agnes), gemma_review=review,
        resolved_affinity_domains=domains, resolved_false_positive_risk=fp_risk,
        resolved_uncertainty=uncertainty, accepted_additional_evidence=valid_additional,
        disputed_fields=disputed, deterministic_resolution=resolution,
        human_review_required=agnes.human_review_required or bool(disputed),
        resolution_note=("Gemma agrees with Agnes; Agnes remains authoritative."
            if resolution == "AGNES_ACCEPTED"
            else "Only non-core, explicitly disputed corrections were accepted deterministically."),
    )


def assess_conversation_cascade_v1(
    *, conversation_id: int, title: str | None, text: str, context: str | None,
    agnes_enabled: bool, agnes_model_name: str | None, agnes_base_url: str | None,
    agnes_api_key: str | None, gemma_enabled: bool, gemma_model_name: str | None,
    gemma_base_url: str | None, gemma_api_key: str | None,
    agnes_runner=None, gemma_runner: GemmaReviewRunner | None = None,
) -> CascadeResolutionV1:
    agnes = assess_conversation_v3(
        conversation_id=conversation_id, title=title, text=text, context=context,
        enabled=agnes_enabled, model_name=agnes_model_name, provider_name="agnes",
        base_url=agnes_base_url, api_key=agnes_api_key, runner=agnes_runner,
    )
    reasons = gemma_trigger_reasons(agnes)
    if not reasons:
        return _base_resolution(agnes)
    if not gemma_enabled or not gemma_model_name or not gemma_base_url or not gemma_api_key:
        return _base_resolution(
            agnes, gemma_review_triggered=True, gemma_trigger_reasons=reasons,
            deterministic_resolution="GEMMA_UNAVAILABLE", human_review_required=True,
            resolution_note="Gemma review was required but its configuration is unavailable.",
        )
    active_runner = gemma_runner or build_gemma_review_runner(
        model_name=gemma_model_name, base_url=gemma_base_url, api_key=gemma_api_key,
    )
    try:
        review = active_runner(_gemma_review_prompt(agnes) + "\nCONVERSATION:\n"
            + build_conversation_input(title=title, text=text, context=context))
    except (SemanticProviderError, InvalidModelOutputError, ValidationError):
        return _base_resolution(
            agnes, gemma_review_triggered=True, gemma_trigger_reasons=reasons,
            deterministic_resolution="GEMMA_UNAVAILABLE", human_review_required=True,
            resolution_note="Gemma review failed safely; Agnes was preserved without overwrite.",
        )
    return _resolve_review(agnes=agnes, review=review, title=title, text=text, context=context)
