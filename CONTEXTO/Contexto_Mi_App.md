DOCUMENTO DE CONTEXTO · Cartera360
1. Qué es esta app 
Cartera360 es una aplicación web para automatizar el análisis de antigüedad de saldos de cuentas por cobrar. Usuarios: Encargado de Cuentas por Cobrar, Encargado de Ruta y Jefe Financiero.
2. El proceso hoy 
Ingresar a Oracle, generar reporte, exportar a Excel, calcular porcentajes, identificar clientes críticos, asignar prioridad, generar gráficos y enviar correos. Tiempo: 3 a 4 horas por día.
3. Datos de entrada 
Fecha_Corte, Unidad_Comercio, Ruta, Cliente, Sin_Vencer, Vencido_1_30, Vencido_31_60, Vencido_61_90, Vencido_Mas_90, Total_Cartera.
4. Reglas de negocio para el código 
R1 Importar Excel. 
R2 Validar columnas. 
R3 Calcular totales. 
R4 Calcular porcentajes. 
R5 Ordenar clientes por riesgo. 
R6 Identificar clientes con vencidos mayores a 30 días. 
R7 Generar Excel de salida. 
R8 Generar gráficos e indicadores. 
R9 Detectar clientes sin ruta. 
R10 Detectar saldos negativos por notas de crédito.
5. Lo que hace el agente de IA 
Rol: Analista virtual de cartera. 
Nunca inventa datos. Si falta información devuelve: no indicado. 
Devuelve riesgo, semáforo y recomendación. 
Contrato JSON: cliente, ruta, total_cartera, porcentaje_vencido, nivel_riesgo, semaforo, accion_recomendada, motivo, suspender_credito, escalar_gerencia, enviar_recordatorio.
6. Qué produce la app 
Pantalla con indicadores, semáforos, ranking de clientes, gráficos y archivo Excel descargable.
7. Quién decide 
Encargado de Cuentas por Cobrar, Encargado de Ruta y Jefe Financiero.
8. Datos de prueba 
Clientes sin vencimiento, clientes críticos y casos con notas de crédito o sin ruta.
9. Cifras de control 
Cliente001: Sin_Vencer=1000000, Vencido_1_30=500000, Vencido_31_60=250000, Vencido_61_90=50000. 
Resultado esperado: Semáforo Rojo, Prioridad Alta, Suspender crédito Sí, Escalar Sí, Recordatorio Sí.
10. Casos límite 
Saldo negativo por nota de crédito. 
Cliente sin ruta asignada. 
Archivo vacío o con columnas faltantes.
11. Reglas del sistema 
Python + Flask, patrón MVC, gestionado con uv. Llaves en .env. Archivo iniciar_app.bat. Pantallas en español. Prohibido inventar reglas o campos.
12. Supuestos por confirmar 
Existencia de históricos para detectar aumento de deuda. Uso de correo corporativo para avisos. Definición futura de umbrales de semáforo.
