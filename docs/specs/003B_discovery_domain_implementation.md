# SPEC-003B — Implementación del dominio humano de descubrimiento

**Estado:** VERIFIED
**Fecha de aprobación:** 19 de julio de 2026
**Fecha de verificación:** 19 de julio de 2026
**Baseline previa a SPEC-003B:** `115 passed`
**Baseline verificada final:** `136 passed`
**Depende de:** SPEC-002A, SPEC-003, SPEC-003A
**Desbloquea:** auditoría y cierre de SPEC-005; la UI progresiva y el piloto integral permanecen fuera de alcance

---

## 1. Propósito

Implementar dentro del repositorio actual el dominio que representa el paso de una conversación aparentemente afín a una persona que participa en un diálogo humano de descubrimiento.

El corte vertical obligatorio es:

```text
Conversation con evaluación V3
→ revisión humana
→ aprobación de contacto de descubrimiento
→ creación idempotente de DiscoveryCandidate
→ contacto y respuesta vinculados al candidato
→ diálogo humano
→ DiscoveryOutcome
→ afinidad revelada o descartada
→ invitación a precalificación
→ aceptación explícita
→ gate habilitado para SPEC-005
```

Esta especificación no vende ni convierte automáticamente. Registra y gobierna el vínculo humano mediante el cual puede revelarse una afinidad real con Inlak’ech.

---

## 2. Autoridad

Esta especificación implementa y queda subordinada a:

```text
docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md
docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md
docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md
docs/RADAR_TECHNICAL_IMPACT_AUDIT_2026-07-19.md
docs/specs/003_human_review.md
docs/specs/003A_discovery_funnel.md
docs/specs/005_qualification.md
AGENTS.md
```

Decisiones técnicas aplicables:

- `DTI-01`: usar `DiscoveryCandidate` como único objeto mínimo de persona operativa;
- `DTI-04`: aplicar migraciones versionadas;
- `DTI-05`: separar estados de conversación, descubrimiento y cualificación;
- `DTI-06`: reutilizar `EngagementEvent` con referencia al candidato;
- `DTI-07`: guardar la hipótesis inicial de arquetipo en `DiscoveryOutcome`;
- `DTI-08`: mantener el frontend actual para una especificación posterior de UI.

---

## 3. Condición de inicio

No puede pasar a `IMPLEMENTING` hasta que SPEC-002A esté `VERIFIED` y exista:

- evaluación V3 persistida;
- revisión humana basada en evidencia V3;
- infraestructura de migraciones operativa;
- fallback semántico cerrado;
- suite completa en verde.

La existencia de evaluaciones V2 no satisface este gate.

---

## 4. Alcance

Incluye:

- modelo `DiscoveryCandidate`;
- modelo `DiscoveryOutcome`;
- schemas de entrada y salida;
- estados canónicos del descubrimiento;
- módulo central de transiciones;
- decisión humana `APPROVE_DISCOVERY_CONTACT`;
- creación idempotente del candidato;
- migración de `EngagementEvent` para vincular candidato;
- migración de `QualificationRecord` para trazabilidad futura;
- registro de contacto y respuesta sobre el candidato;
- resultado humano del diálogo;
- afinidad revelada;
- hipótesis de arquetipo posterior al diálogo;
- invitación y aceptación de precalificación;
- gate backend que bloquea precalificación prematura;
- compatibilidad de lectura histórica;
- pruebas focales, de integración y regresión.

---

## 5. Fuera de alcance

No incluye:

- evaluación semántica V3, que pertenece a SPEC-002A;
- modificación de los campos comerciales del cuestionario;
- cambio de umbrales económicos;
- integración real con Relaticle;
- portal del fundador;
- reserva, firma o pago;
- automatización de contacto;
- resolución global de identidades entre plataformas;
- creación de tablas separadas `Person`, `Contact`, `Lead` o `Profile`;
- historial múltiple de hipótesis de arquetipo;
- nuevo frontend;
- rediseño visual completo;
- RAG, chatbot o herramientas semánticas externas.

La interfaz progresiva completa deberá tratarse en una especificación posterior. En este corte puede agregarse únicamente la superficie mínima necesaria para probar el dominio, si resulta indispensable para el criterio extremo a extremo.

---

## 6. Principio de propiedad de la verdad

