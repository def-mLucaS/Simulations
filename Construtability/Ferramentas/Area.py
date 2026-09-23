import math

def areaCirculo(raio):
    return math.pi * raio ** 2

def areaTriangulo(base,altura):
    return base*altura/2

def areaTrianguloEquilatero(lado):
    return (lado**2)*math.sqrt(3)/4

def areaTrianguloIsosceles(ladoComum,ladoDiferente):
    altura = math.sqrt((ladoComum**2)-(ladoDiferente/2)**2)
    return areaTriangulo(ladoDiferente,altura)

def areaRetangulo(lado1,lado2):
    return lado1*lado2