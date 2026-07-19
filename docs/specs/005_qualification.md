# SPEC-005 — Precalificación

**Estado:** IMPLEMENTING — REAL USE PENDING AFTER SPEC-001B

## Propósito

Determinar, de manera visible y reproducible, si una persona está lista para acceder a agenda, debe entrar en maduración o debe recibir únicamente educación sin calendario.

Esta especificación implementa el `Mini-Formulario Portero` definido en el Informe Estratégico Inlak’ech 2.0 y queda subordinada a:

- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/DOCUMENT_PRECEDENCE.md`;
- documentos maestros de Inlak’ech.

## Cinco dimensiones del mini-formulario

1. **Perfil identitario**
   - `INVERSOR`;
   - `RESIDENTE`;
   - `ARTIFICE`.

2. **Capacidad de capital declarada**
   - `< USD 50.000`;
   - `USD 50.000–150.000`;
   - `> USD 150.000`;
   - no declarado.

3. **Horizonte temporal**
   - este mes;
   - 3–6 meses;
   - 6–12 meses;
   - solo mirando;
   - sin definir.

4. **Motivación**
   - respuesta breve abierta;
   - evaluación humana o semántica separada de coherencia.

5. **Anclaje del Artífice**
   - tierra;
   - capital;
   - talento.

El anclaje solo corresponde cuando el perfil declarado es `ARTIFICE`.

Seleccionar `TIERRA`, `CAPITAL` o `TALENTO` no alcanza para obtener verde. Debe existir una descripción concreta y revisable del anclaje. La ausencia de tipo de anclaje produce rojo; un tipo declarado sin evidencia suficiente produce amarillo.

## Regla de separación

```text
perfil identitario del mini-formulario
!= arquetipo psicológico
!= camino de participación
```

El arquetipo puede ser propuesto por RADAR con evidencia. El camino se recomienda a partir de las respuestas documentadas y debe poder revisarse humanamente.

## Semáforo determinístico

### ROJO

Criterios:

- capital declarado inferior a USD 50.000;
- horizonte `SOLO_MIRANDO`;
- perfil sin definir;
- Artífice sin tipo de anclaje.

Resultado:

```text
NO_CALIFICADO
→ EDUCACION_SIN_CALENDARIO
```

### AMARILLO

Criterios:

- capital compatible, pero horizonte de 3–6 meses o 6–12 meses;
- capital todavía no declarado;
- motivación aún no confirmada;
- información mínima incompleta.

Resultado:

```text
EN_MADURACION
→ MADURACION
```

### VERDE

Criterios:

- capital en rango compatible;
- disponibilidad este mes;
- motivación coherente;
- información mínima completa.

Resultado comercial:

```text
CALIFICADO
```

Si además solicita expresamente avanzar:

```text
PRIORITARIO
```

## Recomendación inicial de camino

Según el Informe Estratégico 2.0:

```text
USD 50.000–150.000
→ FUNDADOR_CIMENTACION_ESENCIAL

> USD 150.000
→ FUNDADOR_CIMENTACION_INTEGRAL

ARTIFICE con anclaje
→ ARTIFICE_ANCLAJE
```

El `RESIDENTE` con capacidad alta activa la recomendación de `FUNDADOR_CIMENTACION_INTEGRAL`.

El `SEMBRADOR_PATRIMONIAL` sigue siendo un camino oficial. Se preserva como recomendación cuando la persona lo seleccionó previamente en el selector orientativo del embudo; no se deduce únicamente del perfil `INVERSOR` ni del rango de capital.

Toda recomendación de camino es provisional y requiere confirmación humana antes de considerarse una decisión comercial definitiva.

## Consentimiento

El consentimiento es un gate ético independiente del semáforo de ajuste.

Una persona puede mostrar ajuste verde, pero sin consentimiento explícito:

- no accede a calendario;
- no se transfiere al CRM;
- no se registra contacto comercial adicional.

## Estados

- `NO_CALIFICADO`;
- `EN_MADURACION`;
- `CALIFICADO`;
- `PRIORITARIO`.

## Restricciones

- no inferir capital por profesión, ubicación o perfil público;
- no equiparar arquetipo y camino;
- no crear oportunidad en CRM para rojo o amarillo;
- no transferir datos sin consentimiento;
- no inventar el camino Sembrador cuando el mini-formulario no lo determina;
- toda recomendación de camino debe conservar las respuestas que la originaron.

## Implementado en este corte

- contrato Pydantic validado;
- semáforo determinístico rojo, amarillo y verde;
- Artífice con anclaje documentado;
- consentimiento separado del ajuste comercial;
- persistencia del resultado de precalificación;
- paquete CRM local permitido solo para `CALIFICADO` o `PRIORITARIO` con consentimiento;
- integración externa bloqueada hasta auditar Relaticle.

## Criterios de aceptación pendientes

- aplicar las reglas a respuestas reales obtenidas después de un acercamiento aprobado;
- confirmar que la persona responsable puede revisar y corregir la recomendación de camino;
- demostrar persistencia y recuperación del resultado en un caso real;
- auditar Relaticle antes de cualquier transferencia externa.
