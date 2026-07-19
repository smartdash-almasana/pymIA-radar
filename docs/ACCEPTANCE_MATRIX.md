# Matriz de aceptación

| ID | Capacidad | Evidencia exigida | Estado |
|---|---|---|---|
| A-01 | Ejecutar búsqueda real | Resultado con texto, URL, fuente y fecha | VERIFICADO — SPEC-001 / M1 |
| A-02 | Normalizar resultados | Contrato único validado | VERIFICADO — JSON agent v1.2 |
| A-03 | Evitar duplicados | Segunda ingesta no duplica registros | VERIFICADO — idempotencia real |
| A-04 | Clasificar afinidad | Puntaje y evidencia para corpus real | IMPLEMENTADO — BLOQUEADO POR SPEC-001B Y CORPUS HUMANO |
| A-05 | Detectar intención | Separar afinidad de intención comercial | IMPLEMENTADO — BLOQUEADO POR SPEC-001B Y CALIBRACIÓN |
| A-06 | Explicar decisión | Evidencias, faltantes y riesgos | IMPLEMENTADO — VALIDACIÓN REAL POSTERIOR A SPEC-001B |
| A-07 | Revisar humanamente | Aprobar, editar y descartar | IMPLEMENTADO — USO REAL POSTERIOR A SPEC-001B |
| A-08 | Sugerir acercamiento | Mensaje coherente y editable | PARCIAL — VALIDACIÓN REAL POSTERIOR A SPEC-001B |
| A-09 | Crear candidato CRM | Registro real en Relaticle | BLOQUEADO — RELATICLE NO AUDITADO |
| A-10 | Precalificar | Reglas aplicadas a respuestas reales | IMPLEMENTADO — USO REAL POSTERIOR A SPEC-001B |
| A-11 | Crear oportunidad | Oportunidad y tarea en Relaticle | BLOQUEADO — RELATICLE NO AUDITADO |
| A-12 | E2E completo | Evidencia reproducible del circuito | PENDIENTE |

## Regla

Un estado solo puede cambiar a `VERIFICADO` si existe:

- comando de prueba;
- resultado;
- fecha;
- artefacto o captura;
- referencia al commit.

El detalle consolidado de evidencia, bloqueos y única especificación activa se mantiene en `docs/CURRENT_ENGINEERING_STATE.md`.
