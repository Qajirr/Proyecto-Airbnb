# Documentación del Módulo de Generación de Gráficos (`plot_generators.py`)

Este módulo contiene funciones para generar diversas visualizaciones a partir de los datos analizados.

## Funciones

### `create_price_distribution_histogram(df: pd.DataFrame, output_path: Path)`

Genera un histograma de la distribución de precios.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas con los datos.
    - `output_path` (Path): La ruta donde guardar el gráfico.

### `create_reviews_by_year_barplot(review_trends: pd.Series, output_path: Path)`

Genera un gráfico de barras de las tendencias de reseñas por año.

- **Args:**
    - `review_trends` (pd.Series): Serie de pandas con el conteo de reseñas por año.
    - `output_path` (Path): La ruta donde guardar el gráfico.

### `create_correlation_heatmap(correlation_matrix: pd.DataFrame, output_path: Path)`

Genera un mapa de calor de la matriz de correlación.

- **Args:**
    - `correlation_matrix` (pd.DataFrame): La matriz de correlación.
    - `output_path` (Path): La ruta donde guardar el gráfico.

### `create_value_counts_barplot(counts: pd.Series, column_name: str, output_path: Path)`

Genera un gráfico de barras para el conteo de valores de una columna.

- **Args:**
    - `counts` (pd.Series): Serie de pandas con el conteo de valores.
    - `column_name` (str): Nombre de la columna.
    - `output_path` (Path): La ruta donde guardar el gráfico.

### `create_avg_metric_by_group_barplot(avg_metric: pd.Series, group_name: str, metric_name: str, output_path: Path)`

Genera un gráfico de barras para la métrica promedio por grupo.

- **Args:**
    - `avg_metric` (pd.Series): Serie de pandas con la métrica promedio por grupo.
    - `group_name` (str): Nombre de la columna de agrupación.
    - `metric_name` (str): Nombre de la columna de métrica.
    - `output_path` (Path): La ruta donde guardar el gráfico.

### `create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, output_path: Path)`

Genera un gráfico de dispersión entre dos columnas.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas con los datos.
    - `x_col` (str): Nombre de la columna para el eje X.
    - `y_col` (str): Nombre de la columna para el eje Y.
    - `output_path` (Path): La ruta donde guardar el gráfico.

### `create_box_plot(df: pd.DataFrame, column: str, output_path: Path)`

Genera un diagrama de caja para una columna.

- **Args:**
    - `df` (pd.DataFrame): El DataFrame de pandas con los datos.
    - `column` (str): Nombre de la columna para el diagrama de caja.
    - `output_path` (Path): La ruta donde guardar el gráfico.

### `create_geographical_scatter_plot(gdf: gpd.GeoDataFrame, output_path: Path)`

Genera un gráfico de dispersión geográfico a partir de un GeoDataFrame.

- **Args:**
    - `gdf` (gpd.GeoDataFrame): El GeoDataFrame con los datos geoespaciales.
    - `output_path` (Path): La ruta donde guardar el gráfico.