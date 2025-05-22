# plot_generators.py
# Este módulo contendrá funciones para generar gráficos, preferiblemente con Plotly.

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

import geopandas as gpd

import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno para la configuración de Plotly
# Esto es principalmente para cuando el script se ejecuta directamente.
# Cuando es importado por src/main.py, .env ya debería estar cargado.
_current_file_path = Path(__file__).resolve()
_project_root_for_env = _current_file_path.parent.parent # Asume que plot_generators.py está en src/
_env_path = _project_root_for_env / '.env'

if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    # Fallback si .env no se encuentra en la raíz del proyecto (ej. ejecución desde otro contexto)
    # Intentar cargar .env desde la ubicación de src/main.py si es diferente
    # Esto es un intento, puede que necesite ajuste según la estructura real de ejecución
    if (Path(os.getcwd()) / '.env').exists():
        load_dotenv() # Carga .env desde el directorio de trabajo actual

import plotly.io as pio
# Configuración del tema por defecto para Plotly desde variable de entorno
PLOTLY_THEME = os.getenv('PLOTLY_THEME', 'plotly_dark') # Default a plotly_dark si no está definida
pio.templates.default = PLOTLY_THEME
DEFAULT_MAPBOX_STYLE = os.getenv('MAPBOX_STYLE', 'open-street-map') # Default si no está definida

def create_price_distribution_histogram(df: pd.DataFrame, price_column: str = 'price', title: str = 'Distribución de Precios', price_upper_limit: float = None) -> go.Figure:
    """Genera un histograma de la distribución de precios, con un filtro opcional de límite superior."""
    if price_column not in df.columns:
        raise ValueError(f"La columna '{price_column}' no se encuentra en el DataFrame.")
    
    df_to_plot = df.copy()
    if price_upper_limit is not None:
        df_to_plot = df_to_plot[df_to_plot[price_column] < price_upper_limit]
        title += f" (Precios < {price_upper_limit})"

    if df_to_plot.empty:
        # Devuelve una figura vacía o un mensaje si no hay datos después de filtrar
        fig = go.Figure()
        fig.update_layout(title=title + " - No hay datos para mostrar", xaxis_title=price_column, yaxis_title='Frecuencia')
        return fig
        
    fig = px.histogram(df_to_plot, x=price_column, title=title, marginal="box",
                       labels={price_column: 'Precio'})
    fig.update_layout(bargap=0.1)
    return fig

def create_reviews_by_year_barplot(review_counts: pd.Series, title: str = 'Número de Reseñas por Año') -> go.Figure:
    """Genera un gráfico de barras del número de reseñas por año."""
    if not isinstance(review_counts, pd.Series):
        raise TypeError("El argumento 'review_counts' debe ser una Serie de pandas.")
    
    fig = px.bar(x=review_counts.index, y=review_counts.values, title=title,
                 labels={'x': 'Año', 'y': 'Número de Reseñas'})
    fig.update_layout(xaxis_type='category') # Asegura que los años se traten como categorías
    return fig

def create_correlation_heatmap(correlation_matrix: pd.DataFrame, title: str = 'Mapa de Calor de Correlación') -> go.Figure:
    """Genera un mapa de calor de la matriz de correlación."""
    if not isinstance(correlation_matrix, pd.DataFrame) or correlation_matrix.empty:
        raise ValueError("La 'correlation_matrix' debe ser un DataFrame de pandas no vacío.")

    fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto",
                    title=title, color_continuous_scale='viridis') # Puedes cambiar 'viridis' por otro esquema de color
    return fig

def create_value_counts_barplot(value_counts_series: pd.Series, title: str, xaxis_title: str, yaxis_title: str = 'Conteo') -> go.Figure:
    """Genera un gráfico de barras a partir de una serie de conteo de valores."""
    if not isinstance(value_counts_series, pd.Series):
        raise TypeError("El argumento 'value_counts_series' debe ser una Serie de pandas.")
    
    fig = px.bar(value_counts_series,
                 x=value_counts_series.index,
                 y=value_counts_series.values,
                 title=title,
                 labels={'x': xaxis_title, 'y': yaxis_title})
    fig.update_layout(xaxis_type='category')
    return fig

