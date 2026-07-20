# Contrato de Lista 1 — Candidatos por Afinidad Semántica Presuntiva

**Versión:** `1.0.0`
**Estado:** `APPROVED`
**Aprobado para implementación:** Sí  
**Fecha de aprobación:** 20 de julio de 2026  
**Alcance autorizado:** Lista 1 — candidatos por afinidad semántica presuntiva  
**Fases no autorizadas:** corroboración, mensajería, consentimiento, embudo clasificatorio, CRM y Relaticle
**Documento rector:** `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`
**Contrato técnico de referencia:** `app.schemas.assessment_v3.ConversationAssessmentV3Result`
**Modelo existente de evaluación:** `app.models.assessment_v3.ConversationAssessmentV3`
**Depende de:** SPEC-002A, SPEC-001

---

## 1. Propósito

Construir la primera lista de RADAR: una relación de usuarios públicos que participaron en conversaciones donde se detectó afinidad semántica aparente con Inlak'ech.

Esta lista no es un lead list. No autoriza contacto. No inicia precalificación. No transfiere a Relaticle.

El principio rector es:

```text
La afinidad inicial pertenece a la conversación.
El usuario público se convierte en candidato presuntivo
porque participó en una conversación con afinidad aparente.
No es todavía un lead.
```

---

## 2. Autoridad

Este contrato implementa y queda subordinado a:

```text
docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md
docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md
docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md
docs/specs/002_affinity_classification.md
docs/specs/002A_conversation_assessment_v3.md
docs/SEMANTIC_SKILL_CONTRACT_V1.md
AGENTS.md
```

Decisiones técnicas aplicables:

- `DTI-05`: la evaluación no controla estados de descubrimiento o cualificación.
- Regla LLM/RADAR/humano: el LLM interpreta, RADAR valida, la persona decide.

Ante una contradicción, prevalece el documento maestro de arquitectura.

---

## 3. Fuera de alcance (de esta especificación)

No incluye:

- corroboración humana de afinidad;
- redacción o envío de mensajes;
- consentimiento informado;
- embudo de descubrimiento (SPEC-003A);
- precalificación (SPEC-005);
- transferencia a Relaticle (SPEC-004);
- asignación de arquetipos;
- inferencia de identidad entre plataformas;
- scoring léxico determinístico;
- regex para decidir afinidad;
- Fase 2 del embudo de candidatos.

---

## 4. Entidades

### 4.1. Conversation

Entidad existente en `app.models.conversation.Conversation`. Tabla `conversations`.

Campos relevantes para este contrato:

```text
id
source           # plataforma de origen (ej: reddit, twitter, youtube)
external_id      # id del hilo o publicación en la plataforma
conversation_url # url directa a la conversación pública
author_name      # nombre público del autor del hilo
title
text
published_at
status
```

### 4.2. PublicActor — nueva entidad

Representa una identidad pública en una plataforma específica.

```text
id
platform                   # misma semántica que Conversation.source
platform_actor_id          # identificador público estable en esa plataforma
public_username            # nombre de usuario visible
display_name               # nombre mostrado (opcional)
public_profile_url         # url directa al perfil público
first_seen_at              # cuándo se detectó por primera vez
last_seen_at               # cuándo se vio por última vez
actor_metadata             # JSON con datos públicos adicionales no inferidos
created_at
updated_at

UniqueConstraint(platform, platform_actor_id)
```

`public_actor_id` se construye como `"{platform}:{platform_actor_id}"`.

### 4.3. ConversationParticipant — nueva entidad

Relaciona un actor público con una conversación en la que participó.

```text
id
public_actor_id            # FK → PublicActor
conversation_id            # FK → Conversation
role                       # "author" | "commenter" | "replier"
participant_public_username # username en el momento de la conversación
participant_display_name    # display name en el momento de la conversación
first_seen_at              # timestamp del primer mensaje visible
is_author                  # bool, atajo para role == "author"
created_at

UniqueConstraint(public_actor_id, conversation_id)
```

Un actor puede participar en muchas conversaciones. Una conversación puede tener muchos participantes. La misma persona física en distintas plataformas produce actores distintos.

### 4.4. SemanticAssessmentV3

Entidad existente en `app.models.assessment_v3.ConversationAssessmentV3`. Tabla `conversation_assessments_v3`.

Campos relevantes para la creación de candidatos:

