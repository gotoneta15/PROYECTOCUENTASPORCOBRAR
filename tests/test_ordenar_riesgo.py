"""Pruebas para R5 - Ordenar clientes por riesgo."""

from app.services.importar_excel import importar_excel
from app.services.calcular_totales import calcular_totales
from app.services.calcular_porcentajes import calcular_porcentajes
from app.services.ordenar_riesgo import ordenar_riesgo

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_ordenar_riesgo_devuelve_60_clientes():
    """R5: Se deben ordenar los 60 clientes."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    assert len(ordenados) == 60


def test_ordenar_riesgo_mayor_a_menor():
    """R5: La lista debe estar ordenada de mayor a menor porcentaje_vencido."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)

    for i in range(len(ordenados) - 1):
        actual = ordenados[i].get("porcentaje_vencido") or 0
        siguiente = ordenados[i + 1].get("porcentaje_vencido") or 0
        assert actual >= siguiente


def test_ordenar_riesgo_primero_es_mayor_riesgo():
    """R5: El primer cliente debe tener el porcentaje_vencido más alto."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)

    pct_max = max(c.get("porcentaje_vencido") or 0 for c in porcentajes)
    assert (ordenados[0].get("porcentaje_vencido") or 0) == pct_max
