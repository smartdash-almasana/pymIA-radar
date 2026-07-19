# SPEC-003 — Bandeja de revisión humana

**Estado:** IMPLEMENTING — REAL USE PENDING AFTER SPEC-001B

## Propósito

Permitir que una persona decida qué candidatos avanzan.

## Funciones

- listar;
- filtrar;
- abrir conversación;
- ver evidencia;
- ver URL original;
- aprobar;
- editar respuesta;
- descartar;
- agregar notas.

## Reglas

- ninguna acción externa sin aprobación;
- toda decisión queda registrada;
- el texto sugerido es editable;
- el sistema distingue candidato, contacto y lead.

## Criterios de aceptación

- un usuario puede revisar diez conversaciones;
- puede aprobar, editar y descartar;
- el historial permanece después de reiniciar;
- la acción queda asociada a la conversación correcta.

## Implementado en este corte

- contrato tipado de decisiones humanas;
- aprobación obligatoria antes de registrar contacto;
- historial persistente de revisiones;
- registro persistente de contacto, respuesta, ausencia de respuesta y no contactar;
- transición explícita de estados comerciales;
- bandeja web local con conversación, evaluación, evidencia, decisión, contacto, respuesta, precalificación e historial;
- edición del mensaje desde interfaz;
- filtros locales por estado y búsqueda textual;
- pruebas de bloqueo sin aprobación y trazabilidad completa.

## Pendiente para cierre

- paginación para volúmenes mayores;
- prueba de uso reproducible con diez conversaciones públicas reales;
- evidencia de decisiones humanas persistidas después de reiniciar;
- validación de legibilidad y operación por la persona responsable comercial.
