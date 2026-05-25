import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def cargar_y_limpiar(ruta_archivo):
 
    # Cargar datos
    df = pd.read_excel(ruta_archivo)
    
    # Estandarizar nombres: minusculas y sin espacios
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    
    # Convertir fecha a formato adecuado
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], dayfirst=True)
    
    print("Datos cargados correctamente.")
    print(f"Registros totales: {df.shape[0]} | Variables: {df.shape[1]}")
    
    return df

def calcular_variables_clave(df):

    # Eficiencia: % de contaminante eliminado respecto a la entrada
    df['eficiencia_remocion_dbo_%'] = ((df['dbo_entrada_mg_l'] - df['dbo_salida_mg_l']) / df['dbo_entrada_mg_l']) * 100
    
    # Carga = Concentracion * Caudal / 1000 (indicador de carga real)
    df['carga_contaminante_kg_d'] = (df['dbo_entrada_mg_l'] * df['caudal_entrada_m3_d']) / 1000
    
    # Redondear para mejor lectura
    df = df.round(2)
    return df

def generar_resumen_plantas(df):

    resumen = df.groupby('planta').agg(
        caudal_promedio_m3 = ('caudal_entrada_m3_d', 'mean'),
        dbo_salida_prom = ('dbo_salida_mg_l', 'mean'),
        sst_salida_prom = ('sst_entrada_mg_l', 'mean'), 
        energia_prom = ('energia_aeracion_kwh', 'mean'),
        eficiencia_prom = ('eficiencia_remocion_dbo_%', 'mean'),
        porcentaje_cumplimiento = ('cumplimiento_norma', lambda x: np.mean(x)*100)
    ).reset_index()
    
    return resumen

def exportar_reportes(df):

    #///////REPORTE AREA DE OPERACIONES: Variables de proceso y operacion//////////
    reporte_operativo = df[[
        'fecha_registro', 'planta', 'caudal_entrada_m3_d', 
        'ph_entrada', 'dbo_entrada_mg_l', 'sst_entrada_mg_l', 
        'energia_aeracion_kwh', 'lodos_generados_kg_d', 'cumplimiento_norma'
    ]]
    reporte_operativo.to_excel("reporte_operaciones.xlsx", index=False)

    # /////REPORTE GESTIÓN AMBIENTAL: Datos de calidad y normativa////////////
    reporte_ambiental = df[[
        'fecha_registro', 'planta', 'dbo_salida_mg_l', 'sst_entrada_mg_l', 
        'cumplimiento_norma', 'eficiencia_remocion_dbo_%'
    ]]
    reporte_ambiental.to_excel("reporte_ambiental.xlsx", index=False)
    
    print("Reportes generados: 'reporte_operaciones.xlsx' y 'reporte_ambiental.xlsx'")

def crear_dashboard(df, resumen):
  
    plt.figure(figsize=(16, 12))
    plt.suptitle("Dashboard Exploratorio: Analisis Plantas AquaLimpia", fontsize=16, fontweight='bold')

   
    #////////////// GRAFICO 1: Cumplimiento Normativo (%) por Planta//////////////////////
    
    plt.subplot(2, 2, 1)
    colores = ['#3498db', '#2ecc71', '#f39c12']
    plt.bar(resumen['planta'], resumen['porcentaje_cumplimiento'], color=colores)
    plt.title("1. Porcentaje de Cumplimiento de Norma")
    plt.ylabel("% Cumplimiento")
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    # Agregar valores encima de las barras
    for i, v in enumerate(resumen['porcentaje_cumplimiento']):
        plt.text(i, v + 3, f"{v:.1f}%", ha='center', fontweight='bold')

    
    #/////////////////// GRAFICO 2: Relacion Energia vs Eficiencia //////////////////////////
    
    plt.subplot(2, 2, 2)
    plantas_unicas = df['planta'].unique()
    colores_disp = {'Planta Norte':'#3498db', 'Planta Centro':'#e74c3c', 'Planta Sur':'#2ecc71'}
    
    for planta in plantas_unicas:
        datos_planta = df[df['planta'] == planta]
        plt.scatter(datos_planta['energia_aeracion_kwh'], 
                    datos_planta['eficiencia_remocion_dbo_%'], 
                    label=planta, alpha=0.6, s=50, color=colores_disp[planta])

    plt.title("2. Relacion: Consumo Energetico vs Eficiencia de Remocion")
    plt.xlabel("Energia Aeracion (kWh)")
    plt.ylabel("Eficiencia (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    
    #//////////////////// GRAFICO 3: Distribucion de DBO a la Salida /////////////////////////////
    
    plt.subplot(2, 2, 3)
    datos_por_planta = [df[df['planta'] == p]['dbo_salida_mg_l'] for p in plantas_unicas]
    plt.boxplot(datos_por_planta, labels=plantas_unicas)
    plt.title("3. Variabilidad de Calidad (DBO Salida) por Planta")
    plt.ylabel("DBO (mg/L)")
    plt.axhline(y=50, color='red', linestyle='--', label='Limite Norma (50 mg/L)')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    
    #/////////////////////GRAFICO 4: Eficiencia Promedio ///////////////////////////////////
   
    plt.subplot(2, 2, 4)
    plt.bar(resumen['planta'], resumen['eficiencia_prom'], color=colores)
    plt.title("4. Eficiencia Promedio de Remocion")
    plt.ylabel("Eficiencia (%)")
    plt.ylim(70, 100)
    plt.grid(axis='y', alpha=0.3)

    # Ajustar espacios entre graficos
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("dashboard_aqualimpia.png", dpi=300) 
    plt.show()


if __name__ == "__main__":

    # /////carga del dataset /////
    df_aqua = cargar_y_limpiar("dataset_set_A_aguas_residuales.xlsx")
    
    df_aqua = calcular_variables_clave(df_aqua)
  
    resumen = generar_resumen_plantas(df_aqua)
    print("\nRESUMEN DESEMPEÑO POR PLANTA:")
    print(resumen)
   
    exportar_reportes(df_aqua)
    crear_dashboard(df_aqua, resumen)