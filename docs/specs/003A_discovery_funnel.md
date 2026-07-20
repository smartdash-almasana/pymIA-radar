# SPEC-003A — Embudo humano de descubrimiento

**Estado:** DRAFT

## Propósito

Representar y administrar el tramo humano situado entre la aprobación de un acercamiento y la invitación a precalificación.

Su función es permitir que una persona conozca Inlak’ech y revele libremente si existe simpatía, identificación, curiosidad o afinidad real.

No es una etapa de venta ni una precalificación encubierta.

## Autoridad

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`;
- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/DOCUMENT_PRECEDENCE.md`;
- documentos filosóficos y de arquetipos de Inlak’ech.

## Entrada

Un candidato de descubrimiento aprobado humanamente mediante SPEC-003.

Debe existir:

- conversación original;
- identidad pública utilizable o vía legítima de contacto;
- decisión humana de aprobación;
- mensaje aprobado o editado;
- trazabilidad de la revisión.

## Flujo

```text
DISCOVERY_CANDIDATE
→ DISCOVERY_APPROACH_APPROVED
→ DISCOVERY_CONTACTED
→ DISCOVERY_REPLIED
→ DISCOVERY_DIALOGUE_ACTIVE
→ AFFINITY_REVEALED | AFFINITY_NOT_CONFIRMED
→ DISCOVERY_CLOSED | PREQUALIFICATION_INVITED
→ PREQUALIFICATION_ACCEPTED
```

## Estados objetivo

- `DISCOVERY_CANDIDATE`;
- `DISCOVERY_APPROACH_APPROVED`;
- `DISCOVERY_CONTACTED`;
- `DISCOVERY_REPLIED`;
- `DISCOVERY_DIALOGUE_ACTIVE`;
- `AFFINITY_REVEALED`;
- `AFFINITY_NOT_CONFIRMED`;
- `DISCOVERY_CLOSED`;
- `PREQUALIFICATION_INVITED`;
- `PREQUALIFICATION_ACCEPTED`.

Los estados pueden implementarse mediante eventos y una proyección de estado. No se exige una tabla por estado.

## Eventos mínimos

- aprobación de contacto;
- contacto realizado;
- respuesta recibida;
- diálogo iniciado;
- nota humana;
- afinidad revelada;
- afinidad no confirmada;
- cierre de descubrimiento;
- invitación a precalificación;
- aceptación o rechazo de precalificación.

## Resultado humano

Debe existir un `DiscoveryOutcome` o equivalente con:

```text
conversation_id
person_identity_reference
sympathy_revealed
revealed_affinity_level
revealed_affinity_domains
motivation_declared
questions_or_interests
objections
wants_to_continue
consent_to_prequalification
human_notes
recorded_by
recorded_at
```

Valores iniciales:

```text
sympathy_revealed:
NO | UNCLEAR | YES

revealed_affinity_level:
NONE | PARTIAL | CLEAR
```

## Afinidad revelada

La afinidad se considera revelada cuando la persona, después de conocer suficientemente Inlak’ech, expresa de manera propia y verificable:

- qué le interesa;
- por qué le importa;
- con qué aspectos conecta;
- qué desea comprender o explorar;
- si quiere continuar.

El LLM puede resumir el diálogo, pero el registro de afinidad es una decisión humana.

## Arquetipos

Los arquetipos no pueden provenir de la conversación pública inicial.

Después de diálogo humano suficiente puede registrarse una hipótesis:

```text
archetype_hypothesis
archetype_evidence
archetype_confidence
human_confirmed
confirmed_by
confirmed_at
```

Reglas:

- la evidencia debe provenir del diálogo humano;
- la hipótesis puede permanecer `NO_DEFINIDO`;
- la confirmación es humana;
- no equivale a perfil declarado;
- no equivale a camino de participación;
- no determina la calificación.

## Gate hacia precalificación

Solo puede emitirse `PREQUALIFICATION_INVITED` cuando existen:

- respuesta humana verificable;
- afinidad revelada o interés suficiente;
- voluntad expresa de continuar;
- contexto legítimo para ofrecer la siguiente etapa.

Solo puede emitirse `PREQUALIFICATION_ACCEPTED` con consentimiento explícito.

La ausencia de respuesta, afinidad no confirmada o rechazo debe bloquear SPEC-005.

## Prohibiciones

- contacto automático;
- venta agresiva;
- urgencia artificial;
- inferencia de capacidad económica;
- recolección encubierta de datos;
- arquetipo automático;
- consentimiento inferido;
- precalificación sin invitación y aceptación;
- transferencia prematura al CRM.

## Integración con componentes actuales

Puede reutilizar:

- `ReviewDecision` para aprobación;
- `EngagementEvent` para contacto y respuesta;
- historial y notas existentes;
- interfaz actual como base.

Debe agregarse o evolucionar:

- representación del caso de descubrimiento;
- resultado humano de descubrimiento;
- estados y transiciones;
- gate de precalificación;
- arquetipo posterior al diálogo.

## Criterios de aceptación

- un contacto no puede registrarse sin aprobación;
- una respuesta no confirma automáticamente afinidad;
- el humano puede registrar afinidad revelada, ambigua o no confirmada;
- se conservan motivaciones, preguntas y objeciones;
- el arquetipo permanece vacío antes del diálogo suficiente;
- la invitación a precalificación exige afinidad o interés y voluntad;
- la aceptación exige consentimiento explícito;
- SPEC-005 permanece bloqueada sin aceptación;
- todos los eventos son persistentes y trazables;
- las transiciones inválidas son rechazadas;
- la interfaz separa descubrimiento de precalificación.

## Pruebas objetivo

- flujo exitoso completo;
- contacto sin aprobación bloqueado;
- respuesta sin afinidad;
- afinidad ambigua;
- afinidad revelada sin consentimiento;
- consentimiento sin afinidad suficiente, sujeto a revisión;
- rechazo de continuidad;
- intento de precalificación prematura;
- intento de arquetipo antes del diálogo;
- cierre del caso sin transferencia.

## Estado de implementación

No implementado.

El código vigente no posee todavía `DiscoveryOutcome` ni estados completos de descubrimiento y salta de `REPLIED` a `QUALIFICATION_STARTED`.

Esta especificación debe ser revisada y pasar a `APPROVED` antes de modificar código.
