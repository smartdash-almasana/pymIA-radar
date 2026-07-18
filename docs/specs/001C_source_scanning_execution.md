# SPEC-001C — Plan de ejecución por fuente

**Estado:** IMPLEMENTING

## Propósito

Convertir la cartografía de fuentes de RADAR en una agenda de escaneo reproducible para Inlak'ech.

Esta especificación no clasifica afinidad, intención ni capacidad. Define dónde buscar, cómo ingresar cada hallazgo y cómo medir el rendimiento de cada fuente.

## Entradas

- `config/conversational_scanning_matrix.v1.json`;
- `config/concrete_sources.v1.json`;
- `config/source_scanning_plans.v1.json`;
- política maestra de radarización;
- evidencia de investigación sobre Chichén Itzá, Valladolid, Yucatán y comunidades globales afines.

## Contrato operativo

Cada fuente concreta debe tener exactamente un plan con:

- estado operativo;
- frecuencia;
- modalidad de captura;
- consultas iniciales;
- campos obligatorios;
- requisitos de configuración;
- métricas;
- restricciones y notas.

## Estados

- `ACTIVE`: puede ejecutarse con la infraestructura actual;
- `ASSISTED`: requiere captura o revisión humana;
- `CONFIG_REQUIRED`: existe integración, pero falta configuración o autorización;
- `DISCOVERY_REQUIRED`: primero debe localizarse una instancia, grupo o feed concreto;
- `INSTITUTIONAL`: exige participación, alianza o relación legítima;
- `DEFERRED`: queda expresamente pospuesto.

## Reglas

1. Ninguna fuente concreta puede quedar sin plan.
2. Una fuente no puede tener dos planes activos contradictorios.
3. No se automatiza contenido privado, cerrado o no autorizado.
4. Las fuentes institucionales no se tratan como repositorios para extracción.
5. Todo hallazgo debe poder normalizarse a la entrada común de RADAR.
6. La calidad conversacional se evalúa después de la captura.
7. Aprendizaje, visita, colaboración, residencia e inversión se conservan como intenciones distintas.
8. No se contacta automáticamente.

## Primer lote ejecutable

El primer lote real debe incluir:

- Permies;
- Foros Ciudadanos de Yucatán, cuando exista conversación verificable;
- YouTube y comentarios, una vez configurados;
- Reddit mediante acceso autorizado o captura asistida;
- grupos públicos de Facebook mediante captura asistida;
- Tripadvisor Chichén Itzá;
- descubrimiento de grupos y feeds de Meetup.

## Métricas mínimas

- resultados recuperados;
- tasa de conversaciones sustantivas;
- señales por tipo de intención;
- ruido y falsos positivos;
- duplicados;
- cobertura territorial;
- costo operativo por fuente;
- restricciones o fallos de acceso.

## Gate de cierre

Pasa a `VERIFIED` cuando:

1. los 15 planes carguen y cubran las 15 fuentes concretas;
2. la suite completa pase;
3. se ejecute un primer lote real en al menos tres modalidades: automática, asistida e institucional o de descubrimiento;
4. exista un informe comparativo de rendimiento por fuente;
5. ningún resultado haya sido incorporado mediante edición manual de la base de datos.
