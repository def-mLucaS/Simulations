from ..Ferramentas.Distancia import calcularDistanciaQuilometrosCoordenadas


def calcularPontoMeio(latitudeA, longitudeA, latitudeB, longitudeB, comprimentoRequerido):
    # Calcular a distância entre A e B
    distancia_AB = calcularDistanciaQuilometrosCoordenadas(
        latitudeA, longitudeA, latitudeB, longitudeB)

    # Calcular o vetor direcional entre A e B
    diferenca_lat = latitudeB - latitudeA
    diferenca_lon = longitudeB - longitudeA

    # Normalizar o vetor direcional
    fator_normalizacao = comprimentoRequerido / distancia_AB
    direcao_lat = diferenca_lat * fator_normalizacao
    direcao_lon = diferenca_lon * fator_normalizacao

    # Calcular as coordenadas do ponto C
    lat_C = latitudeA + direcao_lat
    lon_C = longitudeA + direcao_lon

    return lat_C, lon_C
