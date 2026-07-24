# Experimento: Validación de Lista 1 con Conversaciones Públicas Reales

**Fecha**: 2026-07-20 (v1) / 2026-07-20 (v2)
**Commit base**: `c6f2f37`

---

## Versión 1 — Pipeline original (skill v1.0.0, sin normalizer, sin retry)

| Caso | Descripción | Status | Afinidad | Acción | Candidato | Esperado |
|------|-------------|--------|----------|--------|-----------|----------|
| **A** | Ecovillage en México | `INVALID_MODEL_OUTPUT` | N/A | OBSERVE | NO | **FAIL** |
| **B** | Curiosidad sobre Yucatán | `INVALID_MODEL_OUTPUT` | N/A | OBSERVE | NO | **FAIL** |
| **C** | Inversión inmobiliaria | `COMPLETED` | CLEAR | REVIEW | SÍ | **FAIL (falso positivo)** |

---

## Versión 2 — Pipeline corregido (skill v1.1.0 + normalizer + retry)

**Modelo**: MiMo 2.5 Free (via OpenCode Zen)
**Proveedor**: `opencode_zen`
**Skill**: Inlak'ech Affinity v1.1.0
**Cambios**:
- `app/semantics/draft_normalizer.py` — normaliza campos extra, enums, schema_version
- `app/semantics/conversation_assessment_v3.py` — reintento único con temperature=0.0
- `config/semantic_skills/inlakech_affinity_v1.yaml` — anti-patterns, clear_requirements

### Resultados v2

| Caso | Llamadas | Retry? | Status | Afinidad | Acción | Candidato | Esperado |
|------|----------|--------|--------|----------|--------|-----------|----------|
| **A** | 2 (0.1 → 0.0) | SÍ | `INVALID_MODEL_OUTPUT` | N/A | OBSERVE | NO | **FAIL** |
| **B** | 2 (0.1 → 0.0) | SÍ | `INVALID_MODEL_OUTPUT` | N/A | OBSERVE | NO | **FAIL** |
| **C** | 2 (0.1 → 0.0) | SÍ | `INVALID_MODEL_OUTPUT` | N/A | OBSERVE | NO | **PASS (falso negativo)** |

NOTA: El Caso C ahora falla con INVALID_MODEL_OUTPUT en lugar de producir falso positivo. El anti-patrón no pudo evaluarse porque el modelo nunca completó el JSON.

---

## Diagnóstico de Causa Raíz

Tras investigar, el problema NO es de formato ni de schema estricto.
**El problema es que `max_tokens=2048` es insuficiente para MiMo 2.5 Free.**

MiMo 2.5 Free es un **modelo de razonamiento** que emite chain-of-thought extenso
antes del JSON. El desglose de tokens es:

| max_tokens | reasoning_tokens | content_tokens | finish_reason | normalize |
|-----------|-----------------|---------------|---------------|-----------|
| **2048**  | 2047            | ~1            | `length`      | **FAIL** — sin contenido |
| **4096**  | 1981            | 489           | `stop`        | **OK** — CLEAR, 8 evidencias |
| **8192**  | 2612            | 407           | `stop`        | **OK** — CLEAR, 7 evidencias |

Con `max_tokens=2048`, el modelo consume ~2000 tokens en razonamiento y NO LE QUEDA
presupuesto para el JSON. El `content` llega vacío, `_extract_provider_content` lanza
`TypeError`, el retry intenta con temperature=0.0 pero el problema es el mismo.

### Flujo de falla exacto

```
MiMo 2.5 Free recibe prompt + conversación
→ emite 2047 tokens de razonamiento (chain-of-thought)
→ finish_reason = "length" (se acabó el budget)
→ content queda vacío o truncado
→ _extract_provider_content: TypeError("response content has unsupported shape")
→ runner: InvalidModelOutputError("invalid provider response envelope")
→ assess_conversation_v3: retry con temperature=0.0
→ mismo resultado (2048 tokens no alcanzan)
→ INVALID_MODEL_OUTPUT definitivo
```

### Con max_tokens=4096 (diagnóstico)

El modelo produce JSON COMPLETO y VÁLIDO:

```json
{
  "schema_version": "radar-conversation-assessment/v3",
  "real_topic": "Seeking co-creators to build an ecovillage in Mexico...",
  "contextual_meaning": "A Reddit post in r/intentionalcommunity...",
  "apparent_affinity": "CLEAR",
  "apparent_affinity_domains": ["COMMUNITY", "REGENERATION", "TERRITORY",
    "PURPOSEFUL_BUILDING", "BELONGING", "LONG_TERM",
    "NON_SPECULATIVE_DEVELOPMENT", "ACTIVE_PARTICIPATION",
    "MEXICO_YUCATAN_CONNECTION"],
  "apparent_intention": "ACTION_ORIENTED",
  "evidence_fragments": [8 fragments literales],
  "contradictions": [],
  "false_positive_risk": "LOW",
  "uncertainty": "LOW",
  "human_review_reason": "..."
}
```

El normalizador lo procesa sin errores. El schema estricto lo acepta.
Los anti-patterns están presentes en el system prompt.
**Todo funciona correctamente cuando hay presupuesto de tokens suficiente.**

---

## Hallazgos Clave (actualizado)

