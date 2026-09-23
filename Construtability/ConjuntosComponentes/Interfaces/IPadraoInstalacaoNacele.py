from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Nacele import Nacele


class IPadraoInstalacaoNacele:
    def __init__(self, nacele):
        self.__validarNacele__(nacele)
        self._nacele = nacele
        self._tempo_anexar_nacele_na_torre = tempo_processamento[
            "tempo_anexar_nacele_na_torre_offshore"]
        self._liberar_nacele_deck = tempo_processamento["tempo_liberacao_deck_nacele"]

    def __validarNacele__(self, nacele):
        if not isinstance(nacele, Nacele):
            raise KeyError("A classe derivativa deve ser Nacele.")

    def setTempoLiberarNaceleDeck(self, valor):
        self._liberar_nacele_deck = valor

    def getTempoLiberarHubNaceleDeck(self):
        return self._liberar_nacele_deck

    def getTempoElevarNaceleVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarNaceleNaTorre(self):
        return self._tempo_anexar_nacele_torre

    def criarTarefasInstalacaoNacele(self, nomeMacroatividade, cronograma, embarcacao, altura):
        nomeTarefa = embarcacao.nomeTarefa()
        tarefa0 = "Liberar o nacele do deck da embarcação"
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacroatividade, tarefa0, TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_nacele_deck)
        tarefa1 = "Elevar o nacele na posição vertical"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self.getTempoElevarNaceleVertical(embarcacao, altura))
        tarefa2 = "Anexar o nacele na torre"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_nacele_na_torre)

    def getNacele(self):
        return self._nacele
