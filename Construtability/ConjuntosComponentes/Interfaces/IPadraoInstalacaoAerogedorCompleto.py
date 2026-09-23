from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Derivados.AerogeradorCompleto import AerogeradorCompleto


class IPadraoInstalacaoAerogeradorCompleto:
    def __init__(self, aerogerador_completo):
        self.__validarAerogeradorCompleto__(aerogerador_completo)
        self._aerogerador_completo = aerogerador_completo
        self._tempo_anexar_aerogerador_completo_na_fundacao = tempo_processamento[
            "tempo_anexar_aerogerador_completo_na_fundacao_offshore"]
        self._liberar_aerogerador_completo_deck = tempo_processamento[
            "tempo_liberacao_deck_aerogerador_completo"]

    def __validarAerogeradorCompleto__(self, aerogerador_completo):
        if not isinstance(aerogerador_completo, AerogeradorCompleto):
            raise KeyError(
                "A classe derivativa deve do tipo AerogeradorCompleto.")

    def setTempoLiberarAerogeradorCompletoDeck(self, valor):
        self._liberar_aerogerador_completo_deck = valor

    def getTempoLiberarAerogeradorCompletoDeck(self):
        return self._liberar_aerogerador_completo_deck

    def getTempoElevarAerogeradorCompletoVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarAerogeradorCompletoNaSubestrutura(self):
        return self._tempo_anexar_aerogerador_completo_na_fundacao

    def setTempoAnexarAerogeradorCompletoNaSubestrutura(self, valor):
        self._tempo_anexar_aerogerador_completo_na_fundacao = valor

    def criarTarefasInstalacaoAerogeradorCompleto(self, nomeMacroatividade, cronograma, embarcacao):
        nomeTarefa = embarcacao.nomeTarefa()
        tarefa0 = "Liberar o aerogerador completo do deck da embarcacao"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa0,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_aerogerador_completo_deck)
        tarefa1 = "Elevar o aerogerador completo na posição vertical "
        alturaElevacao = self._aerogerador_completo.getAltura()
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1, TipoMicroatividade.INSTALACAO_AEROGERADOR,
                                           self.getTempoElevarAerogeradorCompletoVertical(embarcacao, alturaElevacao))
        tarefa2 = "Anexar o aerogerador completo na fundacao"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_aerogerador_completo_na_fundacao)

    def getAlturaAerogeradorCompleto(self):
        return self._aerogerador_completo.getAltura()
