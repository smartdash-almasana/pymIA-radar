# RADAR — Auditoría técnica de impacto de la arquitectura de descubrimiento

**Fecha:** 19 de julio de 2026
**Estado:** AUDITORÍA DOCUMENTAL — NO IMPLEMENTA CÓDIGO
**Repositorio:** `inlakech-radar`
**Baseline informada por el usuario:** `88 passed`
**Documento rector:** `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`

---

## 1. Veredicto

```text
VIABILIDAD EN EL REPO ACTUAL: SÍ
REPOSITORIO NUEVO: NO
REESCRITURA TOTAL: NO
NUEVA PLATAFORMA: NO
REFORMA DE DOMINIO: SÍ
MIGRACIÓN DE DATOS: NECESARIA
RIESGO GLOBAL: MEDIO, CONTROLABLE POR ETAPAS
```

El repositorio actual contiene los componentes necesarios para evolucionar RADAR:

- descubrimiento;
- persistencia de conversaciones;
- interpretación determinística y LLM;
- revisión humana;
- registro de contacto y respuesta;
- precalificación;
- frontera con Relaticle;
- interfaz web;
- suite de pruebas.

La arquitectura acordada puede implementarse dentro del mismo monolito FastAPI. El cambio no consiste en agregar infraestructura, sino en corregir el dominio y las fronteras entre:

```text
conversación
persona candidata
embudo de descubrimiento
precalificación
lead comercial
```

---

## 2. Alcance de esta auditoría

Se inspeccionaron los contratos y acoplamientos principales de:

```text
app/api/routes.py
app/db/session.py
app/main.py
app/qualification.py
app/crm_transfer.py
app/models/
app/schemas/
app/semantics/
app/discovery/
app/templates/dashboard.txt
app/static/radar.js.txt
tests/
config/inlakech_profile.yaml
config/semantic_calibration_corpus.v1.json
pyproject.toml
```

No se modificó código, configuración, pruebas, datos ni base de datos.

---

## 3. Arquitectura actual comprobada

### 3.1. Flujo real vigente

```text
Conversation
→ AssessmentResult / SemanticAssessmentV2
→ ReviewDecision
→ EngagementEvent(CONTACTED)
→ EngagementEvent(REPLIED)
→ QualificationRecord
→ CRMTransferPayload
```

### 3.2. Estado global vigente

El estado se guarda en:

```text
Conversation.status
```

Las rutas lo mutan directamente mediante strings:

```text
DETECTED / detected
REVIEW_PENDING
APPROACH_APPROVED
CONTACTED
REPLIED
OBSERVING
NURTURING
QUALIFIED
PRIORITY_QUALIFIED
DISCARDED
DO_NOT_CONTACT
```

### 3.3. Propiedad actual de los registros

Todos los objetos operativos principales dependen directamente de `conversation_id`:

- `SemanticAssessmentV2`;
- `ReviewDecision`;
- `EngagementEvent`;
- `QualificationRecord`.

No existe un objeto persistente propio para representar a la persona candidata ni el caso humano de descubrimiento.

---

## 4. Hallazgo estructural principal

### H-01 — `Conversation.status` mezcla tres dominios

**Severidad:** CRÍTICA

Actualmente una conversación puede pasar por estados que pertenecen a objetos diferentes:

```text
REVIEW_PENDING          → estado de revisión de una conversación
CONTACTED / REPLIED     → estado de relación con una persona
QUALIFIED               → estado comercial de un lead
```

Esto genera una identidad de dominio incorrecta:

```text
conversación = persona = lead
```

La arquitectura objetivo exige separar:

```text
Conversation
→ conserva el hallazgo público y su evaluación

DiscoveryCandidate
→ representa a la persona aprobada para descubrimiento

DiscoveryOutcome
→ registra el resultado humano del diálogo

QualificationRecord
→ representa la precalificación consentida
```

### Decisión recomendada

`Conversation.status` debe quedar limitado al ciclo de la conversación:

```text
DETECTED
ASSESSED
REVIEW_PENDING
OBSERVING
DISCARDED
```

