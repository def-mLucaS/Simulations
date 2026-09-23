from ..Componentes.Jaqueta import Jaqueta
from ..Componentes.PecaTransicao import PecaTransicao
from ..ConjuntosComponentes.ConjuntoFundacao import ConjuntoFundacao
from ..Default.Default import tempo_processamento
from ..Default.Default import parametros
from ..Cronograma.Cronograma import TipoMicroatividade
from ..Metodos.TipoConexao import TipoConexao


class ConjuntoJaqueta(ConjuntoFundacao):
    def __init__(self, id, jaqueta, peca_transicao, conexao):
        args = (jaqueta, peca_transicao)
        super().__init__(*args)
        self.__validar__(id, jaqueta, peca_transicao, conexao)
        self._id = id
        self._jaqueta = jaqueta
        self._peca_transicao = peca_transicao
        self._conexao = conexao
        # informacoes instalacao
        self._pesquisar_com_rov = tempo_processamento["tempo_pesquisa_com_rov"]
        self._liberar_jaqueta_deck = tempo_processamento["tempo_liberacao_deck_jaqueta"]
        self._preparar_equipamento_conducao = tempo_processamento[
            "tempo_preparar_equipamento_conducao_jaqueta"]
        self._taxa_conducao_jaqueta = tempo_processamento["taxa_conducao_estaca_jaqueta"]
        self._comprimento_incorporacao = parametros["comprimento_incorporacao_estaca_jaqueta"]
        self._preparar_equipamento_elevacao = tempo_processamento[
            "tempo_preparar_equipamento_elevacao"]
        self._parafusar_conexao = tempo_processamento["tempo_parafuso_peca_transicao"]
        self._aplicar_argamassa_conexao = tempo_processamento["tempo_argamassa_peca_transicao"]
        self._cura_argamassa = tempo_processamento["tempo_cura_argamassa"]

    def __validar__(self, id, jaqueta, peca_transicao, conexao):
        if not (isinstance(id, int)):
            raise KeyError("A informação de ID deve ser dada em um inteiro.")
        if not isinstance(jaqueta, Jaqueta):
            raise KeyError("A classe derivativa deve ser JAQUETA.")
        if not isinstance(peca_transicao, PecaTransicao):
            raise KeyError("A classe derivativa deve ser PECATRANSICAO.")
        if not isinstance(conexao, TipoConexao):
            raise KeyError("A classe deve ser enum TipoConexao.")

    def getTipoConexao(self):
        return self._conexao

    def setTipoConexao(self, conexao):
        self._conexao = conexao

    def getTempoElevarJaquetaVertical(self, embarcacao):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(self._jaqueta.getAltura())

    def getTempoDescerJaquetaAteFundo(self, embarcacao, profundidade):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(profundidade+10)

    def setTempoPesquisaComRov(self, valor):
        self._pesquisar_com_rov = valor

    def getTempoPesquisaComRov(self):
        return self._pesquisar_com_rov

    def setTempoLiberarJaquetaDeck(self, valor):
        self._liberar_jaqueta_deck = valor

    def getTempoLiberarJaquetaDeck(self):
        return self._liberar_jaqueta_deck

    def setTempoPrepararEquipamentoConducao(self, valor):
        self._preparar_equipamento_conducao = valor

    def getTempoPrepararEquipamentoConducao(self):
        return self._preparar_equipamento_conducao

    def setTempoPrepararEquipamentoElevacao(self, valor):
        self._preparar_equipamento_elevacao = valor

    def getTempoPrepararEquipamentoElevacao(self):
        return self._preparar_equipamento_elevacao

    def setTaxaConducaoJaqueta(self, valor):
        self._taxa_conducao_jaqueta = valor  # m/h

    def getTaxaConducaoJaqueta(self):
        return self._taxa_conducao_jaqueta

    def setComprimentoIncorporacao(self, valor):
        self._comprimento_incorporacao = valor  # m

    def getComprimentoIncorporacao(self):
        return self._comprimento_incorporacao

    def setTempoParafusarConexao(self, valor):
        self._parafusar_conexao = valor

    def getTempoParafusarConexao(self):
        return self._parafusar_conexao

    def setTempoAplicarArgamassaConexao(self, valor):
        self._aplicar_argamassa_conexao = valor

    def getTempoAplicarArgamassaConexao(self):
        return self._aplicar_argamassa_conexao

    def setTempoCuraArgamassa(self, valor):
        self._cura_argamassa = valor

    def getTempoCuraArgamassa(self):
        return self._cura_argamassa

    def getTempoCravarJaqueta(self):
        return self._comprimento_incorporacao/self._taxa_conducao_jaqueta  # h

    def getTempoDescerPecaTransicao(self, embarcacao, profundidade):
        extensao = profundidade-self._jaqueta.getAltura()
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(extensao)

    def getTempoCravarJaqueta(self):
        numero_estacas = 3  # fixado em 3 estacas
        return numero_estacas*self._comprimento_incorporacao/self._taxa_conducao_jaqueta  # h

    def executarInstalacao(self, cronograma, embarcacao, dataInicio, profundidade):
        nomeTarefa = embarcacao.nomeTarefa()
        # nomeMacroatividade = "Instalação da jaqueta e da peca de transição"
        nomeMacroatividade = "Instalação fundação de id " + \
            str(self.getId()) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        #
        tarefa0 = "Pesquisar local com o ROV"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa0, TipoMicroatividade.INSTALACAO_FUNDACAO, self._pesquisar_com_rov)
        #
        tarefa1 = "Liberar a jaqueta do deck da embarcação"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa1, TipoMicroatividade.INSTALACAO_FUNDACAO, self._liberar_jaqueta_deck)
        #
        tarefa2 = "Elevar a jaqueta na posição vertical"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoElevarJaquetaVertical(embarcacao))
        #
        tarefa3 = "Descer a jaqueta ate o fundo do mar"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa3,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoDescerJaquetaAteFundo(embarcacao, profundidade))
        #
        tarefa4 = "Preparar o equipamento de condução"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa4,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self._preparar_equipamento_conducao)
        #
        tarefa5 = "Cravar a jaqueta"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa5, TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoCravarJaqueta())
        #
        tarefa6 = "Reequipar o equipamento de elevação"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa6,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self._preparar_equipamento_elevacao)
        #
        tarefa7 = "Descer a peça de transição ate o topo da jaqueta"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa7,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoDescerPecaTransicao(embarcacao, profundidade))
        # Conexao entre peca de transicao e jaqueta
        if (self._conexao == TipoConexao.PARAFUSO):
            tarefa8 = "Parafusar peça de transição na jaqueta"
            cronograma.adicionarMicroatividade(
                nomeTarefa, nomeMacroatividade, tarefa8, TipoMicroatividade.INSTALACAO_FUNDACAO, self._parafusar_conexao)
        elif (self._conexao == TipoConexao.ARGAMASSA):
            tarefa8 = "Aplicar argamassa na conexão"
            cronograma.adicionarMicroatividade(
                nomeTarefa, nomeMacroatividade, tarefa8, TipoMicroatividade.INSTALACAO_FUNDACAO, self._aplicar_argamassa_conexao)
            tarefa9 = "Cura da argamassa"
            cronograma.adicionarMicroatividade(
                nomeTarefa, nomeMacroatividade, tarefa9, TipoMicroatividade.INSTALACAO_FUNDACAO, self._cura_argamassa)
        #
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)

        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)

        return dataFimExecucao

    def getId(self):
        return self._id

    def getJaqueta(self):
        return self._jaqueta

    def getPecaTransicao(self):
        return self._peca_transicao
