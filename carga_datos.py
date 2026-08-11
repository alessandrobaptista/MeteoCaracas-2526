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
    for mun_data, lista_locs in datos_raw.items():
        municipio = Municipio(mun_data)

        for loc_data in lista_locs:
            localidad = Localidad(
                nombre = loc_data.get("localidad"),
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
        total = m.total_localidades()
        con_coords = m.localidades_con_coordenadas()
        sin_coords = m.localidades_sin_coordenadas()
        porcentaje = (con_coords / total * 100) if total > 0 else 0

        print(f"\nMunicipio: {m.nombre}")
        print(f" - Cantidad de localidades cargadas: {total}")
        print(f" - Con coordenadas geográficas: {con_coords}")
        print(f" - Sin coordenadas geográficas conocidas: {sin_coords}")
        print(f" - Porcentaje con coordenadas: {porcentaje:.2f}%")

def buscar_localidades_parcial(municipios: list, texto_buscar: str):
    "Busca coincidencias parciales en el nombre de la localidad (Req. 2.b)"
    texto = texto_buscar.strip().lower()
    coincidencias = []

    for m in municipios:
        for loc in m.localidades:
            if loc.nombre and texto in loc.nombre.lower():
                coincidencias.append((loc, m.nombre))
    return coincidencias

