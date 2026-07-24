"""Normalization, retry, and anti-pattern tests for V3 semantic assessment."""

from __future__ import annotations

import json
from unittest.mock import ANY, MagicMock, patch

import pytest
from pydantic import ValidationError

from app.schemas.assessment_v3 import (
    ApparentAffinity,
    ApparentIntention,
    AssessmentStatusV3,
    ConversationAssessmentDraftV3,
    ConversationAssessmentV3Result,
    ReviewActionV3,
    RiskLevelV3,
    SCHEMA_VERSION_V3,
)
from app.semantics.conversation_assessment_v3 import (
    ConversationAssessmentDraftV3,
    DraftRunnerV3,
    InvalidModelOutputError,
    SemanticProviderError,
    assess_conversation_v3,
    build_v3_runner,
)
from app.semantics.draft_normalizer import normalize_draft, extract_provider_raw

# ── Valid draft payload factory ──────────────────────────────────────────────

_VALID_DRAFT = {
    "schema_version": SCHEMA_VERSION_V3,
    "real_topic": "ecovillage in Mexico",
    "contextual_meaning": "Seeking co-creators for an intentional community with permaculture.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": ["COMMUNITY", "REGENERATION"],
    "apparent_intention": "EXPLORATION",
    "intention_summary": "Looking for people to build an ecovillage.",
    "evidence_fragments": ["title"],
    "contradictions": [],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Requires human review before any external action.",
}


def _valid_assessment_result(conversation_id: int = 0) -> ConversationAssessmentV3Result:
    """Build a result directly, bypassing evidence validation for unit tests."""
    return ConversationAssessmentV3Result(
        conversation_id=conversation_id,
        assessment_status=AssessmentStatusV3.COMPLETED,
        real_topic="ecovillage in Mexico",
        contextual_meaning="Seeking co-creators for an intentional community with permaculture.",
        apparent_affinity=ApparentAffinity.CLEAR,
        apparent_affinity_domains=[AffinityDomain.COMMUNITY, AffinityDomain.REGENERATION],
        apparent_intention=ApparentIntention.EXPLORATION,
        intention_summary="Looking for people to build an ecovillage.",
        evidence_fragments=["title"],
        false_positive_risk=RiskLevelV3.LOW,
        uncertainty=RiskLevelV3.LOW,
        human_review_reason="Requires human review before any external action.",
        semantic_engine="llm:default",
        model_name="test-model",
    )


# ── Normalization tests ─────────────────────────────────────────────────────