def create_avg_metric_by_group_barplot(avg_metric_series: pd.Series, title: str, xaxis_title: str, yaxis_title: str) -> go.Figure:
    """Genera un gráfico de barras a partir de una serie de métricas promedio agrupadas."""
    if not isinstance(avg_metric_series, pd.Series):
        raise TypeError("El argumento 'avg_metric_series' debe ser una Serie de pandas.")

    fig = px.bar(avg_metric_series,
                 x=avg_metric_series.index,
                 y=avg_metric_series.values,
                 title=title,
                 labels={'x': xaxis_title, 'y': yaxis_title})
    fig.update_layout(xaxis_type='category')
    return fig

def create_geographical_scatter_plot(gdf: gpd.GeoDataFrame, color_column: str = None, size_column: str = None, title: str = 'Distribución Geográfica de Listings', mapbox_style: str = None, zoom: int = 10, hover_name_column: str = None, custom_data_cols: list = None) -> go.Figure:
    """Genera un mapa de dispersión geográfico de los listings."""
    # Usar el estilo de mapbox por defecto desde la variable de entorno si no se especifica uno.
    if mapbox_style is None:
        mapbox_style = DEFAULT_MAPBOX_STYLE
    """Genera un mapa de dispersión geográfico de los listings."""
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("El argumento 'gdf' debe ser un GeoDataFrame.")
    if 'geometry' not in gdf.columns or not gdf.geometry.is_valid.all():
        raise ValueError("El GeoDataFrame debe tener una columna 'geometry' válida.")

    # Asegurarse de que las coordenadas estén en EPSG:4326 para Mapbox
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        print(f"Convirtiendo CRS de {gdf.crs} a EPSG:4326 para visualización...")
        gdf = gdf.to_crs(epsg=4326)

    # Extraer latitud y longitud para Plotly
    # Plotly espera columnas separadas de lat y lon, no objetos de geometría directamente para scatter_mapbox
    gdf_display = gdf.copy()
    gdf_display['latitude'] = gdf_display.geometry.y
    gdf_display['longitude'] = gdf_display.geometry.x

    plot_args = {
        'data_frame': gdf_display,
        'lat': 'latitude',
        'lon': 'longitude',
        'title': title,
        'zoom': zoom,
        'height': 700 # Ajustar altura del mapa
    }

    if color_column:
        if color_column not in gdf_display.columns:
            raise ValueError(f"La columna de color '{color_column}' no se encuentra en el GeoDataFrame.")
        plot_args['color'] = color_column
    
    if size_column:
        if size_column not in gdf_display.columns:
            raise ValueError(f"La columna de tamaño '{size_column}' no se encuentra en el GeoDataFrame.")
        if not pd.api.types.is_numeric_dtype(gdf_display[size_column]):
            raise TypeError(f"La columna de tamaño '{size_column}' debe ser numérica.")
        plot_args['size'] = size_column
        # Evitar tamaños negativos o cero si se usan para 'size'
        if (gdf_display[size_column] <= 0).any():
            print(f"Advertencia: La columna '{size_column}' contiene valores no positivos. Se reemplazarán con un valor pequeño para graficar.")
            # Reemplazar no positivos con un valor pequeño o manejar como se prefiera
            min_positive_size = gdf_display[gdf_display[size_column] > 0][size_column].min() / 2 if (gdf_display[size_column] > 0).any() else 1
            gdf_display[size_column] = gdf_display[size_column].apply(lambda x: x if x > 0 else min_positive_size)
            plot_args['data_frame'] = gdf_display # Actualizar el dataframe en los argumentos

    if hover_name_column:
        if hover_name_column not in gdf_display.columns:
            raise ValueError(f"La columna hover_name '{hover_name_column}' no se encuentra.")
        plot_args['hover_name'] = hover_name_column

    if custom_data_cols:
        if not all(col in gdf_display.columns for col in custom_data_cols):
            missing_cols = [col for col in custom_data_cols if col not in gdf_display.columns]
            raise ValueError(f"Las siguientes columnas custom_data no se encuentran: {missing_cols}")
        plot_args['custom_data'] = custom_data_cols

    fig = px.scatter_mapbox(**plot_args)
    fig.update_layout(mapbox_style=mapbox_style, margin={"r":0,"t":50,"l":0,"b":0})
    return fig

