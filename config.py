import os
from pathlib import Path

# RUTAS DEL PROYECTO 
BASE_DIR = Path(__file__).resolve().parent
DIR_EXPORTADOS = BASE_DIR / "datos_exportados"
DIR_GRAFICOS = BASE_DIR / "graficos"
DIR_INFORME = BASE_DIR / "informe"

# CONFIGURACIÓN API 1: CLIMA (Open-Meteo)
URL_CLIMA = "https://api.open-meteo.com/v1/forecast"
LAT_DEFAULT = 41.38  # Barcelona
LON_DEFAULT = 2.16


# Solicitamos: Temperatura, Humedad, Sensación Térmica, Probabilidad de Lluvia, Viento
PARAMS_CLIMA = {
    "latitude": LAT_DEFAULT,
    "longitude": LON_DEFAULT,
    "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,wind_speed_10m",
    "forecast_days": 1,
    "timezone": "auto"
}

# ----------------------------------------------
# CONFIGURACIÓN API 2: CRIPTO (COINGECKO)
URL_CRIPTO = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
PARAMS_CRIPTO = {
    "vs_currency": "usd",
    "days": "1"
}

# ----------------------------------------------
#  RESILIENCIA HTTP
TIMEOUT_REQUESTS = 15
MAX_RETRIES = 3
BACKOFF_FACTOR = 1