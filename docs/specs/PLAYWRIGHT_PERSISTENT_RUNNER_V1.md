# PLAYWRIGHT PERSISTENT RUNNER V1

**Estado:** APPROVED  
**Ciclo:** RADAR-MVP-PLAYWRIGHT-001  
**Objetivo único:** integrar en RADAR un runner persistente basado en Playwright MCP para navegación, captura de texto visible, URL y evidencia, reutilizando una sola instancia de Chromium.

---

## 1. Documento rector

Esta especificación debe leerse junto con:

1. `docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md`
2. `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md`
3. `docs/RADAR_MCP_PLAYWRIGHT_ARQUITECTURA_SUPERADORA_V2.md`

El contrato comercial aplicable es RADAR MVP por USD 2.400.

---

## 2. Alcance autorizado

Implementar un componente productivo mínimo que:

- arranque Playwright MCP una sola vez;
- reutilice una única instancia de Chromium;
- mantenga sesión y cookies durante la vida del runner;
- navegue a una URL;
- obtenga snapshot o texto visible;
- registre la URL final;
- capture evidencia cuando corresponda;
- clasifique errores;
- cierre recursos correctamente.

---

## 3. Fuera de alcance

No implementar en este ciclo:

- `browser_evaluate`;
- ejecución remota de JavaScript;
- bypass de CAPTCHA, 2FA o bloqueos;
- múltiples plataformas productivas;
- workers distribuidos;
- Redis, Celery, RQ o nueva cola;
- CRM;
- mensajería;
- contacto automático;
- deduplicación nueva si ya existe una reutilizable;
- inferencia de autor cuando no pueda resolverse con certeza;
- refactorizaciones ajenas al runner.

---

## 4. Contrato mínimo de entrada

```python
class PlaywrightNavigationRequest(BaseModel):
    url: str
    capture_screenshot: bool = False
    timeout_seconds: int = 30
```

## 5. Contrato mínimo de salida

```python
class PlaywrightNavigationResult(BaseModel):
    requested_url: str
    final_url: str | None
    visible_text: str
    author: str | None
    author_status: Literal["RESOLVED", "PARTIAL", "UNAVAILABLE"]
    screenshot_path: str | None
    status: Literal[
        "SUCCESS",
        "EXTRACTION_PARTIAL",
        "EXTRACTION_FAILED",
        "SESSION_LOST",
        "MCP_CONNECTION_ERROR",
        "MCP_SERIALIZATION_ERROR",
        "CAPTCHA_BLOCKED",
        "LOGIN_REQUIRED",
    ]
    latency_ms: int
    error_detail: str | None
```

El nombre exacto de los modelos puede adaptarse a convenciones existentes del repo, pero no debe ampliarse el contrato.

---

## 6. Reglas obligatorias

- `author` es opcional.
- No inferir autor desde texto ambiguo.
- `browser_evaluate` debe figurar como capacidad no disponible.
- El runner debe reutilizar una sola instancia de Chromium.
- La sesión debe sobrevivir a múltiples navegaciones consecutivas.
- Los errores deben convertirse en estados explícitos.
- No agregar dependencias salvo necesidad demostrada.
- Reutilizar configuración, logging y contratos existentes cuando sea posible.
- No tocar semántica, CRM ni flujo comercial.

---

## 7. Archivos permitidos

El implementador debe identificar el lugar mínimo coherente dentro del repo. Se autorizan únicamente:

- un módulo nuevo bajo `app/integrations/` o `app/services/`;
- un archivo de configuración mínimo si es indispensable;
- tests focales nuevos;
- actualización de `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md` al cerrar.

No se autorizan cambios en módulos de negocio ajenos al runner.

---

## 8. Criterios de aceptación

El ciclo pasa a `VERIFIED` cuando:

1. una sola instancia de Chromium atiende 10 navegaciones consecutivas;
2. 10/10 tareas terminan con estado controlado;
3. la sesión persiste;
4. `visible_text` y `final_url` se recuperan correctamente en los casos de prueba;
5. `author` puede quedar `UNAVAILABLE` sin romper el flujo;
6. la latencia media posterior al arranque es menor a 5 segundos en el entorno de prueba;
7. no se usa `browser_evaluate`;
8. los errores quedan clasificados;
9. los tests focales pasan;
10. la suite completa no agrega regresiones;
11. `git diff --check` pasa;
12. Ponytail review no detecta sobreestructura relevante.

---

## 9. Pruebas obligatorias

- lifecycle del runner;
- reutilización de Chromium;
- persistencia de sesión;
- navegación exitosa;
- autor no disponible;
- error de conexión MCP;
- error de sesión;
- cierre limpio;
- 10 navegaciones consecutivas en prueba de integración controlada.

---

## 10. Formato de cierre

Reportar exactamente:

```text
VERDICT
FILES_MODIFIED
RUNNER_LOCATION
BROWSER_REUSE
SESSION_PERSISTENCE
EXTRACTION_RESULT
AUTHOR_BEHAVIOR
LATENCY
ERROR_CLASSIFICATION
TESTS
PONYTAIL_REVIEW
GIT_STATUS
NEXT_RECOMMENDATION
```

---

## 11. Próximo paso posterior

Solo si esta especificación queda `VERIFIED`:

```text
Persistent Playwright Runner
→ Evidence Pipe existente
→ evaluación semántica
→ Lista 1
```

No se autoriza esa integración dentro de este mismo ciclo.
