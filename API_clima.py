import requests
from clases import RegistroClima

# 'tabla de codigos de clima de open-meteo (WMO)'
CODIGOS_CLIMA = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna intensa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia intensa",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    95: "Tormenta electrica",
    96: "Tormenta con granizo",
}


def obtener_clima_localidad(latitud, longitud):
    # 'si la localidad no tiene coordenadas no hay nada que consultar'
    if latitud is None or longitud is None:
        return None

    # parametros que le pedimos a la API, "current" es lo que queremos del clima de ahorita
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
        "timezone": "auto",
    }

    try:
        resp = requests.get("https://api.open-meteo.com/v1/forecast", params=parametros, timeout=8)
    except requests.exceptions.RequestException as i:
        # esto salta si no hay internet, o si la API no responde a tiempo
        print("No se pudo conectar con Open-Meteo:", i)
        return None

    if resp.status_code != 200:
        print("Open-Meteo respondio con error:", resp.status_code)
        return None

    actual = resp.json().get("current", {})
    codigo = actual.get("weather_code")  # esto es el numero que despues traducimos con CODIGOS_CLIMA

    return RegistroClima(
        temperatura = actual.get("temperature_2m", 0.0),
        humedad = actual.get("relative_humidity_2m", 0.0),
        viento = actual.get("wind_speed_10m", 0.0),
        lluvia = actual.get("precipitation", 0.0),
        estado_tiempo =CODIGOS_CLIMA.get(codigo, "Desconocido"),
    )