```text
id
conversation_id
assessment_status          # COMPLETED | SEMANTIC_ASSESSMENT_UNAVAILABLE | ...
apparent_affinity          # NONE | POSSIBLE | CLEAR
apparent_intention         # NONE | THEMATIC_SYMPATHY | EXPLORATION | ACTION_ORIENTED
evidence_fragments         # lista de citas literales validadas
false_positive_risk        # LOW | MEDIUM | HIGH
review_priority            # entero 0–100
recommended_review_action  # DISCARD | OBSERVE | REVIEW
semantic_engine
model_name
provisional
human_review_required
created_at
```

### 4.5. PresumptiveCandidate — nueva entidad

Registro de que un actor público es candidato presuntivo por su participación en una conversación con afinidad aparente.

```text
id                          # PK
public_actor_id             # FK → PublicActor
conversation_id             # FK → Conversation
assessment_id               # FK → ConversationAssessmentV3
platform                    # denormalizado desde actor
public_username             # denormalizado desde participant
display_name                # denormalizado desde participant
public_profile_url          # denormalizado desde actor
source_url                  # conversation_url denormalizado
apparent_affinity           # copia del valor de la evaluación
apparent_intention          # copia del valor de la evaluación
evidence_fragments          # copia de las citas evaluadas
false_positive_risk         # copia del riesgo
review_priority             # copia de la prioridad calculada
status                      # estado del candidato (enum abajo)
skill_version               # versión del skill semántico usado
model_name                  # modelo que produjo la evaluación
created_at
updated_at

UniqueConstraint(public_actor_id, conversation_id, assessment_id)
```

Se permite que un mismo actor tenga múltiples candidatos (uno por conversación distinta). No se permite duplicar la misma combinación actor + conversación + assessment.

---

## 5. Modelo de estados de PresumptiveCandidate

```text
DISCOVERED                 # creado automáticamente tras evaluación válida
INTERPRETATION_PENDING     # pendiente de interpretación humana
PRESUMPTIVE_CANDIDATE      # interpretación humana confirma candidatura
OBSERVED                   # afinidad ambigua, se mantiene en observación
DISCARDED                  # descartado por revisión humana
INTERPRETATION_FAILED      # el humano no pudo interpretar (información insuficiente)
```

Transiciones permitidas:

```text
DISCOVERED → INTERPRETATION_PENDING (automática si review_action == REVIEW)
DISCOVERED → OBSERVED              (automática si review_action == OBSERVE)
DISCOVERED → DISCARDED             (automática si review_action == DISCARD, no ocurre por regla de ingreso)
INTERPRETATION_PENDING → PRESUMPTIVE_CANDIDATE (humano confirma)
INTERPRETATION_PENDING → OBSERVED               (humano considera insuficiente pero relevante)
INTERPRETATION_PENDING → DISCARDED              (humano descarta)
INTERPRETATION_PENDING → INTERPRETATION_FAILED  (humano no pudo interpretar)
OBSERVED → INTERPRETATION_PENDING (humano reconsidera)
OBSERVED → DISCARDED              (humano descarta)
```

Ninguna transición puede promover a lead, iniciar precalificación o autorizar contacto.

---

## 6. Regla de ingreso

**Crear PresumptiveCandidate** solo cuando se cumplan **todas** estas condiciones:

```text
assessment_status == COMPLETED
apparent_affinity in [POSSIBLE, CLEAR]
evidence_fragments no vacío
recommended_review_action in [OBSERVE, REVIEW]
```

Al crear:

- Si `recommended_review_action == REVIEW` → estado inicial `DISCOVERED` y se promueve automáticamente a `INTERPRETATION_PENDING`.
- Si `recommended_review_action == OBSERVE` → estado inicial `OBSERVED`.

El actor se crea si no existe (upsert por `platform + platform_actor_id`). El participante se crea si no existe (upsert por `public_actor_id + conversation_id`).

---

## 7. Reglas de exclusión

**No crear PresumptiveCandidate** cuando:

```text
apparent_affinity == NONE
evidence_fragments vacía o inválida
assessment_status != COMPLETED
recommended_review_action == DISCARD
conversación duplicada para mismo actor + assessment
contenido técnicamente insuficiente (texto vacío, ruido puro)
```

