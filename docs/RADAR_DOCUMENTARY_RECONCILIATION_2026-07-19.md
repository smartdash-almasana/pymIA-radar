# RADAR — Reconciliación documental del 19/07/2026

## 1. Propósito

Este documento registra la reconciliación entre la demanda original del cliente, la arquitectura maestra de RADAR y la documentación previamente vigente.

La tarea fue exclusivamente documental.

```text
CÓDIGO MODIFICADO: NO
MODELOS MODIFICADOS: NO
SCHEMAS MODIFICADOS: NO
TESTS MODIFICADOS: NO
CONFIGURACIÓN MODIFICADA: NO
DATOS MODIFICADOS: NO
GIT EJECUTADO SOBRE RADAR: NO
```

## 2. Nueva formulación rectora

RADAR debe realizar el siguiente recorrido:

```text
conversación pública
→ afinidad semántica aparente
→ persona potencialmente relevante
→ revisión humana
→ candidato de descubrimiento
→ contacto humano
→ diálogo de descubrimiento
→ afinidad revelada o descartada
→ posible hipótesis de arquetipo basada en diálogo humano
→ consentimiento para continuar
→ precalificación
→ lead calificado
→ embudo comercial
```

Se mantiene un único repositorio.

## 3. Documentos revisados

### Autoridad y producto

- `AGENTS.md`;
- `README.md`;
- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`;
- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/DOCUMENT_PRECEDENCE.md`;
- `docs/PRODUCT_SCOPE.md`;
- `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`;
- `docs/ARCHITECTURE.md`;
- `docs/DECISIONS.md`.

### Planificación y estado

- `docs/ROADMAP.md`;
- `docs/MILESTONES.md`;
- `docs/ACCEPTANCE_MATRIX.md`;
- `docs/CURRENT_ENGINEERING_STATE.md`;
- `docs/CURRENT_ENGINEERING_STATE_2026-07-18.md`;
- `docs/specs/001B_search_repertoire_v2.md`.

### Especificaciones

- `docs/specs/002_affinity_classification.md`;
- `docs/specs/003_human_review.md`;
- `docs/specs/004_relaticle_integration.md`;
- `docs/specs/005_qualification.md`;
- `docs/specs/006_end_to_end_pilot.md`.

### Código leído para detectar gaps, sin modificar

- `app/schemas/assessment.py`;
- `app/models/assessment_v2.py`;
- `app/schemas/review.py`;
- `app/schemas/qualification.py`;
- `app/models/conversation.py`.

## 4. Archivos creados

- `docs/specs/003A_discovery_funnel.md`;
- `docs/CURRENT_ENGINEERING_STATE_2026-07-19.md`;
- `docs/RADAR_DOCUMENTARY_RECONCILIATION_2026-07-19.md`.

El documento maestro de arquitectura ya había sido creado durante el mismo ciclo conceptual:

- `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`.

## 5. Contradicciones encontradas

### C-01 — Objeto inicial ambiguo

La documentación alternaba entre conversación, candidato y persona como objeto inicial.

**Resolución:** la conversación es la unidad inicial. La persona aparece después de detectar afinidad semántica aparente e identidad pública utilizable.

### C-02 — Arquetipo prematuro

La declaración obligatoria, el contrato comercial, SPEC-002 y el contrato de evaluación permitían proponer arquetipo desde una publicación pública.

**Resolución documental:** queda prohibido. El diálogo humano suficiente permite una hipótesis y la persona responsable debe confirmarla.

### C-03 — Capacidad en lectura pública

La capacidad declarada figuraba como dimensión central de la evaluación inicial, aunque normalmente aún no existe declaración.

**Resolución documental:** la lectura pública no evalúa capacidad. Los recursos se registran únicamente durante la precalificación y por declaración explícita.

### C-04 — Salto de respuesta a precalificación

El recorrido documentado y el enum vigente permitían:

```text
REPLIED
→ QUALIFICATION_STARTED
```

**Resolución documental:** se inserta el embudo humano de descubrimiento y el gate `PREQUALIFICATION_ACCEPTED`.

### C-05 — Contacto descrito como conversión

El acercamiento inicial aparecía orientado a conversión comercial.

**Resolución:** el primer contacto abre un diálogo de descubrimiento. No vende, no precalifica y no confirma afinidad.

### C-06 — Candidato y lead mezclados

Algunos textos podían presentar una conversación seleccionada o persona contactada como candidato comercial avanzado.

**Resolución:** se definen objetos separados desde conversación detectada hasta lead transferido.

### C-07 — CRM prematuro

El roadmap y SPEC-004 ubicaban creación de candidatos y oportunidades antes de la precalificación.

**Resolución:** Relaticle recibe leads autorizados; una oportunidad requiere calificación o aprobación comercial explícita documentada.

### C-08 — Arquitectura técnica insuficiente

`docs/ARCHITECTURE.md` solo describía descubrimiento, RADAR y CRM sin representar el dominio humano de descubrimiento.

**Resolución:** arquitectura expandida dentro del mismo monolito modular.

### C-09 — Agentes sin frontera conceptual específica

`AGENTS.md` no impedía de forma explícita que un agente eliminara el descubrimiento, asignara arquetipos prematuramente o iniciara precalificación sin consentimiento.

**Resolución:** reglas agregadas para Codex y OpenCode/DeepSeek V4 Flash.

## 6. Decisiones aplicadas

- un solo cliente: Inlak’ech;
- un solo repositorio;
- conversación como unidad inicial;
- afinidad pública siempre aparente y provisional;
- separación entre embudo de descubrimiento y embudo de conversión;
- contacto humano obligatorio;
- afinidad revelada registrada por humano;
- arquetipo posterior al diálogo y confirmado humanamente;
- consentimiento como frontera independiente;
- precalificación solo con datos declarados;
- Relaticle después de gates autorizados;
- evolución versionada del contrato semántico;
- no microservicios ni plataformas auxiliares.

## 7. Reglas sustituidas

Quedan sustituidas como dirección futura:

- `publicación → arquetipo probable`;
- `lectura pública → capacidad`;
- `respuesta → precalificación` sin descubrimiento;
- `candidato detectado → lead`;
- `contacto inicial → acción de conversión`;
- `puntaje agregado → comprensión suficiente`;
- `creación temprana de oportunidad en CRM`.

Los campos y transiciones que todavía existen en código no fueron eliminados. Se consideran legado pendiente de migración.

## 8. Reglas preservadas

- afinidad e intención son diferentes;
- toda interpretación debe incluir evidencia;
- toda acción externa requiere aprobación humana;
- RADAR nunca envía mensajes automáticamente;
- no inferir capacidad por profesión, ubicación o perfil;
- consentimiento separado de ajuste comercial;
- semáforo determinístico de precalificación reutilizable;
- arquetipo, perfil y camino son dimensiones distintas;
- Relaticle sigue bloqueado hasta auditoría;
- especificaciones `DRAFT` no autorizan código;
- evidencia antes que afirmación.

## 9. Estado de las especificaciones

| Especificación | Estado posterior | Motivo |
|---|---|---|
| SPEC-001B | IMPLEMENTING heredado | Debe auditarse y cerrarse por su propia evidencia; no autoriza arquitectura nueva |
| SPEC-002 | DRAFT | Contrato objetivo nuevo no implementado |
| SPEC-003 | DRAFT | Semántica de contacto de descubrimiento pendiente |
| SPEC-003A | DRAFT — NUEVA | Dominio humano de descubrimiento pendiente |
| SPEC-004 | DRAFT — BLOQUEADA | API real y gates previos pendientes |
| SPEC-005 | DRAFT — BLOQUEADA | Gate de descubrimiento no implementado |
| SPEC-006 | DRAFT — BLOQUEADA | Requiere todos los gates previos |

