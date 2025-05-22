# Documentación del Módulo de Análisis de Datos (`analyzers.py`)

Este módulo contiene funciones para realizar diversos análisis en los datos de Airbnb.

## Funciones

### `analyze_review_trends(df: pd.DataFrame, date_column: str) -> pd.Series`

Analiza las tendencias de reseñas a lo largo del tiempo basándose en una columna de fecha.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas con los datos.
    - `date_column` (str): El nombre de la columna que contiene las fechas de las reseñas.

- **Returns:**
    - `pd.Series`: Una Serie de pandas con el conteo de reseñas por año.

### `calculate_correlation_matrix(df: pd.DataFrame, columns: list) -> pd.DataFrame`

Calcula la matriz de correlación para un subconjunto de columnas numéricas en el DataFrame.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas con los datos.
    - `columns` (list): Una lista de nombres de columnas numéricas para incluir en la matriz de correlación.

- **Returns:**
    - `pd.DataFrame`: La matriz de correlación.

### `get_value_counts(df: pd.DataFrame, column: str) -> pd.Series`

Calcula el conteo de valores únicos para una columna específica.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas con los datos.
    - `column` (str): El nombre de la columna para la cual calcular el conteo de valores.

- **Returns:**
    - `pd.Series`: Una Serie de pandas con el conteo de cada valor único.

### `calculate_avg_metric_by_group(df: pd.DataFrame, group_column: str, metric_column: str, agg_method: str = 'mean', sort_values_by_metric: bool = False, ascending: bool = False) -> pd.Series`

Calcula una métrica agregada (por defecto, el promedio) para una columna, agrupada por los valores de otra columna.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas con los datos.
    - `group_column` (str): El nombre de la columna por la cual agrupar.
    - `metric_column` (str): El nombre de la columna para la cual calcular la métrica.
    - `agg_method` (str): El método de agregación a usar (por defecto, `'mean'`).
    - `sort_values_by_metric` (bool): Si es `True`, ordena los resultados por la métrica calculada.
    - `ascending` (bool): Si es `True`, ordena de forma ascendente; de lo contrario, descendente.

- **Returns:**
    - `pd.Series`: Una Serie de pandas con la métrica agregada por grupo.