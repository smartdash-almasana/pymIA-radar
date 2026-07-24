# RADAR INLAK’ECH — ARQUITECTURA SUPERADORA V2

**Documento:** propuesta técnica ejecutable  
**Objetivo:** convertir RADAR en un sistema profesional de descubrimiento, análisis, validación y derivación comercial de conversaciones públicas, utilizando MCP Playwright como capacidad central de navegación web.

---

# 1. Decisión arquitectónica

La arquitectura propuesta reemplaza el enfoque lineal y ambiguo del diagrama anterior por una arquitectura de seis capas claramente separadas:

```text
FUENTES
→ ACCESO
→ EXTRACCIÓN
→ INTELIGENCIA
→ VALIDACIÓN
→ EMBUDO
```

MCP Playwright pasa a ser una capacidad central de acceso y extracción, pero no concentra toda la lógica del sistema.

La distribución correcta de responsabilidades es:

```text
RADAR gobierna
MCP expone herramientas
Playwright navega
los conectores extraen
el LLM interpreta
las reglas determinísticas deciden elegibilidad
la persona aprueba el paso comercial
Kiwi despliega y sostiene
```

---

# 2. Arquitectura general

```text
┌──────────────────────────────────────────────────────────────┐
│                    1. SOURCE CONTROL PLANE                   │
│ Registro de fuentes, cuentas, sesiones, límites y políticas │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                    2. DISCOVERY ORCHESTRATOR                 │
│ Consultas, objetivos, ventanas temporales y planes de tarea │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                      3. ACCESS ROUTER                        │
│ API | MCP Playwright | RSS | HTTP | Carga manual           │
└───────────────┬──────────────────────┬───────────────────────┘
                ↓                      ↓
       API CONNECTORS        PLAYWRIGHT PLATFORM WORKERS
                ↓                      ↓
┌──────────────────────────────────────────────────────────────┐
│                     4. EVIDENCE PIPE                         │
│ Texto, URL, autor, fecha, HTML útil, captura, metadatos      │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                  5. SEMANTIC INTELLIGENCE                    │
│ Normalización, deduplicación, afinidad, intención y riesgo  │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                    6. HUMAN CONVERSION GATE                  │
│ Aprobar | Observar | Descartar | Preparar acercamiento      │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                        7. EMBUDO                             │
│ CRM | Landing | WhatsApp | Email | Relaticle                │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                    8. KIWI OPERATIONS                        │
│ VPS, despliegues, secretos, backups, monitoreo y workers    │
└──────────────────────────────────────────────────────────────┘
```

---

# 3. Capa 1 — Source Control Plane

Esta capa decide con qué fuente se trabaja y bajo qué configuración.

## Entidades

```text
SourcePlatform
SourceAccount
BrowserSession
AccessPolicy
RatePolicy
ExtractorProfile
```

## Campos mínimos

```text
platform
access_mode
account_id
session_profile
login_required
rate_limit
max_pages_per_run
max_profiles_per_day
status
last_health_check
```

## Estados de fuente

```text
ACTIVE
DEGRADED
LOGIN_REQUIRED
CAPTCHA_BLOCKED
RATE_LIMITED
SELECTOR_BROKEN
DISABLED
```

Esta capa evita que el LLM decida arbitrariamente cómo entrar a una plataforma.

---

# 4. Capa 2 — Discovery Orchestrator

El orquestador convierte una intención de búsqueda en tareas concretas.

Ejemplo:

```text
objetivo:
localizar personas que expresen intención de vivir,
co-crear o participar en comunidades regenerativas
```

Se transforma en:

```text
plataforma: Instagram
consultas: 12
ventana temporal: 180 días
idiomas: español / inglés
máximo de resultados: 300
prioridad: alta
```

## Tipos de tareas

```text
DISCOVER_RESULTS
OPEN_POST
EXPAND_COMMENTS
EXTRACT_POST
EXTRACT_AUTHOR
OPEN_PROFILE
EXTRACT_CONTACT
CAPTURE_EVIDENCE
RECHECK_SOURCE
```

## Estados

```text
CREATED
QUEUED
RUNNING
COMPLETED
RETRYABLE_ERROR
BLOCKED
HUMAN_ACTION_REQUIRED
CANCELLED
```

---

# 5. Capa 3 — Access Router

El Access Router elige el mejor método disponible.

Orden recomendado:

```text
1. API oficial
2. API pública no autenticada
3. RSS / Atom / JSON
4. HTTP estructurado
5. MCP Playwright
6. carga manual
```

La elección no es ideológica. Es operativa.

