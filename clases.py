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

