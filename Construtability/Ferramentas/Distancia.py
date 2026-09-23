import math
from haversine import haversine  # calcula distancia no globo


def calcularDistanciaQuilometrosCoordenadas(coord1, coord2):
    return haversine(coord1, coord2)


def calcularDistanciaMetrosCoordenadas(coord1, coord2):
    return calcularDistanciaQuilometrosCoordenadas(coord1, coord2)*1000


def calcularMatrizDistanciaListaCoordenadas(listaCoordenadas):
    matriz = {}
    for id1 in listaCoordenadas:
        matriz[id1] = {}
        for id2 in listaCoordenadas:
            if id1 == id2:
                matriz[id1][id2] = 0
            else:
                coordenadas1 = id1
                coordenadas2 = id2
                distancia = math.sqrt(
                    (coordenadas1[0] - coordenadas2[0]) ** 2 + (coordenadas1[1] - coordenadas2[1]) ** 2)
                matriz[id1][id2] = distancia
    return matriz
