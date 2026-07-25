# RADAR — Cierre contractual de interfaz visual 001

**Cycle ID:** `RADAR-VISUAL-INTERFACE-CONTRACT-CLOSE-001`  
**Estado:** `VERIFIED`

## Propósito

La interfaz visual permite revisar conversaciones públicas reales sin reemplazar la decisión humana.

## Flujo contractual

```text
ver conversaciones encontradas
→ identificar relevancia aparente
→ abrir conversación
→ consultar fuente original
→ analizar evidencia
→ identificar candidato, preparar borrador o descartar
```

## Reglas de interfaz

- título principal: `RADAR DE CONVERSACIONES`;
- datos provenientes del backend real, sin conversaciones comerciales simuladas;
- visualización tipo radar/mapa de señales;
- modal accesible con conversación y fuente original;
- pantalla de análisis separada;
- etiquetas humanas, sin exponer nombres internos de proveedores;
- conversaciones descartadas fuera de la bandeja operativa;
- no se envía contacto automático;
- identificar una persona candidata exige identidad pública;
- preparar respuesta exige borrador explícito;
- toda decisión queda trazada;
- RADAR encuentra y analiza; la persona revisa y decide.

## Evidencia técnica

- `app/htmx_ui.py`
- `app/templates/radar/`
- `app/static/radar-ui.css.txt`
- `app/static/radar-ui.js.txt`
- `tests/test_htmx_real_data.py`

## Verificación de regresión

- `tests/test_htmx_real_data.py`: passed
- Integración relacionada: 48 passed
- Suite completa: 336 passed, 2 skipped
- Regresiones: 0

## Casos verificados

- página principal sobre backend real;
- fragmentos HTMX parciales;
- apertura de conversación y análisis;
- enlace a fuente original;
- cierre de modal operativo;
- exclusión de fixtures y URLs de ejemplo;
- exclusión de descartadas;
- identificación de candidato sin contacto;
- preparación de borrador sin envío;
- lenguaje neutral respecto de proveedores.

## Veredicto

```text
INTERFAZ VISUAL MVP: CONTRACTUALMENTE CERRADA
DATOS REALES: SÍ
REVISIÓN HUMANA: PRESERVADA
CONTACTO AUTOMÁTICO: NO
DESCARTE OPERATIVO: SÍ
TRAZABILIDAD: SÍ
```
