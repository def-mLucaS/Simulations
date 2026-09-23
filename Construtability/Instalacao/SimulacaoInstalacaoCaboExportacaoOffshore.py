from ..Instalacao.AbstractSimulacaoInstalacao import AbstractSimulacaoInstalacao
from ..ConjuntosComponentes.ConjuntoSecaoCaboExportacaoOffshore import ConjuntoSecaoCaboExportacaoOffshore
from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Entidades.PlantaCabosExportacaoOffshore import PlantaCabosExportacaoOffshore
from ..Instalacao.StatusInstalacao import StatusInstalacao
from ..MovimentacaoComponente.CableVessel import CableVessel
from ..MovimentacaoComponente.SolucaoEmbarcacao import SolucaoEmbarcacao


class SimulacaoInstalacaoCaboExportacaoOffshore(AbstractSimulacaoInstalacao):
    def __init__(self, dataInicio, parque, porto, plantaCabosExportacaoOffshore, kitsSecaoCaboExportacaoOffshore, solucaoEmbarcacao):
        self.__validarDados__(plantaCabosExportacaoOffshore,
                              kitsSecaoCaboExportacaoOffshore, solucaoEmbarcacao)
        self._parque = parque
        self._porto = porto
        self._kitsSecaoCabo = kitsSecaoCaboExportacaoOffshore
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = plantaCabosExportacaoOffshore
        pontosInstalacao = self._planta.getPontos()
        for chavePonto, ponto in pontosInstalacao.items():
            status = StatusInstalacao.getStatusFinalizouEtapa(
                EtapaInstalacao.SISTEMA_ARRAY)
            ponto.setStatusInstalacao(status)

        etapaInstalacao = EtapaInstalacao.CABO_EXPORTACAO_ONSHORE
        super().__init__(dataInicio, etapaInstalacao, parque, porto,
                         plantaCabosExportacaoOffshore, kitsSecaoCaboExportacaoOffshore, solucaoEmbarcacao)

    def __validarDados__(self, plantaCabosExportacaoOffshore, kitsSecaoCaboExportacaoOffshore, solucaoEmbarcacao):
        if not isinstance(kitsSecaoCaboExportacaoOffshore, dict) or not all(isinstance(item, ConjuntoSecaoCaboExportacaoOffshore) for item in kitsSecaoCaboExportacaoOffshore.values()):
            raise KeyError(
                "A classe derivativa deve ser ConjuntoSecaoCaboExportacaoOffshore.")
        if not isinstance(plantaCabosExportacaoOffshore, PlantaCabosExportacaoOffshore):
            raise KeyError(
                "A classe derivativa deve ser PlantaCabosExportacaoOffshore.")
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

    # def executarCarregamentoNoPortoCriterioPontosMaisProximos(self,conjuntos,etapa,cronograma,chaveEmbarcacao,planta):
    #     conjuntosNoPorto = self.getKitsNoPorto(conjuntos, etapa)
    #
    #     numeroKits = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].calculaNumeroConjuntosCarregaveis(conjuntosNoPorto)
    #     if (numeroKits == 0):
    #         capacidadeEmbarcacao = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getMaximaCapacidadeCargaDeck()
    #         # poderia pegar um kit por qualquer criterio
    #         primeiroKit = next(iter(conjuntosNoPorto)).getListaComponentes()
    #         comprimentoMaximoSuportado = math.inf # para todas as secoes do kit
    #         for secaoCabo in primeiroKit.getListaComponentes():
    #             densidade = secaoCabo.getDensidade()  # [t/m]
    #             comprimento = secaoCabo.getComprimento()  # [m]
    #             comprimentoSuportado = min(comprimento,capacidadeEmbarcacao / densidade)
    #             comprimentoMaximoSuportado = min(comprimentoMaximoSuportado,comprimentoSuportado)
    #         # depois de achar o comprimento necessario preciso repartir o kit em dois
    #         latitudeInicio = primeiroKit.getPontoInicioInstalacao().getLatitude()
    #         longitudeInicio = primeiroKit.getPontoInicioInstalacao().getLongitude()
    #         latitudeFim = primeiroKit.getPontoFimInstalacao().getLatitude()
    #         longitudeFim = primeiroKit.getPontoFimInstalacao().getLongitude()
    #         latitudePontoMeio, longitudePontoMeio = calcularPontoMeio(latitudeInicio,longitudeInicio,latitudeFim,longitudeFim)

    #         # raise ValueError("A embarcacao nao suporta o kit de instalacao")
    #     print("Quantidade de kits no porto: ", len(conjuntosNoPorto))
    #     print("Quantidade sendo carregada no navio: ", numeroKits)
    #
    #     # ID turbinas escolhidas que serao instaladas na etapa (criterio de distancia entre elas)
    #     turbinasDeck = self._planta.getPontosProximosNaoIniciadosNaEtapa(etapa,numeroKits)
    #     print("Turbinas escolhidas para serem carregadas na embarcacao : ")
    #     print(turbinasDeck)
    #
    #     # Extrai os conjuntos que serao transportados a partir da lista de turbinas escolhidas
    #     conjuntosTransportados = self.extraiKits(turbinasDeck,conjuntos)
    #     print("ID dos kits transportados: ")
    #     print(conjuntosTransportados.keys())
    #
    #     # Para cada turbina que está no deck inicia a etapa
    #     for idTurbina in turbinasDeck:
    #         planta.setIniciouEtapa(etapa,idTurbina)
    #         print("No ponto de instalacao ", idTurbina, "iniciou-se a etapa de ", etapa.name)
    #
    #     # Carregar embarcacao
    #     if (self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual() is None):
    #         self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].setDataAtual(self.dataInicioInstalacao)
    #     print("Data atual: ", self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual())
    #     print("Inicia o processo de carregamento da embarcacao alimentadora")
    #     self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].carregarConjuntoComponentes(cronograma,conjuntosTransportados,turbinasDeck)
    #
    # def getKitsNoPorto(self,conjuntos,etapa):
    #     listaTurbinasPorto =self._planta.getPontosNaoIniciadosNaEtapa(etapa)
    #     kits = self.extraiKits(listaTurbinasPorto,conjuntos)
    #     return kits
    #
    # def extraiKits(self,listaTurbinas,conjuntos):
    #     kits = {chave: valor for chave, valor in conjuntos.items() if chave in listaTurbinas}
    #     return kits
