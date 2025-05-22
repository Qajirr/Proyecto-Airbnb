# analyzers.py
# Este módulo contendrá funciones y clases para realizar análisis específicos.

import pandas as pd

def analyze_review_trends(df: pd.DataFrame, date_column: str = 'last_review') -> pd.Series:
    """Analiza las tendencias de las reseñas a lo largo del tiempo."""
    if date_column not in df.columns:
        raise ValueError(f"La columna '{date_column}' no se encuentra en el DataFrame.")
    
    # Convierte la columna de fecha a datetime, si no lo está ya
    df_copy = df.copy()
    try:
        df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='coerce')
    except Exception as e:
        print(f"Advertencia: No se pudo convertir la columna '{date_column}' a datetime. Error: {e}")
        # Retorna una serie vacía o maneja el error como prefieras
        return pd.Series(dtype='int64')

    # Elimina filas donde la fecha no pudo ser convertida (NaT)
    df_copy.dropna(subset=[date_column], inplace=True)

    if df_copy.empty:
        print("No hay datos de reseñas válidos después de la conversión de fechas.")
        return pd.Series(dtype='int64')

    review_count_by_year = df_copy[date_column].dt.year.value_counts().sort_index()
    return review_count_by_year

def calculate_correlation_matrix(df: pd.DataFrame, columns_to_correlate: list = None) -> pd.DataFrame:
    """Calcula la matriz de correlación para las columnas numéricas especificadas."""
    if columns_to_correlate:
        numeric_df = df[columns_to_correlate].select_dtypes(include=['number'])
    else:
        numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty:
        print("No hay columnas numéricas para calcular la correlación.")
        return pd.DataFrame()
        
    correlation_matrix = numeric_df.corr()
    return correlation_matrix

def get_descriptive_stats(df: pd.DataFrame, column: str) -> pd.Series:
    """Calcula estadísticas descriptivas para una columna específica."""
    if column not in df.columns:
        raise ValueError(f"La columna '{column}' no se encuentra en el DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise TypeError(f"La columna '{column}' debe ser de tipo numérico para calcular estadísticas descriptivas.")
    return df[column].describe()

def calculate_avg_metric_by_group(df: pd.DataFrame, group_col: str, metric_col: str, agg_func: str = 'mean', sort_values_by_metric: bool = True, ascending: bool = False) -> pd.Series:
    """Calcula una métrica agregada (por defecto, la media) para una columna, agrupada por otra columna."""
    if group_col not in df.columns:
        raise ValueError(f"La columna de agrupación '{group_col}' no se encuentra en el DataFrame.")
    if metric_col not in df.columns:
        raise ValueError(f"La columna de métrica '{metric_col}' no se encuentra en el DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[metric_col]):
        # Permitir 'count' como agg_func incluso para no numéricos
        if agg_func != 'count':
            raise TypeError(f"La columna de métrica '{metric_col}' debe ser numérica para la función de agregación '{agg_func}'.")
    
    grouped_metric = df.groupby(group_col)[metric_col].agg(agg_func)
    if sort_values_by_metric:
        grouped_metric = grouped_metric.sort_values(ascending=ascending)
    else:
        grouped_metric = grouped_metric.sort_index(ascending=ascending)
    return grouped_metric

def get_value_counts(df: pd.DataFrame, column: str, sort_by_index: bool = False) -> pd.Series:
    """Obtiene el conteo de valores para una columna específica."""
    if column not in df.columns:
        raise ValueError(f"La columna '{column}' no se encuentra en el DataFrame.")
    counts = df[column].value_counts()
    if sort_by_index:
        counts = counts.sort_index()
    return counts

if __name__ == '__main__':
    # Para probar, necesitamos el módulo loaders y transformers
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    sys.path.append(str(project_root))

    df_full_example = pd.DataFrame()
    try:
        from src.loaders import download_and_load_listings_csv
        from src.transformers import dataframe_to_geodataframe
        SANTIAGO_LISTINGS_URL = 'https://data.insideairbnb.com/chile/rm/santiago/2023-12-26/visualisations/listings.csv'
        LOCAL_FILE_PATH = 'listings_santiago_analyzers_test.csv.gz'
        df_raw = download_and_load_listings_csv(SANTIAGO_LISTINGS_URL, LOCAL_FILE_PATH, force_download=False)
        if not df_raw.empty:
            df_full_example = dataframe_to_geodataframe(df_raw)
    except ImportError:
        print("Advertencia: No se pudieron importar loaders o transformers. Usando datos de ejemplo limitados.")
    except Exception as e:
        print(f"Advertencia: Error al cargar datos reales: {e}. Usando datos de ejemplo limitados.")

    if df_full_example.empty:
        print("Usando DataFrame de ejemplo simple debido a problemas de carga o para pruebas rápidas.")
        data_example = {
            'id': [1, 2, 3, 4, 5, 6],
            'price': [100, 150, 120, 200, 90, 150],
            'minimum_nights': [1, 2, 1, 3, 2, 1],
            'number_of_reviews': [10, 5, 20, 2, 15, 5],
            'last_review': ['2020-01-15', '2021-03-20', '2020-05-10', '2022-01-01', '2021-11-05', '2021-03-20'],
            'reviews_per_month': [1.0, 0.5, 2.5, 0.1, 1.5, 0.5],
            'neighbourhood': ['Providencia', 'Las Condes', 'Providencia', 'Santiago', 'Las Condes', 'Providencia'],
            'room_type': ['Entire home/apt', 'Private room', 'Entire home/apt', 'Entire home/apt', 'Private room', 'Shared room']
        }
        df_full_example = pd.DataFrame(data_example)

    print("\n--- Análisis de Tendencias de Reseñas ---")
    if 'last_review' in df_full_example.columns:
        review_trends = analyze_review_trends(df_full_example, date_column='last_review')
        print(review_trends)
    else:
        print("Columna 'last_review' no disponible para análisis de tendencias.")

    print("\n--- Matriz de Correlación ---")
    numeric_cols_for_corr = ['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month']
    # Filtrar columnas que realmente existen en el df_full_example
    actual_numeric_cols = [col for col in numeric_cols_for_corr if col in df_full_example.columns and pd.api.types.is_numeric_dtype(df_full_example[col])]
    if actual_numeric_cols:
        corr_matrix = calculate_correlation_matrix(df_full_example, actual_numeric_cols)
        print(corr_matrix)
    else:
        print("No hay suficientes columnas numéricas disponibles para la matriz de correlación.")

    print("\n--- Estadísticas Descriptivas para 'price' ---")
    if 'price' in df_full_example.columns and pd.api.types.is_numeric_dtype(df_full_example['price']):
        price_stats = get_descriptive_stats(df_full_example, 'price')
        print(price_stats)
    else:
        print("Columna 'price' no disponible o no numérica para estadísticas descriptivas.")

    print("\n--- Precio Promedio por 'neighbourhood' ---")
    if 'neighbourhood' in df_full_example.columns and 'price' in df_full_example.columns and pd.api.types.is_numeric_dtype(df_full_example['price']):
        avg_price_neighbourhood = calculate_avg_metric_by_group(df_full_example, 'neighbourhood', 'price', agg_func='mean')
        print(avg_price_neighbourhood.head())
    else:
        print("Columnas 'neighbourhood' o 'price' no disponibles/adecuadas para este análisis.")

    print("\n--- Conteo de Listados por 'room_type' ---")
    if 'room_type' in df_full_example.columns:
        room_type_counts = get_value_counts(df_full_example, 'room_type')
        print(room_type_counts)
    else:
        print("Columna 'room_type' no disponible para conteo de valores.")