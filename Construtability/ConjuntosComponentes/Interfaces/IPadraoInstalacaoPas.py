from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Pa import Pa


class IPadraoInstalacaoPas:
    def __init__(self, pa1, pa2, pa3):
        self.__validarPas__(pa1, pa2, pa3)
        self._pas = (pa1, pa2, pa3)
        self._tempo_anexar_pa = tempo_processamento["tempo_anexar_pa_hub_offshore"]
        self._liberar_pa_deck = tempo_processamento["tempo_liberacao_deck_pa"]

    def __validarPas__(self, pa1, pa2, pa3):
        if not isinstance(pa1, Pa):
            raise KeyError("A classe derivativa deve ser Pa.")
        if not isinstance(pa2, Pa):
            raise KeyError("A classe derivativa deve ser Pa.")
        if not isinstance(pa3, Pa):
            raise KeyError("A classe derivativa deve ser Pa.")

    def setTempoLiberarPaDeck(self, valor):
        self._liberar_pa_deck = valor

    def getTempoLiberarPaDeck(self):
        return self._liberar_pa_deck

    def getTempoElevarPaVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarPaNoHub(self):
        return self._tempo_anexar_pa

    def criarTarefasInstalacaoPas(self, nomeMacroatividade, cronograma, embarcacao, altura):
        nomeTarefa = embarcacao.nomeTarefa()
        numeroPa = 0
        for pa in self._pas:
            numeroPa += 1
            tarefa0 = "Liberar a pá " + \
                str(numeroPa) + " do deck da embarcação"
            cronograma.adicionarMicroatividade(
                nomeTarefa, nomeMacroatividade, tarefa0, TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_pa_deck)
            tarefa1 = "Elevar o pá " + str(numeroPa) + " na posição vertical"
            cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                               TipoMicroatividade.INSTALACAO_AEROGERADOR, self.getTempoElevarPaVertical(embarcacao, altura))
            tarefa2 = "Anexar o pá " + str(numeroPa) + " no hub"
            cronograma.adicionarMicroatividade(
                nomeTarefa, nomeMacroatividade, tarefa2, TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_pa)

    def getPas(self):
        return self._pas
