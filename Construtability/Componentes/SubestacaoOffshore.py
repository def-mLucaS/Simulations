from ..Componentes.AbstractComponenteRetangular import ComponenteRetangular
from ..Default.Default import tempo_processamento


class SubestacaoOffshore(ComponenteRetangular):
    def __init__(self, comprimento, largura, altura, massa):
        # informacoes para o construtor da classe base
        info_componente = {
            "comprimento": comprimento,
            "largura": largura,  # [m]
            "altura": altura,  # [m]
            "massa": massa,  # [t]
            "with_armazenamento_horizontal": False,
            "with_armazenamento_vertical": True,
            "is_empilhavel": False
        }
        super().__init__(**info_componente)
        self._tempo_anexar_subestacao_na_fundacao_offshore = tempo_processamento[
            "tempo_anexar_subestacao_na_fundacao_offshore"]
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_subestacao"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento[
            "tempo_liberacao_deck_subestacao"]

    def getTipoComponente(self):
        return "subestacao_offshore"

    def getTempoAnexarSubestacaoNaFundacao(self):
        return self._tempo_anexar_subestacao_na_fundacao_offshore

    def setTempoAnexarSubestacaoNaFundacao(self, tempo):
        self._tempo_anexar_subestacao_na_fundacao_offshore = tempo

    def getTempoFixacaoDeck(self):
        return self._tempo_fixacao_deck_embarcacao

    def setTempoFixacaoDeck(self, tempo):
        self._tempo_fixacao_deck_embarcacao = tempo

    def getTempoLiberacaoDeck(self):
        return self._tempo_liberacao_deck_embarcacao

    def setTempoLiberacaoDeck(self, tempo):
        self._tempo_liberacao_deck_embarcacao = tempo

    def getTempoElevarSubestacaoVertical(self, embarcacao):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(self.getAltura())
