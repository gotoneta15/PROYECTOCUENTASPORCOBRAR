"""R4 - Calcular porcentajes.

Calcula el porcentaje_vencido de cada cliente y los porcentajes de cada
columna numérica sobre Total_Cartera:

    porcentaje_vencido = (vencidos_totales / Total_Cartera) * 100
    porcentaje_Sin_Vencer = (Sin_Vencer / Total_Cartera) * 100
    porcentaje_Vencido_1_30 = (Vencido_1_30 / Total_Cartera) * 100
    porcentaje_Vencido_31_60 = (Vencido_31_60 / Total_Cartera) * 100
    porcentaje_Vencido_61_90 = (Vencido_61_90 / Total_Cartera) * 100
    porcentaje_Vencido_Mas_90 = (Vencido_Mas_90 / Total_Cartera) * 100

donde vencidos_totales = Vencido_1_30 + Vencido_31_60 + Vencido_61_90 + Vencido_Mas_90.
"""

from typing import Any

COLUMNAS_NUMERICAS_PORCENTAJE = [
    "Sin_Vencer",
    "Vencido_1_30",
    "Vencido_31_60",
    "Vencido_61_90",
    "Vencido_Mas_90",
]


def calcular_porcentajes(por_cliente: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Calcula porcentajes de cada columna numérica sobre Total_Cartera.

    Args:
        por_cliente: Lista de diccionarios con los datos de cada cliente
                     (salida de R3 - Calcular totales). Cada uno debe tener
                     Total_Cartera y las columnas numéricas.

    Returns:
        Lista de diccionarios con los mismos campos más:
            - vencidos_totales: suma de las 4 columnas de vencimiento.
            - porcentaje_vencido: (vencidos_totales / Total_Cartera) * 100,
              redondeado a 2 decimales. Si Total_Cartera es 0 o falta, es 0.0.
            - porcentaje_<columna>: (columna / Total_Cartera) * 100 para cada
              columna numérica (Sin_Vencer, Vencido_1_30, Vencido_31_60,
              Vencido_61_90, Vencido_Mas_90).
    """
    resultado: list[dict[str, Any]] = []

    for cliente in por_cliente:
        total_cartera = cliente.get("Total_Cartera") or 0
        try:
            total_cartera = int(total_cartera)
        except (TypeError, ValueError):
            total_cartera = 0

        vencidos_totales = cliente.get("total_vencidos") or 0
        try:
            vencidos_totales = int(vencidos_totales)
        except (TypeError, ValueError):
            vencidos_totales = 0

        if total_cartera > 0:
            porcentaje_vencido = round((vencidos_totales / total_cartera) * 100, 2)
        else:
            porcentaje_vencido = 0.0

        entrada = dict(cliente)
        entrada["vencidos_totales"] = vencidos_totales
        entrada["porcentaje_vencido"] = porcentaje_vencido

        # Calcular porcentaje de cada columna numérica sobre Total_Cartera
        for col in COLUMNAS_NUMERICAS_PORCENTAJE:
            valor_col = cliente.get(col) or 0
            try:
                valor_col = int(valor_col)
            except (TypeError, ValueError):
                valor_col = 0

            if total_cartera > 0:
                pct_col = round((valor_col / total_cartera) * 100, 2)
            else:
                pct_col = 0.0

            entrada[f"porcentaje_{col}"] = pct_col

        resultado.append(entrada)

    return resultado


if __name__ == "__main__":
    # Prueba rápida integrada con R1 y R3
    from app.services.importar_excel import importar_excel
    from app.services.calcular_totales import calcular_totales

    registros = importar_excel("insumos/Base_Datos_Proyecto_IA_Cartera.xlsx")
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])

    print(f"Clientes procesados: {len(porcentajes)}")
    print("\nPrimeros 3 clientes (porcentajes de todas las columnas):")
    for c in porcentajes[:3]:
        print(f"  {c['cliente']}:")
        print(f"    Total_Cartera: {c['Total_Cartera']:,}")
        print(f"    Sin_Vencer: {c['Sin_Vencer']:,} ({c['porcentaje_Sin_Vencer']}%)")
        print(f"    Vencido_1_30: {c['Vencido_1_30']:,} ({c['porcentaje_Vencido_1_30']}%)")
        print(f"    Vencido_31_60: {c['Vencido_31_60']:,} ({c['porcentaje_Vencido_31_60']}%)")
        print(f"    Vencido_61_90: {c['Vencido_61_90']:,} ({c['porcentaje_Vencido_61_90']}%)")
        print(f"    Vencido_Mas_90: {c['Vencido_Mas_90']:,} ({c['porcentaje_Vencido_Mas_90']}%)")
        print(f"    % Vencido total: {c['porcentaje_vencido']}%")
