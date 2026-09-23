from ..Componentes.IComponente import Componente


class SecaoCabo(Componente):
    def __init__(self, diametro, densidade, comprimento):
        # (diametro [mm], densidade [kg/m], comprimento [m])

        self._diametro = diametro/1000    # [m]
        self._densidade = densidade/1000  # [t/m]
        self._comprimento = comprimento   # [m]
        self._massa = None                # [t]
        self.__carregar__()

    def __carregar__(self):
        self._massa = self._densidade*self._comprimento

    def getComprimento(self):
        ''''
        Comprimento esta em metros
        '''
        return self._comprimento

    def getLargura(self):
        '''
        Diametro da bitola
        '''
        return self._diametro

    def getDiametro(self):
        '''
        Diametro da bitola
        '''
        return self._diametro

    def getMassa(self):
        ''''
        Massa dada em toneladas
        '''
        return self._massa

    def getDensidade(self):
        ''''
        Densidade em toneladas por metro
        '''
        return self._densidade

    def getTipoComponente(self):
        return "secao de cabo"
