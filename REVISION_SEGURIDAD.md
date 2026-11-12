# REVISION_SEGURIDAD.md — Informe de hallazgos del @revisor

Este documento entrega una lista de hallazgos encontrados durante la revisión de seguridad y cumplimiento de reglas del proyecto Cartera360. **No se modificó ningún archivo**; solo se reportan hallazgos con prioridad y corrección propuesta.

---

## Metodología

Se revisaron todos los archivos de código Python, plantillas HTML, scripts de inicio, archivos de configuración y el archivo `.env`. Se comparó contra lo definido en `contexto/Contexto_Mi_App.md` y `PLAN.md` (AGENTS.md no existe aún).

---

## Hallazgos

### 1. Ausencia de archivo `.gitignore` — PRIORIDAD: ALTA

**Descripción:** No existe un archivo `.gitignore` en la raíz del proyecto. Sin él, archivos y carpetas sensibles podrían subirse accidentalmente a GitHub, incluyendo:
- `.env` con la llave de API
- `.venv/` (entorno virtual completo)
- `__pycache__/` (archivos compilados de Python)
- `instance/` (copias de archivos Excel subidos por usuarios)
- `salida/` (archivos Excel generados)
- `uv.lock` (puede contener rutas o versiones sensibles)
- `.pytest_cache/`

**Archivos expuestos actualmente en el proyecto que NO deberían subirse:**
- `.env` (contiene `IA_API_KEY=tu_llave_de_api_aqui`)
- `.venv/` (directorio completo del entorno virtual)
- `__pycache__/` (en app/, app/controllers/, app/services/, tests/)
- `instance/Base_Datos_Proyecto_IA_Cartera.xlsx` (copia de archivo de usuario)
- `salida/resultado_cartera.xlsx` (archivo generado)
- `.pytest_cache/`

**Corrección propuesta:** Crear un archivo `.gitignore` con al menos:
```
.env
.venv/
__pycache__/
*.pyc
instance/
salida/
.pytest_cache/
*.egg-info/
.idea/
.vscode/
.DS_Store
```

---

### 2. Llave de API en archivo `.env` sin valor real — PRIORIDAD: ALTA

**Descripción:** El archivo `.env` existe y contiene `IA_API_KEY=tu_llave_de_api_aqui`. Aunque es un placeholder y no una llave real, el archivo en sí debería estar en `.gitignore` para evitar que se suba con una llave real en el futuro.

**Corrección propuesta:** Agregar `.env` al `.gitignore` y documentar que los desarrolladores deben crear su propio `.env` local con una llave real.

---

### 3. Modo debug activado en `.env` — PRIORIDAD: MEDIA

**Descripción:** El archivo `.env` tiene `FLASK_DEBUG=1`. En producción, esto expendería stack traces, código fuente y variables de entorno ante errores, lo cual es un riesgo de información.

**Corrección propuesta:** Cambiar `FLASK_DEBUG=0` para producción, o usar una variable separada `FLASK_ENV=production` y `FLASK_DEBUG=0`.

---

### 4. Umbrales de semáforo y nivel de riesgo hardcodeados — PRIORIDAD: MEDIA

**Descripción:** En `app/controllers/routes.py` (líneas 155-166) se definen umbrales de riesgo directamente en el código:
- >= 50%: Crítico / Rojo
- >= 30%: Alto / Rojo
- >= 10%: Medio / Amarillo
- < 10%: Bajo / Verde

El contexto (sección 12, Supuestos por confirmar) indica que la "Definición futura de umbrales de semáforo" está pendiente. Estos umbrales no están definidos en AGENTS.md ni en el contexto.

**Corrección propuesta:** Mover estos umbrales a variables de entorno o a un archivo de configuración, y documentarlos como pendientes de confirmación por el negocio.

---

### 5. Datos de prueba hardcodeados en bloque `__main__` — PRIORIDAD: BAJA

**Descripción:** En `app/services/agente_ia.py` (líneas 187-192), el bloque `if __name__ == "__main__":` contiene valores hardcodeados:
- cliente="Cliente001", ruta="R001", total_cartera=2610000, porcentaje_vencido=11.88

Son valores de prueba del dataset real, no secretos, pero están embedidos en el código.

**Corrección propuesta:** Remover o parametrizar estos valores; usar argumentos de línea de comandos o variables de entorno para pruebas manuales.

---

### 6. Carpeta `instance/` contiene copia de archivo de usuario — PRIORIDAD: MEDIA

**Descripción:** El archivo `instance/Base_Datos_Proyecto_IA_Cartera.xlsx` es una copia del Excel subido por un usuario a través de la pantalla de inicio. Contiene datos de clientes reales y debería excluirse del control de versiones.

**Corrección propuesta:** Agregar `instance/` al `.gitignore` y considerar limpiar esta carpeta después del procesamiento.

---

### 7. Carpeta `salida/` contiene archivo generado — PRIORIDAD: BAJA

