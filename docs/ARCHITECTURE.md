# Arquitectura de RADAR

## Principio

RADAR se mantiene como una aplicación monolítica modular dentro del repositorio actual.

```text
last30days y fuentes autorizadas
        ↓
RADAR: recuperación, normalización y persistencia
        ↓
interpretación semántica de la conversación
        ↓
revisión humana
        ↓
embudo humano de descubrimiento
        ↓
precalificación consentida
        ↓
Relaticle y embudo comercial
```

No se crea otro repositorio, backend, frontend ni CRM.

---

## 1. Descubrimiento externo

### last30days-skill y fuentes autorizadas

Responsabilidades:

- localizar conversaciones públicas;
- devolver texto, contexto, URL, fecha, fuente e identidad pública disponible;
- respetar contratos y límites de cada fuente.

Se mantiene separado e integrado mediante adaptadores.

No decide afinidad, arquetipo, capacidad ni calificación.

---

## 2. Núcleo RADAR

RADAR administra:

- normalización;
- persistencia;
- deduplicación;
- interpretación semántica;
- evidencia y provisionalidad;
- revisión humana;
- estados del descubrimiento;
- contacto y respuesta registrados;
- resultado humano del descubrimiento;
- consentimiento;
- precalificación;
- transferencia controlada.

Principio:

```text
el LLM interpreta
→ RADAR valida, gobierna y registra
→ el humano decide y se vincula
```

---

## 3. Capa semántica

La unidad inicial es la conversación.

La salida objetivo debe describir:

- tema real;
- significado contextual;
- afinidad semántica aparente;
- campos de afinidad;
- intención aparente;
- evidencia;
- contradicciones;
- información faltante;
- incertidumbre;
- riesgo de falso positivo.

No debe asignar durante esta etapa:

- arquetipo;
- capacidad económica;
- camino de participación;
- calificación comercial.

Toda salida es provisional y requiere revisión humana.

---

## 4. Revisión humana

La bandeja permite:

- leer la conversación y su contexto;
- revisar la interpretación;
- observar evidencia e incertidumbre;
- descartar;
- no contactar;
- mantener en observación;
- aprobar un contacto de descubrimiento;
- editar el mensaje sugerido.

No existe acción externa automática.

---

## 5. Embudo de descubrimiento

Dominio explícito situado entre la revisión y la precalificación.

```text
candidato de descubrimiento
→ contacto humano
→ respuesta
→ diálogo
→ afinidad revelada o no confirmada
→ motivaciones y objeciones
→ posible hipótesis de arquetipo
→ consentimiento o cierre
```

Debe existir un registro humano equivalente a `DiscoveryOutcome`.

El arquetipo solo puede formularse después de diálogo suficiente y requiere confirmación humana.

---

## 6. Precalificación

Solo se habilita cuando existen:

- respuesta humana verificable;
- afinidad revelada o interés suficiente;
- voluntad de continuar;
- consentimiento explícito.

La precalificación utiliza datos declarados y reglas determinísticas revisables.

No debe ejecutarse directamente desde una publicación pública ni desde una respuesta aislada sin gate humano.

---

## 7. Relaticle

CRM externo para:

- personas autorizadas;
- oportunidades;
- tareas;
- notas;
- seguimiento comercial.

No recibe conversaciones crudas ni candidatos prematuros.

La integración permanece bloqueada hasta auditar el contrato real. La oportunidad se crea únicamente para un lead calificado o por aprobación comercial explícita documentada.

---

## 8. Componentes reutilizados

- FastAPI;
- SQLAlchemy;
- SQLite local y futura PostgreSQL;
- Jinja/JavaScript de la interfaz actual;
- adaptador last30days;
- modelo `Conversation`;
- integración Agnes/OpenAI-compatible;
- validación Pydantic;
- `ReviewDecision`;
- `EngagementEvent`;
- precalificación determinística;
- frontera con Relaticle.

## 9. Evoluciones necesarias

- contrato semántico centrado en conversación;
- versión persistente compatible con ese contrato;
- estados del embudo de descubrimiento;
- `DiscoveryCase` o representación equivalente;
- `DiscoveryOutcome` o representación equivalente;
- arquetipo posterior al diálogo humano;
- gate explícito hacia precalificación;
- interfaz progresiva por etapa.

## 10. Exclusiones de arquitectura

No agregar sin necesidad demostrada:

- microservicios;
- Redis;
- Celery;
- base vectorial;
- frontend separado;
- orquestador externo;
- BERTopic;
- SetFit;
- Argilla;
- Haystack;
- otro CRM;
- otro repositorio.
