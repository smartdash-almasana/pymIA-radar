# PROPUESTA COMERCIAL Y TÉCNICA
# RADAR INLAK’ECH — VERSIÓN OPERATIVA 1

**Documento para presentación al cliente**  
**Fecha:** 21 de julio de 2026  
**Moneda:** dólares estadounidenses (USD)  
**Validez económica de la propuesta:** 30 días  
**Producto:** RADAR Inlak’ech  
**Objetivo:** convertir conversaciones públicas de internet en oportunidades trazables para revisión humana y futura incorporación al sistema operativo integral de Inlak’ech.

---

## 1. Resumen ejecutivo

RADAR Inlak’ech será una herramienta propia de descubrimiento y evaluación de conversaciones públicas. Su función será localizar señales de afinidad con Inlak’ech, recuperar la evidencia original, identificar la cuenta pública que realizó la intervención, evaluar su posible relevancia y presentar cada caso en una bandeja de revisión humana.

El producto no se ofrecerá como un simple scraper ni como una base de datos comprada. Se construirá como una pieza operativa integrable al futuro sistema de Inlak’ech:

```text
fuentes de internet
→ navegación y extracción
→ evidencia trazable
→ interpretación semántica
→ revisión humana
→ candidato presuntivo aprobado
→ salida preparada hacia el siguiente tramo del embudo
```

La versión presupuestada entrega un RADAR operativo, probado y desplegado. Incluye la arquitectura de acceso mediante APIs, HTTP, RSS y MCP Playwright; workers aislados por plataforma; conservación de evidencia; deduplicación; evaluación semántica; panel HTMX; métricas; auditoría y un contrato técnico preparado para integrar más adelante CRM, WhatsApp, landing pages, Relaticle u otros módulos del sistema operativo de Inlak’ech.

### Recomendación económica

> **Precio fijo recomendado de desarrollo: USD 2480**

### Plazo estimado

> **6 a 7 semanas calendario**, incluyendo implementación, pruebas con fuentes reales, correcciones, despliegue y aceptación.

Esta estimación parte del RADAR ya existente: repositorio, modelos, base de datos local, evaluación semántica, interfaz inicial, pruebas y documentación previa. No se cotiza un producto desde cero.

---

# 2. Qué problema resuelve

Inlak’ech necesita encontrar personas, grupos y proyectos que ya estén expresando públicamente intereses compatibles con su propuesta, por ejemplo:

- intención de vivir o participar en comunidades regenerativas;
- búsqueda de ecoaldeas, cohousing o comunidades intencionales;
- interés por permacultura, regeneración territorial o vida comunitaria;
- búsqueda de proyectos con impacto y pertenencia;
- búsqueda de colaboradores, fundadores, afiliados o aliados;
- preguntas sobre inversión consciente, gobernanza, seguridad, comunidad o propósito;
- interés explícito en México, Yucatán o proyectos de vida territorial compatibles.

Actualmente esas señales están dispersas en redes, foros, publicaciones, perfiles y comentarios. El trabajo manual consume tiempo, produce registros incompletos y no deja evidencia organizada.

RADAR convierte ese trabajo en un proceso repetible y auditable.

---

# 3. Qué entregará RADAR V1

## 3.1 Descubrimiento multiplataforma

El sistema podrá ejecutar campañas de búsqueda configurables mediante distintos métodos:

```text
API oficial
API pública
HTTP estructurado
RSS / Atom
MCP Playwright
carga manual de URLs
```

Se incluirá un laboratorio y conectores operativos para probar y trabajar sobre las plataformas priorizadas por el cliente:

- Facebook;
- Instagram;
- LinkedIn;
- TikTok;
- fuentes abiertas ya incorporadas o técnicamente compatibles, como Bluesky, foros públicos, Reddit, RSS y sitios basados en Discourse.

La condición real de cada fuente quedará visible en el sistema:

```text
ACTIVE
DEGRADED
LOGIN_REQUIRED
CAPTCHA_BLOCKED
RATE_LIMITED
SELECTOR_BROKEN
DISABLED
```

El producto no ocultará los bloqueos: los detectará, clasificará y reportará.

## 3.2 Workers MCP Playwright por plataforma

Se implementará una arquitectura de navegación controlada con perfiles y sesiones aisladas.

Cada worker podrá realizar operaciones como:

