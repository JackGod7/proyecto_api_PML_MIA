import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import os
import sys

# Ajuste de ruta para importar config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def obtener_session_resiliente() -> requests.Session:
    """
    Sesión HTTP con Retry Strategy - Singleton pattern.
    """
    session = requests.Session()
    
    # Configuración de reintentos
    retry_strategy = Retry(
        total=config.MAX_RETRIES,
        backoff_factor=config.BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def inicializar_directorios():
    """Genera las carpetas de salida si no existen."""
    dirs = [config.DIR_EXPORTADOS, config.DIR_GRAFICOS, config.DIR_INFORME]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def exportar_excel(df: pd.DataFrame, nombre_archivo: str):
    """Guarda DataFrame en Excel en la ruta configurada."""
    try:
        ruta = config.DIR_EXPORTADOS / nombre_archivo
        df.to_excel(ruta, index=False, engine='openpyxl')
        print(f"[IO] Excel guardado: {ruta}")
    except Exception as e:
        print(f"[IO] Error exportando Excel: {e}")