Los estados de contacto, descubrimiento y precalificación deben pertenecer al candidato o al registro correspondiente, no a la conversación.

---

## 5. Hallazgos por dominio

### H-02 — No existe el objeto persona/candidato

**Severidad:** CRÍTICA

`Conversation` solo conserva:

```text
author_name
source
external_id
conversation_url
```

No existe una entidad que pueda registrar de manera coherente:

- identidad pública;
- vía legítima de contacto;
- contacto autorizado;
- conversación de origen;
- estado de descubrimiento;
- voluntad de continuar;
- consentimiento;
- relación con posteriores conversaciones.

#### Recomendación mínima

Agregar un único objeto de persona operativa:

```text
DiscoveryCandidate
```

No crear simultáneamente `Person`, `Lead`, `Contact` y `Candidate` como tablas separadas. Eso sería sobrediseño.

`DiscoveryCandidate` debe representar a la persona únicamente desde que la revisión humana aprueba el contacto de descubrimiento.

Campos mínimos propuestos:

```text
id
origin_conversation_id
public_name
public_identity_reference
public_profile_url
authorized_contact
state
created_by
created_at
updated_at
```

La resolución de una misma persona en varias plataformas puede posponerse hasta existir evidencia real de necesidad. El primer corte puede conservar una conversación de origen por candidato.

---

### H-03 — La evaluación pública diagnostica demasiado

**Severidad:** CRÍTICA

`AssessmentResult`, `LLMAssessmentDraft`, `SemanticAssessmentV2` y el prompt de Agnes incluyen:

- `declared_capacity`;
- `probable_archetype`;
- `archetype_confidence`;
- `archetype_evidence`;
- etapas como `LISTO_PARA_PRECALIFICAR`.

El clasificador determinístico también asigna arquetipos mediante coincidencias de términos.

Esto contradice la arquitectura aprobada porque una conversación pública solo autoriza:

```text
tema real
contexto
afinidad aparente
intención aparente
evidencia
contradicciones
incertidumbre
riesgo de falso positivo
```

#### Recomendación

No mutar silenciosamente `SemanticAssessmentV2`.

Crear una versión nueva:

```text
ConversationAssessmentV3
```

Contrato mínimo recomendado:

```text
real_topic
contextual_meaning
apparent_affinity
apparent_affinity_domains
apparent_intention
intention_summary
evidence_fragments
contradictions
missing_context
false_positive_risk
uncertainty
human_review_reason
review_priority
recommended_review_action
semantic_engine
model_name
provisional
human_review_required
```

Excluir de V3:

```text
declared_capacity
probable_archetype
archetype_confidence
archetype_evidence
participation_path
qualification_status
```

Conservar V2 como evidencia histórica y compatibilidad de lectura.

---

### H-04 — El fallback determinístico puede producir promoción semántica falsa

**Severidad:** CRÍTICA

`assess_with_optional_llm_details()` captura cualquier excepción y ejecuta:

```text
classify_conversation(text)
```

Ese clasificador usa palabras y puntajes para:

- estimar afinidad;
- estimar intención;
- asignar arquetipo;
- recomendar acercamiento.

Si Agnes falla, RADAR puede presentar como interpretación semántica una coincidencia léxica. Este comportamiento reproduce el error del caso fútbol/comunidad.

#### Recomendación

El fallback debe ser **conservador y cerrado**:

```text
LLM disponible y salida válida
→ evaluación semántica V3

LLM no disponible o salida inválida
→ SEMANTIC_ASSESSMENT_UNAVAILABLE
→ no promover automáticamente
→ revisión humana o reintento
```

El filtro determinístico puede utilizarse para:

- detectar contenido insuficiente;
- detectar duplicación;
- detectar promoción evidente;
- ordenar reintentos;
- bloquear entradas manifiestamente inválidas.

No debe simular comprensión contextual.

---

### H-05 — La literalidad de la evidencia no se valida

**Severidad:** ALTA

