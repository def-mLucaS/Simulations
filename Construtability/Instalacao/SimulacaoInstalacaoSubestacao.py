from ..Instalacao.AbstractSimulacaoInstalacao import AbstractSimulacaoInstalacao
from ..ConjuntosComponentes.ConjuntoSubestacao import ConjuntoSubestacao
from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Entidades.PlantaSubestacao import PlantaSubestacao
from ..Instalacao.StatusInstalacao import StatusInstalacao


class SimulacaoInstalacaoSubestacao(AbstractSimulacaoInstalacao):
    def __init__(self, dataInicio, parque, porto, plantaSubestacao, kitsSubestacao, solucaoEmbarcacao):
        self.__validarSubestacaoPlanta__(kitsSubestacao, plantaSubestacao)
        self._parque = parque
        self._porto = porto
        self._kitsFundacao = kitsSubestacao
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = plantaSubestacao
        pontosInstalacao = self._planta.getPontos()
        for chavePonto, ponto in pontosInstalacao.items():
            status = StatusInstalacao.getStatusFinalizouEtapa(
                EtapaInstalacao.SUBESTACAO_FUNDACAO)
            ponto.setStatusInstalacao(status)

        etapaInstalacao = EtapaInstalacao.SUBESTACAO_CAIXA
        super().__init__(dataInicio, etapaInstalacao, parque, porto,
                         plantaSubestacao, kitsSubestacao, solucaoEmbarcacao)

    def __validarSubestacaoPlanta__(self, kitsSubestacao, plantaSubestacao):
        if not isinstance(kitsSubestacao, dict) or not all(isinstance(item, ConjuntoSubestacao) for item in kitsSubestacao.values()):
            raise KeyError("A classe derivativa deve ser ConjuntoSubestacao.")
        if not isinstance(plantaSubestacao, PlantaSubestacao):
            raise KeyError("A classe derivativa deve ser PlantaSubestacao.")

    def _executarInstalacao(self, cronograma, chaveEmbarcacao, dataInicio, idTurbina):
        conjunto = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].conjuntosTransportados[idTurbina]
        dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual(
        )
        dataFim = conjunto.executarInstalacao(cronograma, self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao],
                                              dataInicio)
        return dataFim
