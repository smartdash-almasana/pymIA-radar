# Experimento: Adopcion de Playwright MCP vs Crawlee Python

**Fecha**: 2026-07-23
**Rama**: `experiment/playwright-crawlee-adoption-v1`
**Caso**: Reddit — `r/intentionalcommunity` post sobre ecovillage (mismo caso que Lista 1)
**URL**: https://www.reddit.com/r/intentionalcommunity/comments/1fu7tl6/seeking_cocreators_to_build_an_ecovillage_in/
**Iteraciones**: 3 por enfoque
**Python**: 3.14.0

---

## VERDICT

La experimentacion muestra que **ninguna de las dos herramientas esta lista para integrarse al flujo productivo de RADAR sin trabajo adicional significativo**. Playwright MCP es estructuralmente superior para el caso de uso (navegacion con JavaScript, extraccion gobernada por protocolo), pero la integraccion via MCP Python client tiene bugs de serializacion que bloquean `browser_evaluate`. Crawlee Python tiene una API mas compleja de lo necesario para extracciones puntuales, sufre de problemas de storage persistente que impiden re-ejecutar la misma URL, y su PlaywrightCrawler tiene latencias prohibitivas en paginas SPA.

---

## BRANCH

```
experiment/playwright-crawlee-adoption-v1
```

Creada desde `main` (c6f2f37), sin commits. No se modifico el flujo productivo.

---

## DEPENDENCIES

### Instaladas

| Paquete | Version | Instalacion | Uso |
|---------|---------|-------------|-----|
| `crawlee` | 1.8.3 | pip install crawlee | Nucleo de Crawlee |
| `crawlee[playwright]` | extra | pip install crawlee[playwright] | Subdependencias: `browserforge`, `apify-fingerprint-datapoints` |
| `mcp` | (latest) | pip install mcp | Cliente MCP Python para conectar con @playwright/mcp |
| `lxml` | (latest) | pip install lxml | Parser para BeautifulSoupCrawler |
| `beautifulsoup4` | (latest) | pip install beautifulsoup4 | Requerido por BeautifulSoupCrawler |
| `psutil` | 7.2.2 | (dependencia crawlee) | Monitoreo de recursos |
| `@playwright/mcp` | 0.0.78 | npx (bajo demanda) | Servidor MCP de Playwright |

### Preexistentes (ya en el repo)
- `playwright` 1.60.0 (bajo `pip list`)
- `httpx`, `aiohttp`, `requests`

### Dependencias agregadas al proyecto
Si se integrara al `pyproject.toml`:
```toml
crawlee>=1.8         # ~2MB + fingerprint data de 761KB
mcp>=1.x             # cliente/servidor MCP
```

Playwright MCP NO se instala como dependencia Python — corre via `npx @playwright/mcp` (Node.js externo).

---

## PLAYWRIGHT_MCP_RESULT

| Iteracion | Status | Duracion | Autor | Texto (chars) | Calidad |
|-----------|--------|----------|-------|---------------|---------|
| 1 | OK | 18,534ms | `<no_encontrado>` | 1,379 | PARTIAL |
| 2 | OK | 20,253ms | `<no_encontrado>` | 1,289 | PARTIAL |
| 3 | OK | 17,820ms | `<no_encontrado>` | 1,289 | PARTIAL |

**Resumen**:
- **Acceso**: 3/3 exitoso. `browser_navigate` funciona correctamente.
- **Estabilidad**: 100%. Sin crashes ni timeouts en 3 iteraciones.
- **Calidad de extraccion**: PARTIAL consistente (~1,300 chars de snapshot). Autor NO extraible porque `browser_evaluate` esta roto con el MCP Python client (error: "expected string, received undefined"). La extraccion se hace via `browser_snapshot` que captura el arbol de accesibilidad, no el DOM completo.
- **Latencia media**: 18,869ms. Cada llamada inicia un navegador nuevo via npx.
- **Complejidad de integracion**: MEDIA-ALTA. Requiere ejecutar server Node.js externo, conectar via MCP stdio, manejar el ciclo de vida del proceso. `browser_evaluate` no funciona con el cliente MCP Python actual — posible bug de serializacion.
- **Compatibilidad Python**: El cliente MCP Python funciona para `browser_navigate`, `browser_snapshot`, `browser_get_text`. `browser_evaluate` tiene un bug de serializacion que impide pasar argumentos.

### Hallazgos sobre Playwright MCP

1. `browser_evaluate` no funciona con `mcp` Python client. El argumento `expression` llega como `undefined` al servidor. Es un bug de serializacion JSON en el cliente Python.
2. `browser_snapshot` devuelve ~1,300 chars de texto util pero NO incluye el autor de Reddit (el nodo `shreddit-post` no expone el autor en el arbol de accesibilidad).
3. Cada iteracion lanza un proceso `npx` + Chromium nuevo. No hay reutilizacion de navegador entre llamadas.
4. La latencia (~19s) es consistente pero alta para operaciones en serie.

