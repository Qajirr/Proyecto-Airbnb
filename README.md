# Proyecto-Airbnb

Este repositorio contiene el código para el proyecto de análisis de datos de Airbnb. El proyecto incluye módulos para la ingesta de datos, preprocesamiento, análisis, modelado y visualización.

Para obtener documentación detallada sobre cada módulo, consulte la carpeta `/docs`:

- [Visión General](docs/overview.md)
- [Carga de Datos](docs/loaders.md)
- [Análisis de Datos](docs/analyzers.md)
- [Preprocesamiento](docs/transformers.md)
- [Generación de Gráficos](docs/plot_generators.md)

## Uso

Para empezar con el proyecto, sigue estos pasos:

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/Qajirr/Proyecto-Airbnb.git
    cd Proyecto-Airbnb
    ```

2.  **Crear un entorno virtual e instalar dependencias:**

    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # En Windows
    # source .venv/bin/activate  # En macOS/Linux
    pip install -r requirements.txt
    ```

3.  **Configurar variables de entorno:**

    Crea un archivo `.env` en la raíz del proyecto basado en `.env.example` y añade tus credenciales o configuraciones necesarias.

4.  **Ejecutar el pipeline principal:**

    ```bash
    python main.py
    ```

Este comando ejecutará el pipeline completo, desde la ingesta de datos hasta la generación de visualizaciones.