# RADAR Inlak’ech — Reporte de situación y ciclos restantes hasta constituir el MVP

**Versión:** V1  
**Destinatarios:** socios de Inlak’ech y equipo de seguimiento  
**Objetivo:** explicar, con un nivel técnico medio y de manera pedagógica, qué está construido, qué falta y cómo se completa el MVP comprometido.

---

## 1. Resumen ejecutivo

RADAR ya superó la etapa de prueba conceptual. Hoy existe una base funcional capaz de:

```text
abrir una fuente pública
→ navegar de forma persistente
→ extraer contenido visible
→ guardar evidencia
→ registrar una conversación
→ evitar duplicados
```

Esto significa que la primera parte del producto —descubrimiento y captura de evidencia— ya está técnicamente constituida.

El sistema también cuenta con:

- una evaluación semántica V3 ya desarrollada;
- una bandeja de revisión humana;
- una lista preliminar de candidatos;
- reglas de trazabilidad, control y revisión.

Lo que falta no es “inventar” RADAR desde cero, sino conectar y cerrar las piezas existentes dentro de un flujo único, verificable y listo para una prueba integral.

### Situación actual, en una frase

> RADAR ya sabe encontrar, registrar y conservar conversaciones con evidencia; ahora debe cerrar el recorrido completo desde esa conversación hasta una oportunidad aprobada y preparada para ser transferida.

---

## 2. Qué problema resuelve RADAR

RADAR busca conversaciones públicas en las que una persona manifiesta dudas, interés, afinidad, intención o preguntas que podrían relacionarse con Inlak’ech.

No convierte automáticamente a esa persona en lead. Tampoco decide por sí solo que existe afinidad real.

Su función es ordenar un proceso humano:

```text
conversación pública
→ afinidad aparente
→ evaluación con evidencia
→ revisión humana
→ aprobación, observación o descarte
→ contacto humano posterior
→ eventual precalificación
```

El principio central es:

> El sistema encuentra e interpreta señales. La decisión sigue siendo humana.

---

## 3. Qué ya está construido

## 3.1 Navegación y descubrimiento

RADAR ya cuenta con un navegador persistente basado en Playwright MCP.

En términos simples, esto permite que el sistema:

- abra páginas públicas;
- mantenga una sesión de navegación;
- lea el contenido visible;
- identifique la URL final real;
- tome capturas de pantalla cuando corresponde;
- clasifique bloqueos como CAPTCHA, login requerido o pérdida de sesión.

La persistencia de la sesión evita abrir un navegador nuevo para cada consulta y mejora estabilidad y velocidad.

### Estado

```text
PLAYWRIGHT MCP: VERIFICADO
NAVEGACIÓN PERSISTENTE: VERIFICADA
CAPTURA DE TEXTO Y URL: VERIFICADA
CAPTURA DE PANTALLA: VERIFICADA
CLASIFICACIÓN DE ERRORES: VERIFICADA
```

---

## 3.2 Evidencia y trazabilidad

Cada conversación encontrada puede conservar:

- texto visible;
- URL solicitada;
- URL final;
- autor, cuando está disponible;
- estado de identificación del autor;
- captura de pantalla;
- tiempo de respuesta;
- estado de navegación;
- origen de la búsqueda.

Esto es importante porque RADAR no debe limitarse a decir “encontré algo relevante”. Debe poder mostrar qué encontró, dónde lo encontró y por qué fue considerado.

### Estado

```text
EVIDENCIA: INTEGRADA
TRAZABILIDAD: PRESERVADA
PERSISTENCIA: INTEGRADA CON EL SISTEMA EXISTENTE
```

---

## 3.3 Control de duplicados

Uno de los problemas más frecuentes en sistemas de búsqueda es guardar varias veces la misma publicación.

Ese riesgo ya fue tratado. RADAR identifica una conversación usando:

```text
fuente normalizada + URL canónica
```

Esto permite reconocer como una misma conversación casos como:

- la misma URL con o sin barra final;
- la misma URL con parámetros de campaña;
- la misma publicación con texto levemente actualizado;
- la misma fuente escrita con mayúsculas, minúsculas o espacios.

