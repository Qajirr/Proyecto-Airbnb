import pandas as pd
import geopandas as gpd
from pathlib import Path
import os
from dotenv import load_dotenv
from plotly.offline import plot # Descomentar si se desea guardar/mostrar plots

# Asegurarse de que el directorio src esté en el PYTHONPATH para importaciones directas
import sys
current_dir = Path(__file__).parent
project_root = current_dir.parent # Asumiendo que src está en la raíz del proyecto
sys.path.append(str(project_root))

# Cargar variables de entorno desde .env
load_dotenv(project_root / '.env')

try:
    from src.loaders import download_and_load_listings_csv
    from src.transformers import dataframe_to_geodataframe, clean_data # Asumiendo que clean_data existe o se añadirá
    from src.analyzers import (
        analyze_review_trends,
        calculate_correlation_matrix,
        get_value_counts,
        calculate_avg_metric_by_group
    )
    from src.plot_generators import (
        create_price_distribution_histogram,
        create_reviews_by_year_barplot,
        create_correlation_heatmap,
        create_value_counts_barplot,
        create_avg_metric_by_group_barplot,
        create_scatter_plot,
        create_box_plot,
        create_geographical_scatter_plot
    )
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de que el proyecto esté estructurado correctamente y que src esté en el PYTHONPATH.")
    sys.exit(1)

SANTIAGO_LISTINGS_URL = os.getenv('SANTIAGO_LISTINGS_URL')
LOCAL_DATA_FOLDER_NAME = os.getenv('LOCAL_DATA_FOLDER_NAME', 'data') # Default to 'data' if not set
LOCAL_FILE_NAME = os.getenv('LOCAL_FILE_NAME')

LOCAL_DATA_PATH = project_root / LOCAL_DATA_FOLDER_NAME
LOCAL_FILE_PATH = LOCAL_DATA_PATH / LOCAL_FILE_NAME

# Crear directorio data si no existe
LOCAL_DATA_PATH.mkdir(parents=True, exist_ok=True)

def _perform_data_analysis(df_analysis):
    """Helper function to perform various data analyses."""
    print("\n--- 3. Realizando Análisis ---")
    review_trends = pd.Series(dtype='int64')
    correlation_matrix = pd.DataFrame()
    room_type_counts = pd.Series(dtype='int64')
    avg_price_by_neighbourhood = pd.Series(dtype='float64')

    try:
        if 'last_review' in df_analysis.columns:
            review_trends = analyze_review_trends(df_analysis, 'last_review')
            print(f"Tendencias de reseñas analizadas. Años encontrados: {review_trends.index.tolist()}")
        else:
            print("Columna 'last_review' no encontrada para analizar tendencias de reseñas.")

        numeric_cols_corr = ['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month']
        actual_numeric_cols_corr = [col for col in numeric_cols_corr if col in df_analysis.columns and pd.api.types.is_numeric_dtype(df_analysis[col])]
        if actual_numeric_cols_corr:
            correlation_matrix = calculate_correlation_matrix(df_analysis, actual_numeric_cols_corr)
            print("Matriz de correlación calculada.")
        else:
            print("No hay suficientes columnas numéricas para calcular la matriz de correlación.")

        if 'room_type' in df_analysis.columns:
            room_type_counts = get_value_counts(df_analysis, 'room_type')
            print(f"Conteo de tipos de habitación: {room_type_counts.to_dict()}")
        else:
            print("Columna 'room_type' no encontrada.")

        if 'neighbourhood' in df_analysis.columns and 'price' in df_analysis.columns and pd.api.types.is_numeric_dtype(df_analysis['price']):
            avg_price_by_neighbourhood = calculate_avg_metric_by_group(df_analysis, 'neighbourhood', 'price', 'mean', sort_values_by_metric=True, ascending=False).head(10)
            print(f"Precio promedio por los 10 barrios principales calculado.")
        else:
            print("Columnas 'neighbourhood' o 'price' no disponibles/adecuadas para calcular precio promedio por barrio.")

    except Exception as e:
        print(f"Error durante el análisis de datos: {e}")
        # Continuar para intentar generar gráficos con lo que se tenga, 
        # las variables de resultados mantendrán sus valores por defecto (vacíos)

    return review_trends, correlation_matrix, room_type_counts, avg_price_by_neighbourhood

