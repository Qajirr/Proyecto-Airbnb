# Documentación General del Proyecto Airbnb Analysis

Este documento sirve como punto de partida para entender la estructura y el funcionamiento del proyecto de análisis de datos de Airbnb.

## Estructura del Proyecto

El proyecto sigue una estructura modular para separar las diferentes etapas del pipeline de análisis:

- `/src`: Contiene el código fuente principal.
    - `main.py`: Punto de entrada del pipeline.
    - `loaders.py`: Módulo para la carga de datos.
    - `transformers.py`: Módulo para la transformación y limpieza de datos.
    - `analyzers.py`: Módulo para el análisis de datos.
    - `plot_generators.py`: Módulo para la generación de visualizaciones.
- `/data`: Carpeta para almacenar los datos descargados.
- `/plots`: Carpeta para almacenar los gráficos generados.
- `/docs`: Carpeta para la documentación.
- `/tests`: Carpeta para las pruebas unitarias.
- `.env`: Archivo para variables de entorno (no incluido en el repositorio por seguridad).
- `requirements.txt`: Lista de dependencias del proyecto.

## Pipeline de Análisis

El pipeline de análisis se ejecuta a través de `main.py` y consta de las siguientes etapas:

1.  **Carga de Datos:** Descarga y carga el conjunto de datos de Airbnb.
2.  **Transformación y Limpieza:** Procesa los datos crudos para prepararlos para el análisis.
3.  **Análisis de Datos:** Realiza análisis estadísticos y exploratorios.
4.  **Generación de Gráficos:** Crea visualizaciones a partir de los resultados del análisis.

## Módulos Detallados

A continuación, se listan los documentos de cada módulo para una referencia más detallada:

- [Módulo de Carga de Datos (`loaders.py`)](loaders.md)
- [Módulo de Transformación de Datos (`transformers.py`)](transformers.md)
- [Módulo de Análisis de Datos (`analyzers.py`)](analyzers.md)
- [Módulo de Generación de Gráficos (`plot_generators.py`)](plot_generators.md)

---

*Nota: Este documento se actualizará a medida que el proyecto evolucione.*