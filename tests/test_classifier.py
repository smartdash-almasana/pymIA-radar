from app.schemas.assessment import DeclaredCapacity, ReviewAction
from app.semantics.classifier import classify_conversation


def test_relevant_conversation_is_multidimensional_and_provisional() -> None:
    result = classify_conversation(
        "Busco una inversión regenerativa de largo plazo en Yucatán, "
        "con comunidad y propósito."
    )
    assert result.thematic_affinity > 0
    assert result.values_affinity > 0
    assert result.intent_score > 0
    assert result.declared_capacity == DeclaredCapacity.UNKNOWN
    assert result.human_review_required is True
    assert result.provisional is True
    assert result.recommended_action in {
        ReviewAction.OBSERVE,
        ReviewAction.REVIEW_OR_NURTURE,
        ReviewAction.APPROACH_REVIEW,
    }


def test_superficial_travel_mention_is_not_promoted_to_lead() -> None:
    result = classify_conversation(
        "Busco vacaciones baratas para visitar Chichén Itzá."
    )
    assert result.recommended_action == ReviewAction.DISCARD
    assert result.declared_capacity == DeclaredCapacity.UNKNOWN
    assert result.review_priority < 40


def test_capacity_is_never_inferred_from_investment_language() -> None:
    result = classify_conversation(
        "Soy empresario y estoy evaluando invertir en un proyecto de largo plazo en Yucatán."
    )
    assert result.intent_score > 0
    assert result.declared_capacity == DeclaredCapacity.UNKNOWN


def test_objection_is_preserved_as_evidence() -> None:
    result = classify_conversation(
        "Estoy evaluando invertir en Yucatán, pero me preocupa la seguridad jurídica y la transparencia."
    )
    assert "seguridad jurídica" in result.objections
    assert "transparencia" in result.objections
