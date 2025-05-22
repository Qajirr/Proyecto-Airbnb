# main.py
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

def run_main_application():
    """Configura el entorno y ejecuta la aplicación principal."""
    # Añadir el directorio raíz del proyecto al sys.path
    # para permitir importaciones como from src.module import ...
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))

    # Cargar variables de entorno desde .env en la raíz del proyecto
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"Archivo .env cargado desde {env_path} por el main.py raíz.")
    else:
        print(f"Advertencia: Archivo .env no encontrado en {env_path}. La aplicación podría no funcionar como se espera.")

    try:
        from src.main import main as src_main
    except ImportError as e:
        print(f"Error al importar src.main: {e}")
        print("Asegúrate de que la estructura del proyecto es correcta y PYTHONPATH está configurado si es necesario.")
        print(f"sys.path actual: {sys.path}")
        return

    src_main()

if __name__ == "__main__":
    run_main_application()