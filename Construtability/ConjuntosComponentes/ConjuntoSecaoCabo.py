from ..ConjuntosComponentes.ConjuntoComponentes import ConjuntoComponentes
from ..Componentes.SecaoCabo import SecaoCabo
from ..Ferramentas.Distancia import calcularDistanciaQuilometrosCoordenadas
from ..Default.Default import tempo_processamento
from ..Cronograma.TipoMicroatividade import TipoMicroatividade


class ConjuntoSecaoCabo(ConjuntoComponentes):
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
        self._tempo_preparar_cabo = tempo_processamento["tempo_preparar_cabo"]
        self._tempo_descer_cabo_fundo_do_mar = tempo_processamento["tempo_descer_cabo_fundo_do_mar"]
        self._tempo_puxar_cabo_para_dentro_turbina_ou_subestacao = tempo_processamento[
            "tempo_puxar_cabo_para_dentro_turbina_ou_subestacao"]
        self._taxa_colocacao_aterramento = tempo_processamento["taxa_colocacao_aterramento"]
        self._tempo_testar_terminar_cabo = tempo_processamento["tempo_testar_terminar_cabo"]

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

    def setTempoPrepararCabo(self, valor):
        self._tempo_preparar_cabo = valor

    def getTempoPrepararCabo(self):
        return self._tempo_preparar_cabo

    def setTempoDescerCaboFundoDoMar(self, valor):
        self._tempo_descer_cabo_fundo_do_mar = valor

    def getTempoDescerCaboFundoDoMar(self):
        return self._tempo_descer_cabo_fundo_do_mar

    def setTempoPuxarCaboParaDentro(self, valor):
        self._tempo_puxar_cabo_para_dentro_turbina_ou_subestacao = valor

    def getTempoPuxarCaboParaDentro(self):
        return self._tempo_puxar_cabo_para_dentro_turbina_ou_subestacao

    def setTaxaColocarAterrarCabo(self, valor):
        self._taxa_colocacao_aterramento = valor

    def getTaxaColocarAterrarCabo(self):
        return self._taxa_colocacao_aterramento

    def getTempoColocarAterrarCabo(self):
        distancia = self.getDistanciaEntrePontosInstalacao()
        return distancia*self.getTaxaColocarAterrarCabo()

    def setTempoTestarTerminarCabo(self, valor):
        self._tempo_testar_terminar_cabo = valor

    def getTempoTestarTerminarCabo(self):
        return self._tempo_testar_terminar_cabo

    def executarInstalacao(self, cronograma, embarcacao, dataInicio):
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação da secao de cabo de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        #
        tarefa0 = "Posicionar no local de instalacao"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa0,
                                           TipoMicroatividade.INSTALACAO_SISTEMA_ARRAY, self._tempo_posicionar_instalar_cabo)
        #
        tarefa1 = "Preparar cabo"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_SISTEMA_ARRAY, self._tempo_preparar_cabo)
        #
        tarefa2 = "Descer cabo ate o fundo do mar"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_SISTEMA_ARRAY, self._tempo_descer_cabo_fundo_do_mar)
        #
        tarefa3 = "Puxar cabo para dentro da turbina ou subestacao"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa3,
                                           TipoMicroatividade.INSTALACAO_SISTEMA_ARRAY, self._tempo_puxar_cabo_para_dentro_turbina_ou_subestacao)
        #
        tarefa4 = "Colocar e aterrar cabo"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa4,
                                           TipoMicroatividade.INSTALACAO_SISTEMA_ARRAY, self.getTempoColocarAterrarCabo())
        #
        tarefa5 = "Testar e terminar o cabo"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa5,
                                           TipoMicroatividade.INSTALACAO_SISTEMA_ARRAY, self._tempo_testar_terminar_cabo)
        #
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao
    #

    def getId(self):
        return self._id