El prompt exige citas literales, pero el código no verifica que cada elemento de `evidence_fragments` exista en el texto original.

#### Recomendación

Agregar una validación determinística posterior al LLM:

```text
para cada evidence_fragment:
    normalizar espacios
    comprobar pertenencia al texto fuente normalizado
    rechazar o marcar fragmentos no verificables
```

La salida no debe poder alcanzar `CLEAR` si no conserva evidencia verificable.

Pruebas obligatorias:

- cita literal válida;
- cita inventada;
- diferencia solo de espacios;
- fragmento traducido, que debe rechazarse como cita;
- fragmento no presente por contexto truncado.

---

### H-06 — El prompt de Agnes responde al contrato anterior

**Severidad:** ALTA

El prompt HTTP y las instrucciones de Pydantic AI exigen:

- puntajes 0–100;
- capacidad declarada;
- etapa de decisión;
- arquetipo.

#### Recomendación

Versionar prompt y schema en conjunto:

```text
radar-conversation-assessment/v3
```

El prompt debe responder primero:

1. de qué trata realmente la conversación;
2. qué contexto le da sentido;
3. qué está haciendo el hablante;
4. qué intención aparente existe;
5. qué afinidad aparente tiene con Inlak’ech;
6. qué evidencia sostiene la lectura;
7. qué contradicciones e incertidumbres permanecen.

El modelo no debe elegir estado de workflow ni decisión de contacto.

---

### H-07 — La calibración mide el objeto equivocado

**Severidad:** ALTA

`HumanAssessmentLabel` y `CalibrationReport` miden actualmente:

- etapa de decisión;
- exactitud de arquetipo;
- tolerancia de puntajes temáticos, de valores e intención.

El corpus V1 contiene arquetipos esperados asignados desde textos públicos.

#### Recomendación

Conservar el corpus V1 como histórico y crear:

```text
radar-conversation-calibration-corpus/v2
```

Etiquetas mínimas:

```text
expected_real_topic
expected_contextual_meaning
expected_apparent_affinity
expected_affinity_domains
expected_apparent_intention
expected_false_positive_risk
expected_review_action
required_evidence_fragments
forbidden_inferences
```

Métricas prioritarias:

```text
affinity_class_accuracy
false_positive_rate
evidence_validity_rate
intent_class_accuracy
human_review_recall
forbidden_inference_rate
```

Eliminar `archetype_accuracy` de la calibración pública.

---

### H-08 — La revisión aprueba un acercamiento, pero no crea una persona operativa

**Severidad:** ALTA

`ReviewDecisionType.APPROVE_APPROACH` cambia directamente:

```text
Conversation.status = APPROACH_APPROVED
```

No crea un objeto persona/candidato.

#### Recomendación

Evolucionar la decisión a:

```text
APPROVE_DISCOVERY_CONTACT
```

La aprobación debe crear idempotentemente un `DiscoveryCandidate` ligado a la conversación de origen.

Compatibilidad:

- leer `APPROVE_APPROACH` histórico;
- no reescribir registros existentes;
- la nueva API debe usar el nombre semánticamente correcto.

---

### H-09 — Contacto y respuesta siguen perteneciendo a la conversación

**Severidad:** ALTA

`EngagementEvent` registra contacto y respuesta mediante `conversation_id`.

Una respuesta es un evento de la relación con una persona, no una propiedad de la conversación pública original.

#### Recomendación

Dos alternativas técnicas:

#### Alternativa A — Migración formal

Agregar `discovery_candidate_id` nullable a `EngagementEvent`, conservar `conversation_id` para trazabilidad y exigir candidato en eventos nuevos.

#### Alternativa B — Tabla versionada

Crear `DiscoveryInteraction` para los casos nuevos y conservar `EngagementEvent` como legado.

**Recomendación de esta auditoría:** Alternativa A, siempre que antes se incorpore una herramienta de migración de esquema. Evita duplicar conceptos y conserva historial.

---

### H-10 — No existe resultado humano del descubrimiento

**Severidad:** CRÍTICA

