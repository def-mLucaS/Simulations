from ..Instalacao.AbstractSimulacaoInstalacao import AbstractSimulacaoInstalacao
from ..ConjuntosComponentes.ConjuntoSecaoCaboExportacaoOnshore import ConjuntoSecaoCaboExportacaoOnshore
from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Entidades.PlantaCabosExportacaoOnshore import PlantaCabosExportacaoOnshore
from ..Instalacao.StatusInstalacao import StatusInstalacao
from ..MovimentacaoComponente.CableVessel import CableVessel
from ..MovimentacaoComponente.SolucaoEmbarcacao import SolucaoEmbarcacao


class SimulacaoInstalacaoCaboExportacaoOnshore(AbstractSimulacaoInstalacao):
    def __init__(self, dataInicio, parque, porto, plantaCabosExportacaoOnshore, kitsSecaoCaboExportacaoOnshore, solucaoEmbarcacao):
        self.__validarDados__(plantaCabosExportacaoOnshore,
                              kitsSecaoCaboExportacaoOnshore, solucaoEmbarcacao)
        self._parque = parque
        self._porto = porto
        self._kitsSecaoCabo = kitsSecaoCaboExportacaoOnshore
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = plantaCabosExportacaoOnshore
        pontosInstalacao = self._planta.getPontos()
        for chavePonto, ponto in pontosInstalacao.items():
            status = StatusInstalacao.getStatusFinalizouEtapa(
                EtapaInstalacao.SISTEMA_ARRAY)
            ponto.setStatusInstalacao(status)

        etapaInstalacao = EtapaInstalacao.CABO_EXPORTACAO_ONSHORE
        super().__init__(dataInicio, etapaInstalacao, parque, porto,
                         plantaCabosExportacaoOnshore, kitsSecaoCaboExportacaoOnshore, solucaoEmbarcacao)

    def __validarDados__(self, plantaCabosExportacaoOnshore, kitsSecaoCaboExportacaoOnshore, solucaoEmbarcacao):
        if not isinstance(kitsSecaoCaboExportacaoOnshore, dict) or not all(isinstance(item, ConjuntoSecaoCaboExportacaoOnshore) for item in kitsSecaoCaboExportacaoOnshore.values()):
            raise KeyError(
                "A classe derivativa deve ser ConjuntoSecaoCaboExportacaoOnshore.")
        if not isinstance(plantaCabosExportacaoOnshore, PlantaCabosExportacaoOnshore):
            raise KeyError(
                "A classe derivativa deve ser PlantaCabosExportacaoOnshore.")
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
