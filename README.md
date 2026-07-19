# Inlak'ech Radar

Sistema dedicado de prospección conversacional para Inlak'ech.

## Definición canónica

Inlak'ech es el proyecto global.

RADAR no es el proyecto global. Es un instrumento comercial y de inteligencia para ayudar a Inlak'ech a encontrar a las personas correctas.

## Declaración obligatoria

La autoridad principal del producto es `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`.

El contrato funcional integral es `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`.

La política rectora para localizar conversaciones de peso es `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`.

## Objetivo

Encontrar conversaciones públicas afines a Inlak'ech, analizarlas con evidencia, someterlas a revisión humana y facilitar el acercamiento comercial a las personas correctas.

## Arquitectura

```text
motores de descubrimiento y captura asistida
        ↓
normalización, persistencia y deduplicación
        ↓
evaluación multidimensional con evidencia
        ↓
bandeja de revisión humana
        ↓
acercamiento humano y registro de respuesta
        ↓
precalificación y consentimiento
        ↓
lead calificado
        ↓
transferencia controlada a Relaticle
```

## Requisitos

- Docker Desktop
- Docker Compose
- Git
- Python 3.12 (solo para desarrollo fuera de Docker)
- Claves de API según las fuentes y el modelo elegido

## Inicio rápido

1. Copiar `.env.example` como `.env`.
2. Ajustar las variables.
3. Ejecutar:

```bash
docker compose up --build
```

4. Abrir:

- Radar: http://localhost:8000
- Documentación API: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Estado del repositorio

Checkpoint vigente:

```text
docs/CURRENT_ENGINEERING_STATE.md
```

Capacidades con evidencia técnica:

- integración real con `last30days-skill` mediante JSON agent v1.2;
- normalización, persistencia y deduplicación;
- API FastAPI y bandeja local de revisión;
- evaluación determinística y semántica estructurada;
- integración Agnes endurecida con fallback auditable;
- revisión humana obligatoria antes de registrar contacto;
- registro de respuesta y precalificación determinística;
- frontera bloqueada para Relaticle hasta auditar su contrato real.

Capacidades todavía no verificadas como producto real:

- repertorio de búsqueda v2 ejecutado y comparado;
- escaneo operativo por fuentes concretas;
- corpus humano suficiente para calibración;
- precisión semántica medida sobre casos reales;
- revisión, acercamiento, respuesta y precalificación con personas reales;
- transferencia real a Relaticle;
- piloto extremo a extremo.

La única especificación activa en este corte es `SPEC-001B — Repertorio de búsqueda v2`. El resto queda verificado, en cola, bloqueado o pendiente de uso real según `docs/CURRENT_ENGINEERING_STATE.md`.

## Método de desarrollo

El repositorio usa Spec-Driven Development liviano.

Documentos principales:

- `AGENTS.md`
- `docs/SPEC_DRIVEN_DEVELOPMENT.md`
- `docs/PRODUCT_SCOPE.md`
- `docs/ACCEPTANCE_MATRIX.md`
- `docs/MILESTONES.md`
- `docs/specs/`
