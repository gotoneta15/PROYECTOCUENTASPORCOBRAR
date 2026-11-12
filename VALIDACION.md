# VALIDACION.md — Resultado de pruebas vs cifras de control

Este documento compara los resultados obtenidos por la aplicación con las **cifras de control** y los **casos límite** definidos en el documento de contexto (AGENTS.md).

## Fuente de datos

- **Archivo de insumos:** `insumos/Base_Datos_Proyecto_IA_Cartera.xlsx`
- **Hoja:** Cartera
- **Registros:** 60 clientes (Cliente001 a Cliente060)
- **Fecha de corte:** 30/09/2026

---

## 1. CIFRAS DE CONTROL — Cliente001

El documento de contexto (sección 9) establece estas cifras esperadas para Cliente001:

| Campo | Esperado (contexto) | Obtenido (Excel real) | ¿Coincide? |
|-------|---------------------|----------------------|------------|
| Sin_Vencer | 1.000.000 | 2.300.000 | ❌ NO |
| Vencido_1_30 | 500.000 | 200.000 | ❌ NO |
| Vencido_31_60 | 250.000 | 75.000 | ❌ NO |
| Vencido_61_90 | 50.000 | 25.000 | ❌ NO |
| Vencido_Mas_90 | — | 10.000 | — |
| Total_Cartera | — | 2.610.000 | — |

**Resultado esperado del contexto:** Semáforo Rojo, Prioridad Alta, Suspender crédito Sí, Escalar Sí, Recordatorio Sí.

**Resultado obtenido con datos reales del Excel:**
- Sin_Vencer: 2.300.000
- Vencido_1_30: 200.000
- Vencido_31_60: 75.000
- Vencido_61_90: 25.000
- Vencido_Mas_90: 10.000
- Total_Cartera: 2.610.000
- vencidos_totales: 310.000
- porcentaje_vencido: 11.88%
- Nivel de riesgo: Bajo
- Semáforo: Verde

**Conclusión:** Las cifras de control del contexto **no coinciden** con los datos reales del archivo de insumos. Esta contradicción ya fue reportada en PLAN.md (sección 6, pregunta 2). El tester no ajusta números; reporte la diferencia con su causa probable: el documento de contexto puede basarse en una versión anterior o de ejemplo del archivo, mientras que el Excel real contiene datos actualizados.

---

## 2. CASOS LÍMITE

| Caso límite | Esperado | Obtenido | Estado |
|-------------|----------|----------|--------|
| Saldo negativo por nota de crédito | Detectar cliente con saldo < 0 | 0 clientes con saldo negativo | ✅ Pasa (ningún saldo negativo en datos reales) |
| Cliente sin ruta asignada | Detectar cliente con Ruta vacía | 0 clientes sin ruta | ✅ Pasa (todos tienen ruta en datos reales) |
| Archivo vacío | Rechazar con error claro | No probado con archivo vacío | ⏳ Pendiente |
| Archivo con columnas faltantes | Rechazar con error claro | No probado con columnas faltantes | ⏳ Pendiente |

---

## 3. INDICADORES GLOBALES (obtenidos del Excel real)

| Indicador | Valor |
|-----------|-------|
| Total clientes | 60 |
| Total Cartera | 223.050.000 |
| Total Sin Vencer | 201.000.000 |
| Total Vencidos | 22.050.000 |
| Total Vencidos > 30 días | 7.050.000 |
| % Vencido Global | 9.89% |
| Clientes Crítico (>=50%) | 0 |
| Clientes Alto (>=30%) | 0 |
| Clientes Medio (>=10%) | 30 |
| Clientes Bajo (<10%) | 30 |

---

## 4. RESUMEN DE PRUEBAS Pytest

| Archivo de prueba | Casos | Estado |
|-------------------|-------|--------|
| tests/test_importar_excel.py | 4 | ✅ Pasan |
| tests/test_validar_columnas.py | 3 | ✅ Pasan |
| tests/test_calcular_totales.py | 4 | ✅ Pasan |
| tests/test_calcular_porcentajes.py | 3 | ✅ Pasan |
| tests/test_ordenar_riesgo.py | 3 | ✅ Pasan |
| tests/test_identificar_vencidos.py | 3 | ✅ Pasan |
| tests/test_detectar_sin_ruta.py | 3 | ✅ Pasan |
| tests/test_detectar_saldos_negativos.py | 3 | ✅ Pasan |
| tests/test_generar_indicadores.py | 3 | ✅ Pasan |
| **Total** | **29** | **✅ Todas pasan** |

---

## 5. NOTAS

- Las pruebas validan la lógica de negocio (código, sin IA) contra los datos reales del archivo de insumos.
- La contradicción en las cifras de control (Cliente001) no se resuelve ajustando números; se documenta aquí para que el usuario defina la fuente de verdad.
- Los casos límite de archivo vacío y columnas faltantes están cubiertos por el código (R1 y R2 lanzan excepciones), pero no se ejecutaron con archivos de prueba reales en esta entrega.
