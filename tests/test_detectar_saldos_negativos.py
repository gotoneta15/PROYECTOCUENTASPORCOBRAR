"""Pruebas para R10 - Detectar saldos negativos por notas de crédito."""

from app.services.importar_excel import importar_excel
from app.services.calcular_totales import calcular_totales
from app.services.calcular_porcentajes import calcular_porcentajes
from app.services.ordenar_riesgo import ordenar_riesgo
from app.services.identificar_vencidos import identificar_vencidos_mas_30
from app.services.detectar_sin_ruta import detectar_clientes_sin_ruta
from app.services.detectar_saldos_negativos import detectar_saldos_negativos

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_detectar_saldos_negativos_clasifica_todos_los_clientes():
    """R10: Todos los 60 clientes deben clasificarse (con o sin saldo negativo)."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    vencidos = identificar_vencidos_mas_30(ordenados)
    sin_ruta = detectar_clientes_sin_ruta(
        vencidos["clientes_con_vencidos_mas_30"]
        + vencidos["clientes_sin_vencidos_mas_30"]
    )
    todos = (
        sin_ruta["clientes_sin_ruta"]
        + sin_ruta["clientes_con_ruta"]
    )
    resultado = detectar_saldos_negativos(todos)

    total = (
        resultado["total_con_saldo_negativo"]
        + resultado["total_sin_saldo_negativo"]
    )
    assert total == 60


def test_detectar_saldos_negativos_con_datos_reales():
    """R10: Con el archivo real, ningún cliente tiene saldo negativo."""
    registros = importar_excel(RUTA_EXCEL)
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    vencidos = identificar_vencidos_mas_30(ordenados)
    sin_ruta = detectar_clientes_sin_ruta(
        vencidos["clientes_con_vencidos_mas_30"]
        + vencidos["clientes_sin_vencidos_mas_30"]
    )
    todos = (
        sin_ruta["clientes_sin_ruta"]
        + sin_ruta["clientes_con_ruta"]
    )
    resultado = detectar_saldos_negativos(todos)

    assert resultado["total_con_saldo_negativo"] == 0
    assert resultado["total_sin_saldo_negativo"] == 60


def test_detectar_saldos_negativos_cliente_con_saldo_negativo():
    """R10: Un cliente con Saldo Vencido_1_30 negativo debe detectarse."""
    clientes = [
        {
            "Cliente": "ClienteA",
            "Sin_Vencer": 100000,
            "Vencido_1_30": -50000,
            "Vencido_31_60": 0,
            "Vencido_61_90": 0,
            "Vencido_Mas_90": 0,
            "Total_Cartera": 50000,
        },
        {
            "Cliente": "ClienteB",
            "Sin_Vencer": 100000,
            "Vencido_1_30": 0,
            "Vencido_31_60": 0,
            "Vencido_61_90": 0,
            "Vencido_Mas_90": 0,
            "Total_Cartera": 100000,
        },
    ]
    resultado = detectar_saldos_negativos(clientes)

    assert resultado["total_con_saldo_negativo"] == 1
    assert resultado["total_sin_saldo_negativo"] == 1
    assert len(resultado["detalle_negativos"]) == 1
    assert resultado["detalle_negativos"][0]["cliente"] == "ClienteA"
    assert resultado["detalle_negativos"][0]["columna"] == "Vencido_1_30"
    assert resultado["detalle_negativos"][0]["valor"] == -50000
