"""Pruebas para R3 - Calcular totales."""

from app.services.importar_excel import importar_excel
from app.services.calcular_totales import calcular_totales

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_calcular_totales_devuelve_60_clientes():
    """R3: Los totales deben procesar los 60 clientes."""
    registros = importar_excel(RUTA_EXCEL)
    resultado = calcular_totales(registros)
    assert resultado["total_clientes"] == 60


def test_calcular_totales_totales_globales():
    """R3: Los totales globales deben coincidir con la suma de todas las filas."""
    registros = importar_excel(RUTA_EXCEL)
    resultado = calcular_totales(registros)
    totales = resultado["totales_globales"]

    # Suma manual de cada columna
    suma_sin_vencer = sum(r["Sin_Vencer"] or 0 for r in registros)
    suma_total_cartera = sum(r["Total_Cartera"] or 0 for r in registros)

    assert totales["Sin_Vencer"] == suma_sin_vencer
    assert totales["Total_Cartera"] == suma_total_cartera


def test_calcular_totales_total_vencidos_no_incluye_sin_vencer():
    """R3: total_vencidos debe ser solo Vencido_1_30 + Vencido_31_60 + Vencido_61_90 + Vencido_Mas_90."""
    registros = importar_excel(RUTA_EXCEL)
    resultado = calcular_totales(registros)
    cliente001 = resultado["por_cliente"][0]

    vencidos_esperados = (
        (registros[0]["Vencido_1_30"] or 0)
        + (registros[0]["Vencido_31_60"] or 0)
        + (registros[0]["Vencido_61_90"] or 0)
        + (registros[0]["Vencido_Mas_90"] or 0)
    )
    assert cliente001["total_vencidos"] == vencidos_esperados


def test_calcular_totales_conserva_campos_no_numericos():
    """R3: Cada cliente debe conservar Cliente, Ruta, Unidad_Comercio y Fecha_Corte."""
    registros = importar_excel(RUTA_EXCEL)
    resultado = calcular_totales(registros)
    cliente = resultado["por_cliente"][0]

    assert cliente["Cliente"] == "Cliente001"
    assert cliente["Ruta"] == "R001"
    assert cliente["Unidad_Comercio"] == "Centro"
    assert cliente["Fecha_Corte"] == "30/09/2026"
