from ..MovimentacaoComponente.Embarcacao import Embarcacao
from ..MovimentacaoComponente.Wtiv import Wtiv
from ..MovimentacaoComponente.Barcaca import Barcaca
from ..MovimentacaoComponente.ConjuntoRebocadores import ConjuntoRebocadores
from ..MovimentacaoComponente.ConjuntoRebocadoresBarcaca import ConjuntoRebocadoresBarcaca
from ..MovimentacaoComponente.HeavyLift import HeavyLift
from ..MovimentacaoComponente.JackUp import JackUp
from ..MovimentacaoComponente.CableVessel import CableVessel


class SolucaoEmbarcacao:
    def __init__(self, *args):
        self.embarcacoes = dict()
        self._listaAlimentadoras = []
        self._listaInstaladoras = []
        self._temBarcaca = False
        self._temAlimentador = False
        self.leitura(*args)

    def leitura(self, *args):
        listaEmbarcacoes = args
        for embarcacao in listaEmbarcacoes:
            self.embarcacoes[embarcacao.getNome()] = embarcacao
        for chave, valor in self.embarcacoes.items():
            if isinstance(valor, Embarcacao):
                if isinstance(valor, Wtiv) or isinstance(valor, HeavyLift) or isinstance(valor, JackUp) or isinstance(valor, CableVessel):
                    self._listaInstaladoras.append(chave)
                elif (isinstance(valor, Barcaca) or isinstance(valor, ConjuntoRebocadores) or isinstance(valor, ConjuntoRebocadoresBarcaca)):
                    self._listaAlimentadoras.append(chave)
                    self._temAlimentador = True
                    if isinstance(valor, Barcaca) or isinstance(valor, ConjuntoRebocadoresBarcaca):
                        self._temBarcaca = True
            else:
                raise KeyError("A classe derivativa deve ser EMBARCACAO.")
        if len(self._listaAlimentadoras) == 0:
            # Caso não existam alimentadores, os próprios instaladores são alimentadores
            self._listaAlimentadoras = self._listaInstaladoras

    def limparEmbarcacoes(self, dataInicio):
        for chave, valor in self.embarcacoes.items():
            valor.limparEmbarcacao(dataInicio)

    def temAlimentador(self):
        return self._temAlimentador

    def temBarcaca(self):
        return self._temBarcaca

    def getListaAlimentadoras(self):
        return self._listaAlimentadoras

    def getAlimentadora(self, chave):
        return self.embarcacoes[chave]

    def getListaInstaladoras(self):
        return self._listaInstaladoras

    def getInstaladora(self, chave):
        return self.embarcacoes[chave]

    def getDicionarioEmbarcacoes(self):
        return self.embarcacoes
