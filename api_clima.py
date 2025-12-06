import pandas as pd
from helpers.utils import obtener_session_resiliente
from interfaces import FuenteDeDatos
import config

class ServicioClima(FuenteDeDatos):
    """Implementación concreta para Open-Meteo."""
    
    def __init__(self):
        self.session = obtener_session_resiliente()
        
    def obtener_datos(self) -> pd.DataFrame:
        try:
            response = self.session.get(
                config.URL_CLIMA, 
                params=config.PARAMS_CLIMA, 
                timeout=config.TIMEOUT_REQUESTS
            )
            response.raise_for_status()
            
            data = response.json()
            hourly = data.get('hourly', {})
            
            if not hourly: return pd.DataFrame()

            # ETL Climático
            df = pd.DataFrame({
                'fecha_hora': pd.to_datetime(hourly.get('time', [])),
                'temperatura_c': hourly.get('temperature_2m', []),
                'sensacion_termica_c': hourly.get('apparent_temperature', []),
                'humedad_relativa_%': hourly.get('relative_humidity_2m', []),
                'probabilidad_lluvia_%': hourly.get('precipitation_probability', []),
                'velocidad_viento_kmh': hourly.get('wind_speed_10m', [])
            })
            
            print(f"[CLIMA] Datos obtenidos: {len(df)} registros.")
            return df
            
        except Exception as e:
            print(f"[CLIMA] Error: {e}")
            return pd.DataFrame()