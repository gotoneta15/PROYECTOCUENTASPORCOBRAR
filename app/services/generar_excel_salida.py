"""R7 - Generar Excel de salida.

Toma los datos procesados de todos los clientes (desde R1 hasta R6) y
genera un archivo Excel de salida con los resultados, listo para descargar.
"""

from pathlib import Path
from typing import Any

import openpyxl

COLUMNAS_SALIDA = [
    "Cliente",
    "Ruta",
    "Unidad_Comercio",
    "Fecha_Corte",
    "Sin_Vencer",
    "Vencido_1_30",
    "Vencido_31_60",
    "Vencido_61_90",
    "Vencido_Mas_90",
    "Total_Cartera",
    "vencidos_totales",
    "porcentaje_vencido",
    "vencidos_mas_30_dias",
]


def generar_excel_salida(
    datos_procesados: list[dict[str, Any]],
    ruta_salida: str = "salida/resultado_cartera.xlsx",
) -> str:
    """Genera un archivo Excel de salida con los datos procesados.

    Args:
        datos_procesados: Lista de diccionarios con los datos de cada cliente
                          (salida de R6 - Identificar vencidos > 30 días).
        ruta_salida: Ruta donde se guardará el archivo Excel de salida.

    Returns:
        Ruta al archivo generado.

    Raises:
        ValueError: Si la lista de datos está vacía.
    """
    if not datos_procesados:
        raise ValueError("No hay datos para escribir en el Excel de salida.")

    path = Path(ruta_salida)
    path.parent.mkdir(parents=True, exist_ok=True)

    workbook = openpyxl.Workbook()
    hoja = workbook.active
    hoja.title = "Resultado_Cartera"

    # Escribir encabezados
    for col_idx, columna in enumerate(COLUMNAS_SALIDA, start=1):
        hoja.cell(row=1, column=col_idx, value=columna)

    # Escribir filas de datos
    for fila_idx, cliente in enumerate(datos_procesados, start=2):
        for col_idx, columna in enumerate(COLUMNAS_SALIDA, start=1):
            valor = cliente.get(columna)
            hoja.cell(row=fila_idx, column=col_idx, value=valor)

    workbook.save(path)
    return str(path)


if __name__ == "__main__":
    # Prueba rápida integrada con R1 a R6
    from app.services.importar_excel import importar_excel
    from app.services.calcular_totales import calcular_totales
    from app.services.calcular_porcentajes import calcular_porcentajes
    from app.services.ordenar_riesgo import ordenar_riesgo
    from app.services.identificar_vencidos import identificar_vencidos_mas_30

    registros = importar_excel("insumos/Base_Datos_Proyecto_IA_Cartera.xlsx")
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    vencidos = identificar_vencidos_mas_30(ordenados)

    # Combinar ambas listas (con y sin vencidos > 30) para el Excel de salida
    todos = (
        vencidos["clientes_con_vencidos_mas_30"]
        + vencidos["clientes_sin_vencidos_mas_30"]
    )

    ruta = generar_excel_salida(todos)
    print(f"Excel de salida generado: {ruta}")
    print(f"Registros escritos: {len(todos)}")
    print(f"Columnas: {COLUMNAS_SALIDA}")
