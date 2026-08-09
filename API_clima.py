import requests
from clases import RegistroClima

"Codigos de clima de open-meteo (WMO) traducidos a texto"
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
    "Consulta el clima actual de una localidad en la API de Open-Meteo"
    if latitud is None or longitud is None:
        return None

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
        "timezone": "auto",
    }



    try:
        "(timeout = 10) ---> Espera maximo 10 segundos la respuesta antes de dar error de conexion "
        resp = requests.get("https://api.open-meteo.com/v1/forecast", params=parametros, timeout=10)
    except requests.exceptions.RequestException as i:
        print("No se pudo conectar con Open-Meteo:", i)
        return None

    

    if resp.status_code != 200:
        "200 es el codigo HTTP que indica que todo esta bien, si no es 200,la peticion fallo"
        print("Open-Meteo respondio con error:", resp.status_code)
        return None

    actual = resp.json().get("current", {})
    codigo = actual.get("weather_code")

    return RegistroClima(
        temperatura = actual.get("temperature_2m", 0.0),
        humedad = actual.get("relative_humidity_2m", 0.0),
        viento = actual.get("wind_speed_10m", 0.0),
        lluvia = actual.get("precipitation", 0.0),
        estado_tiempo =CODIGOS_CLIMA.get(codigo, "Desconocido"),
    )
