"""Módulo de carga y pocedimiento de datos desde el JSON"""

import json
from clases import Localidad, Municipio

def cargar_datos_json(ruta_archivo: str = "zonas_caracas.json"):
    """Lee el archivo JSON y convierte la estructura a objetos Municipio y Localidad."""
    with open(ruta_archivo, "r", encoding = "utf-8") as archivo:
        datos_raw = json.load(archivo)

    lista_municipios = []
    for mun_data in datos_raw:
        municipio = Municipio(mun_data["municipio"])
        for loc_data in mun_data.get("localidades", []):
            localidad = Localidad(
                nombre = loc_data["nombre"],
                latitud = loc_data.get("latitud"),
                longitud = loc_data.get("longitud")
            )
            municipio.agregar_localidad(localidad)
        lista_municipios.append(municipio)

    return lista_municipios

