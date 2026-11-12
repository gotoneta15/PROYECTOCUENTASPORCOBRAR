"""R10 - Detectar saldos negativos por notas de crédito.

Identifica clientes que tienen al menos una columna de saldo con valor
negativo, lo que indica la presencia de una nota de crédito.
"""

from typing import Any

COLUMNAS_SALDO = [
    "Sin_Vencer",
    "Vencido_1_30",
    "Vencido_31_60",
    "Vencido_61_90",
    "Vencido_Mas_90",
    "Total_Cartera",
]


def detectar_saldos_negativos(
    datos_procesados: list[dict[str, Any]],
) -> dict[str, Any]:
    """Detecta clientes con saldos negativos en cualquier columna.

    Args:
        datos_procesados: Lista de diccionarios con los datos de cada cliente
                          (salida de R9 - Detectar clientes sin ruta o R6).

    Returns:
        Diccionario con:
            - clientes_con_saldo_negativo: lista de clientes que tienen al
              menos una columna de saldo negativa.
            - total_con_saldo_negativo: cantidad de esos clientes.
            - clientes_sin_saldo_negativo: lista de clientes sin saldos
              negativos.
            - total_sin_saldo_negativo: cantidad de clientes sin saldos
              negativos.
            - detalle_negativos: lista de diccionarios con cliente, columna
              y valor negativo detectado.
    """
    clientes_con_negativo: list[dict[str, Any]] = []
    clientes_sin_negativo: list[dict[str, Any]] = []
    detalle_negativos: list[dict[str, Any]] = []

    for cliente in datos_procesados:
        cliente_nombre = cliente.get("Cliente") or cliente.get("cliente") or "Sin nombre"
        columnas_negativas: list[dict[str, Any]] = []

        for col in COLUMNAS_SALDO:
            valor = cliente.get(col)
            if valor is None:
                continue
            try:
                valor_num = int(valor)
            except (TypeError, ValueError):
                continue
            if valor_num < 0:
                columnas_negativas.append({
                    "columna": col,
                    "valor": valor_num,
                })

        if columnas_negativas:
            entrada = dict(cliente)
            entrada["columnas_negativas"] = columnas_negativas
            clientes_con_negativo.append(entrada)
            for neg in columnas_negativas:
                detalle_negativos.append({
                    "cliente": cliente_nombre,
                    "columna": neg["columna"],
                    "valor": neg["valor"],
                })
        else:
            clientes_sin_negativo.append(cliente)

    return {
        "clientes_con_saldo_negativo": clientes_con_negativo,
        "total_con_saldo_negativo": len(clientes_con_negativo),
        "clientes_sin_saldo_negativo": clientes_sin_negativo,
        "total_sin_saldo_negativo": len(clientes_sin_negativo),
        "detalle_negativos": detalle_negativos,
    }


if __name__ == "__main__":
    # Prueba rápida integrada con R1 a R9
    from app.services.importar_excel import importar_excel
    from app.services.calcular_totales import calcular_totales
    from app.services.calcular_porcentajes import calcular_porcentajes
    from app.services.ordenar_riesgo import ordenar_riesgo
    from app.services.identificar_vencidos import identificar_vencidos_mas_30
    from app.services.detectar_sin_ruta import detectar_clientes_sin_ruta

    registros = importar_excel("insumos/Base_Datos_Proyecto_IA_Cartera.xlsx")
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

    print(f"Total clientes: {len(todos)}")
    print(f"Clientes con saldo negativo: {resultado['total_con_saldo_negativo']}")
    print(f"Clientes sin saldo negativo: {resultado['total_sin_saldo_negativo']}")
    if resultado["clientes_con_saldo_negativo"]:
        print("\nClientes con saldo negativo:")
        for c in resultado["clientes_con_saldo_negativo"]:
            print(f"  {c.get('Cliente') or c.get('cliente')}: "
                  f"columnas_negativas={c['columnas_negativas']}")
    if resultado["detalle_negativos"]:
        print("\nDetalle de saldos negativos:")
        for d in resultado["detalle_negativos"]:
            print(f"  {d['cliente']}: {d['columna']} = {d['valor']:,}")
