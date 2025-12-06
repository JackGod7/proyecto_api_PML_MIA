import pandas as pd
from helpers.utils import obtener_session_resiliente
from interfaces import FuenteDeDatos
import config

class ServicioCripto(FuenteDeDatos):
    """Implementación concreta para api de CoinGecko."""
    
    def __init__(self):
        self.session = obtener_session_resiliente()
        
    def obtener_datos(self) -> pd.DataFrame:
        try:
            response = self.session.get(
                config.URL_CRIPTO,
                params=config.PARAMS_CRIPTO,
                timeout=config.TIMEOUT_REQUESTS
            )
            response.raise_for_status()
            
            data = response.json()
            prices = data.get('prices', [])
            
            if not prices: return pd.DataFrame()

            # ETL Cripto
            df = pd.DataFrame(prices, columns=['timestamp', 'priceUsd'])
            df['fecha_hora'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['precio_btc_usd'] = df['priceUsd'].astype(float)
            
            # Seleccionamos y ordenamos columnas
            df = df[['fecha_hora', 'precio_btc_usd']]
            
            print(f"[CRIPTO] Datos obtenidos: {len(df)} registros.")
            return df

        except Exception as e:
            print(f"[CRIPTO] Error: {e}")
            return pd.DataFrame()