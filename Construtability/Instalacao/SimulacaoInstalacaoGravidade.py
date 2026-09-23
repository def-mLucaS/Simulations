from ..Instalacao.SimulacaoInstalacaoFundacao import SimulacaoInstalacaoFundacao
from ..MovimentacaoComponente.HeavyLift import HeavyLift
from ..MovimentacaoComponente.JackUp import JackUp
from ..MovimentacaoComponente.ConjuntoRebocadores import ConjuntoRebocadores
from ..MovimentacaoComponente.ConjuntoRebocadoresBarcaca import ConjuntoRebocadoresBarcaca
from ..MovimentacaoComponente.Barcaca import Barcaca


class SimulacaoInstalacaoGravidade(SimulacaoInstalacaoFundacao):
    def __init__(self, parque, porto, kitsGravidade, solucaoEmbarcacao):
        self.__validarDadosInstalacaoGravidade__(solucaoEmbarcacao)
        super().__init__(parque, porto, kitsGravidade, solucaoEmbarcacao)

    def __validarDadosInstalacaoGravidade__(self, solucaoEmbarcacao):
        listaAlimentadoras = solucaoEmbarcacao.getListaAlimentadoras()
        listaInstaladoras = solucaoEmbarcacao.getListaInstaladoras()
        for chave in listaAlimentadoras:
            alimentadora = solucaoEmbarcacao.getAlimentadora(chave)
            if not (isinstance(alimentadora, HeavyLift) or isinstance(alimentadora, JackUp) or isinstance(alimentadora, Barcaca) or isinstance(alimentadora, ConjuntoRebocadores) or isinstance(alimentadora, ConjuntoRebocadoresBarcaca)):
                raise KeyError(
                    "A embarcação instaladora deve ser do tipo HeavyLift ou JackUp ou barcaça ou conjunto de rebocadores ou conjunto de rebocadores com barcaça.")
        for chave in listaInstaladoras:
            instaladora = solucaoEmbarcacao.getInstaladora(chave)
            if not (isinstance(instaladora, HeavyLift) or isinstance(instaladora, JackUp)):
                raise KeyError(
                    "A embarcação instaladora deve ser do tipo HeavyLift ou JackUp.")

    def _executarInstalacao(self, cronograma, chaveEmbarcacao, dataInicio, idTurbina):
        profundidade = self._planta.getProfundidade(idTurbina)
        conjunto = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].conjuntosTransportados[idTurbina]
        dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual(
        )
        dataFim = conjunto.executarInstalacao(cronograma, self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao],
                                              dataInicio, profundidade)
        return dataFim
