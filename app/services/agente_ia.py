"""Integración con el agente de IA (Analista virtual de cartera).

Lee la llave de API desde .env, prepara el contrato JSON de entrada y
envía los datos al agente de IA. Valida que la respuesta contenga los 11
campos del contrato de salida.
"""

import json
import os
from typing import Any

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Campos que el agente de IA debe devolver (contrato de salida)
CAMPOS_CONTRATO_SALIDA = [
    "cliente",
    "ruta",
    "total_cartera",
    "porcentaje_vencido",
    "nivel_riesgo",
    "semaforo",
    "accion_recomendada",
    "motivo",
    "suspender_credito",
    "escalar_gerencia",
    "enviar_recordatorio",
]


def cargar_configuracion_ia() -> dict[str, str]:
    """Lee la configuración del agente de IA desde .env.

    Returns:
        Diccionario con IA_API_KEY e IA_API_URL.

    Raises:
        ValueError: Si IA_API_KEY no está configurada en .env.
    """
    api_key = os.getenv("IA_API_KEY")
    api_url = os.getenv("IA_API_URL", "")

    if not api_key or api_key == "tu_llave_de_api_aqui":
        raise ValueError(
            "IA_API_KEY no está configurada en .env. "
            "Agrega tu llave de API real al archivo .env antes de usar el agente de IA."
        )

    return {
        "IA_API_KEY": api_key,
        "IA_API_URL": api_url,
    }


def preparar_contrato_entrada(
    cliente: str,
    ruta: str,
    total_cartera: int,
    porcentaje_vencido: float,
) -> dict[str, Any]:
    """Prepara el contrato JSON de entrada para el agente de IA.

    Args:
        cliente: Nombre del cliente.
        ruta: Ruta asignada al cliente.
        total_cartera: Total de cartera del cliente.
        porcentaje_vencido: Porcentaje de vencido del cliente.

    Returns:
        Diccionario con los datos de entrada para el agente.
    """
    return {
        "cliente": cliente,
        "ruta": ruta,
        "total_cartera": total_cartera,
        "porcentaje_vencido": porcentaje_vencido,
    }


def llamar_agente_ia(
    contrato_entrada: dict[str, Any],
) -> dict[str, Any]:
    """Envía el contrato de entrada al agente de IA y retorna su respuesta.

    Esta función es un placeholder para la integración real con el proveedor
    de IA. En producción, aquí se haría la llamada HTTP al endpoint de IA
    usando la llave de .env.

    Args:
        contrato_entrada: Datos de entrada para el agente de IA.

    Returns:
        Diccionario con la respuesta del agente (11 campos del contrato).

    Raises:
        ValueError: Si la respuesta no es un JSON válido o falta campos.
    """
    config = cargar_configuracion_ia()

    # TODO: En producción, hacer llamada HTTP real a config["IA_API_URL"]
    # con headers de autorización usando config["IA_API_KEY"].
    # Por ahora, retornamos una respuesta de ejemplo con los 11 campos.

    respuesta_ejemplo = {
        "cliente": contrato_entrada.get("cliente", "no indicado"),
        "ruta": contrato_entrada.get("ruta", "no indicado"),
        "total_cartera": contrato_entrada.get("total_cartera", 0),
        "porcentaje_vencido": contrato_entrada.get("porcentaje_vencido", 0.0),
        "nivel_riesgo": "no indicado",
        "semaforo": "no indicado",
        "accion_recomendada": "no indicado",
        "motivo": "no indicado",
        "suspender_credito": "no indicado",
        "escalar_gerencia": "no indicado",
        "enviar_recordatorio": "no indicado",
    }

    # Validar que tenga todos los 11 campos del contrato
    _validar_respuesta_agente(respuesta_ejemplo)

    return respuesta_ejemplo


def _validar_respuesta_agente(respuesta: dict[str, Any]) -> None:
    """Valida que la respuesta del agente tenga los 11 campos del contrato.

    Args:
        respuesta: Diccionario con la respuesta del agente.

    Raises:
        ValueError: Si falta algún campo obligatorio del contrato.
    """
    if not isinstance(respuesta, dict):
        raise ValueError(
            f"La respuesta del agente no es un diccionario válido: {type(respuesta)}"
        )

    campos_faltantes = [
        campo for campo in CAMPOS_CONTRATO_SALIDA if campo not in respuesta
    ]

    if campos_faltantes:
        raise ValueError(
            f"La respuesta del agente falta los campos: {', '.join(campos_faltantes)}"
        )


def procesar_cliente_con_agente(
    cliente: str,
    ruta: str,
    total_cartera: int,
    porcentaje_vencido: float,
) -> dict[str, Any]:
    """Procesa un cliente completo a través del agente de IA.

    Combina la preparación del contrato de entrada, la llamada al agente
    y la validación de la respuesta.

    Args:
        cliente: Nombre del cliente.
        ruta: Ruta asignada.
        total_cartera: Total de cartera.
        porcentaje_vencido: Porcentaje de vencido.

    Returns:
        Diccionario con los 11 campos del contrato de salida del agente.
    """
    contrato_entrada = preparar_contrato_entrada(
        cliente=cliente,
        ruta=ruta,
        total_cartera=total_cartera,
        porcentaje_vencido=porcentaje_vencido,
    )
    return llamar_agente_ia(contrato_entrada)


if __name__ == "__main__":
    # Prueba rápida de la estructura (fallará si no hay IA_API_KEY real en .env)
    try:
        config = cargar_configuracion_ia()
        print("Configuración de IA cargada correctamente.")
        print(f"  IA_API_KEY: {config['IA_API_KEY'][:8]}...")
        print(f"  IA_API_URL: {config['IA_API_URL']}")

        respuesta = procesar_cliente_con_agente(
            cliente="Cliente001",
            ruta="R001",
            total_cartera=2610000,
            porcentaje_vencido=11.88,
        )
        print("\nRespuesta del agente de IA:")
        for campo, valor in respuesta.items():
            print(f"  {campo}: {valor}")

    except ValueError as e:
        print(f"Error (esperado si no hay llave real en .env): {e}")
