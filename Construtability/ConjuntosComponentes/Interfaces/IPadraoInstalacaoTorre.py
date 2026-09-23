from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Derivados.Torre import Torre


class IPadraoInstalacaoTorre:
    def __init__(self, torre):
        self.__validarTorre__(torre)
        self._torre = torre
        self._tempo_anexar_torre_na_subestrutura = tempo_processamento[
            "tempo_anexar_torre_na_fundacao_offshore"]
        self._liberar_torre_deck = tempo_processamento["tempo_liberacao_deck_torre"]

    def __validarTorre__(self, torre):
        if not isinstance(torre, Torre):
            raise KeyError("A classe derivativa deve do tipo Torre.")

    def setTempoLiberarTorreDeck(self, valor):
        self._liberar_torre_deck = valor

    def getTempoLiberarTorreDeck(self):
        return self._liberar_torre_deck

    def getTempoElevarTorreVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarTorreNaSubestrutura(self):
        return self._tempo_anexar_torre_na_subestrutura

    def setTempoAnexarTorreNaSubestrutura(self, valor):
        self._tempo_anexar_torre_na_subestrutura = valor

    def criarTarefasInstalacaoTorre(self, nomeMacroatividade, cronograma, embarcacao):
        nomeTarefa = embarcacao.nomeTarefa()
        tarefa0 = "Liberar a de torre do deck da embarcação"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa0, TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_torre_deck)
        tarefa1 = "Elevar a de torre na posição vertical "
        alturaElevacao = self._torre.getAltura()
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self.getTempoElevarTorreVertical(embarcacao, alturaElevacao))
        tarefa2 = "Anexar torre na fundacao"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_torre_na_subestrutura)

    def getAlturaTorre(self):
        return self._torre.getAltura()
