"""Pruebas para R1 - Importar Excel."""

from app.services.importar_excel import importar_excel

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_importar_excel_devuelve_60_registros():
    """R1: El archivo de insumos debe devolver exactamente 60 registros de clientes."""
    registros = importar_excel(RUTA_EXCEL)
    assert len(registros) == 60


def test_importar_excel_tiene_10_columnas():
    """R1: Cada registro debe tener exactamente las 10 columnas esperadas."""
    registros = importar_excel(RUTA_EXCEL)
    columnas_esperadas = [
        "Fecha_Corte", "Unidad_Comercio", "Ruta", "Cliente",
        "Sin_Vencer", "Vencido_1_30", "Vencido_31_60", "Vencido_61_90",
        "Vencido_Mas_90", "Total_Cartera",
    ]
    assert list(registros[0].keys()) == columnas_esperadas


def test_importar_excel_primero_registro_cliente001():
    """R1: El primer cliente debe ser Cliente001 con Ruta R001."""
    registros = importar_excel(RUTA_EXCEL)
    assert registros[0]["Cliente"] == "Cliente001"
    assert registros[0]["Ruta"] == "R001"
    assert registros[0]["Unidad_Comercio"] == "Centro"


def test_importar_excel_ultimo_registro_cliente060():
    """R1: El último cliente debe ser Cliente060 con Ruta R060."""
    registros = importar_excel(RUTA_EXCEL)
    assert registros[-1]["Cliente"] == "Cliente060"
    assert registros[-1]["Ruta"] == "R060"
