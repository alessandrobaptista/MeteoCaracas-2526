from carga_datos import cargar_datos_json, buscar_localidad
from reportes import generar_grafico_coordenadas
from API_clima import obtener_clima_localidad

def main():
    municipios = cargar_datos_json()

    if len(municipios) == 0:
        print("Error al intentar cargar los municipios del archivo")
        return

    while True:
        print (" --- METEOCARACAS --- ")
        print (" 1. Ver resumen de los municipios y coordenadas ")
        print (" 2. Consultar el clima actual ")
        print (" 3. Generar gráfica ")
        print (" 4. Salir ")

        opcion = input (" Elige una opcion (1-4): ")

        if opcion == "1":
            for municipio in municipios:
                print (f" Total Localidades: {municipio.total_localidades()}")
                print (f" Municipio: {municipio.nombre}")
                print (f" Con coordenadas: {municipio.localidades_con_coordenadas()}")
                print (f" Sin coordenadas: {municipio.localidades_con_coordenadas()}")

        elif opcion == "2":
            pass

        elif opcion == "3":
            generar_grafico_coordenadas(municipios)

        elif opcion == "4":
            print (" Gracias por usar METEOCARACAS, nos vemos!")
            break

if __name__ == "__main__":
    main()