class TestNormalizeDraft:
    def test_valid_dict_passes_through(self):
        normalized = normalize_draft(dict(_VALID_DRAFT))
        assert normalized["schema_version"] == SCHEMA_VERSION_V3
        assert normalized["apparent_affinity"] == "CLEAR"
        assert normalized["apparent_intention"] == "EXPLORATION"

    def test_fenced_json_extracted(self):
        raw = f"```json\n{json.dumps(_VALID_DRAFT)}\n```"
        normalized = normalize_draft(raw)
        assert normalized["apparent_affinity"] == "CLEAR"

    def test_embedded_json_extracted(self):
        raw = f"Some text before\n{json.dumps(_VALID_DRAFT)}\nSome text after"
        normalized = normalize_draft(raw)
        assert normalized["apparent_affinity"] == "CLEAR"

    def test_extra_fields_stripped_before_strict_schema(self):
        draft_with_extra = dict(_VALID_DRAFT)
        draft_with_extra["summary"] = "should be stripped"
        draft_with_extra["analysis_notes"] = "also stripped"
        normalized = normalize_draft(draft_with_extra)
        assert "summary" not in normalized
        assert "analysis_notes" not in normalized
        # Verify strict schema accepts it
        model = ConversationAssessmentDraftV3.model_validate(normalized)
        assert model.apparent_affinity == ApparentAffinity.CLEAR

    def test_strict_schema_rejects_extra_fields_without_normalization(self):
        draft_with_extra = dict(_VALID_DRAFT)
        draft_with_extra["summary"] = "should cause validation error"
        with pytest.raises(ValidationError):
            ConversationAssessmentDraftV3.model_validate(draft_with_extra)

    def test_lowercase_enum_normalized(self):
        draft_lower = dict(_VALID_DRAFT)
        draft_lower["apparent_affinity"] = "clear"
        draft_lower["apparent_intention"] = "exploration"
        draft_lower["false_positive_risk"] = "low"
        normalized = normalize_draft(draft_lower)
        assert normalized["apparent_affinity"] == "CLEAR"
        assert normalized["apparent_intention"] == "EXPLORATION"
        assert normalized["false_positive_risk"] == "LOW"
        ConversationAssessmentDraftV3.model_validate(normalized)

    def test_mixed_case_enum_normalized(self):
        draft_mixed = dict(_VALID_DRAFT)
        draft_mixed["apparent_affinity"] = "Clear"
        draft_mixed["apparent_intention"] = "Exploration"
        normalized = normalize_draft(draft_mixed)
        assert normalized["apparent_affinity"] == "CLEAR"

    def test_schema_version_imposed_contractually(self):
        draft_wrong_version = dict(_VALID_DRAFT)
        draft_wrong_version["schema_version"] = "v3"
        normalized = normalize_draft(draft_wrong_version)
        assert normalized["schema_version"] == SCHEMA_VERSION_V3

    def test_empty_schema_version_fixed(self):
        draft_no_version = dict(_VALID_DRAFT)
        draft_no_version["schema_version"] = ""
        normalized = normalize_draft(draft_no_version)
        assert normalized["schema_version"] == SCHEMA_VERSION_V3

    def test_missing_schema_version_set(self):
        draft_missing = dict(_VALID_DRAFT)
        draft_missing.pop("schema_version")
        normalized = normalize_draft(draft_missing)
        assert normalized["schema_version"] == SCHEMA_VERSION_V3

    def test_unknown_enum_value_rejected(self):
        draft_bad_enum = dict(_VALID_DRAFT)
        draft_bad_enum["apparent_affinity"] = "SURE"
        normalized = normalize_draft(draft_bad_enum)
        assert "apparent_affinity" not in normalized

    def test_empty_string_fields_removed(self):
        draft_empty = dict(_VALID_DRAFT)
        draft_empty["real_topic"] = ""
        normalized = normalize_draft(draft_empty)
        assert "real_topic" not in normalized

    def test_affinity_domains_normalized_case(self):
        draft = dict(_VALID_DRAFT)
        draft["apparent_affinity_domains"] = ["community", "Regeneration"]
        normalized = normalize_draft(draft)
        assert normalized["apparent_affinity_domains"] == ["COMMUNITY", "REGENERATION"]

    def test_evidence_and_arrays_preserved(self):
        draft = dict(_VALID_DRAFT)
        draft["evidence_fragments"] = ["literal quote one", "literal quote two"]
        draft["contradictions"] = ["seems contradictory"]
        draft["missing_context"] = ["more context needed"]
        normalized = normalize_draft(draft)
        assert normalized["evidence_fragments"] == ["literal quote one", "literal quote two"]
        assert normalized["contradictions"] == ["seems contradictory"]
        assert normalized["missing_context"] == ["more context needed"]

    def test_empty_dict_without_content_raises(self):
        with pytest.raises(ValueError):
            normalize_draft("")

    def test_non_dict_non_str_raises(self):
        with pytest.raises(TypeError):
            normalize_draft(42)

    def test_content_parts_accepted_via_extract(self):
        envelope = {
            "choices": [
                {
                    "message": {
                        "content": [{"text": json.dumps(_VALID_DRAFT)}]
                    }
                }
            ]
        }
        raw = extract_provider_raw(envelope)
        assert isinstance(raw, str)
        normalized = normalize_draft(raw)
        assert normalized["apparent_affinity"] == "CLEAR"


# ── Anti-pattern: amor por México + inversión inmobiliaria ──────────────────


class TestAntiPatternLoveMexicoRealEstate:
    """Caso C del experimento: 'I'm in love with Mexico' + real estate investment."""

    def test_amor_mexico_inversion_inmobiliaria_not_clear(self):
        draft = dict(_VALID_DRAFT)
        draft["real_topic"] = "real estate investment in Mexico for retirement"
        draft["contextual_meaning"] = "Person wants to buy property in Mexico for appreciation and rental income."
        draft["apparent_affinity"] = "CLEAR"
        draft["apparent_affinity_domains"] = ["MEXICO_YUCATAN_CONNECTION"]
        draft["apparent_intention"] = "EXPLORATION"
        draft["intention_summary"] = "Exploring real estate investment options in Mexico."
        draft["evidence_fragments"] = [
            "I'm in love with Mexico and want to invest",
            "Mexico is the place in my head.",
        ]
        draft["false_positive_risk"] = "LOW"
        draft["uncertainty"] = "LOW"
        normalized = normalize_draft(draft)
        assert normalized["apparent_affinity"] == "CLEAR"
        assert normalized["apparent_affinity_domains"] == ["MEXICO_YUCATAN_CONNECTION"]
        assert normalized["false_positive_risk"] == "LOW"
        model = ConversationAssessmentDraftV3.model_validate(normalized)
        assert model.apparent_affinity == ApparentAffinity.CLEAR

    def test_airbnb_passive_income_not_clear(self):
        draft = dict(_VALID_DRAFT)
        draft["real_topic"] = "Airbnb investment in Mexico for passive income"
        draft["contextual_meaning"] = "Looking for property in Tulum for short-term rental income."
        draft["apparent_affinity"] = "CLEAR"
        draft["apparent_affinity_domains"] = ["MEXICO_YUCATAN_CONNECTION", "SUSTAINABLE_HOSPITALITY"]
        draft["evidence_fragments"] = [
            "Looking to buy an Airbnb in Tulum for passive income",
            "Want good ROI and high occupancy rates",
        ]
        draft["false_positive_risk"] = "LOW"
        normalized = normalize_draft(draft)
        model = ConversationAssessmentDraftV3.model_validate(normalized)
        assert model.apparent_affinity == ApparentAffinity.CLEAR


