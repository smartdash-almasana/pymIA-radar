# SPEC-001 — Descubrimiento e ingesta

**Estado:** DRAFT

## Propósito

Convertir resultados reales de last30days-skill en conversaciones persistidas y trazables.

## Entradas

- consulta temática;
- configuración de fuente;
- resultado real del repositorio externo.

## Salidas

Cada conversación debe contener:

- fuente;
- identificador externo;
- URL;
- autor, si existe;
- título;
- texto;
- contexto;
- fecha;
- consulta de origen;
- métricas de interacción.

## Reglas

- no inventar campos faltantes;
- conservar texto original;
- registrar fuente y consulta;
- deduplicar por fuente e identificador;
- permitir reejecución.

## Criterios de aceptación

1. Ejecutar tres consultas reales.
2. Guardar al menos un resultado válido.
3. Repetir la ingesta sin duplicarlo.
4. Recuperar el registro desde la API.
5. Documentar limitaciones por fuente.

## Pruebas

- normalización;
- validación de URL;
- campos faltantes;
- deduplicación;
- reingesta.