Un caso `DISCARD` no crea candidato incluso si algún otro campo parece positivo. La evaluación ya determinó que no amerita seguimiento.

---

## 8. Reglas de identidad pública

### 8.1. Identificador único

```text
public_actor_id = "{platform}:{platform_actor_id}"
```

Ejemplos:

```text
reddit:t3_h9a2b3c4d5
twitter:1234567890
youtube:UC_x5XG1OV2P6uF5KFMl3mg
```

### 8.2. Prohibiciones expresas

El sistema no puede inferir ni almacenar en `PublicActor` o `PresumptiveCandidate`:

```text
nombre legal
correo electrónico
teléfono
domicilio
capacidad económica
identidad entre plataformas (misma persona en Reddit y Twitter)
arquetipo
lead status
```

El campo `actor_metadata` en `PublicActor` solo puede contener datos explícitamente públicos y observables (ej: fecha de creación de la cuenta, karma público, bio pública). No puede contener inferencias.

### 8.3. Separación entre plataformas

Un actor en Reddit y otro en Twitter con el mismo nombre de usuario son dos `PublicActor` distintos. No existe reconciliación automática ni cruce de identidades.

---

## 9. Contrato de UI mínimo

### 9.1. Columnas de la lista

```text
Usuario        → public_username + display_name
Plataforma     → platform
Tema real      → real_topic desde la evaluación
Afinidad       → apparent_affinity
Intención      → apparent_intention
Evidencia      → evidence_fragments (primer fragmento o resumen)
Riesgo         → false_positive_risk
Prioridad      → review_priority
Estado         → status del candidato
```

### 9.2. Acciones disponibles

```text
Abrir detalle          → vista completa del candidato con evaluación asociada
Abrir fuente original  → source_url (conversación pública)
Observar               → cambia estado a OBSERVED (solo si está en INTERPRETATION_PENDING)
Descartar              → cambia estado a DISCARDED (solo si está en INTERPRETATION_PENDING o OBSERVED)
```

### 9.3. Prohibiciones de UI

La lista no contiene:

```text
botón "Contactar"
botón "Precalificar"
botón "Transferir a Relaticle"
indicador de lead
score comercial
arquetipo
```

---

## 10. Flujo de creación

```text
Conversation real persistida
→ evaluación V3 ejecutada
→ assessment_status == COMPLETED
→ apparent_affinity in [POSSIBLE, CLEAR]
→ evidence_fragments válidos
→ recommended_review_action in [OBSERVE, REVIEW]

→ para cada ConversationParticipant:
    → upsert PublicActor
    → upsert ConversationParticipant
    → crear PresumptiveCandidate
```

Un PresumptiveCandidate se crea **por cada participante** de la conversación, no solo el autor. Esto permite descubrir actores relevantes que comentaron con afinidad aunque el hilo original sea neutral.

---

## 11. Criterios de aceptación

| # | Criterio | Condición |
|---|----------|-----------|
| 1 | **Caso positivo crea candidato** | CLEAR + evidence válida + REVIEW → PresumptiveCandidate creado |
| 2 | **Caso ambiguo crea candidato observado** | POSSIBLE + OBSERVE → PresumptiveCandidate en estado OBSERVED |
| 3 | **Caso fútbol no crea candidato** | NONE + cualquier evidencia → sin candidato |
| 4 | **Duplicado no crea segundo candidato** | Mismo actor + conversación + assessment → único registro |
| 5 | **Un actor puede participar en varias conversaciones** | Mismo actor, distintas conversaciones → múltiples candidatos |
| 6 | **Identidad pública no se mezcla entre plataformas** | Mismo username, distinta plataforma → actores distintos |
| 7 | **Lista usa datos reales** | Los datos provienen de evaluaciones reales, no simulados |
| 8 | **Pendientes y fallidas no aparecen como candidatos activos** | assessment_status != COMPLETED → sin candidato |
| 9 | **No se crea lead** | No hay tabla lead, no hay flag is_lead |
| 10 | **No se envía mensaje** | Ninguna acción externa de comunicación |

---

## 12. Archivos de impacto esperado

Archivos nuevos:

```text
app/models/public_actor.py
app/models/conversation_participant.py
app/models/presumptive_candidate.py
app/schemas/public_actor.py
app/schemas/conversation_participant.py
app/schemas/presumptive_candidate.py
tests/test_presumptive_candidate_creation.py
tests/test_presumptive_candidate_rules.py
```

