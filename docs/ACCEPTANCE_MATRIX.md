# Matriz de aceptación

| ID | Capacidad | Evidencia exigida | Estado |
|---|---|---|---|
| A-01 | Ejecutar búsqueda real | Resultado con texto, URL, fuente y fecha | VERIFICADO — SPEC-001 / M1 |
| A-02 | Normalizar resultados | Contrato único validado | VERIFICADO — JSON agent v1.2 |
| A-03 | Evitar duplicados | Segunda ingesta no duplica registros equivalentes | VERIFICADO EN ALCANCE PREVIO — REVISAR CORPUS OPERATIVO |
| A-04 | Interpretar tema y contexto | Salida V3 estructurada centrada en conversación real | VERIFICADO — SPEC-002A; 27 focales y 115 pruebas totales el 19/07/2026 |
| A-05 | Detectar afinidad aparente | Afinidad explicada con evidencia literal validada | VERIFICADO — SPEC-002A y corpus de calibración V2 |
| A-06 | Distinguir intención aparente | Separar simpatía temática, exploración y acción | VERIFICADO — SPEC-002A |
| A-07 | Representar incertidumbre | Contradicciones, faltantes, riesgo y fallback cerrado | VERIFICADO — SPEC-002A |
| A-08 | Revisar humanamente | Aprobar contacto de descubrimiento, editar, observar, descartar y no contactar | VERIFICADO — SPEC-003B; aprobación V3 crea candidato idempotente |
| A-09 | Registrar contacto humano | Evidencia de envío asociada a `DiscoveryCandidate` | VERIFICADO — eventos nuevos requieren candidato y transición válida |
| A-10 | Registrar respuesta | Respuesta asociada al candidato y a la conversación de origen | VERIFICADO — respuesta vinculada sin habilitar precalificación |
| A-11 | Administrar descubrimiento | Candidato, diálogo y estados persistentes | VERIFICADO — SPEC-003B; modelos, workflow, migración y API |
| A-12 | Registrar afinidad revelada | `DiscoveryOutcome` confirmado por humano | VERIFICADO — outcome humano persistente e idempotente |
| A-13 | Restringir arquetipo | Ningún arquetipo desde publicación; hipótesis posterior y confirmada | VERIFICADO — confirmación exige evidencia humana; V2 no se copia |
| A-14 | Bloquear precalificación prematura | Requiere `PREQUALIFICATION_ACCEPTED` y consentimiento | VERIFICADO — backend devuelve 409 ante gate incompleto |
| A-15 | Precalificar | Reglas aplicadas a respuestas declaradas reales | VERIFICADO EN BACKEND — gate de SPEC-003B y reglas determinísticas; cierre documental de SPEC-005 pendiente |
| A-16 | Calificar | Resultado explicable y revisable | IMPLEMENTACIÓN DETERMINÍSTICA REUTILIZABLE — auditoría específica de SPEC-005 pendiente |
| A-17 | Transferir a Relaticle | Registro real solo para lead permitido | BLOQUEADO — RELATICLE NO AUDITADO |
| A-18 | Crear oportunidad | Oportunidad y tarea autorizadas en Relaticle | BLOQUEADO — RELATICLE NO AUDITADO |
| A-19 | E2E completo | Conversación → descubrimiento humano → consentimiento → lead → CRM | PENDIENTE — SPEC-006 DRAFT |

## Reglas de estado

Un estado solo puede cambiar a `VERIFICADO` si existe:

- especificación aprobada;
- comando o procedimiento de prueba;
- resultado reproducible;
- fecha;
- artefacto o captura;
- referencia al cambio correspondiente.

`DOCUMENTADO` no equivale a `IMPLEMENTADO`.

`IMPLEMENTADO` no equivale a `VERIFICADO`.

Una capacidad de código legado puede marcarse como reutilizable, pero no como cumplimiento de la arquitectura nueva hasta que implemente sus gates y contratos.

## Gates críticos

```text
SPEC-002A VERIFIED
→ SPEC-003B puede implementarse
→ SPEC-003B VERIFIED
→ SPEC-005 conectada detrás de PREQUALIFICATION_ACCEPTED
→ Relaticle auditado
→ SPEC-006
```

El estado consolidado se mantiene en `docs/CURRENT_ENGINEERING_STATE.md`.
