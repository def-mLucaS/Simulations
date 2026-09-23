def calcularCentroide(coordenadas):
    # Verifica se a lista de coordenadas esta vazia
    if not coordenadas:
        return None

    # Inicializa as variáveis de soma das coordenadas
    soma_lat = 0
    soma_lon = 0

    # Itera sobre as coordenadas e acumula as latitudes e longitudes
    for coordenada in coordenadas:
        lat, lon = coordenada
        soma_lat += lat
        soma_lon += lon

    # Calcula a média das latitudes e longitudes
    media_lat = soma_lat / len(coordenadas)
    media_lon = soma_lon / len(coordenadas)

    # Retorna o centroide como um tuple (latitude, longitude)
    return media_lat, media_lon

