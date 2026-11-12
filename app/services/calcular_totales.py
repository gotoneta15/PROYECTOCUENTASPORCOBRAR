"""R3 - Calcular totales.

Suma las columnas numéricas de cartera por cliente y calcula los totales globales.
"""

from typing import Any

# Columnas numéricas que se suman para los totales globales
COLUMNAS_NUMERICAS = [
    "Sin_Vencer",
    "Vencido_1_30",
    "Vencido_31_60",
    "Vencido_61_90",
    "Vencido_Mas_90",
    "Total_Cartera",
]

# Columnas que forman el total de vencidos (excluye Sin_Vencer y Total_Cartera)
COLUMNAS_VENCIDOS = [
    "Vencido_1_30",
    "Vencido_31_60",
    "Vencido_61_90",
    "Vencido_Mas_90",
]


def calcular_totales(registros: list[dict[str, Any]]) -> dict[str, Any]:
    """Calcula los totales de las columnas numéricas.

    Para cada registro, suma las columnas de vencimiento y compara con
    Total_Cartera. También calcula los totales globales de todas las columnas.

    Args:
        registros: Lista de diccionarios con los datos de cada cliente
                   (salida de R1 - Importar Excel).

    Returns:
        Diccionario con:
            - totales_globales: suma de cada columna numérica en todos los clientes.
            - total_clientes: número de clientes procesados.
            - por_cliente: lista con el total de vencidos por cliente.
    """
    if not registros:
        return {
            "totales_globales": {col: 0 for col in COLUMNAS_NUMERICAS},
            "total_clientes": 0,
            "por_cliente": [],
        }

    totales_globales: dict[str, int] = {col: 0 for col in COLUMNAS_NUMERICAS}
    por_cliente: list[dict[str, Any]] = []

    for registro in registros:
        cliente = registro.get("Cliente", "Sin nombre")
        total_vencidos = 0
        detalle_cliente: dict[str, Any] = {"cliente": cliente}

        for col in COLUMNAS_NUMERICAS:
            valor = registro.get(col) or 0
            try:
                valor_num = int(valor)
            except (TypeError, ValueError):
                valor_num = 0
            totales_globales[col] += valor_num
            detalle_cliente[col] = valor_num

        # total_vencidos solo incluye las columnas de vencimiento (no Sin_Vencer)
        for col in COLUMNAS_VENCIDOS:
            valor = registro.get(col) or 0
            try:
                total_vencidos += int(valor)
            except (TypeError, ValueError):
                pass

        # Conservar campos no numéricos para uso posterior (R9, R7, frontend)
        detalle_cliente["Cliente"] = registro.get("Cliente")
        detalle_cliente["Ruta"] = registro.get("Ruta")
        detalle_cliente["Unidad_Comercio"] = registro.get("Unidad_Comercio")
        detalle_cliente["Fecha_Corte"] = registro.get("Fecha_Corte")

        detalle_cliente["total_vencidos"] = total_vencidos
        por_cliente.append(detalle_cliente)

    return {
        "totales_globales": totales_globales,
        "total_clientes": len(registros),
        "por_cliente": por_cliente,
    }


if __name__ == "__main__":
    # Prueba rápida integrada con R1
    from app.services.importar_excel import importar_excel

    registros = importar_excel("insumos/Base_Datos_Proyecto_IA_Cartera.xlsx")
    resultado = calcular_totales(registros)

    print(f"Total de clientes: {resultado['total_clientes']}")
    print("Totales globales:")
    for col, valor in resultado["totales_globales"].items():
        print(f"  {col}: {valor:,}")
    print("\nPrimeros 3 clientes (total_vencidos):")
    for c in resultado["por_cliente"][:3]:
        print(f"  {c['cliente']}: total_vencidos={c['total_vencidos']:,}")