def create_scatter_plot(df: pd.DataFrame, x_column: str, y_column: str, color_column: str = None, size_column: str = None, title: str = 'Gráfico de Dispersión', xaxis_title: str = None, yaxis_title: str = None, hover_name_column: str = None) -> go.Figure:
    """Genera un gráfico de dispersión utilizando Plotly Express."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El argumento 'df' debe ser un DataFrame de pandas.")
    if x_column not in df.columns:
        raise ValueError(f"La columna x '{x_column}' no se encuentra en el DataFrame.")
    if y_column not in df.columns:
        raise ValueError(f"La columna y '{y_column}' no se encuentra en el DataFrame.")

    plot_args = {
        'data_frame': df,
        'x': x_column,
        'y': y_column,
        'title': title,
        'labels': {x_column: xaxis_title if xaxis_title else x_column, 
                   y_column: yaxis_title if yaxis_title else y_column}
    }

    if color_column:
        if color_column not in df.columns:
            raise ValueError(f"La columna de color '{color_column}' no se encuentra en el DataFrame.")
        plot_args['color'] = color_column
    
    if size_column:
        if size_column not in df.columns:
            raise ValueError(f"La columna de tamaño '{size_column}' no se encuentra en el DataFrame.")
        if not pd.api.types.is_numeric_dtype(df[size_column]):
            raise TypeError(f"La columna de tamaño '{size_column}' debe ser numérica.")
        plot_args['size'] = size_column
        # Evitar tamaños negativos o cero si se usan para 'size'
        if (df[size_column] <= 0).any():
            print(f"Advertencia: La columna '{size_column}' contiene valores no positivos. Se reemplazarán con un valor pequeño para graficar.")
            min_positive_size = df[df[size_column] > 0][size_column].min() / 2 if (df[size_column] > 0).any() else 1
            df_copy = df.copy()
            df_copy[size_column] = df_copy[size_column].apply(lambda x: x if x > 0 else min_positive_size)
            plot_args['data_frame'] = df_copy

    if hover_name_column:
        if hover_name_column not in df.columns:
            raise ValueError(f"La columna hover_name '{hover_name_column}' no se encuentra.")
        plot_args['hover_name'] = hover_name_column

    fig = px.scatter(**plot_args)
    return fig

def create_box_plot(df: pd.DataFrame, x_column: str, y_column: str, color_column: str = None, title: str = 'Diagrama de Caja', xaxis_title: str = None, yaxis_title: str = None, points: str = 'outliers') -> go.Figure:
    """Genera un diagrama de caja utilizando Plotly Express."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El argumento 'df' debe ser un DataFrame de pandas.")
    if x_column not in df.columns:
        raise ValueError(f"La columna x '{x_column}' no se encuentra en el DataFrame.")
    if y_column not in df.columns:
        raise ValueError(f"La columna y '{y_column}' no se encuentra en el DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[y_column]):
        raise TypeError(f"La columna y '{y_column}' debe ser numérica para un diagrama de caja.")

    plot_args = {
        'data_frame': df,
        'x': x_column,
        'y': y_column,
        'title': title,
        'labels': {x_column: xaxis_title if xaxis_title else x_column, 
                   y_column: yaxis_title if yaxis_title else y_column},
        'points': points
    }

    if color_column:
        if color_column not in df.columns:
            raise ValueError(f"La columna de color '{color_column}' no se encuentra en el DataFrame.")
        plot_args['color'] = color_column

    fig = px.box(**plot_args)
    return fig

if __name__ == '__main__':
    # Para probar, necesitamos los módulos loaders, transformers y analyzers
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    sys.path.append(str(project_root))

    # Asegurar que las variables de entorno se cargan para las pruebas si este script se ejecuta directamente
    # (ya se hace al inicio del script, pero una doble verificación o carga explícita aquí podría ser útil
    # si la lógica de carga superior se vuelve condicional)
    # load_dotenv(project_root / '.env') # Ya se maneja arriba de forma más robusta

    gdf_full_example = gpd.GeoDataFrame() # Inicializar como GeoDataFrame vacío
    df_raw_example = pd.DataFrame() # Para datos no geográficos

    try:
        from src.loaders import download_and_load_listings_csv
        from src.transformers import dataframe_to_geodataframe
        from src.analyzers import analyze_review_trends, calculate_correlation_matrix, get_value_counts, calculate_avg_metric_by_group

        SANTIAGO_LISTINGS_URL = 'https://data.insideairbnb.com/chile/rm/santiago/2023-12-26/visualisations/listings.csv'
        LOCAL_FILE_PATH = 'listings_santiago_plots_test.csv.gz'
        df_raw_example = download_and_load_listings_csv(SANTIAGO_LISTINGS_URL, LOCAL_FILE_PATH, force_download=False)
        
        if not df_raw_example.empty:
            required_geo_cols = ['longitude', 'latitude']
            if all(col in df_raw_example.columns for col in required_geo_cols):
                 gdf_full_example = dataframe_to_geodataframe(df_raw_example)
                 other_cols_to_ensure = ['price', 'last_review', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'room_type', 'neighbourhood', 'name', 'id']
                 for col in other_cols_to_ensure:
                     if col not in gdf_full_example.columns and col in df_raw_example.columns:
                         gdf_full_example[col] = df_raw_example[col]
            else:
                print("Advertencia: Faltan columnas de longitud/latitud para crear GeoDataFrame. Algunas pruebas de gráficos geográficos pueden fallar.")

    except ImportError:
        print("Advertencia: No se pudieron importar todos los módulos. Usando datos de ejemplo limitados.")
    except Exception as e:
        print(f"Advertencia: Error al cargar/transformar datos reales: {e}. Usando datos de ejemplo limitados.")

    if df_raw_example.empty or not all(col in df_raw_example.columns for col in ['price', 'last_review', 'room_type', 'neighbourhood', 'number_of_reviews', 'minimum_nights']):
        print("Usando DataFrame de ejemplo simple debido a problemas de carga o para pruebas rápidas.")
        data_for_df = {
            'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'name': [f'Lugar {i}' for i in range(1,11)],
            'price': [100, 150, 120, 200, 90, 110, 220, 130, 180, 95],
            'last_review': pd.to_datetime(['2020-01-15', '2021-03-20', '2020-05-10', '2022-01-01', '2021-11-05',
                            '2020-02-20', '2021-07-10', '2020-09-01', '2022-03-15', '2021-12-25']),
            'minimum_nights': [1, 2, 1, 3, 2, 1, 4, 2, 3, 1],
            'number_of_reviews': [10, 5, 20, 2, 15, 8, 3, 12, 6, 18],
            'reviews_per_month': [1.0, 0.5, 2.5, 0.1, 1.5, 0.8, 0.2, 1.2, 0.6, 1.8],
            'room_type': ['Entire home/apt', 'Private room', 'Entire home/apt', 'Private room', 'Shared room', 'Entire home/apt', 'Private room', 'Entire home/apt', 'Private room', 'Shared room'],
            'neighbourhood': ['Providencia', 'Las Condes', 'Providencia', 'Santiago', 'Las Condes', 'Providencia', 'Ñuñoa', 'Santiago', 'Las Condes', 'Ñuñoa'],
            'longitude': [-70.6, -70.5, -70.61, -70.65, -70.52, -70.59, -70.58, -70.66, -70.53, -70.57],
            'latitude': [-33.4, -33.3, -33.42, -33.45, -33.32, -33.41, -33.46, -33.44, -33.33, -33.47]
        }
        df_raw_example = pd.DataFrame(data_for_df)
        if all(col in df_raw_example.columns for col in ['longitude', 'latitude']):
            gdf_full_example = dataframe_to_geodataframe(df_raw_example)
        else:
            gdf_full_example = gpd.GeoDataFrame(df_raw_example) 

    df_for_plots = gdf_full_example if not gdf_full_example.empty and 'price' in gdf_full_example.columns else df_raw_example

    print("\n--- Iniciando pruebas de generación de gráficos ---")

    # 1. Histograma de distribución de precios
    if 'price' in df_for_plots.columns:
        try:
            fig_price_dist_full = create_price_distribution_histogram(df_for_plots, title='Distribución de Todos los Precios')
            print("1. Histograma de distribución de todos los precios generado.")
            fig_price_dist_filtered = create_price_distribution_histogram(df_for_plots, price_upper_limit=200000, title='Distribución de Precios (Menores a 200k)')
            print("1. Histograma de distribución de precios filtrados generado.")
        except ValueError as e:
            print(f"Error al generar histograma de precios: {e}")
    else:
        print("Columna 'price' no disponible para histograma.")

    # 2. Gráfico de barras de reseñas por año
    if 'last_review' in df_for_plots.columns:
        try:
            review_trends_example = analyze_review_trends(df_for_plots, date_column='last_review')
            if not review_trends_example.empty:
                fig_reviews_year = create_reviews_by_year_barplot(review_trends_example)
                print("2. Gráfico de barras de reseñas por año generado.")
            else:
                print("No hay datos de tendencias de reseñas para graficar.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de reseñas por año: {e}")
    else:
        print("Columna 'last_review' no disponible para gráfico de reseñas por año.")

    # 3. Mapa de calor de correlación
    numeric_cols_corr = ['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month']
    actual_numeric_cols_corr = [col for col in numeric_cols_corr if col in df_for_plots.columns and pd.api.types.is_numeric_dtype(df_for_plots[col])]
    if actual_numeric_cols_corr:
        try:
            corr_matrix_example = calculate_correlation_matrix(df_for_plots, actual_numeric_cols_corr)
            if not corr_matrix_example.empty:
                fig_corr_heatmap = create_correlation_heatmap(corr_matrix_example)
                print("3. Mapa de calor de correlación generado.")
            else:
                print("Matriz de correlación vacía, no se genera mapa de calor.")
        except ValueError as e:
            print(f"Error al generar mapa de calor: {e}")
    else:
        print("No hay suficientes columnas numéricas para el mapa de calor.")

    # 4. Gráfico de barras de conteo de room_type
    if 'room_type' in df_for_plots.columns:
        try:
            room_type_counts_series = get_value_counts(df_for_plots, 'room_type')
            if not room_type_counts_series.empty:
                fig_room_type_counts = create_value_counts_barplot(room_type_counts_series, title='Conteo de Tipos de Habitación', xaxis_title='Tipo de Habitación')
                print("4. Gráfico de conteo de tipos de habitación generado.")
            else:
                print("No hay datos de conteo de tipos de habitación para graficar.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de tipos de habitación: {e}")
    else:
        print("Columna 'room_type' no disponible para gráfico de conteo.")

    # 5. Gráfico de barras de precio promedio por neighbourhood
    if 'neighbourhood' in df_for_plots.columns and 'price' in df_for_plots.columns and pd.api.types.is_numeric_dtype(df_for_plots['price']):
        try:
            avg_price_neighbourhood_series = calculate_avg_metric_by_group(df_for_plots, group_col='neighbourhood', metric_col='price', agg_func='mean', sort_values_by_metric=True, ascending=False).head(10)
            if not avg_price_neighbourhood_series.empty:
                fig_avg_price_neighbourhood = create_avg_metric_by_group_barplot(avg_price_neighbourhood_series, title='Top 10 Barrios por Precio Promedio', xaxis_title='Barrio', yaxis_title='Precio Promedio')
                print("5. Gráfico de precio promedio por barrio generado.")
            else:
                print("No hay datos de precio promedio por barrio para graficar.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de precio promedio por barrio: {e}")
    else:
        print("Columnas 'neighbourhood' o 'price' no disponibles/adecuadas para gráfico de precio promedio.")

    # 6. Mapa de dispersión geográfico
    if not gdf_full_example.empty and 'geometry' in gdf_full_example.columns:
        try:
            color_col_geo = 'price' if 'price' in gdf_full_example.columns else None
            size_col_geo = 'number_of_reviews' if 'number_of_reviews' in gdf_full_example.columns and pd.api.types.is_numeric_dtype(gdf_full_example['number_of_reviews']) else None
            hover_name_geo = 'name' if 'name' in gdf_full_example.columns else None
            custom_data_geo = ['id', 'room_type'] if all(c in gdf_full_example.columns for c in ['id', 'room_type']) else None 
            fig_geo_scatter = create_geographical_scatter_plot(gdf_full_example, color_column=color_col_geo, size_column=size_col_geo, hover_name_column=hover_name_geo, custom_data_cols=custom_data_geo, title='Distribución Geográfica de Listings (Santiago)')
            print("6. Mapa de dispersión geográfico generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar mapa de dispersión geográfico: {e}")
    else:
        print("GeoDataFrame vacío o sin columna 'geometry', no se puede generar mapa geográfico.")

    # 7. Gráfico de dispersión de precio vs. número de reseñas
    if all(col in df_for_plots.columns for col in ['price', 'number_of_reviews']):
        try:
            color_scatter = 'room_type' if 'room_type' in df_for_plots.columns else None
            size_scatter = 'minimum_nights' if 'minimum_nights' in df_for_plots.columns and pd.api.types.is_numeric_dtype(df_for_plots['minimum_nights']) else None
            fig_scatter_price_reviews = create_scatter_plot(df_for_plots, 
                                                            x_column='price', 
                                                            y_column='number_of_reviews', 
                                                            color_column=color_scatter, 
                                                            size_column=size_scatter,
                                                            title='Precio vs. Número de Reseñas',
                                                            xaxis_title='Precio',
                                                            yaxis_title='Número de Reseñas')
            print("7. Gráfico de dispersión Precio vs. Número de Reseñas generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de dispersión Precio vs. Número de Reseñas: {e}")
    else:
        print("Columnas 'price' o 'number_of_reviews' no disponibles para gráfico de dispersión.")

    # 8. Diagrama de caja de precio por tipo de habitación
    if all(col in df_for_plots.columns for col in ['room_type', 'price']) and pd.api.types.is_numeric_dtype(df_for_plots['price']):
        try:
            fig_boxplot_price_roomtype = create_box_plot(df_for_plots, 
                                                         x_column='room_type', 
                                                         y_column='price', 
                                                         color_column='room_type',
                                                         title='Distribución de Precios por Tipo de Habitación',
                                                         xaxis_title='Tipo de Habitación',
                                                         yaxis_title='Precio')
            print("8. Diagrama de caja Precio por Tipo de Habitación generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar diagrama de caja Precio por Tipo de Habitación: {e}")
    else:
        print("Columnas 'room_type' o 'price' no disponibles/adecuadas para diagrama de caja.")

    print("\n--- Pruebas de generación de gráficos completadas ---")