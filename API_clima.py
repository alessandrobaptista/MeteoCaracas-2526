import requests
from clases import RegistroClima, RegistroHistoricoMensual

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

def obtener_historial_localidad(latitud, longitud, fecha_inicio, fecha_fin):
    "Consulta el historial climatico mensual de una localidad en Open-Meteo"
    if latitud is None or longitud is None:
        return []

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": fecha_inicio,
        "end_date": fecha_fin,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "auto",
    }

    try:
        "(timeout = 15) ---> Espera maximo 15 segundos la respuesta antes de dar error de conexion "
        resp = requests.get("https://archive-api.open-meteo.com/v1/archive", params=parametros, timeout=15)
    except requests.exceptions.RequestException as i:
        print("No se pudo conectar con el historico de Open-Meteo:", i)
        return []

    if resp.status_code != 200:
        print("Open-Meteo respondio con error:", resp.status_code)
        return []

    horas = resp.json().get("hourly", {})
    marcas = horas.get("time", [])
    if not marcas:
        return []

    "Agrupamos hora por hora en un diccionario (anio, mes) para sacar los promedios"
    grupos = {}
    for pos in range(len(marcas)):
        "cada marca de tiempo llega como '2024-01-15T13:00', el anio son los primeros 4 caracteres y el mes los del 6 al 7"
        anio = int(marcas[pos][0:4])
        mes = int(marcas[pos][5:7])
        clave = (anio, mes)

        if clave not in grupos:
            grupos[clave] = {"temp": [], "hum": [], "lluvia": 0.0, "viento": []}

        grupos[clave]["temp"].append(horas["temperature_2m"][pos])
        grupos[clave]["hum"].append(horas["relative_humidity_2m"][pos])
        grupos[clave]["lluvia"] += horas["precipitation"][pos]
        grupos[clave]["viento"].append(horas["wind_speed_10m"][pos])

    resultado = []
    for (anio, mes) in sorted(grupos.keys()):
        g = grupos[(anio, mes)]
        resultado.append(RegistroHistoricoMensual(
            anio = anio,
            mes = mes,
            temperatura = sum(g["temp"]) / len(g["temp"]),
            humedad = sum(g["hum"]) / len(g["hum"]),
            precipitacion = g["lluvia"],
            viento = sum(g["viento"]) / len(g["viento"]),
        ))

    return resultado
