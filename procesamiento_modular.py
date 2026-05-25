import pandas as pd
import numpy as np
from scipy import stats  # Libreria adicional para analisis estadistico

def cargar_y_limpiar(ruta_archivo):
   
    df = pd.read_excel(ruta_archivo)
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], dayfirst=True)
    
    print("Datos cargados correctamente.")
    print(f"Registros totales: {df.shape[0]} | Variables: {df.shape[1]}")
    return df

def calcular_variables_clave(df):
  
    df['eficiencia_remocion_dbo_%'] = ((df['dbo_entrada_mg_l'] - df['dbo_salida_mg_l']) / df['dbo_entrada_mg_l']) * 100
    df['carga_contaminante_kg_d'] = (df['dbo_entrada_mg_l'] * df['caudal_entrada_m3_d']) / 1000

    
    df['z_score'] = np.abs(stats.zscore(df['dbo_salida_mg_l']))
    df['alerta_anomalia'] = np.where(df['z_score'] > 2.5, 'SI', 'NO')
    
    return df.round(2)

def generar_resumen_plantas(df):
   
    resumen = df.groupby('planta').agg(
        caudal_promedio_m3 = ('caudal_entrada_m3_d', 'mean'),
        dbo_salida_prom = ('dbo_salida_mg_l', 'mean'),
        sst_salida_prom = ('sst_entrada_mg_l', 'mean'), 
        energia_prom = ('energia_aeracion_kwh', 'mean'),
        eficiencia_prom = ('eficiencia_remocion_dbo_%', 'mean'),
        porcentaje_cumplimiento = ('cumplimiento_norma', lambda x: np.mean(x)*100),
        dias_con_alerta = ('alerta_anomalia', 'sum') # Nueva columna de analisis
    ).reset_index()
    return resumen

def exportar_reportes(df):
   
    reporte_operativo = df[[
        'fecha_registro', 'planta', 'caudal_entrada_m3_d', 'ph_entrada', 
        'dbo_entrada_mg_l', 'sst_entrada_mg_l', 'energia_aeracion_kwh', 
        'lodos_generados_kg_d', 'cumplimiento_norma', 'alerta_anomalia'
    ]]
    reporte_operativo.to_excel("reporte_operaciones_modular.xlsx", index=False)

    reporte_ambiental = df[[
        'fecha_registro', 'planta', 'dbo_salida_mg_l', 'sst_entrada_mg_l', 
        'cumplimiento_norma', 'eficiencia_remocion_dbo_%'
    ]]
    reporte_ambiental.to_excel("reporte_ambiental_modular.xlsx", index=False)
    
    print("Reportes modulares generados correctamente.")