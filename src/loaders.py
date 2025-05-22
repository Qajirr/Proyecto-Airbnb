# loaders.py
# Este módulo contendrá funciones y clases para cargar datos.

import pandas as pd
import requests
from pathlib import Path

def download_and_load_listings_csv(url: str, download_path: str = 'listings.csv.gz', force_download: bool = False) -> pd.DataFrame:
    """
    Descarga un archivo CSV desde una URL si no existe localmente o si se fuerza la descarga,
    luego lo carga en un DataFrame de pandas.

    Args:
        url (str): La URL desde donde descargar el archivo CSV.
        download_path (str): La ruta local donde guardar/leer el archivo descargado.
        force_download (bool): Si es True, fuerza la descarga incluso si el archivo ya existe.

    Returns:
        pd.DataFrame: El DataFrame cargado desde el archivo CSV.
    """
    file_path = Path(download_path)

    if force_download or not file_path.exists():
        print(f"Descargando datos desde {url}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Datos guardados en {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar el archivo: {e}")
            # Si la descarga falla y el archivo ya existía (y no se forzó la descarga), intenta cargarlo
            if file_path.exists() and not force_download:
                print(f"Intentando cargar datos desde el archivo local existente {file_path}...")
            else:
                raise  # Relanza la excepción si no hay archivo local o se forzó la descarga
    else:
        print(f"Cargando datos desde el archivo local {file_path}")

    try:
        data = pd.read_csv(file_path)
        print("Datos cargados exitosamente.")
        return data
    except Exception as e:
        print(f"Error al leer el archivo CSV {file_path}: {e}")
        raise

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    # Obtener la ruta del directorio raíz del proyecto para cargar .env
    # Asumimos que loaders.py está en src/
    current_script_path = Path(__file__).resolve()
    project_root_path = current_script_path.parent.parent
    dotenv_path = project_root_path / '.env'

    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
        print(f"Archivo .env cargado desde {dotenv_path}")
    else:
        print(f"Advertencia: No se encontró el archivo .env en {dotenv_path}. Usando valores por defecto o esperando que las variables ya estén seteadas.")

    # Ejemplo de uso
    # Usar variables de entorno si están disponibles, con fallbacks por si no
    SANTIAGO_LISTINGS_URL = os.getenv('SANTIAGO_LISTINGS_URL')
    LOCAL_DATA_FOLDER_NAME_EXAMPLE = os.getenv('LOCAL_DATA_FOLDER_NAME')
    LOCAL_FILE_NAME_EXAMPLE = os.getenv('LOCAL_FILE_NAME')
    
    # Construir la ruta completa para el archivo local de prueba
    local_data_path_example = project_root_path / LOCAL_DATA_FOLDER_NAME_EXAMPLE
    local_data_path_example.mkdir(parents=True, exist_ok=True) # Crear carpeta si no existe
    LOCAL_FILE_PATH_EXAMPLE = str(local_data_path_example / LOCAL_FILE_NAME_EXAMPLE)

    print(f"URL para prueba: {SANTIAGO_LISTINGS_URL}")
    print(f"Ruta de archivo local para prueba: {LOCAL_FILE_PATH_EXAMPLE}")

    try:
        # Forzar descarga para la prueba para asegurar que la URL es válida y el proceso funciona
        df_listings = download_and_load_listings_csv(SANTIAGO_LISTINGS_URL, LOCAL_FILE_PATH_EXAMPLE, force_download=True)
        print("\nColumnas del DataFrame cargado:")
        print(df_listings.columns)
        print("\nPrimeras 5 filas del DataFrame:")
        print(df_listings.head())
    except Exception as e:
        print(f"No se pudieron cargar los datos: {e}")