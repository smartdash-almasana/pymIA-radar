# HIGGSFIELD SKILLS — ADOPCIÓN CONTROLADA V1

**Estado:** APPROVED  
**Ámbito:** herramientas creativas y de presentación vinculadas a Inlak’ech y RADAR  
**Repositorio evaluado:** `higgsfield-ai/skills`

---

## 1. Decisión

Se autoriza incorporar Higgsfield Skills como herramienta externa opcional para producción visual, audiovisual y sitios promocionales.

No se autoriza utilizar Higgsfield para redefinir la arquitectura productiva de RADAR ni para sustituir su aplicación FastAPI + HTMX.

---

## 2. Capacidades relevantes

El repositorio ofrece siete skills:

- `higgsfield-generate`;
- `higgsfield-soul-id`;
- `higgsfield-product-photoshoot`;
- `higgsfield-marketplace-cards`;
- `higgsfield-websites`;
- `higgsfield-video-explainer`;
- `higgsfield-game-generation`.

Para Inlak’ech y RADAR se consideran directamente útiles:

1. `higgsfield-generate`
   - imágenes de campaña;
   - video promocional;
   - piezas sociales;
   - loops visuales y recursos para landing pages.

2. `higgsfield-product-photoshoot`
   - hero banners;
   - piezas visuales de marca;
   - carruseles sociales;
   - material de campañas.

3. `higgsfield-video-explainer`
   - presentación audiovisual de Inlak’ech;
   - explicación del funcionamiento de RADAR;
   - materiales de onboarding o demostración.

4. `higgsfield-websites`
   - prototipos o landing pages promocionales separadas;
   - no puede reemplazar ni migrar la interfaz operativa de RADAR sin una especificación independiente aprobada.

Las demás skills quedan disponibles, pero no tienen uso productivo autorizado dentro del MVP actual.

---

## 3. Límites obligatorios

Higgsfield no puede:

- modificar el flujo de descubrimiento de RADAR;
- intervenir en Playwright, Evidence Pipe, semántica o revisión humana;
- crear un frontend paralelo para RADAR;
- migrar RADAR a React, TanStack Start o Cloudflare;
- desplegar infraestructura sin autorización expresa;
- generar ni publicar contenido automáticamente;
- usar rostros reales sin autorización y material de referencia legítimo;
- realizar cargos, consumir créditos o iniciar trabajos pagos sin confirmación humana;
- introducir secretos, tokens o credenciales en el repositorio.

---

## 4. Regla para `higgsfield-websites`

`higgsfield-websites` utiliza React 19, TanStack Start y Cloudflare.

Ese stack es incompatible con la arquitectura actual de RADAR como reemplazo directo. Solo puede usarse para:

- landing pages externas;
- micrositios promocionales;
- prototipos aislados;
- demostraciones visuales.

Nunca debe utilizarse para reescribir la bandeja HTMX ni el backend actual sin una decisión arquitectónica explícita del usuario.

---

## 5. Instalación

La instalación recomendada por el proyecto es:

```text
npx skills add higgsfield-ai/skills
```

La CLI de Higgsfield requiere autenticación mediante navegador y una cuenta con plan o créditos disponibles.

Por lo tanto:

- la instalación técnica puede ejecutarla OpenCode;
- la autenticación debe completarla el usuario;
- ninguna generación paga debe iniciarse sin aprobación humana;
- la verificación inicial debe limitarse a comprobar instalación, versión y estado de cuenta;
- no se ejecutará una generación de prueba que consuma créditos sin consentimiento.

---

## 6. Uso autorizado en este proyecto

### Permitido

- generar assets visuales para una landing de Inlak’ech;
- crear banners, imágenes hero y piezas sociales;
- generar un video explicativo aprobado;
- experimentar con una landing externa;
- evaluar una pieza creativa antes de incorporarla manualmente.

### No permitido dentro del MVP RADAR

- cambiar la arquitectura productiva;
- agregar Higgsfield como dependencia runtime de RADAR;
- invocar su API desde el flujo de descubrimiento;
- almacenar credenciales en `.env` versionado;
- automatizar publicaciones o campañas;
- incorporar costos operativos sin aprobación.

---

## 7. Relación con otras herramientas

```text
Ponytail
→ controla simplicidad y sobreingeniería del código

Impeccable
→ controla calidad visual y UX del frontend

Higgsfield Skills
→ produce assets creativos, audiovisuales y sitios promocionales

Contratos RADAR
→ gobiernan producto, arquitectura y comportamiento
```

Ninguna de estas herramientas puede sobreescribir los contratos del repositorio.

---

## 8. Criterio de adopción

La incorporación se considera correcta cuando:

- las skills están instaladas en el entorno del agente, no dentro del runtime de RADAR;
- la autenticación queda fuera del repositorio;
- no se consumen créditos sin autorización;
- RADAR conserva FastAPI + HTMX;
- los activos generados se revisan manualmente antes de incorporarse;
- toda landing o micrositio externo se mantiene separado del flujo operativo.

---

## 9. Veredicto

```text
UTILIDAD PARA LANDINGS Y CAMPAÑAS: ALTA
UTILIDAD PARA ASSETS VISUALES: ALTA
UTILIDAD PARA BACKEND RADAR: NULA
UTILIDAD PARA PLAYWRIGHT/SEMÁNTICA: NULA
RIESGO DE DERIVA ARQUITECTÓNICA: ALTO SI SE USA WEBSITES SIN LÍMITES
ADOPCIÓN: AUTORIZADA CON ALCANCE CONTROLADO
```
