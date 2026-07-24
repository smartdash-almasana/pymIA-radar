# RADAR MVP — ESTADO DE IMPLEMENTACIÓN V1

**Proyecto:** Inlak’ech RADAR  
**Propósito:** fuente operativa de verdad para continuar el desarrollo sin depender del chat  
**Estado:** ACTIVO  
**Contrato comercial aplicable:** RADAR Inlak’ech MVP — USD 2.400 — Versión 3 corregida

---

## 1. Regla de autoridad

Este archivo registra el estado operativo actual del MVP.

El chat, OpenCode y otros agentes pueden proponer o ejecutar tareas, pero no son la fuente de verdad.

Orden práctico para continuar:

1. contrato comercial vigente;
2. `docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md`;
3. este archivo;
4. especificación aprobada del ciclo activo;
5. código, tests e informes como evidencia.

Cada ciclo debe actualizar este archivo al cerrar.

---

## 2. Objetivo contractual del MVP

RADAR debe demostrar idoneidad como herramienta de descubrimiento y filtrado:

```text
descubrir
→ extraer evidencia
→ evaluar
→ revisar
→ aprobar
→ preparar oportunidad para CRM
```

El MVP no incluye CRM, mensajería automática ni garantía de cantidad fija de candidatos.

---

## 3. Alcance comprometido

### Incluido

- fuentes públicas mediante conectores existentes o de bajo costo técnico;
- laboratorio MCP Playwright en Facebook, Instagram, LinkedIn y TikTok;
- estabilización de un worker Playwright para la plataforma que demuestre mejor idoneidad;
- evidencia, normalización y deduplicación;
- evaluación semántica;
- revisión humana HTMX;
- contrato neutral `ApprovedOpportunityV1`;
- exportación JSON y CSV;
- endpoint interno de lectura;
- piloto integral de aceptación;
- documentación y pruebas.

### Excluido

- CRM;
- selección del CRM;
- integración activa con un CRM específico;
- mensajería automática;
- WhatsApp, email marketing o seguimiento comercial;
- evasión agresiva de CAPTCHAs o bloqueos;
- promesa de cantidad fija de candidatos;
- cuatro workers productivos completos.

---

## 4. Estado técnico confirmado

### 4.1 Herramienta de navegador

```text
Playwright MCP: SELECCIONADO
Crawlee Python: DESCARTADO
```

Evidencia experimental:

- 10/10 tareas completadas;
- una sola instancia de Chromium;
- sesión persistente;
- latencia media posterior al arranque: 4,3 segundos;
- navegación, snapshot, texto y URL: aptos;
- `browser_evaluate`: no disponible por bug de serialización del cliente MCP Python;
- autor en Reddit: extracción parcial, aproximadamente 20 %.

Decisión:

> Integrar Playwright MCP como navegador persistente y extractor de texto/URL. No diseñar el flujo productivo suponiendo que `browser_evaluate` funciona.

Integración runner base:

> `app/integrations/playwright_mcp.py` — `PlaywrightMCPClient` implementado y verificado.
> Ciclo `RADAR-PLAYWRIGHT-RUNNER-001` cerrado. Especificación `VERIFIED`.

Cierre técnico:

> Ciclo `RADAR-PLAYWRIGHT-RUNNER-CLOSE-002`: `final_url` extraído real de `browser_navigate` (no copia de `requested_url`); `browser_take_screenshot` integrado con `capture_screenshot=True`; clasificación real de errores (`CAPTCHA_BLOCKED`, `LOGIN_REQUIRED`, `MCP_SERIALIZATION_ERROR`, `MCP_CONNECTION_ERROR`, `SESSION_LOST`). Sin `browser_evaluate`. Especificación `VERIFIED`.

### 4.2 Semántica

Existe:

- evaluación V3;
- skill versionada;
- schema estricto;
- normalizador;
- reintento único;
- anti-patrones;
- evidencia literal;
- fallback/failover.

Pendiente:

