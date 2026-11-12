"""R5 - Ordenar clientes por riesgo.

Ordena la lista de clientes de mayor a menor riesgo, usando
porcentaje_vencido como criterio de ordenamiento.
"""

from typing import Any


def ordenar_riesgo(porcentajes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ordena clientes de mayor a menor porcentaje de vencido.

    Args:
        porcentajes: Lista de diccionarios con datos de clientes
                     (salida de R4 - Calcular porcentajes). Cada uno debe
                     tener el campo porcentaje_vencido.

    Returns:
        Lista ordenada de mayor a menor porcentaje_vencido.
    """
    return sorted(
        porcentajes,
        key=lambda c: c.get("porcentaje_vencido") or 0,
        reverse=True,
    )


if __name__ == "__main__":
    # Prueba rápida integrada con R1, R3 y R4
    from app.services.importar_excel import importar_excel
    from app.services.calcular_totales import calcular_totales
    from app.services.calcular_porcentajes import calcular_porcentajes

    registros = importar_excel("insumos/Base_Datos_Proyecto_IA_Cartera.xlsx")
    totales = calcular_totales(registros)
    porcentajes = calcular_porcentajes(totales["por_cliente"])
    ordenados = ordenar_riesgo(porcentajes)

    print(f"Clientes ordenados: {len(ordenados)}")
    print("\nTop 5 clientes por riesgo (mayor porcentaje_vencido primero):")
    for i, c in enumerate(ordenados[:5], 1):
        print(f"  {i}. {c['cliente']}: porcentaje_vencido={c['porcentaje_vencido']}%")

    print("\nÚltimos 5 clientes por riesgo (menor porcentaje_vencido):")
    for i, c in enumerate(ordenados[-5:], len(ordenados) - 4):
        print(f"  {i}. {c['cliente']}: porcentaje_vencido={c['porcentaje_vencido']}%")
