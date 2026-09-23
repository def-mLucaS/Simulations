from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Pa import Pa


class IPadraoInstalacaoPa:
    def __init__(self, pa):
        self.__validarPa__(pa)
        self._pa = pa
        self._tempo_anexar_pa_na_orelha_coelho = tempo_processamento[
            "tempo_anexar_pa_na_orelha_coelho_offshore"]
        self._liberar_pa_deck = tempo_processamento["tempo_liberacao_deck_pa"]

    def __validarPa__(self, pa):
        if not isinstance(pa, Pa):
            raise KeyError("A classe derivativa deve ser Pa.")

    def setTempoLiberarPaDeck(self, valor):
        self._liberar_pa_deck = valor

    def getTempoLiberarHubPaDeck(self):
        return self._liberar_pa_deck

    def getTempoElevarPaVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarPaNaTorre(self):
        return self._tempo_anexar_pa_torre

    def criarTarefasInstalacaoPa(self, nomeMacroatividade, cronograma, embarcacao, altura):
        nomeTarefa = embarcacao.nomeTarefa()
        tarefa0 = "Liberar o pa do deck da embarcação"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa0, TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_pa_deck)
        tarefa1 = "Elevar a pá na posição vertical"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self.getTempoElevarPaVertical(embarcacao, altura))
        tarefa2 = "Anexar a pá na orelha de coelho"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_pa_na_orelha_coelho)

    def getPa(self):
        return self._pa
