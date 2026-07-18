# Inlak'ech Radar

Sistema dedicado de prospección conversacional para Inlak'ech.

## Definición canónica

Inlak'ech es el proyecto global.

RADAR no es el proyecto global. Es un instrumento comercial y de inteligencia para ayudar a Inlak'ech a encontrar a las personas correctas.

## Declaración obligatoria

La autoridad principal del producto es `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`.

La política rectora para localizar conversaciones de peso es `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`.

## Objetivo

Encontrar conversaciones públicas afines a Inlak'ech, analizarlas con evidencia, someterlas a revisión humana y facilitar el acercamiento comercial a las personas correctas.

## Arquitectura

```text
last30days-skill
        ↓
adaptador de descubrimiento
        ↓
motor de afinidad e intención
        ↓
bandeja de revisión humana
        ↓
Relaticle
        ↓
cuestionario de precalificación
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

Este ZIP contiene el esqueleto funcional del proyecto:

- API FastAPI
- PostgreSQL
- modelos iniciales
- configuración narrativa de Inlak'ech
- endpoint de clasificación preliminar
- endpoint de revisión
- cliente inicial para Relaticle
- adaptador inicial para last30days-skill
- cuestionario de precalificación
- pruebas básicas

Todavía deben conectarse las credenciales reales, auditarse los repositorios externos y calibrarse el motor semántico con los documentos maestros completos.

## Método de desarrollo

El repositorio usa Spec-Driven Development liviano.

Documentos principales:

- `AGENTS.md`
- `docs/SPEC_DRIVEN_DEVELOPMENT.md`
- `docs/PRODUCT_SCOPE.md`
- `docs/ACCEPTANCE_MATRIX.md`
- `docs/MILESTONES.md`
- `docs/specs/`
