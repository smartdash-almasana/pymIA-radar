# AGENTS.md — Reglas de desarrollo de Inlak'ech Radar

## Misión única

Construir una solución dedicada a un solo cliente que:

1. encuentre conversaciones públicas relevantes;
2. evalúe afinidad e intención con evidencia;
3. obligue a revisión humana;
4. facilite un acercamiento ético;
5. precalifique al interesado;
6. transfiera el lead calificado al embudo comercial.

## Fuera de alcance

No desarrollar:

- SaaS multiempresa;
- facturación;
- planes;
- administración de organizaciones;
- chatbot institucional;
- RAG general;
- publicación automática;
- scraping autenticado masivo;
- contacto automático sin aprobación;
- CRM propio;
- infraestructura distribuida.

## Principios técnicos

- Python 3.12.
- FastAPI, SQLAlchemy, PostgreSQL, Jinja/HTMX.
- Docker Compose para desarrollo y despliegue inicial.
- Reutilizar last30days-skill para descubrimiento.
- Reutilizar Relaticle para seguimiento comercial.
- Toda clasificación debe devolver evidencia.
- Toda acción externa exige aprobación humana.
- No inventar endpoints ni contratos de repositorios externos.
- Auditar primero; adaptar después.
- No incorporar Redis, Celery, pgvector o frontend separado sin evidencia de necesidad.

## Regla de avance

Ninguna fase se considera terminada por tener código escrito.

Debe cumplir:

- especificación;
- pruebas focales;
- criterio de aceptación;
- evidencia reproducible;
- documentación actualizada.

## Estado permitido de una especificación

- DRAFT
- APPROVED
- IMPLEMENTING
- VERIFIED
- BLOCKED
- SUPERSEDED

Solo una especificación `APPROVED` puede pasar a implementación.
