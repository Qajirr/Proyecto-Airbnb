# Documentación del Módulo de Transformación de Datos (`transformers.py`)

Este módulo contiene funciones para la limpieza y transformación de datos, incluyendo la conversión a GeoDataFrame.

## Funciones

### `clean_data(df: pd.DataFrame) -> pd.DataFrame`

Realiza la limpieza de los datos del DataFrame de entrada. (Nota: La implementación específica de esta función no está visible en el contexto proporcionado, por lo que esta descripción es genérica).

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas a limpiar.

- **Returns:**
    - `pd.DataFrame`: El DataFrame limpio.

### `dataframe_to_geodataframe(df: pd.DataFrame) -> gpd.GeoDataFrame`

Convierte un DataFrame de pandas a un GeoDataFrame, asumiendo que contiene columnas de latitud y longitud.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas a convertir.

- **Returns:**
    - `gpd.GeoDataFrame`: El GeoDataFrame resultante.