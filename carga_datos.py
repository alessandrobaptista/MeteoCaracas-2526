import json
from clases import Localidad, Municipio

def cargar_datos_json(ruta_archivo: str = "zonas_caracas.json"):
    "Lee el archivo JSON y convierte la estructura a objetos Municipio y Localidad"
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos_raw = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar el archivo de datos: {e}")
        return []

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

def generar_resumen_coordenadas(municipios: list):
    "Imprime el resumen de localidades con y sin coordenadas"
    print("\n-- Resumen de coordenadas por municipio --")
    for m in municipios:
        print(f"\nMunicipio: {m.nombre}")
        print(f" - Total localidades: {m.total_localidades()}")
        print(f" - Con coordenadas: {m.localidades_con_coordenadas()}")
        print(f" - Sin coordenadas: {m.localidades_sin_coordenadas()}")

def buscar_localidad(municipios: list, nombre_localidad: str):
    "Busca y retorna un objeto Localidad por su nombre"
    nombre_buscar = nombre_localidad.strip().lower()
    for m in municipios:
        for loc in m.localidades:
            if loc.nombre.lower() == nombre_buscar:
                return loc
    return None

