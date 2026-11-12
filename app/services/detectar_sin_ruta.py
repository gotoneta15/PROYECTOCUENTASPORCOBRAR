"""R9 - Detectar clientes sin ruta.

Identifica clientes cuyo campo Ruta esté vacío o sea None.
"""

from typing import Any


def detectar_clientes_sin_ruta(
    datos_procesados: list[dict[str, Any]],
) -> dict[str, Any]:
    """Detecta clientes que no tienen ruta asignada.

    Args:
        datos_procesados: Lista de diccionarios con los datos de cada cliente
                          (salida de R8 - Generar indicadores o R6).

    Returns:
        Diccionario con:
            - clientes_sin_ruta: lista de clientes sin ruta.
            - total_sin_ruta: cantidad de clientes sin ruta.
            - clientes_con_ruta: lista de clientes con ruta.
            - total_con_ruta: cantidad de clientes con ruta.
    """
    clientes_sin_ruta: list[dict[str, Any]] = []
    clientes_con_ruta: list[dict[str, Any]] = []

    for cliente in datos_procesados:
        ruta = cliente.get("Ruta")
        if ruta is None or str(ruta).strip() == "":
            clientes_sin_ruta.append(cliente)
        else:
            clientes_con_ruta.append(cliente)

    return {
        "clientes_sin_ruta": clientes_sin_ruta,
        "total_sin_ruta": len(clientes_sin_ruta),
        "clientes_con_ruta": clientes_con_ruta,
        "total_con_ruta": len(clientes_con_ruta),
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

    resultado = detectar_clientes_sin_ruta(todos)

    print(f"Total clientes: {len(todos)}")
    print(f"Clientes sin ruta: {resultado['total_sin_ruta']}")
    print(f"Clientes con ruta: {resultado['total_con_ruta']}")
    if resultado["clientes_sin_ruta"]:
        print("\nClientes sin ruta:")
        for c in resultado["clientes_sin_ruta"]:
            print(f"  {c['Cliente']}: Ruta='{c.get('Ruta')}'")