```text
buscar resultados
abrir publicaciones
expandir comentarios
leer contenido renderizado
abrir perfiles
extraer identificadores y enlaces
capturar evidencia
verificar que una URL siga activa
```

No se usará un único navegador genérico para todas las redes. Cada plataforma tendrá su configuración, selectores, estado y telemetría.

## 3.3 Registro de evidencia

Cada registro aceptado conservará internamente:

- plataforma;
- URL original;
- texto exacto evaluado;
- autor o cuenta pública;
- fecha publicada cuando esté disponible;
- fecha de captura;
- identificadores de contenido y actor;
- método de acceso;
- versión del extractor;
- captura o artefacto cuando corresponda;
- evaluación semántica;
- decisión humana.

Esto permitirá explicar por qué un caso fue seleccionado y volver a abrir la fuente original.

## 3.4 Normalización y deduplicación

RADAR evitará procesar repetidamente la misma publicación o cuenta utilizando:

```text
platform_actor_id
platform_content_id
URL canónica
hash del contenido
```

No se fusionarán automáticamente identidades de redes diferentes.

## 3.5 Evaluación semántica

El evaluador analizará la intervención concreta y generará una salida estructurada con:

- afinidad temática;
- afinidad con valores;
- intención aparente;
- calidad de evidencia;
- riesgo de falso positivo;
- fragmentos literales de respaldo;
- acción recomendada;
- datos faltantes.

Clasificación operativa:

```text
CLEAR
POSSIBLE
NONE
```

Acción propuesta:

```text
REVIEW
OBSERVE
DISCARD
```

El modelo interpreta. Las reglas del sistema validan. La persona decide.

## 3.6 Bandeja de revisión humana

La interfaz permitirá:

```text
ver conversaciones encontradas
ordenar por prioridad
abrir la intervención exacta
abrir el perfil público
visitar la fuente original
ver evidencia y evaluación
aprobar
observar
descartar
solicitar nueva comprobación
```

La aprobación humana será obligatoria antes de pasar un registro al siguiente tramo.

## 3.7 Campañas y consultas configurables

El equipo podrá definir:

- plataforma;
- consultas;
- idioma;
- región;
- ventana temporal;
- volumen máximo;
- frecuencia;
- prioridad;
- objetivo de búsqueda.

Las campañas quedarán registradas para comparar su rendimiento.

## 3.8 Métricas operativas

El panel registrará como mínimo:

- resultados recuperados;
- páginas abiertas;
- contenido extraído correctamente;
- cuentas únicas;
- duplicados;
- errores de selector;
- sesiones vencidas;
- CAPTCHAs o bloqueos;
- evaluaciones válidas;
- falsos positivos detectados por revisión;
- candidatos aprobados;
- tiempo de revisión;
- costo técnico por candidato aprobado.

## 3.9 Despliegue operativo

La versión final quedará desplegada en infraestructura privada mediante:

```text
Docker Compose
FastAPI
HTMX + Jinja2
PostgreSQL
Redis
workers de tareas
MCP Playwright
almacenamiento de evidencia
proxy HTTPS
backups
logs
health checks
```

Kiwi podrá utilizarse como plano de despliegue y operación, manteniendo separadas las responsabilidades del producto.

---

# 4. Qué conseguirá el cliente

Al terminar esta etapa, Inlak’ech conseguirá:

## 4.1 Una herramienta propia, no una campaña aislada

RADAR quedará instalado, documentado y preparado para ejecutar nuevas campañas sin reconstruir el sistema en cada oportunidad.

## 4.2 Conversaciones reales con evidencia

Cada resultado podrá abrirse y verificarse en su fuente original. El equipo sabrá qué expresó la cuenta y por qué RADAR la seleccionó.

## 4.3 Priorización del trabajo humano

La herramienta reducirá el universo de publicaciones a una bandeja ordenada de casos que merecen atención.

## 4.4 Aprendizaje por plataforma

El equipo podrá medir con datos reales:

- dónde aparecen las mejores conversaciones;
- qué consultas producen resultados útiles;
- qué plataformas son estables;
- qué perfiles responden a cada objetivo;
- cuánto cuesta revisar y obtener un caso aprobado.

## 4.5 Base técnica para el ecosistema Inlak’ech

RADAR no quedará aislado. Entregará objetos y eventos estables para que otras piezas puedan consumirlos más adelante.

## 4.6 Autonomía tecnológica

El código, la base, la configuración, las campañas y la evidencia quedarán bajo control del proyecto, sujetos a las condiciones de las fuentes externas utilizadas.

