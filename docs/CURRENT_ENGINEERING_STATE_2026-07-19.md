# Estado actual de ingeniería — 19/07/2026

## Propósito

Este checkpoint registra la reconciliación documental posterior a la definición del embudo humano de descubrimiento.

Registra qué partes de la arquitectura están documentadas, implementadas o verificadas. Distingue expresamente:

```text
DOCUMENTADO
IMPLEMENTADO
VERIFICADO
PENDIENTE
```

## Estado de la reconciliación

```text
ARQUITECTURA NUEVA: DOCUMENTADA
AUDITORÍA TÉCNICA DE IMPACTO: COMPLETADA
DOMINIO HUMANO DE DESCUBRIMIENTO: VERIFIED — candidato, eventos, outcome, consentimiento y gate de precalificación
MIGRACIÓN DE ESQUEMA: 20260719_0003 (head) VERIFICADA EN SQLITE
SPEC-002A: VERIFIED — contrato V3, evidencia literal, fallback cerrado, persistencia, API y migraciones
SPEC-003B: VERIFIED — Ciclos 1 y 2 cerrados
PRUEBAS DE RADAR: 136 PASSED — ejecutadas el 19/07/2026
COMMIT/PUSH: NO REALIZADOS
```

## Decisión estructural

RADAR permanece en el repositorio actual y adopta dos embudos separados:

```text
conversación pública
→ afinidad semántica aparente
→ revisión humana
→ contacto y embudo de descubrimiento
→ afinidad revelada o descartada
→ consentimiento
→ precalificación
→ lead calificado
→ Relaticle
```

No se crea otro repositorio ni una plataforma auxiliar.

## Documentos rectores reconciliados

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`;
- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/DOCUMENT_PRECEDENCE.md`;
- `docs/PRODUCT_SCOPE.md`;
- `docs/ARCHITECTURE.md`;
- `docs/RADAR_TECHNICAL_IMPACT_AUDIT_2026-07-19.md`;
- `AGENTS.md`;
- `README.md`.

## Especificaciones reconciliadas

| Especificación | Estado posterior | Observación |
|---|---|---|
| SPEC-001 / 001A / 001B / 001C | Sin redefinición de código | El descubrimiento público sigue siendo base; debe sanearse la admisión operativa |
| SPEC-002 | DRAFT CONCEPTUAL | Define el objeto semántico; su implementación queda concretada por SPEC-002A |
| SPEC-002A | VERIFIED | Evaluación V3, migraciones, evidencia literal y fallback cerrado; 27 focales y 115 pruebas totales |
| SPEC-003 | DRAFT CONCEPTUAL | Revisión orientada a contacto de descubrimiento |
| SPEC-003A | DRAFT CONCEPTUAL | Define el embudo humano de descubrimiento |
| SPEC-003B | VERIFIED | Candidato idempotente, eventos vinculados, outcome humano, consentimiento, invitación/aceptación y gate backend verificados; UI queda fuera de esta especificación |
| SPEC-004 | DRAFT / BLOQUEADA | Relaticle sigue pendiente de auditoría real |
| SPEC-005 | DRAFT — AUDITORÍA AUTORIZADA | El gate `PREQUALIFICATION_ACCEPTED` ya está implementado; falta reconciliar el contrato de cualificación y su compatibilidad legada |
| SPEC-006 | DRAFT — BLOQUEADA | Piloto debe incluir descubrimiento humano y consentimiento |

## Capacidades existentes reutilizables

- integración real con last30days mediante adaptador;
- normalización, persistencia y deduplicación;
- modelo `Conversation`;
- API FastAPI y bandeja local;
- integración Agnes/OpenAI-compatible;
- contratos Pydantic;
- revisión humana antes de registrar contacto;
- `EngagementEvent` para contacto y respuesta;
- precalificación determinística;
- frontera local con Relaticle.

Estas capacidades no equivalen al cumplimiento de la arquitectura nueva.

## Gaps técnicos confirmados

### 1. Contrato semántico legado

`app/schemas/assessment.py` y `SemanticAssessmentV2` todavía contienen:

- `declared_capacity`;
- `probable_archetype`;
- `archetype_confidence`;
- `archetype_evidence`;
- puntajes centrados en evaluación prematura de persona.