**Descripción:** El archivo `salida/resultado_cartera.xlsx` fue generado por R7 durante las pruebas. Es un archivo de salida derivado, no fuente, y no debería subirse a GitHub.

**Corrección propuesta:** Agregar `salida/` al `.gitignore`.

---

### 8. Archivos `__pycache__` y `.pyc` — PRIORIDAD: BAJA

**Descripción:** Existen múltiples carpetas `__pycache__` con archivos `.pyc` compilados en `app/`, `app/controllers/`, `app/services/` y `tests/`. Estos son artefactos de compilación y no deberían subirse.

**Corrección propuesta:** Agregar `__pycache__/` y `*.pyc` al `.gitignore`.

---

### 9. Protección contra traversal de rutas en subida de archivos — CUMPLE

**Descripción:** En `app/controllers/routes.py` (línea 66) se usa `secure_filename(archivo.filename)` antes de guardar el archivo subido. Esto previene ataques de path traversal.

**Estado:** ✅ Cumple. No se requiere corrección.

---

### 10. Llave de API no está hardcodeada en el código — CUMPLE

**Descripción:** En `app/services/agente_ia.py`, la función `cargar_configuracion_ia()` lee `IA_API_KEY` desde `.env` usando `os.getenv()`. No hay llaves escritas directamente en el código Python.

**Estado:** ✅ Cumple. No se requiere corrección.

---

### 11. Validación de columnas implementada — CUMPLE

**Descripción:** `R2 - Validar columnas` en `app/services/validar_columnas.py` verifica que el archivo tenga exactamente las 10 columnas esperadas y rechaza columnas faltantes o extra.

**Estado:** ✅ Cumple. No se requiere corrección.

---

### 12. No hay CSRF protection en el formulario de subida — PRIORIDAD: MEDIA

**Descripción:** El formulario de subida de archivo en `app/templates/inicio.html` no tiene protección CSRF (Cross-Site Request Forgery). Un atacante podría inducir a un usuario autenticado a subir un archivo malicioso.

**Corrección propuesta:** Agregar protección CSRF usando Flask-WTF o un token CSRF generado por el servidor.

---

### 13. Archivos temporales no se limpian después del procesamiento — PRIORIDAD: BAJA

**Descripción:** En `app/controllers/routes.py`, el archivo subido se guarda en `instance/` pero nunca se elimina después de ser procesado. Con el tiempo, esto acumularía archivos en el servidor.

**Corrección propuesta:** Agregar `os.remove(ruta_temporal)` después de leer el archivo con `importar_excel()`, o limpiar la carpeta `instance/` periódicamente.

---

### 14. Columnas y campos coinciden con AGENTS.md — CUMPLE

**Descripción:** Todas las columnas usadas en el código (`Fecha_Corte, Unidad_Comercio, Ruta, Cliente, Sin_Vencer, Vencido_1_30, Vencido_31_60, Vencido_61_90, Vencido_Mas_90, Total_Cartera`) coinciden exactamente con lo definido en el contexto y AGENTS.md. No se inventaron columnas ni campos.

**Estado:** ✅ Cumple. No se requiere corrección.

---

### 15. Reglas de negocio R1-R10 implementadas según AGENTS.md — CUMPLE

**Descripción:** Todas las reglas de negocio (R1 a R10) están implementadas en los servicios correspondientes y respetan la definición del contexto.

**Estado:** ✅ Cumple. No se requiere corrección.

---

### 16. AGENTS.md no existe — PRIORIDAD: ALTA

**Descripción:** No existe el archivo `AGENTS.md` en la raíz del proyecto. El contexto (sección 11, Reglas del sistema) menciona que todas las reglas deben estar en AGENTS.md, pero este archivo no fue creado.

**Corrección propuesta:** Crear `AGENTS.md` con las secciones definidas en el contexto: Qué es esta app, Datos de entrada, Reglas de negocio, Lo que hace el agente de IA (contrato JSON), Qué produce la app, Quién decide, Cifras de control, Casos límite, Reglas del sistema.

---

## Resumen de prioridades

| Prioridad | Cantidad | Hallazgos |
|-----------|----------|-----------|
| Alta | 3 | Falta `.gitignore`; `.env` expuesto; Falta `AGENTS.md` |
| Media | 3 | `FLASK_DEBUG=1`; Umbrales hardcodeados; Falta CSRF protection |
| Baja | 3 | Datos de prueba hardcodeados; `instance/` expuesto; Archivos temporales no limpiados |

---

## Próximos pasos recomendados

1. Crear `.gitignore` inmediatamente (alta prioridad).
2. Crear `AGENTS.md` con las reglas del proyecto (alta prioridad).
3. Cambiar `FLASK_DEBUG=0` en `.env` para producción (media prioridad).
4. Mover umbrales de semáforo a configuración externa (media prioridad).
5. Agregar protección CSRF al formulario de subida (media prioridad).
6. Limpiar archivos temporales después del procesamiento (baja prioridad).

---

**Revisor:** @revisor  
**Fecha:** 04/11/2026  
**Estado:** Revisión completada sin modificaciones al código
