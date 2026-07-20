# SPEC-002 — Interpretación de afinidad e intención aparentes

**Estado:** DRAFT — REQUIERE APROBACIÓN TRAS RECONCILIACIÓN DOCUMENTAL

## Propósito

Interpretar conversaciones públicas según la configuración específica de Inlak’ech, manteniendo como objeto inicial la conversación y evitando atribuciones prematuras sobre la persona.

La salida de esta especificación sirve para ordenar revisión humana. No confirma afinidad personal, no asigna arquetipo y no inicia precalificación.

## Entradas rectoras

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`;
- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`;
- conversaciones reales normalizadas por SPEC-001;
- corpus positivo, negativo y ambiguo validado humanamente.

## Unidad de análisis

```text
conversación pública situada
```

La identidad del autor puede conservarse como referencia pública, pero no es objeto de diagnóstico.

## Salidas obligatorias

- tema real;
- significado contextual;
- afinidad semántica aparente;
- campos de afinidad detectados;
- intención aparente;
- resumen de intención;
- fragmentos de evidencia;
- contradicciones;
- información o contexto faltante;
- riesgo de falso positivo;
- incertidumbre;
- razón para revisión humana;
- acción de bandeja recomendada;
- `human_review_required = true`;
- `provisional = true`.

## Valores conceptuales iniciales

### Afinidad aparente

- `NINGUNA`;
- `POSIBLE`;
- `CLARA`.

### Intención aparente

- `NINGUNA`;
- `SIMPATIA_TEMATICA`;
- `EXPLORACION`;
- `ORIENTADA_A_ACCION`.

### Riesgo e incertidumbre

- `BAJO`;
- `MEDIO`;
- `ALTO`.

## Exclusiones de la salida pública

Esta evaluación no debe producir:

- arquetipo probable;
- confianza de arquetipo;
- capacidad económica;
- perfil identitario;
- camino de participación;
- calificación;
- lead score;
- autorización automática de contacto.

## Reglas

- coincidencia léxica no equivale a sentido;
- tema no equivale a intención;
- afinidad aparente no equivale a afinidad revelada;
- toda inferencia debe citar evidencia;
- las citas deben existir en el texto o contexto persistido;
- contradicciones e incertidumbre deben conservarse;
- casos ambiguos deben pasar a revisión secundaria o quedar fuera de prioridad, según reglas transparentes;
- el LLM interpreta y RADAR valida;
- una salida inválida o sin evidencia no puede habilitar contacto.

## Prioridad de revisión

Puede existir un cálculo secundario para ordenar la bandeja, basado en:

- afinidad aparente;
- intención aparente;
- calidad de evidencia;
- actualidad;
- riesgo de falso positivo.

El número no reemplaza la explicación semántica y no califica a la persona.

## Gap con la implementación vigente

La implementación actual todavía contiene:

- `thematic_affinity` y `values_affinity` numéricos;
- `intent_score`;
- `declared_capacity`;
- `probable_archetype`;
- `archetype_confidence`;
- `archetype_evidence`.

Esos campos constituyen legado técnico pendiente de una evolución versionada. No deben eliminarse ni reinterpretarse silenciosamente sin una especificación de migración aprobada.

## Corpus mínimo

Debe incluir:

- conversaciones claramente afines;
- conversaciones temáticamente cercanas pero no afines;
- simpatía temática sin intención;
- intención explícita;
- intención ambigua;
- falsos positivos léxicos;
- contexto contradictorio;
- caso negativo de rivalidad futbolística recuperado por una consulta sobre comunidad.

## Criterios de aceptación

- contrato Pydantic versionado;
- persistencia versionada sin destruir evaluaciones anteriores;
- evidencia literal validada;
- corpus humano suficiente y separado de calibración;
- positivos, negativos y ambiguos;
- falsos positivos documentados;
- precisión y cobertura medidas sobre muestra independiente;
- ninguna salida pública asigna arquetipo o capacidad;
- revisión humana obligatoria;
- pruebas de contrato, evidencia y fallback.

## Prohibición de implementación

Mientras esta especificación permanezca `DRAFT`, no autoriza cambios en:

```text
app/
tests/
config/
data/
scripts/
```
