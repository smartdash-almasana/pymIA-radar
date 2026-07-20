from app.schemas.assessment_v3 import (
    AffinityDomain, ApparentAffinity, ApparentIntention, AssessmentStatusV3,
    ConversationAssessmentDraftV3, ConversationAssessmentV3Result, RiskLevelV3,
)
from app.semantics.semantic_cascade_v1 import (
    GEMMA_REVIEW_SCHEMA_VERSION, GemmaSemanticReviewV1,
    assess_conversation_cascade_v1,
)


def agnes_draft(*, affinity="NONE", intention="NONE", domains=None, contradictions=None):
    return ConversationAssessmentDraftV3(
        real_topic="topic",
        contextual_meaning="meaning",
        apparent_affinity=affinity,
        apparent_affinity_domains=domains or [],
        apparent_intention=intention,
        intention_summary="summary",
        evidence_fragments=["Texto literal"],
        contradictions=contradictions or [],
        missing_context=[],
        false_positive_risk="LOW",
        uncertainty="LOW",
        human_review_reason="review",
    )


def run_case(draft, gemma_runner=None):
    return assess_conversation_cascade_v1(
        conversation_id=1,
        title=None,
        text="Texto literal",
        context=None,
        agnes_enabled=True,
        agnes_model_name="agnes-test",
        agnes_base_url="https://agnes.example/v1",
        agnes_api_key="secret",
        gemma_enabled=True,
        gemma_model_name="gemma-test",
        gemma_base_url="https://gemma.example/v1",
        gemma_api_key="secret",
        agnes_runner=lambda _: draft,
        gemma_runner=gemma_runner,
    )


def test_gemma_is_not_called_for_clear_discard():
    called = False
    def gemma(_):
        nonlocal called
        called = True
        raise AssertionError
    result = run_case(agnes_draft(), gemma)
    assert result.deterministic_resolution == "GEMMA_NOT_REQUIRED"
    assert result.gemma_review_triggered is False
    assert called is False


def test_gemma_agreement_preserves_agnes():
    draft = agnes_draft(
        affinity="POSSIBLE", intention="THEMATIC_SYMPATHY",
        domains=[AffinityDomain.REGENERATION],
    )
    review = GemmaSemanticReviewV1(
        schema_version=GEMMA_REVIEW_SCHEMA_VERSION,
        agrees_with_agnes=True,
        disputed_fields=[],
        review_note="Agnes is semantically sound.",
    )
    result = run_case(draft, lambda _: review)
    assert result.deterministic_resolution == "AGNES_ACCEPTED"
    assert result.resolved_affinity == ApparentAffinity.POSSIBLE
    assert result.gemma_review_triggered is True


def test_core_conflict_requires_human_review_without_overwrite():
    draft = agnes_draft(
        affinity="POSSIBLE", intention="THEMATIC_SYMPATHY",
        domains=[AffinityDomain.REGENERATION],
    )
    review = GemmaSemanticReviewV1(
        agrees_with_agnes=False,
        disputed_fields=["apparent_intention"],
        proposed_intention=ApparentIntention.ACTION_ORIENTED,
        review_note="Intent may be stronger.",
    )
    result = run_case(draft, lambda _: review)
    assert result.deterministic_resolution == "HUMAN_REVIEW_REQUIRED"
    assert result.resolved_intention == ApparentIntention.THEMATIC_SYMPATHY
    assert result.human_review_required is True


def test_non_core_domain_addition_is_traceable():
    draft = agnes_draft(
        affinity="POSSIBLE", intention="THEMATIC_SYMPATHY",
        domains=[AffinityDomain.REGENERATION],
    )
    review = GemmaSemanticReviewV1(
        agrees_with_agnes=False,
        disputed_fields=["apparent_affinity_domains"],
        proposed_affinity_domains=[
            AffinityDomain.REGENERATION,
            AffinityDomain.MEXICO_YUCATAN_CONNECTION,
        ],
        additional_evidence=["Texto literal", "invented"],
        review_note="Yucatan domain was omitted.",
    )
    result = run_case(draft, lambda _: review)
    assert result.deterministic_resolution == "GEMMA_CORRECTIONS_ACCEPTED"
    assert AffinityDomain.MEXICO_YUCATAN_CONNECTION in result.resolved_affinity_domains
    assert result.accepted_additional_evidence == ["Texto literal"]


def test_missing_gemma_configuration_fails_safe():
    result = assess_conversation_cascade_v1(
        conversation_id=1,
        title=None,
        text="Texto literal",
        context=None,
        agnes_enabled=True,
        agnes_model_name="agnes-test",
        agnes_base_url="https://agnes.example/v1",
        agnes_api_key="secret",
        gemma_enabled=False,
        gemma_model_name=None,
        gemma_base_url=None,
        gemma_api_key=None,
        agnes_runner=lambda _: agnes_draft(
            affinity="POSSIBLE", intention="THEMATIC_SYMPATHY"
        ),
    )
    assert result.deterministic_resolution == "GEMMA_UNAVAILABLE"
    assert result.human_review_required is True
    assert result.provider_failover is False
    assert result.primary_provider_used == "agnes"


# ── Failover tests ──────────────────────────────────────────────────────


from app.semantics.conversation_assessment_v3 import SemanticProviderError


def _failed_agnes_runner(_text):
    """Simulates Agnes timeout by raising SemanticProviderError."""
    raise SemanticProviderError("simulated Agnes timeout")


def _failed_gemma_primary_runner(_text):
    """Simulates Gemma primary failure by raising SemanticProviderError."""
    raise SemanticProviderError("simulated Gemma failure")


