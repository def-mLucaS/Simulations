import math


class ConjuntoComponentes:
    def __init__(self, *args):
        self._listaComponentes = args

    def getMassaTotal(self):
        massa_total = 0
        for componente in self._listaComponentes:
            massa_total += componente.getMassa()
        return massa_total

    def getListaComponentes(self):
        return self._listaComponentes

    def setListaComponentes(self, componentes):
        self._listaComponentes = componentes

    def getDensidadeArea(self):
        densidade_area = -math.inf
        for componente in self.getListaComponentes():
            densidade_area = max(densidade_area, componente.getDensidadeArea())
        return densidade_area

    def getAreaTotal(self):
        area_total = 0
        for componente in self.getListaComponentes():
            area_total += componente.getAreaOcupada()
        return area_total