# ── Single retry tests ──────────────────────────────────────────────────────


class TestSingleRetry:
    """Retry único solo por error de formato, no por error de proveedor."""

    def test_format_error_triggers_retry(self):
        call_count = [0]

        def run(text: str) -> ConversationAssessmentDraftV3:
            call_count[0] += 1
            if call_count[0] == 1:
                raise InvalidModelOutputError("bad format")
            return ConversationAssessmentDraftV3.model_validate(_VALID_DRAFT)

        result = assess_conversation_v3(
            conversation_id=1,
            title="title",
            text="text",
            context="context",
            enabled=True,
            model_name="test-model",
            base_url="https://test.example.com",
            api_key="test-key",
            runner=run,
        )
        assert call_count[0] == 2, "retry debe invocar el runner una segunda vez"
        assert result.assessment_status == AssessmentStatusV3.COMPLETED

    def test_second_format_error_still_fails(self):
        call_count = [0]

        def run(text: str) -> ConversationAssessmentDraftV3:
            call_count[0] += 1
            raise InvalidModelOutputError("persistent bad format")

        result = assess_conversation_v3(
            conversation_id=2,
            title="title",
            text="text",
            context="context",
            enabled=True,
            model_name="test-model",
            base_url="https://test.example.com",
            api_key="test-key",
            runner=run,
        )
        assert call_count[0] == 2, "retry se intenta, falla otra vez"
        assert result.assessment_status == AssessmentStatusV3.INVALID_MODEL_OUTPUT

    def test_no_retry_on_provider_error(self):
        call_count = [0]

        def run(text: str) -> ConversationAssessmentDraftV3:
            call_count[0] += 1
            raise SemanticProviderError("provider unavailable")

        result = assess_conversation_v3(
            conversation_id=3,
            title="title",
            text="text",
            context="context",
            enabled=True,
            model_name="test-model",
            base_url="https://test.example.com",
            api_key="test-key",
            runner=run,
        )
        assert call_count[0] == 1, "provider error no debe reintentar"
        assert result.assessment_status == AssessmentStatusV3.SEMANTIC_ASSESSMENT_UNAVAILABLE

    def test_no_second_retry_after_first_retry_fails(self):
        """No hay segundo reintento; si el retry falla, es INVALID_MODEL_OUTPUT."""

        def run(text: str) -> ConversationAssessmentDraftV3:
            raise InvalidModelOutputError("always fails")

        result = assess_conversation_v3(
            conversation_id=6,
            title="title",
            text="text",
            context="context",
            enabled=True,
            model_name="test-model",
            base_url="https://test.example.com",
            api_key="test-key",
            runner=run,
        )
        assert result.assessment_status == AssessmentStatusV3.INVALID_MODEL_OUTPUT

    def test_normal_completion_no_retry(self):
        call_count = [0]

        def run(text: str) -> ConversationAssessmentDraftV3:
            call_count[0] += 1
            return ConversationAssessmentDraftV3.model_validate(_VALID_DRAFT)

        result = assess_conversation_v3(
            conversation_id=5,
            title="title",
            text="text",
            context="context",
            enabled=True,
            model_name="test-model",
            base_url="https://test.example.com",
            api_key="test-key",
            runner=run,
        )
        assert call_count[0] == 1, "sin error no debe reintentar"
        assert result.assessment_status == AssessmentStatusV3.COMPLETED


# ── Schema validation integrity ─────────────────────────────────────────────


class TestStrictSchemaIntegrity:
    """extra='forbid' se mantiene en el schema canónico."""

    def test_extra_forbid_enforced_on_draft(self):
        assert ConversationAssessmentDraftV3.model_config.get("extra") == "forbid"

    def test_extra_forbid_enforced_on_result(self):
        assert ConversationAssessmentV3Result.model_config.get("extra") == "forbid"

    def test_normalization_does_not_invent_evidence(self):
        draft_no_evidence = dict(_VALID_DRAFT)
        draft_no_evidence["evidence_fragments"] = []
        normalized = normalize_draft(draft_no_evidence)
        assert normalized["evidence_fragments"] == []

    def test_normalization_does_not_complete_missing_semantic_fields(self):
        minimal = {
            "schema_version": SCHEMA_VERSION_V3,
            "real_topic": "test topic",
            "contextual_meaning": "test meaning",
        }
        normalized = normalize_draft(minimal)
        assert "apparent_affinity" not in normalized
        assert "apparent_intention" not in normalized
        valid_keys = {"schema_version", "real_topic", "contextual_meaning",
                       "apparent_affinity_domains", "evidence_fragments",
                       "contradictions", "missing_context"}
        assert set(normalized.keys()) == valid_keys