MCP Playwright se usa cuando:

- el contenido depende de JavaScript;
- hay scroll infinito;
- se necesita abrir comentarios;
- hay navegación entre post y perfil;
- la API no entrega contexto suficiente;
- hay que verificar visualmente una fuente;
- se necesita operar una sesión real.

---

# 6. Capa 4 — Playwright Platform Workers

No se recomienda un navegador único para todo.

Debe existir un worker por plataforma:

```text
playwright-facebook-worker
playwright-instagram-worker
playwright-linkedin-worker
playwright-tiktok-worker
playwright-reddit-worker
playwright-x-worker
```

Cada worker debe tener:

```text
su propia cuenta
su propio perfil persistente
sus propias cookies
su propia cola
sus propios límites
sus propios selectores
su propia telemetría
```

## Contrato de ejecución

```json
{
  "platform": "instagram",
  "operation": "extract_public_post",
  "url": "https://...",
  "session_profile": "instagram_research_01",
  "capture": [
    "author",
    "text",
    "timestamp",
    "profile_url",
    "screenshot"
  ],
  "max_steps": 30
}
```

## Resultado normalizado

```json
{
  "platform": "instagram",
  "actor_id": "...",
  "username": "...",
  "display_name": "...",
  "profile_url": "...",
  "content_id": "...",
  "content_url": "...",
  "content_text": "...",
  "published_at": "...",
  "contact_points": [],
  "captured_at": "...",
  "evidence_artifacts": []
}
```

---

# 7. Resiliencia de extracción

## Selectores

Orden de preferencia:

```text
1. IDs o atributos estructurales
2. roles accesibles
3. atributos semánticos
4. texto estable
5. selectores CSS posicionales
```

## Versionado

Cada extractor debe registrar:

```text
extractor_name
extractor_version
platform_ui_version
captured_at
```

## Pruebas centinela

Antes de ejecutar una campaña:

```text
¿la sesión sigue activa?
¿la búsqueda devuelve resultados?
¿el selector principal existe?
¿la URL del perfil se puede resolver?
¿el extractor devuelve contenido no vacío?
```

Si falla una prueba centinela, se detiene el worker.

---

# 8. Evidence Pipe

Toda extracción debe producir evidencia trazable.

## Evidencia primaria

```text
texto exacto
URL canónica
actor
fecha publicada
fecha de captura
ID de contenido
método de acceso
extractor utilizado
```

## Evidencia secundaria

```text
captura de pantalla
fragmento HTML
metadatos visibles
historial de navegación
```

## Almacenamiento

```text
PostgreSQL → datos normalizados
MinIO → capturas, HTML útil y artefactos
```

No se debe guardar la página completa cuando solo se necesita un fragmento.

---

# 9. Normalización y deduplicación

Antes del análisis semántico:

```text
normalizar URL
normalizar username
resolver actor
extraer contribución concreta
calcular hash
buscar duplicados
```

## Claves

```text
platform_actor_id
platform_content_id
canonical_url
content_hash
```

Una persona no debe convertirse automáticamente en una identidad global entre plataformas.

---

# 10. Semantic Intelligence

El LLM analiza una contribución concreta.

## Entradas

```text
texto
contexto mínimo
plataforma
fecha
actor
fuente
```

## Salidas

```text
apparent_affinity
apparent_intention
evidence_fragments
risk_flags
recommended_action
```

## Clasificaciones

```text
CLEAR
POSSIBLE
NONE
```

## Acciones

```text
REVIEW
OBSERVE
DISCARD
```

## Reglas

```text
LLM interpreta
schema valida
normalizador repara forma
reglas determinísticas deciden admisibilidad
persona decide ingreso comercial
```

---

# 11. Human Conversion Gate

La revisión humana debe ocurrir antes de CRM, WhatsApp o contacto.

## Pantalla

Debe mostrar:

```text
publicación completa
fragmento relevante
perfil
fuente original
fecha
contactos públicos
resultado semántico
evidencias
riesgos
```

## Decisiones

```text
APPROVE_FOR_OUTREACH
OBSERVE
DISCARD
RECHECK
```

## Estados posteriores

```text
OUTREACH_DRAFTED
OUTREACH_APPROVED
FIRST_MESSAGE_SENT
RESPONDED
NO_RESPONSE
OPTED_OUT
QUALIFIED
DISQUALIFIED
```

---

# 12. Derivación al embudo

No todos los casos siguen el mismo recorrido.

## Persona con perfil social

```text
aprobación
→ acercamiento por plataforma
→ respuesta
→ landing o CRM
```

## Persona con email público pertinente

