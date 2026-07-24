**Sistema de descubrimiento, evaluación y revisión de conversaciones públicas**

| **Precio fijo**    | **USD 2.400**                               |
|--------------------|---------------------------------------------|
| **Plazo estimado** | 6 a 8 semanas calendario                    |
| **Modalidad**      | Desarrollo sobre la base existente de RADAR |

> **Definición del producto**  
> RADAR MVP no es un CRM ni un sistema de mensajería. Es la primera pieza operativa del futuro sistema de atracción de Inlak’ech: descubre señales públicas, conserva evidencia, evalúa afinidad, permite revisión humana y entrega oportunidades aprobadas en un formato preparado para integrarse posteriormente con un CRM.

# 1. Resumen ejecutivo

RADAR Inlak’ech será una herramienta propia para localizar, organizar y evaluar conversaciones públicas relacionadas con comunidades regenerativas, ecoaldeas, permacultura, vida comunitaria, inversión consciente, colaboración y afinidades compatibles con Inlak’ech.

El MVP aprovechará la base de software ya existente y concentrará el desarrollo en demostrar que el sistema puede ejecutar un flujo completo y auditable:

**descubrir → extraer evidencia → evaluar → revisar → aprobar → preparar para CRM**

> **Precio y plazo acordados**  
> Costo fijo total: USD 2.400. Plazo estimado: 6 a 8 semanas calendario, sujeto a disponibilidad de cuentas de prueba, accesos y decisiones funcionales del cliente.

# 2. Problema que resuelve

Las señales de personas, proyectos y grupos potencialmente afines se encuentran dispersas en redes, foros y espacios digitales. La búsqueda manual consume tiempo, produce listas incompletas y rara vez conserva la evidencia que explica por qué una cuenta merece atención.

RADAR MVP sistematiza esta primera etapa mediante:

- búsqueda y navegación en fuentes seleccionadas;
- captura de publicación, autor, perfil, enlace y contexto;
- deduplicación de resultados;
- evaluación semántica de afinidad e intención;
- revisión humana obligatoria;
- salida estructurada para una futura integración con CRM.

# 3. Alcance funcional del MVP

## 3.1 Descubrimiento y acceso

- Conectores ya disponibles o de bajo costo técnico: API pública, HTTP, RSS, JSON y carga manual de URL.
- Laboratorio MCP Playwright sobre Facebook, Instagram, LinkedIn y TikTok para medir acceso real, contenido visible, estabilidad y bloqueos.
- Estabilización de un worker Playwright para la plataforma que demuestre mejor comportamiento durante el laboratorio.
- Posibilidad de mantener otros accesos como experimentales o manuales cuando no alcancen estabilidad suficiente.

## 3.2 Evidencia y normalización

- Registro de texto relevante, URL canónica, autor visible, perfil, fecha y momento de captura.
- Captura visual o artefacto equivalente cuando sea necesario para auditoría.
- Normalización de cuentas y publicaciones.
- Deduplicación por identificadores, URL y huella de contenido.

## 3.3 Evaluación semántica

- Clasificación de afinidad aparente: CLEAR, POSSIBLE o NONE.
- Acción sugerida: REVIEW, OBSERVE o DISCARD.
- Extracción de fragmentos de evidencia.
- Detección de falsos positivos frecuentes: turismo, inmobiliaria convencional, marketing verde, entusiasmo genérico o menciones sin intención.

## 3.4 Revisión humana

- Bandeja HTMX con conversación, evidencia, perfil, fuente y evaluación.
- Acciones: aprobar, observar, descartar y reabrir la fuente original.
- Ningún caso avanza hacia el futuro embudo sin aprobación humana.

## 3.5 Preparación para CRM

- Contrato de datos versionado ApprovedOpportunityV1.
- Identificador único de oportunidad.
- Estados READY_FOR_CRM, EXPORTED, TRANSFER_CONFIRMED y TRANSFER_FAILED.
- Exportación JSON y CSV.
- Endpoint interno de lectura.
- Campo external_crm_id reservado para la integración futura.
- Documentación del contrato y pruebas de validación.