Después de `REPLIED` no existe un registro que permita afirmar:

- si la persona comprendió qué es Inlak’ech;
- si reveló simpatía;
- qué afinidad expresó;
- qué motivación declaró;
- qué objeciones presentó;
- si desea continuar;
- si consiente precalificación.

#### Recomendación

Agregar:

```text
DiscoveryOutcome
```

Campos mínimos:

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
human_notes
archetype_hypothesis
archetype_evidence
archetype_confidence
archetype_human_confirmed
recorded_by
recorded_at
```

El arquetipo puede convivir en este registro durante el primer corte. No hace falta crear una tabla separada mientras no exista necesidad de múltiples evaluaciones históricas de arquetipo.

---

### H-11 — Una respuesta habilita directamente la precalificación

**Severidad:** CRÍTICA

La ruta actual acepta precalificación si:

```python
conversation.status in {"REPLIED", "QUALIFICATION_STARTED", "NURTURING"}
```

Esto implementa exactamente el salto que la arquitectura nueva prohíbe.

#### Recomendación

La ruta debe exigir:

```text
DiscoveryCandidate existente
+
DiscoveryOutcome válido
+
revealed_affinity_level en PARTIAL o CLEAR
+
wants_to_continue = true
+
consent_to_prequalification = true
+
estado PREQUALIFICATION_ACCEPTED
```

Una respuesta cordial o una solicitud de información no debe alcanzar precalificación automáticamente.

---

### H-12 — `qualify_contact()` controla estados que no le pertenecen

**Severidad:** ALTA

La función determinística devuelve `RadarCommercialState`, incluyendo:

- `OBSERVING`;
- `DO_NOT_CONTACT`;
- `NURTURING`;
- `QUALIFIED`.

Esto acopla el motor de precalificación con el workflow global.

#### Recomendación

Separar:

```text
QualificationResult
→ ajuste, semáforo, acción y camino recomendado

