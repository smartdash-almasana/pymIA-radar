# SPEC-001B — Repertorio de búsqueda v2

**Estado:** IMPLEMENTING — ACTIVE

## Propósito

Ampliar la recuperación de conversaciones públicas reales para Inlak'ech mediante consultas menos rígidas que las usadas en el repertorio v1.

Esta es la única especificación activa en el corte documentado por `docs/CURRENT_ENGINEERING_STATE.md`.

## Hallazgo de partida

El repertorio v1 ejecutó 10 consultas reales y produjo 4 resultados: 2 `substantive` y 2 `review`. Ocho consultas no recuperaron resultados. Las frases exactas y la acumulación de conceptos redujeron demasiado la cobertura.

## Hipótesis de v2

Consultas más cortas, sin comillas exactas y organizadas por tema y geografía deben aumentar la recuperación sin abandonar la evaluación posterior de calidad conversacional.

## Alcance

- 20 consultas dedicadas exclusivamente a Inlak'ech;
- español e inglés;
- inversión de impacto y sustentable;
- proyectos con propósito;
- ecoaldeas y comunidades intencionales;
- hospitalidad y turismo sustentable;
- desarrollo regenerativo e inmobiliario sustentable;
- Yucatán y México;
- patrimonio y largo plazo.

## Reglas

- no usar frases exactas salvo evidencia posterior que lo justifique;
- no mezclar más de tres conceptos principales por consulta;
- no evaluar afinidad ni intención en esta especificación;
- conservar resultados reales, fuente, consulta y trazabilidad;
- ejecutar sin `--quick` como configuración base;
- comparar rendimiento contra v1;
- no alterar ni reemplazar el catálogo v1.

## Entrada

`config/search_queries.v2.json`

## Ejecución reproducible

```powershell
python scripts/run_search_corpus.py `
  --catalog config/search_queries.v2.json `
  --runs-root data/last30days-runs/corpus-v2 `
  --report data/last30days-runs/corpus-v2/report.json `
  --persist `
  --no-quick
```

## Criterios de aceptación

1. Catálogo v2 válido con 20 consultas y IDs únicos.
2. Las consultas no contienen frases exactas entre comillas.
3. Ejecución real de las 20 consultas sin fallos ocultos.
4. Informe consolidado con `KEEP`, `REFINE` o `REJECT`.
5. Persistencia idempotente.
6. Comparación explícita con las 4 conversaciones recuperadas por v1.
7. Documentación de cobertura por fuente.
8. Suite completa aprobada.

## Gate de cierre

Pasa a `VERIFIED` cuando exista evidencia real reproducible de las 20 ejecuciones, un informe comparativo v1/v2 y una decisión documentada sobre qué consultas integrarán el repertorio operativo siguiente.

Mientras este gate permanezca abierto, no debe iniciarse la ejecución de `SPEC-001C`, la calibración semántica ni el piloto.
