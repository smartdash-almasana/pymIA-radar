# RADAR — Piloto integral de aceptación 001

**Cycle ID:** `RADAR-PILOT-INTEGRAL-ACCEPTANCE-001`
**Status:** `APPROVED`
**Scope:** verificar el flujo completo `NavigationResult → Conversation → assessment → candidate → review → opportunity → JSON/CSV` sin escrituras directas sobre tablas, sin contacto ni mensajería.

---

## 1. Objetivo

Demostrar que todos los servicios existentes pueden encadenarse correctamente para producir una oportunidad exportable desde una navegación Playwright, pasando por evaluación semántica, candidato presuntivo, revisión humana y contrato CRM-neutral.

---

## 2. Flujo rector

```
NavigationResult
→ persist_discovery_results → Conversation
→ assess_conversation_cascade_v1 → ConversationAssessmentV3
→ create_or_update_presumptive_candidate → PresumptiveCandidate
→ ReviewDecision(APPROVE_DISCOVERY_CONTACT)
→ create_opportunity_from_review → ApprovedOpportunityV1
→ opportunity_to_json / opportunities_to_csv
```

Cada etapa reusa servicios existentes. No se escribe directamente sobre tablas desde el runner del piloto.

---

## 3. Reglas verificadas

- revisión humana obligatoria (no se puede saltar con reviewer automatizado)
- navegación bloqueada (`CAPTCHA_BLOCKED`, `LOGIN_REQUIRED`, etc.) detiene el flujo antes de persistir
- assessment no elegible (`NONE`, `INVALID_MODEL_OUTPUT`) no genera candidato
- `created_by` vacío en `ReviewDecision` impide crear `ApprovedOpportunityV1`
- `Conversation` es idempotente (mismo `NavigationResult` → misma `Conversation`)
- `ApprovedOpportunityV1` es idempotente por `human_review_id`
- sin contacto, mensajería, precalificación, Relaticle ni CRM externo

---

## 4. Archivos

| Archivo | Rol |
|---|---|
| `app/services/pilot_integral_acceptance.py` | Runner que orquesta el flujo completo |
| `tests/test_pilot_integral_acceptance.py` | 6 tests focales de aceptación |
| `docs/audits/RADAR_PILOT_INTEGRAL_ACCEPTANCE_REPORT_001.md` | Reporte de verificación |
| `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md` | Actualización de estado |

---

## 5. Criterios de aceptación

1. Happy path produce `ApprovedOpportunityV1` con `status=READY_FOR_CRM` y export JSON/CSV válidos.
2. Navegación bloqueada retorna `None` en todas las etapas.
3. Assessment no elegible no produce candidato ni oportunidad.
4. `created_by` vacío en review bloquea creación de oportunidad.
5. Misma navegación dos veces produce única `Conversation`.
6. Misma review dos veces produce única `ApprovedOpportunityV1`.