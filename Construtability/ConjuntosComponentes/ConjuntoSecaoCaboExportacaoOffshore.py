from ..ConjuntosComponentes.ConjuntoComponentes import ConjuntoComponentes
from ..Componentes.SecaoCabo import SecaoCabo
from ..Ferramentas.Distancia import calcularDistanciaQuilometrosCoordenadas
from ..Default.Default import tempo_processamento
from ..Cronograma.TipoMicroatividade import TipoMicroatividade


class ConjuntoSecaoCaboExportacaoOffshore(ConjuntoComponentes):
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
        self._tempo_elevar_cabo = tempo_processamento["tempo_elevar_cabo"]
        self._tempo_emendar_cabo = tempo_processamento["tempo_emendar_cabo"]
        self._tempo_descer_cabo_fundo_do_mar = tempo_processamento["tempo_descer_cabo_fundo_do_mar"]
        self._taxa_colocacao_aterramento = tempo_processamento["taxa_colocacao_aterramento"]
        self._emenda = False

    def getPontoInicioInstalacao(self):
        return self._pontoInicio

    def getPontoFimInstalacao(self):
        return self._pontoFim

    def getDistanciaEntrePontosInstalacao(self):
        return calcularDistanciaQuilometrosCoordenadas(self._pontoInicio.getCoordenadas(), self._pontoFim.getCoordenadas())

    def setTempoPosicionar(self, valor):
        self._tempo_posicionar_instalar_cabo = valor

    def getTempoPosicionar(self):
        return self._tempo_posicionar_instalar_cabo

    def setTempoElevarCabo(self, valor):
        self._tempo_elevar_cabo = valor

    def getTempoElevarCabo(self):
        return self._tempo_elevar_cabo

    def setTempoEmendarCabo(self, valor):
        self._tempo_emendar_cabo = valor

    def getTempoEmendarCabo(self):
        return self._tempo_emendar_cabo

    def setTempoDescerCaboFundoDoMar(self, valor):
        self._tempo_descer_cabo_fundo_do_mar = valor

    def getTempoDescerCaboFundoDoMar(self):
        return self._tempo_descer_cabo_fundo_do_mar

    def setTaxaColocarAterrarCabo(self, valor):
        self._taxa_colocacao_aterramento = valor

    def getTaxaColocarAterrarCabo(self):
        return self._taxa_colocacao_aterramento

    def getTempoColocarAterrarCabo(self):
        distancia = self.getDistanciaEntrePontosInstalacao()
        return distancia*self.getTaxaColocarAterrarCabo()

    def setEmenda(self, valor):
        self._emenda = valor

    def getEmenda(self, valor):
        return self._emenda

    def executarInstalacao(self, cronograma, embarcacao, dataInicio):
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação da secao de cabo de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        if self._emenda is True:
            # posicionar no local
            tarefaEmenda0 = "Posicionar no local de instalacao para emenda"
            cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefaEmenda0,
                                               TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                               self._tempo_posicionar_instalar_cabo)
            # levantar o cabo
            tarefaEmenda1 = "Elevar o cabo para realizar emenda"
            cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefaEmenda1,
                                               TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                               self._tempo_elevar_cabo)
            # emendar o cabo
            tarefaEmenda2 = "Realizar emenda do cabo de exportacao"
            cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefaEmenda2,
                                               TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                               self._tempo_emendar_cabo)
            # descer o  cabo
            tarefaEmenda3 = "Descer cabo ate o fundo do mar"
            cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefaEmenda3,
                                               TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                               self._tempo_descer_cabo_fundo_do_mar)
            #
        tarefaGeral = "Colocar e aterrar cabo"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefaGeral,
                                           TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO,
                                           self.getTempoColocarAterrarCabo())
        # executando
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao
    #

    def getId(self):
        return self._id
