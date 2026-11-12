@echo off
:: =============================================================================
/// Cartera360 - Script de inicio de la aplicación Flask
// =============================================================================

echo Iniciando Cartera360...

:: Activar entorno virtual de uv si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call ".venv\Scripts\activate.bat"
) else (
    echo Advertencia: No se encontró el entorno virtual .venv
)

:: Instalar dependencias si es necesario
echo Verificando dependencias con uv...
uv sync

:: Iniciar la aplicación Flask en segundo plano
echo Iniciando servidor Flask...
start /B uv run flask --app wsgi.py run --host=127.0.0.1 --port=5000

:: Esperar a que el servidor esté listo
echo Esperando a que el servidor esté listo...
timeout /t 5 /nobreak >nul

:: Abrir el navegador en la URL de la app
echo Abriendo navegador en http://127.0.0.1:5000/
start "" "http://127.0.0.1:5000/"

echo Cartera360 está corriendo en http://127.0.0.1:5000/
echo Presiona cualquier clave para detener el servidor...
pause >nul

:: Detener el servidor Flask
taskkill /f /im python.exe >nul 2>&1
echo Servidor detenido.