Archivos existentes permitidos:

```text
app/models/__init__.py
app/schemas/__init__.py
app/db/session.py
app/semantics/conversation_assessment_v3.py (lectura de evaluación para crear candidato)
documentación de estado y aceptación
```

No modificar en este corte:

```text
app/models/qualification.py
app/models/engagement.py
app/models/review.py
app/qualification.py
app/crm_transfer.py
app/integrations/relaticle.py
app/templates/dashboard.txt
app/static/radar.js.txt
app/static/radar.css.txt
app/htmx_ui.py
tests/test_* no relacionados con candidatos
```

---

## 13. Decisiones técnicas

| Decisión | Opción elegida | Alternativa descartada |
|----------|---------------|----------------------|
| public_actor_id | `{platform}:{platform_actor_id}` | UUID propio — no aporta trazabilidad |
| Desnormalización | Copiar campos de evaluación al candidato | JOIN siempre — lectura más costosa sin beneficio |
| Upsert de actor | Upsert por unique constraint | Crear siempre — genera duplicados |
| Un candidato por participante | Sí, no solo el autor | Solo autor — pierde comentaristas relevantes |
| Estado inicial según review_action | DISCOVERED → INTERPRETATION_PENDING u OBSERVED | Un solo estado "nuevo" — obliga a revisar todo |

---

## 14. Riesgos identificados

| Riesgo | Mitigación |
|--------|-----------|
| Volumen alto de candidatos si una conversación viral tiene muchos participantes | Limitar a participantes con intervención semánticamente relevante (futuro) |
| Un actor malicioso crea cuentas para aparecer en la lista | La evaluación es sobre la conversación, no sobre la persona; el humano decide |
| Datos públicos eliminados después de la captura | La evaluación se conserva; el source_url puede quedar inaccesible pero la evidencia persiste |
| Misma persona en dos plataformas tratada como dos actores | Es intencional por diseño (prohibición de inferir identidad entre plataformas) |

---

## 15. Pruebas obligatorias (para fase de implementación)

### Focales

- creación de candidato con CLEAR + REVIEW;
- creación de candidato con POSSIBLE + OBSERVE;
- exclusión por NONE;
- exclusión por assessment_status != COMPLETED;
- exclusión por evidence vacía;
- exclusión por DISCARD;
- exclusión por duplicado exacto;
- un actor en dos conversaciones produce dos candidatos;
- mismo username en distintas plataformas produce actores distintos;
- upsert de PublicActor no duplica;
- no creación de lead;
- no envío de mensaje.

### Persistencia

- crear y recuperar candidato;
- transición de estados;
- candidate único por unique constraint;
- cascada: borrar evaluación no borra candidato (diseño: no hay cascade automático).

---

## 16. Formato de cierre técnico (para implementación)

```text
VERDICT: PENDING
ENTITY_MODEL: PublicActor, ConversationParticipant, PresumptiveCandidate
STATE_MODEL: DISCOVERED → INTERPRETATION_PENDING | OBSERVED → PRESUMPTIVE_CANDIDATE | DISCARDED | INTERPRETATION_FAILED
ENTRY_RULES: assessment_status == COMPLETED AND apparent_affinity in [POSSIBLE, CLEAR] AND evidence_fragments NOT empty AND recommended_review_action in [OBSERVE, REVIEW]
EXCLUSION_RULES: apparent_affinity == NONE OR assessment_status != COMPLETED OR evidence empty OR DISCARD OR duplicate
PUBLIC_IDENTITY_RULES: public_actor_id = "{platform}:{platform_actor_id}" — no inferir nombre legal, correo, teléfono, domicilio, capacidad, identidad entre plataformas, arquetipo ni lead status
UI_CONTRACT: columnas = usuario, plataforma, tema real, afinidad, intención, evidencia, riesgo, prioridad, estado; acciones = abrir detalle, abrir fuente, observar, descartar
ACCEPTANCE_CASES: 10 criterios definidos en sección 11
CODEX_SCOPE: modelos, schemas, lógica de creación, pruebas focales; NO modificar qualification, engagement, review, crm, relaticle, ui
FILES_CREATED: docs/PRESUMPTIVE_CANDIDATE_LIST_CONTRACT_V1.md
GIT_STATUS: unmodified — solo archivo nuevo no commiteado
```
