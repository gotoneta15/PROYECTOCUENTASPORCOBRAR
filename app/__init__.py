"""Cartera360 - Factoría de la aplicación Flask (patrón MVC)."""

from flask import Flask


def create_app():
    """Crea y configura la instancia de la aplicación Flask."""
    app = Flask(__name__)

    # Registro de blueprints de controladores
    from app.controllers import routes
    app.register_blueprint(routes.bp)

    return app
