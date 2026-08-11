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

def generar_grafico_historico (anios, temperaturas):

    plt.figure(figsize=(10,5))
    plt.plot (anios, temperaturas, marker = "o", color="g")
    plt.title ("Evolución de la temperatura durante los años")
    plt.xlabel ("Años")
    plt.ylabel ("Temperatura promedio")
    plt.grid (True)
    plt.xticks (rotation=45)
    plt.show()