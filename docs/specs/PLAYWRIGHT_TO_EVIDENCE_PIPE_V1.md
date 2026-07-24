# PLAYWRIGHT TO EVIDENCE PIPE V1

**Estado:** VERIFIED
**Ciclo:** RADAR-PLAYWRIGHT-EVIDENCE-001
**Objetivo:** conectar `PlaywrightMCPClient` con el flujo existente de descubrimiento, deduplicación y persistencia, sin duplicar lógica.

## Fuente de verdad

1. `AGENTS.md`
2. `docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md`
3. `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md`
4. `docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_V1.md`
5. `docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_CLOSE_002.md`

## Reutilización obligatoria

Usar:

- `app.discovery.contracts.DiscoveryResult`
- `app.discovery.ingestion.persist_discovery_results`

La identidad productiva existente sigue siendo:

```text
source + external_id
```

No crear otra deduplicación ni otra tabla.

## Flujo autorizado

```text
NavigationRequest
→ PlaywrightMCPClient.navigate()
→ NavigationResult
→ adaptador a DiscoveryResult
→ persist_discovery_results()
→ Conversation
```

## Alcance

Implementar un adaptador mínimo que:

- reciba `NavigationResult` y metadatos explícitos de fuente/consulta;
- acepte solo `SUCCESS` y `EXTRACTION_PARTIAL` utilizable;
- rechace estados fallidos o bloqueados;
- use `final_url` real como URL canónica;
- rechace `final_url=None`;
- conserve texto visible y autor opcional;
- conserve en `engagement` estado de navegación, `author_status`, latencia y `screenshot_path`;
- genere `external_id` estable;
- use `persist_discovery_results` para persistir e impedir duplicados.

## External ID

Prioridad:

1. identificador explícito de plataforma, si existe;
2. huella estable basada en `source + final_url + texto normalizado`.

Prohibido usar timestamp, UUID aleatorio o posición de ejecución.

## Estados

Admitidos:

```text
SUCCESS
EXTRACTION_PARTIAL
```

`EXTRACTION_PARTIAL` solo se admite con texto suficiente y URL final real.

Rechazados:

```text
EXTRACTION_FAILED
SESSION_LOST
MCP_CONNECTION_ERROR
MCP_SERIALIZATION_ERROR
CAPTCHA_BLOCKED
LOGIN_REQUIRED
```

Los rechazados no crean `Conversation`.

## Contrato sugerido

```python
class PlaywrightDiscoveryInput(BaseModel):
    source: str
    query_origin: str | None = None
    external_id: str | None = None
    title: str | None = None
    context: str | None = None


def build_discovery_result_from_playwright(
    *, navigation: NavigationResult, metadata: PlaywrightDiscoveryInput
) -> DiscoveryResult:
    ...
```

El nombre puede adaptarse a las convenciones existentes.

## Archivos autorizados

- un adaptador nuevo bajo `app/discovery/` o `app/integrations/`;
- tests focales nuevos;
- modificación mínima de un orquestador existente solo si es indispensable;
- `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md` al cerrar;
- esta especificación para marcar `VERIFIED`.

No modificar modelos, migraciones, semántica, HTMX, CRM, mensajería ni deduplicación existente.

## Criterios de aceptación

1. `NavigationResult` válido se transforma en `DiscoveryResult`.
2. Se conserva texto, URL, autor opcional y trazabilidad.
3. `external_id` es determinístico.
4. Dos ejecuciones del mismo caso crean una sola `Conversation`.
5. Estados rechazados no persisten.
6. `EXTRACTION_PARTIAL` sin autor puede persistir sin inventarlo.
7. `final_url=None` no persiste.
8. Se reutiliza `persist_discovery_results`.
9. Tests focales verdes.
10. Suite completa sin regresiones nuevas.
11. `git diff --check` limpio.
12. Ponytail sin sobreestructura relevante.

## Pruebas obligatorias

- `SUCCESS`;
- `EXTRACTION_PARTIAL` sin autor;
- rechazo de estados fallidos/bloqueados;
- rechazo de texto vacío o insuficiente;
- rechazo de URL final ausente;
- estabilidad de `external_id`;
- idempotencia real con `persist_discovery_results`;
- conservación de screenshot y latencia.

## Fuera de alcance

No implementar evaluación semántica posterior, Lista 1, `ApprovedOpportunityV1`, interfaz, CRM, mensajería, nuevas plataformas, colas ni cierre de `TestSingleRetry`.

## Formato de cierre

```text
VERDICT
SOURCE_OF_TRUTH_READ
FILES_ALLOWED
FILES_MODIFIED
ADAPTER_LOCATION
DISCOVERY_RESULT_MAPPING
EXTERNAL_ID_STRATEGY
REJECTED_STATUS_BEHAVIOR
TRACEABILITY_PRESERVED
IDEMPOTENCY
FOCAL_TESTS
FULL_SUITE
REGRESSIONS
PONYTAIL_REVIEW
DIFF_CHECK
GIT_STATUS
REMAINING_GAPS
NEXT_RECOMMENDATION
```

## Próximo paso permitido

Solo después de `VERIFIED`:

```text
Conversation persistida con evidencia Playwright
→ evaluación semántica existente
→ revisión humana / Lista 1
```
