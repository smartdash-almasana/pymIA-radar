# SPEC-003 — Bandeja de revisión humana

**Estado:** IMPLEMENTING

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
- pruebas de bloqueo sin aprobación y trazabilidad completa.

## Pendiente para cierre

- interfaz web de bandeja;
- filtros y paginación;
- visualización conjunta de evaluación, evidencia, revisiones y eventos;
- edición desde interfaz;
- pruebas de uso con diez conversaciones reales.