### Estado

```text
IDEMPOTENCIA: VERIFICADA
DUPLICADOS POR CAMBIOS MENORES: CONTROLADOS
```

---

## 3.4 Evaluación semántica

RADAR ya posee una evaluación semántica V3.

Esta capa intenta responder preguntas como:

- ¿hay afinidad temática?
- ¿hay afinidad de valores?
- ¿hay intención aparente?
- ¿la evidencia es suficiente?
- ¿existe riesgo de falso positivo?
- ¿qué acción se recomienda?

La evaluación no depende solo de palabras clave. Busca interpretar contexto y sentido.

También existe:

- un esquema estructurado de salida;
- normalización de respuestas;
- evidencia literal;
- anti-patrones;
- fallback y failover entre proveedores;
- revisión humana obligatoria.

### Estado

```text
MOTOR SEMÁNTICO: IMPLEMENTADO
CONEXIÓN DEFINITIVA CON PLAYWRIGHT: PENDIENTE
CIERRE CONTRACTUAL DE CALIDAD: PENDIENTE
```

---

## 3.5 Revisión humana

Existe una interfaz HTMX para revisar conversaciones.

El flujo esperado es:

```text
abrir conversación
→ ver evidencia
→ abrir fuente original
→ revisar evaluación
→ aprobar / observar / descartar
```

La interfaz ya existe, pero debe verificarse de punta a punta con conversaciones provenientes del nuevo flujo Playwright.

### Estado

```text
BANDEJA DE REVISIÓN: EXISTE
VALIDACIÓN INTEGRAL: PENDIENTE
```

---

## 3.6 Calidad actual

La suite actual registra:

```text
298 pruebas aprobadas
2 fallos preexistentes
2 pruebas omitidas
0 regresiones nuevas en el ciclo Playwright
```

Los dos fallos pendientes están concentrados en el mecanismo de reintento del análisis semántico.

No afectan el flujo ya cerrado de:

```text
Playwright
→ evidencia
→ persistencia
→ conversación idempotente
```

Pero deben resolverse antes de declarar el MVP completamente constituido.

---

## 4. Qué está cerrado y qué todavía no

| Área | Estado | Explicación |
|---|---|---|
| Navegación pública | Cerrada técnicamente | Playwright abre, lee y conserva sesión |
| Evidencia | Cerrada técnicamente | Texto, URL, captura y trazabilidad disponibles |
| Duplicados | Cerrada técnicamente | Misma publicación no genera múltiples registros |
| Persistencia | Cerrada técnicamente | La conversación entra al sistema normal de RADAR |
| Evaluación semántica | Implementada | Falta conectarla de forma definitiva al flujo Playwright |
| Revisión humana | Implementada parcialmente | Falta verificar el recorrido integral |
| Lista de candidatos | Preliminar | Debe recibir casos reales del flujo completo |
| Oportunidad aprobada | Pendiente | Falta `ApprovedOpportunityV1` |
| Exportación JSON/CSV | Pendiente | Forma parte del cierre CRM-ready |
| Endpoint interno | Pendiente | Necesario para lectura neutral de oportunidades |
| Piloto contractual | Pendiente | Debe validar el sistema de punta a punta |

---

## 5. Lectura realista del avance

Hay dos maneras distintas de medir el progreso.

### Base técnica del núcleo

La base técnica de descubrimiento, evidencia y persistencia está aproximadamente en:

```text
90–95 %
```

### MVP completo constituido

El MVP completo, considerando integración, revisión, oportunidad aprobada, exportación y piloto, está aproximadamente en:

```text
70–80 %
```

La diferencia existe porque las piezas más complejas ya están construidas, pero todavía falta demostrar que funcionan como un solo producto.

---

# 6. Ciclos restantes hasta constituir el MVP

## Ciclo 1 — Cierre del reintento semántico

### Objetivo

Resolver los dos fallos conocidos de `TestSingleRetry`.

### Qué significa

