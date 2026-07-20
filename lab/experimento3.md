# experimento3

- Fecha UTC: `2026-07-20T01:13:37.263414+00:00`
- Fuente: `corpus`
- Corpus: `lab/corpus/semantic_lab_corpus.v1.json`
- Casos: `CASE_001, CASE_002, CASE_003, CASE_004, CASE_005`
- Providers: `agnes, gemma`
- Repeticiones por provider: `3`
- Total llamadas: `30`
- Prompt version: `radar-conversation-assessment/v3`
- Fallback silencioso: `false`

## Resumen

- agnes: status dominante `COMPLETED (15/15)`, errores `None (15/15)`
- gemma: status dominante `COMPLETED (15/15)`, errores `None (15/15)`

## Registros trazables

### CASE_001 · agnes · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:04:02.864264+00:00",
  "finished_at": "2026-07-20T01:04:50.873241+00:00",
  "latency_ms": 48008,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Football rivalry and player comparison\",\n  \"contextual_meaning\": \"The speaker asserts that the traditional national team rivalry between Argentina and Portugal is nonexistent, suggesting instead that the competitive narrative is centered on the individual rivalry between two specific players, Lionel Messi and Cristiano Ronaldo.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"Expression of a personal opinion regarding sports dynamics and player legacies without any indication of interest in the RADAR topics.\",\n  \"evidence_fragments\": [\n    \"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The content is purely related to football and sports commentary. There is no semantic overlap with the defined affinity domains such as conscious investment, territory, or community regeneration.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry and player comparison",
    "contextual_meaning": "The speaker asserts that the traditional national team rivalry between Argentina and Portugal is nonexistent, suggesting instead that the competitive narrative is centered on the individual rivalry between two specific players, Lionel Messi and Cristiano Ronaldo.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "Expression of a personal opinion regarding sports dynamics and player legacies without any indication of interest in the RADAR topics.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is purely related to football and sports commentary. There is no semantic overlap with the defined affinity domains such as conscious investment, territory, or community regeneration.",
    "review_priority": 11,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:04:50.872944Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_001 · agnes · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:04:50.873280+00:00",
  "finished_at": "2026-07-20T01:04:58.190959+00:00",
  "latency_ms": 7317,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Football rivalry and player comparison\",\n  \"contextual_meaning\": \"The speaker asserts that the traditional national team rivalry between Argentina and Portugal is nonexistent, suggesting instead that the competitive narrative is centered on the individual rivalry between two specific players, Lionel Messi and Cristiano Ronaldo.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"Expression of a personal opinion regarding sports dynamics and player legacies without any indication of interest in the RADAR topics.\",\n  \"evidence_fragments\": [\n    \"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The content is purely related to football and sports commentary. There is no semantic overlap with the defined affinity domains such as conscious investment, territory, or community regeneration.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry and player comparison",
    "contextual_meaning": "The speaker asserts that the traditional national team rivalry between Argentina and Portugal is nonexistent, suggesting instead that the competitive narrative is centered on the individual rivalry between two specific players, Lionel Messi and Cristiano Ronaldo.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "Expression of a personal opinion regarding sports dynamics and player legacies without any indication of interest in the RADAR topics.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is purely related to football and sports commentary. There is no semantic overlap with the defined affinity domains such as conscious investment, territory, or community regeneration.",
    "review_priority": 11,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:04:58.190861Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_001 · agnes · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:04:58.190998+00:00",
  "finished_at": "2026-07-20T01:05:06.528139+00:00",
  "latency_ms": 8337,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Football rivalry and player comparison\",\n  \"contextual_meaning\": \"The speaker asserts that the traditional national team rivalry between Argentina and Portugal is nonexistent, suggesting instead that the competitive narrative is centered on the individual rivalry between two specific players, Lionel Messi and Cristiano Ronaldo.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"Expression of a personal opinion regarding sports dynamics and player legacies without any indication of interest in the RADAR topics.\",\n  \"evidence_fragments\": [\n    \"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The content is purely related to football and sports commentary. There is no semantic overlap with the defined affinity domains such as conscious investment, territory, or community regeneration.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry and player comparison",
    "contextual_meaning": "The speaker asserts that the traditional national team rivalry between Argentina and Portugal is nonexistent, suggesting instead that the competitive narrative is centered on the individual rivalry between two specific players, Lionel Messi and Cristiano Ronaldo.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "Expression of a personal opinion regarding sports dynamics and player legacies without any indication of interest in the RADAR topics.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is purely related to football and sports commentary. There is no semantic overlap with the defined affinity domains such as conscious investment, territory, or community regeneration.",
    "review_priority": 11,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:05:06.528027Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_001 · gemma · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:05:06.528213+00:00",
  "finished_at": "2026-07-20T01:05:28.406515+00:00",
  "latency_ms": 21878,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Title: `CASE_001`\n    *   Text: `No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.` (Translation: There is no rivalry between Argentina and Portugal, only between Messi and Cristiano.)\n    *   Goal: Analyze for Inlak'ech RADAR based on specific schema.\n    *   Constraints: Single JSON object, no markdown, no commentary, specific schema version, specific enums, literal quotes for evidence.\n\n    *   The text is a comment about football (soccer) rivalries between players (Messi and Ronaldo) and their respective countries.\n    *   It has absolutely nothing to do with conscious investment, regeneration, Yucatan, territory, or any of the Inlak'ech RADAR affinity domains.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: Football rivalry (Messi vs. Cristiano Ronaldo).\n    *   `contextual_meaning`: The speaker is distinguishing between a national rivalry and a personal rivalry between two athletes.\n    *   `apparent_affinity`: `NONE` (No connection to the project's values).\n    *   `apparent_affinity_domains`: `[]`\n    *   `apparent_intention`: `NONE`\n    *   `intention_summary`: The user is expressing an opinion about sports.\n    *   `evidence_fragments`: [\"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"]\n    *   `contradictions`: `[]`\n    *   `missing_context`: `[]`\n    *   `false_positive_risk`: `LOW` (It's clearly about sports).\n    *   `uncertainty`: `LOW`\n    *   `human_review_reason`: \"The conversation is about sports (football) and has no relevance to the project's affinity domains.\"\n\n    *   Valid JSON? Yes.\n    *   No markdown fences? Yes.\n    *   Schema version correct? Yes.\n    *   Enums correct? Yes.\n    *   Literal quotes? Yes.\n    *   No inferred economic/lead status? Yes.</thought>{\n\"schema_version\": \"radar-conversation-assessment/v3\",\n\"real_topic\": \"Football rivalry\",\n\"contextual_meaning\": \"The speaker is stating that the rivalry exists between individual players (Messi and Cristiano Ronaldo) rather than between their respective nations (Argentina and Portugal).\",\n\"apparent_affinity\": \"NONE\",\n\"apparent_affinity_domains\": [],\n\"apparent_intention\": \"NONE\",\n\"intention_summary\": \"The user is sharing a personal opinion regarding sports rivalries.\",\n\"evidence_fragments\": [\n\"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n],\n\"contradictions\": [],\n\"missing_context\": [],\n\"false_positive_risk\": \"LOW\",\n\"uncertainty\": \"LOW\",\n\"human_review_reason\": \"The content is entirely unrelated to the project's domains, focusing exclusively on sports.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry",
    "contextual_meaning": "The speaker is stating that the rivalry exists between individual players (Messi and Cristiano Ronaldo) rather than between their respective nations (Argentina and Portugal).",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "NONE",
    "intention_summary": "The user is sharing a personal opinion regarding sports rivalries.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is entirely unrelated to the project's domains, focusing exclusively on sports.",
    "review_priority": 3,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:05:28.406385Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_001 · gemma · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:05:28.406553+00:00",
  "finished_at": "2026-07-20T01:05:50.745194+00:00",
  "latency_ms": 22338,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Title: `CASE_001`\n    *   Text: `No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.` (Translation: There is no rivalry between Argentina and Portugal, only between Messi and Cristiano.)\n    *   Goal: Analyze for Inlak'ech RADAR based on specific schema.\n    *   Constraints: Single JSON object, no markdown, no commentary, specific schema version, specific enums, literal quotes for evidence.\n\n    *   Topic: Football (Soccer) rivalry.\n    *   Context: Comparing national team rivalry vs. individual player rivalry (Messi vs. Ronaldo).\n    *   Affinity to Inlak'ech RADAR domains (Conscious Investment, Legacy, Regeneration, etc.): None. This is a sports comment.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: Football rivalry (Messi vs. Cristiano Ronaldo).\n    *   `contextual_meaning`: The user is stating that the rivalry is personal between two athletes rather than national between Argentina and Portugal.\n    *   `apparent_affinity`: `NONE` (No connection to the specific domains).\n    *   `apparent_affinity_domains`: `[]`\n    *   `apparent_intention`: `NONE`\n    *   `intention_summary`: The user is expressing an opinion about sports.\n    *   `evidence_fragments`: [\"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"]\n    *   `contradictions`: `[]`\n    *   `missing_context`: `[\"The broader conversation or reason for this statement is unknown.\"]`\n    *   `false_positive_risk`: `LOW` (It's clearly about sports).\n    *   `uncertainty`: `LOW`\n    *   `human_review_reason`: \"The text is a comment about sports and has no relation to the project's affinity domains.\"\n\n    *   Valid JSON? Yes.\n    *   No markdown fences? Yes.\n    *   Schema version correct? Yes.\n    *   Enums correct? Yes.\n    *   Literal quotes? Yes.\n    *   No inferred economic/lead status? Yes.</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Football rivalry\",\n  \"contextual_meaning\": \"The speaker is distinguishing between a national rivalry and an individual rivalry between two athletes, Messi and Cristiano Ronaldo.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"NONE\",\n  \"intention_summary\": \"The user is expressing a personal opinion regarding sports rivalries.\",\n  \"evidence_fragments\": [\n    \"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"The context of the conversation leading to this statement is missing.\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The content is strictly related to sports and contains no indicators of affinity with the project's domains.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry",
    "contextual_meaning": "The speaker is distinguishing between a national rivalry and an individual rivalry between two athletes, Messi and Cristiano Ronaldo.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "NONE",
    "intention_summary": "The user is expressing a personal opinion regarding sports rivalries.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The context of the conversation leading to this statement is missing."
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is strictly related to sports and contains no indicators of affinity with the project's domains.",
    "review_priority": 3,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:05:50.745085Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_001 · gemma · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_001",
  "input_text": "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:05:50.745231+00:00",
  "finished_at": "2026-07-20T01:06:13.353767+00:00",
  "latency_ms": 22608,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Title: `CASE_001`\n    *   Text: `No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.` (Translation: There is no rivalry between Argentina and Portugal, only between Messi and Cristiano.)\n    *   Goal: Analyze for Inlak'ech RADAR based on specific schema.\n    *   Constraints: Single JSON object, no markdown, no commentary, specific schema version, specific enums, literal quotes for evidence.\n\n    *   Topic: Football (Soccer) rivalry.\n    *   Context: Comparing national team rivalry vs. individual player rivalry (Messi vs. Ronaldo).\n    *   Affinity to Inlak'ech RADAR domains (Conscious Investment, Legacy, Regeneration, etc.): None. This is a sports comment.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: Football rivalry between players vs nations.\n    *   `contextual_meaning`: The user is expressing an opinion that the rivalry is personal between two athletes rather than nationalistic.\n    *   `apparent_affinity`: `NONE` (No connection to the specific domains).\n    *   `apparent_affinity_domains`: `[]`\n    *   `apparent_intention`: `NONE` (No intent related to the project).\n    *   `intention_summary`: The user is making a comment about sports.\n    *   `evidence_fragments`: [\"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"]\n    *   `contradictions`: `[]`\n    *   `missing_context`: `[\"The broader conversation or reason for this statement is unknown.\"]`\n    *   `false_positive_risk`: `LOW` (It's clearly about sports).\n    *   `uncertainty`: `LOW`\n    *   `human_review_reason`: \"The text is a comment about sports rivalry and has no relation to the project's affinity domains.\"\n\n    *   JSON object? Yes.\n    *   No markdown fences? Yes.\n    *   `schema_version` correct? Yes.\n    *   Enums correct? Yes.\n    *   Literal quotes? Yes.\n    *   No inferred economic/lead status? Yes.\n    *   `human_review_reason` non-empty string? Yes.</thought>{\n\"schema_version\": \"radar-conversation-assessment/v3\",\n\"real_topic\": \"Football rivalry\",\n\"contextual_meaning\": \"The user is stating that the rivalry exists between individual players (Messi and Cristiano Ronaldo) rather than between the nations of Argentina and Portugal.\",\n\"apparent_affinity\": \"NONE\",\n\"apparent_affinity_domains\": [],\n\"apparent_intention\": \"NONE\",\n\"intention_summary\": \"The user is expressing a personal opinion regarding sports rivalry.\",\n\"evidence_fragments\": [\n\"No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano.\"\n],\n\"contradictions\": [],\n\"missing_context\": [\n\"The context of the conversation leading to this statement is missing.\"\n],\n\"false_positive_risk\": \"LOW\",\n\"uncertainty\": \"LOW\",\n\"human_review_reason\": \"The content is strictly related to sports and contains no indicators of affinity with the project's domains.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 1,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Football rivalry",
    "contextual_meaning": "The user is stating that the rivalry exists between individual players (Messi and Cristiano Ronaldo) rather than between the nations of Argentina and Portugal.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "NONE",
    "intention_summary": "The user is expressing a personal opinion regarding sports rivalry.",
    "evidence_fragments": [
      "No hay rivalidad entre Argentina y Portugal, solo entre Messi y Cristiano."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The context of the conversation leading to this statement is missing."
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The content is strictly related to sports and contains no indicators of affinity with the project's domains.",
    "review_priority": 3,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:06:13.353669Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · agnes · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:06:13.353822+00:00",
  "finished_at": "2026-07-20T01:06:22.524411+00:00",
  "latency_ms": 9170,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Speculative investment in Yucatán\",\n  \"contextual_meaning\": \"The user expresses interest in investing in the Yucatán region but explicitly states a desire for immediate speculative returns, rejecting long-term or non-speculative approaches.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user is seeking immediate financial gain through speculation in Yucatán real estate or assets, which contradicts the principles of non-speculative development and strategic patience associated with Inlak'ech.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\"\n  ],\n  \"contradictions\": [\n    \"The explicit rejection of non-speculative models ('solo busco una salida especulativa') directly opposes the 'NON_SPECULATIVE_DEVELOPMENT' domain.\"\n  ],\n  \"missing_context\": [\n    \"No information on the specific asset class, timeline beyond 'immediate', or prior engagement with sustainable practices.\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The statement is a direct contradiction of core values (speculation vs. non-speculative development). No further review needed to determine lack of affinity, but confirmation of the specific investment vehicle may be useful for record-keeping.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Speculative investment in Yucatán",
    "contextual_meaning": "The user expresses interest in investing in the Yucatán region but explicitly states a desire for immediate speculative returns, rejecting long-term or non-speculative approaches.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user is seeking immediate financial gain through speculation in Yucatán real estate or assets, which contradicts the principles of non-speculative development and strategic patience associated with Inlak'ech.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [
      "The explicit rejection of non-speculative models ('solo busco una salida especulativa') directly opposes the 'NON_SPECULATIVE_DEVELOPMENT' domain."
    ],
    "missing_context": [
      "No information on the specific asset class, timeline beyond 'immediate', or prior engagement with sustainable practices."
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The statement is a direct contradiction of core values (speculation vs. non-speculative development). No further review needed to determine lack of affinity, but confirmation of the specific investment vehicle may be useful for record-keeping.",
    "review_priority": 28,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:06:22.524309Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · agnes · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:06:22.524450+00:00",
  "finished_at": "2026-07-20T01:06:29.995668+00:00",
  "latency_ms": 7471,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Speculative investment in Yucatán\",\n  \"contextual_meaning\": \"The user expresses interest in investing in the Yucatán region but explicitly states a desire for immediate speculative returns, rejecting long-term or non-speculative approaches.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user is seeking immediate financial gain through speculation in Yucatán real estate or assets, which contradicts the principles of non-speculative development and strategic patience associated with Inlak'ech.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\"\n  ],\n  \"contradictions\": [\n    \"The explicit rejection of non-speculative models ('solo busco una salida especulativa') directly opposes the 'NON_SPECULATIVE_DEVELOPMENT' domain.\"\n  ],\n  \"missing_context\": [\n    \"No information on the specific asset class, timeline beyond 'immediate', or prior engagement with sustainable practices.\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The statement is a direct contradiction of core values (speculation vs. non-speculative development). No further review needed to determine lack of affinity, but confirmation of the specific investment vehicle may be useful for record-keeping.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Speculative investment in Yucatán",
    "contextual_meaning": "The user expresses interest in investing in the Yucatán region but explicitly states a desire for immediate speculative returns, rejecting long-term or non-speculative approaches.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user is seeking immediate financial gain through speculation in Yucatán real estate or assets, which contradicts the principles of non-speculative development and strategic patience associated with Inlak'ech.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [
      "The explicit rejection of non-speculative models ('solo busco una salida especulativa') directly opposes the 'NON_SPECULATIVE_DEVELOPMENT' domain."
    ],
    "missing_context": [
      "No information on the specific asset class, timeline beyond 'immediate', or prior engagement with sustainable practices."
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The statement is a direct contradiction of core values (speculation vs. non-speculative development). No further review needed to determine lack of affinity, but confirmation of the specific investment vehicle may be useful for record-keeping.",
    "review_priority": 28,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:06:29.995559Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · agnes · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:06:29.995702+00:00",
  "finished_at": "2026-07-20T01:06:37.544543+00:00",
  "latency_ms": 7548,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Speculative investment in Yucatán\",\n  \"contextual_meaning\": \"The user expresses interest in investing in the Yucatán region but explicitly states a desire for immediate speculative returns, rejecting long-term or non-speculative approaches.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user is seeking immediate financial gain through speculation in Yucatán real estate or assets, which contradicts the principles of non-speculative development and strategic patience associated with Inlak'ech.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\"\n  ],\n  \"contradictions\": [\n    \"The explicit rejection of non-speculative models ('solo busco una salida especulativa') directly opposes the 'NON_SPECULATIVE_DEVELOPMENT' domain.\"\n  ],\n  \"missing_context\": [\n    \"No information on the specific asset class, timeline beyond 'immediate', or prior engagement with sustainable practices.\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The statement is a direct contradiction of core values (speculation vs. non-speculative development). No further review needed to determine lack of affinity, but confirmation of the specific investment vehicle may be useful for record-keeping.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Speculative investment in Yucatán",
    "contextual_meaning": "The user expresses interest in investing in the Yucatán region but explicitly states a desire for immediate speculative returns, rejecting long-term or non-speculative approaches.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user is seeking immediate financial gain through speculation in Yucatán real estate or assets, which contradicts the principles of non-speculative development and strategic patience associated with Inlak'ech.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [
      "The explicit rejection of non-speculative models ('solo busco una salida especulativa') directly opposes the 'NON_SPECULATIVE_DEVELOPMENT' domain."
    ],
    "missing_context": [
      "No information on the specific asset class, timeline beyond 'immediate', or prior engagement with sustainable practices."
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The statement is a direct contradiction of core values (speculation vs. non-speculative development). No further review needed to determine lack of affinity, but confirmation of the specific investment vehicle may be useful for record-keeping.",
    "review_priority": 28,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:06:37.544455Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · gemma · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:06:37.544590+00:00",
  "finished_at": "2026-07-20T01:07:11.977226+00:00",
  "latency_ms": 34432,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Task: Analyze for Inlak'ech RADAR.\n    *   Output: Single valid JSON object.\n    *   Constraints: No markdown, no commentary, specific schema version, specific enums, literal quotes for evidence, no inference of economic capacity/lead status/etc.\n\n    *   TITLE: `CASE_002`\n    *   TEXT: `Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.` (Translation: \"I want to invest in Yucatan, but I'm only looking for an immediate speculative exit.\")\n\n    *   `real_topic`: Investment in Yucatán.\n    *   `contextual_meaning`: The user is interested in investing in Yucatán but explicitly states their goal is short-term speculation (flipping/quick profit).\n    *   `apparent_affinity`: The user's goal is \"speculative immediate exit,\" which is the opposite of the RADAR values (like NON_SPECULATIVE_DEVELOPMENT, LONG_TERM, STRATEGIC_PATIENCE). Therefore, affinity is `NONE`.\n    *   `apparent_affinity_domains`: `[]` (Empty, as they are explicitly seeking speculation).\n    *   `apparent_intention`: `EXPLORATION` (They are expressing a desire to invest, but the nature of the intent is contrary to the project's values). Actually, \"Quiero invertir\" is an action-oriented statement, but since it's purely speculative, it doesn't align with the *desired* action-oriented intent of the project. However, the prompt asks for the *user's* intention. They are stating a clear goal. I'll mark it as `ACTION_ORIENTED` because they want to invest, but the summary will clarify it's speculative. Wait, looking at the enums: `THEMATIC_SYMPATHY`, `EXPLORATION`, `ACTION_ORIENTED`. They are stating a specific goal. I'll use `ACTION_ORIENTED`.\n    *   `intention_summary`: The user wants to make a short-term speculative investment in Yucatán.\n    *   `evidence_fragments`: `[\"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\"]`\n    *   `contradictions`: `[]`\n    *   `missing_context`: `[\"The user does not specify the type of asset or the amount they wish to invest.\"]`\n    *   `false_positive_risk`: `LOW` (The statement is very explicit).\n    *   `uncertainty`: `LOW` (The statement is clear).\n    *   `human_review_reason`: \"User explicitly states a desire for immediate speculative exit, which contradicts the core values of non-speculative development and long-term vision.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Investment in Yucatán\"\n    *   `contextual_meaning`: \"The user is seeking a short-term financial gain through speculative investment in the Yucatán region.\"\n    *   `apparent_affinity`: \"NONE\"\n    *   `apparent_affinity_domains`: []\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"Seeking an immediate speculative exit for an investment in Yucatán.\"\n    *   `evidence_fragments`: [\"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Specific investment vehicle or budget\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"The user explicitly expresses a speculative intent, which is diametrically opposed to the project's non-speculative and long-term principles.\"\n\n    *   Single JSON object? Yes.\n    *   No markdown fences? Yes.\n    *   Schema version correct? Yes.\n    *   Enums correct? Yes.\n    *   Literal quotes? Yes.\n    *   No forbidden inferences? Yes.</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Investment in Yucatán\",\n  \"contextual_meaning\": \"The user is interested in investing in the Yucatán region but explicitly states that their goal is a short-term speculative profit.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user wants to engage in a speculative investment with an immediate exit strategy.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"The specific type of investment or asset class the user is interested in.\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user explicitly declares a speculative intent, which is the opposite of the project's core values regarding non-speculative development and long-term commitment.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Investment in Yucatán",
    "contextual_meaning": "The user is interested in investing in the Yucatán region but explicitly states that their goal is a short-term speculative profit.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user wants to engage in a speculative investment with an immediate exit strategy.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata."
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The specific type of investment or asset class the user is interested in."
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user explicitly declares a speculative intent, which is the opposite of the project's core values regarding non-speculative development and long-term commitment.",
    "review_priority": 28,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:07:11.977146Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · gemma · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:07:11.977254+00:00",
  "finished_at": "2026-07-20T01:07:39.445790+00:00",
  "latency_ms": 27468,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Goal: Analyze for Inlak'ech RADAR.\n    *   Output: Single valid JSON object.\n    *   Constraints: No markdown, no commentary, specific schema version, specific enums, literal quotes for evidence, no inference of economic capacity/lead status/etc.\n\n    *   TITLE: CASE_002\n    *   TEXT: \"Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.\" (Translation: I want to invest in Yucatan, but I'm only looking for an immediate speculative exit.)\n\n    *   `real_topic`: Investment in Yucatán.\n    *   `contextual_meaning`: The user is interested in investing in Yucatán but explicitly states their goal is short-term speculation (flipping/quick profit).\n    *   `apparent_affinity`: NONE. (The user explicitly seeks \"speculative immediate exit,\" which contradicts the core values of Inlak'ech RADAR, such as NON_SPECULATIVE_DEVELOPMENT and LONG_TERM).\n    *   `apparent_affinity_domains`: []. (No alignment with the provided domains).\n    *   `apparent_intention`: ACTION_ORIENTED. (They want to invest).\n    *   `intention_summary`: Seeking a short-term speculative investment opportunity in Yucatán.\n    *   `evidence_fragments`: [\"Quiero invertir en Yucatán\", \"solo busco una salida especulativa inmediata\"]\n    *   `contradictions`: [].\n    *   `missing_context`: [\"Specific budget\", \"Type of asset preferred\"].\n    *   `false_positive_risk`: LOW. (The statement is very explicit).\n    *   `uncertainty`: LOW.\n    *   `human_review_reason`: The user explicitly states a desire for speculative investment, which is the opposite of the project's philosophy.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Investment in Yucatán\"\n    *   `contextual_meaning`: \"The user expresses a desire to invest in the Yucatán region specifically for the purpose of immediate financial speculation.\"\n    *   `apparent_affinity`: \"NONE\"\n    *   `apparent_affinity_domains`: []\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"The user is looking for a quick, speculative return on investment in Yucatán.\"\n    *   `evidence_fragments`: [\"Quiero invertir en Yucatán\", \"solo busco una salida especulativa inmediata\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Investment amount\", \"Specific location or asset type\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"User explicitly requests a speculative exit, which directly conflicts with the non-speculative development values of the project.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Investment in Yucatán\",\n  \"contextual_meaning\": \"The user is interested in investing in Yucatán but explicitly states that their goal is a short-term speculative profit.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user is seeking an immediate speculative investment opportunity in Yucatán.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán\",\n    \"solo busco una salida especulativa inmediata\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Investment budget\",\n    \"Preferred asset type\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user explicitly identifies as a speculative investor, which is diametrically opposed to the project's core values of non-speculative development and long-term vision.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Investment in Yucatán",
    "contextual_meaning": "The user is interested in investing in Yucatán but explicitly states that their goal is a short-term speculative profit.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user is seeking an immediate speculative investment opportunity in Yucatán.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán",
      "solo busco una salida especulativa inmediata"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Investment budget",
      "Preferred asset type"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user explicitly identifies as a speculative investor, which is diametrically opposed to the project's core values of non-speculative development and long-term vision.",
    "review_priority": 31,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:07:39.445546Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_002 · gemma · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_002",
  "input_text": "Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:07:39.445854+00:00",
  "finished_at": "2026-07-20T01:08:10.134284+00:00",
  "latency_ms": 30688,
  "raw_output": "<thought>*   Input: A short conversation snippet.\n    *   Title: `CASE_002`\n    *   Text: `Quiero invertir en Yucatán, pero solo busco una salida especulativa inmediata.` (Translation: \"I want to invest in Yucatan, but I'm only looking for an immediate speculative exit.\")\n    *   Goal: Analyze for Inlak'ech RADAR based on specific schema.\n\n    *   `real_topic`: Investment in Yucatán.\n    *   `contextual_meaning`: The user is interested in investing in the region but explicitly states their goal is short-term speculation (flipping/quick profit).\n    *   `apparent_affinity`: The user's goal (speculation) is the opposite of the RADAR values (e.g., NON_SPECULATIVE_DEVELOPMENT, LONG_TERM). Therefore, affinity is `NONE`.\n    *   `apparent_affinity_domains`: Empty array `[]` because the intent is speculative.\n    *   `apparent_intention`: The user is stating a desire to act (`ACTION_ORIENTED`), but for a purpose that contradicts the project's values. However, in terms of the *type* of intent, they are looking for an investment opportunity. I'll mark it as `ACTION_ORIENTED` because they \"want to invest,\" but the summary will clarify the nature.\n    *   `intention_summary`: The user is seeking a short-term speculative investment opportunity in Yucatán.\n    *   `evidence_fragments`: [\"Quiero invertir en Yucatán\", \"solo busco una salida especulativa inmediata\"]\n    *   `contradictions`: None within the text, but the intent contradicts the project's philosophy.\n    *   `missing_context`: Budget, specific area of interest, timeline for \"immediate\".\n    *   `false_positive_risk`: `LOW` (The statement is very explicit).\n    *   `uncertainty`: `LOW` (The statement is very explicit).\n    *   `human_review_reason`: The user explicitly states a desire for speculative investment, which is contrary to the project's non-speculative principles.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Investment in Yucatán\"\n    *   `contextual_meaning`: \"The user expresses a desire to invest in the Yucatán region specifically for the purpose of achieving a quick speculative profit.\"\n    *   `apparent_affinity`: \"NONE\"\n    *   `apparent_affinity_domains`: []\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"Seeking a short-term speculative investment exit in Yucatán.\"\n    *   `evidence_fragments`: [\"Quiero invertir en Yucatán\", \"solo busco una salida especulativa inmediata\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Investment budget\", \"Specific location preferences\", \"Definition of 'immediate' timeframe\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"User explicitly identifies as a speculative investor, which is diametrically opposed to the project's core values of non-speculative development and long-term commitment.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Investment in Yucatán\",\n  \"contextual_meaning\": \"The user is interested in investing in the Yucatán region, but explicitly states that their sole objective is a quick speculative profit.\",\n  \"apparent_affinity\": \"NONE\",\n  \"apparent_affinity_domains\": [],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user is seeking a short-term speculative investment opportunity with an immediate exit strategy.\",\n  \"evidence_fragments\": [\n    \"Quiero invertir en Yucatán\",\n    \"solo busco una salida especulativa inmediata\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Investment budget\",\n    \"Specific area of interest\",\n    \"Timeline for 'immediate' exit\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user explicitly declares a speculative intent, which is the opposite of the project's non-speculative and long-term values.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 2,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Investment in Yucatán",
    "contextual_meaning": "The user is interested in investing in the Yucatán region, but explicitly states that their sole objective is a quick speculative profit.",
    "apparent_affinity": "NONE",
    "apparent_affinity_domains": [],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user is seeking a short-term speculative investment opportunity with an immediate exit strategy.",
    "evidence_fragments": [
      "Quiero invertir en Yucatán",
      "solo busco una salida especulativa inmediata"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Investment budget",
      "Specific area of interest",
      "Timeline for 'immediate' exit"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user explicitly declares a speculative intent, which is the opposite of the project's non-speculative and long-term values.",
    "review_priority": 31,
    "recommended_review_action": "DISCARD",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": false,
    "created_at": "2026-07-20T01:08:10.134204Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_003 · agnes · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_003",
  "input_text": "Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:08:10.134324+00:00",
  "finished_at": "2026-07-20T01:08:19.739660+00:00",
  "latency_ms": 9605,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Expression of preference for regenerative projects without intent to participate\",\n  \"contextual_meaning\": \"The speaker acknowledges a positive sentiment towards regenerative initiatives but explicitly states a lack of desire to engage or take part in them.\",\n  \"apparent_affinity\": \"POSSIBLE\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\"\n  ],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"The user expresses thematic sympathy for regeneration but clearly indicates no intention to act or participate.\",\n  \"evidence_fragments\": [\n    \"Me gustan los proyectos regenerativos\",\n    \"aunque no estoy buscando participar en ninguno\"\n  ],\n  \"contradictions\": [\n    \"Affinity for the domain is present, but intention to participate is explicitly absent.\"\n  ],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Explicit statement of non-participation despite expressed interest in the theme requires verification of whether this is a firm boundary or a temporary stance.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 3,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Expression of preference for regenerative projects without intent to participate",
    "contextual_meaning": "The speaker acknowledges a positive sentiment towards regenerative initiatives but explicitly states a lack of desire to engage or take part in them.",
    "apparent_affinity": "POSSIBLE",
    "apparent_affinity_domains": [
      "REGENERATION"
    ],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "The user expresses thematic sympathy for regeneration but clearly indicates no intention to act or participate.",
    "evidence_fragments": [
      "Me gustan los proyectos regenerativos",
      "aunque no estoy buscando participar en ninguno"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [
      "Affinity for the domain is present, but intention to participate is explicitly absent."
    ],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Explicit statement of non-participation despite expressed interest in the theme requires verification of whether this is a firm boundary or a temporary stance.",
    "review_priority": 62,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:08:19.739571Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_003 · agnes · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_003",
  "input_text": "Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:08:19.739689+00:00",
  "finished_at": "2026-07-20T01:08:27.059976+00:00",
  "latency_ms": 7320,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Expression of preference for regenerative projects without intent to participate\",\n  \"contextual_meaning\": \"The speaker acknowledges a positive sentiment towards regenerative initiatives but explicitly states a lack of desire to engage or take part in them.\",\n  \"apparent_affinity\": \"POSSIBLE\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\"\n  ],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"The user expresses thematic sympathy for regeneration but clearly indicates no intention to act or participate.\",\n  \"evidence_fragments\": [\n    \"Me gustan los proyectos regenerativos\",\n    \"aunque no estoy buscando participar en ninguno\"\n  ],\n  \"contradictions\": [\n    \"Affinity for the domain is present, but intention to participate is explicitly absent.\"\n  ],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Explicit statement of non-participation despite expressed interest in the theme requires verification of whether this is a firm boundary or a temporary stance.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 3,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Expression of preference for regenerative projects without intent to participate",
    "contextual_meaning": "The speaker acknowledges a positive sentiment towards regenerative initiatives but explicitly states a lack of desire to engage or take part in them.",
    "apparent_affinity": "POSSIBLE",
    "apparent_affinity_domains": [
      "REGENERATION"
    ],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "The user expresses thematic sympathy for regeneration but clearly indicates no intention to act or participate.",
    "evidence_fragments": [
      "Me gustan los proyectos regenerativos",
      "aunque no estoy buscando participar en ninguno"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [
      "Affinity for the domain is present, but intention to participate is explicitly absent."
    ],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Explicit statement of non-participation despite expressed interest in the theme requires verification of whether this is a firm boundary or a temporary stance.",
    "review_priority": 62,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:08:27.059872Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_003 · agnes · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_003",
  "input_text": "Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:08:27.060014+00:00",
  "finished_at": "2026-07-20T01:08:34.432054+00:00",
  "latency_ms": 7372,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Expression of preference for regenerative projects without intent to participate\",\n  \"contextual_meaning\": \"The speaker acknowledges a positive sentiment towards regenerative initiatives but explicitly states a lack of desire to engage or take part in them.\",\n  \"apparent_affinity\": \"POSSIBLE\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\"\n  ],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"The user expresses thematic sympathy for regeneration but clearly indicates no intention to act or participate.\",\n  \"evidence_fragments\": [\n    \"Me gustan los proyectos regenerativos\",\n    \"aunque no estoy buscando participar en ninguno\"\n  ],\n  \"contradictions\": [\n    \"Affinity for the domain is present, but intention to participate is explicitly absent.\"\n  ],\n  \"missing_context\": [],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Explicit statement of non-participation despite expressed interest in the theme requires verification of whether this is a firm boundary or a temporary stance.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 3,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Expression of preference for regenerative projects without intent to participate",
    "contextual_meaning": "The speaker acknowledges a positive sentiment towards regenerative initiatives but explicitly states a lack of desire to engage or take part in them.",
    "apparent_affinity": "POSSIBLE",
    "apparent_affinity_domains": [
      "REGENERATION"
    ],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "The user expresses thematic sympathy for regeneration but clearly indicates no intention to act or participate.",
    "evidence_fragments": [
      "Me gustan los proyectos regenerativos",
      "aunque no estoy buscando participar en ninguno"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [
      "Affinity for the domain is present, but intention to participate is explicitly absent."
    ],
    "missing_context": [],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Explicit statement of non-participation despite expressed interest in the theme requires verification of whether this is a firm boundary or a temporary stance.",
    "review_priority": 62,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:08:34.431981Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_003 · gemma · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_003",
  "input_text": "Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:08:34.432089+00:00",
  "finished_at": "2026-07-20T01:09:01.625263+00:00",
  "latency_ms": 27193,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Task: Analyze for Inlak'ech RADAR.\n    *   Output: Single valid JSON object.\n    *   Constraints: No markdown, no commentary, specific schema version, specific enums, literal quotes for evidence, no inference of economic/lead status.\n\n    *   TITLE: CASE_003\n    *   TEXT: \"Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.\" (Translation: \"I like regenerative projects, although I am not looking to participate in any.\")\n\n    *   `real_topic`: Regenerative projects.\n    *   `contextual_meaning`: The user expresses a positive sentiment towards regenerative projects but explicitly states they are not seeking active participation.\n    *   `apparent_affinity`: `POSSIBLE` (They like them, but aren't acting on it).\n    *   `apparent_affinity_domains`: `REGENERATION`.\n    *   `apparent_intention`: `THEMATIC_SYMPATHY` (They like the idea/theme, but explicitly deny action-oriented intent).\n    *   `intention_summary`: The user likes the concept of regenerative projects but is not looking to join or participate in one.\n    *   `evidence_fragments`: [\"Me gustan los proyectos regenerativos\", \"no estoy buscando participar en ninguno\"]\n    *   `contradictions`: [] (The statement is consistent: likes the idea, doesn't want to participate).\n    *   `missing_context`: [\"Why the user is not looking to participate\", \"What specific types of regenerative projects they like\"]\n    *   `false_positive_risk`: `LOW` (The statement is very direct).\n    *   `uncertainty`: `LOW` (The meaning is clear).\n    *   `human_review_reason`: \"User explicitly states a lack of desire to participate despite liking the theme.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Regenerative projects\"\n    *   `contextual_meaning`: \"The user expresses an appreciation for regenerative projects while explicitly stating they are not seeking to participate in any.\"\n    *   `apparent_affinity`: \"POSSIBLE\"\n    *   `apparent_affinity_domains`: [\"REGENERATION\"]\n    *   `apparent_intention`: \"THEMATIC_SYMPATHY\"\n    *   `intention_summary`: \"The user likes the concept of regeneration but explicitly declines active participation.\"\n    *   `evidence_fragments`: [\"Me gustan los proyectos regenerativos\", \"no estoy buscando participar en ninguno\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"The reason for not wanting to participate\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"User explicitly states they are not looking to participate, creating a clear boundary between thematic interest and action.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Regenerative projects\",\n  \"contextual_meaning\": \"The user expresses a positive sentiment toward the concept of regenerative projects but explicitly states they are not seeking to participate in any.\",\n  \"apparent_affinity\": \"POSSIBLE\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\"\n  ],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"The user likes the idea of regenerative projects but explicitly denies any intention to participate.\",\n  \"evidence_fragments\": [\n    \"Me gustan los proyectos regenerativos\",\n    \"no estoy buscando participar en ninguno\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"The reason why the user is not looking to participate\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user explicitly states a lack of desire to participate despite their thematic interest.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 3,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Regenerative projects",
    "contextual_meaning": "The user expresses a positive sentiment toward the concept of regenerative projects but explicitly states they are not seeking to participate in any.",
    "apparent_affinity": "POSSIBLE",
    "apparent_affinity_domains": [
      "REGENERATION"
    ],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "The user likes the idea of regenerative projects but explicitly denies any intention to participate.",
    "evidence_fragments": [
      "Me gustan los proyectos regenerativos",
      "no estoy buscando participar en ninguno"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The reason why the user is not looking to participate"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user explicitly states a lack of desire to participate despite their thematic interest.",
    "review_priority": 62,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:09:01.625188Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_003 · gemma · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_003",
  "input_text": "Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:09:01.625292+00:00",
  "finished_at": "2026-07-20T01:09:28.621150+00:00",
  "latency_ms": 26995,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Task: Analyze for Inlak'ech RADAR.\n    *   Output: Single valid JSON object.\n    *   Constraints: No markdown, no commentary, specific schema version, specific enums, literal quotes for evidence, no inference of economic/lead status.\n\n    *   TITLE: CASE_003\n    *   TEXT: \"Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.\" (Translation: \"I like regenerative projects, although I am not looking to participate in any.\")\n\n    *   `real_topic`: Interest in regenerative projects.\n    *   `contextual_meaning`: The user expresses a general liking for regenerative projects but explicitly states they are not seeking active participation.\n    *   `apparent_affinity`: `POSSIBLE` (They like the concept, but aren't acting on it).\n    *   `apparent_affinity_domains`: `REGENERATION`.\n    *   `apparent_intention`: `THEMATIC_SYMPATHY` (They like the idea, but explicitly deny `ACTION_ORIENTED` or `EXPLORATION` intent).\n    *   `intention_summary`: The user expresses appreciation for regenerative projects while explicitly stating they are not looking to participate.\n    *   `evidence_fragments`: [\"Me gustan los proyectos regenerativos\", \"no estoy buscando participar en ninguno\"]\n    *   `contradictions`: [] (The statement is consistent: likes the idea, doesn't want to join).\n    *   `missing_context`: [\"Why the user is not looking to participate\", \"What specific types of regenerative projects they like\"]\n    *   `false_positive_risk`: `LOW` (The statement is very direct).\n    *   `uncertainty`: `LOW` (The meaning is clear).\n    *   `human_review_reason`: \"User explicitly states they are not looking to participate despite liking the theme.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Regenerative projects\"\n    *   `contextual_meaning`: \"The user expresses a general appreciation for regenerative projects but explicitly clarifies that they are not seeking to participate in any at this time.\"\n    *   `apparent_affinity`: \"POSSIBLE\"\n    *   `apparent_affinity_domains`: [\"REGENERATION\"]\n    *   `apparent_intention`: \"THEMATIC_SYMPATHY\"\n    *   `intention_summary`: \"The user likes the concept of regeneration but explicitly declines active participation.\"\n    *   `evidence_fragments`: [\"Me gustan los proyectos regenerativos\", \"no estoy buscando participar en ninguno\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"The reason for not wanting to participate\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"User explicitly states they are not looking to participate despite liking the theme.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Regenerative projects\",\n  \"contextual_meaning\": \"The user expresses a general appreciation for regenerative projects but explicitly clarifies that they are not seeking to participate in any at this time.\",\n  \"apparent_affinity\": \"POSSIBLE\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\"\n  ],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"The user likes the concept of regeneration but explicitly declines active participation.\",\n  \"evidence_fragments\": [\n    \"Me gustan los proyectos regenerativos\",\n    \"no estoy buscando participar en ninguno\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"The reason for not wanting to participate\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"User explicitly states they are not looking to participate despite liking the theme.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 3,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Regenerative projects",
    "contextual_meaning": "The user expresses a general appreciation for regenerative projects but explicitly clarifies that they are not seeking to participate in any at this time.",
    "apparent_affinity": "POSSIBLE",
    "apparent_affinity_domains": [
      "REGENERATION"
    ],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "The user likes the concept of regeneration but explicitly declines active participation.",
    "evidence_fragments": [
      "Me gustan los proyectos regenerativos",
      "no estoy buscando participar en ninguno"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The reason for not wanting to participate"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "User explicitly states they are not looking to participate despite liking the theme.",
    "review_priority": 62,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:09:28.621070Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_003 · gemma · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_003",
  "input_text": "Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:09:28.621176+00:00",
  "finished_at": "2026-07-20T01:09:54.671869+00:00",
  "latency_ms": 26050,
  "raw_output": "<thought>*   Input: A short conversation/text.\n    *   Task: Analyze for Inlak'ech RADAR.\n    *   Output: Single valid JSON object.\n    *   Schema Version: \"radar-conversation-assessment/v3\".\n    *   Constraints: No markdown, no commentary, no inferred economic/lead status, literal quotes for evidence, specific enums.\n\n    *   TITLE: CASE_003\n    *   TEXT: \"Me gustan los proyectos regenerativos, aunque no estoy buscando participar en ninguno.\" (Translation: \"I like regenerative projects, although I am not looking to participate in any.\")\n\n    *   `real_topic`: Regenerative projects.\n    *   `contextual_meaning`: The user expresses an appreciation for regenerative projects but explicitly states they are not seeking active participation at this time.\n    *   `apparent_affinity`: `POSSIBLE` (They like them, but aren't acting on it).\n    *   `apparent_affinity_domains`: `REGENERATION`.\n    *   `apparent_intention`: `THEMATIC_SYMPATHY` (They like the idea/theme, but explicitly deny action-oriented intent).\n    *   `intention_summary`: The user expresses a general liking for regenerative projects while explicitly stating they are not looking to participate.\n    *   `evidence_fragments`: [\"Me gustan los proyectos regenerativos\", \"no estoy buscando participar en ninguno\"]\n    *   `contradictions`: [] (The statement is consistent: likes the concept, doesn't want to join).\n    *   `missing_context`: [\"The reason why the user is not looking to participate\"]\n    *   `false_positive_risk`: `LOW` (The statement is very direct).\n    *   `uncertainty`: `LOW` (The statement is clear).\n    *   `human_review_reason`: \"User explicitly states they are not looking to participate despite liking the theme.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Regenerative projects\"\n    *   `contextual_meaning`: \"The user expresses an aesthetic or ideological appreciation for regenerative projects but explicitly declines active participation.\"\n    *   `apparent_affinity`: \"POSSIBLE\"\n    *   `apparent_affinity_domains`: [\"REGENERATION\"]\n    *   `apparent_intention`: \"THEMATIC_SYMPATHY\"\n    *   `intention_summary`: \"Expresses liking for the concept of regeneration without a desire for active involvement.\"\n    *   `evidence_fragments`: [\"Me gustan los proyectos regenerativos\", \"no estoy buscando participar en ninguno\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Reason for lack of interest in participation\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"User explicitly states they are not looking to participate despite liking the theme.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Regenerative projects\",\n  \"contextual_meaning\": \"The user expresses an ideological appreciation for regenerative projects but explicitly states they are not seeking to participate in any.\",\n  \"apparent_affinity\": \"POSSIBLE\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\"\n  ],\n  \"apparent_intention\": \"THEMATIC_SYMPATHY\",\n  \"intention_summary\": \"The user likes the concept of regenerative projects but explicitly denies any current intention to participate.\",\n  \"evidence_fragments\": [\n    \"Me gustan los proyectos regenerativos\",\n    \"no estoy buscando participar en ninguno\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"The reason why the user is not seeking participation\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"User explicitly states they are not looking to participate despite liking the theme.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 3,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Regenerative projects",
    "contextual_meaning": "The user expresses an ideological appreciation for regenerative projects but explicitly states they are not seeking to participate in any.",
    "apparent_affinity": "POSSIBLE",
    "apparent_affinity_domains": [
      "REGENERATION"
    ],
    "apparent_intention": "THEMATIC_SYMPATHY",
    "intention_summary": "The user likes the concept of regenerative projects but explicitly denies any current intention to participate.",
    "evidence_fragments": [
      "Me gustan los proyectos regenerativos",
      "no estoy buscando participar en ninguno"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The reason why the user is not seeking participation"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "User explicitly states they are not looking to participate despite liking the theme.",
    "review_priority": 62,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:09:54.671787Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_004 · agnes · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_004",
  "input_text": "Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:09:54.671915+00:00",
  "finished_at": "2026-07-20T01:10:03.623793+00:00",
  "latency_ms": 8951,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Search for a regenerative community in Yucatan and inquiry about participation methods.\",\n  \"contextual_meaning\": \"The user is actively looking for a specific type of social-environmental structure (regenerative community) in a defined geographic location (Yucatan) and is asking for procedural information on how to join or engage with such a group.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"COMMUNITY\",\n    \"REGENERATION\",\n    \"TERRITORY\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"EXPLORATION\",\n  \"intention_summary\": \"The user expresses a clear desire to find a community and asks for information on participation, indicating an exploratory phase rather than immediate transactional action or mere thematic sympathy.\",\n  \"evidence_fragments\": [\n    \"Busco una comunidad regenerativa en Yucatán\",\n    \"quiero conocer cómo se participa\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Specific interests within regeneration (e.g., agriculture, housing, governance)\",\n    \"Timeline for potential involvement\",\n    \"Prior experience with regenerative communities\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"User shows clear interest in regenerative communities in Yucatan and asks about participation, but lacks specific details on their background or immediate next steps.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 4,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Search for a regenerative community in Yucatan and inquiry about participation methods.",
    "contextual_meaning": "The user is actively looking for a specific type of social-environmental structure (regenerative community) in a defined geographic location (Yucatan) and is asking for procedural information on how to join or engage with such a group.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "COMMUNITY",
      "REGENERATION",
      "TERRITORY",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "EXPLORATION",
    "intention_summary": "The user expresses a clear desire to find a community and asks for information on participation, indicating an exploratory phase rather than immediate transactional action or mere thematic sympathy.",
    "evidence_fragments": [
      "Busco una comunidad regenerativa en Yucatán",
      "quiero conocer cómo se participa"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Specific interests within regeneration (e.g., agriculture, housing, governance)",
      "Timeline for potential involvement",
      "Prior experience with regenerative communities"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "User shows clear interest in regenerative communities in Yucatan and asks about participation, but lacks specific details on their background or immediate next steps.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:10:03.623720Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_004 · agnes · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_004",
  "input_text": "Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:10:03.623818+00:00",
  "finished_at": "2026-07-20T01:10:10.881439+00:00",
  "latency_ms": 7257,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Search for a regenerative community in Yucatan and inquiry about participation methods.\",\n  \"contextual_meaning\": \"The user is actively looking for a specific type of social-environmental structure (regenerative community) in a defined geographic location (Yucatan) and is asking for procedural information on how to join or engage with such a group.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"COMMUNITY\",\n    \"REGENERATION\",\n    \"TERRITORY\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"EXPLORATION\",\n  \"intention_summary\": \"The user expresses a clear desire to find a community and asks for information on participation, indicating an exploratory phase rather than immediate transactional action or mere thematic sympathy.\",\n  \"evidence_fragments\": [\n    \"Busco una comunidad regenerativa en Yucatán\",\n    \"quiero conocer cómo se participa\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Specific interests within regeneration (e.g., agriculture, housing, governance)\",\n    \"Timeline for potential involvement\",\n    \"Prior experience with regenerative communities\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"User shows clear interest in regenerative communities in Yucatan and asks about participation, but lacks specific details on their background or immediate next steps.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 4,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Search for a regenerative community in Yucatan and inquiry about participation methods.",
    "contextual_meaning": "The user is actively looking for a specific type of social-environmental structure (regenerative community) in a defined geographic location (Yucatan) and is asking for procedural information on how to join or engage with such a group.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "COMMUNITY",
      "REGENERATION",
      "TERRITORY",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "EXPLORATION",
    "intention_summary": "The user expresses a clear desire to find a community and asks for information on participation, indicating an exploratory phase rather than immediate transactional action or mere thematic sympathy.",
    "evidence_fragments": [
      "Busco una comunidad regenerativa en Yucatán",
      "quiero conocer cómo se participa"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Specific interests within regeneration (e.g., agriculture, housing, governance)",
      "Timeline for potential involvement",
      "Prior experience with regenerative communities"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "User shows clear interest in regenerative communities in Yucatan and asks about participation, but lacks specific details on their background or immediate next steps.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:10:10.881365Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_004 · agnes · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_004",
  "input_text": "Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:10:10.881465+00:00",
  "finished_at": "2026-07-20T01:10:18.043985+00:00",
  "latency_ms": 7162,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Search for a regenerative community in Yucatan and inquiry about participation methods.\",\n  \"contextual_meaning\": \"The user is actively looking for a specific type of social-environmental structure (regenerative community) in a defined geographic location (Yucatan) and is asking for procedural information on how to join or engage with such a group.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"COMMUNITY\",\n    \"REGENERATION\",\n    \"TERRITORY\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"EXPLORATION\",\n  \"intention_summary\": \"The user expresses a clear desire to find a community and asks for information on participation, indicating an exploratory phase rather than immediate transactional action or mere thematic sympathy.\",\n  \"evidence_fragments\": [\n    \"Busco una comunidad regenerativa en Yucatán\",\n    \"quiero conocer cómo se participa\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Specific interests within regeneration (e.g., agriculture, housing, governance)\",\n    \"Timeline for potential involvement\",\n    \"Prior experience with regenerative communities\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"User shows clear interest in regenerative communities in Yucatan and asks about participation, but lacks specific details on their background or immediate next steps.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 4,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Search for a regenerative community in Yucatan and inquiry about participation methods.",
    "contextual_meaning": "The user is actively looking for a specific type of social-environmental structure (regenerative community) in a defined geographic location (Yucatan) and is asking for procedural information on how to join or engage with such a group.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "COMMUNITY",
      "REGENERATION",
      "TERRITORY",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "EXPLORATION",
    "intention_summary": "The user expresses a clear desire to find a community and asks for information on participation, indicating an exploratory phase rather than immediate transactional action or mere thematic sympathy.",
    "evidence_fragments": [
      "Busco una comunidad regenerativa en Yucatán",
      "quiero conocer cómo se participa"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Specific interests within regeneration (e.g., agriculture, housing, governance)",
      "Timeline for potential involvement",
      "Prior experience with regenerative communities"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "User shows clear interest in regenerative communities in Yucatan and asks about participation, but lacks specific details on their background or immediate next steps.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:10:18.043913Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_004 · gemma · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_004",
  "input_text": "Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:10:18.044019+00:00",
  "finished_at": "2026-07-20T01:10:46.922705+00:00",
  "latency_ms": 28878,
  "raw_output": "<thought>*   Input: A short text in Spanish: \"Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.\" (I am looking for a regenerative community in Yucatan and I want to know how to participate.)\n    *   Goal: Analyze for Inlak'ech RADAR and return a specific JSON object.\n    *   Constraints: No markdown, no commentary, strict schema version, specific enums, literal quotes for evidence.\n\n    *   `real_topic`: Searching for a regenerative community in Yucatán and participation methods.\n    *   `contextual_meaning`: The user is explicitly expressing interest in joining or engaging with a regenerative project/community in the Yucatán region.\n    *   `apparent_affinity`: CLEAR (The user explicitly mentions \"comunidad regenerativa\" and \"Yucatán\").\n    *   `apparent_affinity_domains`: REGENERATION, MEXICO_YUCATAN_CONNECTION, ACTIVE_PARTICIPATION.\n    *   `apparent_intention`: ACTION_ORIENTED (They are asking *how* to participate).\n    *   `intention_summary`: The user wants to find a regenerative community in Yucatán and learn the specific steps or requirements to participate.\n    *   `evidence_fragments`: [\"Busco una comunidad regenerativa en Yucatán\", \"quiero conocer cómo se participa\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"User's background\", \"Specific type of regeneration (agricultural, social, etc.)\", \"Current location of the user\"]\n    *   `false_positive_risk`: LOW (The request is very direct).\n    *   `uncertainty`: LOW (The intent is clear).\n    *   `human_review_reason`: \"Direct inquiry about participation in a regenerative community in Yucatan.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Búsqueda de comunidad regenerativa en Yucatán\"\n    *   `contextual_meaning`: \"El usuario expresa un interés explícito en localizar y unirse a una comunidad con enfoque regenerativo en la región de Yucatán.\"\n    *   `apparent_affinity`: \"CLEAR\"\n    *   `apparent_affinity_domains`: [\"REGENERATION\", \"MEXICO_YUCATAN_CONNECTION\", \"ACTIVE_PARTICIPATION\"]\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"El usuario busca información concreta sobre los mecanismos de participación en comunidades regenerativas en Yucatán.\"\n    *   `evidence_fragments`: [\"Busco una comunidad regenerativa en Yucatán\", \"quiero conocer cómo se participa\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Perfil del usuario\", \"Tipo específico de regeneración de interés\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"Direct request for participation information in a regenerative community in Yucatan.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Búsqueda de comunidad regenerativa en Yucatán\",\n  \"contextual_meaning\": \"El usuario expresa un interés explícito en localizar y unirse a una comunidad con enfoque regenerativo en la región de Yucatán, solicitando información sobre los procesos de participación.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\",\n    \"MEXICO_YUCATAN_CONNECTION\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"El usuario desea conocer los pasos o requisitos necesarios para participar en una comunidad regenerativa en Yucatán.\",\n  \"evidence_fragments\": [\n    \"Busco una comunidad regenerativa en Yucatán\",\n    \"quiero conocer cómo se participa\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Perfil profesional o personal del usuario\",\n    \"Tipo de participación deseada (residencia, inversión, voluntariado)\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Direct inquiry regarding participation in a regenerative community in Yucatan.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 4,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Búsqueda de comunidad regenerativa en Yucatán",
    "contextual_meaning": "El usuario expresa un interés explícito en localizar y unirse a una comunidad con enfoque regenerativo en la región de Yucatán, solicitando información sobre los procesos de participación.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "REGENERATION",
      "MEXICO_YUCATAN_CONNECTION",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "El usuario desea conocer los pasos o requisitos necesarios para participar en una comunidad regenerativa en Yucatán.",
    "evidence_fragments": [
      "Busco una comunidad regenerativa en Yucatán",
      "quiero conocer cómo se participa"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Perfil profesional o personal del usuario",
      "Tipo de participación deseada (residencia, inversión, voluntariado)"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Direct inquiry regarding participation in a regenerative community in Yucatan.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:10:46.922633Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_004 · gemma · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_004",
  "input_text": "Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:10:46.922732+00:00",
  "finished_at": "2026-07-20T01:11:14.423767+00:00",
  "latency_ms": 27501,
  "raw_output": "<thought>*   Input: A short text in Spanish: \"Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.\" (I am looking for a regenerative community in Yucatan and I want to know how to participate.)\n    *   Goal: Analyze for Inlak'ech RADAR and return a JSON object following a specific schema.\n\n    *   `real_topic`: Searching for a regenerative community in Yucatan and participation methods.\n    *   `contextual_meaning`: The user is explicitly expressing interest in joining or engaging with a regenerative project/community in the Yucatan region.\n    *   `apparent_affinity`: CLEAR (The user explicitly mentions \"comunidad regenerativa\" and \"Yucatán\").\n    *   `apparent_affinity_domains`: REGENERATION, MEXICO_YUCATAN_CONNECTION, ACTIVE_PARTICIPATION.\n    *   `apparent_intention`: ACTION_ORIENTED (They are asking *how* to participate).\n    *   `intention_summary`: The user wants to find a regenerative community in Yucatan and learn the specific steps or requirements to participate.\n    *   `evidence_fragments`: [\"Busco una comunidad regenerativa en Yucatán\", \"quiero conocer cómo se participa\"]\n    *   `contradictions`: [] (None)\n    *   `missing_context`: [\"User's background\", \"Specific type of participation (financial, labor, residential)\", \"Current location\"]\n    *   `false_positive_risk`: LOW (The request is very direct).\n    *   `uncertainty`: LOW (The intent is clear).\n    *   `human_review_reason`: \"Direct request for participation in a regenerative community in Yucatan.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Búsqueda de comunidad regenerativa en Yucatán\"\n    *   `contextual_meaning`: \"El usuario expresa un interés explícito en localizar y unirse a una comunidad con enfoque regenerativo en la región de Yucatán.\"\n    *   `apparent_affinity`: \"CLEAR\"\n    *   `apparent_affinity_domains`: [\"REGENERATION\", \"MEXICO_YUCATAN_CONNECTION\", \"ACTIVE_PARTICIPATION\"]\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"El usuario busca información concreta sobre los mecanismos de participación en comunidades regenerativas en Yucatán.\"\n    *   `evidence_fragments`: [\"Busco una comunidad regenerativa en Yucatán\", \"quiero conocer cómo se participa\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Perfil del usuario\", \"Tipo de participación deseada (económica, laboral, residencial)\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"Direct request for participation in a regenerative community in Yucatan.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Búsqueda de comunidad regenerativa en Yucatán\",\n  \"contextual_meaning\": \"El usuario expresa un interés explícito en localizar y unirse a una comunidad con enfoque regenerativo en la región de Yucatán, solicitando información sobre los procesos de participación.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\",\n    \"MEXICO_YUCATAN_CONNECTION\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"El usuario desea conocer los pasos o requisitos necesarios para participar activamente en una comunidad regenerativa en Yucatán.\",\n  \"evidence_fragments\": [\n    \"Busco una comunidad regenerativa en Yucatán\",\n    \"quiero conocer cómo se participa\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Perfil o habilidades del usuario\",\n    \"Tipo de participación buscada (residencial, inversión, voluntariado)\",\n    \"Ubicación actual del usuario\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Direct request for participation in a regenerative community in Yucatan.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 4,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Búsqueda de comunidad regenerativa en Yucatán",
    "contextual_meaning": "El usuario expresa un interés explícito en localizar y unirse a una comunidad con enfoque regenerativo en la región de Yucatán, solicitando información sobre los procesos de participación.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "REGENERATION",
      "MEXICO_YUCATAN_CONNECTION",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "El usuario desea conocer los pasos o requisitos necesarios para participar activamente en una comunidad regenerativa en Yucatán.",
    "evidence_fragments": [
      "Busco una comunidad regenerativa en Yucatán",
      "quiero conocer cómo se participa"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Perfil o habilidades del usuario",
      "Tipo de participación buscada (residencial, inversión, voluntariado)",
      "Ubicación actual del usuario"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Direct request for participation in a regenerative community in Yucatan.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:11:14.423689Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_004 · gemma · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_004",
  "input_text": "Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:11:14.423794+00:00",
  "finished_at": "2026-07-20T01:11:42.641364+00:00",
  "latency_ms": 28217,
  "raw_output": "<thought>*   Input: A short text in Spanish: \"Busco una comunidad regenerativa en Yucatán y quiero conocer cómo se participa.\" (I am looking for a regenerative community in Yucatan and I want to know how to participate.)\n    *   Goal: Analyze for Inlak'ech RADAR and return a specific JSON object.\n    *   Constraints: No markdown, no commentary, strict schema version, specific enums, literal quotes for evidence.\n\n    *   `real_topic`: Searching for a regenerative community in Yucatan and participation methods.\n    *   `contextual_meaning`: The user is explicitly expressing interest in joining or engaging with a regenerative project/community in the Yucatan region.\n    *   `apparent_affinity`: CLEAR (The user explicitly mentions \"comunidad regenerativa\").\n    *   `apparent_affinity_domains`: REGENERATION, MEXICO_YUCATAN_CONNECTION, ACTIVE_PARTICIPATION.\n    *   `apparent_intention`: ACTION_ORIENTED (They are asking \"cómo se participa\" - how to participate).\n    *   `intention_summary`: The user wants to find a regenerative community in Yucatan and learn the steps to become a participant.\n    *   `evidence_fragments`: [\"Busco una comunidad regenerativa en Yucatán\", \"quiero conocer cómo se participa\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"User's background\", \"Specific type of regeneration (agricultural, social, etc.)\", \"Current location of the user\"]\n    *   `false_positive_risk`: LOW (The request is very direct).\n    *   `uncertainty`: LOW (The intent is clear).\n    *   `human_review_reason`: \"Direct inquiry about participation in a regenerative community in Yucatan.\"\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Búsqueda de comunidad regenerativa en Yucatán\"\n    *   `contextual_meaning`: \"El usuario expresa un interés explícito en localizar y unirse a una comunidad con enfoque regenerativo en la región de Yucatán.\"\n    *   `apparent_affinity`: \"CLEAR\"\n    *   `apparent_affinity_domains`: [\"REGENERATION\", \"MEXICO_YUCATAN_CONNECTION\", \"ACTIVE_PARTICIPATION\"]\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"El usuario busca información concreta sobre los mecanismos de participación en comunidades regenerativas en Yucatán.\"\n    *   `evidence_fragments`: [\"Busco una comunidad regenerativa en Yucatán\", \"quiero conocer cómo se participa\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Perfil del usuario\", \"Tipo específico de regeneración de interés\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"Direct request for participation information in a regenerative community.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Búsqueda de comunidad regenerativa en Yucatán\",\n  \"contextual_meaning\": \"El usuario manifiesta un interés explícito en encontrar una comunidad con enfoque regenerativo en la región de Yucatán y solicita información sobre los procesos para integrarse o participar en ella.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"REGENERATION\",\n    \"MEXICO_YUCATAN_CONNECTION\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"El usuario desea conocer los pasos o requisitos para participar en una comunidad regenerativa en Yucatán.\",\n  \"evidence_fragments\": [\n    \"Busco una comunidad regenerativa en Yucatán\",\n    \"quiero conocer cómo se participa\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Perfil profesional o personal del usuario\",\n    \"Tipo de participación deseada (residencia, voluntariado, inversión, etc.)\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Direct inquiry regarding participation in a regenerative community in Yucatan.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 4,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Búsqueda de comunidad regenerativa en Yucatán",
    "contextual_meaning": "El usuario manifiesta un interés explícito en encontrar una comunidad con enfoque regenerativo en la región de Yucatán y solicita información sobre los procesos para integrarse o participar en ella.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "REGENERATION",
      "MEXICO_YUCATAN_CONNECTION",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "El usuario desea conocer los pasos o requisitos para participar en una comunidad regenerativa en Yucatán.",
    "evidence_fragments": [
      "Busco una comunidad regenerativa en Yucatán",
      "quiero conocer cómo se participa"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Perfil profesional o personal del usuario",
      "Tipo de participación deseada (residencia, voluntariado, inversión, etc.)"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Direct inquiry regarding participation in a regenerative community in Yucatan.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:11:42.641288Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_005 · agnes · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_005",
  "input_text": "Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:11:42.641403+00:00",
  "finished_at": "2026-07-20T01:11:55.395883+00:00",
  "latency_ms": 12754,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Expression of interest in long-term participation and request for initial conversation.\",\n  \"contextual_meaning\": \"The sender identifies a desire for long-term engagement and proactively seeks a dialogue to learn more about the organization's work.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"LONG_TERM\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"Direct request to initiate contact for informational purposes regarding potential involvement.\",\n  \"evidence_fragments\": [\n    \"Quiero participar en un proyecto de largo plazo\",\n    \"puedo conversar esta semana para conocer Inlak'ech\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Specific domain of interest within the organization's scope\",\n    \"Nature of the intended participation (financial, volunteer, professional)\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Confirm specific areas of alignment and clarify the type of long-term project interest.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 5,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Expression of interest in long-term participation and request for initial conversation.",
    "contextual_meaning": "The sender identifies a desire for long-term engagement and proactively seeks a dialogue to learn more about the organization's work.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "LONG_TERM",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "Direct request to initiate contact for informational purposes regarding potential involvement.",
    "evidence_fragments": [
      "Quiero participar en un proyecto de largo plazo",
      "puedo conversar esta semana para conocer Inlak'ech"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Specific domain of interest within the organization's scope",
      "Nature of the intended participation (financial, volunteer, professional)"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Confirm specific areas of alignment and clarify the type of long-term project interest.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:11:55.395797Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_005 · agnes · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_005",
  "input_text": "Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:11:55.395913+00:00",
  "finished_at": "2026-07-20T01:12:03.006773+00:00",
  "latency_ms": 7610,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Expression of interest in long-term participation and request for initial conversation.\",\n  \"contextual_meaning\": \"The sender identifies a desire for long-term engagement and proactively seeks a dialogue to learn more about the organization's work.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"LONG_TERM\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"Direct request to initiate contact for informational purposes regarding potential involvement.\",\n  \"evidence_fragments\": [\n    \"Quiero participar en un proyecto de largo plazo\",\n    \"puedo conversar esta semana para conocer Inlak'ech\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Specific domain of interest within the organization's scope\",\n    \"Nature of the intended participation (financial, volunteer, professional)\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Confirm specific areas of alignment and clarify the type of long-term project interest.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 5,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Expression of interest in long-term participation and request for initial conversation.",
    "contextual_meaning": "The sender identifies a desire for long-term engagement and proactively seeks a dialogue to learn more about the organization's work.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "LONG_TERM",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "Direct request to initiate contact for informational purposes regarding potential involvement.",
    "evidence_fragments": [
      "Quiero participar en un proyecto de largo plazo",
      "puedo conversar esta semana para conocer Inlak'ech"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Specific domain of interest within the organization's scope",
      "Nature of the intended participation (financial, volunteer, professional)"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Confirm specific areas of alignment and clarify the type of long-term project interest.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:12:03.006699Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_005 · agnes · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_005",
  "input_text": "Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.",
  "provider": "agnes",
  "model": "agnes-2.0-flash",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:12:03.006799+00:00",
  "finished_at": "2026-07-20T01:12:10.194459+00:00",
  "latency_ms": 7187,
  "raw_output": "{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Expression of interest in long-term participation and request for initial conversation.\",\n  \"contextual_meaning\": \"The sender identifies a desire for long-term engagement and proactively seeks a dialogue to learn more about the organization's work.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"LONG_TERM\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"Direct request to initiate contact for informational purposes regarding potential involvement.\",\n  \"evidence_fragments\": [\n    \"Quiero participar en un proyecto de largo plazo\",\n    \"puedo conversar esta semana para conocer Inlak'ech\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"Specific domain of interest within the organization's scope\",\n    \"Nature of the intended participation (financial, volunteer, professional)\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Confirm specific areas of alignment and clarify the type of long-term project interest.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 5,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Expression of interest in long-term participation and request for initial conversation.",
    "contextual_meaning": "The sender identifies a desire for long-term engagement and proactively seeks a dialogue to learn more about the organization's work.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "LONG_TERM",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "Direct request to initiate contact for informational purposes regarding potential involvement.",
    "evidence_fragments": [
      "Quiero participar en un proyecto de largo plazo",
      "puedo conversar esta semana para conocer Inlak'ech"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "Specific domain of interest within the organization's scope",
      "Nature of the intended participation (financial, volunteer, professional)"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Confirm specific areas of alignment and clarify the type of long-term project interest.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:agnes",
    "model_name": "agnes-2.0-flash",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:12:10.194364Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_005 · gemma · repetición 1

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_005",
  "input_text": "Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 1,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:12:10.194506+00:00",
  "finished_at": "2026-07-20T01:12:39.468796+00:00",
  "latency_ms": 29274,
  "raw_output": "<thought>*   Input: A short conversation snippet.\n    *   Title: `CASE_005`\n    *   Text: `Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.`\n    *   Goal: Analyze for Inlak'ech RADAR and return a specific JSON object.\n\n    *   \"Quiero participar en un proyecto de largo plazo\" -> I want to participate in a long-term project.\n    *   \"puedo conversar esta semana para conocer Inlak'ech\" -> I can talk this week to get to know Inlak'ech.\n\n    *   `real_topic`: Interest in participating in a long-term project and scheduling a call to learn about Inlak'ech.\n    *   `contextual_meaning`: The user is expressing a direct desire to engage with the organization/project and is proposing a meeting.\n    *   `apparent_affinity`: CLEAR (Directly states desire to participate in a long-term project).\n    *   `apparent_affinity_domains`: `LONG_TERM`, `ACTIVE_PARTICIPATION`.\n    *   `apparent_intention`: ACTION_ORIENTED (Wants to participate and schedule a call).\n    *   `intention_summary`: The user wants to join a long-term project and is available for a conversation this week to learn more.\n    *   `evidence_fragments`: [\"Quiero participar en un proyecto de largo plazo\", \"puedo conversar esta semana para conocer Inlak'ech\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Specific skills or resources the user brings\", \"The specific nature of the 'long-term project' they are referring to\"]\n    *   `false_positive_risk`: LOW (The statement is explicit).\n    *   `uncertainty`: LOW (The intent is clear).\n    *   `human_review_reason`: User explicitly requested a conversation to participate in a long-term project.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Interest in long-term project participation\"\n    *   `contextual_meaning`: \"The user is expressing a direct desire to get involved with Inlak'ech through a long-term commitment and is proposing a meeting to discuss it.\"\n    *   `apparent_affinity`: \"CLEAR\"\n    *   `apparent_affinity_domains`: [\"LONG_TERM\", \"ACTIVE_PARTICIPATION\"]\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"The user wants to participate in a long-term project and is available for a call this week to learn more about Inlak'ech.\"\n    *   `evidence_fragments`: [\"Quiero participar en un proyecto de largo plazo\", \"puedo conversar esta semana para conocer Inlak'ech\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"User's background or specific area of interest within the project\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"Direct request for engagement and scheduling a call.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Interest in long-term project participation\",\n  \"contextual_meaning\": \"The user is expressing a direct desire to get involved with Inlak'ech through a long-term commitment and is proposing a meeting to discuss it.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"LONG_TERM\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user wants to participate in a long-term project and is available for a call this week to learn more about Inlak'ech.\",\n  \"evidence_fragments\": [\n    \"Quiero participar en un proyecto de largo plazo\",\n    \"puedo conversar esta semana para conocer Inlak'ech\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"User's specific skills, resources, or background\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"Direct request for engagement and scheduling a call to join a long-term project.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 5,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Interest in long-term project participation",
    "contextual_meaning": "The user is expressing a direct desire to get involved with Inlak'ech through a long-term commitment and is proposing a meeting to discuss it.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "LONG_TERM",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user wants to participate in a long-term project and is available for a call this week to learn more about Inlak'ech.",
    "evidence_fragments": [
      "Quiero participar en un proyecto de largo plazo",
      "puedo conversar esta semana para conocer Inlak'ech"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "User's specific skills, resources, or background"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "Direct request for engagement and scheduling a call to join a long-term project.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:12:39.468719Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_005 · gemma · repetición 2

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_005",
  "input_text": "Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 2,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:12:39.468822+00:00",
  "finished_at": "2026-07-20T01:13:08.275228+00:00",
  "latency_ms": 28806,
  "raw_output": "<thought>*   Input: A short conversation snippet.\n    *   Title: `CASE_005`\n    *   Text: `Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.`\n    *   Goal: Analyze for Inlak'ech RADAR and return a specific JSON object.\n\n    *   \"Quiero participar en un proyecto de largo plazo\" -> I want to participate in a long-term project.\n    *   \"puedo conversar esta semana para conocer Inlak'ech\" -> I can talk this week to get to know Inlak'ech.\n\n    *   `real_topic`: Interest in participating in a long-term project with Inlak'ech.\n    *   `contextual_meaning`: The user is expressing a direct desire to engage with the organization/project and is offering their availability for a call/meeting to learn more.\n    *   `apparent_affinity`: CLEAR (Directly states desire to participate in a long-term project).\n    *   `apparent_affinity_domains`: `LONG_TERM`, `ACTIVE_PARTICIPATION`.\n    *   `apparent_intention`: ACTION_ORIENTED (Wants to participate and is proposing a time to talk).\n    *   `intention_summary`: The user wants to join a long-term project and is requesting an introductory conversation.\n    *   `evidence_fragments`: [\"Quiero participar en un proyecto de largo plazo\", \"puedo conversar esta semana para conocer Inlak'ech\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Specific skills or resources the user brings\", \"How they found Inlak'ech\"]\n    *   `false_positive_risk`: LOW (The statement is explicit).\n    *   `uncertainty`: LOW.\n    *   `human_review_reason`: User explicitly requested a conversation to participate in a long-term project.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Interest in long-term project participation\"\n    *   `contextual_meaning`: \"The user is expressing a direct desire to get involved with Inlak'ech through a long-term project and is proposing a meeting to discuss further.\"\n    *   `apparent_affinity`: \"CLEAR\"\n    *   `apparent_affinity_domains`: [\"LONG_TERM\", \"ACTIVE_PARTICIPATION\"]\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"The user wants to participate in a long-term project and is available for a call this week to learn more about Inlak'ech.\"\n    *   `evidence_fragments`: [\"Quiero participar en un proyecto de largo plazo\", \"puedo conversar esta semana para conocer Inlak'ech\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"The user's background or specific area of interest within the project\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"Direct expression of intent to participate and request for a meeting.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Interest in long-term project participation\",\n  \"contextual_meaning\": \"The user is explicitly expressing a desire to get involved with Inlak'ech in a long-term capacity and is proposing a meeting to explore this further.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"LONG_TERM\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user wants to participate in a long-term project and is offering their availability this week for an introductory conversation.\",\n  \"evidence_fragments\": [\n    \"Quiero participar en un proyecto de largo plazo\",\n    \"puedo conversar esta semana para conocer Inlak'ech\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"The user's specific skills, professional background, or the nature of the participation they are seeking\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user has made a direct request for a meeting to discuss participation in a long-term project.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 5,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Interest in long-term project participation",
    "contextual_meaning": "The user is explicitly expressing a desire to get involved with Inlak'ech in a long-term capacity and is proposing a meeting to explore this further.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "LONG_TERM",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user wants to participate in a long-term project and is offering their availability this week for an introductory conversation.",
    "evidence_fragments": [
      "Quiero participar en un proyecto de largo plazo",
      "puedo conversar esta semana para conocer Inlak'ech"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The user's specific skills, professional background, or the nature of the participation they are seeking"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user has made a direct request for a meeting to discuss participation in a long-term project.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:13:08.275151Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```

### CASE_005 · gemma · repetición 3

```json
{
  "experiment_id": "experimento3",
  "case_id": "CASE_005",
  "input_text": "Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.",
  "provider": "gemma",
  "model": "gemma-4-31b-it",
  "repetition": 3,
  "prompt_version": "radar-conversation-assessment/v3",
  "started_at": "2026-07-20T01:13:08.275255+00:00",
  "finished_at": "2026-07-20T01:13:37.263385+00:00",
  "latency_ms": 28988,
  "raw_output": "<thought>*   Input: A short conversation snippet.\n    *   Title: `CASE_005`\n    *   Text: `Quiero participar en un proyecto de largo plazo y puedo conversar esta semana para conocer Inlak'ech.`\n    *   Goal: Analyze for Inlak'ech RADAR and return a specific JSON object.\n\n    *   \"Quiero participar en un proyecto de largo plazo\" -> I want to participate in a long-term project.\n    *   \"puedo conversar esta semana para conocer Inlak'ech\" -> I can talk this week to get to know Inlak'ech.\n\n    *   `real_topic`: Interest in participating in a long-term project and scheduling a call to learn about Inlak'ech.\n    *   `contextual_meaning`: The user is expressing a direct desire to engage with the Inlak'ech project, specifically mentioning a long-term perspective and a willingness to have an introductory conversation.\n    *   `apparent_affinity`: CLEAR (Directly states desire to participate in a long-term project).\n    *   `apparent_affinity_domains`: `LONG_TERM`, `ACTIVE_PARTICIPATION`.\n    *   `apparent_intention`: ACTION_ORIENTED (Wants to participate and schedule a call).\n    *   `intention_summary`: The user wants to join a long-term project and is proposing a meeting this week to learn more.\n    *   `evidence_fragments`: [\"Quiero participar en un proyecto de largo plazo\", \"puedo conversar esta semana para conocer Inlak'ech\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"Specific skills or resources the user brings\", \"The nature of the 'participation' they are seeking\"]\n    *   `false_positive_risk`: LOW (The statement is explicit).\n    *   `uncertainty`: LOW (The intent is clear).\n    *   `human_review_reason`: User explicitly requests a conversation to participate in a long-term project.\n\n    *   `schema_version`: \"radar-conversation-assessment/v3\"\n    *   `real_topic`: \"Interest in long-term project participation\"\n    *   `contextual_meaning`: \"The user expresses a clear desire to get involved with Inlak'ech on a long-term basis and suggests a meeting to discuss further.\"\n    *   `apparent_affinity`: \"CLEAR\"\n    *   `apparent_affinity_domains`: [\"LONG_TERM\", \"ACTIVE_PARTICIPATION\"]\n    *   `apparent_intention`: \"ACTION_ORIENTED\"\n    *   `intention_summary`: \"The user wants to participate in a long-term project and is available for a call this week to learn more about Inlak'ech.\"\n    *   `evidence_fragments`: [\"Quiero participar en un proyecto de largo plazo\", \"puedo conversar esta semana para conocer Inlak'ech\"]\n    *   `contradictions`: []\n    *   `missing_context`: [\"The user's specific background or capacity for participation\"]\n    *   `false_positive_risk`: \"LOW\"\n    *   `uncertainty`: \"LOW\"\n    *   `human_review_reason`: \"Direct request for participation and a meeting.\"</thought>{\n  \"schema_version\": \"radar-conversation-assessment/v3\",\n  \"real_topic\": \"Interest in long-term project participation\",\n  \"contextual_meaning\": \"The user is explicitly expressing a desire to get involved with Inlak'ech through a long-term project and is proposing a meeting to learn more.\",\n  \"apparent_affinity\": \"CLEAR\",\n  \"apparent_affinity_domains\": [\n    \"LONG_TERM\",\n    \"ACTIVE_PARTICIPATION\"\n  ],\n  \"apparent_intention\": \"ACTION_ORIENTED\",\n  \"intention_summary\": \"The user wants to participate in a long-term project and is available to have a conversation this week to get to know Inlak'ech.\",\n  \"evidence_fragments\": [\n    \"Quiero participar en un proyecto de largo plazo\",\n    \"puedo conversar esta semana para conocer Inlak'ech\"\n  ],\n  \"contradictions\": [],\n  \"missing_context\": [\n    \"The user's specific skills, resources, or the nature of the participation they are offering\"\n  ],\n  \"false_positive_risk\": \"LOW\",\n  \"uncertainty\": \"LOW\",\n  \"human_review_reason\": \"The user explicitly states a desire to participate and requests a meeting.\"\n}",
  "parsed_output": {
    "id": null,
    "conversation_id": 5,
    "schema_version": "radar-conversation-assessment/v3",
    "assessment_status": "COMPLETED",
    "real_topic": "Interest in long-term project participation",
    "contextual_meaning": "The user is explicitly expressing a desire to get involved with Inlak'ech through a long-term project and is proposing a meeting to learn more.",
    "apparent_affinity": "CLEAR",
    "apparent_affinity_domains": [
      "LONG_TERM",
      "ACTIVE_PARTICIPATION"
    ],
    "apparent_intention": "ACTION_ORIENTED",
    "intention_summary": "The user wants to participate in a long-term project and is available to have a conversation this week to get to know Inlak'ech.",
    "evidence_fragments": [
      "Quiero participar en un proyecto de largo plazo",
      "puedo conversar esta semana para conocer Inlak'ech"
    ],
    "rejected_evidence_fragments": [],
    "contradictions": [],
    "missing_context": [
      "The user's specific skills, resources, or the nature of the participation they are offering"
    ],
    "false_positive_risk": "LOW",
    "uncertainty": "LOW",
    "human_review_reason": "The user explicitly states a desire to participate and requests a meeting.",
    "review_priority": 100,
    "recommended_review_action": "REVIEW",
    "semantic_engine": "llm:openai_compatible",
    "model_name": "gemma-4-31b-it",
    "safe_error_code": null,
    "provisional": true,
    "human_review_required": true,
    "created_at": "2026-07-20T01:13:37.263308Z"
  },
  "error": null,
  "fallback_used": false,
  "status": "COMPLETED"
}
```
