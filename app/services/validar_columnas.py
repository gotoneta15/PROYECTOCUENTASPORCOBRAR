"""R2 - Validar columnas.

Verifica que el archivo de insumos tenga exactamente las 10 columnas esperadas,
según lo definido en el contexto y AGENTS.md.
"""

from typing import Any

from app.services.importar_excel import COLUMNAS_ESPERADAS


def validar_columnas(encabezados: list[str]) -> dict[str, Any]:
    """Valida que los encabezados del archivo coincidan con los esperados.

    Args:
        encabezados: Lista de nombres de columna leídos del Excel.

    Returns:
        Diccionario con:
            - valido: bool, True si todas las columnas esperadas están presentes
              y no hay columnas extra.
            - columnas_faltantes: lista de columnas esperadas que no se encontraron.
            - columnas_extra: lista de columnas presentes que no están en el esperado.
            - mensaje: str, legible para el usuario.
    """
    set_esperadas = set(COLUMNAS_ESPERADAS)
    set_presentes = set(encabezados)

    columnas_faltantes = [c for c in COLUMNAS_ESPERADAS if c not in set_presentes]
    columnas_extra = [c for c in encabezados if c not in set_esperadas]

    valido = len(columnas_faltantes) == 0 and len(columnas_extra) == 0

    if valido:
        mensaje = "Columnas válidas: el archivo contiene las 10 columnas esperadas."
    else:
        partes = []
        if columnas_faltantes:
            partes.append(f"Faltan columnas: {', '.join(columnas_faltantes)}")
        if columnas_extra:
            partes.append(f"Columnas extra no esperadas: {', '.join(columnas_extra)}")
        mensaje = "Columnas inválidas: " + "; ".join(partes)

    return {
        "valido": valido,
        "columnas_faltantes": columnas_faltantes,
        "columnas_extra": columnas_extra,
        "mensaje": mensaje,
    }


if __name__ == "__main__":
    # Prueba con las columnas correctas
    resultado_correcto = validar_columnas(COLUMNAS_ESPERADAS)
    print("Prueba 1 (columnas correctas):", resultado_correcto["mensaje"])
    print("  valido:", resultado_correcto["valido"])

    # Prueba con una columna faltante
    resultado_faltante = validar_columnas(
        ["Fecha_Corte", "Unidad_Comercio", "Ruta", "Cliente", "Sin_Vencer",
         "Vencido_1_30", "Vencido_31_60", "Vencido_61_90", "Vencido_Mas_90"]
    )
    print("Prueba 2 (falta Total_Cartera):", resultado_faltante["mensaje"])
    print("  valido:", resultado_faltante["valido"])
    print("  faltantes:", resultado_faltante["columnas_faltantes"])

    # Prueba con una columna extra
    resultado_extra = validar_columnas(COLUMNAS_ESPERADAS + ["Columna_Inventada"])
    print("Prueba 3 (columna extra):", resultado_extra["mensaje"])
    print("  valido:", resultado_extra["valido"])
    print("  extra:", resultado_extra["columnas_extra"])
