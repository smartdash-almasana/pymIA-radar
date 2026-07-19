# SPEC-004 — Integración con Relaticle

**Estado:** DRAFT — BLOCKED

## Propósito

Transferir candidatos aprobados al CRM sin duplicaciones ni pérdida de evidencia.

## Registros mínimos

- persona;
- oportunidad;
- tarea;
- nota con fuente y conversación;
- campos de afinidad e intención.

## Reglas

- usar API real auditada;
- no inventar rutas;
- conservar ID remoto;
- registrar errores;
- reintentos idempotentes;
- no crear persona antes de tener identidad o vía legítima de contacto.

## Bloqueo vigente

La frontera local existe y rechaza cualquier transferencia porque la API real de Relaticle no fue auditada. No se permite inventar endpoints, autenticación ni entidades remotas.

## Criterios de aceptación pendientes

- auditar contrato y autenticación reales;
- crear un registro real;
- leerlo nuevamente;
- actualizar su estado;
- evitar duplicado en un segundo envío;
- guardar vínculo local-remoto.
