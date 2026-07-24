# RADAR — Piloto integral de aceptación — Reporte de verificación

**Cycle ID:** `RADAR-PILOT-INTEGRAL-ACCEPTANCE-001`
**Estado:** `IMPLEMENTING` → `VERIFIED`
**Fecha:** 2026-07-24

---

## Resumen

El piloto integral demuestra que el flujo completo desde `NavigationResult` hasta `ApprovedOpportunityV1` con exportación JSON/CSV funciona correctamente, reutilizando exclusivamente servicios existentes.

---

## Flujo verificado

```
NavigationResult
→ persist_discovery_results → Conversation ✓
→ assess_conversation_cascade_v1 → ConversationAssessmentV3 ✓
→ create_or_update_presumptive_candidate → PresumptiveCandidate ✓
→ ReviewDecision(APPROVE_DISCOVERY_CONTACT) ✓
→ create_opportunity_from_review → ApprovedOpportunityV1 ✓
→ opportunity_to_json / opportunities_to_csv ✓
```

Sin escrituras directas sobre tablas desde el runner del piloto.

---

## Reglas verificadas

| Regla | Verificación |
|---|---|
| Revisión humana obligatoria | `created_by` se pasa desde el runner; si vacío, `create_opportunity_from_review` retorna `None` |
| Navegación bloqueada detiene el flujo | `CAPTCHA_BLOCKED` → pipeline retorna sin conversation/assessment/candidate |
| Assessment no elegible no genera candidato | `NONE` affinity → `create_or_update_presumptive_candidate` retorna `None` |
| `created_by` vacío impide oportunidad | Review se crea, pero `create_opportunity_from_review` retorna `None` por guardia interna |
| `Conversation` idempotente | Mismo `NavigationResult` → misma `Conversation` (1 registro) |
| `ApprovedOpportunityV1` idempotente | Misma review → mismo `ApprovedOpportunityV1` por `UniqueConstraint("human_review_id")` |
| Sin CRM, mensajería ni precalificación | No hay llamadas a CRM, webhooks, Relaticle ni contacto automático en el flujo |

---

## Resultados de pruebas

| Suite | Resultado |
|---|---|
| `test_pilot_integral_acceptance.py` | 6/6 passed |
| `test_playwright_semantic_integration.py` | 12/12 passed |
| `test_approved_opportunity_v1.py` | 18/18 passed |
| Suite completa | 336 passed, 2 skipped |
| Regresiones | 0 |

---

## Archivos del ciclo

- `app/services/pilot_integral_acceptance.py` — runner del flujo integral
- `tests/test_pilot_integral_acceptance.py` — 6 tests focales
- `docs/specs/RADAR_PILOT_INTEGRAL_ACCEPTANCE_001.md` — especificación APPROVED → VERIFIED

---

## Conclusión

El piloto integral de aceptación se verifica exitosamente. Todos los componentes del flujo (`NavigationResult → Conversation → ConversationAssessmentV3 → PresumptiveCandidate → ReviewDecision → ApprovedOpportunityV1 → JSON/CSV`) funcionan correctamente, son idempotentes donde corresponde, y respetan las reglas de negocio (revisión humana obligatoria, detención ante bloqueo, assessment no elegible, `created_by` requerido). Sin regresiones. Sin contacto ni mensajería.