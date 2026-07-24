# RADAR — Estado Actual del Proyecto

**Rama:** `experiment/playwright-crawlee-adoption-v1`
**Último commit:** integración del flujo Playwright → Evidence Pipe → Conversation
**Propósito:** handoff para que otro desarrollador continúe desde este punto.

---

## Objetivo de RADAR

RADAR es un instrumento de prospección conversacional, descubrimiento humano y precalificación para **Inlak'ech**. Encuentra conversaciones públicas relevantes, interpreta afinidad aparente, obliga a revisión humana y administra un embudo de descubrimiento hasta entregar leads calificados al CRM (Relaticle).

## Contrato MVP (USD 2400)

El MVP debe demostrar:

```text
descubrir → extraer evidencia → evaluar → revisar → aprobar → preparar oportunidad para CRM
```

No incluye CRM, mensajería automática ni cantidad fija de candidatos.

---

## Arquitectura actual

```
Playwright MCP (Chromium persistente)
→ NavigationRequest / NavigationResult
→ app/integrations/playwright_mcp.py (PlaywrightMCPClient)
→ app/discovery/playwright_adapter.py (adaptador)
→ DiscoveryResult
→ persist_discovery_results()
→ Conversation (SQLAlchemy, tabla conversations)
```

### Componentes clave

| Componente | Ruta | Rol |
|---|---|---|
| PlaywrightMCPClient | `app/integrations/playwright_mcp.py` | Chromium persistente vía MCP, navegación, snapshot, screenshot |
| NavigationResult | `app/integrations/playwright_mcp.py` | Contrato de salida: status, texto, URL, autor, screenshot, latencia |
| Adaptador | `app/discovery/playwright_adapter.py` | Convierte NavigationResult → DiscoveryResult, canonicaliza URL, normaliza source |
| persistence | `app/discovery/ingestion.py` | `persist_discovery_results()` — idempotente vía `source + external_id` |
| Conversation (ORM) | `app/models/conversation.py` | Tabla `conversations`, UniqueConstraint en `(source, external_id)` |
| Discovery contracts | `app/discovery/contracts.py` | DiscoveryResult (Pydantic) |
| Conversation schemas | `app/schemas/conversation.py` | ConversationCreate, conversation_orm_payload |

### Flujo de identidad (determinístico)

```text
external_id = pw:{sha256(source.strip().lower() : canonical_url)[:16]}
```

- **Canonicalización**: lowercase scheme+host, sin fragmento, sin slash final (excepto raíz), sin parámetros utm/fbclid/gclid, parámetros funcionales preservados en orden.
- **Source**: normalizado a lowercase sin espacios. Usado tanto para el hash como para `DiscoveryResult.source`.
- **Texto**: no participa en la identidad. Conservado como evidencia en `DiscoveryResult.text`.

### Estados de navegación

| Estado | Persiste | Descripción |
|---|---|---|
| SUCCESS | ✅ | Texto > 200 chars + autor detectado |
| EXTRACTION_PARTIAL | ✅ | Texto > 50 chars, autor opcional |
| EXTRACTION_FAILED | ❌ | Snapshot sin contenido utilizable |
| CAPTCHA_BLOCKED | ❌ | Keywords de captcha detectadas |
| LOGIN_REQUIRED | ❌ | Keywords de login detectadas |
| SESSION_LOST | ❌ | Sesión no iniciada o error no clasificado |
| MCP_CONNECTION_ERROR | ❌ | Error de conexión MCP |
| MCP_SERIALIZATION_ERROR | ❌ | Error de serialización MCP |

---

## Decisiones técnicas cerradas

- **Playwright MCP** sobre Crawlee Python (10/10 tareas, latencia media ~4s post-arranque).
- **Una sola instancia de Chromium**, sesión persistente.
- **`browser_snapshot`** para extracción de texto. Sin `browser_evaluate` (bug de serialización en cliente MCP Python).
- **Autor opcional** con estados `RESOLVED`, `PARTIAL`, `UNAVAILABLE`.
- **`final_url` real** extraído de respuesta `browser_navigate` (no copia de `requested_url`).
- **Screenshot** condicional via `browser_take_screenshot`.
- **`external_id` determinístico** sin timestamp/UUID/texto.
- **Deduplicación única** vía `source + external_id` en `persist_discovery_results`.

---

## Limitaciones conocidas

- `browser_evaluate` no disponible (bug de serialización del cliente MCP Python).
- Extracción de autor en Reddit: ~20 % (parcial).
- Sin `browser_evaluate`, no se puede extraer metadata estructurada desde el DOM.
- Los 6 estados de error bloqueados (CAPTCHA, LOGIN, etc.) no crean Conversation — la navegación debe reintentarse manualmente.

---

## Tests

| Suite | Tests | Estado |
|---|---|---|
| `test_playwright_mcp_integration.py` | 39 | ✅ Verde |
| `test_playwright_adapter.py` | 31 | ✅ Verde |
| `test_discovery_ingestion.py` | 1 | ✅ Verde |
| **Full suite** | **298 pass, 2 fail, 2 skip** | ✅ 0 regresiones |

### Fallos preexistentes (no resueltos)

```text
tests/test_assessment_v3_normalization.py::TestSingleRetry::test_format_error_triggers_retry
tests/test_assessment_v3_normalization.py::TestSingleRetry::test_second_format_error_still_fails
```

Son previos a todo el trabajo de Playwright. No modificados.

---

## Gaps pendientes

1. **Evaluación semántica integrada** — conectar Conversation persistida → `assessment_v3`.
2. **Revisión humana / Lista 1** — flujo HTMX completo para revisar conversaciones entrantes.
3. **`ApprovedOpportunityV1`** — contrato neutral con JSON, CSV y endpoint para entregar al CRM.
4. **Piloto integral** — demostrar el flujo completo de principio a fin.
5. **`TestSingleRetry`** — resolver o aceptar los 2 fallos preexistentes (más antiguo).

---

## Orden de lectura recomendado

```text
1. AGENTS.md                         — reglas del proyecto
2. docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md
3. docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md
4. docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_V1.md
5. docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_CLOSE_002.md
6. docs/specs/PLAYWRIGHT_TO_EVIDENCE_PIPE_V1.md
7. docs/specs/PLAYWRIGHT_EVIDENCE_IDENTITY_CLOSE_002.md
8. app/integrations/playwright_mcp.py
9. app/discovery/playwright_adapter.py
10. app/discovery/ingestion.py
11. app/discovery/contracts.py
12. app/models/conversation.py
13. tests/test_playwright_mcp_integration.py
14. tests/test_playwright_adapter.py
```

---

## Comandos

```bash
# Instalar dependencias
pip install -e ".[dev]"

# Ejecutar tests
pytest -q tests/test_playwright_mcp_integration.py
pytest -q tests/test_playwright_adapter.py
pytest -q tests/test_discovery_ingestion.py
pytest -q                          # suite completa

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload

# Ejecutar experimento Playwright (requiere npx y Chromium)
python scripts/experimento_playwright_mcp_runtime.py
```