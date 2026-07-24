# RADAR INLAK’ECH — RECOMENDACIÓN ESTRATÉGICA V1

**Estado:** documento de decisión interna  
**Fecha:** 20 de julio de 2026  
**Proyecto global:** Inlak’ech  
**Herramienta:** RADAR — Motor de Afinidad Conversacional e Inteligencia Comercial

---

## 1. Veredicto

RADAR debe continuar, pero con un alcance preciso:

> **RADAR debe operar como sistema de descubrimiento, interpretación y priorización de conversaciones públicas que puedan revelar afinidad presuntiva con Inlak’ech.**

No debe convertirse en un scraper universal de perfiles, ni en una herramienta de contacto automático masivo.

La secuencia recomendada es:

```text
conversación pública
→ interpretación semántica
→ candidato presuntivo
→ revisión humana
→ acercamiento prudente
→ respuesta voluntaria
→ corroboración
→ clasificación comercial
```

La prioridad inmediata sigue siendo **Lista 1**. No corresponde avanzar todavía con contacto automático, precalificación, CRM o Relaticle hasta demostrar que la detección semántica y la identificación pública funcionan con precisión suficiente.

---

## 2. Qué demostraron los experimentos

Los experimentos realizados permiten sostener cinco afirmaciones.

### 2.1 Existe suficiente materia prima pública

Se encontraron conversaciones, publicaciones, perfiles y directorios relacionados con:

- comunidades intencionales;
- ecoaldeas;
- permacultura;
- vida rural;
- proyectos regenerativos;
- cohousing;
- búsqueda de socios o integrantes;
- búsqueda de comunidades donde vivir o participar.

Por lo tanto, el problema no es la inexistencia de señales. El problema es su calidad, vigencia, verificabilidad y permiso de acceso.

### 2.2 No existe una vía única para todas las plataformas

Cada red presenta condiciones distintas:

- API pública;
- API limitada;
- acceso mediante login;
- contenido indexado pero no automatizable;
- grupos cerrados;
- términos que prohíben scraping;
- perfiles visibles pero uso comercial restringido.

Conclusión: **no debe construirse un scraper generalista**. Deben existir conectores específicos y una política ejecutable por plataforma.

### 2.3 Los registros reunidos no equivalen a candidatos verificados

Los lotes obtenidos de Permies, Bluesky, IC.org, Reddit y LinkedIn demostraron que es posible localizar cuentas y publicaciones, pero también expusieron problemas:

- mezcla de personas, organizaciones y proyectos;
- contactos antiguos;
- perfiles sin declaración literal;
- varios usuarios extraídos de un mismo hilo sin validación individual;
- publicaciones posiblemente vencidas;
- dificultad para verificar intención actual;
- fuentes que no permiten automatización comercial.

Por lo tanto, debe usarse la expresión **registro preliminar**, no candidato, hasta que se complete la evaluación y revisión.

### 2.4 El modelo semántico todavía no está validado en vivo

La skill v1.1.0, el normalizador y el reintento por formato pasaron pruebas automatizadas. Sin embargo, la ejecución viva con MiMo reveló truncamiento por `max_tokens=2048`.

La corrección a 4096 está técnicamente justificada, pero aún falta demostrar en vivo que:

```text
Caso A → CLEAR / REVIEW
Caso B → POSSIBLE / OBSERVE
Caso C → NONE / DISCARD
```

Hasta completar esa prueba, el componente semántico no debe considerarse listo para producción.

### 2.5 El contacto público no autoriza cualquier contacto

Un correo o perfil visible puede haber sido publicado para:

- voluntariado;
- inscripción a una comunidad;
- relaciones personales;
- búsqueda de trabajo;
- captación de miembros;
- consultas técnicas.

No debe suponerse automáticamente que autoriza una propuesta comercial diferente. RADAR debe conservar el contexto y propósito original del contacto.

---

## 3. Función exacta de RADAR dentro del embudo de Inlak’ech

RADAR no es el embudo completo. Es el sistema que alimenta y ordena su primera parte.

### 3.1 Etapa 1 — Descubrimiento

RADAR encuentra conversaciones públicas en fuentes permitidas.

Salida:

```text
resultado recuperado
```

Todavía no existe candidato.

### 3.2 Etapa 2 — Interpretación

El evaluador semántico analiza una intervención concreta de una cuenta pública.

Salida:

```text
conversación interpretada
```

Debe conservar evidencia literal y contexto.

### 3.3 Etapa 3 — Lista 1

Si la evaluación cumple las reglas de ingreso, la cuenta pasa a:

```text
candidato presuntivo para revisión
```

Esto no significa que la persona tenga interés en Inlak’ech. Significa únicamente que expresó algo compatible con algunas dimensiones relevantes.

### 3.4 Etapa 4 — Revisión humana

