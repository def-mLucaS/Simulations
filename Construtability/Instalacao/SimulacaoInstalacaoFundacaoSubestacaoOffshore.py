from ..Instalacao.AbstractSimulacaoInstalacao import AbstractSimulacaoInstalacao
from ..ConjuntosComponentes.ConjuntoFundacao import ConjuntoFundacao
from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Entidades.PlantaSubestacao import PlantaSubestacao
from ..Instalacao.StatusInstalacao import StatusInstalacao


class SimulacaoInstalacaoFundacaoSubestacaoOffshore(AbstractSimulacaoInstalacao):
    def __init__(self, dataInicio, parque, porto, plantaSubestacao, kitsFundacao, solucaoEmbarcacao):
        self.__validarFundacaoPlanta__(kitsFundacao, plantaSubestacao)
        self._parque = parque
        self._porto = porto
        self._kitsFundacao = kitsFundacao
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = plantaSubestacao
        pontosInstalacao = self._planta.getPontos()
        for chavePonto, ponto in pontosInstalacao.items():
            status = StatusInstalacao.getStatusFinalizouEtapa(
                EtapaInstalacao.FUNDACAO)
            ponto.setStatusInstalacao(status)

        etapaInstalacao = EtapaInstalacao.SUBESTACAO_FUNDACAO
        super().__init__(dataInicio, etapaInstalacao, parque, porto,
                         plantaSubestacao, kitsFundacao, solucaoEmbarcacao)

    def __validarFundacaoPlanta__(self, kitsFundacao, plantaSubestacao):
        if not isinstance(kitsFundacao, dict) or not all(isinstance(item, ConjuntoFundacao) for item in kitsFundacao.values()):
            raise KeyError("A classe derivativa deve ser ConjuntoFundacao.")
        if not isinstance(plantaSubestacao, PlantaSubestacao):
            raise KeyError("A classe derivativa deve ser PlantaSubestacao.")

    def _executarInstalacao(self, cronograma, chaveEmbarcacao, dataInicio, idTurbina):
        profundidade = self._planta.getProfundidade(idTurbina)
        conjunto = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].conjuntosTransportados[idTurbina]
        dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual(
        )
        dataFim = conjunto.executarInstalacao(cronograma, self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao],
                                              dataInicio, profundidade)
        return dataFim
