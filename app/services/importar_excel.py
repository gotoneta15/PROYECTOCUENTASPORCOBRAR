"""R1 - Importar Excel.

Lee el archivo de insumos de cartera y devuelve los registros como lista de
diccionarios, uno por fila de datos.
"""

from pathlib import Path
from typing import Any

import openpyxl

# Columnas esperadas en el archivo de insumos (según contexto y AGENTS.md)
COLUMNAS_ESPERADAS = [
    "Fecha_Corte",
    "Unidad_Comercio",
    "Ruta",
    "Cliente",
    "Sin_Vencer",
    "Vencido_1_30",
    "Vencido_31_60",
    "Vencido_61_90",
    "Vencido_Mas_90",
    "Total_Cartera",
]

HOJA_CARTERA = "Cartera"


def importar_excel(ruta_archivo: str) -> list[dict[str, Any]]:
    """Importa el Excel de cartera y retorna una lista de diccionarios.

    Cada diccionario representa un cliente con las 10 columnas del insumo.

    Args:
        ruta_archivo: Ruta al archivo .xlsx de insumos.

    Returns:
        Lista de diccionarios con los datos de cada cliente.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo está vacío o no tiene la hoja esperada.
    """
    path = Path(ruta_archivo)

    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

    workbook = openpyxl.load_workbook(path, data_only=True)

    if HOJA_CARTERA not in workbook.sheetnames:
        raise ValueError(
            f"La hoja '{HOJA_CARTERA}' no existe en el archivo. "
            f"Hojas disponibles: {workbook.sheetnames}"
        )

    hoja = workbook[HOJA_CARTERA]

    # Leer encabezados de la primera fila
    encabezados = []
    for celda in hoja[1]:
        valor = celda.value
        if valor is None:
            break
        encabezados.append(str(valor).strip())

    if not encabezados:
        raise ValueError("El archivo Excel está vacío o no tiene encabezados.")

    # Leer filas de datos (a partir de la fila 2)
    registros: list[dict[str, Any]] = []
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        # Saltar filas completamente vacías
        if all(celda is None for celda in fila):
            continue

        registro: dict[str, Any] = {}
        for i, encabezado in enumerate(encabezados):
            valor = fila[i] if i < len(fila) else None
            registro[encabezado] = valor
        registros.append(registro)

    return registros


if __name__ == "__main__":
    # Prueba rápida de funcionamiento
    registros = importar_excel("insumos/Base_Datos_Proyecto_IA_Cartera.xlsx")
    print(f"Registros importados: {len(registros)}")
    print(f"Columnas: {list(registros[0].keys()) if registros else 'ninguna'}")
    print("Primer registro:", registros[0] if registros else "vacio")
    print("Ultimo registro:", registros[-1] if registros else "vacio")
