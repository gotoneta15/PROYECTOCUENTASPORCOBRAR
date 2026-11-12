# PLAN.md — Plan de entregas del proyecto Cartera360

## 1. RESUMEN (5 líneas)

Vamos a construir Cartera360, una aplicación web en Python + Flask con patrón MVC que automatiza el análisis de antigüedad de saldos de cuentas por cobrar. Entra un Excel de insumos con columnas de cartera (Sin_Vencer, Vencido_1_30, etc.) y el agente de IA devuelve riesgo, semáforo y recomendación por cliente en formato JSON. Sale una pantalla con indicadores, semáforos, ranking de clientes, gráficos y un archivo Excel descargable. Los usuarios que deciden son Encargado de Cuentas por Cobrar, Encargado de Ruta y Jefe Financiero.

---

## 2. LO QUE ENCONTRÉ

### En contexto/ (Contexto_Mi_App.md)
- App: Cartera360, web para análisis de antigüedad de cuentas por cobrar.
- Datos de entrada (10 columnas): Fecha_Corte, Unidad_Comercio, Ruta, Cliente, Sin_Vencer, Vencido_1_30, Vencido_31_60, Vencido_61_90, Vencido_Mas_90, Total_Cartera.
- Reglas de negocio R1 a R10 (Importar Excel, Validar columnas, Calcular totales, Calcular porcentajes, Ordenar por riesgo, Vencidos >30 días, Excel de salida, Gráficos e indicadores, Clientes sin ruta, Saldos negativos por notas de crédito).
- Agente de IA: contrato JSON con 11 campos (cliente, ruta, total_cartera, porcentaje_vencido, nivel_riesgo, semaforo, accion_recomendada, motivo, suspender_credito, escalar_gerencia, enviar_recordatorio).
- Cifras de control: Cliente001 → Sin_Vencer=1.000.000, Vencido_1_30=500.000, Vencido_31_60=250.000, Vencido_61_90=50.000 → Semáforo Rojo, Prioridad Alta, Suspender crédito Sí, Escalar Sí, Recordatorio Sí.
- Casos límite: saldo negativo por nota de crédito, cliente sin ruta, archivo vacío o con columnas faltantes.
- Reglas del sistema: Python + Flask, MVC, uv, llaves en .env, iniciar_app.bat, pantallas en español, prohibido inventar reglas/campos.
- Supuestos por confirmar: históricos para detectar aumento de deuda, correo corporativo para avisos, umbrales de semáforo.

### En insumos/
- Archivo: `Base_Datos_Proyecto_IA_Cartera.xlsx` (1 hoja: "Cartera").
- 61 filas totales = 1 encabezado + 60 registros de datos.
- 10 columnas que coinciden exactamente con las del contexto: Fecha_Corte, Unidad_Comercio, Ruta, Cliente, Sin_Vencer, Vencido_1_30, Vencido_31_60, Vencido_61_90, Vencido_Mas_90, Total_Cartera.
- También existe `~$Base_Datos_Proyecto_IA_Cartera.xlsx` (archivo temporal de Excel, se ignora).

### ¿Coincide con AGENTS.md?
- **AGENTS.md no existe todavía** en la raíz del proyecto. Debe crearse antes de construir.

### Qué falta o no cuadra
1. **Contradicción en cifras de control**: El contexto dice que Cliente001 tiene Sin_Vencer=1.000.000, Vencido_1_30=500.000, Vencido_31_60=250.000, Vencido_61_90=50.000. Pero en el Excel real, Cliente001 (fila de datos 2) tiene Sin_Vencer=2.300.000, Vencido_1_30=200.000, Vencido_31_60=75.000, Vencido_61_90=25.000, Vencido_Mas_90=10.000, Total_Cartera=2.610.000. **No cuadran.** El tester no podrá validar contra ambas al mismo tiempo.
2. **Archivos mencionados en el contexto que no existen**: `.env` y `iniciar_app.bat` están listados en las reglas del sistema pero no están en el proyecto.
3. **Supuestos sin confirmar**: históricos, correo corporativo y umbrales de semáforo están pendientes.

---

