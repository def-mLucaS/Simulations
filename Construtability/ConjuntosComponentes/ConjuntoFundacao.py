import math
from ..ConjuntosComponentes.ConjuntoComponentes import ConjuntoComponentes

class ConjuntoFundacao(ConjuntoComponentes):
    def __init__(self, *args):
        super().__init__(*args)

    def executarInstalacao(self,cronograma,nomeTarefa,dataInicio,embarcacao,profundidade):
       pass

    def getDensidadeArea(self):
        densidade_area = -math.inf
        for componente in self.getListaComponentes():
            densidade_area = max(densidade_area,componente.getDensidadeArea())
        return densidade_area

    def getAreaTotal(self):
        area_total = 0
        for componente in self.getListaComponentes():
            area_total += componente.getAreaOcupada()
        return area_total