WorkflowTransitionService
→ estado global permitido según resultado, consentimiento y evidencia
```

`qualify_contact()` no debería decidir el estado del descubrimiento ni de la conversación.

La lógica comercial de capital, horizonte, motivación y camino puede conservarse prácticamente intacta.

---

### H-13 — El consentimiento está duplicado y mezclado

**Severidad:** MEDIA-ALTA

`QualificationInput.consent_to_continue` funciona simultáneamente como:

- permiso para continuar;
- gate de calendario;
- gate de CRM;
- señal de estado.

La arquitectura nueva necesita distinguir:

```text
consent_to_prequalification
consent_to_commercial_followup
consent_to_crm_transfer
```

En un primer corte pueden reducirse a dos momentos:

1. consentimiento para precalificación, registrado en `DiscoveryOutcome`;
2. consentimiento para transferencia/seguimiento comercial, registrado en la precalificación.

No asumir que aceptar un cuestionario equivale a aceptar transferencia externa.

---

### H-14 — La transferencia CRM no prueba el descubrimiento

**Severidad:** MEDIA-ALTA

`build_crm_transfer_payload()` valida:

- consentimiento dentro de `QualificationInput`;
- `crm_transfer_allowed`.

No recibe ni valida:

- candidato de descubrimiento;
- afinidad revelada;
- resultado humano;
- origen de consentimiento;
- identificador de trazabilidad del caso.

#### Recomendación

El payload futuro debe incluir:

```text
discovery_candidate_id
discovery_outcome_id
qualification_record_id
consent_recorded_at
source_conversation_id
```

La frontera Relaticle debe verificar esos identificadores antes de construir el paquete.

---

### H-15 — La UI expone precalificación después de cualquier respuesta

**Severidad:** ALTA

La interfaz presenta:

```text
Precalificación (cuando ya hubo respuesta)
```

No existe panel para:

- diálogo de descubrimiento;
- afinidad revelada;
- decisión de continuar;
- consentimiento para precalificación;
- hipótesis humana de arquetipo.

#### Recomendación

Divulgación progresiva en tres vistas o paneles:

#### Vista 1 — Conversación

- texto y contexto;
- interpretación V3;
- evidencia;
- revisión humana;
- aprobar contacto de descubrimiento.

#### Vista 2 — Descubrimiento

- identidad pública;
- mensaje aprobado;
- contacto y respuesta;
- diálogo resumido;
- resultado humano;
- afinidad revelada;
- posible arquetipo;
- consentimiento.

#### Vista 3 — Precalificación

Visible únicamente con `PREQUALIFICATION_ACCEPTED`.

La aplicación puede continuar con HTML/CSS/JavaScript actuales. No requiere un frontend separado.

---

### H-16 — Los estados están dispersos y no existe una máquina de transiciones

**Severidad:** ALTA

Los cambios de estado se realizan en `app/api/routes.py` mediante diccionarios y asignaciones directas.

#### Recomendación

Agregar un único módulo simple:

```text
app/workflow.py
```

Responsabilidades:

- enums canónicos;
- transiciones permitidas;
- errores de transición;
- aplicación idempotente;
- separación de estado de conversación, descubrimiento y cualificación.

No introducir un framework externo de workflow.

Pruebas mínimas:

```text
DETECTED → QUALIFICATION_STARTED       bloqueada
REPLIED → PREQUALIFICATION_ACCEPTED    bloqueada sin outcome
AFFINITY_NOT_CONFIRMED → QUALIFICATION bloqueada
PREQUALIFICATION_ACCEPTED → QUALIFICATION_STARTED permitida
QUALIFIED → TRANSFERRED_TO_CRM         permitida con consentimiento
```

---

### H-17 — No existe mecanismo de migración de esquema

**Severidad:** ALTA

`init_db()` utiliza:

```text
Base.metadata.create_all()
```

Esto crea tablas nuevas, pero no agrega columnas ni transforma tablas existentes.

El proyecto declara PostgreSQL como destino y ya posee datos locales. Una reforma transversal no debe depender de borrar la base.

#### Recomendación

Antes de modificar tablas existentes, incorporar migraciones versionadas, preferentemente Alembic.

La necesidad está demostrada por:

- nueva entidad `DiscoveryCandidate`;
- nueva entidad `DiscoveryOutcome`;
- posible FK desde `EngagementEvent`;
- posible FK desde `QualificationRecord`;
- transición de estado histórica;
- preservación de `SemanticAssessmentV2`.

No se propone infraestructura distribuida. Se propone control básico de evolución del esquema relacional.

---

### H-18 — La entrada experimental y la ingesta operativa están separadas, pero falta el gate semántico de admisión

**Severidad:** MEDIA

Estado observado:

- `run_search_corpus.py` genera artefactos e informes y no persiste por sí mismo;
- `persist_discovery_results()` persiste cualquier lista que reciba;
- no existe wiring productivo entre corpus runner e ingesta;
- `conversation_quality.py` mide calidad estructural, no afinidad semántica.

Esto es correcto como separación experimental, pero antes de conectar búsqueda real con la bandeja debe existir una decisión explícita de admisión.

#### Recomendación

```text
resultado recuperado
→ normalización y deduplicación
→ evaluación de suficiencia estructural
→ evaluación semántica V3
→ admisión a revisión humana
```

`substantive` no debe equivaler a `afín`.

---

## 6. Arquitectura técnica mínima recomendada

```text
Conversation
    └── ConversationAssessmentV3

Conversation + aprobación humana
    └── DiscoveryCandidate
            ├── EngagementEvent
            └── DiscoveryOutcome
                    └── QualificationRecord
                            └── CRMTransferPayload
