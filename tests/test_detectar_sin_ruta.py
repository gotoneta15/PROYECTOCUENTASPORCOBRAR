"""Pruebas para R9 - Detectar clientes sin ruta."""

from app.services.importar_excel import importar_excel
from app.services.calcular_totales import calcular_totales
from app.services.calcular_porcentajes import calcular_porcentajes
from app.services.ordenar_riesgo import ordenar_riesgo
from app.services.identificar_vencidos import identificar_vencidos_mas_30
from app.services.detectar_sin_ruta import detectar_clientes_sin_ruta

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_detectar_sin_ruta_clasifica_todos_los_clientes():
    """R9: Todos los 60 clientes deben clasificarse (con o sin ruta)."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    vencidos = identificar_vencidos_mas_30(ordenados)
    todos = (
        vencidos["clientes_con_vencidos_mas_30"]
        + vencidos["clientes_sin_vencidos_mas_30"]
    )
    resultado = detectar_clientes_sin_ruta(todos)

    total = resultado["total_sin_ruta"] + resultado["total_con_ruta"]
    assert total == 60


def test_detectar_sin_ruta_con_datos_reales():
    """R9: Con el archivo real, todos los 60 clientes tienen ruta asignada."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    vencidos = identificar_vencidos_mas_30(ordenados)
    todos = (
        vencidos["clientes_con_vencidos_mas_30"]
        + vencidos["clientes_sin_vencidos_mas_30"]
    )
    resultado = detectar_clientes_sin_ruta(todos)

    assert resultado["total_sin_ruta"] == 0
    assert resultado["total_con_ruta"] == 60


def test_detectar_sin_ruta_cliente_sin_ruta():
    """R9: Un cliente con Ruta vacía debe detectarse como sin ruta."""
    clientes = [
        {"Cliente": "ClienteA", "Ruta": "R001"},
        {"Cliente": "ClienteB", "Ruta": ""},
        {"Cliente": "ClienteC", "Ruta": None},
        {"Cliente": "ClienteD", "Ruta": "R002"},
    ]
    resultado = detectar_clientes_sin_ruta(clientes)

    assert resultado["total_sin_ruta"] == 2
    assert resultado["total_con_ruta"] == 2
    assert len(resultado["clientes_sin_ruta"]) == 2
    assert len(resultado["clientes_con_ruta"]) == 2
