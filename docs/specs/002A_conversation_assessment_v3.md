# SPEC-002A — Evaluación conversacional V3

**Estado:** VERIFIED
**Fecha de aprobación:** 19 de julio de 2026
**Baseline previa informada:** `88 passed`
**Depende de:** SPEC-001, arquitectura maestra y auditoría técnica de impacto
**Bloquea:** SPEC-003B y toda reforma del embudo humano de descubrimiento

---

## 1. Propósito

Implementar una evaluación semántica versionada que interprete una conversación pública sin diagnosticar prematuramente a la persona que participa.

El corte vertical obligatorio es:

```text
Conversation real persistida
→ solicitud de evaluación V3
→ interpretación semántica estructurada
→ validación literal de evidencia
→ política determinística conservadora
→ persistencia versionada
→ resultado explicable para revisión humana
```

La salida debe responder:

1. de qué trata realmente la conversación;
2. qué contexto le da sentido;
3. qué afinidad aparente presenta con Inlak’ech;
4. qué intención aparente se expresa;
5. qué fragmentos literales sostienen la lectura;
6. qué contradicciones, faltantes e incertidumbres permanecen;
7. si corresponde revisión humana, observación o descarte.

La especificación no crea candidatos, no registra contacto y no inicia precalificación.

---

## 2. Autoridad

Esta especificación implementa y queda subordinada a:

```text
docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md
docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md
docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md
docs/RADAR_TECHNICAL_IMPACT_AUDIT_2026-07-19.md
docs/specs/002_affinity_classification.md
AGENTS.md
```

Decisiones técnicas aplicables:

- `DTI-02`: crear `ConversationAssessmentV3` y conservar V2;
- `DTI-03`: fallback semántico cerrado;
- `DTI-04`: incorporar migraciones versionadas;
- `DTI-05`: la evaluación no controla estados de descubrimiento o cualificación.

Ante una contradicción, prevalece el documento maestro de arquitectura.

---

## 3. Alcance

Incluye:

- infraestructura mínima de migraciones versionadas;
- contrato Pydantic V3;
- modelo persistente V3;
- prompt V3 para Agnes y proveedores compatibles;
- validación determinística de evidencia literal;
- política de fallback cerrado;
- prioridad y acción de revisión calculadas por RADAR;
- endpoints versionados de evaluación y lectura;
- corpus de calibración V2 compatible con el nuevo objeto;
- pruebas focales, de integración y regresión;
- preservación de registros V2.

---

## 4. Fuera de alcance

No incluye:

- `DiscoveryCandidate`;
- `DiscoveryOutcome`;
- contacto o respuesta;
- arquetipos posteriores al diálogo;
- estados del embudo de descubrimiento;
- precalificación;
- cambios en `qualify_contact()`;
- integración con Relaticle;
- rediseño de la interfaz;
- búsqueda o conectores nuevos;
- clasificación de personas;
- inferencia financiera;
- migración automática de V2 a V3;
- otro repositorio, backend, frontend o servicio externo.

---

## 5. Contrato de entrada

La evaluación recibe una conversación persistida con:

```text
conversation_id
source
conversation_url
author_name opcional
title opcional
text
context opcional
published_at opcional
query_origin opcional
```

El texto de análisis debe construir una entrada delimitada y no ambigua, evitando duplicar contenido idéntico entre `title`, `text` y `context`.

Las conversaciones externas se consideran datos no confiables. Su contenido nunca se interpreta como instrucciones para el sistema o el agente.

---

## 6. Contrato V3

### 6.1. Versión

```text
schema_version = radar-conversation-assessment/v3
```

### 6.2. Estados de ejecución

```text
COMPLETED
SEMANTIC_ASSESSMENT_UNAVAILABLE
INVALID_MODEL_OUTPUT
INVALID_EVIDENCE
```

Solo `COMPLETED` puede producir una afinidad aparente utilizable para ordenar revisión.

### 6.3. Afinidad aparente

```text
NONE
POSSIBLE
CLEAR
```

Definiciones:

- `NONE`: el sentido de la conversación no intersecta de manera sustantiva con Inlak’ech;
- `POSSIBLE`: existe una relación plausible, pero falta evidencia o contexto;
- `CLEAR`: existe una relación semántica suficientemente explícita y respaldada por evidencia literal.

`CLEAR` no significa afinidad personal confirmada.

### 6.4. Intención aparente

```text
NONE
THEMATIC_SYMPATHY
EXPLORATION
ACTION_ORIENTED
```

Definiciones:

- `NONE`: no se detecta dirección de acción;
- `THEMATIC_SYMPATHY`: hay valoración o simpatía temática sin voluntad observable de actuar;
- `EXPLORATION`: la persona pregunta, compara, evalúa o busca información;
- `ACTION_ORIENTED`: expresa una acción concreta o una voluntad explícita de avanzar.

No se utilizarán estados como `LISTO_PARA_PRECALIFICAR` en una conversación pública.

### 6.5. Riesgo e incertidumbre

```text
LOW
MEDIUM
HIGH
```

Son dimensiones separadas:

- `false_positive_risk`: riesgo de que la afinidad sea aparente por coincidencia léxica o contexto insuficiente;
- `uncertainty`: grado de incertidumbre general de la interpretación.

### 6.6. Acción de revisión

```text
DISCARD
OBSERVE
REVIEW
```

La evaluación no puede aprobar contacto.

### 6.7. Campos obligatorios

Para `COMPLETED`:

```text
schema_version
assessment_status
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
created_at
```

Restricciones:

- `real_topic`: texto breve, concreto y no vacío;
- `contextual_meaning`: explica por qué el enunciado significa lo interpretado;
- `apparent_affinity_domains`: lista controlada de dominios de Inlak’ech;
- `evidence_fragments`: citas literales validadas;
- `review_priority`: entero `0–100`, calculado por RADAR;
- `provisional`: siempre `true`;
- `human_review_required`: siempre `true` para `POSSIBLE` o `CLEAR`.

### 6.8. Campos expresamente prohibidos

La respuesta V3 no contiene:

```text
declared_capacity
probable_archetype
archetype_confidence
archetype_evidence
participation_path
qualification_status
capital_band
commercial_lead_score
```

---

## 7. Dominios iniciales de afinidad

La lista controlada inicial puede incluir:

```text
CONSCIOUS_INVESTMENT
LEGACY
COMMUNITY
REGENERATION
TERRITORY
USEFUL_BEAUTY
STRATEGIC_PATIENCE
PURPOSEFUL_BUILDING
BELONGING
LONG_TERM
SUSTAINABLE_HOSPITALITY
NON_SPECULATIVE_DEVELOPMENT
ACTIVE_PARTICIPATION
CULTURAL_RESPECT
MEXICO_YUCATAN_CONNECTION
```

La aparición de una palabra no autoriza el dominio. Debe existir relación contextual.

La taxonomía se centraliza en un único contrato o configuración versionada. No se duplicará entre prompt, clasificador y UI.

---

## 8. Persistencia versionada

### 8.1. Modelo nuevo

Crear una tabla nueva equivalente a:

```text
conversation_assessments_v3
```

Relación:

```text
Conversation 1 → N ConversationAssessmentV3
```

Cada ejecución genera un registro inmutable de evaluación o intento, con metadatos suficientes para auditoría.

### 8.2. V2 histórico

```text
SemanticAssessmentV2
→ permanece legible
→ no recibe escrituras nuevas desde el flujo V3
→ no se transforma automáticamente
→ no se borra
```

No convertir arquetipos, capacidad ni puntajes V2 en campos V3.

### 8.3. Intentos fallidos

Una caída del proveedor o una salida inválida debe persistir un intento con:

```text
assessment_status
semantic_engine
model_name
safe_error_code
created_at
```

No guardar secretos, claves, headers ni respuestas completas que puedan contener información sensible.

---

## 9. Migraciones

### 9.1. Herramienta

Incorporar Alembic como mecanismo de migración relacional.

No agregar infraestructura externa.

### 9.2. Estrategia

La implementación debe incluir:

