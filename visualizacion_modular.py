import matplotlib.pyplot as plt
import seaborn as sns  

def crear_dashboard(df, resumen):
  

    sns.set_style("whitegrid")
    plt.figure(figsize=(16, 12))
    plt.suptitle("Dashboard Modular: Analisis Plantas AquaLimpia", fontsize=16, fontweight='bold')

# GRAFICO 1: Cumplimiento Normativo
    plt.subplot(2, 2, 1)
    colores = ['#3498db', '#2ecc71', '#f39c12']
    plt.bar(resumen['planta'], resumen['porcentaje_cumplimiento'], color=colores)
    plt.title("1. Porcentaje de Cumplimiento de Norma")
    plt.ylabel("% Cumplimiento")
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    for i, v in enumerate(resumen['porcentaje_cumplimiento']):
        plt.text(i, v + 3, f"{v:.1f}%", ha='center', fontweight='bold')

# GRAFICO 2: Relacion Energia vs Eficiencia
    plt.subplot(2, 2, 2)
    plantas_unicas = df['planta'].unique()
    colores_disp = {'Planta Norte':'#3498db', 'Planta Centro':'#e74c3c', 'Planta Sur':'#2ecc71'}
    for planta in plantas_unicas:
        datos_planta = df[df['planta'] == planta]
        plt.scatter(datos_planta['energia_aeracion_kwh'], datos_planta['eficiencia_remocion_dbo_%'], 
                    label=planta, alpha=0.6, s=50, color=colores_disp[planta])
    plt.title("2. Relacion: Consumo Energetico vs Eficiencia de Remocion")
    plt.xlabel("Energia Aeracion (kWh)")
    plt.ylabel("Eficiencia (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)

# GRAFICO 3: Variabilidad de Calidad
    plt.subplot(2, 2, 3)
    datos_por_planta = [df[df['planta'] == p]['dbo_salida_mg_l'] for p in plantas_unicas]
    plt.boxplot(datos_por_planta, labels=plantas_unicas)
    plt.title("3. Variabilidad de Calidad (DBO Salida) por Planta")
    plt.ylabel("DBO (mg/L)")
    plt.axhline(y=50, color='red', linestyle='--', label='Limite Norma (50 mg/L)')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

# GRAFICO 4: Eficiencia Promedio
    plt.subplot(2, 2, 4)
    plt.bar(resumen['planta'], resumen['eficiencia_prom'], color=colores)
    plt.title("4. Eficiencia Promedio de Remocion")
    plt.ylabel("Eficiencia (%)")
    plt.ylim(70, 100)
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("dashboard_modular_aqualimpia.png", dpi=300) 
    plt.show()