# RADAR — Arquitectura maestra y dirección de desarrollo

**Cliente único:** Inlak’ech
**Estado:** BORRADOR RECTOR PARA RECONCILIACIÓN DOCUMENTAL
**Fecha:** 19 de julio de 2026
**Repositorio:** `inlakech-radar`
**Decisión estructural:** no crear un repositorio nuevo

---

## 1. Propósito

Este documento fija la arquitectura funcional, semántica, humana y técnica de RADAR a partir de la demanda original del cliente y de las precisiones surgidas durante su revisión.

Su objetivo es impedir dos derivas:

1. reducir RADAR a un buscador o scraper;
2. convertir RADAR en una plataforma semántica general, sobredimensionada y separada de la necesidad comercial concreta de Inlak’ech.

RADAR debe hacer lo que pide el cliente, ni más ni menos:

> Encontrar conversaciones públicas aparentemente afines a Inlak’ech, identificar a las personas que las expresan, facilitar un contacto humano de descubrimiento y, solo cuando la afinidad se revela y existe consentimiento para continuar, iniciar la precalificación y entregar los mejores candidatos al embudo comercial.

Este documento no autoriza por sí solo cambios de código. Primero debe reconciliarse con los documentos vigentes que todavía contienen reglas anteriores incompatibles.

---

## 2. Demanda original del cliente

El cliente no pidió un scraper aislado. Pidió un sistema de prospección conversacional, descubrimiento humano y precalificación conectado con su embudo comercial.

La demanda completa es:

```text
Redes y conversaciones públicas
        ↓
Detección de conversaciones aparentemente afines
        ↓
Identificación de la persona vinculada
        ↓
Análisis de contexto e intención aparente
        ↓
Sugerencia de acercamiento
        ↓
Revisión humana
        ↓
Contacto humano
        ↓
Embudo de descubrimiento
        ↓
Afinidad revelada o descartada
        ↓
Consentimiento para continuar
        ↓
Cuestionario de precalificación
        ↓
Lead calificado
        ↓
Embudo comercial principal
        ↓
Reserva
        ↓
Firma y pago
        ↓
Seguimiento como fundador
```

El scraping, la búsqueda, el uso de un LLM y la integración con un CRM son piezas auxiliares. Ninguna de ellas constituye por sí sola el producto.

---

## 3. Corrección central de arquitectura

La arquitectura anterior comprimía excesivamente el tramo existente entre la respuesta al primer contacto y la precalificación.

Antes:

```text
candidato
→ contacto
→ respuesta
→ precalificación
```

Arquitectura corregida:

```text
conversación aparentemente afín
→ persona potencialmente relevante
→ revisión humana
→ contacto humano
→ diálogo de descubrimiento
→ afinidad revelada o descartada
→ posible arquetipo basado en diálogo humano
→ consentimiento para continuar
→ precalificación
```

La nueva pieza explícita es el **embudo de descubrimiento**.

Su función no es convertir, inducir una acción ni calificar económicamente. Su función es permitir que la persona conozca Inlak’ech y revele libremente si existe simpatía, identificación, curiosidad o afinidad real con el proyecto.

---

## 4. Dos embudos distintos

### 4.1. Embudo de descubrimiento

Finalidad:

> Revelar si la afinidad aparente detectada en una conversación pública se sostiene cuando una persona conoce Inlak’ech mediante un contacto humano legítimo.

```text
afinidad semántica aparente
→ persona potencialmente relevante
→ revisión humana
→ acercamiento aprobado
→ contacto humano
→ conocimiento inicial de Inlak’ech
→ diálogo de descubrimiento
→ afinidad revelada, ambigua o descartada
→ motivaciones y objeciones conocidas
→ posible hipótesis de arquetipo
→ consentimiento o rechazo para continuar
```

En este embudo no se debe:

- vender;
- presionar;
- forzar una reunión;
- inferir capacidad económica;
- asignar un arquetipo por una publicación;
- convertir automáticamente a la persona en lead;
- trasladar datos al CRM sin fundamento y consentimiento.

### 4.2. Embudo de conversión

Comienza únicamente cuando se cumplen simultáneamente:

```text
afinidad revelada
+
interés en continuar
+
consentimiento explícito
```

```text
invitación a precalificación
→ aceptación
→ cuestionario
→ respuestas declaradas
→ cualificación
→ camino de participación
→ lead calificado
→ transferencia al embudo comercial
```