---

# 5. Qué no conseguirá ni debe prometerse

## 5.1 No garantiza una cantidad fija de candidatos

RADAR garantiza el proceso técnico de búsqueda, extracción, evaluación y revisión. No puede garantizar que una plataforma contenga diez, cien o mil personas válidas para una consulta determinada.

La cantidad depende de:

- actividad pública existente;
- calidad de las consultas;
- región e idioma;
- ventana temporal;
- visibilidad de los perfiles;
- acceso disponible;
- cambios de cada plataforma.

## 5.2 No garantiza conversiones comerciales

Una afinidad presuntiva no equivale a interés confirmado, capacidad económica, disponibilidad ni intención de participar en Inlak’ech.

La conversión solo puede medirse después del acercamiento y la respuesta voluntaria.

## 5.3 No garantiza acceso permanente a todas las redes

Facebook, Instagram, TikTok, LinkedIn y otras plataformas pueden modificar:

- interfaz;
- selectores;
- autenticación;
- límites;
- CAPTCHAs;
- visibilidad;
- condiciones de acceso.

RADAR detectará estos cambios y permitirá reparar los conectores, pero no puede controlar decisiones de terceros.

## 5.4 No rompe CAPTCHAs ni controles de seguridad

La versión propuesta no incluye evasión agresiva, compra de identidades, granjas de cuentas ni mecanismos destinados a vulnerar controles.

Cuando una tarea requiera acción humana, el sistema la marcará como `HUMAN_ACTION_REQUIRED`.

## 5.5 No obtiene datos ocultos

No se prometen:

- correos privados;
- teléfonos no publicados;
- perfiles ocultos;
- datos de grupos sin acceso legítimo;
- identificación cruzada automática entre redes;
- capacidad económica inferida como hecho.

## 5.6 No incluye todavía el tramo completo de contacto y conversión

Esta propuesta no incluye:

- envío automático de mensajes;
- campañas de WhatsApp;
- secuencias de seguimiento;
- CRM comercial completo;
- landing pages personalizadas;
- nurturing;
- calificación conversacional;
- integración productiva completa con Relaticle;
- cierre de inversión o afiliación.

Incluye el enchufe técnico para construir ese tramo sin rehacer RADAR.

---

# 6. Enchufe preparado para la segunda etapa

RADAR V1 entregará un contrato explícito de salida para el futuro sistema operativo de Inlak’ech.

## 6.1 Entidad de salida

```text
ApprovedOpportunityV1
```

Campos previstos:

```text
opportunity_id
actor_type
platform
public_actor_id
public_profile_url
source_contribution_id
source_url
evidence_summary
affinity_assessment
intent_assessment
risk_flags
public_contact_points
human_decision
approved_at
recommended_next_route
```

## 6.2 Rutas previstas

```text
COLLABORATOR_OUTREACH
INVESTOR_OUTREACH
AFFILIATE_OUTREACH
COMMUNITY_MEMBER_OUTREACH
INSTITUTIONAL_PARTNERSHIP
OBSERVATION
```

## 6.3 Interfaces de integración

Se dejarán preparados:

- endpoint interno de lectura;
- exportación JSON/CSV;
- evento de dominio;
- webhook configurable, inicialmente desactivado;
- adaptador de salida desacoplado;
- estados de transferencia;
- idempotencia para no transferir dos veces el mismo caso.

## 6.4 Sistemas futuros compatibles

El contrato podrá alimentar posteriormente:

- CRM propio;
- Relaticle;
- WhatsApp Business;
- email;
- landing pages;
- formularios;
- módulo de perfiles o arquetipos;
- agenda de entrevistas;
- sistema de afiliados;
- seguimiento de inversores;
- panel integral de Inlak’ech.

## 6.5 Principio de integración

```text
RADAR descubre y justifica.
El siguiente tramo contacta y corrobora.
El CRM administra la relación.
El sistema operativo de Inlak’ech integra la trayectoria completa.
```

---

# 7. Sección técnica

## 7.1 Arquitectura

```text
Source Control Plane
→ Discovery Orchestrator
→ Access Router
→ API / HTTP / RSS / MCP Playwright
→ Evidence Pipe
→ Normalización y deduplicación
→ Semantic Intelligence
→ Eligibility Gate
→ Human Review
→ ApprovedOpportunityV1
```

## 7.2 Stack

### Aplicación

