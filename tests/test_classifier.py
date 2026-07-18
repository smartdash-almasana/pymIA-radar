from app.semantics.classifier import classify_conversation

def test_relevant_conversation():
    result = classify_conversation(
        "Busco una inversión regenerativa de largo plazo en Yucatán, "
        "con comunidad y propósito."
    )
    assert result.relevant is True
    assert result.affinity_score > 0

def test_irrelevant_conversation():
    result = classify_conversation(
        "Busco vacaciones baratas para visitar Chichén Itzá."
    )
    assert result.recommended_action in {"discard", "human_review"}