1. **Bug preexistente: `max_tokens=2048` es insuficiente para MiMo 2.5 Free**
   - El modelo consume ~2000 tokens en razonamiento, dejando ~0 para el JSON
   - Aumentar a 4096 soluciona COMPLETAMENTE el INVALID_MODEL_OUTPUT
   - Afecta a 4 archivos en el código base

2. **El normalizador funciona correctamente** — con JSON completo, extrae campos,
   normaliza enums, impone schema_version, y el schema estricto lo acepta

3. **El reintento funciona pero no ayuda** — el problema no es de formato sino de
   presupuesto de tokens; temperature=0.0 no cambia el consumo de razonamiento

4. **Los anti-patterns no pudieron evaluarse** — el modelo nunca completó JSON
   para el Caso C, por lo que no se pudo verificar si previenen el falso positivo

5. **El falso positivo del Caso C en v1 fue aleatorio** — el modelo devolvió JSON
   parcial que por casualidad se interpretó como CLEAR. Con max_tokens adecuado,
   el comportamiento podría ser diferente (y potencialmente correcto)

---

## Recomendaciones (actualizado)

1. **Aumentar `max_tokens` de 2048 a 4096** en los 4 archivos que lo hardcodean
   (`conversation_assessment_v3.py`, `lab_service.py`, `llm_classifier.py`,
   `semantic_cascade_v1.py`)
2. **Re-ejecutar el experimento v3** con max_tokens=4096 para validar:
   - Caso A → CLEAR/REVIEW/candidato (ecovillage)
   - Caso B → clasificación de curiosidad general en Yucatán
   - Caso C → NONE/DISCARD/sin candidato (anti-patrón de inversión)
3. **Verificar que los anti-patterns funcionan** en el Caso C
4. **Considerar hacer configurable `max_tokens`** vía variable de entorno

---

## Archivos

- `scripts/experimento_lista1_casos_reales.py` (v1, eliminado)
- `scripts/experimento_lista1_v2.py` (v2, temporal)
- `scripts/diagnostico_max_tokens.py` (diagnóstico)
- `.tmp/reporte-experimento-lista1-20260720-194714.json` (v1)
- `.tmp/reporte-experimento-lista1-v2-20260720-204314.json` (v2)
- `.tmp/diagnostico-raw-4096.txt` (JSON completo con max_tokens=4096)
- `app/semantics/draft_normalizer.py` — nuevo normalizador (funciona)
- `app/semantics/conversation_assessment_v3.py` — retry agregado (no ayuda sin max_tokens)
- `config/semantic_skills/inlakech_affinity_v1.yaml` — v1.1.0 (no se pudo validar)

---

## Versión 3 — max_tokens=4096 (centralizado) + truncation detection

**Commit**: actual
**Modelo**: MiMo 2.5 Free (vía Agnes)
**Proveedor**: `agnes`
**Skill**: Inlak'ech Affinity v1.1.0
**max_tokens**: 4096 (centralizado vía `settings.semantic_max_tokens`)
**Nuevo status**: `MODEL_OUTPUT_TRUNCATED` en `AssessmentStatusV3`

### Cambios aplicados

| Archivo | Cambio |
|---------|--------|
| `app/core/config.py` | Nuevo `semantic_max_tokens: int = 4096` |
| `app/schemas/assessment_v3.py` | Nuevo `MODEL_OUTPUT_TRUNCATED` status |
| `app/semantics/conversation_assessment_v3.py` | `max_tokens=4096` + finish_reason detection |
| `app/lab_service.py` | `max_tokens=settings.semantic_max_tokens` + truncation check |
| `app/semantics/llm_classifier.py` | `max_tokens=settings.semantic_max_tokens` |
| `app/semantics/semantic_cascade_v1.py` | `max_tokens=settings.semantic_max_tokens` |

### Resultados v3

| Caso | Status | Afinidad | Intención | Evidencia | Acción | Error | Esperado | Resultado |
|------|--------|----------|-----------|-----------|--------|-------|----------|-----------|
| **A** | COMPLETED | CLEAR | ACTION_ORIENTED | 7 | REVIEW | — | CLEAR / ACTION_ORIENTED | **PASS** |
| **B** | COMPLETED | POSSIBLE | EXPLORATION | 2 | REVIEW | PARTIAL_EVIDENCE_REJECTED | NONE / NONE | **FAIL** |
| **C** | COMPLETED | POSSIBLE | ACTION_ORIENTED | 3 | REVIEW | — | NONE / NONE | **FAIL** |

### Análisis

- **Caso A**: Funciona correctamente. CLEAR + ACTION_ORIENTED con 7 evidencias literales.
- **Caso B**: Falso positivo. Curiosidad casual sobre Yucatán interpretada como POSSIBLE/EXPLORATION.
- **Caso C**: Falso positivo. Inversión especulativa interpretada como POSSIBLE/ACTION_ORIENTED. Los anti-patterns de v1.1.0 no previenen esta clasificación.
- **Truncation detection**: No se activó (ningún caso llegó a finish_reason=length con 4096 tokens).

### Problema actual

El pipeline técnico funciona (COMPLETED, sin errores). El problema es de **precisión semántica**: el skill v1.1.0 no discrimina suficientemente entre afinidad real (Caso A) y ruido temático (Casos B y C). Los anti-patterns existen en el system prompt pero el modelo no los aplica consistentemente.
