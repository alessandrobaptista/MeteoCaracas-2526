from carga_datos import cargar_datos_json
from reportes import generar_grafico_coordenadas

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
                print (f" Municipio: ")
                print (f" Total Localidades: ")
                print (f" Con coordenadas: ")
                print (f" Sin coordenadas:")

        elif opcion == "2":
            pass

        elif opcion == "3":
            generar_grafico_coordenadas(municipios)

        elif opcion == "4":
            print (" Gracias por usar METEOCARACAS, nos vemos!")
            break

if __name__ == "__main__":
    main()