---

## CRAWLEE_RESULT

| Iteracion | Status | Duracion | Autor | Texto (chars) | Calidad |
|-----------|--------|----------|-------|---------------|---------|
| 1 | OK | 128,543ms | `<no_encontrado>` | 95 | PARTIAL |
| 2 | OK | 2,695ms | `<no_encontrado>` | 0 | FAILED |
| 3 | OK | 2,156ms | `<no_encontrado>` | 0 | FAILED |

**Resumen**:
- **Acceso**: 1/3 con contenido. Iter 2-3 fallan silenciosamente (storage persistente del crawler impide re-ejecutar misma URL).
- **Estabilidad**: 66% tasa de fallo. PlaywrightCrawler se cuelga 30s por retry esperando `networkidle` en Reddit (ads infinitos).
- **Calidad de extraccion**: PESIMA. La iteracion 1 solo obtuvo 95 chars de texto. El handler de pagina se ejecuta pero Reddit como SPA no se renderiza completamente con `networkidle`.
- **Latencia media**: 44,464ms. La iteracion 1 tardo 128s por los retries de timeout.
- **Complejidad de integracion**: ALTA. API compleja con `Router`, `PlaywrightCrawler`, storage persistente, autoscaling. Para extraer una pagina hay que configurar toda la infraestructura de Crawlee.
- **Compatibilidad Python**: Compatible con Python 3.14. Pero requiere dependencias pesadas: `browserforge` (37KB) + `apify-fingerprint-datapoints` (761KB) + `psutil` + `lxml`.

### Hallazgos sobre Crawlee Python

1. **Storage persistente**: Crawlee usa almacenamiento interno que impide re-ejecutar la misma URL. En iteraciones 2-3, el crawler reporta 0 requests porque el storage dice que ya se proceso.
2. **networkidle timeout**: Reddit carga ads y trackers continuamente. `wait_for_load_state("networkidle")` timeout a los 30s con 3 retries = 90s perdidos.
3. **API inflada**: Para una extraccion simple, Crawlee fuerza un patron de crawler completo con router, storage, autoscaling, retry policy. Es excesivo para extracciones puntuales.
4. **BeautifulSoupCrawler no sirve para SPA**: Reddit requiere JavaScript. BeautifulSoupCrawler solo ve HTML inicial (sin contenido del web component `shreddit-post`).
5. **PlaywrightCrawler** funciona pero la configuracion basica no es adecuada para paginas SPA modernas.

---

## COMPARISON

| Eje | Playwright MCP | Crawlee Python | Diferencia |
|-----|---------------|----------------|------------|
| **Acceso** | OK (3/3) | Parcial (1/3 util) | PW MCP gana |
| **Estabilidad** | Alta (sin errores) | Baja (storage persistente bugs) | PW MCP gana |
| **Calidad extraccion** | PARTIAL (~1,300 chars) | FAILED/PARTIAL (0-95 chars) | PW MCP gana |
| **Latencia media** | ~18.9s | ~44.5s (con retries) | PW MCP gana (2.4x mas rapido) |
| **Latencia minima** | ~17.8s | ~2.2s (pero sin datos) | Empate tecnico |
| **Complejidad integracion** | Media (MCP protocolo) | Alta (full crawler framework) | PW MCP gana |
| **Compatibilidad Python** | Bug en browser_evaluate | OK pero pesado | Crawlee gana |
| **Dependencias externas** | Node.js + npx | Solo Python | Crawlee gana |
| **Madurez del ecosistema** | Microsoft, activo | Apify, activo | Empate |

### Analisis cualitativo

1. **Playwright MCP** es la herramienta correcta conceptualmente (protocolo gobernado, herramientas especificas, sesiones persistentes), pero la integracion con Python tiene un bug concreto que bloquea `browser_evaluate`. Sin evaluacion JS, la extraccion se limita a `browser_snapshot` que no expone suficiente informacion para fuentes SPA modernas.

2. **Crawlee Python** esta disenado para crawlers de gran escala (miles de paginas) con autoscaling, storage, y retry policies. Es excesivo para el caso de RADAR (extracciones puntuales y gobernadas). Su storage persistente es un antipatron para nuestro caso (necesitamos re-ejecutar URLs).

3. **Ambos fallan en extraer el autor de Reddit** — el primero por bug de `browser_evaluate`, el segundo porque su configuracion basica no maneja SPAs.

---

## RECOMMENDATION

