class Localidad:
    "Representa una localidad dentro de un municipio"

    def __init__(
            self, nombre: str, latitud: float = None, longitud: float = None
    ):
        "Inicializa los atributos básicos de la localidad"
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenadas(self):
        "Verifica si la localidad posee coordenadas válidas"
        return self.latitud is not None and self.longitud is not None

class Municipio:
    "Representa un municipio con sus localidades"

    def __init__(self, nombre: str):
        "Inicializa el municipio con su nomre y lista vacía de localidades"
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, localidad: Localidad):
        "Agrega un objeto Localidad a la lista del municipio"
        self.localidades.append(localidad)

    def total_localidades(self):
        "Retorna el número total de localidades en el municipio"
        return len(self.localidades)

    def localidades_con_coordenadas(self):
        "Cuenta cuántas localidades tienen coordenadas válidas"
        con = 0 
        for loc in self.localidades:
            if loc.tiene_coordenadas():
                con += 1
        return con

    def localidades_sin_coordenadas(self):
        "Cuenta cuántas localidades no tienen coordenadas válidas"
        return self.total_localidades() - self.localidades_con_coordenadas()

    def __str__(self):
        "Representación en cadena del municipio y su número de localidades válidas"
        return f"Municipio: {self.nombre} ({self.total_localidades()} localidades)"
        
class RegistroClima:
    "Guarda los datos del clima actual de una localidad"

    def __init__(self, temperatura, humedad, viento, lluvia, estado_tiempo = "Desconocido"):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.lluvia = lluvia
        self.estado_tiempo = estado_tiempo

    def __str__(self):
        "Representación en cadena de los datos del clima"
        return f"Temp: {self.temperatura}°C | Humedad: {self.humedad}% | Viento: {self.viento} km/h | Lluvia: {self.lluvia} mm | Estado: {self.estado_tiempo}"

class RegistroHistoricoMensual:
    "Guarda los datos históricos mensuales del clima de una localidad"
    def __init__(self, anio, mes, temperatura, humedad, precipitacion, viento):
        self.anio = anio
        self.mes = mes
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento

    def __str__(self):
        "Representación en cadena de los datos históricos mensuales del clima"
        return f"{self.anio}-{self.mes:02d} -> Temp: {self.temperatura:.1f}°C | Humedad: {self.humedad:.1f}% | Precip: {self.recipitacion:.1f}mm | Viento: {self.viento:.1f}km/h"

    