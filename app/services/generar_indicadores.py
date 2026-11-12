"""R8 - Generar gráficos e indicadores.

Calcula indicadores globales (contadores grandes) a partir de los datos
procesados de todos los clientes. Estos indicadores se muestran en el
tablero de la app (frontend).
"""

from typing import Any


def generar_indicadores(
    datos_procesados: list[dict[str, Any]],
) -> dict[str, Any]:
    """Calcula indicadores globales de cartera.

    Args:
        datos_procesados: Lista de diccionarios con los datos de cada cliente
                          (salida de R6 - Identificar vencidos > 30 días).
                          Cada uno debe tener: Total_Cartera, vencidos_totales,
                          porcentaje_vencido, vencidos_mas_30_dias.

    Returns:
        Diccionario con indicadores globales:
            - total_clientes: número total de clientes.
            - total_cartera: suma de Total_Cartera.
            - total_sin_vencer: suma de Sin_Vencer.
            - total_vencidos: suma de vencidos_totales.
            - total_vencidos_mas_30: suma de vencidos_mas_30_dias.
            - porcentaje_vencido_global: (total_vencidos / total_cartera) * 100.
            - clientes_criticos: clientes con porcentaje_vencido >= 50%.
            - clientes_con_riesgo_alto: clientes con porcentaje_vencido >= 30% y < 50%.
            - clientes_con_riesgo_medio: clientes con porcentaje_vencido >= 10% y < 30%.
            - clientes_con_riesgo_bajo: clientes con porcentaje_vencido < 10%.
    """
    if not datos_procesados:
        return {
            "total_clientes": 0,
            "total_cartera": 0,
            "total_sin_vencer": 0,
            "total_vencidos": 0,
            "total_vencidos_mas_30": 0,
            "porcentaje_vencido_global": 0.0,
            "clientes_criticos": [],
            "clientes_con_riesgo_alto": [],
            "clientes_con_riesgo_medio": [],
            "clientes_con_riesgo_bajo": [],
            "conteo_por_nivel": {
                "critico": 0,
                "alto": 0,
                "medio": 0,
                "bajo": 0,
            },
        }

    total_clientes = len(datos_procesados)
    total_cartera = 0
    total_sin_vencer = 0
    total_vencidos = 0
    total_vencidos_mas_30 = 0

    clientes_criticos: list[dict[str, Any]] = []
    clientes_con_riesgo_alto: list[dict[str, Any]] = []
    clientes_con_riesgo_medio: list[dict[str, Any]] = []
    clientes_con_riesgo_bajo: list[dict[str, Any]] = []

    for cliente in datos_procesados:
        total_cartera += cliente.get("Total_Cartera") or 0
        total_sin_vencer += cliente.get("Sin_Vencer") or 0
        total_vencidos += cliente.get("vencidos_totales") or 0
        total_vencidos_mas_30 += cliente.get("vencidos_mas_30_dias") or 0

        porcentaje = cliente.get("porcentaje_vencido") or 0
        try:
            porcentaje = float(porcentaje)
        except (TypeError, ValueError):
            porcentaje = 0.0

        if porcentaje >= 50:
            clientes_criticos.append(cliente)
        elif porcentaje >= 30:
            clientes_con_riesgo_alto.append(cliente)
        elif porcentaje >= 10:
            clientes_con_riesgo_medio.append(cliente)
        else:
            clientes_con_riesgo_bajo.append(cliente)

    if total_cartera > 0:
        porcentaje_vencido_global = round((total_vencidos / total_cartera) * 100, 2)
    else:
        porcentaje_vencido_global = 0.0

    return {
        "total_clientes": total_clientes,
        "total_cartera": total_cartera,
        "total_sin_vencer": total_sin_vencer,
        "total_vencidos": total_vencidos,
        "total_vencidos_mas_30": total_vencidos_mas_30,
        "porcentaje_vencido_global": porcentaje_vencido_global,
        "clientes_criticos": clientes_criticos,
        "clientes_con_riesgo_alto": clientes_con_riesgo_alto,
        "clientes_con_riesgo_medio": clientes_con_riesgo_medio,
        "clientes_con_riesgo_bajo": clientes_con_riesgo_bajo,
        "conteo_por_nivel": {
            "critico": len(clientes_criticos),
            "alto": len(clientes_con_riesgo_alto),
            "medio": len(clientes_con_riesgo_medio),
            "bajo": len(clientes_con_riesgo_bajo),
        },
    }


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

    todos = (
        vencidos["clientes_con_vencidos_mas_30"]
        + vencidos["clientes_sin_vencidos_mas_30"]
    )

    indicadores = generar_indicadores(todos)

    print("=== INDICADORES GLOBALES ===")
    print(f"Total clientes: {indicadores['total_clientes']}")
    print(f"Total cartera: {indicadores['total_cartera']:,}")
    print(f"Total sin vencer: {indicadores['total_sin_vencer']:,}")
    print(f"Total vencidos: {indicadores['total_vencidos']:,}")
    print(f"Total vencidos > 30 días: {indicadores['total_vencidos_mas_30']:,}")
    print(f"Porcentaje vencido global: {indicadores['porcentaje_vencido_global']}%")
    print("\nConteo por nivel de riesgo:")
    for nivel, conteo in indicadores["conteo_por_nivel"].items():
        print(f"  {nivel}: {conteo}")
    print(f"\nClientes críticos: {len(indicadores['clientes_criticos'])}")
    print(f"Clientes riesgo alto: {len(indicadores['clientes_con_riesgo_alto'])}")
    print(f"Clientes riesgo medio: {len(indicadores['clientes_con_riesgo_medio'])}")
    print(f"Clientes riesgo bajo: {len(indicadores['clientes_con_riesgo_bajo'])}")