```text
Python 3.12+
FastAPI
HTMX
Jinja2
Pydantic v2
SQLAlchemy 2
Alembic
```

### Datos

```text
PostgreSQL
Redis
MinIO o almacenamiento equivalente
```

### Navegación y conectores

```text
MCP Playwright
Playwright
httpx
APIs oficiales
RSS / Atom
extractores específicos por plataforma
```

### Ejecución

```text
RQ o Dramatiq
scheduler
workers aislados
colas por plataforma
```

### Operación

```text
Docker Compose
Kiwi
proxy HTTPS
backups
logs estructurados
health checks
alertas
```

## 7.3 Seguridad

Se implementarán:

- secretos fuera del código;
- aislamiento de sesiones por plataforma;
- cookies fuera de la base comercial;
- perfiles de navegador protegidos;
- acceso autenticado al panel;
- registros de acciones;
- backups;
- separación entre evidencia, sesión y datos comerciales.

## 7.4 Calidad y pruebas

La entrega incluirá:

- pruebas unitarias;
- pruebas contractuales de conectores;
- pruebas de estados y deduplicación;
- pruebas del schema semántico;
- corpus de falsos positivos;
- pruebas end-to-end del panel;
- probes reales separados de la suite normal;
- prueba de recuperación ante sesión vencida o selector roto.

## 7.5 Criterio de aceptación

El producto se considerará entregado cuando:

1. pueda crear y ejecutar campañas desde el sistema;
2. utilice al menos los métodos API, HTTP/RSS, Playwright y URL manual;
3. los workers de las plataformas priorizadas hayan sido probados y su estado real quede documentado;
4. una publicación recuperada pueda transformarse en evidencia normalizada;
5. la evaluación semántica produzca salida válida o error explícito;
6. los duplicados no creen candidatos repetidos;
7. la bandeja permita aprobar, observar y descartar;
8. un aprobado genere `ApprovedOpportunityV1`;
9. exista exportación y endpoint para la segunda etapa;
10. el sistema esté desplegado con backups, logs y documentación operativa.

No se utilizará como criterio de aceptación una cantidad comercial fija de candidatos, porque esa cifra depende del contenido y acceso de terceros.

---

# 8. Plan de implementación y plazo

## Etapa 1 — Base y cierre semántico

**Duración:** 1 semana

- auditoría del estado actual;
- centralización de configuración del modelo;
- prueba viva de casos reales;
- cierre de contratos de evaluación;
- normalización de estados.

## Etapa 2 — Source Control Plane y tareas

**Duración:** 1 a 1,5 semanas

- registro de fuentes;
- campañas;
- cuentas y sesiones;
- cola de tareas;
- límites;
- estados y errores.

## Etapa 3 — Laboratorio MCP Playwright

**Duración:** 1,5 a 2 semanas

- Facebook;
- Instagram;
- LinkedIn;
- TikTok;
- pruebas de acceso;
- extracción real;
- capturas;
- matriz de alcance;
- identificación de bloqueos.

## Etapa 4 — Workers y Evidence Pipe

**Duración:** 2 semanas

- workers aislados;
- extractores versionados;
- sesiones persistentes;
- evidencias;
- almacenamiento;
- normalización;
- deduplicación.

## Etapa 5 — Integración con Lista 1 e interfaz

**Duración:** 1,5 semanas

- contribución individual;
- evaluación;
- reglas de elegibilidad;
- bandeja;
- decisiones humanas;
- métricas.

## Etapa 6 — Enchufe al segundo tramo

**Duración:** 1 semana

- `ApprovedOpportunityV1`;
- endpoint;
- exportación;
- eventos;
- webhook desactivado;
- rutas de oportunidad;
- pruebas de idempotencia.

## Etapa 7 — Piloto, estabilización y entrega

**Duración:** 1,5 a 2 semanas

- ejecución con fuentes reales;
- corrección de extractores;
- pruebas integrales;
- despliegue;
- backups;
- documentación;
- capacitación;
- aceptación.

### Tiempo total comprometible

> **6 a 8 semanas calendario.**

El rango contempla que las plataformas externas pueden requerir ajustes durante las pruebas. Un cronograma de menos de siete semanas sería posible como demostrador, pero no sería una estimación responsable para entregar un producto probado y operable.

---

# 9. Presupuesto de desarrollo

## 9.1 Desglose

