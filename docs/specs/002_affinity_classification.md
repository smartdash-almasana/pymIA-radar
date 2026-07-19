# SPEC-002 — Afinidad e intención

**Estado:** IMPLEMENTING — BLOCKED BY HUMAN CORPUS AND SPEC-001B

## Propósito

Evaluar conversaciones según la configuración específica de Inlak'ech.

## Entradas rectoras

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`;
- conversaciones reales normalizadas por SPEC-001;
- corpus positivo, negativo y ambiguo construido con evidencia.

El texto rector de búsqueda orienta qué conversaciones localizar, pero no reemplaza la evaluación separada de afinidad, intención, capacidad y calificación.

## Salidas obligatorias

- afinidad temática `0–100`;
- afinidad de valores `0–100`;
- intención `0–100`;
- capacidad declarada, sin inferencias;
- momento de decisión;
- calidad de evidencia `0–100`;
- riesgo de falso positivo;
- prioridad para revisión humana;
- arquetipo probable, confianza y evidencia;
- fragmentos justificativos;
- objeciones;
- información faltante;
- acción recomendada.

La salida debe cumplir `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`.

## Reglas

- afinidad e intención son dimensiones diferentes;
- ninguna inferencia financiera puede presentarse como hecho;
- toda puntuación debe citar evidencia textual;
- casos ambiguos deben pasar a revisión;
- señales espirituales sin intención no equivalen a lead.

## Implementado en este corte

- salida estructurada validada con Pydantic;
- evaluación determinística de prioridad y acción;
- integración semántica opcional con proveedor remoto;
- persistencia de evaluaciones y metadatos del motor;
- corpus exportable en estado `DRAFT`;
- calibración bloqueada cuando no existe validación humana.

## Criterios de aceptación pendientes

- corpus mínimo de 100 conversaciones públicas válidas;
- positivos, negativos y ambiguos etiquetados humanamente;
- falsos positivos documentados;
- precisión medida sobre corpus humano independiente;
- precisión objetivo definida y satisfecha antes del piloto.
