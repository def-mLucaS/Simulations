from ..Instalacao.AbstractSimulacaoInstalacao import AbstractSimulacaoInstalacao
from ..ConjuntosComponentes.Interfaces.IConjuntoAerogerador import IConjuntoAerogerador
from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Instalacao.StatusInstalacao import StatusInstalacao
from ..MovimentacaoComponente.Wtiv import Wtiv
from ..MovimentacaoComponente.Barcaca import Barcaca


class SimulacaoInstalacaoAerogerador(AbstractSimulacaoInstalacao):
    def __init__(self, dataInicio, parque, porto, kitsAerogerador, solucaoEmbarcacao):
        self.__validarFundacao__(kitsAerogerador, solucaoEmbarcacao)
        self._parque = parque
        turbinas = parque.getPlanta().getPontos()
        for chaveTurbina, turbina in turbinas.items():
            status = StatusInstalacao.getStatusFinalizouEtapa(
                EtapaInstalacao.CABO_EXPORTACAO_OFFSHORE)
            turbina.setStatusInstalacao(status)
        self._porto = porto
        self._kitsAerogerador = kitsAerogerador
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = parque.getPlanta()
        etapaInstalacao = EtapaInstalacao.AEROGERADOR
        super().__init__(dataInicio, etapaInstalacao, parque, porto,
                         parque.getPlanta(), kitsAerogerador, solucaoEmbarcacao)

    def __validarFundacao__(self, kitsAerogerador, solucaoEmbarcacao):
        if not isinstance(kitsAerogerador, dict) or not all(isinstance(item, IConjuntoAerogerador) for item in kitsAerogerador.values()):
            raise KeyError(
                "A classe derivativa deve ser IConjuntoAerogerador.")
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
        conjunto = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].conjuntosTransportados[idTurbina]
        dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual(
        )
        dataFim = conjunto.executarInstalacao(
            cronograma, dataInicio, self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao])
        return dataFim
