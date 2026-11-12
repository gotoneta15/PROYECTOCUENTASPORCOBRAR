"""Pruebas para R6 - Identificar clientes con vencidos mayores a 30 días."""

from app.services.importar_excel import importar_excel
from app.services.calcular_totales import calcular_totales
from app.services.calcular_porcentajes import calcular_porcentajes
from app.services.ordenar_riesgo import ordenar_riesgo
from app.services.identificar_vencidos import identificar_vencidos_mas_30

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_identificar_vencidos_clasifica_todos_los_clientes():
    """R6: Todos los 60 clientes deben clasificarse (con o sin vencidos > 30 días)."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    resultado = identificar_vencidos_mas_30(ordenados)

    total = (
        resultado["total_con_vencidos_mas_30"]
        + resultado["total_sin_vencidos_mas_30"]
    )
    assert total == 60


def test_identificar_vencidos_suma_correcta():
    """R6: vencidos_mas_30_dias = Vencido_31_60 + Vencido_61_90 + Vencido_Mas_90."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    resultado = identificar_vencidos_mas_30(ordenados)

    # Buscar al Cliente001 en la lista (puede no estar en posición [0] porque
    # la lista está ordenada por porcentaje_vencido descendente)
    cliente001 = next(
        (c for c in resultado["clientes_con_vencidos_mas_30"]
         if c.get("Cliente") == "Cliente001"),
        None,
    )
    assert cliente001 is not None, "Cliente001 no encontrado en la lista"
    esperado = (
        (registros[0]["Vencido_31_60"] or 0)
        + (registros[0]["Vencido_61_90"] or 0)
        + (registros[0]["Vencido_Mas_90"] or 0)
    )
    assert cliente001["vencidos_mas_30_dias"] == esperado


def test_identificar_vencidos_todos_tienen_vencidos_mas_30():
    """R6: Con estos datos, los 60 clientes tienen vencidos mayores a 30 días."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    resultado = identificar_vencidos_mas_30(ordenados)

    assert resultado["total_con_vencidos_mas_30"] == 60
    assert resultado["total_sin_vencidos_mas_30"] == 0