- ejecutar corpus contractual de aceptación;
- demostrar al menos 95 % de salidas estructuralmente válidas;
- demostrar al menos 80 % de concordancia humana en casos claros;
- demostrar 0 `CLEAR` en anti-patrones inmobiliarios, turísticos o promocionales evidentes.

### 4.3 Interfaz

Existe bandeja HTMX y flujo de revisión.

Pendiente verificar contractualmente:

```text
abrir conversación
→ ver evidencia
→ abrir fuente
→ aprobar / observar / descartar
```

sin errores bloqueantes.

### 4.4 CRM-ready

Existe código histórico de transferencia, pero no debe asumirse equivalente al contrato nuevo.

Pendiente implementar o verificar expresamente:

```text
ApprovedOpportunityV1
```

con:

- identificador estable;
- estados `READY_FOR_CRM`, `EXPORTED`, `TRANSFER_CONFIRMED`, `TRANSFER_FAILED`;
- `external_crm_id`;
- JSON;
- CSV;
- endpoint interno;
- tests de validación.

---

## 5. Alineación con el contrato

```text
ARQUITECTURA: ALINEADA
PLAYWRIGHT: PROBADO Y APTO CON ALCANCE LIMITADO
SEMÁNTICA: IMPLEMENTADA, PENDIENTE DE CIERRE CONTRACTUAL
INTERFAZ: MAYORMENTE IMPLEMENTADA
CRM-READY: PENDIENTE
PILOTO INTEGRAL: PENDIENTE
DERIVA: NO DETECTADA
```

Alineación estimada actual: 75–80 %.

---

## 6. Gaps contractuales pendientes

1. Integrar el persistent runner dentro de RADAR.
2. Formalizar autor opcional mediante estado:
   - `RESOLVED`;
   - `PARTIAL`;
   - `UNAVAILABLE`.
3. Cerrar o reconciliar los dos tests semánticos preexistentes.
4. Implementar `ApprovedOpportunityV1` neutral con JSON, CSV y endpoint.
5. Ejecutar el piloto contractual completo.

---

## 7. Ciclos cerrados

### ID

```text
RADAR-PLAYWRIGHT-RUNNER-001
```

### Resultado

```text
ESTADO: COMPLETADO
```

### Evidencia

- `app/integrations/playwright_mcp.py`: `PlaywrightMCPClient` con Chromium persistente, sesión única, navegación y extracción vía `browser_snapshot`. Sin `browser_evaluate`.
- `tests/test_playwright_mcp_integration.py`: 39 tests focales (modelos, extracción de autor, texto visible, lifecycle, URL final, screenshot, clasificación de errores). 39/39 verdes.
- Verificación real: 10/10 navegaciones consecutivas, Chromium único, sesión persistente, latencia media post-arranque ~4s (< 5s).
- `docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_V1.md`: especificación `APPROVED` → `VERIFIED`.
- Regresiones: 0. Suite completa: 267 passed, 2 pre-existing failures (`TestSingleRetry`).

### Artefactos

- `app/integrations/playwright_mcp.py`
- `tests/test_playwright_mcp_integration.py`
- Dependencia `mcp>=1.0` agregada a `pyproject.toml`

---

### ID

```text
RADAR-PLAYWRIGHT-RUNNER-CLOSE-002
```

### Resultado

```text
ESTADO: VERIFIED
```

### Evidencia

- `final_url` extraído real desde respuesta `browser_navigate` (patrón `- Page URL: <url>`). No replica `requested_url` sin verificación.
- `browser_take_screenshot` integrado cuando `capture_screenshot=True`. `screenshot_path` apunta a archivo real en `.tmp/screenshots/`.
- Clasificación real de errores:
  - `CAPTCHA_BLOCKED`: detección por palabras clave en snapshot.
  - `LOGIN_REQUIRED`: detección por palabras clave en snapshot.
  - `MCP_SERIALIZATION_ERROR`: por excepción con `Serialization` en nombre.
  - `MCP_CONNECTION_ERROR`: por excepción con `Connection` o error en `browser_navigate`.
  - `SESSION_LOST`: por sesión no iniciada o excepción no clasificada.
  - `EXTRACTION_FAILED`: por fallo de snapshot.
