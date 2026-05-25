#INTEGRACIÓN DE SCRIPTS MODULARES

from procesamiento_modular import cargar_y_limpiar, calcular_variables_clave, generar_resumen_plantas, exportar_reportes
from visualizacion_modular import crear_dashboard


if __name__ == "__main__":

    print("=== EJECUCION VERSION MODULAR ===")
    
    # 1. Carga desde archivo externo
    df_aqua = cargar_y_limpiar("dataset_set_A_aguas_residuales.xlsx")
    
    # 2. Calculos y nuevas metricas con librerias adicionales
    df_procesado = calcular_variables_clave(df_aqua)
  
    # 3. Resumen de desempeño
    resumen_plantas = generar_resumen_plantas(df_procesado)
    print("\nRESUMEN DESEMPEÑO (MODULAR):")
    print(resumen_plantas)
   
    # 4. Generacion de salidas
    exportar_reportes(df_procesado)
    crear_dashboard(df_procesado, resumen_plantas)

    print("\n=== Proceso finalizado: Version Modular completada ===")