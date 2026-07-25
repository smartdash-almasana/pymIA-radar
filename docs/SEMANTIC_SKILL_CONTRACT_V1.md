# Contrato semántico V1 — Inlak'ech Affinity

Este contrato define cómo RADAR interpreta conversaciones públicas para detectar afinidad semántica aparente con Inlak'ech. La regla central es estable: el LLM interpreta el sentido, RADAR valida, registra y gobierna, y la persona decide.

## Autoridad y alcance

- **Skill ID:** `inlakech_affinity_v1`
- **Versión:** `1.0.0`
- **Estado:** `VERIFIED`
- **Archivo normativo:** `config/semantic_skills/inlakech_affinity_v1.yaml`
- **Contrato técnico validado:** `app.schemas.assessment_v3.ConversationAssessmentV3Result`

Este contrato no habilita contacto automático, publicación automática, precalificación, scoring comercial ni transferencia a CRM. Solo define interpretación semántica, validación posterior y revisión humana.

## Identidad de Inlak'ech

Inlak'ech es un proyecto de regeneración territorial, inversión consciente, comunidad, territorio, belleza útil, respeto cultural y construcción de largo plazo en Yucatán. RADAR existe para encontrar conversaciones públicas que puedan merecer revisión humana por compatibilidad semántica aparente con esa identidad.

## Qué es y qué no es afinidad

**Afinidad semántica aparente** es compatibilidad provisional entre el sentido completo de una conversación pública y la identidad de Inlak'ech.

No es:

- coincidencia de palabras aisladas;
- afinidad personal confirmada;
- consentimiento;
- autorización de contacto;
- capacidad económica declarada;
- calificación comercial;
- diagnóstico psicológico o financiero;
- asignación de arquetipo.

## Niveles de afinidad

| Nivel | Significado |
| --- | --- |
| `NONE` | El sentido completo no intersecta sustantivamente con Inlak'ech. |
| `POSSIBLE` | Hay compatibilidad plausible, pero falta evidencia o contexto. |
| `CLEAR` | Hay compatibilidad clara respaldada por evidencia literal. |

`CLEAR` exige revisión humana. No convierte a la persona en lead.

## Intención aparente

| Nivel | Significado |
| --- | --- |
| `NONE` | No hay dirección de acción relevante. |
| `THEMATIC_SYMPATHY` | Hay valoración temática sin voluntad observable de actuar. |
| `EXPLORATION` | La persona pregunta, compara, evalúa o busca información. |
| `ACTION_ORIENTED` | La persona expresa un paso concreto o voluntad explícita de avanzar. |

La intención aparente no confirma interés en Inlak'ech.

## Evidencia literal

Toda evaluación completada debe sostenerse con fragmentos literales continuos tomados del título, texto o contexto de la conversación. RADAR puede normalizar espacios para validar presencia, pero no puede aceptar paráfrasis, traducciones, correcciones ni fragmentos discontinuos como evidencia.

La evidencia solo sostiene la lectura semántica. No prueba consentimiento, capacidad, calificación ni autorización.

## Ironía y lenguaje coloquial

El LLM debe interpretar ironía, metáforas, bromas, citas, crítica y lenguaje coloquial desde el sentido completo. Si una frase usa una palabra compatible con Inlak'ech pero el contexto real indica fútbol, burla, rechazo, ruido o un tema distinto, la afinidad debe bajar y el riesgo de falso positivo debe subir.

## Inferencias permitidas y prohibidas

Permitidas en el contrato V3:

- `real_topic`
- `contextual_meaning`
- `apparent_affinity`
- `apparent_affinity_domains`
- `apparent_intention`
- `intention_summary`
- `evidence_fragments`
- `rejected_evidence_fragments`
- `contradictions`
- `missing_context`
- `false_positive_risk`
- `uncertainty`
- `human_review_reason`
- `review_priority`
- `recommended_review_action`

Prohibidas:

- `probable_archetype`
- `declared_capacity`
- `capital_band`
- `participation_path`
- `qualification_status`
- `commercial_lead_score`
- `contact_authorization`
- `consent_inference`
- `psychological_diagnosis`
- `financial_capacity_from_public_profile`

## Riesgo de falso positivo

| Nivel | Uso |
| --- | --- |
| `LOW` | Sentido, evidencia y contexto están alineados. |
| `MEDIUM` | El tema puede encajar, pero falta intención o contexto. |
| `HIGH` | La coincidencia aparente surge de tema ajeno, ironía, ruido o léxico aislado. |

RADAR registra y muestra el riesgo. No lo convierte en acción externa.

## Prioridad de revisión

`review_priority` es propuesta por el LLM desde el contexto completo. RADAR solo aplica límites de coherencia posteriores: rango 0–100, evidencia literal válida, enums estables y revisión humana obligatoria ante failover.

No hay fórmula ponderada, regex, scoring determinístico ni prioridad calculada por palabras aisladas.

## Proveedores y failover

- **API:** OpenCode Zen
- **Primario:** MiMo 2.5 Free
- **Revisor condicional:** Nemotron 3 Ultra Free

Reglas:

1. MiMo interpreta como primario.
2. Nemotron revisa solo si se activan condiciones semánticas de ambigüedad, riesgo, contradicción o contexto insuficiente.
3. Si MiMo falla, Nemotron actúa una sola vez como primario de contingencia.
4. Ese caso se registra como `EXPLICIT_PROVIDER_FAILOVER` y exige revisión humana.
5. Si ambos fallan, se registra `ALL_PROVIDERS_UNAVAILABLE`.
6. Ante salida con formato inválido se permite un único reintento con la misma entrada. No se reintenta ante `SemanticProviderError`. El máximo total es de dos llamadas al runner; un segundo fallo de formato se registra como `INVALID_MODEL_OUTPUT`.

## Casos de calibración

### Positivo

Una conversación donde alguien busca una comunidad regenerativa de largo plazo en Yucatán, con intención de participar y no solo invertir, puede producir `CLEAR`, `EXPLORATION` o `ACTION_ORIENTED`, `LOW` y `REVIEW`, siempre con evidencia literal.

### Ambiguo

Una conversación sobre turismo sustentable en Yucatán sin intención de participar puede producir `POSSIBLE`, `THEMATIC_SYMPATHY`, `MEDIUM` y `OBSERVE`.

### Negativo obligatorio

Conversación futbolística:

> Argentina and France played a crazy final; Spain has talent too, but Messi is still the best.

Resultado esperado:

```json
{
  "real_topic": "fútbol internacional",
  "apparent_affinity": "NONE",
  "apparent_intention": "NONE",
  "false_positive_risk": "HIGH",
  "recommended_review_action": "DISCARD"
}
```

La interpretación surge del sentido completo: fútbol internacional. No de palabras aisladas.

## Contrato JSON V3

El contrato V3 permanece tipado en Python. El YAML no crea enums dinámicos. Los dominios YAML deben coincidir exactamente con `AffinityDomain`.

Campos del resultado V3:

```text
schema_version
assessment_status
real_topic
contextual_meaning
apparent_affinity
apparent_affinity_domains
apparent_intention
intention_summary
evidence_fragments
rejected_evidence_fragments
contradictions
missing_context
false_positive_risk
uncertainty
human_review_reason
review_priority
recommended_review_action
semantic_engine
model_name
safe_error_code
provisional
human_review_required
created_at
```

## Regla LLM/RADAR/humano

```text
El LLM interpreta el sentido.
RADAR valida, registra y gobierna.
La persona decide.
```

Ninguna salida semántica autoriza contacto, publicación, precalificación o decisión comercial automática.