Una persona verifica:

- que la fuente sea válida;
- que la intención sea personal;
- que la cuenta siga activa;
- que la publicación sea vigente;
- que no sea marketing, turismo o especulación;
- que exista un canal de contacto pertinente;
- que no haya inferencias indebidas.

### 3.5 Etapa 5 — Acercamiento

El primer mensaje no debe vender ni clasificar. Debe abrir una conversación prudente y contextual.

El objetivo es corroborar:

```text
¿la persona realmente tiene interés en conocer Inlak’ech?
```

### 3.6 Etapa 6 — Respuesta y corroboración

Solo una respuesta voluntaria permite avanzar de afinidad presuntiva a interés corroborado.

### 3.7 Etapa 7 — Clasificación comercial

Recién aquí corresponde aplicar:

- caminos de participación;
- dimensiones del embudo;
- precalificación;
- CRM;
- Relaticle.

---

## 4. Alcance recomendado por plataforma

### 4.1 Prioridad alta

#### Bluesky

**Decisión:** primera plataforma para implementación real.

Ventajas:

- perfiles públicos;
- identificadores estables;
- API pública;
- publicaciones y respuestas estructuradas;
- menor dependencia de scraping HTML.

Uso recomendado:

```text
descubrimiento automático
+ evaluación semántica
+ revisión humana
```

No automatizar follows, respuestas o mensajes masivos.

#### Mastodon

**Decisión:** segunda plataforma.

Ventajas:

- API pública por instancia;
- perfiles y publicaciones públicas;
- comunidades temáticas.

Dificultades:

- fragmentación por servidores;
- búsquedas diferentes según instancia;
- políticas locales.

#### Discourse, Lemmy, RSS y foros públicos autorizados

**Decisión:** incorporar después de Bluesky y Mastodon.

Ventajas:

- conversaciones densas;
- estructura pública;
- RSS, JSON o API en muchos casos.

Condición: auditar cada sitio individualmente.

#### YouTube Data API

**Decisión:** viable para canales y videos seleccionados.

No sirve para buscar semánticamente todos los comentarios de YouTube. Primero deben seleccionarse videos o canales relevantes y luego analizar sus comentarios.

### 4.2 Prioridad media y condicionada

#### Permies

**Decisión:** fuente de alto valor temático, pero no integrar de manera masiva hasta revisar reglas, actualidad y forma permitida de acceso.

Los experimentos mostraron buen contenido, pero también:

- publicaciones antiguas;
- correos desactualizados;
- proyectos cerrados;
- mezcla de perfiles y roles.

#### IC.org y directorios similares

**Decisión:** crear un módulo separado para proyectos y comunidades.

No mezclar:

```text
persona que busca comunidad
```

con:

```text
comunidad que busca integrantes
```

Son entidades y recorridos comerciales diferentes.

### 4.3 Manual, API autorizada o acuerdo

#### Reddit

Alto valor conversacional, pero uso comercial automático restringido. Puede servir para investigación, corpus y revisión manual. No debe integrarse automáticamente sin autorización o acuerdo.

#### LinkedIn

No scrapear. Solo:

- revisión manual;
- enlaces aportados;
- APIs o permisos oficiales;
- contactos provenientes de actividad propia.

#### Facebook Groups e Instagram

Alto valor temático, pero acceso irregular y dependiente de login, membresía y permisos. Deben manejarse por:

- API autorizada;
- revisión manual;
- URL aportada;
- administradores o comunidades asociadas.

#### TikTok y X

No integrar por scraping HTML. Solo API, permiso escrito o revisión manual.

---

## 5. Arquitectura recomendada

No debe cambiarse el stack actual. RADAR debe evolucionar como **monolito modular**.

### 5.1 Stack

```text
Python
FastAPI
HTMX + Jinja2
Pydantic v2
SQLAlchemy + Alembic
SQLite local
PostgreSQL producción
httpx
APIs oficiales
Docker Compose
```

Redis + RQ solo cuando comiencen las búsquedas programadas o concurrentes.

### 5.2 Módulos a consolidar

```text
sources/
  registry
  platform_policy
  connectors

discovery/
  queries
  collector
  deduplication

evidence/
  contribution
  snapshot
  validator

semantics/
  assessment_v3
  normalizer
  provider_router

candidates/
  presumptive_candidate
  eligibility
  states

review/
  human_decisions

governance/
  audit
  retention
  suppression
```

### 5.3 Entidad crítica faltante

La afinidad debe evaluarse sobre la intervención concreta de una persona, no sobre todos los participantes del hilo.

Agregar o consolidar:

```text
ConversationContribution
```

Campos mínimos:

```text
conversation_id
actor_id
contribution_url
contribution_text
published_at
```

### 5.4 Separación de actores

RADAR debe distinguir:

```text
PERSON
PROJECT
COMMUNITY
ORGANIZATION
```

No deben compartir indiscriminadamente la misma Lista 1.

### 5.5 Policy Gate ejecutable

Cada conector debe consultar una política antes de operar.

Estados:

```text
SUPPORTED
CONDITIONAL
MANUAL_ONLY
NOT_SUPPORTED
```

Si una plataforma está en `MANUAL_ONLY` o `NOT_SUPPORTED`, el conector automático debe negarse a ejecutarse.

---

## 6. Qué construir ahora

### Prioridad 1 — Cerrar la prueba semántica viva

1. Centralizar `SEMANTIC_MAX_TOKENS=4096`.
2. Repetir los tres casos.
3. Confirmar que el caso inmobiliario queda fuera.
4. Registrar reintentos, truncamiento y failover.
5. Ejecutar un corpus de al menos 50 casos antes de declarar estabilidad.

### Prioridad 2 — Consolidar Lista 1 por contribución

1. Vincular evaluación a comentario o publicación concreta.
2. No crear candidato para todos los participantes del hilo.
3. Conservar evidencia literal.
4. Mantener identidad separada por plataforma.

### Prioridad 3 — Implementar Policy Gate

Crear una matriz ejecutable de plataformas antes de sumar conectores.

### Prioridad 4 — Conector real de Bluesky

Primera prueba recomendada:

```text
500 publicaciones públicas
ventana: últimos 180 días
idiomas: español e inglés
objetivo: 10 candidatos revisados y válidos
```

### Prioridad 5 — Interfaz de revisión

La pantalla debe permitir:

```text
ver conversación
ver intervención exacta
abrir perfil
abrir fuente
ver evaluación
aprobar
observar
descartar
```

### Prioridad 6 — Medición

Registrar:

- publicaciones recuperadas;
- cuentas únicas;
- perfiles accesibles;
- evaluaciones válidas;
- `INVALID_MODEL_OUTPUT`;
- reintentos;
- failovers;
- candidatos creados;
- falsos positivos;
- falsos negativos;
- tiempo de revisión;
- costo por candidato válido.

---

## 7. Qué no construir todavía

No avanzar todavía con:

- scraper universal;
- contacto automático;
- mensajes masivos;
- enriquecimiento entre plataformas;
- búsqueda de teléfonos o correos ocultos;
- inferencia de capacidad económica;
- clasificación por arquetipo antes de respuesta;
- CRM automático;
- integración con Relaticle;
- microservicios;
- Kubernetes;
- base vectorial como requisito central.

---

## 8. Criterios para aprobar la siguiente etapa

### 8.1 Evaluador semántico

Mínimos recomendados:

```text
≥95 % de salidas estructuralmente válidas
≥90 % de acuerdo con revisión humana
0 falsos CLEAR en casos inmobiliarios evidentes
```

### 8.2 Descubrimiento en Bluesky

La prueba debe demostrar:

```text
500 publicaciones revisadas
≥10 candidatos válidos
100 % con evidencia literal
100 % con perfil público accesible
≤10 % de falsos positivos después de revisión
```

### 8.3 Operación humana

El tiempo medio de revisión debe ser suficientemente bajo como para justificar el sistema. Si cada candidato exige una investigación extensa, RADAR no será económicamente viable.

### 8.4 Contacto

No activar contacto hasta definir:

- mensaje inicial;
- finalidad;
- canal permitido;
- exclusión voluntaria;
- registro de respuesta;
- reglas para no insistir.

---

## 9. Riesgos principales

| Riesgo | Dificultad |
|---|---:|
| Restricciones contractuales por plataforma | 10/10 |
| Confundir visibilidad pública con permiso comercial | 10/10 |
| Mezclar personas con proyectos | 9/10 |
| Vigencia de publicaciones y contactos | 9/10 |
| Falta de evidencia literal | 9/10 |
| Falsos positivos semánticos | 8/10 |
| Variación de modelos gratuitos | 8/10 |
| Contacto fuera del propósito original | 8/10 |
| Identidad fragmentada entre redes | 7/10 |
| Costo de revisión humana | 7/10 |
| Cambios de APIs y condiciones | 7/10 |

---

## 10. Recomendación final

La continuación más coherente y robusta es:

```text
cerrar evaluación semántica viva
→ incorporar evaluación por contribución
→ implementar Policy Gate
→ construir conector Bluesky
→ ejecutar piloto de 500 publicaciones
→ revisar 10 candidatos válidos
→ medir precisión, costo y tiempo
→ decidir segunda plataforma
```

RADAR debe ser evaluado por su capacidad de producir **pocos candidatos bien justificados**, no grandes cantidades de nombres.

El producto correcto no es:

```text
una base de datos de personas scrapeadas
```

Es:

```text
un sistema trazable que detecta conversaciones públicas relevantes,
explica por qué una cuenta merece revisión
y permite iniciar una relación de forma prudente y voluntaria.
```

### Decisión recomendada

**Continuar RADAR.**  
**Mantener Lista 1 como alcance activo.**  
**No activar contacto automático.**  
**Usar Bluesky como primer conector real.**  
**Separar personas de proyectos.**  
**Exigir evidencia literal y revisión humana.**  
**Avanzar a corroboración y embudo comercial solo después de demostrar precisión y viabilidad operativa.**


---

## 11. Decisión de arquitectura: incorporación plena de MCP Playwright

Se corrige la recomendación anterior.

**MCP Playwright pasa a formar parte activa de la estrategia técnica de RADAR.**

No se lo tratará como herramienta marginal ni excepcional. Se lo utilizará como capa operativa principal para explorar, navegar, verificar y extraer información visible en plataformas web cuando la API no alcance o no exista.

### 11.1 Función dentro de RADAR

```text
consulta de búsqueda
→ navegador automatizado con Playwright MCP
→ navegación de resultados
→ apertura de publicaciones y perfiles
→ extracción de contenido visible
→ normalización
→ evaluación semántica
→ revisión humana
→ Lista 1
```

### 11.2 Capacidades que se incorporan

MCP Playwright se utilizará para:

- abrir plataformas dinámicas;
- ejecutar JavaScript;
- recorrer resultados;
- hacer scroll;
- abrir publicaciones completas;
- leer conversaciones y comentarios visibles;
- acceder a perfiles visibles;
- verificar vigencia de enlaces;
- capturar evidencia;
- registrar nombre, contacto público y URL;
- asistir la revisión humana;
- probar de extremo a extremo la interfaz HTMX de RADAR;
- repetir búsquedas y recorridos de manera controlada.

### 11.3 Plataformas a probar

La estrategia incluirá pruebas reales, una por una, en:

```text
Facebook
Instagram
TikTok
LinkedIn
X
Reddit
YouTube
Bluesky
Mastodon
Permies
IC.org
otros foros y directorios relevantes
```

No se descartará una plataforma por anticipado. Cada una será evaluada mediante experimentos reproducibles.

### 11.4 Criterio operativo

RADAR decidirá por evidencia empírica:

- qué contenido puede abrirse;
- qué contenido puede recorrerse;
- cuántos resultados pueden recuperarse;
- qué selectores son estables;
- cuánto tarda cada búsqueda;
- cuándo aparecen bloqueos;
- qué información pública puede extraerse;
- qué porcentaje de resultados termina en candidato útil.

### 11.5 Registro obligatorio por experimento

Cada prueba con Playwright debe guardar:

```text
plataforma
consulta utilizada
fecha y hora
sesión autenticada o pública
páginas recorridas
resultados visibles
resultados extraídos
bloqueos encontrados
CAPTCHA o login requerido
tiempo total
errores
selectores utilizados
capturas o evidencia
candidatos producidos
```

### 11.6 Arquitectura corregida

```text
Source Registry
→ Playwright MCP / API / RSS / carga manual
→ extractor específico por plataforma
→ normalizador común
→ deduplicación
→ evaluación semántica
→ evidencia
→ revisión humana
→ Lista 1
```

Playwright MCP no reemplaza los conectores específicos: los ejecuta o complementa cuando la fuente requiere navegador real.

### 11.7 Módulos recomendados

```text
app/browser/
  session_manager.py
  playwright_mcp_client.py
  navigation.py
  extraction.py
  evidence_capture.py
  rate_control.py

app/sources/connectors/
  facebook_playwright.py
  instagram_playwright.py
  tiktok_playwright.py
  linkedin_playwright.py
  x_playwright.py
  reddit_playwright.py
  generic_web_playwright.py
```

Cada conector deberá devolver el mismo contrato normalizado.

### 11.8 Primera fase de ejecución

1. Instalar y conectar MCP Playwright al entorno de desarrollo.
2. Crear un laboratorio de navegación separado del flujo productivo.
3. Probar las plataformas prioritarias una por una.
4. Recolectar diez registros verificables por plataforma cuando sea posible.
5. Documentar exactamente dónde falla cada plataforma.
6. Convertir los recorridos que funcionen en conectores repetibles.
7. Integrarlos a Lista 1.
8. Medir rendimiento y estabilidad antes de programar ejecuciones periódicas.

### 11.9 Nueva decisión final

**RADAR avanzará con MCP Playwright como capacidad central de exploración y captación web.**

La herramienta se evaluará por resultados reales y no por restricciones supuestas de antemano.

El criterio será:

```text
probar
→ medir
→ documentar
→ estabilizar
→ integrar
```

No se limitará anticipadamente su alcance técnico. Las decisiones posteriores se tomarán con evidencia producida por los experimentos.