| Componente | Valor USD |
|---|---:|
| Auditoría, cierre de contratos y estabilización semántica | 220 |
| Source Control Plane, campañas, colas y estados | 350 |
| Laboratorio MCP Playwright multiplataforma | 360 |
| Workers, sesiones, extractores y Evidence Pipe | 500 |
| Normalización, deduplicación e integración con Lista 1 | 280 |
| Interfaz de revisión, métricas y auditoría | 260 |
| Enchufe `ApprovedOpportunityV1` para segunda etapa | 170 |
| Despliegue, seguridad, backups y observabilidad | 140 |
| Piloto real, correcciones, documentación y capacitación | 200 |
| **TOTAL FIJO** | **24.800** |

## 9.2 Forma de pago sugerida

| Hito | Porcentaje | Importe USD |
|---|---:|---:|
| Inicio, alcance y planificación cerrados | 30 % | 744 |
| Source Control Plane y laboratorio Playwright operativos | 30 % | 744 |
| Flujo completo hasta revisión y salida V1 | 25 % | 620 |
| Piloto, despliegue y aceptación | 15 % | 372 |
| **Total** | **100 %** | **2480** |

## 9.3 Garantía incluida

Se incluyen **30 días corridos de garantía correctiva** desde la aceptación para errores reproducibles del software entregado.

La garantía no cubre cambios posteriores de interfaz, autenticación, API o condiciones de plataformas externas. Esos cambios forman parte del mantenimiento evolutivo.

---

# 10. Fundamento de la valoración

La valoración se calculó combinando:

- existencia de una base RADAR ya desarrollada;
- necesidad de ingeniería especializada en automatización web, sesiones, evidencia, colas y conectores;
- evaluación semántica y pruebas con modelos;
- interfaz y operación humana;
- despliegue productivo;
- integración futura;
- riesgo técnico de plataformas cambiantes;
- prueba real y estabilización.

Las referencias de mercado consultadas para 2026 ubican:

- desarrolladores senior de Argentina y LATAM aproximadamente entre USD 55 y USD 85 por hora;
- arquitectos o líderes técnicos aproximadamente entre USD 65 y USD 95 por hora;
- equipos nearshore generales aproximadamente entre USD 30 y USD 80 por hora;
- MVPs de software personalizado en LATAM aproximadamente entre USD 10.000 y USD 40.000, con plataformas complejas por encima de ese rango;
- proyectos independientes de IA entre USD 1.500 y USD 30.000 o más, y proyectos de agencia desde USD 15.000 hasta USD 80.000;
- automatizaciones Playwright subestimadas frecuentemente porque el costo real incluye implementación, infraestructura y mantenimiento, no la licencia gratuita del framework.

Sobre esas referencias, el precio de USD 2480 es consistente con un proyecto especializado de complejidad media-alta, pero se mantiene por debajo de una cotización de agencia completa porque:

1. ya existe una base funcional;
2. se reutilizará el stack actual;
3. se trabajará como monolito modular;
4. se utilizará desarrollo asistido por IA;
5. no se incluye todavía el CRM ni el tramo de contacto automático.

---

# 11. Costos operativos mensuales estimados

Estos importes no forman parte del precio de desarrollo.

## 11.1 Infraestructura inicial

| Concepto | Estimación mensual USD |
|---|---:|
| VPS principal con recursos para aplicación, base y workers | 50–160 |
| Almacenamiento y backups | 10–40 |
| Dominio, correo técnico y servicios auxiliares | 5–25 |
| Monitoreo o registro de errores | 0–40 |
| Consumo de modelos o proveedores semánticos | 0–150 |
| **Operación técnica estimada** | **65–415/mes** |

El costo crecerá con:

- cantidad de workers simultáneos;
- volumen de páginas;
- capturas almacenadas;
- modelos pagos;
- proxies o servicios externos autorizados;
- APIs comerciales;
- frecuencia de las campañas.

## 11.2 Trabajo humano

La revisión de candidatos no está incluida en el costo de infraestructura. Inlak’ech deberá asignar una persona o contratar un servicio operativo para revisar, aprobar y luego contactar.

## 11.3 Mantenimiento recomendado

### Plan mínimo

```text
USD 65 por mes
hasta 8 horas técnicas
```

Adecuado para:

- actualizaciones menores;
- reparación de selectores;
- revisión de logs;
- ajustes de consultas;
- soporte operativo.

### Plan operativo

```text
USD 125 por mes
hasta 20 horas técnicas
```

