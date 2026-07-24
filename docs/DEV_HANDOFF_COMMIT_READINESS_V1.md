# RADAR — Preparación de commit y push

**Estado:** PREPARED — requiere cierre local de Git  
**Repo:** `E:\BuenosPasos\inlakech-radar`  
**Rama esperada:** `experiment/playwright-crawlee-adoption-v1` (verificar antes del commit)

## Estado verificado

- Tests focales Playwright/Evidence Pipe: **71 passed**.
- Suite completa: **298 passed, 2 failed, 2 skipped**.
- Fallos conocidos: los dos tests `TestSingleRetry`.
- Último commit observado: `c6f2f37 feat(radar): implement presumptive candidate list`.
- El trabajo actual todavía no fue committeado.

## Candidatos legítimos a versionar

### Gobierno y configuración

- `AGENTS.md`
- `pyproject.toml`
- `opencode.json`

### Código y tests

- `app/integrations/playwright_mcp.py`
- `app/discovery/playwright_adapter.py`
- `tests/test_playwright_mcp_integration.py`
- `tests/test_playwright_adapter.py`

El par siguiente pertenece al trabajo semántico previo y debe revisarse como unidad antes de incluirlo:

- `app/semantics/draft_normalizer.py`
- `tests/test_assessment_v3_normalization.py`

No debe presentarse como cierre del retry: hoy sus dos tests siguen fallando.

### Especificaciones, auditoría y estado

- `docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md`
- `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md`
- `docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_V1.md`
- `docs/specs/PLAYWRIGHT_PERSISTENT_RUNNER_CLOSE_002.md`
- `docs/specs/PLAYWRIGHT_TO_EVIDENCE_PIPE_V1.md`
- `docs/specs/PLAYWRIGHT_EVIDENCE_IDENTITY_CLOSE_002.md`
- `docs/specs/SEMANTIC_SINGLE_RETRY_CLOSE_001.md`
- `docs/audits/CONVERSATION_TO_SEMANTIC_REVIEW_AUDIT_V1.md`
- `docs/DEV_HANDOFF_COMMIT_READINESS_V1.md`

### Documentos de producto

- `docs/PROPUESTA_COMERCIAL_TECNICA_RADAR_INLAKECH_V1.md`
- `docs/PROPUESTA_RADAR_INLAKECH_MVP_USD_2400_V2.md`
- `docs/RADAR_INLAKECH_RECOMENDACION_ESTRATEGICA_V1.md`
- `docs/RADAR_MCP_PLAYWRIGHT_ARQUITECTURA_SUPERADORA_V2.md`
- `docs/RADAR_MVP_REPORTE_PARA_SOCIOS_V1.md`
- `docs/HIGGSFIELD_SKILLS_ADOPTION_V1.md`

La propuesta V2 debe quedar identificada como antecedente; la fuente comercial vigente es la versión V3 corregida.

### Laboratorio reproducible

Pueden incluirse, después de revisar que solo contienen evidencia técnica:

- `lab/experimento-lista1-casos-reales.md`
- `lab/experimento-playwright-crawlee-adopcion-v1.md`
- `lab/experimento-playwright-mcp-runtime-v1.md`
- `scripts/experimento_lista1_v3.py`
- `scripts/experimento_playwright_crawlee.py`
- `scripts/experimento_playwright_mcp_runtime.py`

## No versionar

Excluir:

- `.playwright-mcp/`
- `.tmp/`
- `storage/`
- archivos de entorno local, cookies, capturas temporales y bases locales.

Agregar a `.gitignore`:

```gitignore
.playwright-mcp/
.tmp/
storage/
```

## Riesgos a revisar antes del staging

1. No mezclar el arreglo pendiente de `TestSingleRetry` con el cierre Playwright.
2. No presentar la propuesta V2 como contrato rector.
3. Confirmar que los scripts de laboratorio no contienen datos locales.
4. Mantener Higgsfield fuera del runtime de RADAR.
5. No hacer merge a `main`.

## Cierre recomendado

Preferir dos commits:

```text
feat(radar): integrate persistent Playwright evidence flow
docs(radar): prepare semantic retry and developer handoff
```

El cierre local debe verificar rama, limpiar staging, ejecutar tests, `git diff --check`, revisar el diff staged, commitear y subir la rama actual sin force push.

## Bloqueo operativo actual

MCP-local permite leer, modificar, probar y consultar Git, pero no expone `git add` ni `git commit` en esta sesión. El cierre final debe hacerse desde OpenCode/Codex o manualmente al regresar a la PC.
