# M1 — Descubrimiento e ingesta: checkpoint de implementación

## Estado

```text
SPEC-001 = VERIFIED
M1_RUNTIME_REAL = COMPLETED
```

## Verificado con fixtures

- entrypoint real auditado;
- contrato JSON agent v1.2 documentado;
- versión desconocida rechazada;
- JSON inválido rechazado;
- URL inválida rechazada;
- resumen vacío rechazado;
- query mismatch rechazado;
- lista vacía válida;
- duplicados internos eliminados;
- contexto de cluster mapeado;
- trazabilidad de comando, stderr, código y duración;
- persistencia idempotente por `source + external_id`;
- recuperación desde base local;
- fechas y URLs adaptadas correctamente al límite SQLAlchemy.

## Evidencia actual

```text
python -m pytest -q
15 passed
```

## Verificado con ejecuciones reales

| Item | Resultado |
|------|-----------|
| Python | 3.14.0 (3.12+) |
| Preflight | Ready to research with safe defaults |
| Consulta 1: "inversión regenerativa comunidad largo plazo" | 2 resultados Reddit, schema v1.2 |
| Consulta 2: "patrimonio con propósito impacto territorial" | 0 resultados (lista vacía válida, schema v1.2) |
| Consulta 3: "proyectos regenerativos inversión consciente" | 0 resultados (lista vacía válida, schema v1.2) |
| Persistencia primera ingesta | 2 conversaciones (`id=10`, `id=11`) |
| Reingesta (idempotencia) | 0 nuevos registros creados |
| Recuperación API | `GET /api/conversations` → 11 registros |
| `schema_version` | `"1.2"` en las 3 ejecuciones |
| `source_status` | Preservado (reddit: partial, hackernews: no-results) |
| Suite de pruebas | 15 passed |

## Limitaciones por fuente

- **Reddit**: acceso keyless por RSS (tier 1); solo recupera threads recientes.
- **HackerNews**: buscó pero filtró todos los resultados por relevancia.
- **GitHub**, **Polymarket**: sin resultados en estas consultas en español.
- **X/Twitter, YouTube**: no disponibles sin configuración adicional (API key o cookies).
- **Clasificación LLM**: no disponible sin OpenRouter key habilitada para reranking. Usó fallback determinístico.
- Todas las fuentes declararon `no-results` o `partial` coherentemente.

## Artefactos

```text
data/last30days-runs/run-001/  → 2 resultados reales (stdout.json, stderr)
data/last30days-runs/run-002/  → lista vacía válida
data/last30days-runs/run-003/  → lista vacía válida
data/last30days-runs/ está gitignored — no contiene secretos.
```

## Docker

Docker no bloqueó ninguno de estos puntos. La validación se ejecutó 100% local con Python 3.14.
