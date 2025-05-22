# Documentación del Módulo de Carga de Datos (`loaders.py`)

Este módulo contiene funciones para la ingesta de datos, principalmente descargando archivos CSV desde URLs y cargándolos en DataFrames de pandas.

## Funciones

### `download_and_load_listings_csv(url: str, download_path: str = 'listings.csv.gz', force_download: bool = False) -> pd.DataFrame`

Descarga un archivo CSV desde una URL si no existe localmente o si se fuerza la descarga, luego lo carga en un DataFrame de pandas.

- **Args:**
    - `url` (str): La URL desde donde descargar el archivo CSV.
    - `download_path` (str): La ruta local donde guardar/leer el archivo descargado. Por defecto es `'listings.csv.gz'`.
    - `force_download` (bool): Si es `True`, fuerza la descarga incluso si el archivo ya existe. Por defecto es `False`.

- **Returns:**
    - `pd.DataFrame`: El DataFrame cargado desde el archivo CSV.

- **Excepciones:**
    - `requests.exceptions.RequestException`: Si ocurre un error durante la descarga.
    - `Exception`: Si ocurre un error al leer el archivo CSV.