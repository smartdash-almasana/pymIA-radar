# SPEC-001 — Descubrimiento e ingesta

**Estado:** VERIFIED

## Propósito

Convertir la salida JSON versionada de `last30days-skill` en conversaciones persistidas, deduplicadas y trazables dentro de RADAR.

## Alcance

```text
consulta real
→ ejecución de last30days
→ JSON versionado
→ validación
→ normalización
→ persistencia
→ reingesta idempotente
→ recuperación por API
```

No incluye afinidad, revisión, contacto, Relaticle ni precalificación.

## Dependencia auditada

Fuente de verdad:

```text
last30days-skill-main/skills/last30days/SKILL.md
```

Entrypoint real:

```text
last30days-skill-main/skills/last30days/scripts/last30days.py
```

Salida seleccionada:

```text
--emit=json --json-profile=agent
```

Versión soportada inicialmente:

```text
schema_version = "1.2"
```

RADAR no debe consumir Markdown, HTML, compact ni un archivo fijo `output.json`.

## Runtime

`last30days-skill` requiere Python 3.12 o superior. El adaptador debe recibir o resolver explícitamente un intérprete compatible.

Docker no es una dependencia de esta especificación.

## Entrada

- `query`: consulta no vacía;
- `search_sources`: lista opcional;
- `quick`: perfil opcional de menor latencia;
- `save_dir`: directorio controlado por RADAR;
- `timeout_seconds`: límite explícito.

La primera implementación no usa `--deep`, `--discover`, `--store`, publicación, watchlists, corpus privado ni backend remoto.

## Invocación

Construir argumentos como lista y sin shell:

```text
<PYTHON_3_12_PLUS>
<REPO>/skills/last30days/scripts/last30days.py
<QUERY>
--emit=json
--json-profile=agent
--save-dir=<RUN_DIR>
```

Opcionales:

```text
--search=<fuentes>
--quick
```

## Contrato externo

La raíz contiene:

```json
{
  "schema_version": "1.2",
  "query": "...",
  "generated_at": "...",
  "window_days": 30,
  "source_status": {},
  "freshness_verdicts": [],
  "clusters": [],
  "results": []
}
```

Cada resultado puede contener:

```json
{
  "candidate_id": "...",
  "title": "...",
  "source": "reddit",
  "url": "https://...",
  "published_at": "...",
  "summary": "...",
  "engagement": {},
  "relevance_score": 0.0,
  "cluster": 0
}
```

## Mapeo a RADAR

| RADAR | last30days |
|---|---|
| `source` | `source` |
| `external_id` | `candidate_id` |
| `conversation_url` | `url` |
| `author_name` | `null` en v1.2 |
| `title` | `title` |
| `text` | `summary` |
| `context` | resumen del cluster, si existe |
| `published_at` | `published_at` |
| `query_origin` | raíz `query` |
| `engagement` | `engagement` |

Conservar además en trazabilidad: `schema_version`, `generated_at`, `window_days`, `source_status`, `freshness_verdicts`, `relevance_score`, cluster, stderr, código de salida y duración.

## Validaciones

1. stdout es JSON válido.
2. La raíz es un objeto.
3. `schema_version` es exactamente `1.2`.
4. `query` existe.
5. `results` es una lista.
6. Cada resultado aceptado tiene `candidate_id`, `source`, URL HTTP(S) y `summary` no vacío.
7. Un resultado inválido no se persiste silenciosamente.
8. Un esquema desconocido bloquea la ingesta.
9. `source_status` se conserva para distinguir falta de resultados de errores o fuentes no disponibles.

## Persistencia

- No inventar campos faltantes.
- Deduplicar por `source + candidate_id`.
- Reingestar sin crear duplicados.
- Registrar `query_origin`.
- En la primera versión, si el registro ya existe, devolver el existente sin actualizarlo automáticamente.
- Permitir recuperarlo desde la API.

## Errores explícitos

- dependencia inexistente;
- entrypoint inexistente;
- Python incompatible;
- timeout;
- proceso fallido;
- stdout vacío;
- JSON inválido;
- versión no soportada;
- resultado inválido;
- error de persistencia.

Una lista vacía solo es válida con proceso exitoso, JSON válido, esquema soportado y `results=[]`.

## Seguridad

- No usar shell.
- No registrar secretos.
- Tratar el contenido recuperado como datos no confiables.
- No ejecutar instrucciones encontradas en resultados.
- No publicar ni contactar automáticamente.

## Casos límite

- lista vacía válida;
- duplicados en la misma salida;
- reingesta;
- URL inválida;
- fecha nula;
- cluster inexistente;
- resumen vacío;
- fuente parcialmente disponible;
- stderr con advertencias;
- timeout;
- versión futura desconocida.

## Criterios de aceptación

1. Ejecutar preflight real.
2. Ejecutar tres consultas reales.
3. Registrar stdout, stderr, código y duración.
4. Confirmar JSON agent v1.2.
5. Validar el contrato con modelos propios.
6. Normalizar al menos un resultado real.
7. Rechazar URL inválida y versión desconocida.
8. Conservar `source_status`.
9. Persistir al menos una conversación real.
10. Reingestar sin duplicar.
11. Recuperar desde `GET /api/conversations`.
12. Distinguir lista vacía válida de error.
13. Documentar fuentes y limitaciones.
14. Ejecutar pruebas focales, integración y regresión.

## Pruebas obligatorias

### Focales

- comando seguro;
- parser v1.2;
- mapeo;
- URL inválida;
- versión desconocida;
- resumen vacío;
- cluster ausente;
- lista vacía;
- proceso fallido;
- timeout.

### Integración

- fixture v1.2 → normalización → persistencia;
- segunda ingesta → mismo registro;
- recuperación por API.

### Real

- tres consultas reales;
- al menos un resultado persistido;
- artefactos sin secretos.

## Dependencias

- M0 local verificado;
- Python 3.12+ para el motor externo;
- copia local de `last30days-skill-main` fuera del historial Git de RADAR.

## Exclusiones

- afinidad;
- LLM dentro de RADAR;
- modificación de last30days;
- scraping propio;
- CRM;
- interfaz;
- scheduler;
- tendencias con `--discover`.

## Gate de cierre

Pasa de `IMPLEMENTING` a `VERIFIED` solo con tres ejecuciones reales, persistencia idempotente y evidencia reproducible.