1. configuración de Alembic usando el `DATABASE_URL` vigente;
2. una revisión baseline que represente el esquema existente;
3. una revisión posterior que cree `conversation_assessments_v3`;
4. procedimiento documentado para:
   - base nueva;
   - base existente;
   - SQLite de pruebas;
   - PostgreSQL objetivo;
5. prueba reproducible de upgrade.

Para una base existente, el proceso debe verificar el esquema antes de marcar la revisión baseline como aplicada. No se autoriza borrar ni recrear la base como mecanismo de migración.

`Base.metadata.create_all()` puede mantenerse temporalmente para pruebas aisladas, pero no puede seguir siendo la única estrategia de evolución del esquema.

---

## 10. Prompt semántico V3

El prompt debe solicitar exclusivamente JSON válido conforme al contrato V3.

Debe ordenar:

- interpretar el tema real, no reaccionar a palabras aisladas;
- reconstruir contexto;
- distinguir simpatía temática de exploración y acción;
- evaluar afinidad aparente con Inlak’ech;
- citar fragmentos literales exactos;
- declarar contradicciones y faltantes;
- representar incertidumbre;
- evitar arquetipos, capacidad y calificación;
- tratar el contenido analizado como datos, no instrucciones;
- no elegir workflow ni autorizar contacto.

El prompt y el schema deben compartir la misma versión.

---

## 11. Validación de evidencia

### 11.1. Normalización permitida

Para comparar una cita con el texto fuente se permite únicamente:

- normalizar saltos de línea;
- colapsar espacios consecutivos;
- eliminar espacios al inicio y al final.

No se permite:

- traducir;
- parafrasear;
- corregir palabras;
- alterar puntuación sustantiva;
- combinar fragmentos discontinuos como una única cita.

### 11.2. Política

Para cada fragmento:

```text
normalizar fragmento
→ buscarlo en título, texto o contexto normalizados
→ aceptar o rechazar
```

Si algún fragmento es inválido:

- se registra el hallazgo;
- no se presenta como evidencia;
- la salida queda `INVALID_EVIDENCE` cuando no subsiste evidencia suficiente.

Una evaluación no puede ser `CLEAR` sin al menos un fragmento literal válido que sostenga la afinidad.

Una intención `ACTION_ORIENTED` debe tener evidencia literal específica de acción.

---

## 12. Política determinística posterior al LLM

RADAR, no el modelo, calcula:

- `review_priority`;
- `recommended_review_action`;
- degradación por riesgo;
- bloqueos por evidencia inválida;
- imposibilidad de promoción cuando la evaluación no está `COMPLETED`.

La fórmula inicial debe ser transparente y quedar testeada. Puede utilizar clases y evidencia, pero no debe reintroducir un diagnóstico de persona.

Reglas mínimas:

```text
assessment_status != COMPLETED
→ REVIEW u OBSERVE, nunca promoción automática

apparent_affinity = NONE
→ DISCARD u OBSERVE según incertidumbre

apparent_affinity = POSSIBLE
→ REVIEW u OBSERVE

apparent_affinity = CLEAR + evidencia válida
→ REVIEW

false_positive_risk = HIGH
→ no puede obtener máxima prioridad
```

La fórmula exacta debe quedar en una única función pura y documentada.

---

## 13. Fallback cerrado

### 13.1. Regla

```text
LLM disponible + salida válida + evidencia válida
→ COMPLETED

LLM no disponible
→ SEMANTIC_ASSESSMENT_UNAVAILABLE

JSON o schema inválido
→ INVALID_MODEL_OUTPUT

evidencia insuficiente o inventada
→ INVALID_EVIDENCE
```

Ninguno de esos errores puede activar el clasificador léxico legado para promover una conversación.

### 13.2. Uso permitido del filtro determinístico

Puede utilizarse para:

- suficiencia estructural;
- contenido vacío;
- duplicación;
- promoción manifiesta;
- priorización de reintentos;
- validación de contratos.

No puede simular comprensión contextual ni producir `CLEAR`.

---

## 14. API versionada

Agregar endpoints explícitos:

