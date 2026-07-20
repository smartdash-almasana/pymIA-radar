# Roadmap de RADAR

Este roadmap está subordinado a la arquitectura maestra y no autoriza implementación de especificaciones `DRAFT`.

## Fase 0 — Baseline y autoridad

- verificar repositorio y pruebas;
- auditar last30days y Relaticle;
- congelar alcance dedicado a Inlak’ech;
- reconciliar documentación;
- aprobar contratos antes de modificar código.

## Fase 1 — Descubrimiento público

- ejecutar búsquedas reales;
- normalizar resultados;
- deduplicar;
- persistir fuente, URL, fecha, autor, texto y contexto;
- separar evidencia experimental de operación.

## Fase 2 — Interpretación de conversación

**Estado:** `SPEC-002A — Evaluación conversacional V3` verificada el 19/07/2026.

- contrato semántico centrado en tema, contexto y afinidad aparente;
- intención aparente separada;
- evidencia literal;
- contradicciones e incertidumbre;
- corpus positivo, negativo y ambiguo;
- control negativo de falso positivo futbolístico;
- evolución versionada de la persistencia.

## Fase 3 — Revisión humana

**Estado backend:** verificado dentro de SPEC-003B.

- aprobación de contacto basada en evaluación V3;
- creación idempotente de candidato;
- edición, observación, descarte y no contacto;
- historial preservado;
- presentación progresiva en UI pendiente de especificación propia.

## Fase 4 — Embudo de descubrimiento

**Estado:** `SPEC-003B — Implementación del dominio humano de descubrimiento` está `VERIFIED`.

- migración `20260719_0003`;
- `DiscoveryCandidate` y estados separados de la conversación;
- eventos vinculados;
- `DiscoveryOutcome` humano;
- invitación y aceptación de precalificación;
- gate backend con `PREQUALIFICATION_ACCEPTED`;
- motivaciones, objeciones y arquetipo posterior al diálogo registrados humanamente.

## Fase 5 — Precalificación

**Estado:** gate backend verificado por SPEC-003B; auditoría y cierre documental de SPEC-005 pendientes.

- gate `PREQUALIFICATION_ACCEPTED`;
- mini-formulario;
- datos declarados;
- semáforo determinístico;
- recomendación revisable de camino;
- estados de maduración y calificación;
- bloqueo sin consentimiento.

## Fase 6 — Relaticle

- auditar API real;
- definir contrato de transferencia;
- crear persona únicamente cuando corresponda;
- crear oportunidad solo para lead calificado o aprobación explícita;
- transferir evidencia, notas y siguiente acción.

## Fase 7 — Piloto real

- 100 a 300 conversaciones para búsqueda y semántica;
- revisión humana real;
- contactos reales autorizados;
- casos con afinidad revelada y no confirmada;
- consentimientos y rechazos;
- precalificación real;
- al menos un caso extremo a extremo;
- informe de falsos positivos, decisiones y gaps.

## Orden obligatorio

```text
descubrimiento público
→ SPEC-002A VERIFIED
→ SPEC-003B VERIFIED
→ descubrimiento humano y consentimiento verificados en backend
→ auditoría de SPEC-005 detrás de PREQUALIFICATION_ACCEPTED
→ CRM auditado
→ piloto integral
```

No adelantar CRM, precalificación ni piloto antes de cerrar los gates previos.
