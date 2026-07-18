# RADAR — Contrato obligatorio de conversión comercial

## Autoridad

Este documento define el funcionamiento integral de RADAR para el único cliente actual: **Inlak'ech**.

RADAR no termina cuando encuentra una conversación. Acompaña el recorrido desde la conversación pública detectada hasta el lead calificado y su transferencia controlada a Relaticle.

```text
DESCUBRIMIENTO
→ EVALUACIÓN
→ REVISIÓN Y ACERCAMIENTO
→ RESPUESTA
→ PRECALIFICACIÓN
→ LEAD CALIFICADO
→ TRANSFERENCIA A RELATICLE
```

La cartografía de fuentes, las consultas y los conectores son entradas del producto. No constituyen por sí mismos el producto completo.

## 1. Definiciones comerciales obligatorias

- **Conversación detectada:** hallazgo persistido sin decisión humana.
- **Candidato:** conversación que RADAR selecciona para revisión.
- **Candidato aprobado:** una persona responsable decide que merece acercamiento.
- **Contactado:** existe evidencia de que el acercamiento fue realizado.
- **Interesado:** respondió positivamente o pidió más información.
- **Precalificado:** completó la información mínima requerida.
- **Lead calificado:** cumple condiciones explícitas para ingresar al embudo comercial.
- **Oportunidad:** el equipo comercial confirmó una posibilidad concreta y abrió seguimiento en Relaticle.

Está prohibido llamar `lead` a toda persona o conversación encontrada.

## 2. Dimensiones de evaluación separadas

RADAR no debe producir un único puntaje opaco.

### Afinidad temática

Compatibilidad de la conversación con los universos de Inlak'ech. Escala `0–100`.

### Afinidad de valores

Compatibilidad verificable con regeneración, comunidad, legado, largo plazo, pertenencia, honestidad, territorio, participación y rechazo de la especulación inmediata. Escala `0–100`.

### Intención

Señales de que la persona considera una acción: pedir recomendaciones, comparar, participar, invertir, mudarse, consultar costos, solicitar contacto o declarar un plazo. Escala `0–100`.

### Capacidad declarada

Solo se registra con evidencia explícita. Valores:

- `NO_CONOCIDA`
- `BAJA_DECLARADA`
- `MEDIA_DECLARADA`
- `ALTA_DECLARADA`

Nunca inferir capacidad por profesión, apariencia, ubicación o perfil social.

### Momento de decisión

- `DESCUBRIMIENTO`
- `EXPLORACIÓN`
- `COMPARACIÓN`
- `EVALUACIÓN_ACTIVA`
- `LISTO_PARA_CONVERSAR`
- `LISTO_PARA_PRECALIFICAR`

### Calidad de evidencia

Escala `0–100`, basada en extensión, claridad, contexto, continuidad, respuestas del autor, preguntas, objeciones y actualidad.

### Riesgo de falso positivo

- `BAJO`
- `MEDIO`
- `ALTO`

## 3. Prioridad para revisión humana

La prioridad ordena la bandeja; no califica al contacto.

```text
prioridad_revision =
  25% afinidad temática
+ 25% afinidad de valores
+ 30% intención
+ 20% calidad de evidencia
- penalización por riesgo
```

Categorías iniciales:

- `80–100`: `REVISAR_PARA_ACERCAMIENTO`
- `60–79`: `REVISAR_O_MADURAR`
- `40–59`: `OBSERVAR`
- `0–39`: `DESCARTAR`

La penalización por riesgo deberá quedar explícita y testeada antes de implementar el clasificador productivo.

## 4. Arquetipos tentativos

RADAR puede proponer, nunca diagnosticar:

- `PIONERO_VISIONARIO`
- `SEMBRADOR_PACIENTE`
- `ARTIFICE_REGENERATIVO`

Toda propuesta debe incluir confianza y fragmentos de evidencia.

## 5. Bandeja de revisión humana

Cada ficha debe mostrar como mínimo:

- fuente, URL, fecha, texto y contexto;
- autor o identidad pública disponible;
- consulta de origen;
- afinidad temática y de valores;
- intención;
- calidad de evidencia;
- riesgo de falso positivo;
- arquetipo tentativo;
- fragmentos justificativos;
- objeciones e información faltante;
- acción recomendada;
- propuesta editable de acercamiento.

