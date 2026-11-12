"""R6 - Identificar clientes con vencidos mayores a 30 días.

Un cliente tiene vencidos mayores a 30 días si la suma de
Vencido_31_60 + Vencido_61_90 + Vencido_Mas_90 es mayor a 0.
"""

from typing import Any

COLUMNAS_VENCIDOS_MAS_30 = [
    "Vencido_31_60",
    "Vencido_61_90",
    "Vencido_Mas_90",
]


def identificar_vencidos_mas_30(
    porcentajes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Identifica clientes con vencidos mayores a 30 días.

    Args:
        porcentajes: Lista de diccionarios con datos de clientes
                     (salida de R4 - Calcular porcentajes). Cada uno debe
                     tener las columnas de vencimiento.

    Returns:
        Diccionario con:
            - clientes_con_vencidos_mas_30: lista de clientes que tienen
              vencidos mayores a 30 días.
            - total_con_vencidos_mas_30: cantidad de esos clientes.
            - clientes_sin_vencidos_mas_30: lista de clientes que no tienen
              vencidos mayores a 30 días.
    """
    clientes_con_vencidos: list[dict[str, Any]] = []
    clientes_sin_vencidos: list[dict[str, Any]] = []

    for cliente in porcentajes:
        vencidos_mas_30 = 0
        for col in COLUMNAS_VENCIDOS_MAS_30:
            valor = cliente.get(col) or 0
            try:
                vencidos_mas_30 += int(valor)
            except (TypeError, ValueError):
                pass

        entrada = dict(cliente)
        entrada["vencidos_mas_30_dias"] = vencidos_mas_30

        if vencidos_mas_30 > 0:
            clientes_con_vencidos.append(entrada)
        else:
            clientes_sin_vencidos.append(entrada)

    return {
        "clientes_con_vencidos_mas_30": clientes_con_vencidos,
        "total_con_vencidos_mas_30": len(clientes_con_vencidos),
        "clientes_sin_vencidos_mas_30": clientes_sin_vencidos,
        "total_sin_vencidos_mas_30": len(clientes_sin_vencidos),
    }


if __name__ == "__main__":
    # Prueba rápida integrada con R1, R3, R4 y R5
    from app.services.importar_excel import importar_excel
    from app.services.calcular_totales import calcular_totales
    from app.services.calcular_porcentajes import calcular_porcentajes
    from app.services.ordenar_riesgo import ordenar_riesgo

    registros = importar_excel("insumos/Base_Datos_Proyecto_IA_Cartera.xlsx")
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)
    resultado = identificar_vencidos_mas_30(ordenados)

    print(f"Total clientes: {len(ordenados)}")
    print(f"Clientes con vencidos > 30 días: {resultado['total_con_vencidos_mas_30']}")
    print(f"Clientes sin vencidos > 30 días: {resultado['total_sin_vencidos_mas_30']}")
    print("\nPrimeros 5 clientes con vencidos > 30 días:")
    for c in resultado["clientes_con_vencidos_mas_30"][:5]:
        print(f"  {c['cliente']}: vencidos_mas_30_dias={c['vencidos_mas_30_dias']:,}, "
              f"porcentaje_vencido={c['porcentaje_vencido']}%")