Adecuado para:

- varias plataformas activas;
- correcciones frecuentes;
- nuevos extractores pequeños;
- optimización de campañas;
- acompañamiento del piloto comercial.

Las horas adicionales se cotizarían a **USD 65 por hora**.

---

# 12. Opciones comerciales

## Opción A — RADAR V1 completo recomendado

```text
USD 2480
9 a 11 semanas
```

Incluye todo el alcance de este documento.

## Opción B — Piloto técnico reducido

```text
USD 1290
5 a 7 semanas
```

Incluye:

- cierre semántico;
- laboratorio Playwright;
- un worker estabilizado;
- evidencia;
- Lista 1;
- interfaz básica;
- exportación manual.

No incluye:

- todos los workers priorizados;
- observabilidad completa;
- enchufe de eventos y webhook;
- despliegue endurecido;
- piloto multiplataforma amplio.

Esta opción reduce inversión, pero posterga parte del trabajo necesario para integrarlo al sistema operativo de Inlak’ech.

## Opción C — RADAR V1 más segundo tramo

No se recomienda cerrar ahora un precio fijo sin definir:

- canales de contacto;
- CRM elegido;
- WhatsApp Business;
- Relaticle;
- mensajes y secuencias;
- reglas de consentimiento;
- perfiles y caminos comerciales.

Como referencia preliminar, el segundo tramo completo podría requerir entre **USD 14.000 y USD 28.000 adicionales**, según las integraciones y el grado de automatización.

---

# 13. Responsabilidades del cliente

Para cumplir el plazo, Inlak’ech deberá aportar:

- acceso oportuno a cuentas de prueba autorizadas;
- aprobación de consultas y objetivos;
- definición de regiones e idiomas;
- disponibilidad de un revisor humano;
- hosting, dominio y credenciales necesarias;
- respuesta a decisiones funcionales en un máximo de 48 horas hábiles;
- validación de entregas parciales;
- contenido institucional necesario para preparar la segunda etapa.

Los retrasos en accesos, cuentas, validaciones o decisiones desplazarán el calendario.

---

# 14. Propiedad y entrega

Con el pago completo, el cliente recibirá:

- código fuente desarrollado;
- documentación técnica;
- documentación operativa;
- contratos de datos;
- configuración de despliegue;
- pruebas;
- manual de operación;
- acceso al repositorio acordado.

No se transfieren derechos sobre componentes de terceros, plataformas, APIs, modelos o librerías, que conservan sus propias licencias y condiciones.

---

# 15. Conclusión

RADAR V1 no promete una fuente infinita de inversores o colaboradores. Entrega algo más defendible:

> Un sistema propio capaz de recorrer fuentes reales, conservar evidencia, identificar señales, reducir ruido, priorizar conversaciones y entregar oportunidades aprobadas a la siguiente pieza del ecosistema Inlak’ech.

La inversión recomendada es:

```text
USD 24.800
```

El plazo responsable de entrega es:

```text
6 a 9 semanas calendario
```

El producto quedará preparado para que una segunda etapa incorpore:

```text
acercamiento
→ respuesta
→ corroboración
→ precalificación
→ CRM
→ Relaticle
→ seguimiento de colaboradores, inversores, afiliados y aliados
```

## Recomendación final

Contratar **RADAR V1 completo** y medir durante el piloto:

- costo por conversación útil;
- costo por candidato aprobado;
- plataformas con mayor rendimiento;
- tiempo humano de revisión;
- tasa de respuesta posterior.

Solo después de esos datos conviene presupuestar y automatizar el tramo de atracción y conversión. Así, cada nueva pieza se integrará sobre evidencia operativa y no sobre supuestos.

---

# 16. Referencias de mercado utilizadas

- Freshwork, *How much does custom software development cost? 2026 guide (nearshore LATAM)*.
- SODI, *Cuánto cuesta el software a medida en Argentina 2026*.
- TecLatam, *Nearshore Web Development Rates in Latin America 2026*.
- ProLatamWork, *LATAM Developer Hourly Rates 2026*.
- DIPA Solutions, *Cuánto cuesta desarrollar software a medida en LATAM 2026*.
- Carlos García, *How much does an independent AI consultant charge in LATAM in 2026*.
- DeviQA, *How much does Playwright test automation actually cost?*.
- DigitalOcean, documentación oficial de precios de Droplets, almacenamiento y monitoreo, consultada en julio de 2026.
