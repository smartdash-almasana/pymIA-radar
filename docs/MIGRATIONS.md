# Migraciones de base de datos — RADAR

## Autoridad

RADAR utiliza Alembic para evolucionar el esquema sin borrar datos.

Revisiones iniciales:

```text
20260719_0001 — baseline del esquema anterior a V3
20260719_0002 — conversation_assessments_v3
```

`Base.metadata.create_all()` permanece temporalmente para pruebas aisladas y bases locales nuevas, pero no sustituye las migraciones.

## Reglas

- realizar respaldo antes de migrar una base con datos reales;
- no borrar ni recrear la base para aplicar una revisión;
- no convertir evaluaciones V2 en V3;
- no marcar una baseline como aplicada sin verificar el esquema existente;
- no registrar secretos ni imprimir el `DATABASE_URL` completo;
- ejecutar desde la raíz de `inlakech-radar`.

## Base nueva

Con `DATABASE_URL` configurado:

```powershell
python -m alembic upgrade head
```

Esto crea el esquema histórico y luego agrega `conversation_assessments_v3`.

## Base existente sin Alembic

Primero verificar que la base coincide con el esquema histórico esperado:

```powershell
python scripts/verify_alembic_baseline.py
```

La salida autorizante es:

```text
STATUS=BASELINE_MATCH
SAFE_TO_STAMP_BASELINE=true
```

Solo en ese caso:

```powershell
python -m alembic stamp 20260719_0001
python -m alembic upgrade head
```

`stamp` no modifica tablas; registra que el esquema histórico ya existe. El `upgrade` posterior crea únicamente la tabla V3 y sus índices.

Si la verificación informa `BASELINE_MISMATCH`, detener la migración. No usar `stamp` para ocultar diferencias.

## Base ya versionada

Consultar la revisión:

```powershell
python -m alembic current
```

Aplicar pendientes:

```powershell
python -m alembic upgrade head
```

## SQLite de pruebas

Ejemplo con una base temporal:

```powershell
$env:DATABASE_URL="sqlite+pysqlite:///./data/migration-test.db"
python -m alembic upgrade head
```

Las pruebas automatizadas cubren:

- upgrade de base nueva;
- baseline seguida de V3;
- verificación de una base existente sin tabla `alembic_version`;
- rechazo de un esquema incompleto;
- downgrade de V3 conservando las tablas históricas.

## PostgreSQL

La configuración usa el mismo `DATABASE_URL` de la aplicación:

```text
postgresql+psycopg://usuario:clave@host:puerto/base
```

No incorporar credenciales al repositorio. Antes del primer upgrade real:

1. crear respaldo;
2. verificar conectividad;
3. ejecutar `python -m alembic current`;
4. verificar o aplicar baseline según corresponda;
5. ejecutar `python -m alembic upgrade head`;
6. comprobar la tabla `conversation_assessments_v3`;
7. ejecutar la suite de RADAR.

## Downgrade de V3

La revisión V3 es técnicamente reversible mientras sus registros no necesiten conservarse:

```powershell
python -m alembic downgrade 20260719_0001
```

Este comando elimina `conversation_assessments_v3`, pero conserva el esquema histórico. Antes de usarlo en una base con evaluaciones V3, exportar o respaldar esos registros.

## Validación posterior

```powershell
python -m pytest -q
```

El upgrade no autoriza por sí mismo el embudo de descubrimiento ni SPEC-003B.
