# RADAR — Contrato integral de descubrimiento y conversión

## Autoridad

Este documento define el funcionamiento integral de RADAR para el único cliente actual: **Inlak’ech**.

Debe leerse subordinado a:

```text
docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md
docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md
docs/DOCUMENT_PRECEDENCE.md
```

El nombre histórico del archivo se conserva por compatibilidad, pero el contrato ya no describe un recorrido comercial único. Distingue de manera obligatoria:

1. **embudo de descubrimiento**, donde la afinidad puede revelarse mediante vínculo humano;
2. **embudo de conversión**, donde una persona que aceptó continuar puede ser precalificada.

---

## 1. Flujo integral

```text
DESCUBRIMIENTO DE CONVERSACIÓN
→ INTERPRETACIÓN SEMÁNTICA APARENTE
→ REVISIÓN HUMANA
→ IDENTIFICACIÓN DE PERSONA
→ CONTACTO HUMANO DE DESCUBRIMIENTO
→ DIÁLOGO DE DESCUBRIMIENTO
→ AFINIDAD REVELADA O DESCARTADA
→ CONSENTIMIENTO PARA CONTINUAR
→ PRECALIFICACIÓN
→ LEAD CALIFICADO
→ TRANSFERENCIA CONTROLADA A RELATICLE
```

La cartografía de fuentes, las consultas y los conectores son entradas del producto. No constituyen el producto completo.

---

## 2. Definiciones obligatorias

- **Conversación detectada:** hallazgo persistido sin evaluación semántica válida.
- **Conversación aparentemente afín:** conversación cuya interpretación provisional muestra relación plausible con Inlak’ech.
- **Persona potencialmente relevante:** identidad pública asociada a una conversación aparentemente afín.
- **Candidato de descubrimiento:** persona cuya situación fue revisada y aprobada humanamente para considerar un acercamiento.
- **Participante del descubrimiento:** persona efectivamente contactada que está conociendo Inlak’ech.
- **Afinidad revelada:** simpatía, identificación, curiosidad o interés expresados por la persona durante el diálogo humano.
- **Afinidad no confirmada:** ausencia, rechazo o insuficiencia de evidencia humana para continuar.
- **Persona invitada a precalificación:** persona que manifestó voluntad de continuar y recibió una invitación explícita.
- **Precalificado:** persona que respondió información mínima suficiente.
- **Lead calificado:** persona que cumple condiciones explícitas y revisables para ingresar al embudo comercial.
- **Oportunidad:** posibilidad concreta confirmada por el equipo comercial y gestionada en Relaticle.

Está prohibido llamar `lead` a una conversación, a una persona detectada o a un candidato de descubrimiento.

---

## 3. Evaluación semántica de la conversación

La evaluación inicial tiene como objeto la conversación, no la personalidad ni la solvencia del autor.

Debe producir, como mínimo:

- tema real;
- significado contextual;
- afinidad semántica aparente;
- campos de afinidad;
- intención aparente;
- resumen de la intención;
- evidencia textual;
- contradicciones;
- contexto faltante;
- riesgo de falso positivo;
- incertidumbre;
- razón para revisión humana.

Debe excluir:

- arquetipo probable;
- capacidad económica estimada;
- camino de participación;
- calificación comercial;
- autorización automática de contacto.

La evaluación siempre debe declarar:

```text
provisional = true
human_review_required = true
```

---

## 4. Afinidad e intención

### Afinidad semántica aparente

Compatibilidad provisional del sentido de la conversación con campos relevantes de Inlak’ech.

Puede clasificarse inicialmente como:

- `NINGUNA`;
- `POSIBLE`;
- `CLARA`.

### Intención aparente

Dirección de acción expresada o inferida con evidencia.

Puede distinguir:

- `NINGUNA`;
- `SIMPATIA_TEMATICA`;
- `EXPLORACION`;
- `ORIENTADA_A_ACCION`.