| Verdad | Objeto responsable |
|---|---|
| Qué se publicó | `Conversation` |
| Qué interpretó RADAR | `ConversationAssessmentV3` |
| Qué persona fue aprobada para diálogo | `DiscoveryCandidate` |
| Qué contacto y respuesta ocurrieron | `EngagementEvent` vinculado al candidato |
| Qué afinidad se reveló | `DiscoveryOutcome` registrado por humano |
| Qué información comercial declaró | `QualificationRecord` |
| Qué puede transferirse | `CRMTransferPayload` futuro |

Una tabla no debe apropiarse de estados que pertenecen a otra.

---

## 7. Objeto `DiscoveryCandidate`

### 7.1. Significado

Representa a la persona vinculada con una conversación pública que un humano aprobó para un contacto de descubrimiento.

No es un lead.

No implica afinidad confirmada.

No implica consentimiento para precalificación.

### 7.2. Campos mínimos

```text
id
origin_conversation_id
public_name
public_identity_reference
public_profile_url
authorized_contact
discovery_state
created_by
created_at
updated_at
```

Restricciones:

- `origin_conversation_id` es obligatorio;
- en el primer corte existe como máximo un candidato por conversación de origen;
- `public_name` puede ser nulo si la plataforma no lo informa;
- `public_identity_reference` conserva el identificador público de plataforma cuando existe;
- `authorized_contact` permanece nulo hasta que exista una vía legítima y utilizable;
- `created_by` identifica a la persona responsable de aprobar el caso;
- crear el mismo candidato dos veces debe devolver el registro existente, no duplicarlo.

No resolver automáticamente que dos identidades de plataformas distintas pertenecen a la misma persona.

---

## 8. Estados del descubrimiento

Enum canónico:

```text
DISCOVERY_CANDIDATE
DISCOVERY_APPROACH_APPROVED
DISCOVERY_CONTACTED
DISCOVERY_REPLIED
DISCOVERY_DIALOGUE_ACTIVE
AFFINITY_REVEALED
AFFINITY_NOT_CONFIRMED
DISCOVERY_CLOSED
PREQUALIFICATION_INVITED
PREQUALIFICATION_ACCEPTED
DO_NOT_CONTACT
```

### 8.1. Significado

- `DISCOVERY_CANDIDATE`: persona creada a partir de revisión humana;
- `DISCOVERY_APPROACH_APPROVED`: mensaje o aproximación aprobados;
- `DISCOVERY_CONTACTED`: existe evidencia del contacto;
- `DISCOVERY_REPLIED`: existe respuesta verificable;
- `DISCOVERY_DIALOGUE_ACTIVE`: hay intercambio humano de descubrimiento;
- `AFFINITY_REVEALED`: un humano registró afinidad parcial o clara;
- `AFFINITY_NOT_CONFIRMED`: el diálogo no confirmó afinidad suficiente;
- `DISCOVERY_CLOSED`: caso cerrado sin continuidad;
- `PREQUALIFICATION_INVITED`: se ofreció continuar hacia el cuestionario;
- `PREQUALIFICATION_ACCEPTED`: la persona aceptó y consintió esa instancia;
- `DO_NOT_CONTACT`: existe decisión explícita de no continuar contacto.

### 8.2. Transiciones permitidas

```text
DISCOVERY_CANDIDATE
→ DISCOVERY_APPROACH_APPROVED
→ DISCOVERY_CONTACTED
→ DISCOVERY_REPLIED
→ DISCOVERY_DIALOGUE_ACTIVE
→ AFFINITY_REVEALED
→ PREQUALIFICATION_INVITED
→ PREQUALIFICATION_ACCEPTED
```

Ramas válidas:

```text
DISCOVERY_CANDIDATE → DO_NOT_CONTACT
DISCOVERY_APPROACH_APPROVED → DO_NOT_CONTACT
DISCOVERY_CONTACTED → DO_NOT_CONTACT
DISCOVERY_REPLIED → AFFINITY_NOT_CONFIRMED
DISCOVERY_DIALOGUE_ACTIVE → AFFINITY_NOT_CONFIRMED
AFFINITY_NOT_CONFIRMED → DISCOVERY_CLOSED
AFFINITY_REVEALED → DISCOVERY_CLOSED
PREQUALIFICATION_INVITED → DISCOVERY_CLOSED
```

No permitir saltos que omitan evidencia obligatoria.

---

## 9. Estado de la conversación

Los estados nuevos de contacto o cualificación no deben escribirse en `Conversation.status`.

Para escritura nueva, el ciclo de conversación queda limitado conceptualmente a:

```text
DETECTED
ASSESSED
REVIEW_PENDING
OBSERVING
REVIEWED
DISCARDED
```