def _generate_all_visualizations(df_analysis, review_trends, correlation_matrix, room_type_counts, avg_price_by_neighbourhood, gdf, output_plots_path):
    """Helper function to generate and print status of all visualizations."""
    print("\n--- 4. Generando Gráficos ---")
    print(f"Los gráficos se guardarán (si se activa la función plot) en: {output_plots_path}")

    # Lógica para generar y guardar los gráficos individuales
    # Las funciones de generación de gráficos (create_...) devuelven figuras de Plotly.
    # Necesitarías añadir lógica aquí para llamar a esas funciones y guardar las figuras si es necesario.

    # 4.1 Histograma de distribución de precios
    if 'price' in df_analysis.columns:
        try:
            fig_price_dist_full = create_price_distribution_histogram(df_analysis, title='Distribución de Todos los Precios')
            plot(fig_price_dist_full, filename=str(output_plots_path / 'price_distribution_full.html')) # Descomentar si se usa plotly.offline.plot
            print("Histograma de distribución de todos los precios generado.")
            # fig_price_dist_filtered = create_price_distribution_histogram(df_analysis, price_upper_limit=200000, title='Distribución de Precios (Menores a 200k)')
            # plot(fig_price_dist_filtered, filename=output_plots_path / 'price_distribution_filtered.html') # Descomentar si se usa plotly.offline.plot
            # print("Histograma de distribución de precios filtrados generado.")
        except ValueError as e:
            print(f"Error al generar histograma de precios: {e}")

    # 4.2 Gráfico de barras de reseñas por año
    if not review_trends.empty:
        try:
            fig_reviews_year = create_reviews_by_year_barplot(review_trends)
            plot(fig_reviews_year, filename=str(output_plots_path / 'reviews_by_year.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de barras de reseñas por año generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de reseñas por año: {e}")

    # 4.3 Mapa de calor de correlación
    if not correlation_matrix.empty:
        try:
            fig_corr_heatmap = create_correlation_heatmap(correlation_matrix)
            plot(fig_corr_heatmap, filename=str(output_plots_path / 'correlation_heatmap.html')) # Descomentar si se usa plotly.offline.plot
            print("Mapa de calor de correlación generado.")
        except ValueError as e:
            print(f"Error al generar mapa de calor: {e}")

    # 4.4 Gráfico de barras de conteo de room_type
    if not room_type_counts.empty:
        try:
            fig_room_type_counts = create_value_counts_barplot(room_type_counts, title='Conteo de Tipos de Habitación', xaxis_title='Tipo de Habitación')
            plot(fig_room_type_counts, filename=str(output_plots_path / 'room_type_counts.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de conteo de tipos de habitación generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de tipos de habitación: {e}")

    # 4.5 Gráfico de barras de precio promedio por neighbourhood
    if not avg_price_by_neighbourhood.empty:
        try:
            fig_avg_price_neighbourhood = create_avg_metric_by_group_barplot(avg_price_by_neighbourhood, title='Precio Promedio por Barrio (Top 10)', xaxis_title='Barrio', yaxis_title='Precio Promedio')
            plot(fig_avg_price_neighbourhood, filename=str(output_plots_path / 'avg_price_by_neighbourhood.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de precio promedio por barrio generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de precio promedio por barrio: {e}")

    # 4.6 Mapa de dispersión geográfico
    if gdf is not None and not gdf.empty and 'price' in gdf.columns:
        try:
            fig_geo_scatter = create_geographical_scatter_plot(gdf, color_column='price', size_column='price', title='Distribución Geográfica de Precios', hover_name_column='name', custom_data_cols=['room_type', 'minimum_nights'])
            plot(fig_geo_scatter, filename=str(output_plots_path / 'geo_price_distribution.html')) # Descomentar si se usa plotly.offline.plot
            print("Mapa de dispersión geográfico generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar mapa de dispersión geográfico: {e}")

    # 4.7 Gráfico de dispersión general (ejemplo: precio vs minimum_nights)
    if 'price' in df_analysis.columns and 'minimum_nights' in df_analysis.columns:
        try:
            fig_scatter_price_nights = create_scatter_plot(df_analysis, x_column='minimum_nights', y_column='price', color_column='room_type', title='Precio vs Mínimo de Noches', xaxis_title='Mínimo de Noches', yaxis_title='Precio', hover_name_column='name')
            plot(fig_scatter_price_nights, filename=str(output_plots_path / 'price_vs_minimum_nights.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de dispersión (precio vs minimum_nights) generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de dispersión (precio vs minimum_nights): {e}")

    # 4.8 Diagrama de caja (ejemplo: precio por room_type)
    if 'room_type' in df_analysis.columns and 'price' in df_analysis.columns:
        try:
            fig_box_price_room = create_box_plot(df_analysis, x_column='room_type', y_column='price', title='Distribución de Precios por Tipo de Habitación', xaxis_title='Tipo de Habitación', yaxis_title='Precio')
            plot(fig_box_price_room, filename=str(output_plots_path / 'price_by_room_type_box.html')) # Descomentar si se usa plotly.offline.plot
            print("Diagrama de caja (precio por room_type) generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar diagrama de caja (precio por room_type): {e}")

    print("Generación de gráficos completada.")

def main():
    """Función principal para ejecutar el pipeline de análisis de Airbnb."""
    print("--- Iniciando pipeline de análisis de datos de Airbnb ---")

    # 1. Carga de datos
    print("\n--- 1. Cargando Datos ---")
    try:
        df_raw = download_and_load_listings_csv(SANTIAGO_LISTINGS_URL, str(LOCAL_FILE_PATH), force_download=False)
        if df_raw.empty:
            print("No se pudieron cargar los datos. Terminando ejecución.")
            return
        print(f"Datos crudos cargados: {df_raw.shape[0]} filas, {df_raw.shape[1]} columnas.")
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return

    # 2. Transformación y Limpieza de Datos
    print("\n--- 2. Transformando y Limpiando Datos ---")
    gdf = None
    try:
        # Limpieza de datos utilizando la función clean_data
        df_cleaned = clean_data(df_raw)
        if df_cleaned.empty:
            print("El DataFrame quedó vacío después de la limpieza. Terminando ejecución.")
            return
        print(f"Datos limpios: {df_cleaned.shape[0]} filas, {df_cleaned.shape[1]} columnas.")
        
        # Convertir a GeoDataFrame
        if 'longitude' in df_cleaned.columns and 'latitude' in df_cleaned.columns:
            gdf = dataframe_to_geodataframe(df_cleaned)
            print(f"GeoDataFrame creado: {gdf.shape[0]} filas, {gdf.shape[1]} columnas.")
        else:
            print("Advertencia: No se encontraron columnas 'longitude'/'latitude'. Se continuará sin datos geoespaciales para algunos gráficos.")
            gdf = gpd.GeoDataFrame(df_cleaned) # Puede que no tenga geometría
    except Exception as e:
        print(f"Error durante la transformación de datos: {e}")
        return

    # DataFrame a usar para análisis y plots (priorizar gdf si tiene datos)
    df_analysis = gdf if gdf is not None and not gdf.empty else df_cleaned
    if df_analysis.empty:
        print("DataFrame para análisis está vacío. Terminando.")
        return

    # 3. Análisis de Datos
    review_trends, correlation_matrix, room_type_counts, avg_price_by_neighbourhood = _perform_data_analysis(df_analysis)

    # 4. Generación de Gráficos
    OUTPUT_PLOTS_FOLDER_NAME = os.getenv('OUTPUT_PLOTS_FOLDER_NAME', 'plots') # Default to 'plots' if not set
    output_plots_path = project_root / OUTPUT_PLOTS_FOLDER_NAME
    output_plots_path.mkdir(parents=True, exist_ok=True)

    # Lógica para generar y guardar los gráficos individuales
    # Las funciones de generación de gráficos (create_...) devuelven figuras de Plotly.
    # Necesitarías añadir lógica aquí para llamar a esas funciones y guardar las figuras si es necesario.

    # 4.1 Histograma de distribución de precios
    if 'price' in df_analysis.columns:
        try:
            fig_price_dist_full = create_price_distribution_histogram(df_analysis, title='Distribución de Todos los Precios')
            plot(fig_price_dist_full, filename=str(output_plots_path / 'price_distribution_full.html')) # Descomentar si se usa plotly.offline.plot
            print("Histograma de distribución de todos los precios generado.")
            # fig_price_dist_filtered = create_price_distribution_histogram(df_analysis, price_upper_limit=200000, title='Distribución de Precios (Menores a 200k)')
            # plot(fig_price_dist_filtered, filename=output_plots_path / 'price_distribution_filtered.html') # Descomentar si se usa plotly.offline.plot
            # print("Histograma de distribución de precios filtrados generado.")
        except ValueError as e:
            print(f"Error al generar histograma de precios: {e}")

    # 4.2 Gráfico de barras de reseñas por año
    if not review_trends.empty:
        try:
            fig_reviews_year = create_reviews_by_year_barplot(review_trends)
            plot(fig_reviews_year, filename=str(output_plots_path / 'reviews_by_year.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de barras de reseñas por año generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de reseñas por año: {e}")

    # 4.3 Mapa de calor de correlación
    if not correlation_matrix.empty:
        try:
            fig_corr_heatmap = create_correlation_heatmap(correlation_matrix)
            plot(fig_corr_heatmap, filename=str(output_plots_path / 'correlation_heatmap.html')) # Descomentar si se usa plotly.offline.plot
            print("Mapa de calor de correlación generado.")
        except ValueError as e:
            print(f"Error al generar mapa de calor: {e}")

    # 4.4 Gráfico de barras de conteo de room_type
    if not room_type_counts.empty:
        try:
            fig_room_type_counts = create_value_counts_barplot(room_type_counts, title='Conteo de Tipos de Habitación', xaxis_title='Tipo de Habitación')
            plot(fig_room_type_counts, filename=str(output_plots_path / 'room_type_counts.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de conteo de tipos de habitación generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de tipos de habitación: {e}")

    # 4.5 Gráfico de barras de precio promedio por neighbourhood
    if not avg_price_by_neighbourhood.empty:
        try:
            fig_avg_price_neighbourhood = create_avg_metric_by_group_barplot(avg_price_by_neighbourhood, title='Precio Promedio por Barrio (Top 10)', xaxis_title='Barrio', yaxis_title='Precio Promedio')
            plot(fig_avg_price_neighbourhood, filename=str(output_plots_path / 'avg_price_by_neighbourhood.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de precio promedio por barrio generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de precio promedio por barrio: {e}")

    # 4.6 Mapa de dispersión geográfico
    if gdf is not None and not gdf.empty and 'price' in gdf.columns:
        try:
            fig_geo_scatter = create_geographical_scatter_plot(gdf, color_column='price', size_column='price', title='Distribución Geográfica de Precios', hover_name_column='name', custom_data_cols=['room_type', 'minimum_nights'])
            plot(fig_geo_scatter, filename=str(output_plots_path / 'geo_price_distribution.html')) # Descomentar si se usa plotly.offline.plot
            print("Mapa de dispersión geográfico generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar mapa de dispersión geográfico: {e}")

    # 4.7 Gráfico de dispersión general (ejemplo: precio vs minimum_nights)
    if 'price' in df_analysis.columns and 'minimum_nights' in df_analysis.columns:
        try:
            fig_scatter_price_nights = create_scatter_plot(df_analysis, x_column='minimum_nights', y_column='price', color_column='room_type', title='Precio vs Mínimo de Noches', xaxis_title='Mínimo de Noches', yaxis_title='Precio', hover_name_column='name')
            plot(fig_scatter_price_nights, filename=str(output_plots_path / 'price_vs_minimum_nights.html')) # Descomentar si se usa plotly.offline.plot
            print("Gráfico de dispersión (precio vs minimum_nights) generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar gráfico de dispersión (precio vs minimum_nights): {e}")

    # 4.8 Diagrama de caja (ejemplo: precio por room_type)
    if 'room_type' in df_analysis.columns and 'price' in df_analysis.columns:
        try:
            fig_box_price_room = create_box_plot(df_analysis, x_column='room_type', y_column='price', title='Distribución de Precios por Tipo de Habitación', xaxis_title='Tipo de Habitación', yaxis_title='Precio')
            plot(fig_box_price_room, filename=str(output_plots_path / 'price_by_room_type_box.html')) # Descomentar si se usa plotly.offline.plot
            print("Diagrama de caja (precio por room_type) generado.")
        except (TypeError, ValueError) as e:
            print(f"Error al generar diagrama de caja (precio por room_type): {e}")

    print("Generación de gráficos completada.")

    print("\n--- Pipeline de análisis de datos de Airbnb completado ---")

if __name__ == '__main__':
    main()