# Registro de decisiones

## D-001 — Solución dedicada

Se construye para un solo cliente. Se pospone cualquier arquitectura SaaS.

## D-002 — Descubrimiento reutilizado

Se reutiliza last30days-skill. No se reconstruye su lógica sin una causa técnica demostrada.

## D-003 — CRM reutilizado

Se reutiliza Relaticle. No se construye un CRM propio.

## D-004 — Aplicación monolítica modular

FastAPI + Jinja/HTMX + PostgreSQL en un único repositorio.

## D-005 — Revisión humana obligatoria

El sistema no contacta ni publica automáticamente.

## D-006 — Clasificación híbrida

Filtro determinístico más modelo estructurado, siempre con evidencia.

## D-007 — Infraestructura simple

El desarrollo local puede ejecutarse sin Docker con Python, FastAPI y una base aislada para pruebas. Docker Compose queda como opción recomendada para empaquetado reproducible, validación de PostgreSQL en contenedor y despliegue posterior en una única VM.

La ausencia o demora de Docker no bloquea el desarrollo funcional ni el cierre de la baseline local.
