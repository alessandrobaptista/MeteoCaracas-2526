import matplotlib.pyplot as plt

def generar_grafico_coordenadas (municipios):
    nombres = [municipio.nombre for municipio in municipios]
    con_coords = [municipio.localidades_con_coordenadas() for municipio in municipios]
    sin_coords = [municipio.localidades_sin_coordenadas() for municipio in municipios]

    plt.bar (nombres, con_coords, label ="Con coordenadas", color ="g")
    plt.bar (
        nombres,
        sin_coords,
        bottom = con_coords,
        label = "Sin coordenadas",
        color = "r",
    )

    plt.title ("Coordenadas por Municipio ")
    plt.xlabel ("Municipios")
    plt.ylabel ("Cantidad")
    plt.legend ()
    plt.show ()