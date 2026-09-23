import math
from ..Ferramentas.Area import areaTrianguloIsosceles, areaTrianguloEquilatero
from ..Componentes.IComponente import Componente
# considera-se como premissa que o componente está deitado na extensao de sua altura
# logo:
# um componente na vertical possuirá uma altura igual a self._altura
# um componente na horizontal possuíra uma altura igual ao maximo entre comprimento e largura


class ComponenteTriangular(Componente):
    def __init__(self, lado1, lado2, lado3, altura, massa):
        self._lado1 = lado1
        self._lado2 = lado2
        self._lado3 = lado3
        self._altura = altura
        self._massa = massa
        self._area_ocupada = self.__estimarAreaOcupada__(lado1, lado2, lado3)
        self._densidade_area = self.__estimarDensidadeArea__(
            massa, lado1, lado2, lado3)

    @staticmethod
    def __estimarAreaOcupada__(lado1, lado2, lado3):
        if ((lado1 == lado2) and (lado2 == lado3)):
            return areaTrianguloEquilatero(lado1)
        elif (lado1 == lado2):
            return areaTrianguloIsosceles(lado1, lado3)
        elif (lado2 == lado3):
            return areaTrianguloIsosceles(lado2, lado1)
        elif (lado1 == lado3):
            return areaTrianguloIsosceles(lado1, lado2)
        else:  # estima como sendo um triangulo equilatero
            lado = max(lado1, lado2, lado3)
            return areaTrianguloEquilatero(lado)

    @staticmethod
    def __estimarDensidadeArea__(massa, lado1, lado2, lado3):
        area = ComponenteTriangular.__estimarAreaOcupada__(lado1, lado2, lado3)
        return massa / area if area > 0 else 0

    def getAreaOcupada(self):
        ''''
        Area esta em metros quadrados
        '''
        return self._area_ocupada

    def getDensidadeArea(self):
        ''''
        Area esta em tonela por metros quadrados
        '''
        return self._densidade_area

    def getAltura(self):
        ''''
        Altura esta em metros
        '''
        return self._altura

    def getComprimento(self):
        ''''
        Comprimento esta em metros
        '''
        return max(self._lado1, self._lado2, self._lado3)

    def getLargura(self):
        '''
        Largura esta em metros
        '''
        return max(self._lado1, self._lado2, self._lado3)

    def getMassa(self):
        ''''
        Massa dada em toneladas
        '''
        return self._massa

    def getTempoFixacaoDeck(self):
        pass

    def getTipoComponente(self):
        pass
