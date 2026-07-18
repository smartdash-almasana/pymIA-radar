# M0 — Baseline local verificable

**Estado:** VERIFIED_LOCAL

**Fecha:** 2026-07-18

## Alcance verificado

La baseline local de Inlak'ech RADAR fue validada sin depender de Docker.

Circuito demostrado:

```text
/health
→ creación de conversación
→ persistencia
→ reingesta sin duplicación
→ listado
→ evaluación
→ revisión humana
→ actualización de estado
```

## Evidencia

Comando:

```text
python -m pytest -q
```

Resultado más reciente:

```text
4 passed
```

Pruebas relevantes:

- `tests/test_health.py`
- `tests/test_classifier.py`
- `tests/test_api_flow.py`

## Decisiones aplicadas

- SQLite se usa exclusivamente como base aislada de pruebas.
- La base temporal se crea dentro de `.pytest_cache/`.
- PostgreSQL sigue siendo la base prevista para ejecución persistente real.
- Docker Compose es opcional para desarrollo local y recomendable para empaquetado y despliegue reproducible.
- La falta o demora de Docker no bloquea M0 local ni la preparación metodológica de M1.

## Límites de esta verificación

No queda verificado todavía:

- Docker Compose;
- PostgreSQL en contenedor;
- despliegue remoto;
- descubrimiento real con `last30days-skill`;
- integración real con Relaticle;
- precisión del motor semántico sobre corpus real.

## Estado de avance

```text
M0_LOCAL = VERIFIED
M0_DOCKER = PENDING
M1_IMPLEMENTATION = NOT_AUTHORIZED
SPEC_001 = DRAFT
```

## Próxima acción metodológica

Auditar `last30days-skill`, revisar y completar `SPEC-001`, y solicitar su aprobación antes de implementar descubrimiento real.
