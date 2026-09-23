from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Hub import Hub
from ...Componentes.Nacele import Nacele
from ...Componentes.Derivados.HubNacele import HubNacele


class IPadraoInstalacaoHubNacele:
    def __init__(self, hub, nacele):
        self.__validarHubNacele__(hub, nacele)
        self._hubNacele = HubNacele(hub, nacele)
        self._tempo_anexar_hub_nacele_na_torre = tempo_processamento[
            "tempo_anexar_hub_nacele_na_torre_offshore"]
        self._liberar_hub_nacele_deck = tempo_processamento["tempo_liberacao_deck_hub_nacele"]

    def __validarHubNacele__(self, hub, nacele):
        if not isinstance(nacele, Nacele):
            raise KeyError("A classe derivativa deve ser Nacele.")
        if not isinstance(hub, Hub):
            raise KeyError("A classe derivativa deve ser Hub.")

    def setTempoLiberarHubNaceleDeck(self, valor):
        self._liberar_hub_nacele_deck = valor

    def getTempoLiberarHubNaceleDeck(self):
        return self._liberar_hub_nacele_deck

    def getTempoElevarHubNaceleVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarHubNaceleNaTorre(self):
        return self._tempo_anexar_hub_nacele_torre

    def criarTarefasInstalacaoHubNacele(self, nomeMacroatividade, cronograma, embarcacao, altura):
        nomeTarefa = embarcacao.nomeTarefa()
        tarefa0 = "Liberar o hub+nacele do deck da embarcação"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa0,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_hub_nacele_deck)
        tarefa1 = "Elevar o hub+nacele na posição vertical"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self.getTempoElevarHubNaceleVertical(embarcacao, altura))
        tarefa2 = "Anexar o hub+nacele na torre"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_hub_nacele_na_torre)

    def getHubNacele(self):
        return self._hubNacele
