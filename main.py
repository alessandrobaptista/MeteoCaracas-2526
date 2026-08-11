from carga_datos import cargar_datos_json, buscar_localidades_parcial, generar_resumen_coordenadas
from reportes import generar_grafico_coordenadas, generar_grafico_historico
from API_clima import obtener_clima_localidad, obtener_historial_localidad
from clases import SesionConsultas

def main():
    municipios = cargar_datos_json()
    sesion = SesionConsultas ()

    if len(municipios) == 0:
        print("Error al intentar cargar los municipios del archivo")
        return

    while True:
        print (" --- METEOCARACAS --- ")
        print (" 1. Ver resumen de los municipios y coordenadas ")
        print (" 2. Consultar el clima actual ")
        print (" 3. Estadísticas y gráfica de cobertura ")
        print (" 4. Consulta de datos históricos ")
        print (" 5. Salir ")

        opcion = input (" Elige una opcion (1-5): ")

        if opcion == "1":
            generar_resumen_coordenadas(municipios)

        elif opcion == "2":
            print (" -- Consulta del clima en tiempo real -- ")
            print (" a. Seleccionar municipio y Localidad")
            print (" b. Busqueda mediante nombre de la localidad")
            op = input (" Seleccione como desea realizar la busqueda (a o b): ")

            localidad_seleccionada = None
            nombre_municipio = None

            if op == "a":
                for i, municipio in enumerate(municipios):
                    print (f"{i+1}.{municipio.nombre}")

                try:
                    idx_municipio = int(input("Seleccione el municipio:")) - 1
                    municipio = municipios[idx_municipio]
                    nombre_municipio = municipio.nombre

                    loc =[localidad for localidad in municipio.localidades if localidad.tiene_coordenadas()]
                    if not loc:
                        print ("Este municipio no posee localidades validas")
                        continue

                    for i, localidad in enumerate (loc):
                        print (f"{i+1}.{localidad.nombre}")

                    idx_localiad = int(input("Seleccione la localidad:")) - 1
                    loc_seleccionada = loc[idx_localiad]
                except (ValueError, IndexError):

                    print ("Seleccion no valida")
                    continue

            elif op == "b":
                localidad = input ("Ingrese el nombre de la localidad:").strip()
                coincidencias = buscar_localidades_parcial (municipios, localidad)

                if not coincidencias:
                    print ("No se encontraron coincidencias durante la busqueda")
                    continue

                for i, (loc, municipio_nombre) in enumerate (coincidencias):
                    print (f"{i+1}.{loc.nombre} ({municipio_nombre})")

                try:
                    idx = int(input("Seleecione el numero: ")) - 1
                    loc_seleccionada, nombre_municipio = coincidencias[idx]
                except (ValueError, IndexError):
                    print ("Seleccion no valida")
                    continue
            else:
                print ("Opción no valida")
                continue

            clima = obtener_clima_localidad(loc_seleccionada.latitud,loc_seleccionada.longitud )

            if clima:
                print (f" CLIMA ACTUAL: {nombre_municipio} - {loc_seleccionada.nombre}")
                print (clima)
                sesion.agregar_consulta(nombre_municipio, loc_seleccionada.nombre, clima)

            else:
                print ("No se lograron obtener los datos de la API")


        elif opcion == "3":
            print (" -- ESTADISTICAS -- ")

            if not sesion.consultas:
                print ("Aun no se ha realizado consultas")

            else:
                consultas_ordenadas = sorted (sesion.consultas, key= lambda x: x[2].temperatura)
                fria = consultas_ordenadas[0]
                calida = consultas_ordenadas[-1]
                promedio = sum(c[2].temperatura for c in sesion.consultas) / len(sesion.consultas)

                print (f"Localidad mas fría consultada: {fria[0]} - {fria[1]} ({fria[2].temperatura}°C)")
                print (f"Localidad mas calida consultada: {calida[0]} - {calida[1]} ({calida[2].temperatura}°C)")
                print (f"Temperatura promedio general: {promedio:.2f}°C")

            print (" - ZONAS SIN COORDENADAS - ")
            for municipio in municipios:
                sin_coords = [localidad.nombre for localidad in municipio.localidades if not localidad.tiene_coordenadas()]
                if sin_coords:
                    print (f"[{municipio.nombre}]: {','.join(sin_coords)}")

            generar_grafico_coordenadas(municipios)

        elif opcion == "4":
            nombre = input (" Ingrese el nombre de la localidad para ver su historial")
            coincidencias = buscar_localidades_parcial (municipios, nombre)

            if not coincidencias:
                print ("No se encontraron localidades")
                continue

            for i, (loc, municipio_nombre) in enumerate (coincidencias):
                print (f"{i+1}.{loc.nombre} ({municipio_nombre})")
            
                try:
                    idx = int(input("Seleecione el numero:")) - 1
                    loc_seleccionada, nombre_municipio = coincidencias[idx]

                except (ValueError, IndexError):
                    print ("Seleccion no valida")
                    continue

            if not loc_seleccionada.tiene_coordenadas():
                print ("La localidad no tiene coordenadas conocidad")
                continue

            fecha_inicio = input ("Fecha inicio (AAAA-MM-DD): ").strip()
            fecha_final = input ("Fecha final (AAAA-MM-DD): ").strip()

            datos_historicos = obtener_historial_localidad (loc_seleccionada.latitud, loc_seleccionada.longitud, fecha_inicio, fecha_final)

            if datos_historicos:
                print (f"Historico: {loc_seleccionada.nombre}")
                anios_datos = {}

                for datos in datos_historicos:
                    print (datos)

                    if datos.anio not in anios_datos:
                        anios_datos[datos.anio]= {"temp": [], "hum": [], "prec": []}
                        
                    anios_datos[datos.anio]["temp"].append(datos.temperatura)
                    anios_datos[datos.anio]["hum"].append(datos.humedad)
                    anios_datos[datos.anio]["prec"].append(datos.precipitacion)
                        
                prom_anuales = []
                for anio, valores in anios_datos.items():

                    prom_temp = sum(valores["temp"]) / len(valores["temp"])
                    prom_hum = sum(valores["hum"]) / len(valores["hum"])
                    prom_prec = sum(valores["prec"]) / len(valores["prec"])
                    prom_anuales.append((anio, prom_temp, prom_hum, prom_prec))

                mas_caluroso = max(prom_anuales, key= lambda x: x[1])[0]
                mas_fresco = min(prom_anuales, key= lambda x: x[1])[0]
                mayor_humedad = max(prom_anuales, key= lambda x: x[2])[0]
                mayor_precipitacion = max(prom_anuales, key= lambda x: x[3])[0]

                print (" -- Extremos Historicos (Anuales) -- ")
                print (f" Año mas caluroso: {mas_caluroso}")
                print (f" Año mas fresco: {mas_fresco}")
                print (f" Año con mayor humedad : {mayor_humedad}")
                print (f" Año con mayor precipitacion: {mayor_precipitacion}")

                lista_anios = [str(item[0]) for item in prom_anuales]
                lista_temps = [item[1] for item in prom_anuales]

                generar_grafico_historico(lista_anios, lista_temps)
                

        elif opcion == "5":
            print (" Gracias por usar METEOCARACAS, nos vemos!")
            break
        else:
            print (" Opcion invalida, ingrese el numero nuevamente (1-5)")

if __name__ == "__main__":
    main()