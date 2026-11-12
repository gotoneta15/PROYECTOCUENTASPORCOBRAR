"""Pruebas para R2 - Validar columnas."""

from app.services.validar_columnas import validar_columnas
from app.services.importar_excel import COLUMNAS_ESPERADAS


def test_validar_columnas_columnas_correctas():
    """R2: Las 10 columnas esperadas son válidas."""
    resultado = validar_columnas(COLUMNAS_ESPERADAS)
    assert resultado["valido"] is True
    assert resultado["columnas_faltantes"] == []
    assert resultado["columnas_extra"] == []


def test_validar_columnas_falta_total_cartera():
    """R2: Si falta Total_Cartera, debe reportarse como columna faltante."""
    columnas = [c for c in COLUMNAS_ESPERADAS if c != "Total_Cartera"]
    resultado = validar_columnas(columnas)
    assert resultado["valido"] is False
    assert "Total_Cartera" in resultado["columnas_faltantes"]


def test_validar_columnas_columna_extra():
    """R2: Una columna extra no esperada debe reportarse como inválida."""
    columnas = COLUMNAS_ESPERADAS + ["Columna_Inventada"]
    resultado = validar_columnas(columnas)
    assert resultado["valido"] is False
    assert "Columna_Inventada" in resultado["columnas_extra"]
