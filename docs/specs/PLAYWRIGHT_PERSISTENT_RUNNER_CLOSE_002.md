# PLAYWRIGHT PERSISTENT RUNNER — CIERRE 002

**Estado:** VERIFIED  
**Ciclo:** RADAR-PLAYWRIGHT-RUNNER-CLOSE-002  
**Objetivo único:** cerrar los incumplimientos detectados en la implementación inicial del runner persistente de Playwright MCP sin ampliar alcance.

---

## 1. Fuente de verdad

Leer en este orden:

1. `docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md`
2. `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md`
3. `docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_V1.md`
4. `AGENTS.md`

---

## 2. Problemas a corregir

### 2.1 URL final real

La implementación actual copia `requested_url` dentro de `final_url`.

Debe obtenerse la URL efectiva posterior a navegación y redirecciones mediante una capacidad disponible de Playwright MCP. Si el servidor MCP no expone la URL final de forma confiable, el runner debe devolver:

```text
final_url = null
```

junto con una explicación explícita en `error_detail` o un campo ya existente compatible, pero nunca simular que la URL solicitada es la URL final.

### 2.2 Captura de pantalla

Cuando:

```text
capture_screenshot = true
```

el runner debe invocar la herramienta de captura disponible y devolver una referencia válida en `screenshot_path`.

Cuando sea `false`, debe devolver `null`.

### 2.3 Clasificación real de errores

No alcanza con declarar los estados. Debe existir comportamiento verificable para clasificar, cuando corresponda:

```text
LOGIN_REQUIRED
CAPTCHA_BLOCKED
MCP_SERIALIZATION_ERROR
MCP_CONNECTION_ERROR
SESSION_LOST
EXTRACTION_FAILED
```

No inventar detecciones. Clasificar solo cuando exista evidencia observable en la respuesta, excepción o snapshot.

---

## 3. Alcance autorizado

Modificar únicamente:

- `app/integrations/playwright_mcp.py`
- `tests/test_playwright_mcp_integration.py`
- script experimental del runtime si hace falta para la prueba viva
- `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md` al cerrar
- esta especificación solo para marcar estado final

---

## 4. Fuera de alcance

No implementar:

- `browser_evaluate`;
- JavaScript remoto;
- nuevos workers;
- nuevas plataformas;
- CRM;
- semántica;
- Redis o colas nuevas;
- rediseño del contrato;
- refactors ajenos;
- inferencia de autor;
- bypass de CAPTCHA, login o bloqueos.

---

## 5. Criterios de aceptación

El ciclo pasa a `VERIFIED` cuando:

1. `final_url` representa la URL efectiva o queda `null`; nunca replica la solicitada sin prueba;
2. `capture_screenshot=True` produce una captura real y una referencia válida;
3. `capture_screenshot=False` no genera captura;
4. los errores observables se clasifican mediante comportamiento real;
5. los tests focales cubren URL final, screenshot y clasificación;
6. el runner sigue reutilizando una sola instancia de Chromium;
7. 10/10 navegaciones terminan en estado controlado;
8. la sesión persiste;
9. la latencia media posterior al arranque se mantiene por debajo de 5 segundos o se documenta una variación justificada por la captura;
10. no se usa `browser_evaluate`;
11. Ponytail no detecta sobreestructura relevante;
12. la suite no agrega regresiones;
13. `git diff --check` pasa.

---

## 6. Formato de cierre

```text
VERDICT
FILES_MODIFIED
FINAL_URL_BEHAVIOR
SCREENSHOT_BEHAVIOR
ERROR_CLASSIFICATION
BROWSER_REUSE
SESSION_PERSISTENCE
LIVE_RUN
LATENCY
PONYTAIL_REVIEW
TESTS
REGRESSIONS
GIT_STATUS
NEXT_RECOMMENDATION
```

---

## 7. Próximo paso permitido

Solo después de `VERIFIED`:

```text
Persistent Playwright Runner
→ integración con Evidence Pipe existente
```

No avanzar todavía a `ApprovedOpportunityV1` ni al piloto integral.
