# transformers.py
# Este módulo contendrá funciones y clases para la transformación de datos.

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def dataframe_to_geodataframe(df: pd.DataFrame, lon_col: str = 'longitude', lat_col: str = 'latitude', crs: str = "+init=epsg:4326") -> gpd.GeoDataFrame:
    """
    Convierte un DataFrame de pandas con columnas de longitud y latitud en un GeoDataFrame.

    Args:
        df (pd.DataFrame): El DataFrame de entrada.
        lon_col (str): Nombre de la columna de longitud.
        lat_col (str): Nombre de la columna de latitud.
        crs (str): Sistema de Referencia de Coordenadas a asignar al GeoDataFrame.
                   Por defecto es EPSG:4326.

    Returns:
        gpd.GeoDataFrame: El GeoDataFrame creado.

    Raises:
        ValueError: Si las columnas de longitud o latitud no se encuentran en el DataFrame.
    """
    if not all(col in df.columns for col in [lon_col, lat_col]):
        raise ValueError(f"El DataFrame debe contener las columnas '{lon_col}' y '{lat_col}'.")

    # Crear geometrías de tipo Point a partir de las columnas de longitud y latitud
    # La sintaxis original del notebook era: 
    # xys = data[['longitude', 'latitude']].apply(lambda row: Point(*row), axis=1)
    # gdb = gpd.GeoDataFrame(data.assign(geometry=xys), crs="+init=epsg:4326")
    # Se replica esa lógica aquí:
    
    # Copia para evitar SettingWithCopyWarning si df es una vista
    df_copy = df.copy()
    
    geometry = df_copy[[lon_col, lat_col]].apply(lambda row: Point(row[lon_col], row[lat_col]), axis=1)
    
    # Asigna la nueva columna 'geometry' al DataFrame copiado
    # Usamos assign para devolver un nuevo DataFrame con la columna 'geometry'
    # y luego pasamos este DataFrame modificado al constructor de GeoDataFrame.
    gdf = gpd.GeoDataFrame(df_copy.assign(geometry=geometry), crs=crs)
    
    # Eliminar las columnas originales de latitud y longitud si se desea, 
    # ya que ahora están contenidas en la columna 'geometry'.
    # gdf = gdf.drop(columns=[lon_col, lat_col]) # Opcional

    return gdf

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame eliminando NaNs en columnas críticas y ajustando tipos de datos.
    Esta es una implementación básica y puede necesitar ser extendida.

    Args:
        df (pd.DataFrame): DataFrame de entrada.

    Returns:
        pd.DataFrame: DataFrame limpiado.
    """
    print("Iniciando limpieza de datos...")
    df_cleaned = df.copy()

    # Ejemplo: Imputar NaNs en 'reviews_per_month' con 0, ya que NaN puede significar sin reseñas
    if 'reviews_per_month' in df_cleaned.columns:
        df_cleaned['reviews_per_month'].fillna(0, inplace=True)
        print("Valores NaN en 'reviews_per_month' imputados con 0.")

    # Ejemplo: Convertir 'last_review' a datetime, si no lo está ya
    if 'last_review' in df_cleaned.columns:
        try:
            df_cleaned['last_review'] = pd.to_datetime(df_cleaned['last_review'], errors='coerce')
            print("Columna 'last_review' convertida a datetime.")
        except Exception as e:
            print(f"Advertencia: No se pudo convertir 'last_review' a datetime: {e}")

    # Eliminar filas donde columnas clave como 'price', 'latitude', 'longitude' son NaN
    # ya que son esenciales para muchos análisis y visualizaciones.
    cols_to_check_for_nan = ['price', 'latitude', 'longitude']
    # Filtrar para solo incluir columnas que existen en el DataFrame
    actual_cols_to_check = [col for col in cols_to_check_for_nan if col in df_cleaned.columns]
    
    if actual_cols_to_check:
        original_rows = len(df_cleaned)
        df_cleaned.dropna(subset=actual_cols_to_check, inplace=True)
        rows_dropped = original_rows - len(df_cleaned)
        if rows_dropped > 0:
            print(f"Se eliminaron {rows_dropped} filas debido a NaNs en columnas críticas ({', '.join(actual_cols_to_check)}).")

    # Asegurar que 'price' es numérico (eliminando el símbolo '$' y comas si existen)
    if 'price' in df_cleaned.columns and df_cleaned['price'].dtype == 'object':
        try:
            # Intentar convertir directamente si no hay símbolos de moneda
            df_cleaned['price'] = pd.to_numeric(df_cleaned['price'])
            print("Columna 'price' convertida a tipo numérico.")
        except ValueError:
            # Si falla, intentar eliminar '$' y ',' antes de convertir
            print("Intentando limpiar y convertir la columna 'price' a numérico...")
            df_cleaned['price'] = df_cleaned['price'].astype(str).str.replace(r'[\$,]', '', regex=True)
            df_cleaned['price'] = pd.to_numeric(df_cleaned['price'], errors='coerce')
            # Eliminar filas donde 'price' no pudo ser convertido a numérico (ahora NaN)
            if df_cleaned['price'].isnull().any():
                original_rows_price_conversion = len(df_cleaned)
                df_cleaned.dropna(subset=['price'], inplace=True)
                rows_dropped_price_conversion = original_rows_price_conversion - len(df_cleaned)
                if rows_dropped_price_conversion > 0:
                    print(f"Se eliminaron {rows_dropped_price_conversion} filas donde 'price' no pudo ser convertido a numérico.")
            print("Columna 'price' limpiada y convertida a tipo numérico.")
        except Exception as e:
            print(f"Error al procesar la columna 'price': {e}. Se mantendrá como está o podría tener NaNs.")

    # Limpiar y convertir 'minimum_nights'
    if 'minimum_nights' in df_cleaned.columns:
        df_cleaned['minimum_nights'] = pd.to_numeric(df_cleaned['minimum_nights'], errors='coerce').fillna(0).astype(int)
        print("Columna 'minimum_nights' convertida a int, NaNs imputados con 0.")

    # Limpiar y convertir 'number_of_reviews'
    if 'number_of_reviews' in df_cleaned.columns:
        df_cleaned['number_of_reviews'] = pd.to_numeric(df_cleaned['number_of_reviews'], errors='coerce').fillna(0).astype(int)
        print("Columna 'number_of_reviews' convertida a int, NaNs imputados con 0.")

    # Limpiar columnas categóricas 'room_type' y 'neighbourhood'
    for col_cat in ['room_type', 'neighbourhood']:
        if col_cat in df_cleaned.columns:
            df_cleaned[col_cat] = df_cleaned[col_cat].astype(str).str.strip()
            df_cleaned[col_cat].fillna('Unknown', inplace=True)
            # Reemplazar cadenas vacías con 'Unknown' después de strip
            df_cleaned[col_cat].replace('', 'Unknown', inplace=True) 
            print(f"Columna '{col_cat}' limpiada (string, strip, NaNs/vacío a 'Unknown').")

    print(f"Limpieza de datos completada. Dimensiones del DataFrame: {df_cleaned.shape}")
    return df_cleaned

if __name__ == '__main__':
    # Para probar, necesitamos el módulo loaders
    # Asumimos que loaders.py está en el mismo directorio (src)
    # Para ejecutar este script directamente desde src: python transformers.py
    import sys
    from pathlib import Path
    # Añadir el directorio padre (Proyecto-Airbnb) al sys.path para importar loaders
    # Esto es útil si ejecutas `python src/transformers.py` desde la raíz del proyecto.
    # Si ejecutas desde `src` como `python transformers.py`, entonces `.` es `src`.
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    sys.path.append(str(project_root))

    # Cargar variables de entorno si este script se ejecuta directamente
    import os
    from dotenv import load_dotenv
    dotenv_path = project_root / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
        print(f"Archivo .env cargado desde {dotenv_path} para transformers.py")
    else:
        print(f"Advertencia: No se encontró el archivo .env en {project_root / '.env'} para transformers.py. Usando valores por defecto.")

    try:
        from src.loaders import download_and_load_listings_csv # Ajusta la importación si es necesario
    except ImportError:
        print("Asegúrate de que loaders.py está accesible y los módulos necesarios instalados.")
        print("Intenta ejecutar desde la raíz del proyecto: python -m src.transformers")
        # Como fallback, si la importación falla, creamos un df de ejemplo
        print("Usando DataFrame de ejemplo como fallback por ImportError en loaders.")
        data_example = {
            'id': [1, 2, 3],
            'name': ['Lugar A', 'Lugar B', 'Lugar C'],
            'longitude': [-70.6, -70.5, -70.4],
            'latitude': [-33.4, -33.5, -33.3],
            'price': [100, 150, 120]
        }
        df_listings_example = pd.DataFrame(data_example)
        gdf_created_from_example = True
    else:
        # Usar variables de entorno para URL y path, con fallbacks
        SANTIAGO_LISTINGS_URL_TRANSFORMERS = os.getenv('SANTIAGO_LISTINGS_URL')
        LOCAL_DATA_FOLDER_NAME_TRANSFORMERS = os.getenv('LOCAL_DATA_FOLDER_NAME')
        LOCAL_FILE_NAME_TRANSFORMERS = os.getenv('LOCAL_FILE_NAME')

        # Construir la ruta completa para el archivo local de prueba
        local_data_path_transformers = project_root / LOCAL_DATA_FOLDER_NAME_TRANSFORMERS
        local_data_path_transformers.mkdir(parents=True, exist_ok=True) # Crear carpeta si no existe
        LOCAL_FILE_PATH_TRANSFORMERS = str(local_data_path_transformers / LOCAL_FILE_NAME_TRANSFORMERS)

        print(f"URL para prueba en transformers.py: {SANTIAGO_LISTINGS_URL_TRANSFORMERS}")
        print(f"Ruta de archivo local para prueba en transformers.py: {LOCAL_FILE_PATH_TRANSFORMERS}")

        try:
            df_listings_example = download_and_load_listings_csv(SANTIAGO_LISTINGS_URL_TRANSFORMERS, LOCAL_FILE_PATH_TRANSFORMERS, force_download=True)
            gdf_created_from_example = False
        except Exception as e_load:
            print(f"No se pudieron cargar los datos de Airbnb: {e_load}")
            print("Usando DataFrame de ejemplo como fallback.")
            data_example = {
                'id': [1, 2, 3],
                'name': ['Lugar A', 'Lugar B', 'Lugar C'],
                'longitude': [-70.6, -70.5, -70.4],
                'latitude': [-33.4, -33.5, -33.3],
                'price': [100, 150, 120]
            }
            df_listings_example = pd.DataFrame(data_example)
            gdf_created_from_example = True

    if not df_listings_example.empty:
        try:
            print("\nCreando GeoDataFrame...")
            gdf_listings = dataframe_to_geodataframe(df_listings_example)
            print("GeoDataFrame creado exitosamente.")
            print("\nColumnas del GeoDataFrame:")
            print(gdf_listings.columns)
            print("\nPrimeras 3 filas del GeoDataFrame:")
            print(gdf_listings.head(3))
            print(f"\nCRS del GeoDataFrame: {gdf_listings.crs}")
            if not gdf_created_from_example:
                print(f"\nEl GeoDataFrame tiene {len(gdf_listings)} registros.")
        except ValueError as e:
            print(f"Error al crear GeoDataFrame: {e}")
        except Exception as e_general:
            print(f"Ocurrió un error inesperado: {e_general}")
    else:
        print("El DataFrame de ejemplo está vacío, no se puede crear el GeoDataFrame.")