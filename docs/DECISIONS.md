# Registro de decisiones

## D-001 — Solución dedicada

Se construye para un solo cliente. Se pospone cualquier arquitectura SaaS.

## D-002 — Descubrimiento reutilizado

Se reutiliza last30days-skill. No se reconstruye su lógica sin una causa técnica demostrada.

## D-003 — CRM reutilizado

Se reutiliza Relaticle. No se construye un CRM propio.

## D-004 — Aplicación monolítica modular

FastAPI + Jinja/HTMX + PostgreSQL en un único repositorio.

## D-005 — Revisión humana obligatoria

El sistema no contacta ni publica automáticamente.

## D-006 — Clasificación híbrida

Filtro determinístico más modelo estructurado, siempre con evidencia.

## D-007 — Infraestructura simple

El desarrollo local puede ejecutarse sin Docker con Python, FastAPI y una base aislada para pruebas. Docker Compose queda como opción recomendada para empaquetado reproducible, validación de PostgreSQL en contenedor y despliegue posterior en una única VM.

La ausencia o demora de Docker no bloquea el desarrollo funcional ni el cierre de la baseline local.

## D-008 — Embudo humano de descubrimiento

RADAR mantiene un único repositorio e incorpora explícitamente un embudo de descubrimiento entre la afinidad semántica aparente y la precalificación.

La conversación pública solo permite detectar afinidad e intención aparentes. La afinidad personal, las motivaciones y cualquier hipótesis de arquetipo requieren contacto y diálogo humano. La precalificación comienza únicamente después de afinidad revelada, voluntad de continuar y consentimiento explícito.

Documento rector: `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`.

## D-009 — Gobierno de agentes de desarrollo

Codex se reserva para auditorías y cambios transversales de alto riesgo. OpenCode con DeepSeek V4 Flash se utiliza para tareas acotadas y bien especificadas. Ningún agente puede redefinir el producto, ampliar alcance ni convertir decisiones conceptuales no aprobadas en código productivo.


## D-010 — Aprobación de la arquitectura técnica de descubrimiento

Se aprueban las decisiones `DTI-01` a `DTI-08` documentadas en `docs/RADAR_TECHNICAL_IMPACT_AUDIT_2026-07-19.md`:

1. `DiscoveryCandidate` será el único objeto mínimo de persona operativa del primer corte.
2. Se creará `ConversationAssessmentV3`; `SemanticAssessmentV2` permanecerá como histórico.
3. El fallback semántico será cerrado: una caída del LLM no promocionará conversaciones mediante palabras clave.
4. Se incorporarán migraciones versionadas antes de modificar relaciones entre tablas existentes.
5. Se separarán estado de conversación, estado de descubrimiento y resultado de cualificación.
6. `EngagementEvent` se reutilizará y recibirá referencia nullable al candidato para compatibilidad histórica.
7. La primera hipótesis humana de arquetipo se almacenará en `DiscoveryOutcome`; no se creará todavía una tabla separada.
8. Se conservará la interfaz actual y se reorganizará progresivamente, sin frontend nuevo.

Quedan aprobadas:

```text
docs/specs/002A_conversation_assessment_v3.md
docs/specs/003B_discovery_domain_implementation.md
```

Orden obligatorio:

```text
SPEC-002A → VERIFIED
→ SPEC-003B puede pasar a IMPLEMENTING
```

No se autoriza implementar ambas especificaciones simultáneamente ni mezclar sus cambios en un único lote.
