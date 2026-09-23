from ..Instalacao.AbstractSimulacaoInstalacao import AbstractSimulacaoInstalacao
from ..ConjuntosComponentes.ConjuntoSecaoCabo import ConjuntoSecaoCabo
from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Entidades.PlantaRoteamentoCabos import PlantaRoteamentoCabos
from ..Instalacao.StatusInstalacao import StatusInstalacao
from ..MovimentacaoComponente.CableVessel import CableVessel
from ..MovimentacaoComponente.SolucaoEmbarcacao import SolucaoEmbarcacao


class SimulacaoInstalacaoSistemaArray(AbstractSimulacaoInstalacao):
    def __init__(self, dataInicio, parque, porto, plantaRoteamentoCabos, kitsSecaoCabo, solucaoEmbarcacao):
        self.__validarDados__(plantaRoteamentoCabos,
                              kitsSecaoCabo, solucaoEmbarcacao)
        self._parque = parque
        self._porto = porto
        self._kitsSecaoCabo = kitsSecaoCabo
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = plantaRoteamentoCabos
        pontosInstalacao = self._planta.getPontos()
        for chavePonto, ponto in pontosInstalacao.items():
            status = StatusInstalacao.getStatusFinalizouEtapa(
                EtapaInstalacao.SUBESTACAO_CAIXA)
            ponto.setStatusInstalacao(status)

        etapaInstalacao = EtapaInstalacao.SISTEMA_ARRAY
        super().__init__(dataInicio, etapaInstalacao, parque, porto,
                         plantaRoteamentoCabos, kitsSecaoCabo, solucaoEmbarcacao)

    def __validarDados__(self, plantaRoteamentoCabos, kitsSecaoCabo, solucaoEmbarcacao):
        if not isinstance(kitsSecaoCabo, dict) or not all(isinstance(item, ConjuntoSecaoCabo) for item in kitsSecaoCabo.values()):
            raise KeyError("A classe derivativa deve ser ConjuntoSecaoCabo.")
        if not isinstance(plantaRoteamentoCabos, PlantaRoteamentoCabos):
            raise KeyError(
                "A classe derivativa deve ser PlantaRoteamentoCabos.")
        if not isinstance(solucaoEmbarcacao, SolucaoEmbarcacao):
            raise KeyError("A classe derivativa deve ser SolucaoEmbarcacao.")
        for chave, embarcacao in solucaoEmbarcacao.getDicionarioEmbarcacoes().items():
            if not isinstance(embarcacao, CableVessel):
                raise KeyError(
                    "A classe derivativa de todas as embarcações deve ser CableVessel.")

    def _executarInstalacao(self, cronograma, chaveEmbarcacao, dataInicio, idTurbina):
        conjunto = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].conjuntosTransportados[idTurbina]
        dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual(
        )
        dataFim = conjunto.executarInstalacao(cronograma, self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao],
                                              dataInicio)
        return dataFim