Los valores históricos como `CONTACTED`, `REPLIED`, `NURTURING` o `QUALIFIED` se conservan para lectura y migración, pero dejan de ser la fuente de verdad del nuevo flujo.

La revisión aprobatoria puede marcar la conversación como `REVIEWED`; el estado operativo posterior pertenece al candidato.

---

## 10. Revisión humana

### 10.1. Decisión nueva

Agregar:

```text
APPROVE_DISCOVERY_CONTACT
```

La decisión debe exigir:

- conversación existente;
- evaluación V3 `COMPLETED`;
- revisión humana;
- mensaje o enfoque editable cuando se aprueba contacto;
- identidad del revisor;
- notas opcionales.

### 10.2. Efecto transaccional

La aprobación debe:

1. guardar `ReviewDecision`;
2. crear idempotentemente `DiscoveryCandidate`;
3. asociarlo a la conversación de origen;
4. establecer el estado inicial correcto;
5. no enviar mensajes;
6. no crear precalificación;
7. no transferir al CRM.

### 10.3. Compatibilidad

`APPROVE_APPROACH` histórico permanece legible.

No reescribir decisiones existentes.

Las nuevas capacidades deben usar `APPROVE_DISCOVERY_CONTACT`.

---

## 11. `EngagementEvent`

### 11.1. Evolución

Agregar:

```text
discovery_candidate_id nullable
```

Conservar:

```text
conversation_id
```

para trazabilidad de origen y compatibilidad histórica.

### 11.2. Regla de escritura nueva

Los nuevos eventos humanos de contacto y respuesta requieren `discovery_candidate_id`.

Eventos mínimos:

```text
CONTACTED
REPLIED
NO_RESPONSE
DO_NOT_CONTACT
```

Puede agregarse:

```text
DIALOGUE_NOTE
```

solo si resulta necesario para registrar una síntesis humana sin guardar un transcript completo.

### 11.3. Validaciones

- `CONTACTED` requiere canal, texto enviado y fecha;
- `REPLIED` requiere respuesta y fecha;
- todo evento debe corresponder al candidato y a su conversación de origen;
- un evento repetido idéntico no debe provocar una transición inválida;
- registrar contacto requiere aprobación previa;
- registrar respuesta no autoriza precalificación.

---

## 12. Objeto `DiscoveryOutcome`

### 12.1. Significado

Registra el resultado humano del diálogo de descubrimiento.

No puede ser producido autónomamente por el LLM.

El LLM puede ayudar a resumir texto, pero una persona confirma cada dato operativo.

### 12.2. Campos mínimos

```text
id
discovery_candidate_id
sympathy_revealed
revealed_affinity_level
revealed_affinity_domains
motivation_declared
questions_or_interests
objections
wants_to_continue
consent_to_prequalification
consent_recorded_at
human_notes
archetype_hypothesis
archetype_evidence
archetype_confidence
archetype_human_confirmed
recorded_by
recorded_at
updated_at
```

### 12.3. Enums

```text
sympathy_revealed:
NO
UNCLEAR
YES

revealed_affinity_level:
NONE
PARTIAL
CLEAR
```

Arquetipos posibles:

```text
PIONERO_VISIONARIO
SEMBRADOR_PACIENTE
ARTIFICE_REGENERATIVO
```

### 12.4. Reglas

- un candidato posee como máximo un outcome vigente en el primer corte;
- `recorded_by` es obligatorio;
- `revealed_affinity_level` surge del diálogo humano;
- `consent_to_prequalification=true` exige `wants_to_continue=true`;
- el consentimiento exige `consent_recorded_at`;
- `PREQUALIFICATION_ACCEPTED` exige afinidad `PARTIAL` o `CLEAR`;
- un arquetipo no puede utilizarse operativamente sin `archetype_human_confirmed=true`;
- un arquetipo confirmado exige evidencia no vacía;
- no copiar `probable_archetype` desde V2;
- no inferir capital, plazo o capacidad.

---

## 13. Invitación y aceptación de precalificación

### 13.1. Invitación

Solo puede pasar a `PREQUALIFICATION_INVITED` cuando:

```text
DiscoveryOutcome existe
+
revealed_affinity_level en PARTIAL o CLEAR
+
wants_to_continue = true
```

La invitación es una acción humana registrada.

### 13.2. Aceptación

Solo puede pasar a `PREQUALIFICATION_ACCEPTED` cuando:

```text
estado = PREQUALIFICATION_INVITED
+
consent_to_prequalification = true
+
consent_recorded_at existe
```

Aceptar recibir información no equivale necesariamente a aceptar precalificación.

Una respuesta cordial no equivale a consentimiento.

---

## 14. Gate backend hacia SPEC-005

La creación de una cualificación debe exigir:

```text
DiscoveryCandidate existente
+
DiscoveryOutcome existente
+
revealed_affinity_level en PARTIAL o CLEAR
+
wants_to_continue = true
+
consent_to_prequalification = true
+
discovery_state = PREQUALIFICATION_ACCEPTED
```

Si falta cualquiera de esas condiciones:

```text
HTTP 409
```

con un error explícito y no ambiguo.

El endpoint actual basado únicamente en `conversation.status = REPLIED` debe dejar de habilitar escritura.

---

## 15. Evolución de `QualificationRecord`

Agregar mediante migración:

```text
discovery_candidate_id nullable
discovery_outcome_id nullable
```

Regla para registros nuevos:

- ambas referencias son obligatorias a nivel de aplicación;
- `conversation_id` puede conservarse para trazabilidad y compatibilidad;
- registros históricos pueden mantener valores nulos;
- no crear una cualificación desde una conversación sin candidato.

La modificación del contrato comercial interno de `qualify_contact()` debe limitarse a desacoplarlo del workflow global.

---

## 16. Desacople de `qualify_contact()`

### 16.1. Responsabilidad futura

`qualify_contact()` debe calcular:

```text
traffic_light
qualification_status
qualification_action
recommended_path
crm_transfer_allowed
calendar_access_allowed
reasons
missing_information
```

No debe decidir:

```text
Conversation.status
DiscoveryCandidate.discovery_state
DO_NOT_CONTACT del embudo de descubrimiento
```

### 16.2. Workflow

Un servicio central de transiciones aplicará el estado posterior según:

- resultado de cualificación;
- consentimiento comercial;
- reglas de CRM;
- evidencia disponible.

La lógica vigente de capital, horizonte, motivación, perfil y camino debe preservarse salvo contradicción documentada.

---

## 17. Consentimientos separados

Primer corte obligatorio:

### Consentimiento 1

```text
consent_to_prequalification
```

Se registra en `DiscoveryOutcome` y habilita el cuestionario.

### Consentimiento 2

```text
consent_to_commercial_followup
```

Se registra con la cualificación y gobierna calendario, seguimiento comercial y futura transferencia.

No asumir que el primero implica el segundo.

El nombre legado `consent_to_continue` puede mantenerse transitoriamente en compatibilidad, pero debe documentarse y mapearse de manera inequívoca al consentimiento comercial, no al consentimiento de descubrimiento.

---

## 18. Módulo de workflow

Crear:

```text
app/workflow.py
```

Responsabilidades:

- enums canónicos;
- transiciones permitidas;
- validación de precondiciones;
- errores tipados;
- aplicación idempotente;
- separación entre estado de conversación, descubrimiento y cualificación.

No usar un framework externo.

No dispersar asignaciones directas de estados en rutas.

Las rutas deben delegar al workflow.

---

## 19. API objetivo

### 19.1. Candidatos

```text
GET  /api/discovery-candidates
GET  /api/discovery-candidates/{candidate_id}
```

### 19.2. Revisión y creación

La ruta de revisión existente puede evolucionar, pero la decisión `APPROVE_DISCOVERY_CONTACT` debe devolver o enlazar el candidato creado.

### 19.3. Eventos

```text
POST /api/discovery-candidates/{candidate_id}/engagement-events
GET  /api/discovery-candidates/{candidate_id}/engagement-events
```

### 19.4. Outcome

```text
PUT /api/discovery-candidates/{candidate_id}/outcome
GET /api/discovery-candidates/{candidate_id}/outcome
```

El `PUT` representa el outcome vigente e idempotente del primer corte.

### 19.5. Precalificación

```text
POST /api/discovery-candidates/{candidate_id}/prequalification-invitation
POST /api/discovery-candidates/{candidate_id}/prequalification-acceptance
POST /api/discovery-candidates/{candidate_id}/qualifications
```

El endpoint legado:

```text
POST /api/conversations/{conversation_id}/qualifications
```

puede conservarse temporalmente, pero debe resolver un candidato válido y aplicar exactamente el mismo gate. No puede seguir aceptando `REPLIED` como condición suficiente.

---

## 20. Migraciones

La infraestructura creada en SPEC-002A debe utilizarse para:

1. crear `discovery_candidates`;
2. crear `discovery_outcomes`;
3. agregar `discovery_candidate_id` nullable a `engagement_events`;
4. agregar `discovery_candidate_id` y `discovery_outcome_id` nullable a `qualification_records`;
5. crear índices y restricciones;
6. preservar datos históricos.

### 20.1. Migración histórica segura

Puede crearse un candidato legado únicamente cuando exista evidencia persistida de:

- revisión aprobatoria; o
- contacto; o
- respuesta.

Mapeo permitido:

```text
APPROACH_APPROVED
→ candidato legado sin outcome

CONTACTED
→ candidato legado en DISCOVERY_CONTACTED

REPLIED
→ candidato legado en DISCOVERY_REPLIED
```

No migrar automáticamente:

- afinidad revelada;
- consentimiento;
- arquetipo humano;
- voluntad de continuar;
- cualificación nueva.

La migración debe ser idempotente.

---

## 21. Compatibilidad

Debe preservarse:

- lectura de `ReviewDecision` histórico;
- lectura de `EngagementEvent` histórico sin candidato;
- lectura de `QualificationRecord` histórico;
- `conversation_id` como trazabilidad;
- API existente durante transición breve;
- suite vigente y pruebas V3;
- SQLite local;
- PostgreSQL objetivo.

No se exige que los registros históricos alcancen automáticamente los nuevos gates.

---

## 22. Archivos de impacto esperado

Archivos nuevos probables:

```text
app/models/discovery.py
app/schemas/discovery.py
app/workflow.py
tests/test_discovery_candidate.py
tests/test_discovery_outcome.py
tests/test_workflow_transitions.py
tests/test_prequalification_gate.py
alembic/versions/*
```

Archivos existentes permitidos:

```text
app/api/routes.py
app/db/session.py
app/models/__init__.py
app/models/engagement.py
app/models/qualification.py
app/schemas/review.py
app/schemas/qualification.py
app/qualification.py
app/crm_transfer.py
tests/test_api_flow.py
tests/test_qualification.py
documentación de estado y aceptación
```

Archivos excluidos salvo justificación previa:

```text
app/semantics/llm_classifier.py
app/semantics/classifier.py
app/models/assessment_v2.py
app/models/assessment_v3.py
app/schemas/assessment_v3.py
app/discovery/last30days_adapter.py
app/integrations/relaticle.py
app/templates/dashboard.txt
app/static/radar.js.txt
app/static/radar.css.txt
```

La UI completa no pertenece a este corte.

---

## 23. Casos límite obligatorios

1. aprobación repetida de la misma conversación:
   - un solo candidato;
   - respuesta idempotente.
2. conversación sin autor identificable:
   - candidato permitido con referencia pública suficiente;
   - contacto bloqueado si no existe vía legítima.
3. contacto sin aprobación:
   - `409`.
4. respuesta sin contacto previo:
   - bloqueada salvo migración histórica explícita.
5. respuesta cordial:
   - no habilita precalificación.
6. outcome sin afinidad:
   - `AFFINITY_NOT_CONFIRMED`;
   - precalificación bloqueada.
7. afinidad parcial sin voluntad de continuar:
   - invitación bloqueada.
8. consentimiento sin fecha:
   - validación rechazada.
9. consentimiento con afinidad `NONE`:
   - aceptación bloqueada.
10. arquetipo sin evidencia:
    - no puede confirmarse.
11. arquetipo V2 existente:
    - no se copia al outcome.
12. evento histórico sin candidate ID:
    - sigue legible.
13. cualificación por endpoint legado sin gate:
    - `409`.
14. repetición de aceptación:
    - idempotente.
15. `DO_NOT_CONTACT`:
    - bloquea eventos nuevos y continuidad.

---

## 24. Pruebas obligatorias

### Modelos y schemas

- creación válida e inválida de candidato;
- unicidad por conversación de origen;
- validaciones de outcome;
- consentimiento y fecha;
- arquetipo y evidencia;
- campos históricos nullable.

### Workflow

Bloquear:

```text
DETECTED → QUALIFICATION_STARTED
DISCOVERY_CANDIDATE → DISCOVERY_REPLIED
DISCOVERY_REPLIED → PREQUALIFICATION_ACCEPTED sin outcome
AFFINITY_NOT_CONFIRMED → PREQUALIFICATION_INVITED
PREQUALIFICATION_INVITED → QUALIFICATION_STARTED sin aceptación
DO_NOT_CONTACT → DISCOVERY_CONTACTED
```

