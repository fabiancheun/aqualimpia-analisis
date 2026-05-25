# Análisis de Desempeño Plantas AquaLimpia S.A.

## Objetivo del Proyecto
Analizar el comportamiento operativo y el cumplimiento normativo de las tres plantas de tratamiento de aguas residuales (Norte, Centro y Sur), transformando datos históricos en información útil para identificar fallos, medir eficiencia y apoyar la toma de decisiones gerenciales.

## Estructura de Archivos
El proyecto está organizado de forma ordenada para facilitar su uso:

- `aqualimpia.py`: Script principal en Python. Contiene todo el código de carga, procesamiento, análisis y generación de gráficos.
- `dataset_set_A_aguas_residuales.xlsx`: Archivo de datos original. Contiene los registros históricos de operación y calidad. *Este archivo no se modifica.*
- `reporte_operaciones.xlsx`: Reporte generado automáticamente. Incluye variables detalladas de proceso para el área técnica.
- `reporte_ambiental.xlsx`: Reporte generado automáticamente. Contiene indicadores de calidad y cumplimiento para gestión ambiental.
- `dashboard_aqualimpia.png`: Imagen generada con los gráficos comparativos de desempeño.

## Proceso Analítico Realizado
El análisis sigue un flujo de trabajo estructurado y reproducible:

1.  **Ingesta y Limpieza:** Se cargan los datos y se estandarizan nombres y formatos para asegurar calidad y coherencia.
2.  **Transformación:** Se calculan métricas clave no presentes en los datos brutos:
    *   *Eficiencia de remoción:* Porcentaje de contaminante eliminado.
    *   *Carga contaminante:* Medida real de masa tratada.
3.  **Análisis Comparativo:** Se agrupa la información por planta para obtener promedios, consumos y tasas de cumplimiento normativo.
4.  **Visualización:** Se construye un panel exploratorio para evaluar cumplimiento, relación energía-calidad y estabilidad operativa.
5.  **Generación de Salidas:** Se exportan reportes adaptados a las necesidades de cada área de la empresa.

## Resultados Principales
Tras la ejecución del análisis, se obtuvieron las siguientes conclusiones:

-   **Cumplimiento Normativo:** La Planta Sur presenta el mejor desempeño (29,6% de cumplimiento), seguida por Planta Centro (22,7%) y Planta Norte (16,9%).
-   **Eficiencia Técnica:** Las tres plantas tienen capacidad de tratamiento similar, con una eficiencia de remoción promedio cercana al 87%.
-   **Relación Energía-Calidad:** Se confirma que mayor consumo de aireación mejora la calidad del efluente, hasta llegar a un límite donde el rendimiento deja de aumentar.
-   **Estabilidad Operativa:** La Planta Centro es la más inestable, superando frecuentemente los límites permitidos, mientras que la Planta Sur demuestra mayor consistencia y confiabilidad en sus resultados.

## Instrucciones de Ejecución
1.  Ubicar todos los archivos en una misma carpeta.
2.  Ejecutar el script `aqualimpia.py` en entorno Python con las librerías Pandas, Matplotlib y NumPy instaladas.
3.  Los reportes y la imagen del gráfico se actualizarán automáticamente en la misma ubicación.