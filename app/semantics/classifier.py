from app.schemas.assessment import AssessmentResult
from app.semantics.deterministic_filter import deterministic_score

def classify_conversation(text: str) -> AssessmentResult:
    """Clasificador inicial determinístico.

    La llamada LLM estructurada se incorporará después de validar el corpus real.
    """
    result = deterministic_score(text)
    score = result["score"]

    archetype = None
    normalized = text.lower()
    if any(term in normalized for term in ["legado", "visión", "sistema", "proyecto"]):
        archetype = "pionero_visionario"
    if any(term in normalized for term in ["largo plazo", "paciencia", "raíz", "patrimonio"]):
        archetype = "sembrador_paciente"
    if any(term in normalized for term in ["artesanía", "materiales", "regenerativo", "oficio"]):
        archetype = "artifice_regenerativo"

    return AssessmentResult(
        relevant=result["passes"],
        affinity_score=score,
        investment_intent=min(100, score + (20 if "invert" in normalized else 0)),
        probable_archetype=archetype,
        conversation_stage="exploration" if result["passes"] else "unknown",
        recommended_action="human_review" if result["passes"] else "discard",
        evidence=result["positive_hits"],
        missing_data=["resource_availability", "time_horizon"] if result["passes"] else [],
        risk_flags=[f"negative:{x}" for x in result["negative_hits"]],
        reasoning_summary=(
            "La conversación contiene señales semánticas compatibles con Inlak'ech."
            if result["passes"]
            else "No se encontraron señales suficientes para recomendar revisión."
        ),
    )
