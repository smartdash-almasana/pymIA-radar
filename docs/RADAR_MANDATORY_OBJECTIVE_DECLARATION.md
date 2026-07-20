# DECLARACIÓN DE OBJETIVO OBLIGATORIA

## Estado y autoridad

**Producto:** RADAR — Motor de Afinidad Conversacional, Descubrimiento Humano y Precalificación
**Cliente único:** Inlak’ech
**Estado:** APROBADO COMO OBJETIVO DE PRODUCTO

Este documento está subordinado a la documentación maestra de Inlak’ech en sus dominios de filosofía, identidad, arquetipos, caminos de participación, cifras y embudo comercial. Para la arquitectura específica de RADAR, debe leerse junto con:

```text
docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md
```

Durante esta etapa RADAR no es un SaaS, no es multiempresa y no debe generalizarse para otros clientes.

---

## 1. Objetivo de RADAR

RADAR debe permitir que Inlak’ech encuentre conversaciones públicas cuyo sentido parezca afín al proyecto, identifique a las personas que participan en ellas, facilite un contacto humano de descubrimiento y, únicamente cuando la afinidad se revela y existe consentimiento para continuar, inicie la precalificación y entregue leads calificados al embudo comercial.

Definición obligatoria:

> Encontrar conversaciones públicas aparentemente afines a Inlak’ech, identificar a las personas que las expresan, facilitar un contacto humano de descubrimiento y, solo cuando la afinidad se revela y existe consentimiento para continuar, iniciar la precalificación y entregar los mejores candidatos al embudo comercial.

RADAR no debe limitarse a buscar menciones ni palabras clave. Debe reconstruir el sentido suficiente de la conversación para distinguir afinidad semántica aparente, intención aparente, ruido léxico, contradicciones e incertidumbre.

---

## 2. Recorrido integral obligatorio

```text
conversación pública
→ afinidad semántica aparente
→ persona potencialmente relevante
→ revisión humana
→ candidato de descubrimiento
→ acercamiento aprobado
→ contacto humano
→ diálogo de descubrimiento
→ afinidad revelada, ambigua o descartada
→ posible hipótesis de arquetipo basada en diálogo humano
→ consentimiento o rechazo para continuar
→ precalificación
→ lead calificado
→ transferencia controlada al embudo comercial
```

La búsqueda, el scraping permitido, el LLM, los puntajes y el CRM son piezas auxiliares. Ninguna constituye por sí sola el producto.

---

## 3. Dos embudos distintos

### 3.1. Embudo de descubrimiento

Su finalidad es revelar si la afinidad aparente detectada en una conversación pública se sostiene cuando la persona conoce Inlak’ech mediante un vínculo humano legítimo.

No busca vender, inducir inversión, forzar una reunión ni obtener datos económicos de manera encubierta.

```text
afinidad semántica aparente
→ revisión humana
→ contacto de descubrimiento
→ conocimiento inicial de Inlak’ech
→ diálogo
→ afinidad revelada o no confirmada
→ motivaciones y objeciones conocidas
→ voluntad o rechazo de continuar
```

### 3.2. Embudo de conversión

Solo comienza cuando existen conjuntamente:

```text
afinidad revelada o interés suficiente
+
voluntad de continuar
+
consentimiento explícito
```

Entonces puede iniciarse:

```text
invitación a precalificación
→ aceptación
→ cuestionario
→ respuestas declaradas
→ cualificación
→ camino de participación
→ lead calificado
→ embudo comercial
```

---

## 4. Objetos de dominio obligatorios

- **Conversación detectada:** hallazgo público persistido sin evaluación semántica válida.
- **Conversación aparentemente afín:** conversación cuyo sentido presenta una relación plausible con Inlak’ech. Sigue siendo provisional.
- **Persona potencialmente relevante:** identidad pública vinculada a una conversación aparentemente afín.
- **Candidato de descubrimiento:** persona aprobada humanamente para considerar un acercamiento.
- **Participante del descubrimiento:** persona efectivamente contactada que está conociendo Inlak’ech.
- **Persona con afinidad revelada:** persona que expresó durante el diálogo humano una simpatía, identificación, curiosidad o interés explicable.
- **Persona invitada a precalificación:** persona que aceptó evaluar una continuidad y aportar información.
- **Lead precalificado:** persona que respondió información suficiente y obtuvo una cualificación revisable.
- **Lead transferido:** lead calificado enviado de manera controlada al CRM o embudo autorizado.

Está prohibido llamar `lead` a toda conversación o persona encontrada.

---

## 5. Definición de afinidad

La afinidad no se define por una palabra aislada. Se reconoce provisionalmente por la relación contextual entre lo dicho y campos relevantes para Inlak’ech, entre ellos:

- inversión consciente;
- legado;
- comunidad;
- regeneración;
- territorio;
- belleza útil;
- paciencia estratégica;
- construcción con propósito;
- pertenencia;
- largo plazo;
- hospitalidad sustentable;
- desarrollo no especulativo;
- impacto;
- participación activa;
- respeto cultural;
- conexión con México o Yucatán.

Señales de incompatibilidad o cautela:

- especulación inmediata;
- retorno rápido como único criterio;
- turismo superficial sin vínculo con el proyecto;
- espiritualidad comercial vacía;
- promoción oportunista;
- rechazo explícito del largo plazo;
- coincidencia léxica sin contexto compatible.

Estos campos orientan la interpretación del sentido. No deben implementarse como una lista rígida de palabras.

---

## 6. Diferencias obligatorias

RADAR debe mantener separadas estas dimensiones:

- **Afinidad semántica aparente:** interpretación provisional de una conversación pública.
- **Intención aparente:** dirección de acción expresada o inferida con evidencia en esa conversación.
- **Afinidad revelada:** reacción que la persona manifiesta al conocer Inlak’ech durante el contacto humano.
- **Capacidad declarada:** información aportada voluntariamente durante la precalificación.
- **Calificación:** resultado derivado de respuestas suficientes, reglas transparentes y revisión humana.

Nunca debe asumirse:

```text
afinidad aparente = afinidad revelada
afinidad revelada = intención comercial
intención = capacidad
capacidad = lead calificado
```

---

## 7. Arquetipos

Arquetipos de Inlak’ech:

- `PIONERO_VISIONARIO`;
- `SEMBRADOR_PACIENTE`;
- `ARTIFICE_REGENERATIVO`.

Regla obligatoria:

```text
publicación pública
→ puede aportar señales semánticas
→ no autoriza clasificación de arquetipo

diálogo humano suficiente
→ permite formular una hipótesis

confirmación humana
→ permite utilizarla para adaptar el recorrido
```

El arquetipo no es diagnóstico psicológico, no equivale al perfil declarado y no determina automáticamente el camino de participación ni la calificación.

---

## 8. Responsabilidades

### El LLM puede

- reconstruir tema y contexto;
- detectar afinidad e intención aparentes;
- citar evidencia;
- señalar contradicciones e incertidumbre;
- sugerir un acercamiento editable;
- resumir información surgida de un diálogo humano.

### El LLM no puede

- confirmar afinidad personal;
- inferir capacidad económica;
- asignar definitivamente un arquetipo;
- autorizar o ejecutar contacto;
- inferir consentimiento;
- convertir a una persona en lead;
- transferirla al CRM.

### RADAR puede

- buscar, normalizar y deduplicar;
- validar contratos y evidencia;
- ordenar la revisión;
- sugerir acercamientos;
- registrar decisiones, contactos y respuestas;
- administrar estados de descubrimiento;
- administrar la precalificación;
- aplicar reglas determinísticas a datos declarados;
- transferir únicamente cuando el gate lo permita.

### El humano debe

- revisar evidencia;
- decidir si contactar;
- realizar el contacto;
- conducir el diálogo de descubrimiento;
- registrar si la afinidad se reveló;
- comprender motivaciones y objeciones;
- validar cualquier hipótesis de arquetipo;
- obtener consentimiento;
- revisar la cualificación.

Principio rector:

```text
el LLM interpreta
→ RADAR controla y registra
→ el humano decide y se vincula
```

---

## 9. Resultado operativo esperado

La bandeja inicial debe presentar conversaciones, no supuestos inversores. Cada ficha debe mostrar como mínimo:

- conversación original;
- fuente, enlace y fecha;
- autor o identidad pública disponible;
- consulta de origen;
- tema real y contexto;
- afinidad e intención aparentes;
- evidencia textual;
- contradicciones e información faltante;
- incertidumbre y riesgo de falso positivo;
- razón para revisión;
- sugerencia editable de acercamiento.

No debe mostrar como resultado de la lectura pública:

- arquetipo asignado;
- capacidad económica estimada;
- camino de participación;
- calificación comercial.

---

## 10. Precalificación

Solo comienza después de una respuesta humana verificable, interés suficiente, voluntad de continuar y consentimiento explícito.

En esa etapa sí pueden registrarse datos declarados sobre:

- perfil identitario;
- camino de interés;
- recursos o rango de capital;
- horizonte temporal;
- motivación;
- modalidad de participación;
- objeciones;
- documentación requerida;
- pedido de siguiente paso.

Resultados posibles:

- `NO_CALIFICADO`;
- `EN_MADURACION`;
- `CALIFICADO`;
- `PRIORITARIO`.

Toda decisión debe ser explicable y revisable.

---

## 11. Qué no es RADAR

RADAR no es:

- CRM propio;
- chatbot institucional;
- RAG general;
- sistema de branding;
- plataforma documental;
- herramienta multiempresa;
- sistema de venta automática;
- motor de contacto automático;
- scoring psicológico;
- inferencia financiera desde perfiles públicos;
- plataforma de reserva, firma o pagos;
- portal del fundador.

---

## 12. Criterio de éxito

RADAR será útil cuando demuestre con casos reales que puede:

1. encontrar conversaciones que el equipo no habría detectado;
2. reducir ruido y falsos positivos;
3. explicar por qué una conversación parece afín;
4. permitir una decisión humana informada;
5. facilitar un contacto respetuoso;
6. registrar un diálogo de descubrimiento;
7. distinguir afinidad revelada de ausencia de afinidad;
8. bloquear la precalificación sin consentimiento;
9. precalificar con datos declarados;
10. transferir únicamente leads calificados.

---

## 13. Definición de terminado

RADAR no estará terminado por tener una API, una pantalla, un clasificador, una integración con Agnes, resultados sintéticos o una conexión teórica con Relaticle.

Estará terminado cuando exista evidencia reproducible del siguiente recorrido real:

```text
consulta real
→ conversación pública real
→ afinidad semántica aparente explicada
→ revisión humana
→ candidato de descubrimiento
→ acercamiento humano real
→ respuesta real
→ diálogo de descubrimiento
→ afinidad revelada o descartada
→ consentimiento para continuar
→ precalificación real
→ lead calificado
→ ingreso controlado al embudo comercial
```

---

## 14. Mandato operativo

Toda decisión de producto, arquitectura, interfaz, modelo de datos y prioridad de desarrollo debe demostrar cómo contribuye al recorrido:

> De la conversación pública a la persona; de la persona al descubrimiento humano; del descubrimiento consentido a la precalificación; y de la precalificación al embudo comercial de Inlak’ech.
