# SPEC-004 — Integración con Relaticle

**Estado:** DRAFT — BLOQUEADA POR AUDITORÍA EXTERNA Y GATES PREVIOS

## Propósito

Transferir a Relaticle únicamente personas y leads que hayan atravesado los gates autorizados, sin duplicaciones ni pérdida de evidencia.

Relaticle no recibe conversaciones crudas ni candidatos prematuros.

## Autoridad

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`;
- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/specs/003A_discovery_funnel.md`;
- `docs/specs/005_qualification.md`.

## Gate mínimo

La transferencia comercial estándar requiere:

```text
PREQUALIFICATION_ACCEPTED
→ QUALIFICATION_STARTED
→ QUALIFIED | PRIORITY_QUALIFIED
→ consentimiento vigente
```

Una persona puede crearse antes únicamente por una decisión comercial explícita y documentada, con identidad utilizable, finalidad legítima y consentimiento suficiente. Esa excepción no autoriza crear oportunidad.

## Registros posibles

- persona;
- nota con procedencia y evidencia;
- tarea;
- oportunidad, solo cuando corresponda;
- vínculo local-remoto;
- estado de sincronización.

## Evidencia transferible

- identidad y canal autorizados;
- resultado humano de descubrimiento;
- consentimiento;
- respuestas de precalificación;
- cualificación;
- camino recomendado y su fundamento;
- objeciones;
- siguiente acción aprobada.

No transferir como hechos:

- inferencias tomadas de una publicación pública;
- arquetipo no confirmado;
- capacidad no declarada;
- afinidad meramente aparente.

## Reglas

- usar API real auditada;
- no inventar rutas, entidades ni autenticación;
- conservar ID remoto;
- registrar errores;
- aplicar reintentos idempotentes;
- no crear persona sin identidad o vía legítima;
- no crear oportunidad para `NO_CALIFICADO` o `EN_MADURACION`;
- no transferir sin consentimiento;
- evitar duplicados;
- conservar trazabilidad de cada campo enviado.

## Bloqueo vigente

La frontera local rechaza transferencias porque la API real de Relaticle no fue auditada.

Además, el embudo de descubrimiento y el gate `PREQUALIFICATION_ACCEPTED` todavía no están implementados.

## Criterios de aceptación pendientes

- auditar contrato y autenticación reales;
- aprobar el mapeo de datos;
- crear un registro real permitido;
- leerlo nuevamente;
- actualizar su estado;
- evitar duplicado en un segundo envío;
- guardar vínculo local-remoto;
- bloquear casos prematuros;
- demostrar que una oportunidad solo se crea para un lead autorizado.

## Prohibición de implementación

Mientras esta especificación permanezca `DRAFT`, no autoriza llamadas reales ni adaptación de endpoints.