## 3. ENTREGAS POR SUBAGENTE

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 1 | @arquitecto | PLAN.md (este archivo) | `PLAN.md` | — | Se lee este documento y se aprueba |
| 2 | @backend | Estructura MVC base con `uv`: `app/__init__.py` con `create_app()`, `app/controllers/`, `app/services/`, `wsgi.py` | `app/__init__.py`, `app/controllers/`, `app/services/`, `wsgi.py`, `pyproject.toml` (uv) | PLAN.md aprobado | Ejecutar `uv run flask --app wsgi.py run` y ver que la app arranca sin errores |
| 3 | @backend | R1 Importar Excel: leer `Base_Datos_Proyecto_IA_Cartera.xlsx` y devolver los 60 registros | `app/services/importar_excel.py` | Estructura MVC base | En pantalla (o consola) se ven 60 filas cargadas con las 10 columnas |
| 4 | @backend | R2 Validar columnas: verificar que el Excel tenga exactamente las 10 columnas esperadas | `app/services/validar_columnas.py` | R1 (datos cargados) | Mensaje "Columnas válidas" o error si faltan columnas |
| 5 | @backend | R3 Calcular totales: sumar Sin_Vencer, Vencido_1_30, Vencido_31_60, Vencido_61_90, Vencido_Mas_90, Total_Cartera | `app/services/calcular_totales.py` | R2 (columnas validadas) | Totales mostrados en consola o pantalla |
| 6 | @backend | R4 Calcular porcentajes: porcentaje_vencido = (vencidos totales / Total_Cartera) * 100 por cliente | `app/services/calcular_porcentajes.py` | R3 (totales) | Porcentaje de vencido visible por cliente |
| 7 | @backend | R5 Ordenar clientes por riesgo (mayor porcentaje_vencido primero) | `app/services/ordenar_riesgo.py` | R4 (porcentajes) | Lista ordenada de mayor a menor riesgo |
| 8 | @backend | R6 Identificar clientes con vencidos mayores a 30 días (Vencido_31_60 + Vencido_61_90 + Vencido_Mas_90 > 0) | `app/services/identificar_vencidos.py` | R5 (ordenados) | Indicador de clientes con vencidos >30 días |
| 9 | @backend | R7 Generar Excel de salida con resultados | `app/services/generar_excel_salida.py` | R6 (vencidos identificados) | Archivo Excel descargable generado |
| 10 | @backend | R8 Generar gráficos e indicadores (contadores globales) | `app/services/generar_indicadores.py` | R7 (Excel de salida) | Indicadores y gráficos disponibles para el frontend |
| 11 | @backend | R9 Detectar clientes sin ruta (campo Ruta vacío) | `app/services/detectar_sin_ruta.py` | R8 (indicadores) | Lista de clientes sin ruta |
| 12 | @backend | R10 Detectar saldos negativos por notas de crédito (cualquier campo de saldo < 0) | `app/services/detectar_saldos_negativos.py` | R9 (clientes sin ruta) | Lista de clientes con saldo negativo |
| 13 | @backend | Integración agente de IA: leer llave de `.env`, enviar contrato JSON (11 campos), recibir nivel_riesgo, semaforo, accion_recomendada, etc. | `app/services/agente_ia.py`, `.env` (plantilla) | R1-R10 completas | Respuesta JSON válida del agente con los 11 campos |
| 14 | @backend | `iniciar_app.bat`: abre el navegador y enciende la app Flask | `iniciar_app.bat` | Integración agente IA | Doble clic en `iniciar_app.bat` abre el navegador con la app |
| 15 | @frontend | Pantalla de inicio: formulario para cargar/seleccionar el Excel de insumos | `app/templates/inicio.html`, CSS en `base.html` | Backend listo (R1-R13) | Pantalla de inicio carga y permite seleccionar archivo |
| 16 | @frontend | Pantalla de resultados: contadores grandes (indicadores), semáforos, tabla con filtro, ranking de clientes | `app/templates/resultados.html`, `app/static/` | Pantalla de inicio | Se ven contadores, tabla filtrar, ranking y semáforos |
| 17 | @frontend | Detalle por registro: al clic en un cliente se ve su desglose completo | `app/templates/detalle.html` (o modal en resultados) | Pantalla de resultados | Al seleccionar un cliente se muestra su detalle |
| 18 | @tester | Pruebas en `tests/` con pytest contra cifras de control y casos límite + `VALIDACION.md` (esperado vs obtenido) | `tests/test_*.py`, `VALIDACION.md` | Backend + frontend completos | Se ejecutan pruebas y se ven resultados PASAR/FALLAR |
| 19 | @revisor | Revisión de seguridad: llaves en código, `.gitignore`, datos sensibles, todo esté en AGENTS.md | `revision_seguridad.md` (solo lectura, no modifica app) | Todo completo | Lista de hallazgos con prioridad y corrección propuesta |

