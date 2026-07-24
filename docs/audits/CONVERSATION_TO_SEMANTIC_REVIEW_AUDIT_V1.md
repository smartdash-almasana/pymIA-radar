# RADAR — Auditoría Conversation → evaluación semántica → revisión humana

**Versión:** V1  
**Tipo:** auditoría de integración, sin implementación  
**Estado:** `COMPLETED`  
**Repositorio:** `E:\BuenosPasos\inlakech-radar`

---

## 1. Objetivo

Identificar el recorrido técnico existente desde una `Conversation` persistida hasta:

1. evaluación semántica V3;
2. persistencia del resultado;
3. revisión humana;
4. eventual entrada a Lista 1.

La auditoría busca evitar crear un flujo paralelo o duplicar capacidades ya presentes.

---

## 2. Punto de entrada confirmado

La evaluación semántica ya tiene un endpoint operativo:

```text
POST /conversations/{conversation_id}/assessments/v3
```

Ubicación:

```text
app/api/routes.py
```

El endpoint:

1. busca la `Conversation` por ID;
2. devuelve `404` si no existe;
3. toma `title`, `text` y `context` de la conversación persistida;
4. invoca `assess_conversation_cascade_v1()`;
5. persiste un `ConversationAssessmentV3`;
6. devuelve el assessment estructurado.

Conclusión:

> La conexión lógica `Conversation → evaluación V3` ya existe. El gap no es inventar el evaluador, sino asegurar que las conversaciones provenientes de Playwright entren a este recorrido y verificarlo de punta a punta.

---

## 3. Evaluación y cascada

El endpoint usa:

```text
assess_conversation_cascade_v1()
```

La cascada resuelve:

- evaluación primaria;
- revisión secundaria cuando corresponde;
- failover de proveedor;
- afinidad resuelta;
- intención resuelta;
- riesgo de falso positivo;
- incertidumbre;
- evidencia adicional aceptada;
- trazabilidad de proveedor y resolución.

El resultado principal se persiste en:

```text
ConversationAssessmentV3
```

No hace falta crear otro modelo, otro endpoint ni otro servicio semántico para integrar Playwright.

---

## 4. Persistencia del assessment

El registro persistido conserva, entre otros:

- `conversation_id`;
- estado de evaluación;
- tema y significado contextual;
- afinidad aparente;
- dominios de afinidad;
- intención aparente;
- fragmentos de evidencia;
- contradicciones;
- contexto faltante;
- riesgo de falso positivo;
- incertidumbre;
- prioridad de revisión;
- acción recomendada;
- motor y modelo;
- trazas de cascada y failover;
- necesidad de revisión humana.

Conclusión:

> La evaluación ya queda vinculada de forma directa y auditable con la conversación de origen.

---

## 5. Revisión humana existente

El sistema ya contiene dos superficies relacionadas:

### Bandeja HTMX

```text
app/htmx_ui.py
```

Carga conversaciones y su evaluación más reciente para construir las tarjetas de revisión.

### API de revisión

```text
POST /conversations/{conversation_id}/reviews
```

La aprobación de descubrimiento exige que exista un assessment V3 con estado:

```text
COMPLETED
```

Sin evaluación completada, la API devuelve conflicto y no permite avanzar.

Esto preserva el orden:

```text
Conversation
→ evaluación V3 completada
→ revisión humana
→ decisión
```

---

## 6. Lista 1 / candidato presuntivo

Existe un servicio específico:

```text
app/services/presumptive_candidates.py
```

La elegibilidad requiere:

- assessment `COMPLETED`;
- afinidad `POSSIBLE` o `CLEAR`;
- evidencia disponible;
- acción recomendada `OBSERVE` o `REVIEW`.

El servicio crea o actualiza:

- actor público;
- participante de conversación;
- candidato presuntivo.

La identidad se vincula a:

```text
conversation + assessment + actor público
```

Conclusión:

> Lista 1 ya tiene reglas y persistencia propias. El siguiente ciclo debe reutilizarlas, no recrearlas.

---

## 7. Gap real identificado

El recorrido existe por piezas, pero falta una verificación de integración que demuestre con una conversación proveniente de Playwright:

```text
PlaywrightMCPClient.navigate()
→ navigation_to_discovery()
→ persist_discovery_results()
→ Conversation
→ POST assessment V3 o servicio equivalente reutilizado
→ ConversationAssessmentV3
→ candidato presuntivo elegible cuando corresponda
→ bandeja de revisión humana
```

No está demostrado todavía en una sola prueba o ciclo de aceptación integral.

---

## 8. Riesgos de integración

### Riesgo 1 — Evaluación duplicada

El endpoint permite crear múltiples assessments para una misma conversación. Esto puede ser correcto para historial, pero el ciclo debe definir cuándo crear uno nuevo y cuándo reutilizar el más reciente.

No se debe introducir deduplicación semántica sin una especificación explícita.

### Riesgo 2 — Automatizar demasiado pronto

No debe asumirse que toda conversación persistida debe evaluarse automáticamente al momento de guardarse.

La decisión entre:

```text
evaluación explícita
```

o

```text
evaluación automática controlada
```

es de producto y debe quedar aprobada antes de modificar el flujo.

### Riesgo 3 — Confundir candidato con lead

`PresumptiveCandidate` representa una hipótesis para revisión, no una persona calificada ni un lead.

No debe saltarse:

- revisión humana;
- contacto humano;
- afinidad revelada;
- consentimiento;
- precalificación.

### Riesgo 4 — Autor parcial o ausente

El servicio puede crear un actor público por defecto cuando no hay autor identificado. Debe preservarse el estado de autor y evitar presentar esa identidad técnica como una persona confirmada.

---

## 9. Próxima especificación recomendada

### Cycle ID propuesto

```text
RADAR-PLAYWRIGHT-SEMANTIC-INTEGRATION-001
```

### Objetivo único

Demostrar que una `Conversation` creada desde evidencia Playwright puede evaluarse con el flujo V3 existente y quedar disponible para revisión humana y Lista 1, sin crear un orquestador paralelo.

### Alcance recomendado

- reutilizar `process_and_persist()`;
- reutilizar `assess_conversation_cascade_v1()` o el punto de entrada API existente;
- reutilizar `ConversationAssessmentV3`;
- reutilizar `create_or_update_presumptive_candidate()`;
- agregar una prueba de integración controlada;
- no decidir todavía evaluación automática global.

### Decisión pendiente que requiere aprobación humana

Antes de implementar, elegir explícitamente uno de estos modos:

```text
A. evaluación manual desde la interfaz/API
B. evaluación automática solo en una ejecución de campaña controlada
```

La auditoría no toma esa decisión.

---

## 10. Veredicto

```text
CONVERSATION → ASSESSMENT V3: YA EXISTE
ASSESSMENT V3 → PERSISTENCIA: YA EXISTE
ASSESSMENT → REVISIÓN HUMANA: YA EXISTE
ASSESSMENT → LISTA 1: YA EXISTE
PRUEBA INTEGRAL PLAYWRIGHT → LISTA 1: PENDIENTE
NUEVA ARQUITECTURA NECESARIA: NO
DECISIÓN DE AUTOEVALUACIÓN: PENDIENTE DE APROBACIÓN
```