La frontera entre ambos embudos es un gate ético y funcional obligatorio.

---

## 5. Unidad inicial y progresión de objetos

La unidad inicial de RADAR es la conversación. La persona aparece después, cuando existe evidencia suficiente y una identidad pública utilizable.

### 5.1. Conversación detectada

Hallazgo público persistido, todavía sin evaluación semántica válida.

### 5.2. Conversación aparentemente afín

Conversación cuyo tema, contexto, valores expresados o intención aparente presentan una relación plausible con Inlak’ech.

No es un lead. No confirma afinidad personal.

### 5.3. Persona potencialmente relevante

Identidad pública vinculada a una conversación aparentemente afín.

No es todavía candidato aprobado, participante del descubrimiento ni lead.

### 5.4. Candidato de descubrimiento

Persona cuya conversación fue revisada por un humano y respecto de la cual se aprobó considerar un acercamiento.

### 5.5. Participante del descubrimiento

Persona efectivamente contactada que está conociendo Inlak’ech.

### 5.6. Persona con afinidad revelada

Persona que, durante el diálogo humano, expresó simpatía, identificación, curiosidad o interés real y explicable.

### 5.7. Persona invitada a precalificación

Persona con afinidad revelada a quien se le ofrece continuar y aportar información para evaluar un camino posible.

### 5.8. Lead precalificado

Persona que aceptó continuar, respondió información suficiente y obtuvo un resultado de cualificación revisable.

### 5.9. Lead transferido

Lead calificado enviado de manera controlada al embudo comercial o CRM autorizado.

---

## 6. Tres niveles de afinidad

### 6.1. Afinidad semántica aparente

Se obtiene de una conversación pública.

Significa:

> El sentido de lo dicho parece pertenecer al universo de valores, preocupaciones, deseos o posibilidades de Inlak’ech.

Puede ser evaluada por el LLM y validada por reglas, pero siempre permanece provisional.

### 6.2. Afinidad revelada

Surge en el contacto humano, cuando la persona conoce el proyecto y expresa una reacción propia.

Puede ser:

- no revelada;
- ambigua;
- parcial;
- clara.

La registra el humano. El LLM puede resumir evidencia, pero no decidirla autónomamente.

### 6.3. Afinidad confirmada para continuar

Existe cuando la persona puede expresar qué le interesa, por qué le importa y manifiesta voluntad de continuar.

No equivale todavía a capacidad ni a lead calificado.

---

## 7. Campos semánticos de afinidad con Inlak’ech

La documentación del cliente sirve para definir mejor la afinidad, no para alterar el objetivo del producto.

Campos positivos iniciales:

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
- presión comercial;
- turismo superficial sin relación con el proyecto;
- espiritualidad comercial vacía;
- promoción oportunista;
- rechazo explícito del largo plazo;
- afinidad meramente léxica sin contexto compatible.

Estos campos no deben implementarse como una lista rígida de palabras. Son referencias para interpretar sentido, contexto e intención aparente.

---

## 8. Las cinco preguntas obligatorias de RADAR

Toda capacidad del producto debe ayudar a responder una de estas preguntas:

1. **¿Esta conversación es aparentemente relevante para Inlak’ech?**
2. **¿Qué tipo de afinidad semántica aparece y qué evidencia la sostiene?**
3. **¿Existe intención aparente o solamente simpatía temática?**
4. **¿Cómo puede un humano acercarse sin forzar, manipular ni vender prematuramente?**
5. **Después del descubrimiento humano, existe consentimiento y fundamento para pasar a precalificación?**

Una función que no contribuya a estas preguntas o al registro trazable del recorrido queda fuera de alcance.

---

## 9. Responsabilidades separadas

### 9.1. Responsabilidad del software

RADAR puede:

- ejecutar consultas autorizadas;
- recuperar conversaciones públicas;
- conservar fuente, URL, fecha, autor, texto y contexto;
- normalizar y deduplicar;
- solicitar una interpretación semántica estructurada;
- validar contratos, evidencia y estados;
- ordenar la bandeja humana;
- sugerir un acercamiento editable;
- registrar decisiones, contactos y respuestas;
- administrar el embudo de descubrimiento;
- administrar cuestionarios de precalificación;
- aplicar reglas determinísticas a respuestas declaradas;
- transferir leads únicamente cuando el gate lo permita;
- mantener trazabilidad completa.

### 9.2. Responsabilidad del LLM

El LLM puede:

- reconstruir el tema real;
- resumir el contexto;
- detectar afinidad semántica aparente;
- distinguir simpatía temática de intención aparente;
- citar evidencia textual;
- señalar contradicciones e incertidumbres;
- sugerir un mensaje de acercamiento;
- resumir respuestas humanas;
- asistir en una hipótesis posterior de arquetipo cuando exista diálogo humano suficiente.

El LLM no puede:

- confirmar afinidad personal;
- inferir capacidad económica;
- declarar disponibilidad no expresada;
- clasificar definitivamente un arquetipo desde una publicación pública;
- autorizar un contacto;
- enviar mensajes;
- obtener consentimiento por inferencia;
- convertir a una persona en lead;
- transferirla al CRM por sí solo.

### 9.3. Responsabilidad humana

El humano debe:

- revisar evidencia y contexto;
- aprobar, editar, posponer o descartar;
- realizar el contacto;
- conducir el diálogo de descubrimiento;
- registrar si la afinidad se reveló o no;
- comprender motivaciones y objeciones;
- validar cualquier hipótesis de arquetipo;
- ofrecer la continuidad;
- obtener consentimiento explícito;
- revisar la cualificación y el camino recomendado.

Principio rector:

```text
el LLM interpreta
→ RADAR controla y registra
→ el humano decide y se vincula
```

---

## 10. Contrato semántico objetivo

La primera evaluación debe centrarse en la conversación, no en diagnosticar a la persona.

Salida mínima propuesta para una futura versión del contrato:

```json
{
  "real_topic": "...",
  "contextual_meaning": "...",
  "apparent_affinity": "NONE | POSSIBLE | CLEAR",
  "affinity_domains": ["community", "territory"],
  "apparent_intention": "NONE | THEMATIC_SYMPATHY | EXPLORATION | ACTION_ORIENTED",
  "intention_summary": "...",
  "evidence_fragments": ["..."],
  "contradictions": ["..."],
  "missing_context": ["..."],
  "false_positive_risk": "LOW | MEDIUM | HIGH",
  "uncertainty": "LOW | MEDIUM | HIGH",
  "human_review_reason": "...",
  "provisional": true,
  "human_review_required": true
}
```

Debe excluir en esta etapa:

- arquetipo probable;
- capacidad económica;
- calificación;
- camino de participación;
- lead score;
- decisión de contacto automática.

La prioridad de revisión puede calcularse después, mediante reglas transparentes, pero no debe sustituir la explicación semántica.

---

## 11. Embudo de descubrimiento como dominio explícito

El repositorio necesita representar el descubrimiento sin crear otra aplicación.

### 11.1. Estados mínimos propuestos

```text
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
```

No todos los estados requieren una tabla independiente. Deben modelarse mediante eventos y transiciones válidas, evitando duplicar fuentes de verdad.

### 11.2. Resultado humano del descubrimiento

Debe existir un registro equivalente a `DiscoveryOutcome` con información mínima:

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

Valores iniciales recomendados:

```text
sympathy_revealed:
NO | UNCLEAR | YES

revealed_affinity_level:
NONE | PARTIAL | CLEAR
```

Este resultado debe provenir del diálogo humano. El LLM solo puede ayudar a resumir o estructurar información que el humano confirma.

---

## 12. Arquetipos

Arquetipos vigentes:

- `PIONERO_VISIONARIO`;
- `SEMBRADOR_PACIENTE`;
- `ARTIFICE_REGENERATIVO`.

Regla obligatoria corregida:

```text
publicación pública
→ puede aportar señales semánticas
→ no autoriza clasificación de arquetipo

contacto humano y diálogo suficiente
→ permiten hipótesis de arquetipo

confirmación humana
→ permite usar el arquetipo para adaptar el recorrido
```

El arquetipo:

- no es diagnóstico psicológico;
- no equivale a camino de participación;
- no equivale al perfil declarado en el mini-formulario;
- no determina automáticamente la calificación;
- sirve para adaptar el lenguaje, la profundidad, los contenidos y el ritmo.

Registro recomendado:

```text
archetype_hypothesis
archetype_evidence
archetype_confidence
human_confirmed
confirmed_by
confirmed_at
```

---

## 13. Acercamiento asistido

RADAR puede sugerir un mensaje, pero nunca enviarlo automáticamente.

El mensaje debe:

- partir del enunciado real;
- reconocer la inquietud expresada;
- explicar brevemente por qué podría existir una conexión;
- aportar valor antes de pedir algo;
- presentar Inlak’ech sin exageración;
- solicitar permiso para continuar;
- respetar reglas y cultura de la plataforma.

Secuencia recomendada:

```text
referencia genuina
→ reconocimiento del contexto
→ conexión breve con Inlak’ech
→ aporte útil
→ invitación voluntaria a conocer más
```

El objetivo del primer acercamiento es abrir un diálogo de descubrimiento, no ejecutar una venta.

---

## 14. Frontera con la precalificación

La precalificación solo puede comenzar cuando existen:

```text
respuesta humana verificable
+
afinidad revelada o interés suficiente
+
voluntad de continuar
+
consentimiento explícito
```

Solo en ese punto pueden solicitarse o registrarse:

- perfil identitario declarado;
- camino de interés declarado;
- rango de capital declarado;
- horizonte temporal;
- motivación;
- modalidad de participación;
- objeciones;
- documentación requerida;
- pedido de siguiente paso.

La lógica determinística ya existente puede reutilizarse, siempre que el gate de descubrimiento impida su uso prematuro.

---

## 15. Arquitectura técnica dentro del repositorio actual

No se crea otro repositorio.

### 15.1. Componentes que se conservan

- FastAPI;
- SQLAlchemy;
- base de datos local y futura PostgreSQL;
- adaptador de `last30days`;
- normalización y deduplicación;
- modelo `Conversation`;
- integración Agnes/OpenAI-compatible;
- validación Pydantic;
- revisión humana;
- `EngagementEvent`;
- precalificación determinística;
- frontera con Relaticle;
- interfaz web existente;
- pruebas y disciplina spec-driven.

### 15.2. Componentes que deben evolucionar

#### `SemanticAssessmentV2`

Debe evolucionar de una evaluación prematura de persona y arquetipo hacia una evaluación de conversación centrada en sentido, afinidad aparente e intención aparente.

La evolución debe ser versionada. No se debe mutar silenciosamente la semántica histórica de registros persistidos.

#### `RadarCommercialState`

Actualmente salta de `REPLIED` a `QUALIFICATION_STARTED`.

Debe incorporar o representar explícitamente:

- diálogo de descubrimiento;
- afinidad revelada;
- afinidad no confirmada;
- invitación a precalificación;
- aceptación de precalificación.

#### `ReviewDecision`

Debe quedar semánticamente orientado a aprobar un **contacto de descubrimiento**, no un acercamiento comercial ya calificatorio.

#### `EngagementEvent`

Puede conservarse para registrar contacto y respuesta. Debe permitir enlazar los eventos posteriores del diálogo de descubrimiento sin transformarse en un transcript obligatorio de toda interacción.

#### Interfaz

Debe separar progresivamente:

1. conversaciones para revisar;
2. casos en descubrimiento;
3. personas habilitadas para precalificación;
4. leads calificados y transferencia.

### 15.3. Componentes nuevos mínimos

Se recomienda agregar solamente:

- contrato semántico centrado en conversación;
- representación de `DiscoveryCase` o equivalente;
- representación de `DiscoveryOutcome`;
- estados y gates del embudo de descubrimiento;
- registro de arquetipo posterior a diálogo humano;
- gate explícito hacia precalificación.

No se justifica agregar:

- otro backend;
- otro frontend;
- microservicios;
- Redis;
- Celery;
- base vectorial;
- un orquestador externo;
- BERTopic;
- SetFit;
- Argilla;
- Haystack;
- otro CRM;
- otro repositorio.

---

## 16. Mapeo del repositorio actual

| Capacidad | Ubicación actual | Dirección |
|---|---|---|
| Recuperación pública | `app/discovery/` | Conservar y sanear admisión |
| Normalización y deduplicación | `app/discovery/` y `Conversation` | Conservar |
| Evaluación semántica | `app/semantics/`, `app/schemas/assessment.py` | Versionar y centrar en conversación |
| Persistencia semántica | `SemanticAssessmentV2` | Crear evolución compatible |
| Revisión humana | `ReviewDecision`, API y bandeja | Reinterpretar como revisión para descubrimiento |
| Contacto y respuesta | `EngagementEvent` | Conservar y extender por eventos |
| Estados | `RadarCommercialState` | Insertar frontera de descubrimiento |
| Precalificación | `app/qualification.py`, SPEC-005 | Conservar detrás del nuevo gate |
| CRM | `crm_transfer.py`, integración Relaticle | Mantener bloqueado hasta auditoría |
| UI | templates y estáticos actuales | Divulgación progresiva por etapa |

