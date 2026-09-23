from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Derivados.OrelhaCoelhoNacele import OrelhaCoelhoNacele


class IPadraoInstalacaoOrelhaCoelhoNacele:
    def __init__(self, orelha_coelho):
        self.__validarOrelhaCoelhoNacele__(orelha_coelho)
        self._orelha_coelho = orelha_coelho
        self._tempo_anexar_orelha_coelho_na_subestrutura = tempo_processamento[
            "tempo_anexar_orelha_coelho_na_subestrutura_offshore"]
        self._liberar_orelha_coelho_deck = tempo_processamento[
            "tempo_liberacao_deck_orelha_coelho_nacele"]

    def __validarOrelhaCoelhoNacele__(self, orelha_coelho):
        if not isinstance(orelha_coelho, OrelhaCoelhoNacele):
            raise KeyError(
                "A classe derivativa deve ser do tipo OrelhaCoelhoNacele.")

    def setTempoLiberarOrelhaCoelhoNaceleDeck(self, valor):
        self._liberar_orelha_coelho_deck = valor

    def getTempoLiberarOrelhaCoelhoNaceleDeck(self):
        return self._liberar_orelha_coelho_deck

    def getTempoElevarOrelhaCoelhoNaceleVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarOrelhaCoelhoNaNacele(self):
        return self._tempo_anexar_orelha_coelho_na_nacele

    def setTempoAnexarOrelhaCoelhoNaNacele(self, valor):
        self._tempo_anexar_orelha_coelho_na_nacele = valor

    def criarTarefasInstalacaoOrelhaCoelho(self, nomeMacroatividade, cronograma, embarcacao, altura):
        nomeTarefa = embarcacao.nomeTarefa()
        tarefa0 = "Liberar a orelha de coelho do deck da embarcação"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa0,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_orelha_coelho_deck)
        tarefa1 = "Elevar a orelha de coelho na posição vertical "
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1, TipoMicroatividade.INSTALACAO_AEROGERADOR,
                                           self.getTempoElevarOrelhaCoelhoNaceleVertical(embarcacao, altura))
        tarefa2 = "Anexar orelha de coelho na subestrutura"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_orelha_coelho_na_subestrutura)
