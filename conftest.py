"""Configuración de pytest: agrega el directorio raíz al PYTHONPATH."""

import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path para que pytest encuentre el módulo app
root_dir = Path(__file__).parent.resolve()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
