# RADAR — ApprovedOpportunityV1 001

**Cycle ID:** `RADAR-APPROVED-OPPORTUNITY-V1-001`
**Status:** `APPROVED`
**Scope:** implementar `ApprovedOpportunityV1` como contrato CRM-neutral para convertir una aprobación humana válida en una oportunidad exportable por JSON y CSV.

---

## 1. Objetivo

Construir la entidad que representa la transición de un candidato presuntivo aprobado por revisión humana a una oportunidad lista para ser transferida a un CRM externo. Sin ejecutar la transferencia real.

---

## 2. Flujo

```
ReviewDecision(APPROVE_DISCOVERY_CONTACT)
→ ApprovedOpportunityV1 creada
→ status = READY_FOR_CRM
→ exportable por JSON / CSV
→ external_crm_id = null hasta transferencia exitosa
```

---

## 3. Modelo ApprovedOpportunityV1

### Campos

| Campo | Tipo | Notas |
|-------|------|-------|
| id | int PK | |
| stable_id | str(36) | UUID4 estable |
| schema_version | str(50) | `radar-approved-opportunity/v1` |
| conversation_id | int FK | → conversations.id |
| assessment_id | int FK | → conversation_assessments_v3.id |
| presumptive_candidate_id | int FK | → presumptive_candidates.id |
| public_actor_id | int FK | → public_actors.id |
| source | str(50) | denormalizado |
| source_url | text | denormalizado |
| public_username | str(255) nullable | denormalizado |
| apparent_affinity | str(30) | |
| apparent_intention | str(40) | |
| evidence_fragments | JSON | |
| review_priority | int | |
| human_review_id | int FK | → review_decisions.id |
| human_reviewer_identity | str(255) | |
| approved_at | datetime | |
| status | str(30) | READY_FOR_CRM |
| external_crm_id | str(255) nullable | null hasta exportación |
| export_count | int | default 0 |
| last_exported_at | datetime nullable | |
| created_at | datetime | |
| updated_at | datetime | |

### UniqueConstraint

`human_review_id` — una oportunidad por revisión aprobatoria.

### Estados

| Estado | Significado |
|--------|-------------|
| READY_FOR_CRM | Pendiente de exportación |
| EXPORTED | Exportada, pendiente de confirmación |
| TRANSFER_CONFIRMED | Confirmada en CRM externo |
| TRANSFER_FAILED | Falló la transferencia |

---

## 4. Precondiciones

Para crear una `ApprovedOpportunityV1` deben cumplirse todas:

1. `Conversation` existe
2. `ConversationAssessmentV3` existe con `assessment_status == COMPLETED`
3. `PresumptiveCandidate` existe para esa conversación
4. `ReviewDecision` existe con `decision == APPROVE_DISCOVERY_CONTACT`

---

## 5. Idempotencia

Una `ReviewDecision` aprobatoria produce exactamente una `ApprovedOpportunityV1`.
Repetir la creación con la misma review devuelve la oportunidad existente.

---

## 6. Archivos

### Permitidos

- `app/models/approved_opportunity_v1.py` (nuevo)
- `app/schemas/approved_opportunity_v1.py` (nuevo)
- `app/services/approved_opportunity.py` (nuevo)
- `app/api/routes.py` (modificado)
- `alembic/versions/20260724_0007_add_approved_opportunity_v1.py` (nuevo)
- `tests/test_approved_opportunity_v1.py` (nuevo)
- `docs/specs/APPROVED_OPPORTUNITY_V1_001.md` (nuevo)
- `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md` (modificado)
- `app/models/__init__.py`, `app/db/session.py`, `alembic/env.py` (modificados para registrar modelo)

### Prohibido

- CRM específico
- webhook
- transferencia real
- mensajería
- cambios Playwright
- cambios semánticos
- cambios visuales
- nuevas dependencias
- refactor general
- commit / push / merge

---

## 7. Pruebas obligatorias

1. Aprobación válida crea oportunidad
2. Misma aprobación devuelve misma oportunidad
3. OBSERVE/DISCARD → rechazo
4. Assessment no COMPLETED → rechazo
5. Candidate inexistente → rechazo
6. Conversation inexistente → rechazo
7. JSON export válido con schema_version
8. CSV con encabezado estable
9. Status inicial READY_FOR_CRM
10. external_crm_id null
11. Endpoints create/get/list/export funcionan
12. Flujo Playwright → assessment → candidate no se altera
13. Suite completa sin regresiones