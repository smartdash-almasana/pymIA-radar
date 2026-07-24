# RADAR — CONTRATO DE CAPA DE PRODUCTIVIDAD V1

## Propósito

Este documento establece la forma de trabajo obligatoria para implementar RADAR MVP sin deriva, sin depender del chat como fuente de verdad, sin burocracia innecesaria y con una metodología de desarrollo sana.

La capa de productividad se cierra antes de continuar con experimentos o integración productiva.

---

## 1. Regla antideriva

Todo trabajo debe responder a un objetivo operativo vigente y verificable.

Antes de modificar código, cada ciclo debe declarar:

```text
OBJETIVO
ALCANCE
FUERA_DE_ALCANCE
ARCHIVOS_PREVISTOS
CRITERIO_DE_ACEPTACION
```

Queda prohibido:

- ampliar alcance durante la ejecución sin decisión explícita;
- introducir componentes no necesarios para el objetivo del ciclo;
- reabrir decisiones ya cerradas sin evidencia nueva;
- mezclar investigación, arquitectura, implementación y cierre en un mismo ciclo ambiguo;
- modificar módulos productivos durante experimentos sin autorización expresa.

Si aparece una oportunidad técnica nueva, se registra como pendiente. No se incorpora automáticamente.

---

## 2. Fuente de verdad fuera del chat

El chat, OpenCode y cualquier agente son medios de trabajo, no fuentes de verdad.

La fuente de verdad debe quedar dentro del repositorio.

Documentos rectores mínimos:

```text
docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md
docs/RADAR_MVP_IMPLEMENTATION_BASELINE_V1.md
docs/RADAR_MVP_EXECUTION_STATE_V1.md
docs/RADAR_MVP_ACCEPTANCE_CONTRACT_V1.md
```

Reglas:

- toda decisión estable se escribe en el repo;
- todo experimento produce un informe en `lab/`;
- todo cierre actualiza el estado de ejecución;
- los prompts no sustituyen contratos;
- los reportes de herramientas no sustituyen evidencia reproducible;
- una afirmación técnica solo se considera cerrada si está documentada y respaldada por pruebas o resultados observables.

---

## 3. Llegar al objetivo sin burocracia

Se empleará documentación mínima suficiente.

Cada ciclo produce únicamente:

1. un objetivo claro;
2. una modificación acotada;
3. pruebas proporcionales al riesgo;
4. un resultado verificable;
5. actualización breve del estado.

No se crearán:

- documentos duplicados;
- ADRs para decisiones triviales;
- especificaciones extensas para cambios pequeños;
- capas técnicas sin necesidad demostrada;
- nuevas abstracciones antes de tener un caso real que las exija.

La documentación debe reducir incertidumbre, no agregar carga administrativa.

---

## 4. Metodología sana de desarrollo

### 4.1 Ciclos pequeños y cerrables

Cada ciclo debe poder completarse, probarse y revertirse de forma independiente.

Flujo obligatorio:

```text
auditar
→ definir
→ implementar
→ probar
→ registrar
→ cerrar
```

### 4.2 Experimento separado de producción

Toda tecnología o enfoque no validado se prueba primero en:

```text
rama experimental
+ scripts experimentales
+ informe en lab/
```

Solo pasa a producción cuando:

- el experimento tiene criterio de aceptación;
- los resultados son repetibles;
- el costo de integración es conocido;
- el riesgo está documentado;
- existe decisión explícita de adopción.

### 4.3 Cambios mínimos

Se modifica la menor superficie necesaria.

Queda prohibido:

- refactorizar fuera de alcance;
- limpiar archivos no relacionados;
- cambiar nombres, contratos o estados sin necesidad del ciclo;
- incorporar dependencias sin justificación y prueba focal;
- tocar flujos productivos para resolver un experimento aislado.

### 4.4 Pruebas proporcionales

Cada ciclo debe ejecutar:

```text
tests focales
+ tests vecinos cuando corresponda
+ suite completa antes de integrar
+ git diff --check
```

Los fallos preexistentes deben identificarse y separarse de los introducidos por el ciclo.

### 4.5 Trazabilidad

Todo resultado debe responder:

```text
qué se quiso lograr
qué se cambió
qué se probó
qué resultado dio
qué queda pendiente
```

---

## 5. Unidad de trabajo obligatoria

Toda tarea de OpenCode, Codex o cualquier agente debe usar este formato:

```text
CYCLE_ID:
OBJECTIVE:
IN_SCOPE:
OUT_OF_SCOPE:
PRECONDITIONS:
FILES_ALLOWED:
ACCEPTANCE_CRITERIA:
TESTS_REQUIRED:
DOCUMENTS_TO_UPDATE:
COMMIT_POLICY:
FINAL_REPORT_FORMAT:
```

Si alguno de estos campos no está definido, la tarea no debe comenzar.

---

## 6. Estado único de ejecución

Debe existir un único documento vivo:

```text
docs/RADAR_MVP_EXECUTION_STATE_V1.md
```

Debe contener únicamente:

```text
objetivo vigente
último ciclo cerrado
estado actual
bloqueos
siguiente acción permitida
fuera de alcance vigente
```

No debe convertirse en un historial extenso. El historial queda en Git y en los informes de laboratorio.

---

## 7. Criterio de cierre de ciclo

Un ciclo se considera cerrado solo cuando:

- cumple el objetivo declarado;
- no introduce deriva de alcance;
- los tests requeridos pasan o los fallos preexistentes están demostrados;
- `git diff --check` pasa;
- el estado del repo queda registrado;
- la fuente de verdad fue actualizada;
- existe una siguiente acción inequívoca.

---

## 8. Primera aplicación de este contrato

El próximo ciclo permitido es:

```text
CYCLE_ID: RADAR-MVP-BASELINE-001
OBJECTIVE: auditar el estado real del repo y establecer la línea base de implementación del MVP
IN_SCOPE: código existente, documentos rectores, pruebas, rama actual y gaps contra la propuesta aceptada
OUT_OF_SCOPE: integrar Playwright MCP, modificar producción, agregar dependencias, elegir CRM
DELIVERABLE: docs/RADAR_MVP_IMPLEMENTATION_BASELINE_V1.md
```

Hasta cerrar este ciclo, no corresponde continuar con integración productiva.

---

## 9. Principio rector

```text
El repo gobierna.
El ciclo limita.
La evidencia decide.
El chat asiste.
```
