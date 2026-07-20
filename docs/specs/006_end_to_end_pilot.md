# SPEC-006 — Piloto integral

**Estado:** DRAFT — BLOQUEADA POR SPEC-001B, SPEC-002, SPEC-003, SPEC-003A, SPEC-005 Y RELATICLE

## Propósito

Demostrar con conversaciones y personas reales el recorrido completo de RADAR, incluida la frontera entre descubrimiento humano y conversión.

Esta especificación no puede implementarse mientras permanezcan abiertos los gates de:

- descubrimiento operativo;
- interpretación semántica validada;
- revisión humana real;
- embudo de descubrimiento;
- consentimiento y precalificación;
- Relaticle auditado.

## Flujo obligatorio

```text
consulta real
→ descubrimiento
→ ingesta
→ interpretación de afinidad aparente
→ revisión humana
→ candidato de descubrimiento
→ acercamiento humano
→ respuesta
→ diálogo de descubrimiento
→ afinidad revelada o descartada
→ consentimiento para continuar
→ precalificación
→ lead calificado
→ transferencia controlada a Relaticle
```

No se considera piloto integral un caso que salte directamente de respuesta a precalificación.

## Muestra

Entre 100 y 300 conversaciones para evaluar búsqueda y semántica.

El tramo humano debe incluir casos reales suficientes para observar:

- contacto aprobado;
- respuesta;
- ausencia de respuesta;
- afinidad revelada;
- afinidad no confirmada;
- consentimiento;
- rechazo de continuidad;
- precalificación iniciada;
- cualificación final.

## Métricas

### Descubrimiento público

- conversaciones recuperadas;
- conversaciones sustantivas;
- falsos positivos;
- conversaciones aparentemente afines;
- evidencia inválida o insuficiente.

### Revisión y contacto

- candidatos revisados;
- contactos aprobados;
- contactos realizados;
- respuestas;
- no respuestas;
- `DO_NOT_CONTACT`.

### Descubrimiento humano

- diálogos iniciados;
- afinidades reveladas;
- afinidades ambiguas;
- afinidades no confirmadas;
- hipótesis de arquetipo confirmadas humanamente;
- personas que desean continuar;
- consentimientos y rechazos.

### Conversión

- invitaciones a precalificación;
- cuestionarios aceptados e iniciados;
- cuestionarios completados;
- no calificados;
- en maduración;
- calificados;
- prioritarios;
- transferencias y oportunidades creadas.

## Criterios de cierre

- al menos un caso real atraviesa todo el circuito sin intervención técnica manual sobre la base;
- ningún arquetipo se asigna desde la conversación pública;
- la afinidad revelada es registrada por un humano;
- la precalificación permanece bloqueada sin consentimiento;
- la transferencia solo ocurre para un lead permitido;
- toda transición puede reconstruirse mediante evidencia persistida;
- se documentan también casos que terminan correctamente en descarte o cierre de descubrimiento.

## Prohibición de implementación

Mientras esta especificación permanezca `DRAFT`, no autoriza ejecución de piloto comercial ni cambios de código específicos del piloto.