def _gemma_primary_draft():
    return ConversationAssessmentDraftV3(
        real_topic="topic from Gemma",
        contextual_meaning="meaning from Gemma",
        apparent_affinity="POSSIBLE",
        apparent_affinity_domains=[],
        apparent_intention="EXPLORATION",
        intention_summary="summary from Gemma",
        evidence_fragments=["Texto literal"],
        contradictions=[],
        missing_context=[],
        false_positive_risk="LOW",
        uncertainty="LOW",
        human_review_reason="review from Gemma",
    )


def test_agnes_completes_no_failover():
    """Test 1: Agnes completa y no hay failover."""
    result = run_case(agnes_draft())
    assert result.primary_provider_attempted == "agnes"
    assert result.primary_provider_used == "agnes"
    assert result.provider_failover is False
    assert result.provider_failure_code is None
    assert result.deterministic_resolution == "GEMMA_NOT_REQUIRED"


def test_agnes_timeout_gemma_completes():
    """Test 2: Agnes timeout y Gemma completa como primaria."""
    result = assess_conversation_cascade_v1(
        conversation_id=1,
        title=None,
        text="Texto literal",
        context=None,
        agnes_enabled=True,
        agnes_model_name="agnes-test",
        agnes_base_url="https://agnes.example/v1",
        agnes_api_key="secret",
        gemma_enabled=True,
        gemma_model_name="gemma-test",
        gemma_base_url="https://gemma.example/v1",
        gemma_api_key="secret",
        agnes_runner=_failed_agnes_runner,
        gemma_primary_runner=lambda _: _gemma_primary_draft(),
    )
    assert result.provider_failover is True
    assert result.primary_provider_attempted == "agnes"
    assert result.primary_provider_used == "gemma"
    assert result.provider_failure_code == "SEMANTIC_PROVIDER_UNAVAILABLE"
    assert result.deterministic_resolution == "EXPLICIT_PROVIDER_FAILOVER"
    assert result.human_review_required is True
    # Primary assessment should contain Gemma's output
    assert result.agnes_assessment.assessment_status == "COMPLETED"
    assert result.agnes_assessment.semantic_engine == "llm:gemma"


def test_agnes_fails_gemma_fails_no_persist():
    """Test 3: Agnes falla y Gemma falla — no se persiste evaluación completada."""
    result = assess_conversation_cascade_v1(
        conversation_id=1,
        title=None,
        text="Texto literal",
        context=None,
        agnes_enabled=True,
        agnes_model_name="agnes-test",
        agnes_base_url="https://agnes.example/v1",
        agnes_api_key="secret",
        gemma_enabled=True,
        gemma_model_name="gemma-test",
        gemma_base_url="https://gemma.example/v1",
        gemma_api_key="secret",
        agnes_runner=_failed_agnes_runner,
        gemma_primary_runner=_failed_gemma_primary_runner,
    )
    assert result.provider_failover is True
    assert result.primary_provider_used is None
    assert result.deterministic_resolution == "ALL_PROVIDERS_UNAVAILABLE"
    assert result.agnes_assessment.assessment_status != "COMPLETED"


def test_gemma_not_called_twice_on_failover():
    """Test 4: No se llama dos veces a Gemma en failover."""
    call_count = 0
    def track_primary(_):
        nonlocal call_count
        call_count += 1
        return _gemma_primary_draft()

    result = assess_conversation_cascade_v1(
        conversation_id=1,
        title=None,
        text="Texto literal",
        context=None,
        agnes_enabled=True,
        agnes_model_name="agnes-test",
        agnes_base_url="https://agnes.example/v1",
        agnes_api_key="secret",
        gemma_enabled=True,
        gemma_model_name="gemma-test",
        gemma_base_url="https://gemma.example/v1",
        gemma_api_key="secret",
        agnes_runner=_failed_agnes_runner,
        gemma_primary_runner=track_primary,
    )
    assert call_count == 1
    assert result.provider_failover is True


def test_failover_forces_human_review():
    """Test 5: El failover obliga revisión humana."""
    result = assess_conversation_cascade_v1(
        conversation_id=1,
        title=None,
        text="Texto literal",
        context=None,
        agnes_enabled=True,
        agnes_model_name="agnes-test",
        agnes_base_url="https://agnes.example/v1",
        agnes_api_key="secret",
        gemma_enabled=True,
        gemma_model_name="gemma-test",
        gemma_base_url="https://gemma.example/v1",
        gemma_api_key="secret",
        agnes_runner=_failed_agnes_runner,
        gemma_primary_runner=lambda _: _gemma_primary_draft(),
    )
    assert result.human_review_required is True
    assert result.provider_failover is True


def test_failover_trace_persisted():
    """Test 6: La traza persistida coincide con la resolución."""
    result = assess_conversation_cascade_v1(
        conversation_id=1,
        title=None,
        text="Texto literal",
        context=None,
        agnes_enabled=True,
        agnes_model_name="agnes-test",
        agnes_base_url="https://agnes.example/v1",
        agnes_api_key="secret",
        gemma_enabled=True,
        gemma_model_name="gemma-test",
        gemma_base_url="https://gemma.example/v1",
        gemma_api_key="secret",
        agnes_runner=_failed_agnes_runner,
        gemma_primary_runner=lambda _: _gemma_primary_draft(),
    )
    assert result.primary_provider_attempted == "agnes"
    assert result.primary_provider_used == "gemma"
    assert result.provider_failover is True
    assert result.provider_failure_code is not None
    assert result.provider_failure_detail is not None
    assert result.deterministic_resolution == "EXPLICIT_PROVIDER_FAILOVER"
