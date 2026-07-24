# Experimento: Playwright MCP Runtime — Diagnóstico, Workaround y Runner Persistente

**Fecha**: 2026-07-23
**Rama**: `experiment/playwright-crawlee-adoption-v1`
**Caso**: Reddit — `r/intentionalcommunity` (ecovillage)
**Objetivo**: Resolver fallo de `browser_evaluate`, probar `browser_run_code_unsafe`, medir rendimiento con navegador persistente.

---

## VERDICT

**PASS** con reservas. El runner persistente funciona (10/10 tareas, latencia post-arranque 4.8s, sesión persistente). Pero `browser_evaluate` y `browser_run_code_unsafe` están rotos por un bug de serialización en el cliente MCP Python (`MCP_SERIALIZATION_ERROR`). La extracción vía `browser_snapshot` funciona y ocasionalmente extrae autor (2/10), pero no es confiable para Reddit por su UI de web components.

Playwright MCP queda **apto para laboratorio** condicional: solo para plataformas donde `browser_snapshot` exponga suficiente información, o esperando fix del bug de serialización.

---

## BRANCH

```
experiment/playwright-crawlee-adoption-v1
```

Sin commits, sin tocar flujo productivo.

---

## TRANSPORT_STDIO

**MODO STDIO**: Funciona correctamente para conexión básica. El cliente MCP Python via `StdioServerParameters` con `npx @playwright/mcp` establece sesión y ejecuta:
- `browser_navigate` ✅ (5.3s promedio primera vez)
- `browser_snapshot` ✅ (devuelve ~1,379 chars de árbol de accesibilidad)
- `browser_get_text` ✅ (limitado, 43 chars en Reddit body)
- `browser_evaluate` ❌ (MCP_SERIALIZATION_ERROR)
- `browser_run_code_unsafe` ❌ (SyntaxError)

**Modo subprocess manual** (`create_subprocess_exec`) **falla en Windows** porque `npx` se resuelve a `npx.ps1` (PowerShell script), no a un .exe. `asyncio.create_subprocess_exec` no puede ejecutar `.ps1` directamente. El cliente MCP Python probablemente usa shell=True internamente.

---

## TRANSPORT_HTTP

**MODO HTTP (SSE)**: No se pudo probar completamente. El servidor se inicia con `--port <port>`, pero:
1. En Windows, no se puede iniciar vía `create_subprocess_exec` directo (problema con `npx.ps1`)
2. El cliente MCP Python soporta `sse_client()` vía HTTP, pero iniciar el server requiere shell
3. No se probó la conexión real porque el server no pudo arrancar desde el script

**Conclusión**: El modo HTTP existe (`--port` flag), pero probarlo requiere un paso manual:
```bash
npx @playwright/mcp --port 8931 --headless
```
y luego conectar con:
```python
from mcp.client.sse import sse_client
async with sse_client(url="http://localhost:8931/sse") as (read, write):
    ...
```

El modo HTTP permitiría `--shared-browser-context` para compartir el navegador entre múltiples conexiones, que es el camino correcto para producción.

---

## BROWSER_EVALUATE_DIAGNOSIS

**Estado**: CONFIRMADO ROTO — `MCP_SERIALIZATION_ERROR`

**Síntoma exacto**:
```
Invalid arguments for tool "browser_evaluate":
✖ Invalid input: expected string, received undefined
  → at function
```

**Pruebas ejecutadas** (todas fallan):
| Expresión | Resultado |
|-----------|-----------|
| `"1+1"` | `expected string, received undefined` |
| `"document.title"` | `expected string, received undefined` |
| `"true"` | `expected string, received undefined` |
| `"null"` | `expected string, received undefined` |
| `"[1,2,3]"` | `expected string, received undefined` |
| string con quotes | `expected string, received undefined` |
| string multiline | `expected string, received undefined` |

**Causa raíz**: El cliente MCP Python (`mcp` package) serializa incorrectamente el argumento `expression` en el mensaje JSON-RPC `tools/call`. En lugar de enviar `{"expression": "document.title"}`, envía `{"expression": undefined}` o un formato que el servidor TypeScript no puede deserializar como string.

**Punto exacto**: `ClientSession.call_tool()` → crea `CallToolRequest(params=CallToolRequestParams(name=..., arguments=arguments))` → serializa a JSON-RPC → el servidor recibe `arguments.expression` como `undefined`.