- Sin `browser_evaluate`. Sin nuevas dependencias.
- 39 tests focales, 267 suite pass, 2 pre-existing failures, 0 regresiones.
- `docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_CLOSE_002.md`: `APPROVED` → `VERIFIED`.

---

### ID

```text
RADAR-PLAYWRIGHT-EVIDENCE-001
```

### Resultado

```text
ESTADO: VERIFIED
```

### Evidencia

- `app/discovery/playwright_adapter.py`: adaptador que convierte `NavigationResult` → `DiscoveryResult` usando `persist_discovery_results`. Sin duplicación.
- Admite: `SUCCESS` y `EXTRACTION_PARTIAL`. Rechaza: `EXTRACTION_FAILED`, `SESSION_LOST`, `MCP_CONNECTION_ERROR`, `MCP_SERIALIZATION_ERROR`, `CAPTCHA_BLOCKED`, `LOGIN_REQUIRED`.
- `final_url=None` y `texto < 50` chars rechazados.
- `external_id` original: `pw:{sha256(source:final_url:text[:100])[:16]}` (incluía texto). Sin timestamp ni UUID.
- `engagement` preserva `requested_url`, `final_url`, `author_status`, `navigation_status`, `screenshot_path`, `latency_ms`.
- `process_and_persist()` para integración en un solo paso.
- `tests/test_playwright_adapter.py`: 13 tests focales (mapeo, estado determinístico, idempotencia, rechazo de bloqueados, URL inválida, texto corto, autor nulo, título/contexto).
- Suite completa: 280 pass, 2 pre-existing failures (`TestSingleRetry`), 2 skipped. **0 regresiones nuevas.**
- `docs/specs/PLAYWRIGHT_TO_EVIDENCE_PIPE_V1.md`: `APPROVED` → `VERIFIED`.

### Artefactos

- `app/discovery/playwright_adapter.py`
- `tests/test_playwright_adapter.py`

---

### ID

```text
RADAR-PLAYWRIGHT-EVIDENCE-ID-CLOSE-002
```

### Resultado

```text
ESTADO: VERIFIED
```

### Evidencia

