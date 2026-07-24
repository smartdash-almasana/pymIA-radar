# RADAR — Playwright → Semantic Integration 001

**Cycle ID:** `RADAR-PLAYWRIGHT-SEMANTIC-INTEGRATION-001`
**Status:** `VERIFIED`
**Scope:** demostrar en campaña controlada el recorrido NavigationResult → DiscoveryResult → Conversation → evaluación semántica V3 → ConversationAssessmentV3 → candidato presuntivo / Lista 1.

---

## 1. Flujo implementado

```
NavigationResult
→ navigation_to_discovery() / process_and_persist()
→ DiscoveryResult
→ persist_discovery_results()
→ Conversation
→ assess_conversation_cascade_v1()
→ persist_cascade_assessment()
→ ConversationAssessmentV3
→ create_or_update_presumptive_candidate()
→ PresumptiveCandidate (solo si elegible)
```

## 2. Decisiones

- Evaluación automática solo dentro de esta campaña controlada. No evaluación global.
- `persist_cascade_assessment()` extraído de `routes.py` para reutilizar el mapeo cascade → ORM.
- El endpoint `POST /conversations/{id}/assessments/v3` ahora usa la misma función.
- `run_playwright_semantic_pipeline()` acepta un `agnes_runner` inyectable para tests.
- Sin nuevos modelos, migraciones, estados ni dependencias.

## 3. Archivos

- `app/services/semantic_integration.py` (nuevo)
- `app/api/routes.py` (modificado: usa `persist_cascade_assessment()`)
- `tests/test_playwright_semantic_integration.py` (nuevo)
- `docs/specs/PLAYWRIGHT_SEMANTIC_INTEGRATION_001.md`
- `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md`

## 4. Criterios de aceptación verificados

- navegación válida + assessment elegible → Conversation + assessment + candidate
- Conversation idempotente por source + external_id
- historial de assessments append-only
- un único candidato presuntivo activo por actor + conversación; una reevaluación actualiza su assessment asociado
- candidato persistido de forma durable y verificable tras reabrir sesión
- navegación bloqueada → nada
- assessment INVALID_MODEL_OUTPUT → Conversation + assessment, sin candidate
- assessment COMPLETED no elegible → sin candidate
- endpoint V3 exitoso sigue persistiendo assessments tras la extracción
- revisión humana sigue exigiendo assessment COMPLETED
- autor ausente conserva author_status=UNAVAILABLE en trazabilidad
- 312 tests passed, 2 skipped, 0 regresiones