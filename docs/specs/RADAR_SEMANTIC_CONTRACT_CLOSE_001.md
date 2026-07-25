# RADAR — Cierre contractual semántico 001

**Cycle ID:** `RADAR-SEMANTIC-CONTRACT-CLOSE-001`  
**Estado:** `VERIFIED`

## Alcance cerrado

RADAR interpreta conversaciones públicas bajo la regla:

```text
El LLM interpreta el sentido.
RADAR valida, registra y gobierna.
La persona decide.
```

La salida semántica V3 es provisional y no autoriza contacto, consentimiento, precalificación, capacidad económica, arquetipo ni transferencia comercial.

## Contrato vigente

- Skill: `inlakech_affinity_v1`
- Versión: `1.0.0`
- Schema: `ConversationAssessmentV3Result`
- Afinidad: `NONE | POSSIBLE | CLEAR`
- Intención: `NONE | THEMATIC_SYMPATHY | EXPLORATION | ACTION_ORIENTED`
- Riesgo: `LOW | MEDIUM | HIGH`
- Evidencia: fragmentos literales continuos presentes en título, texto o contexto
- Revisión humana: obligatoria

## Tolerancia operativa

- un intento normal;
- un único reintento por formato inválido;
- sin reintento ante `SemanticProviderError`;
- segundo fallo de formato → `INVALID_MODEL_OUTPUT`;
- failover explícito y trazable;
- ambos proveedores no disponibles → `ALL_PROVIDERS_UNAVAILABLE`.

## Evidencia técnica

- `app/semantics/conversation_assessment_v3.py`
- `app/semantics/semantic_cascade_v1.py`
- `app/services/semantic_integration.py`
- `config/semantic_skills/inlakech_affinity_v1.yaml`
- `docs/SEMANTIC_SKILL_CONTRACT_V1.md`
- `docs/specs/SEMANTIC_SINGLE_RETRY_CLOSE_001.md`
- `tests/test_assessment_v3_normalization.py`
- `tests/test_semantic_cascade_v1.py`
- `tests/test_playwright_semantic_integration.py`
- `tests/test_pilot_integral_acceptance.py`

## Verificación de regresión

- `tests/test_assessment_v3_normalization.py`: passed
- `tests/test_semantic_cascade_v1.py`: passed
- Integración relacionada: 48 passed
- Suite completa: 336 passed, 2 skipped
- Regresiones: 0

## Veredicto

```text
SEMÁNTICA V3: CONTRACTUALMENTE CERRADA
INTERPRETACIÓN: LLM
GOBIERNO: RADAR
DECISIÓN: HUMANA
AUTOMATIZACIÓN COMERCIAL: NO AUTORIZADA
```
