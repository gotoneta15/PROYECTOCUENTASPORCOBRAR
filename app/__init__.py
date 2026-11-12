"""Cartera360 - Factoría de la aplicación Flask (patrón MVC)."""

import os
from flask import Flask

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


def create_app():
    """Crea y configura la instancia de la aplicación Flask."""
    app = Flask(__name__)

    # Clave secreta para sesiones de Flask
    app.secret_key = os.getenv("SECRET_KEY", "cartera360-dev-secret")

    # Registro de blueprints de controladores
    from app.controllers import routes
    app.register_blueprint(routes.bp)

    return app
