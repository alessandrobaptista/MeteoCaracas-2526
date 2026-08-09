import matplotlib.pyplot as plt

def generar_grafico_coordenadas (municipios):
    nombres = []
    con_coords = []
    sin_coords = []

    for municipio in municipios:
        nombres.append()
        con_coords.append()
        sin_coords.append()

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