# PLAYWRIGHT → EVIDENCE PIPE — CIERRE DE IDENTIDAD 002

**Estado:** VERIFIED  
**Ciclo:** RADAR-PLAYWRIGHT-EVIDENCE-ID-CLOSE-002  
**Objetivo único:** corregir la estrategia de identidad del adaptador Playwright para preservar idempotencia cuando cambia el texto de una misma publicación.

---

## 1. Fuente de verdad

Leer en este orden:

1. `AGENTS.md`
2. `docs/RADAR_PRODUCTIVITY_LAYER_CONTRACT_V1.md`
3. `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md`
4. `docs/specs/PLAYWRIGHT_TO_EVIDENCE_PIPE_V1.md`
5. `app/discovery/playwright_adapter.py`
6. `app/discovery/ingestion.py`
7. `tests/test_playwright_adapter.py`

---

## 2. Problema confirmado

La implementación actual deriva `external_id` desde:

```text
source + final_url + text[:100]
```

Esto permite que una misma publicación produzca identificadores diferentes cuando cambia el snapshot, el orden del texto o el contenido visible.

La identidad de una publicación navegada no debe depender del contenido mutable cuando existe una URL final estable.

---

## 3. Decisión obligatoria

Derivar `external_id` exclusivamente desde:

```text
source normalizada + URL final canónica
```

El texto debe conservarse como evidencia, pero no participar de la identidad primaria.

---

## 4. Canonicalización mínima autorizada

No existe actualmente un helper reutilizable de canonicalización en `app/`.

Se autoriza una función privada mínima dentro de:

```text
app/discovery/playwright_adapter.py
```

Debe:

- normalizar esquema y host a minúsculas;
- eliminar fragmentos `#...`;
- eliminar `/` final excepto cuando la ruta sea `/`;
- conservar ruta y parámetros significativos;
- no eliminar parámetros arbitrariamente;
- no introducir una dependencia nueva;
- usar únicamente biblioteca estándar.

No se autoriza construir un sistema complejo de canonicalización ni reglas específicas por plataforma en este ciclo.

---

## 5. Estrategia de identidad

Conceptualmente:

```python
canonical_url = canonicalize_url(navigation.final_url)
raw_identity = f"{source.strip().lower()}:{canonical_url}"
external_id = f"pw:{sha256(raw_identity.encode()).hexdigest()[:16]}"
```

La implementación puede ajustar nombres, pero no el criterio.

---

## 6. Comportamiento esperado

Debe cumplirse:

```text
misma fuente + misma URL canónica + texto diferente
= mismo external_id
= una sola Conversation
```

Y también:

```text
misma URL canónica + fuente diferente
= external_id diferente
```

---

## 7. Archivos autorizados

Modificar únicamente:

- `app/discovery/playwright_adapter.py`
- `tests/test_playwright_adapter.py`
- `docs/RADAR_MVP_IMPLEMENTATION_STATE_V1.md` al cerrar
- esta especificación para marcar `VERIFIED`

No modificar contratos, modelos, migraciones ni persistencia existente.

---

## 8. Tests obligatorios

Agregar pruebas para:

1. misma URL y texto diferente producen el mismo `external_id`;
2. misma URL y texto diferente persisten una sola `Conversation`;
3. URL con y sin `/` final produce la misma identidad;
4. fragmentos distintos `#section-a` y `#section-b` producen la misma identidad;
5. host con diferencias de mayúsculas produce la misma identidad;
6. fuentes diferentes producen identidad diferente;
7. parámetros de consulta significativos se conservan y pueden producir identidad diferente;
8. no cambia el comportamiento de rechazo por estado, URL inválida o texto insuficiente.

---

## 9. Fuera de alcance

No implementar:

- deduplicación semántica;
- reglas específicas por Reddit, Facebook, Instagram, LinkedIn o TikTok;
- eliminación general de query params;
- actualización de conversaciones ya persistidas;
- reconciliación histórica de duplicados;
- semántica;
- Lista 1;
- `ApprovedOpportunityV1`;
- CRM;
- solución de `TestSingleRetry`;
- nuevas dependencias.

---

## 10. Criterios de aceptación

El ciclo queda `VERIFIED` cuando:

- el texto deja de participar en `external_id`;
- la URL se canonicaliza con las reglas mínimas aprobadas;
- misma publicación con texto actualizado mantiene identidad;
- `persist_discovery_results` sigue siendo el único punto de persistencia;
- no aparece una segunda deduplicación;
- tests focales pasan;
- suite completa no agrega regresiones;
- `git diff --check` pasa;
- Ponytail no detecta sobreestructura relevante.

---

## 11. Formato de cierre

```text
VERDICT
FILES_MODIFIED
CANONICALIZATION_RULES
EXTERNAL_ID_STRATEGY
SAME_URL_CHANGED_TEXT
URL_VARIANTS
IDEMPOTENCY
FOCAL_TESTS
FULL_SUITE
REGRESSIONS
PONYTAIL_REVIEW
DIFF_CHECK
GIT_STATUS
NEXT_RECOMMENDATION
```

---

## 12. Próximo paso permitido

Solo después de `VERIFIED`:

```text
Conversation persistida desde Playwright
→ evaluación semántica existente
→ revisión humana / Lista 1
```