> Cada entrega es pequeña: construible y verificable en pocos minutos.

---

## 4. PUNTOS DE CONTROL

| Después de entrega | Quién interviene | Qué debe verse en pantalla exactamente |
|--------------------|------------------|----------------------------------------|
| 3 (R1 Importar Excel) | @tester | 60 registros cargados, 10 columnas, sin errores de importación |
| 5-6 (R3, R4) | @tester | Totales y porcentajes de vencido calculados correctamente |
| 7 (R5 Ordenar por riesgo) | @tester | Cliente con mayor porcentaje_vencido aparece primero |
| 13 (Agente de IA) | @tester + @revisor | Respuesta JSON con los 11 campos del contrato; llave leída de `.env` (no hardcodeada) |
| 16 (Pantalla de resultados) | @tester | Contadores grandes, tabla con filtro, semáforos visibles |
| 18 (Cifras de control) | @tester | **ATENCIÓN:** hay contradicción entre el contexto (Cliente001: Sin_Vencer=1.000.000, Vencido_1_30=500.000...) y el Excel real (Cliente001: Sin_Vencer=2.300.000, Vencido_1_30=200.000...). El tester reportará la diferencia con su causa probable sin ajustar números. |
| 19 (Revisor) | @revisor | Lista de hallazgos de seguridad; ninguna llave en código; `.gitignore` correcto |

---

## 5. RIESGOS

| Riesgo | Qué hará cada subagente |
|--------|------------------------|
| Datos incompletos (columnas faltantes en el Excel) | @backend: R2 valida columnas y devuelve error claro. @frontend: muestra mensaje amigable al usuario. @revisor: verifica que no se inventen columnas. |
| Archivo vacío o sin filas | @backend: R1 detecta archivo vacío y lo reporta. @tester: prueba caso límite de archivo vacío. |
| Respuesta del agente de IA que no es JSON válido | @backend: valida que la respuesta sea JSON; si falla, devuelve error y no inventa datos. @tester: prueba con respuesta malformada. |
| Llave de API gratis con límites de uso | @backend: lee llave de `.env` y maneja errores de cuota/límite sin fallar la app. @revisor: verifica que la llave no esté hardcodeada. |
| Contradicción entre cifras de control del contexto y datos reales del Excel | @tester: reporta la diferencia con causa probable, sin ajustar números. @arquitecto: plantea la pregunta al usuario para definir fuente de verdad. |
| Archivos escaneados (no aplica a este Excel, pero posible futuro) | @backend: rechaza archivos que no sean Excel válido con mensaje claro. |

---

## 6. PREGUNTAS PARA MÍ

Antes de empezar a construir, necesito que confirmes:

1. **AGENTS.md**: ¿Lo creo yo basándome en el contexto y los insumos, o prefieres que lo definas tú primero?
2. **Cifras de control**: ¿Cuál es la fuente de verdad para validar: el documento de contexto (Cliente001: Sin_Vencer=1.000.000...) o el Excel real (Cliente001: Sin_Vencer=2.300.000...)? Esto afecta directamente a las pruebas del @tester.
3. **Archivo de insumos**: ¿Confirmas que `Base_Datos_Proyecto_IA_Cartera.xlsx` es el único archivo de entrada y que la hoja se llama "Cartera"?
4. **Supuestos por confirmar**: ¿Asumimos que NO existen históricos, NO hay correo corporativo y NO hay umbrales de semáforo definidos aún (marcándolos como pendientes en AGENTS.md), o quieres que los implemente de alguna forma provisional?
5. **Archivos faltantes**: ¿Debo crear `.env` (plantilla con la variable de la llave) y `iniciar_app.bat` aunque aún no existan, o esperamos a que los definas?

**Espera mi aprobación de la tabla de entregas antes de que cualquier subagente empiece a construir.**
