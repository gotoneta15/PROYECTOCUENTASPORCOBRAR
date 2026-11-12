"""Rutas principales de la API (controlador)."""

import os
from functools import wraps
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename

from app.services.importar_excel import importar_excel, COLUMNAS_ESPERADAS
from app.services.validar_columnas import validar_columnas
from app.services.calcular_totales import calcular_totales
from app.services.calcular_porcentajes import calcular_porcentajes
from app.services.ordenar_riesgo import ordenar_riesgo
from app.services.identificar_vencidos import identificar_vencidos_mas_30
from app.services.detectar_sin_ruta import detectar_clientes_sin_ruta
from app.services.detectar_saldos_negativos import detectar_saldos_negativos
from app.services.generar_indicadores import generar_indicadores

bp = Blueprint("main", __name__)

# Archivo cargado actualmente (en memoria, se reinicia al reiniciar la app)
archivo_actual = {"nombre": None, "registros": None, "clientes_procesados": None}


def login_requerido(f):
    """Decorador que exige haber iniciado sesión para acceder a la ruta."""
    @wraps(f)
    def envoltura(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return envoltura


def usuario_valido(usuario, clave):
    """Valida credenciales contra las variables de entorno APP_USUARIO y APP_CLAVE."""
    usuario_env = os.getenv("APP_USUARIO")
    clave_env = os.getenv("APP_CLAVE")
    return usuario == usuario_env and clave == clave_env


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Pantalla de login: formulario de usuario y contraseña."""
    error = None

    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave = request.form.get("clave", "")

        if usuario_valido(usuario, clave):
            session["usuario"] = usuario
            return redirect(url_for("main.index"))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("login.html", error=error)


@bp.route("/salir")
def salir():
    """Cierra la sesión y redirige al login."""
    session.pop("usuario", None)
    return redirect(url_for("main.login"))


@bp.route("/")
@login_requerido
def index():
    """Pantalla de inicio: formulario para cargar el Excel de insumos."""
    return render_template(
        "inicio.html",
        archivo_actual=archivo_actual["nombre"],
        error=None,
        mensaje_exito=None,
    )


@bp.route("/cargar-archivo", methods=["POST"])
@login_requerido
def cargar_archivo():
    """Recibe el archivo Excel, valida columnas y lo almacena en memoria."""
    global archivo_actual

    if "archivo_excel" not in request.files:
        return render_template(
            "inicio.html",
            archivo_actual=archivo_actual["nombre"],
            error="No se seleccionó ningún archivo.",
            mensaje_exito=None,
        )

    archivo = request.files["archivo_excel"]

    if archivo.filename == "":
        return render_template(
            "inicio.html",
            archivo_actual=archivo_actual["nombre"],
            error="Nombre de archivo vacío.",
            mensaje_exito=None,
        )

    if not archivo.filename.lower().endswith((".xlsx", ".xls")):
        return render_template(
            "inicio.html",
            archivo_actual=archivo_actual["nombre"],
            error="Solo se permiten archivos .xlsx o .xls.",
            mensaje_exito=None,
        )

    # Guardar temporalmente para leerlo
    nombre_seguro = secure_filename(archivo.filename)
    ruta_temporal = os.path.join(current_app.instance_path, nombre_seguro)
    os.makedirs(current_app.instance_path, exist_ok=True)
    archivo.save(ruta_temporal)

    try:
        # R1: Importar Excel
        registros = importar_excel(ruta_temporal)

        # R2: Validar columnas
        encabezados = list(registros[0].keys()) if registros else []
        validacion = validar_columnas(encabezados)

        if not validacion["valido"]:
            os.remove(ruta_temporal)
            return render_template(
                "inicio.html",
                archivo_actual=archivo_actual["nombre"],
                error=validacion["mensaje"],
                mensaje_exito=None,
            )

        # Almacenar en memoria
        archivo_actual["nombre"] = nombre_seguro
        archivo_actual["registros"] = registros

        return render_template(
            "inicio.html",
            archivo_actual=archivo_actual["nombre"],
            error=None,
            mensaje_exito=f"Archivo '{nombre_seguro}' cargado correctamente. {len(registros)} registros importados.",
        )

    except FileNotFoundError:
        return render_template(
            "inicio.html",
            archivo_actual=archivo_actual["nombre"],
            error="No se pudo leer el archivo subido.",
            mensaje_exito=None,
        )
    except ValueError as e:
        return render_template(
            "inicio.html",
            archivo_actual=archivo_actual["nombre"],
            error=str(e),
            mensaje_exito=None,
        )
    except Exception as e:  # pylint: disable=broad-except
        return render_template(
            "inicio.html",
            archivo_actual=archivo_actual["nombre"],
            error=f"Error inesperado: {str(e)}",
            mensaje_exito=None,
        )


@bp.route("/resultados")
@login_requerido
def resultados():
    """Pantalla de resultados: indicadores, semáforos, ranking de clientes."""
    if archivo_actual["registros"] is None:
        return redirect(url_for("main.index"))

    registros = archivo_actual["registros"]

    # Cadena completa de reglas de negocio (R1-R8)
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
    saldos_negativos = detectar_saldos_negativos(todos)
    indicadores = generar_indicadores(todos)

    # Determinar nivel de riesgo y semáforo para cada cliente
    clientes_con_semaforo = []
    for c in ordenados:
        pct = c.get("porcentaje_vencido") or 0
        try:
            pct = float(pct)
        except (TypeError, ValueError):
            pct = 0.0

        if pct >= 50:
            nivel_riesgo = "Crítico"
            semaforo = "Rojo"
        elif pct >= 30:
            nivel_riesgo = "Alto"
            semaforo = "Rojo"
        elif pct >= 10:
            nivel_riesgo = "Medio"
            semaforo = "Amarillo"
        else:
            nivel_riesgo = "Bajo"
            semaforo = "Verde"

        clientes_con_semaforo.append({
            "Cliente": c.get("Cliente") or c.get("cliente"),
            "Ruta": c.get("Ruta") or c.get("ruta"),
            "Unidad_Comercio": c.get("Unidad_Comercio") or c.get("unidad_comercio"),
            "Fecha_Corte": c.get("Fecha_Corte") or c.get("fecha_corte"),
            "Sin_Vencer": c.get("Sin_Vencer") or 0,
            "Vencido_1_30": c.get("Vencido_1_30") or 0,
            "Vencido_31_60": c.get("Vencido_31_60") or 0,
            "Vencido_61_90": c.get("Vencido_61_90") or 0,
            "Vencido_Mas_90": c.get("Vencido_Mas_90") or 0,
            "Total_Cartera": c.get("Total_Cartera") or c.get("total_cartera") or 0,
            "vencidos_totales": c.get("vencidos_totales") or 0,
            "porcentaje_vencido": c.get("porcentaje_vencido") or 0,
            "vencidos_mas_30_dias": c.get("vencidos_mas_30_dias") or 0,
            # Porcentajes de cada columna sobre Total_Cartera
            "porcentaje_Sin_Vencer": c.get("porcentaje_Sin_Vencer") or 0,
            "porcentaje_Vencido_1_30": c.get("porcentaje_Vencido_1_30") or 0,
            "porcentaje_Vencido_31_60": c.get("porcentaje_Vencido_31_60") or 0,
            "porcentaje_Vencido_61_90": c.get("porcentaje_Vencido_61_90") or 0,
            "porcentaje_Vencido_Mas_90": c.get("porcentaje_Vencido_Mas_90") or 0,
            "nivel_riesgo": nivel_riesgo,
            "semaforo": semaforo,
        })

    # Guardar clientes procesados en memoria para el detalle
    archivo_actual["clientes_procesados"] = clientes_con_semaforo

    return render_template(
        "resultados.html",
        archivo_nombre=archivo_actual["nombre"],
        total_clientes=indicadores["total_clientes"],
        total_cartera=indicadores["total_cartera"],
        total_sin_vencer=indicadores["total_sin_vencer"],
        total_vencidos=indicadores["total_vencidos"],
        total_vencidos_mas_30=indicadores["total_vencidos_mas_30"],
        porcentaje_vencido_global=indicadores["porcentaje_vencido_global"],
        conteo_critico=indicadores["conteo_por_nivel"]["critico"],
        conteo_alto=indicadores["conteo_por_nivel"]["alto"],
        conteo_medio=indicadores["conteo_por_nivel"]["medio"],
        conteo_bajo=indicadores["conteo_por_nivel"]["bajo"],
        clientes=clientes_con_semaforo,
    )


@bp.route("/cliente/<nombre_cliente>")
@login_requerido
def detalle_cliente(nombre_cliente):
    """Pantalla de detalle de un cliente específico."""
    if archivo_actual["clientes_procesados"] is None:
        return redirect(url_for("main.index"))

    clientes = archivo_actual["clientes_procesados"]

    # Buscar el cliente por nombre (case-insensitive)
    cliente_encontrado = None
    for c in clientes:
        if (c.get("Cliente") or c.get("cliente") or "").lower() == nombre_cliente.lower():
            cliente_encontrado = c
            break

    if cliente_encontrado is None:
        return render_template(
            "resultados.html",
            archivo_nombre=archivo_actual["nombre"],
            error=f"Cliente '{nombre_cliente}' no encontrado.",
            total_clientes=0,
            total_cartera=0,
            total_sin_vencer=0,
            total_vencidos=0,
            total_vencidos_mas_30=0,
            porcentaje_vencido_global=0,
            conteo_critico=0,
            conteo_alto=0,
            conteo_medio=0,
            conteo_bajo=0,
            clientes=[],
        )

    return render_template(
        "detalle.html",
        cliente=cliente_encontrado,
    )


@bp.route("/salud")
def salud():
    """Endpoint de salud para verificar que el servidor responde."""
    return jsonify({"status": "saludable"}), 200
