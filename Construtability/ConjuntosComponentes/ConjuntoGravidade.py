from ..Componentes.Gravidade import Gravidade
from ..ConjuntosComponentes.ConjuntoFundacao import ConjuntoFundacao
from ..Default.Default import tempo_processamento
from ..Cronograma.Cronograma import TipoMicroatividade


class ConjuntoGravidade(ConjuntoFundacao):
    def __init__(self, id, gravidade):
        args = (gravidade,)
        super().__init__(*args)
        self._id = id
        self._gravidade = gravidade
        self.__validar__(id, gravidade)
        # informacoes instalacao
        self._tempo_preparacao_solo = tempo_processamento["tempo_preparacao_solo_gravidade"]
        self._pesquisar_com_rov = tempo_processamento["tempo_pesquisa_com_rov"]
        self._posicionar = tempo_processamento["posicionar_gravidade"]
        self._enchimento_lastro = tempo_processamento["tempo_enchimento_lastro"]
        self._tempo_fixar_gravidade_argamassa = tempo_processamento[
            "tempo_fixar_gravidade_argamassa"]

    def __validar__(self, id, gravidade):
        if not (isinstance(id, int)):
            raise KeyError("A informação de ID deve ser dada em um inteiro.")
        if not isinstance(gravidade, Gravidade):
            raise KeyError("A classe derivativa deve ser GRAVIDADE.")

    def setTempoPesquisaComRov(self, valor):
        self._pesquisar_com_rov = valor

    def setTempoPosicionar(self, valor):
        self._posicionar = valor

    def setTempoEnchimentoComLastro(self, valor):
        self._enchimento_lastro = valor

    def setTempoPreparacaoSolo(self, valor):
        self._tempo_preparacao_solo = valor

    def setTempoFixarGravidadeComArgamassa(self, valor):
        self._tempo_fixar_gravidade_argamassa = valor

    def getTempoPesquisaComRov(self):
        return self._pesquisar_com_rov

    def getTempoPosicionar(self):
        return self._posicionar

    def getTempoEnchimentoLastro(self):
        return self._enchimento_lastro

    def getTempoPreparacaoSolo(self):
        return self._tempo_preparacao_solo

    def getTempoFixarGravidadeComArgamassa(self):
        return self._tempo_fixar_gravidade_argamassa

    def getNomeTarefaPreparacaoSolo(self):
        return "Preparacao do Solo"

    def executarTarefaParalelaPreparacaoDoSolo(self, cronograma, dataInicio):
        nomeTarefa = "Tarefas independentes de embarcacoes"
        nomeMacroatividade = "Preparacao do solo para a fundacao id " + \
            str(self._id)
        cronograma.adicionarTarefa(nomeTarefa)
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        tarefa = self.getNomeTarefaPreparacaoSolo()
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self._tempo_preparacao_solo)
        #
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao

    def executarInstalacao(self, cronograma, embarcacao, dataInicio, profundidade):
        # Executar preparacao de solo (tarefa paralela)
        # TODO: discutir se esse tipo de tarefa deve ser considerado mesmo, visto que nao depende da embarcacao
        # dataFim = self.executarTarefaParalelaPreparacaoDoSolo(cronograma, dataInicio)
        # dataInicio = dataFim

        # Tarefas com embarcacoes
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação fundação de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        #
        tarefa0 = "Pesquisar local com o ROV"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa0, TipoMicroatividade.INSTALACAO_FUNDACAO, self._pesquisar_com_rov)
        #
        tarefa1 = "Posicionar fundacao de gravidade"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa1, TipoMicroatividade.INSTALACAO_FUNDACAO, self._posicionar)
        #
        tarefa2 = "Encher com lastro"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa2, TipoMicroatividade.INSTALACAO_FUNDACAO, self._enchimento_lastro)
        #
        tarefa3 = "Fixar gravidade no fundo do mar com argamassa"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa3, TipoMicroatividade.INSTALACAO_FUNDACAO, self._enchimento_lastro)
        #
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)

        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)

        return dataFimExecucao

    def getId(self):
        return self._id

    def getGravidade(self):
        return self._gravidade
