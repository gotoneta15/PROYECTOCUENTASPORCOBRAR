"""Pruebas para R4 - Calcular porcentajes."""

from app.services.importar_excel import importar_excel
from app.services.calcular_totales import calcular_totales
from app.services.calcular_porcentajes import calcular_porcentajes

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_calcular_porcentajes_devuelve_60_clientes():
    """R4: Se debe calcular el porcentaje para los 60 clientes."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    assert len(porcentajes) == 60


def test_calcular_porcentajes_formula_correcta():
    """R4: porcentaje_vencido = (vencidos_totales / Total_Cartera) * 100."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])

    cliente001 = porcentajes[0]
    vencidos = cliente001["vencidos_totales"]
    total = cliente001["Total_Cartera"]
    esperado = round((vencidos / total) * 100, 2)

    assert cliente001["porcentaje_vencido"] == esperado


def test_calcular_porcentajes_total_cartera_cero():
    """R4: Si Total_Cartera es 0, porcentaje_vencido debe ser 0.0."""
    from app.services.calcular_porcentajes import calcular_porcentajes

    clientes = [
        {
            "Cliente": "ClienteTest",
            "Ruta": "R001",
            "Total_Cartera": 0,
            "total_vencidos": 100000,
        }
    ]
    resultado = calcular_porcentajes(clientes)
    assert resultado[0]["porcentaje_vencido"] == 0.0
