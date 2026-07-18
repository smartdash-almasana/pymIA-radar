# SPEC-001A — Repertorio de búsqueda y calidad conversacional

**Estado:** VERIFIED

**Fecha de verificación:** 2026-07-18

**Resultado del corpus v1:**
- Consultas: 10/10 completadas, 0 fallos
- Resultados totales: 4 (2 substantive, 2 review, 0 insufficient)
- Idempotencia: verificada (26 conversaciones persistentes, sin duplicados)
- Casos destacados: Q005 (`"inversión de impacto" turismo sustentable México`) → KEEP con 2 substantive. Q010 (`"intentional community" Mexico investment`) → REFINE con 1 review. Las 8 restantes → REJECT (sin resultados en fuentes actuales).

## Ejecutor reproducible

El catálogo completo se ejecuta con:

```powershell
python scripts/run_search_corpus.py --persist
```

El comando genera `data/last30days-runs/corpus-v1/report.json`, conserva una carpeta por consulta y devuelve error si alguna ejecución falla.

## Propósito

Convertir la política rectora de búsqueda de RADAR en un repertorio versionado y separar la calidad conversacional de la afinidad con Inlak'ech.

## Regla central

Una conversación puede ser sustantiva sin ser afín. Esta especificación solo decide si contiene suficiente contexto, decisión, objeción o lenguaje de acción para ingresar al corpus de evaluación.

No calcula afinidad, intención, capacidad, arquetipo ni calificación comercial.

## Entradas

- `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`;
- `config/search_queries.v1.json`;
- resultados normalizados de descubrimiento.

## Salidas

- catálogo versionado de consultas;
- evaluación `substantive`, `review` o `insufficient`;
- puntaje estructural;
- señales positivas y negativas;
- campos faltantes.

## Señales de calidad

- extensión suficiente;
- pregunta explícita;
- lenguaje de decisión o comparación;
- objeciones o diligencia previa;
- lenguaje de acción;
- contexto disponible.

## Señales de descarte

- fragmento demasiado corto;
- promoción directa;
- ausencia de contexto suficiente.

## Reglas

- no usar palabras de afinidad como prueba de calidad;
- no inferir intención financiera;
- no eliminar automáticamente los casos `review`;
- conservar el texto y la evidencia original;
- el catálogo debe pertenecer exclusivamente a Inlak'ech;
- los identificadores de consulta deben ser únicos y estables.

## Criterios de aceptación

1. Catálogo v1 con las diez consultas iniciales.
2. Validación de esquema y cliente único.
3. Rechazo de identificadores duplicados.
4. Evaluador determinístico y explicable.
5. Diferenciación entre conversación sustantiva, dudosa e insuficiente.
6. Contenido promocional penalizado.
7. Pruebas focales y regresión aprobadas.
8. Ejecución real posterior de las diez consultas con informe de rendimiento por consulta.

## Gate de cierre

Pasa a `VERIFIED` cuando las diez consultas se ejecuten con fuentes reales y exista un informe que documente resultados, ruido, cobertura, conversaciones sustantivas y consultas que deben conservarse, modificarse o descartarse.