```

### Propiedad de la verdad

| Verdad | Objeto responsable |
|---|---|
| Qué se publicó | `Conversation` |
| Qué entendió RADAR | `ConversationAssessmentV3` |
| Qué persona fue aprobada para diálogo | `DiscoveryCandidate` |
| Qué contacto y respuesta ocurrieron | `EngagementEvent` vinculado al candidato |
| Qué afinidad se reveló | `DiscoveryOutcome` humano |
| Qué información comercial declaró | `QualificationRecord` |
| Qué se transfiere | `CRMTransferPayload` |

---

## 7. Impacto archivo por archivo

### 7.1. Archivos productivos de impacto directo

| Archivo | Impacto | Acción futura |
|---|---|---|
| `app/schemas/assessment.py` | Crítico | Crear contrato V3; conservar V2 compatible |
| `app/models/assessment_v2.py` | Histórico | No mutar; agregar modelo V3 |
| `app/semantics/llm_classifier.py` | Crítico | Nuevo draft, prompt, validación de evidencia y fallback cerrado |
| `app/semantics/classifier.py` | Crítico | Retirar arquetipo y promoción semántica; limitar función determinística |
| `app/semantics/calibration.py` | Alto | Versionar etiquetas y métricas |
| `app/semantics/calibration_builder.py` | Alto | Exportar corpus V2 sin arquetipos públicos |
| `app/semantics/calibration_io.py` | Medio | Soportar schema de corpus V2 |
| `app/api/routes.py` | Crítico | Crear candidato, registrar outcome, aplicar gates y separar estados |
| `app/schemas/review.py` | Alto | Aprobar contacto de descubrimiento y contratos de outcome |
| `app/models/review.py` | Bajo | Puede conservarse; decisión nueva se guarda como string |
| `app/models/engagement.py` | Alto | Vincular candidato mediante migración |
| `app/schemas/qualification.py` | Alto | Separar resultado de cualificación de workflow global |
| `app/qualification.py` | Medio | Conservar reglas; retirar control de estado externo |
| `app/models/qualification.py` | Alto | Vincular candidato/outcome mediante migración |
| `app/crm_transfer.py` | Alto | Exigir trazabilidad de descubrimiento y consentimientos |
| `app/db/session.py` | Alto | Registrar modelos nuevos; coexistir con migraciones |
| `app/templates/dashboard.txt` | Alto | Agregar panel de descubrimiento y gate visual |
| `app/static/radar.js.txt` | Alto | Estados nuevos, endpoints y divulgación progresiva |
| `app/static/radar.css.txt` | Bajo-Medio | Estilos de nuevos paneles y estados |

### 7.2. Archivos nuevos mínimos

```text
app/models/assessment_v3.py
app/models/discovery.py
app/schemas/discovery.py
app/workflow.py
```

Podría agregarse un servicio:

```text
app/discovery/service.py
```

solo si evita engordar más `app/api/routes.py`. No es obligatorio crear paquetes adicionales.

### 7.3. Archivos que no necesitan reforma estructural

```text
app/discovery/last30days_adapter.py
app/discovery/last30days_contracts.py
app/discovery/concrete_sources.py
app/discovery/scanning_matrix.py
app/discovery/source_scanning_plan.py
app/integrations/relaticle.py
```

Relaticle sigue bloqueado hasta auditoría real.

---

## 8. Impacto sobre pruebas

### Pruebas que deben sustituirse o evolucionar

```text
tests/test_classifier.py
tests/test_llm_classifier.py
tests/test_semantic_calibration.py
tests/test_semantic_calibration_builder.py
tests/test_semantic_calibration_io.py
tests/test_api_flow.py
tests/test_qualification.py
tests/test_dashboard_ui.py
```

### Pruebas nuevas mínimas

```text
tests/test_conversation_assessment_v3.py
tests/test_evidence_validation.py
tests/test_discovery_candidate.py
tests/test_discovery_outcome.py
tests/test_workflow_transitions.py
tests/test_prequalification_gate.py
tests/test_discovery_ui.py
```

### Casos semánticos obligatorios

1. comunidad + Messi/Cristiano → afinidad inexistente;
2. inversión en Yucatán puramente especulativa → cercanía temática, afinidad incompatible;
3. simpatía temática sin voluntad de actuar;
4. búsqueda exploratoria afín;
5. intención explícita afín;
6. texto insuficiente;
7. cita inventada por el LLM;
8. caída de Agnes sin promoción determinística.

### Caso integral obligatorio

```text
conversación
→ evaluación V3
→ revisión
→ candidato
→ contacto
→ respuesta
→ outcome humano
→ consentimiento
→ precalificación
→ cualificación
```

Y su control negativo:

```text
respuesta
→ sin outcome o sin consentimiento
→ precalificación bloqueada con 409
```

---

## 9. Estrategia de compatibilidad y migración

### 9.1. Registros semánticos

```text
SemanticAssessmentV2
→ solo lectura histórica