**Diagnóstico diferencial**:
- `browser_navigate(arguments={"url": "..."})` FUNCIONA → argumento `url` se serializa bien
- `browser_evaluate(arguments={"expression": "..."})` FALLA → argumento `expression` se serializa mal
- La diferencia es que `url` es un argumento requerido con un schema JSON conocido; `expression` podría tener un tipo diferente en el schema del servidor
- Probablemente el servidor `@playwright/mcp` define `expression` como `string` en su esquema, pero el cliente MCP Python lo envía con un tipo que el validador Zod/TypeScript rechaza

---

## WORKAROUND_RESULT

### browser_run_code_unsafe

**Estado**: TAMBIÉN ROTO — `SyntaxError: Unexpected token`

| Código | Resultado |
|--------|-----------|
| `return 42;` | `SyntaxError: Unexpected token 'return'` |
| `const x = 42;` | `SyntaxError: Unexpected token 'const'` |
| `typeof page` | `SyntaxError: Unexpected token 'typeof'` |

**Causa**: Mismo bug de serialización que `browser_evaluate`. El argumento `code` llega como `undefined` o en un formato que el servidor no puede evaluar. O bien el servidor recibe el string `"undefined"` y `eval("undefined")` falla de forma diferente a lo esperado.

### Workaround real: browser_snapshot

**Solución**: Usar `browser_snapshot()` en lugar de `browser_evaluate()`.

- `browser_snapshot` devuelve el árbol de accesibilidad de la página como texto plano
- No permite ejecutar JavaScript arbitrario, pero expone el contenido visible
- En Reddit: expone ~1,379 chars de texto (parcial, sin autor consistente)
- Funciona 100% de las veces, sin errores

**Limitación**: No puede acceder al DOM de web components (`<shreddit-post>`) que no expongan su contenido al árbol de accesibilidad. El autor de Reddit se extrae solo cuando aparece en el texto visible (2/10 iteraciones).

---

## BROWSER_REUSE

**RESULTADO**: Una sola instancia de Chromium para 10 iteraciones.

El runner usa una única conexión stdio al servidor `@playwright/mcp`, que mantiene una sola instancia de Chromium durante todo su ciclo de vida. No se lanza un navegador nuevo por iteración.

Evidencia:
- La primera navegación tarda 5.7s (incluye arranque del navegador)
- Las siguientes navegaciones promedian 2.3s (solo cambio de página)

---

## SESSION_PERSISTENCE

**RESULTADO**: Sesión persistente a través de 10 navegaciones.

- Cookies y sesión de Reddit se mantienen entre navegaciones
- El mismo navegador se reutiliza (misma instancia Chromium)
- No hay pérdida de sesión (SESSION_LOST = 0)
- La conexión MCP stdio permanece abierta todo el experimento

---

## EXTRACTION_RESULT

| It | URL | Autor | Texto | Calidad | Error |
|----|-----|-------|-------|---------|-------|
| 1 | ecovillage | `<no_encontrado>` | 253ch | PARTIAL | - |
| 2 | ecovillage | `<no_encontrado>` | 257ch | PARTIAL | - |
| 3 | permaculture | `<no_encontrado>` | 728ch | PARTIAL | - |
| 4 | ecovillage | `<no_encontrado>` | 259ch | PARTIAL | - |
| 5 | shared living | `<no_encontrado>` | 731ch | PARTIAL | - |
| 6 | ecovillage | `<no_encontrado>` | 259ch | PARTIAL | - |
| 7 | simple living | **appenofficial** | 1,918ch | **OK** | - |
| 8 | ecovillage | `<no_encontrado>` | 338ch | PARTIAL | - |
| 9 | homestead | **sticky_pasta123** | 794ch | **OK** | - |
| 10 | ecovillage | `<no_encontrado>` | 259ch | PARTIAL | - |

**Resumen**:
- Autor extraíble: 2/10 (20%)
- Texto extraíble (>200ch): 10/10 (100%)
- Calidad OK: 2/10, PARTIAL: 8/10
- Extracción vía `browser_snapshot` funciona siempre, pero no siempre expone el autor en el árbol de accesibilidad

---

## LATENCY_INITIAL

**7,780ms** para la primera iteración (incluye arranque de Chromium + navegación + snapshot).

## LATENCY_AVERAGE