---

## 17. Reconciliación documental obligatoria

Los siguientes documentos contienen reglas que deben revisarse antes de implementar:

- `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- `docs/specs/002_affinity_classification.md`;
- `docs/specs/003_human_review.md`;
- `docs/specs/005_qualification.md`;
- `docs/ARCHITECTURE.md`;
- `AGENTS.md`;
- matrices de aceptación y estado de ingeniería.

Conflictos concretos a resolver:

1. arquetipo probable antes del contacto humano;
2. candidato definido a veces como conversación y a veces como persona;
3. ausencia del participante de descubrimiento;
4. salto directo de respuesta a precalificación;
5. lenguaje de conversión aplicado antes de revelar afinidad;
6. evaluación semántica excesivamente centrada en puntajes;
7. capacidad declarada presente en el contrato público aunque normalmente aún no existe en esa etapa.

La reconciliación debe conservar trazabilidad y marcar expresamente qué reglas quedan sustituidas.

---

## 18. Dirección de implementación

### Fase 0 — Contrato y precedencia

- aprobar este documento;
- reconciliar documentos rectores;
- actualizar `AGENTS.md`;
- definir precedencia;
- congelar cualquier implementación incompatible.

### Fase 1 — Evaluación de conversación

- diseñar versión nueva del contrato semántico;
- eliminar arquetipo y capacidad de la evaluación pública;
- validar evidencia literal;
- documentar positivos, negativos y ambiguos;
- probar el caso de fútbol como control negativo.

### Fase 2 — Dominio de descubrimiento

- crear estados válidos;
- agregar `DiscoveryCase` o equivalente;
- agregar `DiscoveryOutcome`;
- preservar historial y trazabilidad;
- definir migración sin destruir datos previos.

### Fase 3 — Bandeja humana

- separar conversaciones de casos en descubrimiento;
- mostrar sentido, contexto, evidencia e incertidumbre;
- aprobar contacto de descubrimiento;
- registrar contacto, respuesta y resultado humano.

### Fase 4 — Arquetipos posteriores al diálogo

- permitir hipótesis solo con evidencia del contacto humano;
- exigir confirmación humana;
- distinguir arquetipo, perfil declarado y camino.

### Fase 5 — Gate a precalificación

- exigir afinidad revelada, voluntad y consentimiento;
- reutilizar SPEC-005;
- bloquear toda ejecución prematura;
- probar transiciones inválidas.

### Fase 6 — Integración y piloto

- auditar Relaticle;
- transferir únicamente leads permitidos;
- ejecutar piloto real extremo a extremo;
- documentar fallos, decisiones y aprendizaje.

---

## 19. Uso de agentes de desarrollo

RADAR puede apoyarse en Codex y OpenCode con DeepSeek V4 Flash, pero ninguno puede redefinir el producto.

### 19.1. Codex

Usar para tareas importantes, transversales o de alto riesgo:

- auditorías completas del repo;
- reconciliación entre código, modelos y especificaciones;
- migraciones de esquema;
- cambios que atraviesan modelos, API, UI y tests;
- refactorizaciones estructurales;
- verificación de compatibilidad;
- ejecución integral de pruebas;
- revisión de diff y cierre técnico;
- commit y push únicamente cuando sea solicitado explícitamente.

### 19.2. OpenCode + DeepSeek V4 Flash

Usar para tareas acotadas y bien especificadas:

- lectura y síntesis de módulos;
- implementación de pruebas focales;
- cambios locales en schemas o validadores;
- ajustes de interfaz delimitados;
- documentación derivada;
- limpieza repetitiva;
- comparación de estados y enums;
- búsqueda de referencias y callers.

### 19.3. Reglas para ambos agentes

Cada tarea debe incluir:

- documento rector aplicable;
- objetivo único;
- archivos permitidos;
- archivos prohibidos;
- invariantes;
- pruebas obligatorias;
- formato de reporte;
- prohibición de ampliar alcance;
- prohibición de inventar decisiones de negocio;
- obligación de informar dudas o contradicciones;
- revisión de `git diff --check` y `git status` antes del cierre.

No ejecutar agentes simultáneamente sobre los mismos archivos.

No permitir que un agente transforme una hipótesis conceptual en código productivo sin especificación aprobada.

---

## 20. Estrategia de pruebas

### 20.1. Pruebas semánticas

Corpus mínimo con:

- conversaciones claramente afines;
- conversaciones temáticamente cercanas pero no afines;
- simpatía temática sin intención;
- intención explícita;
- ambigüedad;
- falsos positivos léxicos;
- contexto contradictorio.

Toda evaluación debe mostrar evidencia.

### 20.2. Pruebas de estados

Deben bloquearse, entre otras:

```text
DETECTED → QUALIFICATION_STARTED
REPLIED → QUALIFIED
AFFINITY_NOT_CONFIRMED → PREQUALIFICATION_ACCEPTED
PREQUALIFICATION_INVITED → TRANSFERRED_TO_CRM
```

Debe permitirse únicamente una progresión válida y trazable.

### 20.3. Pruebas humanas

El piloto debe demostrar:

- revisión de conversaciones reales;
- decisiones persistidas;
- contacto humano registrado;
- resultado de descubrimiento registrado;
- consentimiento separado;
- precalificación solo después del gate;
- arquetipo basado en diálogo y confirmado humanamente;
- transferencia controlada.

---

## 21. Criterios de aceptación de la arquitectura

La arquitectura se considera correctamente implementada cuando:

1. una conversación pública puede ingresar sin convertirse en persona o lead;
2. la evaluación explica tema, contexto, afinidad aparente e intención aparente;
3. los fragmentos de evidencia existen realmente en el texto;
4. un falso positivo semántico no entra a la bandeja prioritaria;
5. ningún arquetipo se asigna desde la conversación pública;
6. el humano puede aprobar un contacto de descubrimiento;
7. el sistema registra el contacto y la respuesta;
8. el humano registra si la afinidad fue revelada;
9. la precalificación permanece bloqueada sin consentimiento;
10. la cualificación usa datos declarados y revisables;
11. Relaticle no recibe registros prematuros;
12. todo el recorrido puede reconstruirse mediante evidencia persistida.

---

## 22. Exclusiones explícitas

No se construye en esta etapa:

- SaaS multiempresa;
- plataforma semántica general;
- RAG institucional;
- chatbot;
- gemelo semántico;
- CRM propio;
- venta automática;
- contacto automático;
- scoring psicológico;
- inferencia financiera desde redes;
- clasificación automática definitiva de arquetipos;
- portal del fundador dentro de RADAR;
- reserva, firma o pagos dentro de RADAR;
- infraestructura distribuida sin necesidad probada.

---

## 23. Decisiones pendientes que no bloquean la arquitectura

Pueden definirse más adelante mediante especificaciones de negocio:

- fuentes públicas iniciales definitivas;
- repertorio final de consultas;
- taxonomía operativa de afinidades;
- preguntas exactas del diálogo de descubrimiento;
- cuestionario definitivo;
- umbrales de precalificación;
- formato de transferencia a Relaticle;
- responsables humanos y permisos;
- política de retención de datos;
- reglas jurídicas por fuente y jurisdicción.

Estas decisiones no justifican crear otro repositorio ni ampliar la plataforma.

---

## 24. Definición de terminado

RADAR no está terminado por:

- recuperar resultados;
- llamar a Agnes;
- asignar puntajes;
- mostrar una bandeja;
- sugerir mensajes;
- guardar una persona;
- ejecutar un cuestionario sintético.

Para esta etapa, RADAR estará terminado cuando exista evidencia reproducible del siguiente recorrido real:

```text
consulta real
→ conversación pública real
→ afinidad semántica aparente explicada
→ revisión humana
→ persona aprobada para descubrimiento
→ acercamiento humano real
→ respuesta real
→ diálogo de descubrimiento
→ afinidad revelada o descartada
→ consentimiento para continuar
→ precalificación real
→ lead calificado
→ transferencia controlada al embudo comercial
```

---

## 25. Mandato final de desarrollo

Toda decisión técnica debe demostrar cómo ayuda a realizar este recorrido:

> De la conversación pública a la persona; de la persona al embudo humano de descubrimiento; del descubrimiento consentido a la precalificación; y de la precalificación al embudo comercial de Inlak’ech.

No crear otro producto alrededor de RADAR. No crear otro repositorio. No convertir herramientas auxiliares en el centro de la arquitectura. No permitir que el software o el LLM sustituyan el vínculo humano mediante el cual la afinidad con Inlak’ech se revela realmente.