```text
POST /api/conversations/{conversation_id}/assessments/v3
GET  /api/conversations/{conversation_id}/assessments/v3
```

### POST

- verifica que exista la conversación;
- ejecuta el flujo V3;
- persiste el intento;
- devuelve el contrato V3;
- no crea candidato;
- no autoriza contacto;
- no inicia precalificación.

### GET

- devuelve historia V3 ordenada;
- incluye intentos fallidos de manera segura;
- no mezcla registros V2.

Los endpoints V2 existentes permanecen durante la transición, pero no deben ser utilizados por nuevas capacidades. Su retiro requiere una especificación posterior.

---

## 15. Calibración V2

Crear un contrato de corpus:

```text
radar-conversation-calibration-corpus/v2
```

Etiquetas mínimas:

```text
case_id
text
source_conversation_id opcional
source_url opcional
expected_real_topic
expected_contextual_meaning
expected_apparent_affinity
expected_affinity_domains
expected_apparent_intention
expected_false_positive_risk
expected_review_action
required_evidence_fragments
forbidden_inferences
label_provenance
reviewed_by
```

Métricas:

```text
affinity_class_accuracy
intent_class_accuracy
false_positive_rate
evidence_validity_rate
human_review_recall
forbidden_inference_rate
```

No medir `archetype_accuracy` sobre conversaciones públicas.

El corpus V1 queda histórico y no autoriza V3.

---

## 16. Casos límite obligatorios

1. “comunidad” en una conversación sobre Messi y Cristiano:
   - afinidad `NONE`;
   - alto riesgo de falso positivo;
   - no promoción.
2. inversión en Yucatán con búsqueda explícita de especulación inmediata:
   - cercanía temática;
   - afinidad con Inlak’ech `NONE` o cautela explícita;
   - contradicción registrada.
3. simpatía por proyectos regenerativos sin deseo de participar:
   - `THEMATIC_SYMPATHY`;
   - no `ACTION_ORIENTED`.
4. búsqueda exploratoria de comunidad territorial:
   - `EXPLORATION`;
   - evidencia literal.
5. intención expresa de participar o conocer un proyecto:
   - `ACTION_ORIENTED` solo con cita válida.
6. texto insuficiente:
   - no interpretación fuerte;
   - observación o descarte.
7. cita inventada:
   - `INVALID_EVIDENCE` cuando no queda sustento válido.
8. fragmento traducido:
   - rechazado como cita literal.
9. diferencia exclusiva de espacios:
   - aceptada después de normalización.
10. caída de Agnes:
    - `SEMANTIC_ASSESSMENT_UNAVAILABLE`;
    - sin fallback promocional.
11. instrucción maliciosa dentro de la conversación:
    - tratada como contenido;
    - no altera el contrato.
12. repetición de título, texto y contexto:
    - no duplica artificialmente la evidencia.

---

## 17. Compatibilidad

Debe preservarse:

- lectura de evaluaciones V2;
- API V2 durante transición;
- datos existentes;
- proveedor Agnes mediante HTTP JSON directo;
- proveedores OpenAI-compatible admitidos;
- suite vigente de 88 pruebas;
- funcionamiento local con SQLite;
- destino PostgreSQL.

No es requisito que V2 y V3 produzcan la misma decisión. Representan objetos conceptuales distintos.

---

## 18. Archivos de impacto esperado

Archivos nuevos probables:

```text
alembic.ini
alembic/env.py
alembic/versions/*
app/models/assessment_v3.py
app/schemas/assessment_v3.py
app/semantics/conversation_assessment_v3.py
tests/test_conversation_assessment_v3.py
tests/test_evidence_validation.py
tests/test_migrations.py
```

Archivos existentes permitidos:

```text
pyproject.toml
app/db/session.py
app/api/routes.py
app/models/__init__.py
app/semantics/llm_classifier.py
app/semantics/calibration.py
app/semantics/calibration_builder.py
app/semantics/calibration_io.py
scripts relacionados con calibración
documentación de estado y aceptación
```

No modificar en este corte:

```text
app/qualification.py
app/crm_transfer.py
app/models/engagement.py
app/models/qualification.py
app/templates/dashboard.txt
app/static/radar.js.txt
app/static/radar.css.txt
app/integrations/relaticle.py
```

Una desviación requiere justificarla antes de editar.

---

## 19. Pruebas obligatorias

### Focales

- validación de todos los enums y campos V3;
- ausencia de campos prohibidos;
- cálculo determinístico de prioridad;
- evidencia literal válida;
- evidencia inventada;
- normalización de espacios;
- fragmento traducido;
- fallback cerrado;
- error HTTP del proveedor;
- JSON inválido;
- caso Messi/Cristiano;
- caso especulación inmediata;
- simpatía sin intención;
- intención explícita con evidencia.

### Persistencia

- crear y recuperar múltiples V3 para una conversación;
- persistir intentos fallidos;
- no escribir V2;
- no alterar registros V2 existentes.

### Migraciones

- upgrade de base nueva;
- baseline y upgrade de base existente simulada;
- creación de tabla V3;
- downgrade seguro de la revisión V3 cuando sea técnicamente reversible;
- compatibilidad SQLite;
- validación del SQL generado o ejecución sobre PostgreSQL disponible, sin convertir PostgreSQL en bloqueo local si no está accesible.

### API

- 404 para conversación inexistente;
- POST V3 exitoso;
- GET histórico;
- salida no disponible sin promoción;
- metadatos de motor y modelo;
- ninguna creación de candidato o cualificación.

### Regresión

```text
python -m pytest -q
```

Debe preservar las 88 pruebas y agregar las nuevas.

---

## 20. Criterios de aceptación

La especificación pasa a `VERIFIED` cuando exista evidencia reproducible de que:

1. V3 posee contrato y tabla propios;
2. V2 permanece intacto y legible;
3. ningún campo de capacidad, arquetipo o calificación aparece en V3;
4. el prompt V3 interpreta sentido y contexto;
5. las citas son verificadas contra el texto fuente;
6. una cita inventada no puede sostener afinidad `CLEAR`;
7. una caída de Agnes no activa promoción léxica;
8. el caso Messi/Cristiano queda fuera de afinidad;
9. la API V3 persiste y devuelve historia;
10. no se crean candidatos, contactos o cualificaciones;
11. las migraciones funcionan sin borrar datos;
12. la suite completa pasa;
13. `git diff --check` queda limpio;
14. la documentación de estado y aceptación se actualiza.

---

## 21. Evidencia de verificación

```text
FILES_CREATED: alembic/script.py.mako
FILES_MODIFIED: app/semantics/conversation_assessment_v3.py; tests/test_conversation_assessment_v3.py; documentación de cierre
TEMPORARY_FILES_REMOVED: alembic/script.py.template.txt; scripts/write_alembic_template.py
MIGRATION_REVISIONS: 20260719_0001 -> 20260719_0002 (head)
FOCAL_TEST_COMMAND: python -m pytest -q tests/test_conversation_assessment_v3.py tests/test_evidence_validation.py tests/test_api_assessment_v3.py tests/test_semantic_calibration_v2.py tests/test_migrations.py
FOCAL_TEST_RESULT: 27 passed
FULL_TEST_COMMAND: python -m pytest -q
FULL_TEST_RESULT: 115 passed
ALEMBIC_HISTORY_RESULT: 20260719_0001 -> 20260719_0002 (head)
MIGRATION_VALIDATION: SQLite temporal; upgrade head y current finalizaron con 20260719_0002 (head)
DIFF_CHECK: clean
COMMIT: no realizado
PUSH: no realizado
KNOWN_GAPS: SPEC-003B es la siguiente especificación autorizada; no fue implementada en este corte.
```

---

## 22. Orden de implementación

El corte debe ejecutarse en este orden:

```text
1. infraestructura de migración
2. tabla y schema V3
3. validación de evidencia
4. política determinística
5. prompt y runner V3
6. persistencia
7. API versionada
8. calibración V2
9. pruebas focales
10. regresión completa
11. checkpoint documental
```

No iniciar SPEC-003B hasta que SPEC-002A esté `VERIFIED`.
