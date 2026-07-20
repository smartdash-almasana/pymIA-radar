# SPEC-003 — Bandeja de revisión humana

**Estado:** DRAFT — REQUIERE APROBACIÓN TRAS RECONCILIACIÓN DOCUMENTAL

## Propósito

Permitir que una persona revise conversaciones aparentemente afines y decida si existe fundamento legítimo para abrir un contacto humano de descubrimiento.

La revisión no aprueba una venta, una precalificación ni una transferencia comercial.

## Entradas

- conversación original;
- fuente, URL y fecha;
- autor o identidad pública disponible;
- consulta de origen;
- evaluación semántica provisional de SPEC-002;
- evidencia, contradicciones e incertidumbre;
- propuesta editable de acercamiento.

## Funciones

- listar y filtrar conversaciones;
- abrir el contexto completo;
- ver evidencia literal;
- ver URL original;
- revisar afinidad e intención aparentes;
- aprobar contacto de descubrimiento;
- editar el mensaje;
- observar o posponer;
- descartar;
- marcar `DO_NOT_CONTACT`;
- marcar duplicado;
- agregar notas;
- abrir un caso de descubrimiento después de la aprobación.

## Decisiones humanas objetivo

- `APPROVE_DISCOVERY_APPROACH`;
- `KEEP_OBSERVING`;
- `DISCARD`;
- `DO_NOT_CONTACT`;
- `MARK_DUPLICATE`.

La implementación vigente usa `APPROVE_APPROACH`; su evolución debe preservar compatibilidad y aclarar semánticamente que se trata de un contacto de descubrimiento.

## Reglas

- ninguna acción externa sin aprobación humana;
- toda decisión queda registrada;
- el texto sugerido es editable;
- el sistema distingue conversación, persona, candidato de descubrimiento, participante y lead;
- aprobar el contacto no confirma afinidad;
- aprobar el contacto no inicia precalificación;
- no se muestra arquetipo asignado desde la conversación pública;
- ninguna inferencia financiera participa de la decisión;
- la interfaz debe mostrar incertidumbre y razones para no contactar.

## Resultado

Una aprobación válida puede crear o habilitar un `DiscoveryCase` o representación equivalente.

```text
conversación aparentemente afín
→ revisión humana
→ candidato de descubrimiento
```

El contacto efectivo se registra después mediante un evento verificable.

## Implementación vigente reutilizable

- contrato tipado de decisiones humanas;
- aprobación obligatoria antes de registrar contacto;
- historial persistente de revisiones;
- registro de contacto, respuesta, ausencia de respuesta y no contactar;
- bandeja web local;
- edición del mensaje;
- filtros locales;
- pruebas de bloqueo sin aprobación.

## Gaps de implementación

- semántica de aprobación todavía genérica/comercial;
- ausencia de `DiscoveryCase` explícito;
- ausencia de `DiscoveryOutcome`;
- interfaz todavía combina revisión, contacto y precalificación en una única ficha;
- estados actuales no representan todo el embudo de descubrimiento;
- uso real con conversaciones y decisiones humanas pendiente.

## Criterios de aceptación

- un usuario puede revisar al menos diez conversaciones reales;
- puede comprender tema, contexto, evidencia e incertidumbre;
- puede aprobar, editar, observar, descartar y no contactar;
- ninguna aprobación envía mensajes automáticamente;
- una aprobación crea o habilita un caso de descubrimiento trazable;
- el historial permanece después de reiniciar;
- la acción queda asociada a la conversación correcta;
- la precalificación sigue bloqueada;
- no se asigna arquetipo durante la revisión pública.

## Prohibición de implementación

Mientras esta especificación permanezca `DRAFT`, no autoriza cambios de código.
