import math
from ...ConjuntosComponentes.ConjuntoComponentes import ConjuntoComponentes


class IConjuntoAerogerador(ConjuntoComponentes):
    def __init__(self, id):
        self._id = id
        args = self.__criarComponentes__()
        super().__init__(*args)

    def __criarComponentes__(self):
        pass

    def executarInstalacao(self, cronograma, nomeTarefa, dataInicio, embarcacao):
        pass

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

    def getId(self):
        return self._id