# 4. Qué conseguirá el cliente

- Una herramienta propia, documentada y desplegable.
- Un flujo completo desde la conversación pública hasta una oportunidad aprobada.
- Evidencia trazable para explicar cada decisión.
- Una bandeja operativa para priorizar el trabajo humano.
- Información real sobre qué plataformas y consultas producen mejores resultados.
- Un contrato técnico preparado para conectar más adelante CRM, WhatsApp Business, Relaticle, formularios, afiliados, colaboradores o inversores.
- Un piloto que demuestre idoneidad técnica y operativa del MVP.

# 5. Qué no incluye ni debe prometerse

- No garantiza una cantidad fija de candidatos ni conversiones comerciales.
- No garantiza acceso permanente a todas las redes si cambian sus interfaces, sesiones o reglas.
- No incluye evasión agresiva de CAPTCHAs, bloqueos o mecanismos de seguridad.
- No extrae correos, teléfonos ni información privada no visible.
- No incluye el desarrollo del CRM.
- No incluye integración activa con un CRM específico.
- No incluye mensajería automática, WhatsApp, email marketing ni seguimiento comercial.
- No incluye sincronización bidireccional, campañas, scoring comercial final ni cierre de oportunidades.
- No convierte automáticamente una publicación en interés real por Inlak’ech; ese interés deberá corroborarse posteriormente.

# 6. Demostración de idoneidad del MVP

La aceptación no se basará en prometer un número comercial de candidatos, sino en demostrar que RADAR funciona de extremo a extremo, produce evidencia verificable y entrega oportunidades técnicamente utilizables.

| **Prueba** | **Criterio mínimo** | **Evidencia de aceptación** |
|---|---|---|
| Flujo completo | Una campaña real ejecutada de extremo a extremo | Resultados visibles en la bandeja |
| Extracción | Registros válidos en al menos dos tipos de fuente; uno mediante Playwright o navegador controlado | Texto, autor, URL y fecha de captura |
| Trazabilidad | 100% de los casos aprobados con fuente y evidencia | URL y fragmento conservados |
| Deduplicación | Pruebas focales sin duplicación de casos conocidos | Tests y demostración |
| Semántica | ≥95% de salidas estructuralmente válidas en el corpus de aceptación | Reporte de ejecución |
| Acuerdo humano | ≥80% de concordancia sobre un corpus acordado de casos claros | Matriz modelo/revisor |
| Anti-patrones | Casos inmobiliarios, turísticos o promocionales evidentes no deben clasificarse como CLEAR | Casos de prueba y resultados |
| CRM-ready | 100% de oportunidades aprobadas válidas contra ApprovedOpportunityV1 | JSON/CSV y schema validation |
| Interfaz | Aprobar, observar, descartar y abrir fuente sin errores bloqueantes | Prueba funcional |

Estos criterios demuestran idoneidad técnica. La productividad comercial se medirá posteriormente mediante tasa de respuesta, costo por oportunidad y conversiones.

# 7. Sección técnica

## 7.1 Arquitectura

**Discovery Orchestrator → Access Router → Evidence Pipe → Semantic Intelligence → Human Review → ApprovedOpportunityV1**

## 7.2 Stack

- Python 3.12+, FastAPI, Pydantic y SQLAlchemy.
- HTMX y Jinja2 para la interfaz.
- SQLite durante desarrollo y PostgreSQL para despliegue estable si el entorno lo requiere.
- MCP Playwright para navegación y extracción controlada.
- Docker Compose para instalación.
- Redis y cola de tareas únicamente cuando sean necesarios para el worker estabilizado; no se incorporarán componentes sin uso demostrado.

## 7.3 Principios técnicos

- Monolito modular sobre el RADAR existente.
- Separación entre navegación, interpretación, reglas y decisión humana.
- Credenciales y cookies fuera de la base comercial.
- Extractores versionados y errores clasificados.
- Pruebas unitarias, focales y piloto real.
- Contrato de salida independiente del CRM futuro.

# 8. Plan de implementación