```text
aprobación
→ email revisado
→ CRM
```

## Persona que solicita información

```text
respuesta
→ landing personalizada
→ formulario
→ CRM
```

## Comunidad o proyecto

```text
relación institucional
→ CRM B2B
```

## WhatsApp

Solo cuando:

- el número fue entregado o publicado para ese propósito;
- existe una relación previa;
- la persona acepta continuar por ese canal.

---

# 13. Kiwi como plano operativo

Kiwi debe sostener la infraestructura, no tomar decisiones semánticas.

## Responsabilidades

```text
despliegues
actualizaciones
reinicios
health checks
backups
logs
secrets
monitoreo
workers
```

## No debe reemplazar

```text
cola de tareas
base de estados
policy engine
motor semántico
revisión humana
```

---

# 14. Stack propuesto

## Aplicación

```text
Python 3.12+
FastAPI
HTMX
Jinja2
Pydantic v2
SQLAlchemy 2
Alembic
```

## Datos

```text
PostgreSQL
MinIO
Redis
```

## Ejecución

```text
RQ o Dramatiq
Playwright
MCP Server
httpx
```

## Observabilidad

```text
structlog
OpenTelemetry
Sentry
Prometheus, más adelante
```

## Seguridad

```text
secret manager
perfiles cifrados
cookies fuera de la base de negocio
auditoría de acceso
backups cifrados
```

## Despliegue

```text
Docker Compose
VPS privado
workers separados
proxy reverso
Kiwi
```

---

# 15. Fases de construcción

## Fase 1 — Laboratorio Playwright

Objetivo:

```text
probar Facebook
probar Instagram
probar LinkedIn
probar TikTok
```

Entregables:

```text
matriz de acceso
capturas
selectores
bloqueos
latencia
resultados reales
```

## Fase 2 — Worker estable de una plataforma

Elegir la plataforma con mejor resultado real.

Construir:

```text
sesión persistente
cola
extractor
normalizador
evidencia
métricas
```

## Fase 3 — Integración con Lista 1

```text
extracción
→ contribución
→ evaluación
→ revisión
```

## Fase 4 — Piloto comercial

```text
1000 publicaciones
→ 100 casos relevantes
→ 20 aprobados
→ 10 contactos
→ medir respuesta
```

Las cifras son objetivos de prueba, no promesas.

## Fase 5 — Embudo completo

Solo después de validar:

```text
precisión
estabilidad
costo
respuesta
reputación
```

---

# 16. Métricas de control

## Acceso

```text
tasa de páginas abiertas
tasa de sesiones activas
CAPTCHA por 100 tareas
bloqueos por plataforma
```

## Extracción

```text
contenido válido
perfiles resueltos
contactos encontrados
duplicados
errores de selector
```

## Semántica

```text
salidas válidas
CLEAR correctos
POSSIBLE correctos
falsos positivos
falsos negativos
```

## Operación

```text
tiempo por registro
costo por candidato válido
revisión humana por candidato
mantenimiento por plataforma
```

## Embudo

```text
contactados
respondieron
opt-out
calificados
convertidos
```

---

# 17. Diferencia frente a la arquitectura anterior

La versión anterior proponía:

```text
browser
→ MCP-RADAR
→ aprobación
→ CRM / WhatsApp
```

La versión superadora propone:

```text
control de fuentes
→ planificación
→ acceso por mejor canal
→ workers aislados
→ evidencia
→ normalización
→ deduplicación
→ evaluación semántica
→ reglas
→ revisión humana
→ acercamiento
→ embudo
```

La diferencia central es que ahora existen:

- control de sesiones;
- tareas persistentes;
- recuperación de errores;
- evidencia completa;
- extractores versionados;
- deduplicación;
- métricas;
- separación entre navegación, análisis y decisión;
- rutas comerciales diferentes;
- infraestructura operable.

---

# 18. Veredicto final

La arquitectura correcta para Inlak’ech no es un simple scraper con un LLM encima.

Debe ser un sistema de inteligencia comercial conversacional capaz de:

```text
encontrar
navegar
extraer
probar
explicar
priorizar
aprobar
contactar
medir
```

MCP Playwright es una pieza central porque permite operar la web real, dinámica y autenticada.

RADAR sigue siendo el cerebro operativo porque mantiene estados, reglas, evidencia y decisiones.

Kiwi sostiene la infraestructura.

La persona conserva la aprobación de la relación.

## Fórmula final

```text
MCP Playwright ve la web.
RADAR comprende y gobierna.
La persona decide.
Kiwi mantiene todo funcionando.
```
