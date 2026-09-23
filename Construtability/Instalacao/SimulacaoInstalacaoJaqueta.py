from ..ConjuntosComponentes.ConjuntoFundacao import ConjuntoFundacao
from ..Instalacao.SimulacaoInstalacaoFundacao import SimulacaoInstalacaoFundacao
from ..MovimentacaoComponente.Wtiv import Wtiv
from ..MovimentacaoComponente.Barcaca import Barcaca


class SimulacaoInstalacaoJaqueta(SimulacaoInstalacaoFundacao):
    def __init__(self, parque, porto, kitsJaqueta, solucaoEmbarcacao):
        self.__validarDadosInstalacaoJaqueta__(solucaoEmbarcacao)
        super().__init__(parque, porto, kitsJaqueta, solucaoEmbarcacao)

    def __validarDadosInstalacaoJaqueta__(self, solucaoEmbarcacao):
        listaAlimentadoras = solucaoEmbarcacao.getListaAlimentadoras()
        listaInstaladoras = solucaoEmbarcacao.getListaInstaladoras()
        for chave in listaAlimentadoras:
            alimentadora = solucaoEmbarcacao.getAlimentadora(chave)
            if not (isinstance(alimentadora, Wtiv) or isinstance(alimentadora, Barcaca)):
                raise KeyError(
                    "A embarcação instaladora deve ser do tipo BARCACA OU WTIV.")
        for chave in listaInstaladoras:
            instaladora = solucaoEmbarcacao.getInstaladora(chave)
            if not isinstance(instaladora, Wtiv):
                raise KeyError(
                    "A embarcação instaladora deve ser do tipo WTIV.")

    def _executarInstalacao(self, cronograma, chaveEmbarcacao, dataInicio, idTurbina):
        profundidade = self._planta.getProfundidade(idTurbina)
        conjunto = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].conjuntosTransportados[idTurbina]
        dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual(
        )
        dataFim = conjunto.executarInstalacao(cronograma, self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao],
                                              dataInicio, profundidade)
        return dataFim