Cuando el modelo devuelve una respuesta con formato inválido, RADAR debe intentar una segunda vez antes de declarar el fallo.

Hoy las pruebas muestran que ese segundo intento no está ocurriendo como fue especificado.

### Resultado esperado

```text
primer formato inválido
→ segundo intento
→ éxito o fallo definitivo controlado
```

### Criterio de cierre

- los dos tests pasan;
- no se agregan reintentos indefinidos;
- no se altera la semántica de negocio;
- la suite completa queda sin fallos nuevos.

### Tamaño estimado

```text
CICLO CORTO
```

---

## Ciclo 2 — Integración Conversation → evaluación semántica

### Objetivo

Conectar la conversación persistida desde Playwright con el evaluador semántico V3 existente.

### Qué significa

Hoy RADAR puede encontrar y guardar una conversación, y también sabe evaluarla semánticamente. Falta unir ambas capacidades dentro del mismo recorrido.

### Flujo esperado

```text
Playwright encuentra conversación
→ se guarda con evidencia
→ evaluación V3 analiza esa conversación
→ se guarda el resultado
```

### Criterio de cierre

- no se crea otro sistema paralelo;
- se reutiliza el evaluador existente;
- cada evaluación conserva evidencia;
- se registran fallos y fallback;
- existe prueba de integración.

### Tamaño estimado

```text
CICLO MEDIO
```

---

## Ciclo 3 — Cierre de revisión humana y Lista 1

### Objetivo

Comprobar que una conversación evaluada puede ser revisada y clasificada por una persona.

### Flujo esperado

```text
conversación evaluada
→ aparece en bandeja
→ se abre evidencia
→ se visita la fuente
→ humano aprueba / observa / descarta
→ decisión queda registrada
```

### Qué debe verificarse

- la interfaz no bloquea;
- la evidencia es comprensible;
- la evaluación no reemplaza la decisión humana;
- las conversaciones aprobadas entran a Lista 1;
- las descartadas no continúan.

### Tamaño estimado

```text
CICLO MEDIO
```

---

## Ciclo 4 — ApprovedOpportunityV1 y preparación CRM-ready

### Objetivo

Crear una representación neutral y estable de una oportunidad aprobada.

### Qué significa

RADAR no implementará un CRM. Debe producir una salida que cualquier CRM futuro pueda consumir.

El contrato requerido es:

```text
ApprovedOpportunityV1
```

Debe contener, como mínimo:

- identificador estable;
- conversación de origen;
- evidencia;
- resultado semántico;
- decisión humana;
- estado de preparación;
- fecha y trazabilidad;
- referencia externa opcional.

### Estados previstos

```text
READY_FOR_CRM
EXPORTED
TRANSFER_CONFIRMED
TRANSFER_FAILED
```

### Salidas requeridas

- JSON;
- CSV;
- endpoint interno de lectura;
- pruebas de validación.

### Tamaño estimado

```text
CICLO MEDIO
```

---

## Ciclo 5 — Piloto contractual integral

### Objetivo

Ejecutar el sistema completo con una campaña real o controlada y medir resultados.

### Flujo esperado

```text
búsqueda
→ Playwright
→ evidencia
→ conversación
→ evaluación semántica
→ revisión humana
→ Lista 1
→ oportunidad aprobada
→ exportación
```

### Qué debe demostrar

1. al menos dos tipos de fuente, incluyendo navegador;
2. evidencia completa en todas las conversaciones aprobadas;
3. deduplicación correcta;
4. al menos 95 % de salidas semánticas estructuralmente válidas;
5. al menos 80 % de concordancia humana en casos claros;
6. anti-patrones evidentes sin clasificación `CLEAR`;
7. 100 % de oportunidades aprobadas válidas bajo `ApprovedOpportunityV1`;
8. interfaz operativa sin bloqueos.

### Tamaño estimado

```text
CICLO MEDIO A ALTO
```

---

## Ciclo 6 — Cierre documental, entrega y handoff

### Objetivo

Dejar el MVP preparado para revisión, continuidad técnica y entrega.

### Incluye

