# Método de desarrollo

## 1. Enfoque

El proyecto usa **Spec-Driven Development liviano con cortes verticales**.

Cada especificación describe una capacidad completa y observable:

```text
entrada real
→ procesamiento
→ decisión
→ persistencia
→ resultado visible
```

No se desarrollan capas aisladas durante semanas sin demostrar el circuito.

## 2. Unidad de trabajo

Cada capacidad se documenta en `docs/specs/`.

Una especificación debe contener:

1. propósito;
2. alcance;
3. entradas;
4. salidas;
5. reglas;
6. casos límite;
7. criterios de aceptación;
8. pruebas obligatorias;
9. dependencias;
10. exclusiones.

## 3. Ciclo obligatorio

### Paso 1 — Auditar

Leer el código y la documentación de las dependencias reales.

### Paso 2 — Especificar

Redactar el comportamiento antes de programarlo.

### Paso 3 — Aprobar

Confirmar que el alcance coincide con la meta del cliente.

### Paso 4 — Implementar

Construir el menor corte vertical que cumpla la especificación.

### Paso 5 — Verificar

Ejecutar pruebas focales y una prueba de extremo a extremo.

### Paso 6 — Cerrar

Actualizar:

- estado de la especificación;
- matriz de aceptación;
- decisiones técnicas;
- riesgos;
- siguiente capacidad.

## 4. Gates

### Gate A — Descubrimiento real

No avanzar al clasificador hasta obtener conversaciones reales con:

- fuente;
- URL;
- texto;
- fecha;
- consulta de origen.

### Gate B — Persistencia confiable

No avanzar a bandeja hasta asegurar:

- deduplicación;
- trazabilidad;
- reejecución sin corrupción.

### Gate C — Afinidad explicable

No avanzar al contacto hasta que cada evaluación incluya:

- puntaje;
- evidencia;
- faltantes;
- señales negativas;
- recomendación.

### Gate D — Revisión humana

No conectar acciones externas sin:

- aprobar;
- editar;
- descartar;
- registrar quién decidió.

### Gate E — CRM real

No considerar integrada a Relaticle hasta crear y leer registros mediante su API real.

### Gate F — Precalificación

No marcar un lead como calificado sin respuestas mínimas y reglas explícitas.

## 5. Definición global de terminado

El producto queda terminado cuando una ejecución real demuestra:

```text
consulta
→ conversación encontrada
→ evaluación explicable
→ revisión humana
→ acercamiento aprobado
→ respuesta del interesado
→ cuestionario
→ lead calificado
→ oportunidad registrada en Relaticle
```