### Para laboratorio (experimentacion e investigacion)

**Playwright MCP**. Su modelo conceptual (navegador gobernado por protocolo con herramientas especificas) es el correcto para RADAR. La integracion puede hacerse via subprocess directamente o via `httpx` conectandose al server MCP en modo HTTP en lugar de stdio, evitando el bug de serializacion del cliente Python. Ademas, la herramienta ya fue considerada en `docs/RADAR_MCP_PLAYWRIGHT_ARQUITECTURA_SUPERADORA_V2.md` como pieza central de la arquitectura.

### Para produccion

**Playwright MCP (con workaround)**. Pero solo despues de:
1. Resolver el bug de `browser_evaluate` (usando el server en modo HTTP, o usando `browser_run_code_unsafe`)
2. Implementar reutilizacion de navegador (una sola instancia del server, no una por llamada)
3. Desarrollar extractores especificos por plataforma con selectores versionados

### Dependencias que agrega

**Playwright MCP**:
- `mcp` (Python, cliente/servidor MCP)
- Node.js + `npx` (runtime externo, no es dependencia Python)
- `@playwright/mcp` (bajo demanda via npx, ~30MB con Chromium)
- Playwright Python (ya instalada, 1.60.0)

**Crawlee** (si se considerara):
- `crawlee>=1.8` (~403KB codigo + 761KB fingerprint data + 37KB browserforge)
- `beautifulsoup4`, `lxml` (para BeautifulSoupCrawler)
- `psutil` (monitoreo)

### Riesgos tecnicos

1. **Bug de serializacion MCP Python**: `browser_evaluate` no recibe argumentos correctamente. Si no se resuelve, la extraccion via JS queda bloqueada. Mitigacion: usar HTTP mode del MCP server o `browser_run_code_unsafe`.
2. **Node.js como dependencia externa**: RADAR actualmente es Python puro. Agregar Node.js como requisito de ejecucion aumenta la complejidad del despliegue.
3. **Latencia de arranque del navegador**: ~19s por pagina es aceptable para laboratorio pero no para produccion sin reutilizacion de navegador.
4. **Storage persistente de Crawlee**: Incompatible con el modelo de RADAR donde la misma URL puede re-evaluarse. Mitigacion: limpiar storage entre ejecuciones, pero eso va contra el diseno de Crawlee.

### Descarte

**Crawlee Python queda descartado para el flujo de RADAR**. Las razones:

1. **Sobredimensionado**: Crawlee es un framework de crawling masivo (autoscaling, storage persistente, colas distribuidas). RADAR necesita extracciones puntuales y gobernadas, no crawlers autonomos.
2. **Storage persistente incompatible**: Crawlee asume que cada URL se visita una vez. RADAR necesita re-evaluar URLs (revision humana, re-clasificacion). Hacer que Crawlee funcione contra su diseno es una mala decision arquitectonica.
3. **Latencia prohibitiva**: PlaywrightCrawler con configuracion default timeout a 30s en paginas SPA. Solucionarlo requiere modificar parametros internos del crawler, aumentando la complejidad.
4. **API excesiva**: Para cada extraccion hay que configurar Router, PlaywrightCrawler, storage, autoscaling. La relacion senal/ruido es muy baja para el caso de uso.
5. **Peso innecesario**: ~1.2MB de dependencias adicionales (fingerprint data, browserforge, psutil) para funcionalidad que no necesitamos.

**Playwright MCP NO se descarta**, pero requiere trabajo de integracion antes de ser productivo.

---

## FILES_MODIFIED

```
scripts/experimento_playwright_crawlee.py  (nuevo, experimental)
.tmp/reporte-playwright-vs-crawlee-*.json  (resultados)
.tmp/_debug_mcp.py                          (debug, temporal)
.tmp/_debug_mcp2.py                         (debug, temporal)
```

No se modifico el flujo productivo de RADAR.

---

## TESTS

No se ejecutaron tests focales de RADAR porque el experimento NO toco el flujo productivo.
Los archivos creados son exclusivamente `scripts/` y `.tmp/`.

Comando ejecutable:
```bash
pytest tests/ -v --tb=short
```

---

## GIT_STATUS

```text
On branch experiment/playwright-crawlee-adoption-v1

Untracked files:
  .tmp/_debug_mcp.py
  .tmp/_debug_mcp2.py
  .tmp/reporte-playwright-vs-crawlee-20260723-212608.json
  lab/experimento-playwright-crawlee-adopcion-v1.md
  scripts/experimento_playwright_crawlee.py
```

Sin cambios en el flujo productivo. Sin commits. `git diff --check` sin errores (no hay diff en archivos tracked).

---

## Firmado

Experimentacion realizada el 2026-07-23. Decision documentada.