## 10. Gaps de código detectados

### G-01 — `AssessmentResult`

Todavía contiene:

- `declared_capacity`;
- `probable_archetype`;
- `archetype_confidence`;
- `archetype_evidence`.

### G-02 — `SemanticAssessmentV2`

Persiste la semántica anterior. Requiere evolución versionada, no mutación silenciosa.

### G-03 — `RadarCommercialState`

No contiene estados de descubrimiento ni `PREQUALIFICATION_ACCEPTED`.

### G-04 — `ReviewDecisionType`

`APPROVE_APPROACH` debe evolucionar o documentarse como aprobación de contacto de descubrimiento.

### G-05 — `EngagementEvent`

Cubre contacto y respuesta, pero no representa el resultado humano de descubrimiento.

### G-06 — Ausencia de dominio

No existen `DiscoveryCase`, `DiscoveryOutcome` ni equivalentes.

### G-07 — Interfaz

La vista actual no separa progresivamente revisión, descubrimiento, precalificación y transferencia.

### G-08 — API

La API vigente permite iniciar precalificación desde estados anteriores al gate objetivo.

### G-09 — Calibración

El corpus y las pruebas semánticas actuales incluyen arquetipo como salida de la conversación pública.

## 11. Validación realizada

### Integridad documental

Se verificó mediante lectura directa y búsquedas textuales que:

- las menciones restantes a `arquetipo probable` en documentos vigentes aparecen como exclusión, conflicto o gap;
- las referencias a `probable_archetype` continúan en código y tests, correctamente registradas como gap;
- las referencias al salto `REPLIED → QUALIFICATION_STARTED` aparecen como diagnóstico o transición prohibida;
- el checkpoint del 18/07/2026 quedó marcado como histórico;
- el puntero vigente dirige al checkpoint del 19/07/2026.

### Suite de pruebas

No se obtuvo una ejecución válida de la suite de RADAR.

El ejecutor de comandos disponible quedó anclado al repositorio `E:\BuenosPasos\smartbridge\PymIA` y rechazó el directorio de RADAR. Una ejecución producida desde PymIA fue descartada expresamente como evidencia de este proyecto.

Comando pendiente desde PowerShell:

```powershell
cd E:\BuenosPasos\inlakech-radar
python -m pytest -q
```

## 12. Clasificación posterior

```text
ARQUITECTURA: DOCUMENTADA
PRECEDENCIA: DOCUMENTADA
EMBUDO DE DESCUBRIMIENTO: ESPECIFICADO EN DRAFT
CONTRATO SEMÁNTICO NUEVO: ESPECIFICADO EN DRAFT
CÓDIGO: SIN CAMBIOS
MIGRACIÓN: PENDIENTE
PRUEBAS DE RADAR: PENDIENTES
GIT: NO EJECUTADO
```

## 13. Riesgos y asuntos no resueltos

- aprobación humana formal de SPEC-002, SPEC-003 y SPEC-003A;
- diseño exacto de migración de evaluaciones históricas;
- decisión entre tabla de estado, eventos o proyección para descubrimiento;
- taxonomía final de afinidad;
- corpus humano suficiente;
- reglas jurídicas y de retención de datos;
- auditoría real de Relaticle;
- validación de interfaz por la persona responsable.

## 14. Siguiente acción permitida

1. ejecutar la suite de RADAR desde el repo correcto;
2. revisar y aprobar la reconciliación;
3. diseñar una especificación técnica transversal de migración;
4. encargar a Codex la auditoría de impacto sobre modelos, API, UI y tests;
5. implementar primero el contrato semántico versionado y el dominio de descubrimiento;
6. conectar la precalificación únicamente detrás del gate.

No corresponde todavía hacer commit, push ni modificar código sin aprobación explícita.
