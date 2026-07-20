# experimento1

- Fecha UTC: `2026-07-20T00:29:16.912819+00:00`
- Fuente: `corpus`
- Corpus: `lab/corpus/semantic_lab_corpus.v1.json`
- Casos: `CASE_001, CASE_002`
- Providers: `agnes, gemma`
- Repeticiones por provider: `1`
- Total llamadas: `4`
- Prompt version: `radar-conversation-assessment/v3`
- Fallback silencioso: `false`

## Resumen

- agnes: status dominante `COMPLETED (2/2)`, errores `None (2/2)`
- gemma: status dominante `COMPLETED (2/2)`, errores `None (2/2)`

## Registros trazables

### CASE_001 · agnes · repetición 1

```json
{
  "experiment_id": "experimento1",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T00:28:00.527195+00:00",
  "finished_at": "2026-07-20T00:28:14.559954+00:00",
  "latency_ms": 14032,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Football rivalry and player comparison\",\n  \"contextual_meaning\": \"The speaker asserts that the competitive dynamic between national teams (Argentina and Portugal) is nonexistent, narrowing the conflict exclusively to the individual rivalry between two specific football players.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"Expression of a personal opinion regarding sports dynamics without any indication of interest in the organization's themes.\",\n  \"evidence_fragments\": [\n    \"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The content is strictly related to sports entertainment and does not contain any signals relevant to Inlak'ech RADAR's focus areas.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry and player comparison",
    "contextual_meaning": "The speaker asserts that the competitive dynamic between national teams (Argentina and Portugal) is nonexistent, narrowing the conflict exclusively to the individual rivalry between two specific football players.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "Expression of a personal opinion regarding sports dynamics without any indication of interest in the organization's themes.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is strictly related to sports entertainment and does not contain any signals relevant to Inlak'ech RADAR's focus areas.",
    "review_priority": 11,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T00:28:14.559639Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_001 · gemma · repetición 1

```json
{
  "experiment_id": "experimento1",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T00:28:14.560011+00:00",
  "finished_at": "2026-07-20T00:28:36.357560+00:00",
  "latency_ms": 21797,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Title: `CASE_001`\n    *   Text: `No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.` (Translation: There is no rivalry between Argentina and Portugal, only between Messi and Cristiano.)\n    *   Goal: Analyze for Inlak'ech RADAR based on specific schema.\n    *   Constraints: Single JSON object, no markdown, no commentary, specific schema version, specific enums, literal quotes for evidence.\n\n    *   The text is a comment about football (soccer) rivalry between players (Messi and Cristiano Ronaldo) and their respective countries (Argentina and Portugal).\n    *   It has absolutely nothing to do with conscious investment, regeneration, Yucatan, territory, or any of the Inlak'ech RADAR affinity domains.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: Football rivalry (Messi vs. Ronaldo).\n    *   `contextual_meaning`: The user is stating that the rivalry is personal between the athletes, not national between the countries.\n    *   `apparent_affinity`: `NONE` (No connection to the project's values).\n    *   `apparent_affinity_domains`: `[]` (Empty array).\n    *   `apparent_intention`: `NONE` (No intent related to the project).\n    *   `intention_summary`: The user is expressing an opinion about sports.\n    *   `evidence_fragments`: `[\"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"]`\n    *   `contradictions`: `[]`\n    *   `missing_context`: `[]`\n    *   `false_positive_risk`: `LOW` (It's clearly about sports).\n    *   `uncertainty`: `LOW` (The meaning is unambiguous).\n    *   `human_review_reason`: \"The conversation is about sports rivalry and has no relation to the project's affinity domains.\"\n\n    *   Valid JSON? Yes.\n    *   No markdown fences? Yes.\n    *   Schema version correct? Yes.\n    *   Enums correct? Yes.\n    *   Literal quotes? Yes.\n    *   No inferred economic/lead status? Yes.</thought>{\n\"schema_version\": \"radar-conversation-assessment/v3\",\n\"real_topic\": \"Football rivalry\",\n\"contextual_meaning\": \"The speaker is distinguishing between a national rivalry and a personal rivalry between two specific athletes, Lionel Messi and Cristiano Ronaldo.\",\n\"apparent_affinity\": \"NONE\",\n\"apparent_affinity_domains\": [],\n\"apparent_intention\": \"NONE\",\n\"intention_summary\": \"The user is sharing a personal opinion regarding sports competition.\",\n\"evidence_fragments\": [\n\"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n],\n\"contradictions\": [],\n\"missing_context\": [],\n\"false_positive_risk\": \"LOW\",\n\"uncertainty\": \"LOW\",\n\"human_review_reason\": \"The content is entirely unrelated to the project's domains, focusing instead on sports.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry",
    "contextual_meaning": "The speaker is distinguishing between a national rivalry and a personal rivalry between two specific athletes, Lionel Messi and Cristiano Ronaldo.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "NONE",
    "intention_summary": "The user is sharing a personal opinion regarding sports competition.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is entirely unrelated to the project's domains, focusing instead on sports.",
    "review_priority": 3,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T00:28:36.357469Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · agnes · repetición 1

```json
{
  "experiment_id": "experimento1",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T00:28:36.357609+00:00",
  "finished_at": "2026-07-20T00:28:46.247897+00:00",
  "latency_ms": 9890,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Speculative investment in Yucatan\",\n  \"contextual_meaning\": \"The user expresses a desire to invest in the Yucatan region but explicitly states that their goal is limited to an immediate speculative exit, rejecting long-term or non-speculative approaches.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user is actively seeking a specific type of financial transaction (immediate speculative exit) which contradicts the core values of the target framework.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán\",\n    \"solo busco una salida especulativa inmediata\"\n  ],\n  \"contradictions\": [\n    \"The explicit rejection of non-speculative development and long-term patience in favor of immediate speculative gain.\"\n  ],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user's intent is clearly defined as speculative and immediate, which stands in direct opposition to the principles of non-speculative development and strategic patience associated with the target framework.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Speculative investment in Yucatan",
    "contextual_meaning": "The user expresses a desire to invest in the Yucatan region but explicitly states that their goal is limited to an immediate speculative exit, rejecting long-term or non-speculative approaches.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user is actively seeking a specific type of financial transaction (immediate speculative exit) which contradicts the core values of the target framework.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán",
      "solo busco una salida especulativa inmediata"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [
      "The explicit rejection of non-speculative development and long-term patience in favor of immediate speculative gain."
    ],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user's intent is clearly defined as speculative and immediate, which stands in direct opposition to the principles of non-speculative development and strategic patience associated with the target framework.",
    "review_priority": 31,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T00:28:46.247723Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · gemma · repetición 1

```json
{
  "experiment_id": "experimento1",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T00:28:46.247974+00:00",
  "finished_at": "2026-07-20T00:29:16.912778+00:00",
  "latency_ms": 30664,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Goal: Analyze for Inlak'ech RADAR.\n    *   Output: Single valid JSON object.\n    *   Schema Version: \"radar-conversation-assessment/v3\".\n    *   Constraints: No markdown, no commentary, no inferred economic capacity/lead status, literal quotes for evidence, specific enums.\n\n    *   TITLE: CASE_002\n    *   TEXT: \"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\" (Translation: \"I want to invest in Yucatan, but I'm only looking for an immediate speculative exit.\")\n\n    *   `real_topic`: Investment in Yucatán.\n    *   `contextual_meaning`: The user is interested in real estate or financial investment in Yucatán specifically for short-term speculative profit (flipping).\n    *   `apparent_affinity`: NONE. The user explicitly states they want a \"speculative immediate exit,\" which contradicts the core values of Inlak'ech (which usually focus on long-term, non-speculative, regenerative development).\n    *   `apparent_affinity_domains`: []. (No alignment with the provided domains like NON_SPECULATIVE_DEVELOPMENT or LONG_TERM).\n    *   `apparent_intention`: ACTION_ORIENTED (They want to invest).\n    *   `intention_summary`: Seeking a short-term speculative investment opportunity in Yucatán.\n    *   `evidence_fragments`: [\"Quiero invertir en Yucatán\", \"solo busco una salida especulativa inmediata\"]\n    *   `contradictions`: [].\n    *   `missing_context`: [\"The specific type of asset they are looking for\", \"Their budget or timeline beyond 'immediate'\"].\n    *   `false_positive_risk`: LOW (The statement is very explicit).\n    *   `uncertainty`: LOW.\n    *   `human_review_reason`: \"The user explicitly states a desire for speculative investment, which is the opposite of the project's non-speculative philosophy.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Investment in Yucatán\"\n    *   `contextual_meaning`: \"The user is seeking a short-term financial gain through speculative investment in the Yucatán region.\"\n    *   `apparent_affinity`: \"NONE\"\n    *   `apparent_affinity_domains`: []\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"The user intends to invest in Yucatán with the sole purpose of achieving a quick speculative profit.\"\n    *   `evidence_fragments`: [\"Quiero invertir en Yucatán\", \"solo busco una salida especulativa inmediata\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Specific asset type\", \"Investment amount\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"User explicitly requests a speculative exit, which directly conflicts with the non-speculative development values of the project.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Investment in Yucatán\",\n  \"contextual_meaning\": \"The user is expressing a desire to invest in the Yucatán region specifically for the purpose of short-term speculative profit.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user is seeking an immediate speculative exit for an investment in Yucatán.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán\",\n    \"solo busco una salida especulativa inmediata\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Type of investment asset\",\n    \"Budget\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user explicitly states a goal of speculative investment, which is diametrically opposed to the project's core values of non-speculative development and long-term vision.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Investment in Yucatán",
    "contextual_meaning": "The user is expressing a desire to invest in the Yucatán region specifically for the purpose of short-term speculative profit.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user is seeking an immediate speculative exit for an investment in Yucatán.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán",
      "solo busco una salida especulativa inmediata"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Type of investment asset",
      "Budget"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user explicitly states a goal of speculative investment, which is diametrically opposed to the project's core values of non-speculative development and long-term vision.",
    "review_priority": 31,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T00:29:16.912679Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```