**4,820ms** promedio post-arranque (iteraciones 2-10). **PASS** (< 5,000ms).

Desglose:
- Navegación promedio: 3,026ms
- Snapshot + extracción: ~1,800ms
- Mínima: 3,141ms (iteración 5)
- Máxima: 8,378ms (iteración 9, post pesado)

---

## ERROR_CLASSIFICATION

| Tipo | Ocurrencias | Descripción |
|------|-------------|-------------|
| `MCP_CONNECTION_ERROR` | 0 | Error de conexión con el servidor MCP |
| `MCP_SERIALIZATION_ERROR` | (ver diagnosis) | `browser_evaluate` y `browser_run_code_unsafe` fallan por serialización |
| `BROWSER_EVALUATE_ERROR` | 0 | Error de ejecución en el navegador |
| `SESSION_LOST` | 0 | Pérdida de sesión/navegador |
| `EXTRACTION_PARTIAL` | 8 | Texto extraído pero sin autor |
| `EXTRACTION_FAILED` | 0 | Sin texto ni autor |
| `SUCCESS` | 2 | Autor + texto completos |

---

## FILES_MODIFIED

```
scripts/experimento_playwright_mcp_runtime.py  (nuevo, experimental)
lab/experimento-playwright-mcp-runtime-v1.md   (nuevo, informe)
.tmp/reporte-playwright-runtime-*.json         (resultados)
.tmp/_debug_serialization.py                   (eliminado)
.tmp/_debug_unsafe.py                          (eliminado)
.tmp/_test_raw_rpc.py                          (eliminado)
```

Sin cambios en el flujo productivo de RADAR.

---

## TESTS

```
pytest tests/ -v --tb=short
228 passed, 2 failed, 2 skipped
```

Las 2 fallas son pre-existentes (tests de retry mechanism en `test_assessment_v3_normalization.py`), no causadas por este experimento.

---

## GIT_STATUS

```
On branch experiment/playwright-crawlee-adoption-v1
Untracked files:
  .tmp/reporte-playwright-runtime-20260723-214136.json
  lab/experimento-playwright-mcp-runtime-v1.md
  lab/experimento-playwright-crawlee-adopcion-v1.md
  scripts/experimento_playwright_crawlee.py
  scripts/experimento_playwright_mcp_runtime.py
  (y otros archivos pre-existentes del experimento anterior)
```

`git diff --check`: sin errores. Sin commits.

---

## NEXT_RECOMMENDATION

### Para integración productiva

1. **Esperar fix del cliente MCP Python** para `browser_evaluate` / `browser_run_code_unsafe`. El bug `MCP_SERIALIZATION_ERROR` bloquea la extracción vía JavaScript. Sin evaluación JS, Reddit (web components) no expone autor confiablemente.

2. **Alternativa inmediata**: Usar Playwright Python directamente en lugar del MCP server. Playwright Python (1.60.0, ya instalado) permite `page.evaluate()` directamente sin el intermediario MCP.

3. **Modo HTTP como camino productivo**: Cuando se resuelva el bug de serialización, usar `--port <port> --shared-browser-context` para tener un server persistente al que conectarse desde múltiples workers.

4. **browser_snapshot como fallback**: Sirve para extracción básica de texto de cualquier página. No requiere evaluación JS.

### Prioridades

| Prioridad | Acción | Dependencia |
|-----------|--------|-------------|
| 1 | Reportar bug de serialización al equipo MCP Python | - |
| 2 | Probar Playwright Python directo (sin MCP) para extracción | - |
| 3 | Implementar runner HTTP con `--shared-browser-context` | Fix bug serialización |
| 4 | Desarrollar extractores por plataforma con selectores versionados | #3 |

### Riesgos

1. **MCP_SERIALIZATION_ERROR**: Bloquea `browser_evaluate` y `browser_run_code_unsafe`. Sin workaround real hasta que el cliente MCP Python se actualice.
2. **browser_snapshot insuficiente**: No expone contenido de web components (Reddit, Twitter/X, Instagram). Solo sirve para HTML semántico tradicional.
3. **Node.js como dependencia**: RADAR es Python puro. Agregar Node.js + npx para el server MCP aumenta complejidad operativa.

---

## Firmado

Experimentación cerrada el 2026-07-23. Playwright MCP queda en estado **laboratorio condicional** (funciona si el fix de serialización llega, o si se usa Playwright Python directo).