- documentación final;
- instrucciones de instalación;
- estado de arquitectura;
- riesgos conocidos;
- resultados del piloto;
- criterios de aceptación;
- handoff para otro desarrollador;
- commit y push limpios;
- rama y versión identificables.

### Tamaño estimado

```text
CICLO CORTO
```

---

## 7. Cantidad de ciclos restantes

La estimación actual es:

```text
6 ciclos restantes
```

Distribución:

- 2 ciclos cortos;
- 3 ciclos medios;
- 1 ciclo medio/alto.

Esto no equivale necesariamente a seis semanas. Algunos ciclos pueden resolverse en una sesión si no aparecen contradicciones nuevas.

La principal variable no es escribir mucho código, sino validar correctamente cada integración sin romper lo ya construido.

---

## 8. Orden recomendado de ejecución

```text
1. cerrar TestSingleRetry
2. conectar Conversation con evaluación V3
3. cerrar revisión humana y Lista 1
4. implementar ApprovedOpportunityV1
5. ejecutar piloto integral
6. cerrar documentación y entrega
```

No conviene alterar este orden porque cada ciclo depende del anterior.

---

## 9. Riesgos actuales

## 9.1 Riesgos controlados

- bloqueos de algunas plataformas;
- autor no siempre disponible;
- variaciones de formato de los modelos;
- falsos positivos semánticos;
- calidad desigual entre fuentes.

Estos riesgos ya están contemplados mediante estados parciales, evidencia, revisión humana y fallback.

## 9.2 Riesgos de gestión

- mezclar nuevas herramientas antes de cerrar el MVP;
- ampliar el alcance hacia CRM, mensajería o automatización comercial;
- cambiar la interfaz sin validar primero el flujo funcional;
- declarar terminado el producto solo porque los módulos existen.

La regla debe seguir siendo:

> Primero cerrar el recorrido contratado. Después ampliar.

---

## 10. Qué no forma parte del MVP

Para evitar confusión entre socios, el MVP no incluye:

- CRM propio;
- elección definitiva de CRM;
- envío automático de mensajes;
- WhatsApp automático;
- seguimiento comercial completo;
- scraping autenticado masivo;
- evasión agresiva de bloqueos;
- garantía de una cantidad fija de candidatos;
- automatización de contacto sin aprobación humana.

El MVP entrega una herramienta de descubrimiento, evaluación, revisión y preparación de oportunidades.

---

## 11. Hito próximo

El próximo hito significativo será:

```text
PRIMER FLUJO INTEGRAL VERIFICADO
```

Ese hito se alcanza cuando una conversación real:

```text
es encontrada
→ se guarda con evidencia
→ se evalúa
→ aparece en revisión humana
→ se aprueba o descarta
```

A partir de ese momento, RADAR dejará de ser un conjunto de componentes conectables y pasará a ser un producto operativo de punta a punta.

---

## 12. Conclusión para socios

RADAR está en una etapa avanzada de construcción.

La parte más difícil de descubrimiento y evidencia ya fue resuelta: navegación persistente, captura, trazabilidad, persistencia y control de duplicados.

La evaluación semántica y la interfaz también existen. El trabajo restante consiste principalmente en:

- cerrar dos fallos focales;
- integrar piezas ya desarrolladas;
- formalizar la oportunidad aprobada;
- probar el recorrido completo;
- documentar la entrega.

### Diagnóstico final

```text
BASE TÉCNICA: SÓLIDA
ARQUITECTURA: ALINEADA
DESCUBRIMIENTO: OPERATIVO
EVIDENCIA: OPERATIVA
SEMÁNTICA: IMPLEMENTADA, PENDIENTE DE CIERRE
REVISIÓN HUMANA: EXISTENTE, PENDIENTE DE VALIDACIÓN INTEGRAL
CRM-READY: PENDIENTE
PILOTO FINAL: PENDIENTE
```

RADAR no está terminado, pero ya tiene constituido su núcleo técnico principal. El objetivo inmediato es convertir ese núcleo en un único recorrido verificable y, luego, demostrarlo con un piloto contractual completo.
