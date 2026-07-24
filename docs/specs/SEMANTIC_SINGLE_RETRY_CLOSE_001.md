# RADAR — SEMANTIC SINGLE RETRY CLOSE 001

**Cycle ID:** `RADAR-SEMANTIC-RETRY-CLOSE-001`  
**Status:** `APPROVED`  
**Scope:** cierre focal de los dos fallos `TestSingleRetry`  
**Repository:** `E:\BuenosPasos\inlakech-radar`

---

## 1. Objetivo único

Restaurar el contrato de un único reintento ante una salida semántica con formato inválido, sin alterar la lógica de negocio, la cascada semántica, el failover de proveedores ni la evaluación final.

Flujo esperado:

```text
primer intento
→ salida con formato inválido
→ un único segundo intento
→ éxito o INVALID_MODEL_OUTPUT definitivo
```

---

## 2. Evidencia del defecto

La suite actual registra exactamente dos fallos:

```text
TestSingleRetry.test_format_error_triggers_retry
TestSingleRetry.test_second_format_error_still_fails
```

Ambos muestran:

```text
esperado: 2 llamadas al runner
real: 1 llamada
```

En `app/semantics/conversation_assessment_v3.py`, `assess_conversation_v3()` captura inmediatamente:

- `InvalidModelOutputError`;
- `ValidationError`;
- `json.JSONDecodeError`.

Ante cualquiera de esos errores devuelve `INVALID_MODEL_OUTPUT` sin ejecutar el segundo intento.

Los tests vigentes documentan explícitamente:

> Retry único solo por error de formato, no por error de proveedor.

No existe evidencia documental de que este contrato haya sido eliminado.

---

## 3. Comportamiento autorizado

### Debe reintentar una sola vez ante

- `InvalidModelOutputError`;
- `ValidationError` surgido al validar la salida del modelo;
- `json.JSONDecodeError` asociado a una salida inválida.

### No debe reintentar ante

- `SemanticProviderError`;
- timeout;
- conexión fallida;
- proveedor no disponible;
- configuración ausente;
- motor semántico deshabilitado;
- cualquier excepción no clasificada como error de formato.

### Límite obligatorio

Máximo total:

```text
2 ejecuciones del runner
```

No se autoriza loop, backoff, espera, retry configurable ni dependencia nueva.

---

## 4. Implementación mínima esperada

1. Construir una sola vez el `active_runner`.
2. Construir una sola vez el texto de entrada.
3. Ejecutar primer intento.
4. Ante error de formato, ejecutar un segundo y último intento con la misma entrada.
5. Si el segundo intento vuelve a fallar por formato, devolver:

```text
assessment_status = INVALID_MODEL_OUTPUT
safe_error_code = INVALID_MODEL_OUTPUT
```

6. Si el segundo intento es válido, continuar por `finalize_draft_v3()` sin alterar campos, evidencia ni reglas semánticas.
7. Si cualquiera de los intentos produce `SemanticProviderError`, devolver `SEMANTIC_ASSESSMENT_UNAVAILABLE` sin otro intento.

---

## 5. Archivos autorizados

```text
app/semantics/conversation_assessment_v3.py
tests/test_assessment_v3_normalization.py
docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md
docs/specs/SEMANTIC_SINGLE_RETRY_CLOSE_001.md
```

Modificar tests solo si es necesario para reforzar el contrato, nunca para ocultar el defecto.

---

## 6. Archivos y áreas prohibidas

No tocar:

- Playwright MCP;
- Evidence Pipe;
- persistencia de `Conversation`;
- `semantic_cascade_v1.py`;
- configuración de proveedores;
- failover Agnes/Gemma;
- interfaz HTMX;
- Lista 1;
- `ApprovedOpportunityV1`;
- CRM-ready;
- modelos de base de datos;
- migraciones;
- dependencias.

---

## 7. Invariantes

- Sin error, el runner se invoca una vez.
- Con un error de formato inicial y éxito posterior, se invoca dos veces y el resultado es `COMPLETED`.
- Con dos errores de formato consecutivos, se invoca dos veces y el resultado es `INVALID_MODEL_OUTPUT`.
- Ante `SemanticProviderError`, se invoca una sola vez.
- No se inventa evidencia.
- No se relaja `extra="forbid"`.
- No se modifica el contrato semántico V3.
- No se agrega un segundo sistema de retry.

---

## 8. Pruebas obligatorias

Ejecutar:

```text
pytest -q tests/test_assessment_v3_normalization.py
pytest -q tests/test_semantic_cascade_v1.py
pytest -q
```

Verificar específicamente:

1. error de formato inicial → segundo intento → `COMPLETED`;
2. dos errores de formato → exactamente dos llamadas → `INVALID_MODEL_OUTPUT`;
3. error de proveedor → exactamente una llamada;
4. resultado válido inicial → exactamente una llamada;
5. esquema estricto intacto;
6. suite completa sin regresiones.

Además:

```text
git diff --check
git status --short
/ponytail-review
```

---

## 9. Criterio de cierre

El ciclo pasa a `VERIFIED` únicamente cuando:

- los dos fallos desaparecen;
- la suite completa queda verde salvo skips aceptados;
- no se toca ninguna capa fuera de alcance;
- existe como máximo un reintento;
- Ponytail no detecta sobreestructura relevante;
- la documentación de estado queda actualizada con evidencia reproducible.

---

## 10. Reporte requerido

```text
VERDICT
CAUSE_CONFIRMED
FILES_MODIFIED
RETRY_TRIGGER_ERRORS
NO_RETRY_ERRORS
MAX_RUNNER_CALLS
FOCAL_TESTS
CASCADE_TESTS
FULL_SUITE
REGRESSIONS
PONYTAIL_REVIEW
DIFF_CHECK
GIT_STATUS
DOCS_UPDATED
NEXT_RECOMMENDATION
```
