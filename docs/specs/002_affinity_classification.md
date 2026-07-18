# SPEC-002 — Afinidad e intención

**Estado:** DRAFT

## Propósito

Evaluar conversaciones según la configuración específica de Inlak'ech.

## Entradas rectoras

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`;
- conversaciones reales normalizadas por SPEC-001;
- corpus positivo, negativo y ambiguo construido con evidencia.

El texto rector de búsqueda orienta qué conversaciones localizar, pero no reemplaza la evaluación separada de afinidad, intención, capacidad y calificación.

## Salidas obligatorias

- relevancia;
- puntaje de afinidad;
- puntaje de intención;
- arquetipo probable;
- etapa;
- evidencias;
- faltantes;
- señales de riesgo;
- acción recomendada.

## Reglas

- afinidad e intención son dimensiones diferentes;
- ninguna inferencia financiera puede presentarse como hecho;
- toda puntuación debe citar evidencia textual;
- casos ambiguos deben pasar a revisión;
- señales espirituales sin intención no equivalen a lead.

## Criterios de aceptación

- corpus mínimo de 100 conversaciones;
- positivos, negativos y ambiguos;
- falsos positivos documentados;
- salida JSON validada;
- precisión objetivo definida antes del piloto.