Permitir:

```text
DISCOVERY_APPROACH_APPROVED → DISCOVERY_CONTACTED
DISCOVERY_CONTACTED → DISCOVERY_REPLIED
DISCOVERY_DIALOGUE_ACTIVE → AFFINITY_REVEALED
AFFINITY_REVEALED → PREQUALIFICATION_INVITED
PREQUALIFICATION_INVITED → PREQUALIFICATION_ACCEPTED
PREQUALIFICATION_ACCEPTED → QUALIFICATION_STARTED
```

### API

- aprobación crea candidato;
- aprobación repetida no duplica;
- contacto exige candidato y aprobación;
- respuesta no habilita cuestionario;
- outcome humano persistido;
- invitación validada;
- aceptación validada;
- cualificación bloqueada sin gate;
- cualificación permitida con gate;
- endpoint legado aplica las mismas reglas.

### Migración

- tablas nuevas;
- columnas nullable;
- preservación de eventos históricos;
- creación segura de candidatos legado;
- ausencia de outcomes inventados;
- idempotencia.

### Regresión

```text
python -m pytest -q
```

Debe preservar todas las pruebas de SPEC-002A y la baseline acumulada.

---

## 25. Criterios de aceptación

La especificación pasa a `VERIFIED` cuando exista evidencia reproducible de que:

1. una aprobación humana crea un único candidato;
2. la conversación deja de ser propietaria del estado de contacto;
3. los nuevos eventos pertenecen al candidato;
4. los eventos históricos siguen legibles;
5. existe un outcome humano persistente;
6. afinidad revelada y consentimiento no son inferidos por LLM;
7. ningún arquetipo se copia desde V2;
8. la invitación exige afinidad y voluntad;
9. la aceptación exige consentimiento explícito y fecha;
10. una respuesta sola no habilita precalificación;
11. el backend devuelve `409` ante cualquier gate incompleto;
12. `qualify_contact()` queda desacoplado del estado global;
13. las cualificaciones nuevas conservan candidate ID y outcome ID;
14. la migración no destruye ni falsifica historia;
15. la suite completa pasa;
16. `git diff --check` queda limpio;
17. el checkpoint y la matriz de aceptación se actualizan.

---

## 26. Evidencia de verificación

Evidencia consolidada al cierre:

```text
HEAD_BEFORE: no registrado en este corte documental
HEAD_AFTER: no aplica — sin commit
FILES_CREATED: app/workflow.py; app/schemas/discovery.py; app/models/discovery.py; app/discovery_service.py; tests/test_discovery_candidate.py; tests/test_discovery_outcome.py; tests/test_discovery_models.py; tests/test_workflow_transitions.py; tests/test_prequalification_gate.py; alembic/versions/20260719_0003_add_discovery_domain.py
FILES_MODIFIED: app/api/routes.py; app/db/session.py; app/models/__init__.py; app/models/engagement.py; app/models/qualification.py; app/schemas/review.py; tests/conftest.py; tests/test_api_flow.py; tests/test_migrations.py; documentación de estado
MIGRATION_REVISIONS: 20260719_0003 (head)
FOCAL_TEST_COMMANDS: python -m pytest -q tests/test_discovery_candidate.py tests/test_discovery_outcome.py tests/test_workflow_transitions.py tests/test_prequalification_gate.py tests/test_discovery_models.py tests/test_migrations.py
FOCAL_TEST_RESULTS: 26 passed
FULL_TEST_COMMAND: python -m pytest -q
FULL_TEST_RESULT: 136 passed
DIFF_CHECK: PASS informado por Codex antes del cierre; sin cambios de código posteriores
COMMIT: no realizado
PUSH: no realizado
KNOWN_GAPS: UI progresiva, Relaticle y piloto quedan fuera de SPEC-003B; radar_state permanece como salida histórica de compatibilidad sin gobernar Conversation ni DiscoveryCandidate
```

---

## 27. Orden de implementación

Después de verificar SPEC-002A:

```text
1. tablas y migraciones del dominio
2. schemas
3. workflow y transiciones
4. revisión que crea candidato
5. eventos vinculados
6. DiscoveryOutcome
7. invitación y aceptación
8. gate de precalificación
9. desacople de qualify_contact
10. compatibilidad histórica
11. pruebas focales
12. regresión completa
13. checkpoint documental
```

La UI progresiva completa y la integración real con Relaticle quedan fuera de esta implementación.
