"""Punto de entrada WSGI para despliegue de la aplicación."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
