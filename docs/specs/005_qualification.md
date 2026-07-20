# SPEC-005 — Precalificación

**Estado:** DRAFT — BLOQUEADA POR SPEC-003A Y VALIDACIÓN DOCUMENTAL

## Propósito

Determinar, de manera visible y reproducible, si una persona que completó el embudo humano de descubrimiento está lista para acceder a agenda, debe entrar en maduración o debe recibir únicamente educación sin calendario.

Esta especificación implementa el `Mini-Formulario Portero` definido en el Informe Estratégico Inlak’ech 2.0 y queda subordinada a:

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`;
- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/DOCUMENT_PRECEDENCE.md`;
- `docs/specs/003A_discovery_funnel.md`;
- documentos maestros de Inlak’ech.

## Gate obligatorio de entrada

La precalificación solo puede comenzar cuando existen simultáneamente:

```text
respuesta humana verificable
+
afinidad revelada o interés suficiente
+
voluntad expresa de continuar
+
consentimiento explícito para precalificación
```

Debe existir un estado previo:

```text
PREQUALIFICATION_ACCEPTED
```

Sin ese estado, `QUALIFICATION_STARTED` está prohibido.

La afinidad semántica aparente de una publicación pública no habilita esta especificación.

## Cinco dimensiones del mini-formulario

### 1. Perfil identitario declarado

- `INVERSOR`;
- `RESIDENTE`;
- `ARTIFICE`;
- `NO_DEFINIDO`.

### 2. Capacidad de capital declarada

- `< USD 50.000`;
- `USD 50.000–150.000`;
- `> USD 150.000`;
- no declarado.

Nunca inferir capital por profesión, ubicación, apariencia, lenguaje o perfil público.

### 3. Horizonte temporal declarado

- este mes;
- 3–6 meses;
- 6–12 meses;
- solo mirando;
- sin definir.

### 4. Motivación

- respuesta breve abierta;
- evaluación humana o semántica separada de coherencia;
- conservación del texto original.

### 5. Anclaje del Artífice

- tierra;
- capital;
- talento.

El anclaje solo corresponde cuando el perfil declarado es `ARTIFICE`.

Seleccionar un tipo no alcanza para obtener verde. Debe existir una descripción concreta y revisable.

## Separaciones obligatorias

```text
arquetipo
!= perfil identitario del mini-formulario
!= camino de participación
```

- El arquetipo solo puede surgir como hipótesis posterior al diálogo humano y debe ser confirmado por una persona.
- El perfil identitario es una autodefinición situada en el mini-formulario.
- El camino de participación es una recomendación comercial basada en respuestas documentadas.

Ninguna dimensión sustituye automáticamente a otra.

## Semáforo determinístico

### ROJO

Criterios iniciales:

- capital declarado inferior a USD 50.000;
- horizonte `SOLO_MIRANDO`;
- perfil sin definir;
- Artífice sin tipo de anclaje;
- información incompatible con los caminos vigentes.

Resultado:

```text
NO_CALIFICADO
→ EDUCACION_SIN_CALENDARIO
```

### AMARILLO

Criterios iniciales:

- capital compatible, pero horizonte de 3–6 o 6–12 meses;
- capital no declarado;
- motivación aún no confirmada;
- información mínima incompleta;
- objeciones que requieren maduración.

Resultado:

```text
EN_MADURACION
→ MADURACION
```

### VERDE

Criterios iniciales:

- capital en rango compatible;
- disponibilidad este mes;
- motivación coherente;
- información mínima completa;
- consentimiento vigente.

Resultado:

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

El `RESIDENTE` con capacidad alta puede activar la recomendación de `FUNDADOR_CIMENTACION_INTEGRAL`.

El `SEMBRADOR_PATRIMONIAL` sigue siendo un camino oficial y se preserva cuando fue seleccionado o expresado por la persona en un selector autorizado. No se deduce únicamente del perfil `INVERSOR` ni del rango de capital.

Toda recomendación requiere confirmación humana antes de considerarse una decisión comercial definitiva.

## Consentimiento

El consentimiento es un gate ético independiente del semáforo de ajuste.

Una persona puede mostrar ajuste verde, pero sin consentimiento vigente:

- no accede a calendario;
- no se transfiere al CRM;
- no se registra contacto comercial adicional;
- no se crea oportunidad.

El consentimiento no puede inferirse de una respuesta positiva genérica.

## Estados

Entrada requerida:

- `PREQUALIFICATION_ACCEPTED`.

Estados de esta especificación:

- `QUALIFICATION_STARTED`;
- `NURTURING`;
- `QUALIFIED`;
- `PRIORITY_QUALIFIED`;
- `NO_CALIFICADO` como resultado de cualificación;
- `EN_MADURACION` como estado comercial derivado.

## Restricciones

- no iniciar desde `DETECTED`, `REVIEW_PENDING`, `DISCOVERY_CONTACTED` o `DISCOVERY_REPLIED`;
- no inferir capital;
- no equiparar arquetipo y camino;
- no crear oportunidad para rojo o amarillo;
- no transferir datos sin consentimiento;
- no inventar el camino Sembrador;
- conservar todas las respuestas que originaron la recomendación;
- permitir revisión humana de toda salida;
- conservar la procedencia del consentimiento.

## Implementación vigente reutilizable

- contrato Pydantic;
- semáforo determinístico rojo, amarillo y verde;
- Artífice con anclaje documentado;
- consentimiento separado del ajuste comercial;
- persistencia del resultado;
- paquete CRM local restringido a `CALIFICADO` o `PRIORITARIO` con consentimiento;
- integración externa bloqueada hasta auditar Relaticle.

## Gaps de implementación

- el enum actual no contiene `PREQUALIFICATION_INVITED` ni `PREQUALIFICATION_ACCEPTED`;
- el flujo actual puede avanzar de `REPLIED` a `QUALIFICATION_STARTED` sin representar el resultado del descubrimiento;
- no existe `DiscoveryOutcome`;
- el gate nuevo todavía no está implementado;
- los tests vigentes no prueban toda la frontera entre descubrimiento y conversión.

## Criterios de aceptación

- SPEC-003A implementada y verificada;
- `PREQUALIFICATION_ACCEPTED` persistido con evidencia;
- reglas aplicadas a respuestas reales;
- capital e horizonte provenientes de declaración explícita;
- persona responsable puede revisar y corregir la recomendación;
- persistencia y recuperación demostradas;
- intentos prematuros bloqueados;
- consentimiento revocable y trazable;
- Relaticle auditado antes de transferencia externa.

## Prohibición de implementación

Mientras esta especificación permanezca `DRAFT`, no autoriza cambios de código.
