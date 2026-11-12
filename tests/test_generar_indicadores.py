"""Pruebas para R8 - Generar gráficos e indicadores."""

from app.services.importar_excel import importar_excel
from app.services.calcular_totales import calcular_totales
from app.services.calcular_porcentajes import calcular_porcentajes
from app.services.ordenar_riesgo import ordenar_riesgo
from app.services.identificar_vencidos import identificar_vencidos_mas_30
from app.services.detectar_sin_ruta import detectar_clientes_sin_ruta
from app.services.generar_indicadores import generar_indicadores

RUTA_EXCEL = "insumos/Base_Datos_Proyecto_IA_Cartera.xlsx"


def test_generar_indicadores_devuelve_todos_los_campos():
    """R8: Los indicadores deben contener todos los campos esperados."""
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
    indicadores = generar_indicadores(todos)

    campos_esperados = [
        "total_clientes", "total_cartera", "total_sin_vencer",
        "total_vencidos", "total_vencidos_mas_30", "porcentaje_vencido_global",
        "conteo_por_nivel",
    ]
    for campo in campos_esperados:
        assert campo in indicadores


def test_generar_indicadores_conteo_por_nivel_suma_60():
    """R8: La suma de conteo_por_nivel debe ser 60 (total de clientes)."""
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
    indicadores = generar_indicadores(todos)

    conteo = indicadores["conteo_por_nivel"]
    total = (
        conteo["critico"] + conteo["alto"]
        + conteo["medio"] + conteo["bajo"]
    )
    assert total == 60


def test_generar_indicadores_lista_vacia():
    """R8: Con lista vacía, todos los indicadores deben ser 0."""
    indicadores = generar_indicadores([])

    assert indicadores["total_clientes"] == 0
    assert indicadores["total_cartera"] == 0
    assert indicadores["porcentaje_vencido_global"] == 0.0
    assert indicadores["conteo_por_nivel"] == {"critico": 0, "alto": 0, "medio": 0, "bajo": 0}
