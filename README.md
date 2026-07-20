# Inlak'ech RADAR

Sistema dedicado de prospección conversacional, descubrimiento humano y precalificación para Inlak’ech.

## Definición canónica

Inlak’ech es el proyecto global.

RADAR es un instrumento para:

> Encontrar conversaciones públicas aparentemente afines a Inlak’ech, identificar a las personas que las expresan, facilitar un contacto humano de descubrimiento y, solo cuando la afinidad se revela y existe consentimiento, iniciar la precalificación y entregar leads calificados al embudo comercial.

## Autoridad documental

- objetivo obligatorio: `docs/RADAR_MANDATORY_OBJECTIVE_DECLARATION.md`;
- arquitectura maestra: `docs/RADAR_MASTER_ARCHITECTURE_AND_DEVELOPMENT_DIRECTION.md`;
- contrato integral: `docs/RADAR_COMMERCIAL_CONVERSION_CONTRACT.md`;
- precedencia: `docs/DOCUMENT_PRECEDENCE.md`;
- búsqueda: `docs/RADAR_SEARCH_ENGAGEMENT_TEXT.md`;
- estado vigente: `docs/CURRENT_ENGINEERING_STATE.md`.

## Arquitectura funcional

```text
motores de descubrimiento y fuentes autorizadas
        ↓
normalización, persistencia y deduplicación
        ↓
interpretación de la conversación
        ↓
afinidad e intención aparentes con evidencia
        ↓
revisión humana
        ↓
candidato de descubrimiento
        ↓
contacto humano y registro de respuesta
        ↓
diálogo de descubrimiento
        ↓
afinidad revelada o descartada
        ↓
consentimiento para continuar
        ↓
precalificación
        ↓
lead calificado
        ↓
transferencia controlada a Relaticle
```

## Dos embudos

### Descubrimiento

Permite que la persona conozca Inlak’ech y revele libremente si existe afinidad. No es venta ni precalificación encubierta.

### Conversión

Comienza únicamente después de afinidad o interés suficiente, voluntad de continuar y consentimiento explícito.

## Responsabilidades

```text
el LLM interpreta
→ RADAR valida, gobierna y registra
→ el humano decide y se vincula
```

El LLM no asigna arquetipos desde publicaciones públicas, no infiere capacidad económica, no contacta y no convierte personas en leads.

## Arquitectura técnica

Se conserva el repositorio actual y la aplicación monolítica modular:

- Python 3.12;
- FastAPI;
- SQLAlchemy;
- SQLite para desarrollo local y PostgreSQL como objetivo;
- interfaz web actual;
- last30days mediante adaptador;
- Agnes/OpenAI-compatible para interpretación estructurada;
- Relaticle como CRM externo, sujeto a auditoría.

No se crea otro repositorio, microservicio, frontend ni CRM.

## Requisitos

- Python 3.12;
- Git;
- Docker Desktop y Docker Compose cuando se utilice el entorno en contenedores;
- claves de API según fuentes y modelo.

## Inicio rápido local

Desde PowerShell, en la raíz del repositorio:

```powershell
python scripts/run_local.py
```

El comando:

- usa `data/radar-local.db` mediante SQLite;
- ejecuta `alembic upgrade head`;
- configura el repositorio local de last30days;
- inicia RADAR en `http://127.0.0.1:8000`.

La clave del proveedor semántico se configura por variables de entorno cuando se desea ejecutar la evaluación V3 real.

## Recorrido disponible

Desde la interfaz se puede:

1. elegir una consulta del catálogo y buscar conversaciones públicas;
2. admitir únicamente resultados sustantivos en la bandeja;
3. ejecutar la evaluación conversacional V3;
4. revisar y crear un candidato de descubrimiento;
5. registrar contacto, respuesta y outcome humano;
6. registrar invitación y aceptación de precalificación;
7. ejecutar la precalificación únicamente cuando el gate esté completo.

La transferencia real a Relaticle continúa bloqueada hasta auditar su contrato externo.

## Capacidades técnicas existentes reutilizables

- integración real con last30days;
- normalización, persistencia y deduplicación;
- API FastAPI y bandeja local;
- integración semántica estructurada con Agnes;
- revisión humana antes de registrar contacto;
- eventos de contacto y respuesta;
- precalificación determinística existente;
- frontera local con Relaticle.

## Método de desarrollo

El repositorio usa Spec-Driven Development liviano.

Documentos principales:

- `AGENTS.md`;
- `docs/SPEC_DRIVEN_DEVELOPMENT.md`;
- `docs/ENGINEERING_OPERATING_CONTRACT.md`;
- `docs/PRODUCT_SCOPE.md`;
- `docs/ACCEPTANCE_MATRIX.md`;
- `docs/MILESTONES.md`;
- `docs/specs/`.

Una especificación `DRAFT` no autoriza cambios de código.
