from ..Componentes.Monopile import Monopile
from ..Componentes.PecaTransicao import PecaTransicao
from ..ConjuntosComponentes.ConjuntoFundacao import ConjuntoFundacao
from ..Default.Default import tempo_processamento
from ..Default.Default import parametros
from ..Cronograma.Cronograma import TipoMicroatividade
from ..Metodos.TipoConexao import TipoConexao


class ConjuntoMonopile(ConjuntoFundacao):
    def __init__(self, id, monopile, peca_transicao, conexao):
        args = (monopile, peca_transicao)
        super().__init__(*args)
        self.__validar__(id, monopile, peca_transicao, conexao)
        self._id = id
        self._monopile = monopile
        self._peca_transicao = peca_transicao
        self._conexao = conexao
        # informacoes instalacao
        self._pesquisar_com_rov = tempo_processamento["tempo_pesquisa_com_rov"]
        self._liberar_monopile_deck = tempo_processamento["tempo_liberacao_deck_monopile"]
        self._preparar_equipamento_conducao = tempo_processamento[
            "tempo_preparar_equipamento_conducao_monopile"]
        self._taxa_conducao_monopile = tempo_processamento["taxa_conducao_estaca_monopile"]
        self._comprimento_incorporacao = parametros["comprimento_incorporacao_estaca_monopile"]
        self._preparar_equipamento_elevacao = tempo_processamento[
            "tempo_preparar_equipamento_elevacao"]
        self._parafusar_conexao = tempo_processamento["tempo_parafuso_peca_transicao"]
        self._aplicar_argamassa_conexao = tempo_processamento["tempo_argamassa_peca_transicao"]
        self._cura_argamassa = tempo_processamento["tempo_cura_argamassa"]

    def __validar__(self, id, monopile, peca_transicao, conexao):
        if not (isinstance(id, int)):
            raise KeyError("A informação de ID deve ser dada em um inteiro.")
        if not isinstance(monopile, Monopile):
            raise KeyError("A classe derivativa deve ser MONOPILE.")
        if not isinstance(peca_transicao, PecaTransicao):
            raise KeyError("A classe derivativa deve ser PECATRANSICAO.")
        if not isinstance(conexao, TipoConexao):
            raise KeyError("A classe deve ser enum TipoConexao.")

    def getTipoConexao(self):
        return self._conexao

    def setTipoConexao(self, conexao):
        self._conexao = conexao

    def getTempoElevarMonopileVertical(self, embarcacao):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(self._monopile.getAltura())

    def getTempoDescerMonopileAteFundo(self, embarcacao, profundidade):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(profundidade+10)

    def setTempoPesquisaComRov(self, valor):
        self._pesquisar_com_rov = valor

    def getTempoPesquisaComRov(self):
        return self._pesquisar_com_rov

    def setTempoLiberarMonopileDeck(self, valor):
        self._liberar_monopile_deck = valor

    def getTempoLiberarMonopileDeck(self):
        return self._liberar_monopile_deck

    def setTempoPrepararEquipamentoConducao(self, valor):
        self._preparar_equipamento_conducao = valor

    def getTempoPrepararEquipamentoConducao(self):
        return self._preparar_equipamento_conducao

    def setTempoPrepararEquipamentoElevacao(self, valor):
        self._preparar_equipamento_elevacao = valor

    def getTempoPrepararEquipamentoElevacao(self):
        return self._preparar_equipamento_elevacao

    def setTaxaConducaoMonopile(self, valor):
        self._taxa_conducao_monopile = valor  # m/h

    def getTaxaConducaoMonopile(self):
        return self._taxa_conducao_monopile

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

    def getTempoCravarMonopile(self):
        return self._comprimento_incorporacao/self._taxa_conducao_monopile  # h

    def getTempoDescerPecaTransicao(self, embarcacao, profundidade):
        extensao = profundidade-self._monopile.getAltura()
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(extensao)

    def executarInstalacao(self, cronograma, embarcacao, dataInicio, profundidade):
        nomeTarefa = embarcacao.nomeTarefa()
        # nomeMacroatividade = "Instalação da monopile e da peca de transicao"
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
        tarefa1 = "Liberar a monopile do deck da embarcação"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa1, TipoMicroatividade.INSTALACAO_FUNDACAO, self._liberar_monopile_deck)
        #
        tarefa2 = "Elevar a monopile na posição vertical"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoElevarMonopileVertical(embarcacao))
        #
        tarefa3 = "Descer a monopile até o fundo do mar"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa3,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoDescerMonopileAteFundo(embarcacao, profundidade))
        #
        tarefa4 = "Preparar o equipamento de condução"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa4,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self._preparar_equipamento_conducao)
        #
        tarefa5 = "Cravar a monopile"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa5,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoCravarMonopile())
        #
        tarefa6 = "Reequipar o equipamento de elevação"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa6,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self._preparar_equipamento_elevacao)
        #
        tarefa7 = "Descer a peça de transição ate o topo da monopile"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa7,
                                           TipoMicroatividade.INSTALACAO_FUNDACAO, self.getTempoDescerPecaTransicao(embarcacao, profundidade))
        # Conexao entre peca de transicao e monopile
        if (self._conexao == TipoConexao.PARAFUSO):
            tarefa8 = "Parafusar peça de transição na monopile"
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

    def getMonopile(self):
        return self._monopile

    def getPecaTransicao(self):
        return self._peca_transicao