La intención aparente no confirma interés en Inlak’ech, porque la persona todavía puede no conocer el proyecto.

### Riesgo de falso positivo

- `BAJO`;
- `MEDIO`;
- `ALTO`.

### Evidencia

Toda interpretación debe conservar fragmentos textuales reales y explicar la relación entre la evidencia y la conclusión.

---

## 5. Prioridad de revisión humana

La prioridad sirve únicamente para ordenar la bandeja. No califica a la persona.

Puede derivarse de reglas transparentes aplicadas a:

- afinidad aparente;
- intención aparente;
- calidad de evidencia;
- actualidad;
- riesgo de falso positivo.

No puede incorporar:

- arquetipo inferido;
- capacidad económica estimada;
- profesión;
- ubicación social;
- apariencia;
- supuesta solvencia.

La explicación semántica siempre prevalece sobre un número agregado.

---

## 6. Bandeja de revisión humana

Cada ficha debe mostrar como mínimo:

- fuente, URL y fecha;
- texto y contexto;
- autor o identidad pública disponible;
- consulta de origen;
- tema real;
- afinidad e intención aparentes;
- fragmentos justificativos;
- contradicciones;
- información faltante;
- incertidumbre;
- riesgo de falso positivo;
- razón de revisión;
- propuesta editable de acercamiento.

Acciones humanas:

- `APROBAR_CONTACTO_DESCUBRIMIENTO`;
- `EDITAR_MENSAJE`;
- `POSPONER`;
- `OBSERVAR`;
- `DESCARTAR`;
- `NO_CONTACTAR`;
- `MARCAR_DUPLICADO`.

RADAR nunca envía mensajes automáticamente.

---

## 7. Acercamiento de descubrimiento

El acercamiento debe:

- partir del contexto real;
- reconocer la inquietud expresada;
- explicar brevemente una posible conexión con Inlak’ech;
- aportar valor;
- evitar urgencia, presión y venta agresiva;
- solicitar permiso para continuar;
- respetar las reglas de la plataforma.

```text
referencia genuina
→ reconocimiento del contexto
→ conexión breve con Inlak’ech
→ aporte útil
→ invitación voluntaria
```

El estado cambia a `DISCOVERY_CONTACTED` únicamente cuando existe evidencia del envío humano.

---

## 8. Embudo de descubrimiento

Después del contacto pueden registrarse:

- respuesta;
- inicio de diálogo;
- preguntas;
- intereses;
- motivaciones declaradas;
- objeciones;
- simpatía revelada;
- nivel de afinidad revelada;
- voluntad de continuar;
- consentimiento para precalificación.

El resultado debe ser registrado por un humano mediante un `DiscoveryOutcome` o equivalente.

Valores iniciales recomendados:

```text
sympathy_revealed:
NO | UNCLEAR | YES

revealed_affinity_level:
NONE | PARTIAL | CLEAR
```

El LLM puede resumir una respuesta, pero no decidir autónomamente si la afinidad quedó revelada.

---

## 9. Arquetipos

Arquetipos vigentes:

- `PIONERO_VISIONARIO`;
- `SEMBRADOR_PACIENTE`;
- `ARTIFICE_REGENERATIVO`.

Regla:

```text
conversación pública
→ no autoriza arquetipo

diálogo humano suficiente
→ permite hipótesis

confirmación humana
→ permite utilizarla
```

Toda hipótesis debe conservar:

- evidencia del diálogo;
- confianza;
- confirmación humana;
- responsable y fecha.

El arquetipo no equivale al perfil del mini-formulario ni al camino de participación.

---

## 10. Gate entre descubrimiento y conversión

La precalificación solo puede habilitarse cuando existen simultáneamente:

```text
respuesta humana verificable
+
afinidad revelada o interés suficiente
+
voluntad de continuar
+
consentimiento explícito
```

Transiciones prohibidas:

```text
DETECTED → QUALIFICATION_STARTED
DISCOVERY_CONTACTED → QUALIFIED
DISCOVERY_REPLIED → QUALIFICATION_STARTED sin gate humano
AFFINITY_NOT_CONFIRMED → PREQUALIFICATION_ACCEPTED
```

---

## 11. Precalificación

Dimensiones mínimas, todas declaradas o confirmadas:

- perfil identitario;
- camino de participación de interés;
- horizonte temporal;
- recursos o capital declarado;
- motivación;
- modalidad de participación;
- nivel de conocimiento;
- objeciones;
- consentimiento;
- pedido de siguiente paso.

Resultados:

- `NO_CALIFICADO`;
- `EN_MADURACION`;
- `CALIFICADO`;
- `PRIORITARIO`.

Toda decisión debe ser determinística cuando corresponda, explicable y revisable.

---

## 12. Límite entre RADAR y Relaticle

RADAR realiza:

- descubrimiento público;
- persistencia y deduplicación;
- interpretación semántica provisional;
- revisión humana;
- registro de contacto y respuesta;
- administración del descubrimiento;
- registro de afinidad revelada;
- consentimiento;
- precalificación;
- decisión de calificación.

Relaticle administra el seguimiento comercial una vez que existe una persona identificable, consentimiento suficiente y una decisión válida de transferencia.

No crear indiscriminadamente personas u oportunidades en Relaticle.

Crear oportunidad únicamente para leads calificados o por aprobación comercial explícita documentada.

---

## 13. Estados objetivo

```text
DETECTED
SEMANTIC_AFFINITY_DETECTED
HUMAN_REVIEW_PENDING
DISCOVERY_CANDIDATE
DISCOVERY_APPROACH_APPROVED
DISCOVERY_CONTACTED
DISCOVERY_REPLIED
DISCOVERY_DIALOGUE_ACTIVE
AFFINITY_REVEALED
AFFINITY_NOT_CONFIRMED
DISCOVERY_CLOSED
PREQUALIFICATION_INVITED
PREQUALIFICATION_ACCEPTED
QUALIFICATION_STARTED
NURTURING
QUALIFIED
PRIORITY_QUALIFIED
TRANSFERRED_TO_CRM
OPPORTUNITY_OPEN
DISCARDED
DO_NOT_CONTACT
```

Estos son estados objetivo. La documentación de estado de ingeniería debe distinguir cuáles están implementados y cuáles son gaps.

---

## 14. Flujo integral obligatorio

1. Ejecutar consultas autorizadas.
2. Encontrar una conversación real.
3. Normalizar, deduplicar y persistir.
4. Reconstruir tema y contexto.
5. Evaluar afinidad e intención aparentes.
6. Validar evidencia, contradicciones e incertidumbre.
7. Ordenar para revisión humana.
8. Aprobar, observar, posponer, descartar o no contactar.
9. Proponer un acercamiento editable.
10. Registrar el envío humano.
11. Registrar respuesta.
12. Abrir y administrar el diálogo de descubrimiento.
13. Registrar afinidad revelada o no confirmada.
14. Formular una hipótesis de arquetipo únicamente con diálogo suficiente y confirmación humana.
15. Obtener voluntad y consentimiento para continuar.
16. Invitar a precalificación.
17. Aplicar el cuestionario.
18. Evaluar datos declarados.
19. Clasificar el contacto.
20. Transferir únicamente cuando corresponda.
21. Continuar el seguimiento comercial en Relaticle.

---

## 15. Definición de terminado

RADAR no está terminado por buscar fuentes, encontrar conversaciones, asignar puntajes, sugerir mensajes o crear registros locales.

Debe existir evidencia reproducible de:

```text
conversación real
→ afinidad aparente explicada
→ revisión humana
→ contacto de descubrimiento
→ respuesta
→ diálogo humano
→ afinidad revelada o descartada
→ consentimiento
→ precalificación
→ lead calificado
→ transferencia controlada
```