Acciones humanas:

- `APROBAR_ACERCAMIENTO`
- `EDITAR_MENSAJE`
- `POSPONER`
- `OBSERVAR`
- `DESCARTAR`
- `MARCAR_DUPLICADO`
- `REGISTRAR_RESPUESTA`

RADAR nunca envía mensajes automáticamente.

## 6. Acercamiento

Debe partir del contexto real, aportar valor, evitar urgencia y venta agresiva, pedir permiso para continuar y respetar las reglas de la plataforma.

```text
referencia genuina
→ reconocimiento de la inquietud
→ conexión breve con Inlak'ech
→ aporte útil
→ invitación voluntaria
```

El estado solo cambia a `CONTACTED` cuando existe evidencia del envío.

## 7. Precalificación

Solo comienza después de una respuesta positiva.

Dimensiones mínimas:

- motivación;
- camino de participación real de Inlak'ech;
- horizonte temporal;
- recursos declarados;
- nivel de conocimiento;
- objeciones;
- consentimiento explícito.

No inventar caminos de participación ni rangos económicos. Deben provenir de documentación comercial aprobada por Inlak'ech.

Resultados:

- `NO_CALIFICADO`
- `EN_MADURACION`
- `CALIFICADO`
- `PRIORITARIO`

Toda decisión debe ser explicable y revisable.

## 8. Límite entre RADAR y Relaticle

RADAR realiza:

- descubrimiento;
- persistencia y deduplicación;
- evaluación;
- revisión;
- registro del acercamiento y respuesta;
- precalificación;
- decisión de calificación.

Relaticle administra el seguimiento comercial una vez que existe una persona identificable y una vía legítima de contacto, especialmente desde la transferencia de un lead calificado.

No crear indiscriminadamente personas en Relaticle. Crear o actualizar registro cuando:

1. el acercamiento fue aprobado y existe identidad o contacto utilizable;
2. la persona respondió;
3. comenzó la precalificación;
4. el equipo decidió incorporarla al seguimiento.

Crear oportunidad únicamente para leads calificados o por aprobación comercial explícita.

## 9. Estados del ciclo

- `DETECTED`
- `REVIEW_PENDING`
- `OBSERVING`
- `APPROACH_APPROVED`
- `CONTACTED`
- `REPLIED`
- `QUALIFICATION_STARTED`
- `NURTURING`
- `QUALIFIED`
- `PRIORITY_QUALIFIED`
- `TRANSFERRED_TO_CRM`
- `OPPORTUNITY_OPEN`
- `DISCARDED`
- `DO_NOT_CONTACT`

Responsabilidad principal de RADAR: hasta `QUALIFIED` o `PRIORITY_QUALIFIED`.

Responsabilidad principal de Relaticle: desde `TRANSFERRED_TO_CRM` y `OPPORTUNITY_OPEN`.

## 10. Flujo integral obligatorio

1. Ejecutar consultas.
2. Encontrar una conversación real.
3. Normalizar, deduplicar y guardar.
4. Evaluar afinidad temática.
5. Evaluar afinidad de valores.
6. Estimar intención.
7. Evaluar calidad de evidencia y riesgo.
8. Calcular prioridad de revisión.
9. Proponer arquetipo tentativo.
10. Someter a revisión humana.
11. Aprobar, observar, posponer o descartar.
12. Proponer acercamiento editable.
13. Registrar envío humano.
14. Registrar respuesta.
15. Iniciar precalificación únicamente con interés.
16. Evaluar motivación, camino, plazo, recursos y consentimiento.
17. Clasificar el contacto.
18. Transferir a Relaticle cuando corresponda.
19. Crear persona, oportunidad, nota y tarea según reglas.
20. Continuar el seguimiento comercial en Relaticle.

## 11. Definición de terminado

RADAR no está terminado por buscar fuentes, encontrar conversaciones, asignar puntajes o crear contactos en el CRM.

Debe existir evidencia reproducible de:

```text
conversación real
→ candidato evaluado
→ revisión humana
→ acercamiento
→ respuesta
→ precalificación
→ lead calificado
→ oportunidad en Relaticle
```