| **Etapa** | **Trabajo principal** | **Duración estimada** |
|---|---|---|
| 1 | Cierre semántico y criterios de aceptación | 1 semana |
| 2 | Modelo de tareas, evidencia y deduplicación | 1 semana |
| 3 | Laboratorio MCP Playwright multiplataforma | 1 a 1,5 semanas |
| 4 | Worker estabilizado e integración con Lista 1 | 1,5 semanas |
| 5 | Bandeja de revisión y estados | 1 semana |
| 6 | Contrato ApprovedOpportunityV1 y exportaciones | 0,5 a 1 semana |
| 7 | Piloto, correcciones, documentación y entrega | 1 semana |

Plazo total estimado: 6 a 8 semanas calendario. Las etapas pueden solaparse. El calendario se suspende cuando falten accesos, cuentas de prueba o decisiones del cliente.

# 9. Presupuesto

> **Costo fijo total del RADAR MVP**  
> USD 2.400. El importe cubre exclusivamente el alcance definido en este documento.

## 9.1 Esquema de pagos

| **Hito** | **Porcentaje** | **Importe** |
|---|---:|---:|
| Inicio y reserva de calendario | 30% | USD 720 |
| Laboratorio Playwright y flujo de tareas operativo | 30% | USD 720 |
| Flujo completo con revisión y salida CRM-ready | 25% | USD 600 |
| Piloto aprobado y entrega final | 15% | USD 360 |

## 9.2 Garantía

Treinta días corridos desde la aceptación para corregir errores reproducibles del código entregado. No cubre cambios de terceros, nuevas restricciones, modificaciones de APIs, bloqueos de cuentas ni cambios de alcance.

## 9.3 Costos operativos posteriores

El precio de desarrollo no incluye VPS, dominio, almacenamiento, proxies, cuentas, consumo de APIs ni modelos de IA. Como referencia operativa inicial, se recomienda prever entre USD 50 y USD 200 mensuales, según volumen y proveedores elegidos.

El mantenimiento posterior no está incluido. Se cotizará después del piloto, cuando exista información real sobre frecuencia de cambios, bloqueos y carga operativa.

# 10. Responsabilidades del cliente

- Proporcionar cuentas de prueba y accesos legítimos cuando una plataforma lo requiera.
- Definir regiones, idiomas, perfiles prioritarios y consultas iniciales.
- Asignar una persona para revisión y validación de casos.
- Proveer o autorizar el entorno de despliegue.
- Responder decisiones funcionales dentro de 48 horas hábiles.
- Aceptar que el rendimiento de plataformas externas puede cambiar.

# 11. Propiedad y entrega

Con el pago completo, el cliente recibe el código desarrollado dentro del alcance, configuraciones, pruebas, documentación técnica y guía operativa. Las bibliotecas, servicios y modelos de terceros conservan sus licencias y condiciones.

# 12. Segunda etapa y conexión con CRM

RADAR MVP quedará preparado para integrarse con un CRM, pero la conexión efectiva se realizará en una segunda contratación cuando se defina el producto de destino.

La segunda etapa podrá incluir:

- adaptador para HubSpot, Zoho, Odoo, Relaticle u otro CRM;
- sincronización de contactos y oportunidades;
- webhooks reales y confirmación de entrega;
- mensajería por plataforma, email o WhatsApp Business;
- segmentación por colaborador, inversor, afiliado, proveedor o comunidad;
- seguimiento, nutrición y métricas de conversión.

No se fija ahora un precio para esta etapa porque dependerá del CRM elegido, volumen, canales, automatizaciones y reglas comerciales.

# 13. Conclusión

> **Compromiso del MVP**  
> Por USD 2.400, RADAR deberá demostrar idoneidad como herramienta de descubrimiento y filtrado: ejecutar búsquedas reales, conservar evidencia, evaluar afinidad, permitir revisión humana y producir oportunidades aprobadas válidas para una futura conexión con CRM.

La aceptación del MVP no dependerá de prometer ventas o una cantidad fija de candidatos. Dependerá de que el flujo técnico funcione, sea trazable, produzca resultados revisables y deje una salida estable para continuar construyendo el sistema operativo de Inlak’ech.