# Auditoría de integración — last30days-skill

## Veredicto

**PASS para especificación. NO IMPLEMENTADO para runtime.**

## Dependencia auditada

- Runtime spec: `last30days-skill-main/skills/last30days/SKILL.md`
- Entrypoint: `last30days-skill-main/skills/last30days/scripts/last30days.py`
- Esquema: `last30days-skill-main/skills/last30days/scripts/lib/schema.py`
- Versión del skill inspeccionada: `3.16.0`
- Licencia declarada: MIT
- Python requerido: 3.12+

## Hallazgos

1. El adaptador actual de RADAR es un placeholder.
2. Busca un archivo fijo `output.json` que no forma parte del contrato real auditado.
3. El entrypoint real es una CLI Python.
4. La salida estable para agentes es `--emit=json --json-profile=agent`.
5. El esquema auditado es `1.2`.
6. La salida estable contiene `results`, `clusters`, `source_status`, ventana temporal y datos de frescura.
7. Cada resultado incluye `candidate_id`, fuente, URL, resumen, fecha, métricas, relevancia y cluster.
8. El perfil agent v1.2 no exporta autor; RADAR debe usar `null` y no inferirlo.
9. El motor puede funcionar con fuentes gratuitas, pero la cobertura depende de configuración y disponibilidad por fuente.
10. Una lista vacía no equivale necesariamente a error; debe interpretarse junto con `source_status` y el código de salida.

## Decisión de integración

RADAR integrará por subprocess controlado, sin shell, consumiendo stdout JSON. No modificará el repositorio externo ni interpretará Markdown.

## Límites todavía no verificados

- Preflight ejecutado en esta PC.
- Tres consultas reales.
- Duración y comportamiento bajo timeout.
- Fuentes efectivamente disponibles en Windows.
- Fixtures capturadas de ejecuciones reales.

Estos puntos pertenecen a la implementación y verificación de SPEC-001, no a su definición.