ConversationAssessmentV3
→ escritura nueva
```

No convertir registros V2 automáticamente en V3, porque contienen inferencias que la arquitectura nueva considera inválidas.

### 9.2. Estados históricos

Los valores actuales de `Conversation.status` deben conservarse como evidencia.

La migración puede mapear únicamente donde exista evidencia suficiente:

```text
APPROACH_APPROVED / CONTACTED / REPLIED
→ crear DiscoveryCandidate legado
```

Pero no debe inventar:

```text
afinidad revelada
consentimiento
arquetipo humano
```

Esos campos deben permanecer desconocidos hasta revisión humana.

### 9.3. API

Mantener endpoints actuales durante una transición breve:

```text
/conversations/{id}/assess
/conversations/{id}/engagement-events
/conversations/{id}/qualifications
```

Agregar endpoints nuevos o versiones explícitas. Los endpoints antiguos no deben seguir promoviendo estados una vez activado el nuevo workflow.

### 9.4. Base de datos

Orden recomendado:

1. introducir migraciones;
2. crear tablas nuevas;
3. agregar FKs nullable;
4. migrar referencias seguras;
5. activar nuevas rutas;
6. bloquear rutas antiguas de escritura;
7. conservar lectura histórica.

---

## 10. Secuencia de implementación recomendada

### Ciclo 1 — Base de evolución

**Responsable recomendado:** Codex

- incorporar migraciones;
- crear modelos V3 y descubrimiento vacíos;
- no cambiar comportamiento;
- pruebas de creación y migración;
- preservar los 88 tests.

### Ciclo 2 — Interpretación de conversación V3

**Responsable recomendado:** Codex para contrato y wiring; OpenCode/DeepSeek para pruebas focales.

- schema V3;
- prompt V3;
- evidencia literal;
- fallback cerrado;
- persistencia V3;
- corpus de control negativo.

### Ciclo 3 — Candidato y workflow de descubrimiento

**Responsable recomendado:** Codex

- `DiscoveryCandidate`;
- transiciones;
- aprobación humana crea candidato;
- eventos vinculados;
- sin precalificación todavía.

### Ciclo 4 — Resultado humano y arquetipo posterior

**Responsable recomendado:** Codex para dominio; OpenCode/DeepSeek para UI y tests delimitados.

- `DiscoveryOutcome`;
- afinidad revelada;
- consentimiento;
- hipótesis de arquetipo confirmada;
- trazabilidad.

### Ciclo 5 — Gate de precalificación

**Responsable recomendado:** Codex

- bloquear salto desde respuesta;
- desacoplar `qualify_contact()` del estado global;
- conservar reglas comerciales;
- reforzar CRM payload.

### Ciclo 6 — UI progresiva

**Responsable recomendado:** OpenCode/DeepSeek con especificación cerrada; revisión final Codex.

- conversación;
- descubrimiento;
- precalificación;
- estados y permisos;
- pruebas de interfaz.

### Ciclo 7 — Calibración y piloto

- corpus humano V2;
- precisión semántica;
- falso positivo;
- uso humano real;
- piloto extremo a extremo.

---

## 11. Riesgos de implementación

### Riesgo 1 — Cambiar nombres sin cambiar propiedad del estado

Renombrar `REPLIED` a `DISCOVERY_REPLIED` sin crear un objeto candidato no resuelve el problema.

### Riesgo 2 — Reutilizar V2 como si fuera V3

Eliminar campos de V2 rompería historia, API, tests y corpus. Debe versionarse.

### Riesgo 3 — Crear demasiadas entidades

No crear inicialmente `Person`, `Contact`, `Candidate`, `Lead`, `Opportunity` y `Profile` como tablas separadas.

El objeto mínimo es `DiscoveryCandidate`.

### Riesgo 4 — Permitir fallback silencioso

La caída de Agnes no debe degradar a una promoción basada en palabras sin informar al humano.

### Riesgo 5 — Migrar inferencias como hechos

No convertir arquetipos V2 ni capacidad desconocida en datos humanos del nuevo dominio.

### Riesgo 6 — UI habilitada por apariencia

Ocultar visualmente precalificación no alcanza. El backend debe bloquearla.

---

## 12. Complejidad real

La reforma es transversal, pero acotada.

Estimación arquitectónica:

```text
modelos nuevos principales: 3
módulos nuevos mínimos: 4
módulos productivos existentes afectados: 15–19
archivos de pruebas afectados o nuevos: 12–15
servicios externos nuevos: 0
repositorios nuevos: 0
microservicios nuevos: 0
```

La mayor dificultad no está en el volumen de código, sino en:

- migrar sin perder evidencia;
- separar estados correctamente;
- impedir inferencias prematuras;
- mantener compatibilidad durante la transición.

---

## 13. Decisiones técnicas que deben aprobarse antes del código

### DTI-01

Usar `DiscoveryCandidate` como objeto mínimo de persona operativa, sin crear una entidad CRM genérica.

### DTI-02

Crear `ConversationAssessmentV3` y conservar `SemanticAssessmentV2` como histórico.

### DTI-03

Adoptar fallback semántico cerrado: una caída del LLM no promueve automáticamente una conversación.

### DTI-04

Introducir migraciones versionadas antes de agregar FKs a tablas existentes.

### DTI-05

Separar estado de conversación, estado de descubrimiento y resultado de cualificación.

### DTI-06

Mantener `EngagementEvent`, agregando referencia al candidato mediante migración, en vez de duplicarlo con otra tabla.

### DTI-07

Guardar la primera hipótesis humana de arquetipo dentro de `DiscoveryOutcome`; separar tabla solo cuando se necesite historial múltiple.

### DTI-08

Mantener la UI actual y reorganizarla progresivamente, sin frontend nuevo.

---

## 14. Criterio de cierre de la auditoría

La auditoría queda completa porque identifica:

- objetos faltantes;
- acoplamientos incompatibles;
- rutas afectadas;
- datos que requieren migración;
- contratos que deben versionarse;
- pruebas que deben evolucionar;
- orden seguro de implementación;
- tareas adecuadas para Codex y OpenCode/DeepSeek.

No autoriza implementación automática. El siguiente paso es aprobar las decisiones `DTI-01` a `DTI-08` y convertir los ciclos 1 y 2 en especificaciones técnicas cerradas.

---

## 15. Siguiente acción recomendada

Crear y aprobar, en este orden:

```text
docs/specs/002A_conversation_assessment_v3.md
docs/specs/003B_discovery_domain_implementation.md
```

La primera especificación debe cubrir únicamente el contrato semántico V3, persistencia versionada, validación de evidencia y fallback cerrado.

La segunda debe cubrir candidato, estados, migración, outcome humano y gate de precalificación.

No conviene implementar ambos dominios en un único lote.


---

## 16. Resolución posterior de la auditoría

**Fecha:** 19 de julio de 2026
**Estado:** DECISIONES APROBADAS

Las decisiones `DTI-01` a `DTI-08` fueron aprobadas mediante `D-010` en `docs/DECISIONS.md`.

Se crearon y aprobaron:

```text
docs/specs/002A_conversation_assessment_v3.md
docs/specs/003B_discovery_domain_implementation.md
```

Orden obligatorio:

```text
SPEC-002A → IMPLEMENTING → VERIFIED
→ SPEC-003B puede pasar a IMPLEMENTING
```

La aprobación de SPEC-003B no autoriza su implementación anticipada ni la mezcla de ambos dominios en un único lote.
