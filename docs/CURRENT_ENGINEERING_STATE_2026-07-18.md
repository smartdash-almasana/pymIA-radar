# Estado actual de ingeniería — 18/07/2026

> **ESTADO HISTÓRICO — SUPERSEDIDO COMO CHECKPOINT VIGENTE EL 19/07/2026.**
> Se conserva como evidencia del estado anterior a la reconciliación del embudo humano de descubrimiento. La fuente vigente es `docs/CURRENT_ENGINEERING_STATE_2026-07-19.md`.

## Propósito

Este checkpoint reconcilia el estado documental con el código y la evidencia reproducible del repositorio.

No redefine RADAR ni modifica su arquitectura. Su función es declarar qué capacidades están verificadas, cuáles están implementadas sin evidencia real suficiente y cuál es la única especificación activa.

## Baseline

```text
HEAD_BEFORE_RECONCILIATION: b1b2c4c
BRANCH: main
WORKING_TREE_BEFORE: clean
TEST_BASELINE: 84 passed
```

## Alcance de esta reconciliación

Solo documentación. No se modifica código productivo, configuración ejecutable, base local, corpus, credenciales ni integraciones externas.

## Estado por especificación

| Especificación | Estado operativo reconciliado | Evidencia | Gate pendiente |
|---|---|---|---|
| SPEC-001 Descubrimiento e ingesta | VERIFIED | Ejecuciones reales de last30days, JSON v1.2, normalización, persistencia, deduplicación y API | Ninguno dentro de su alcance |
| SPEC-001A Calidad de corpus v1 | VERIFIED | 10 consultas reales, 4 resultados, 2 substantive, 2 review, informe reproducible | Ninguno dentro de su alcance |
| SPEC-001B Repertorio v2 | IMPLEMENTING — ACTIVE | Catálogo de 20 consultas y runner existentes | Ejecutar corpus v2, comparar contra v1 y decidir repertorio operativo |
| SPEC-001C Escaneo por fuentes | IMPLEMENTING — QUEUED | 15 fuentes, 15 planes y validación de cobertura | Ejecutar al menos tres modalidades y producir informe comparativo por fuente |
| SPEC-002 Afinidad e intención | IMPLEMENTING — BLOCKED BY HUMAN CORPUS AND SPEC-001B | Clasificador determinístico, Agnes estructurado, persistencia y calibración DRAFT | Cerrar SPEC-001B; luego corpus humano mínimo, positivos/negativos/ambiguos y precisión medida |
| SPEC-003 Revisión humana | IMPLEMENTING — REAL USE PENDING AFTER SPEC-001B | API, bandeja, decisiones, eventos y bloqueo de contacto sin aprobación | Cerrar SPEC-001B y luego uso verificable con diez conversaciones reales |
| SPEC-004 Relaticle | DRAFT — BLOCKED | Frontera local que impide llamadas no auditadas | Auditoría real del contrato/API de Relaticle |
| SPEC-005 Precalificación | IMPLEMENTING — REAL USE PENDING AFTER SPEC-001B | Reglas determinísticas, consentimiento, persistencia y paquete CRM local | Cerrar SPEC-001B y luego ejecución con respuestas reales y confirmación humana |
| SPEC-006 Piloto integral | DRAFT — BLOCKED BY SPEC-001B AND PREVIOUS GATES | Flujo objetivo documentado | Todos los gates previos y al menos un caso real extremo a extremo |

## Única especificación activa

```text
SPEC-001B — Repertorio de búsqueda v2
```

Ninguna otra especificación debe ampliarse hasta cerrar el gate de SPEC-001B.

## Capacidades verificadas

- integración real con last30days mediante subprocess controlado;
- contrato JSON agent v1.2;
- normalización, persistencia y deduplicación;
- API local y bandeja web;
- evaluación determinística y semántica estructurada;
- integración Agnes endurecida;
- prioridad y acción final calculadas por RADAR;
- revisión humana obligatoria antes de registrar contacto;
- precalificación determinística y consentimiento separado;
- bloqueo explícito de Relaticle no auditado.

## Capacidades no verificadas como producto real

- repertorio v2 ejecutado y comparado;
- escaneo operativo de fuentes concretas;
- corpus humano de calibración;
- precisión semántica con muestra suficiente;
- revisión de diez conversaciones reales;
- acercamiento real aprobado y respuesta registrada;
- precalificación con una persona real;
- transferencia real a Relaticle;
- piloto extremo a extremo.

## Datos locales actuales

Los archivos bajo `data/` son evidencia local y permanecen fuera del commit cuando están ignorados.

El corpus exportado desde evaluaciones persistidas continúa:

```text
status = DRAFT
label_provenance = MACHINE_SEEDED_REQUIRES_HUMAN_REVIEW
human_validated = false
ready_for_pilot = false
```

No autoriza calibración válida ni piloto.

Los casos locales actuales no deben presentarse como muestra comercial válida hasta completar la ejecución y selección del repertorio v2.

## Regla de avance

El siguiente trabajo permitido es únicamente:

```text
ejecutar SPEC-001B
→ producir corpus-v2/report.json
→ comparar v1 contra v2
→ documentar KEEP / REFINE / REJECT
→ cerrar o corregir SPEC-001B
```

No corresponde durante este ciclo:

- modificar Agnes;
- calibrar el modelo;
- limpiar manualmente SQLite;
- cargar conversaciones inventadas;
- ampliar la bandeja;
- integrar Relaticle;
- implementar conectores para las 15 fuentes;
- iniciar el piloto.

## Validación de la reconciliación

```text
python -m pytest -q
84 passed
```

La reconciliación debe cerrarse en un commit exclusivamente documental antes de ejecutar SPEC-001B.
