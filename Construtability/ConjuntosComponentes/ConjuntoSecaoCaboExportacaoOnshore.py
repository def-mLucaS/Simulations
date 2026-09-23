from ..ConjuntosComponentes.ConjuntoComponentes import ConjuntoComponentes
from ..Componentes.SecaoCabo import SecaoCabo
from ..Ferramentas.Distancia import calcularDistanciaMetrosCoordenadas
from ..Default.Default import tempo_processamento
from ..Cronograma.TipoMicroatividade import TipoMicroatividade


class ConjuntoSecaoCaboExportacaoOnshore(ConjuntoComponentes):
    def __init__(self, id, pontoInicio, pontoFim, *args):
        self._id = id
        self._pontoInicio = pontoInicio  # tipo PontoInstalacao
        self._pontoFim = pontoFim
        listaSecaoCabos = list()
        for arg in args:
            if isinstance(arg, SecaoCabo):
                listaSecaoCabos.append(arg)
            else:
                raise KeyError("A classe derivativa deve ser SecaoCabo.")
        self._listaComponentes = listaSecaoCabos
        # informacoes instalacao
        self._tempo_posicionar_instalar_cabo = tempo_processamento["tempo_posicionar_instalar_cabo"]
        # km/h
        self._taxa_preparar_solo_arado = tempo_processamento["taxa_preparar_solo_arado"]
        # km/h
        self._taxa_puxar_cabo_guincho = tempo_processamento["taxa_puxar_cabo_guincho"]
        # km/h
        self._taxa_guiar_cabo_exportacao = tempo_processamento["taxa_guiar_cabo_exportacao"]
        self._tempo_testar_terminar_cabo = tempo_processamento["tempo_testar_terminar_cabo"]

    def getPontoInicioInstalacao(self):
        return self._pontoInicio

    def getPontoFimInstalacao(self):
        return self._pontoFim

    def getDistanciaEntrePontosInstalacao(self):
        return calcularDistanciaMetrosCoordenadas(self._pontoInicio.getCoordenadas(), self._pontoFim.getCoordenadas())

    def setTempoPosicionar(self, valor):
        self._tempo_posicionar_instalar_cabo = valor

    def getTempoPosicionar(self):
        return self._tempo_posicionar_instalar_cabo

    def setTempoTestarTerminarCabo(self, valor):
        self._tempo_testar_terminar_cabo = valor

    def getTempoTestarTerminarCabo(self):
        return self._tempo_testar_terminar_cabo

    def setTaxaPrepararSoloComArado(self, valor):
        # taxa em km/h
        self._taxa_preparar_solo_arado = valor

    def getTaxaPrepararSoloComArado(self):
        # taxa em km/h
        return self._taxa_preparar_solo_arado

    def getTempoPrepararSoloComArado(self):
        distanciaKm = self.getDistanciaEntrePontosInstalacao()/1000
        return distanciaKm/self.getTaxaPrepararSoloComArado()

    def setTaxaPuxarCaboComGuincho(self, valor):
        # taxa em km/h
        self._taxa_puxar_cabo_guincho = valor

    def getTaxaPuxarCaboComGuincho(self):
        # taxa em km/h
        return self._taxa_puxar_cabo_guincho

    def getTempoPuxarCaboComGuincho(self):
        distanciaKm = self.getDistanciaEntrePontosInstalacao()/1000
        return distanciaKm/self._taxa_puxar_cabo_guincho

    def setTaxaGuiarCabo(self, valor):
        # taxa em km/h
        self._taxa_guiar_cabo_exportacao = valor

    def getTaxaGuiarCabo(self):
        # taxa em km/h
        return self._taxa_guiar_cabo_exportacao

    def getTempoGuiarCabo(self):
        distanciaKm = self.getDistanciaEntrePontosInstalacao()/1000
        return distanciaKm/self._taxa_guiar_cabo_exportacao

    def executarInstalacao(self, cronograma, embarcacao, dataInicio):
        numeroCabos = len(self.getListaComponentes())
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação da secao de cabo de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        tarefa0 = "Posicionar no local de chegada do cabo na costa"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa0,
                                           TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                           self._tempo_posicionar_instalar_cabo)

        tarefa1 = "Preparar solo com arado"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                           self. getTempoPrepararSoloComArado())

        tarefa2 = "Puxar cabos com guincho"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                           self. getTempoPuxarCaboComGuincho()*numeroCabos)

        tarefa3 = "Guiar cabos de exportação"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa3,
                                           TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                           self. getTempoGuiarCabo()*numeroCabos)

        tarefa4 = "Testar e terminar cabos no ponto onshore"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa4,
                                           TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                           self. getTempoTestarTerminarCabo()*numeroCabos)

        # executando
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao
    #

    def getId(self):
        return self._id