La arquitectura objetivo exige una versión centrada en:

- tema real;
- contexto;
- afinidad aparente;
- intención aparente;
- evidencia;
- contradicciones;
- faltantes;
- incertidumbre.

La evolución debe ser versionada y no destruir registros históricos.

### 2. Compatibilidad comercial legada

`QualificationResult.radar_state` y `QualificationRecord.radar_state` permanecen como salida histórica de compatibilidad.

En el flujo nuevo no modifican `Conversation.status`, no modifican `DiscoveryCandidate.discovery_state` y no sustituyen el gate `PREQUALIFICATION_ACCEPTED`.

Su versionado definitivo corresponde al cierre específico de SPEC-005.

### 3. Interfaz no separada por etapas

El backend ya separa conversación, candidato, outcome y cualificación, pero la bandeja actual todavía los reúne en una ficha. La interfaz requiere divulgación progresiva:

1. conversaciones para revisar;
2. casos en descubrimiento;
3. personas habilitadas para precalificación;
4. leads calificados y transferencia.

### 4. Relaticle no auditado

La integración externa continúa bloqueada. No debe crearse persona u oportunidad real sin contrato verificado y reglas de transferencia aprobadas.

## Reglas sustituidas documentalmente

Quedan sustituidas como objetivo futuro las reglas que permitían:

- arquetipo probable desde una publicación pública;
- capacidad como dimensión central de la lectura pública;
- salto directo de respuesta a precalificación;
- tratar al candidato de revisión como lead;
- lenguaje de conversión antes de revelar afinidad.

El código que todavía las contiene se considera legado pendiente, no implementación válida de la arquitectura nueva.

## Reglas preservadas

- cliente único Inlak’ech;
- un solo repositorio;
- búsqueda y fuentes como piezas auxiliares;
- revisión humana obligatoria;
- no contacto automático;
- evidencia y trazabilidad;
- capacidad únicamente declarada;
- consentimiento separado;
- precalificación determinística reutilizable;
- Relaticle como CRM externo;
- no SaaS, no CRM propio, no microservicios innecesarios.

## Estado de pruebas

La verificación reproducible acumulada produjo:

```text
python -m pytest -q tests/test_conversation_assessment_v3.py tests/test_evidence_validation.py tests/test_api_assessment_v3.py tests/test_semantic_calibration_v2.py tests/test_migrations.py
27 passed

python -m pytest -q tests/test_discovery_candidate.py tests/test_discovery_outcome.py tests/test_workflow_transitions.py tests/test_prequalification_gate.py tests/test_discovery_models.py tests/test_migrations.py
26 passed

python -m pytest -q
136 passed

SQLite temporal: python -m alembic upgrade head; python -m alembic current
20260719_0003 (head)
```

También se verificó `python -m alembic history` y `git diff --check` sin errores.

## Decisiones técnicas aprobadas

Las decisiones `DTI-01` a `DTI-08` quedaron aprobadas mediante `D-010` en `docs/DECISIONS.md`.

Especificaciones cerradas:

```text
docs/specs/002A_conversation_assessment_v3.md
docs/specs/003B_discovery_domain_implementation.md
```

## Siguiente acción permitida

La siguiente acción es auditar y reconciliar `SPEC-005` contra el gate `PREQUALIFICATION_ACCEPTED` ya implementado. La interfaz progresiva debe redactarse y aprobarse como una especificación separada antes de modificarse.

Orden obligatorio siguiente:

```text
SPEC-002A VERIFIED
→ SPEC-003B VERIFIED
→ auditoría y cierre de SPEC-005
→ especificación de UI progresiva
→ Relaticle auditado
→ piloto integral
```

## Prohibiciones vigentes

No corresponde todavía:

- modificar el dominio verificado de SPEC-003B sin una nueva especificación aprobada;
- eliminar o mutar registros `SemanticAssessmentV2`;
- convertir evaluaciones V2 en V3;
- crear candidatos desde datos públicos sin aprobación humana;
- asignar arquetipos desde conversaciones;
- conectar precalificación directamente a `REPLIED`;
- ampliar la interfaz fuera del alcance aprobado;
- integrar Relaticle;
- ejecutar piloto comercial;
- crear otro repositorio.