- `external_id` ya no depende del texto. Identidad determinada exclusivamente por `normalized_source + URL canónica`.
- `source` se normaliza con `source.strip().lower()` y se usa tanto para `external_id` como para `DiscoveryResult.source`. Variantes como `"Reddit"`, `" reddit "`, `"reddit"` producen el mismo `external_id` y la misma `Conversation`.
- Función `_canonicalize_url()` agregada en `app/discovery/playwright_adapter.py`: lowercase scheme+host, elimina fragmento, elimina slash final (excepto raíz), elimina parámetros de rastreo conocidos (`utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `fbclid`, `gclid`), preserva parámetros funcionales en orden.
- `conversation_url` conserva `final_url` original. `final_url` original conservado en `engagement`.
- `navigation_to_discovery()` y `process_and_persist()` preservados sin cambios de firma.
- `persist_discovery_results()` sigue siendo el único punto de persistencia. Sin nueva deduplicación.
- `tests/test_playwright_adapter.py`: 31 tests focales (9 de canonicalización + 17 de adaptador + 5 de persistencia, incluyendo `test_source_is_normalized_for_identity_and_persistence` y `test_idempotent_source_variants`). Todos verifican identidad independiente del texto y normalización de source.
- Suite completa: 298 pass, 2 pre-existing failures (`TestSingleRetry`), 2 skipped. **0 regresiones nuevas.**
- `docs/specs/PLAYWRIGHT_EVIDENCE_IDENTITY_CLOSE_002.md`: `APPROVED` → `VERIFIED`.

### Artefactos

- `app/discovery/playwright_adapter.py` (modificado)
- `tests/test_playwright_adapter.py` (modificado)

---

## 8. Estado técnico actualizado

```text
PLAYWRIGHT MCP RUNNER: VERIFICADO Y CERRADO TÉCNICAMENTE
EVIDENCE PIPE: INTEGRADO CON PLAYWRIGHT
IDENTIDAD PLAYWRIGHT: CORREGIDA (URL canónica, source normalizado, sin texto)
ARQUITECTURA: ALINEADA
SEMÁNTICA: IMPLEMENTADA, PENDIENTE DE CIERRE CONTRACTUAL
INTERFAZ: MAYORMENTE IMPLEMENTADA
CRM-READY: PENDIENTE
PILOTO INTEGRAL: PENDIENTE
DERIVA: NO DETECTADA
```

Alineación estimada actual: 90–95 %.

### Gaps contractuales pendientes

1. ~~Integrar el persistent runner dentro de RADAR.~~ ✅
2. ~~Formalizar autor opcional mediante estado (RESOLVED/PARTIAL/UNAVAILABLE).~~ ✅
3. ~~Cierre técnico: final_url real, screenshot, clasificación de errores.~~ ✅
4. ~~Integrar runner con Evidence Pipe existente.~~ ✅
5. ~~Corregir identidad determinística de evidencia Playwright.~~ ✅
6. ~~Cerrar los dos tests semánticos preexistentes.~~ ✅
7. Implementar `ApprovedOpportunityV1` neutral con JSON, CSV y endpoint.
8. Ejecutar el piloto contractual completo.

---

## 9. Próximo paso exacto permitido

```text
Evidence Pipe integrado
→ evaluación semántica existente sobre evidencia Playwright
→ revisión humana / Lista 1
```

La integración con Evidence Pipe está completa. El siguiente paso es usar el flujo completo:

```text
PlaywrightMCPClient.navigate()
→ navigation_to_discovery()
→ persist_discovery_results()
→ Conversation (persistida con evidencia)
→ evaluación semántica existente
```

El ciclo semántico de reintento único quedó cerrado:

```text
CYCLE_ID: RADAR-SEMANTIC-RETRY-CLOSE-001
ESTADO: VERIFIED
EVIDENCIA: 28 focales + 11 cascade + suite completa 300 passed, 2 skipped
```

El próximo ciclo permitido es integrar y verificar el recorrido:

```text
Conversation persistida desde Playwright
→ evaluación semántica V3 existente
→ persistencia de ConversationAssessmentV3
→ revisión humana / Lista 1
```

---

## 9. Regla de continuidad entre chats

Al comenzar un nuevo chat, leer en este orden:

```text
docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md
docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md
docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_V1.md
docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_CLOSE_002.md
docs/specs/PLAYWRIGHT_TO_EVIDENCE_PIPE_V1.md
docs/specs/PLAYWRIGHT_EVIDENCE_IDENTITY_CLOSE_002.md
```

No reconstruir decisiones desde memoria ni desde conversaciones anteriores.


---

## Ciclo cerrado — RADAR-PLAYWRIGHT-SEMANTIC-INTEGRATION-001

**Estado:** `VERIFIED`

Flujo demostrado en campaña controlada:

```text
NavigationResult
→ DiscoveryResult
→ Conversation
→ evaluación semántica V3
→ ConversationAssessmentV3
→ PresumptiveCandidate cuando corresponde
```

Evidencia:

- `app/services/semantic_integration.py`: servicio focal de integración;
- `app/api/routes.py`: reutiliza `persist_cascade_assessment()` y evita duplicar el mapeo semántico;
- `app/services/presumptive_candidates.py`: una reevaluación actualiza el candidato existente para la misma conversación en lugar de crear duplicados conceptuales;
- candidato persistido de forma durable mediante commit explícito;
- endpoint V3 exitoso y gate de revisión humana verificados;
- autor ausente conserva `author_status=UNAVAILABLE` en trazabilidad;
- pruebas focales relacionadas: 30 passed;
- suite completa: 312 passed, 2 skipped;
- regresiones: 0.

Próximo gap contractual:

```text
ApprovedOpportunityV1
→ JSON / CSV / endpoint interno
→ piloto integral de aceptación
```
