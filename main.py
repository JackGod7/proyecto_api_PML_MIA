import pandas as pd
import config
from helpers import utils
from api_clima import ServicioClima
from api_segunda import ServicioCripto
from visualizer import Visualizador

def ejecutar_pipeline():
    print("- INICIANDO SISTEMA -")
    
    # 1. Inicialización
    utils.inicializar_directorios()
    viz_engine = Visualizador()
    
    # 2. Ingesta de Datos
    servicios = {
        'clima': ServicioClima(),
        'crypto': ServicioCripto()
    }
    
    data_warehouse = {}
    
    print("\n[FASE 1] Ingesta de Datos...")
    for nombre, servicio in servicios.items():
        data_warehouse[nombre] = servicio.obtener_datos()
        
    df_clima = data_warehouse['clima']
    df_btc = data_warehouse['crypto']

    # Validación de integridad
    if df_clima.empty or df_btc.empty:
        print("[ERROR] Fallo crítico en la obtención de datos. Revise logs.")
        return

    # 3. Exportación de Resultados
    print("\n[FASE 2] Exportación de Resultados...")
    ruta_excel = config.DIR_EXPORTADOS / "Resultados_Consolidados.xlsx"
    
    try:
        with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
            df_clima.to_excel(writer, sheet_name='Dataset_Clima', index=False)
            df_btc.to_excel(writer, sheet_name='Dataset_Bitcoin', index=False)
            
            # Estadísticas descriptivas
            df_clima.describe().to_excel(writer, sheet_name='Stats_Clima')
            df_btc.describe().to_excel(writer, sheet_name='Stats_Bitcoin')
            
        print(f"[EXCEL] Reporte generado: {ruta_excel}")
    except Exception as e:
        print(f"[EXCEL] Error de I/O: {e}")

    # 4. Capa de Presentación (Visualización)
    print("\n[FASE 3] Generación de Dashboard...")
    try:
        viz_engine.generar_dashboard(df_clima, df_btc)
    except Exception as e:
        print(f"[VIZUALIZACION] Error renderizando gráficos: {e}")
        import traceback
        traceback.print_exc()

    print("\n- PROCESO FINALIZADO -")

if __name__ == "__main__":
    ejecutar_pipeline()