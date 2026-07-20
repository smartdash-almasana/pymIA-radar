from app.semantics.conversation_assessment_v3 import (
    build_conversation_input,
    distinct_conversation_parts,
    normalize_literal_text,
    validate_evidence_fragments,
)


def test_literal_evidence_accepts_whitespace_normalization() -> None:
    valid, rejected = validate_evidence_fragments(
        ["Busco una comunidad\n regenerativa en Yucatán."],
        ["Busco una comunidad regenerativa en Yucatán."],
    )
    assert valid == ["Busco una comunidad regenerativa en Yucatán."]
    assert rejected == []


def test_invented_or_translated_evidence_is_rejected() -> None:
    valid, rejected = validate_evidence_fragments(
        ["Busco una comunidad regenerativa en Yucatán."],
        ["I am looking for a regenerative community in Yucatan."],
    )
    assert valid == []
    assert rejected == ["I am looking for a regenerative community in Yucatan."]


def test_conversation_input_does_not_duplicate_identical_parts() -> None:
    rendered = build_conversation_input(
        title="Texto repetido",
        text="Texto repetido",
        context="Contexto diferente",
    )
    assert rendered.count("Texto repetido") == 1
    assert "[CONTEXT]" in rendered


def test_distinct_parts_and_normalization_are_stable() -> None:
    parts = distinct_conversation_parts(
        title="  Una   frase ",
        text="Una frase",
        context="Otra frase",
    )
    assert len(parts) == 2
    assert normalize_literal_text(parts[0]) == "Una frase"
