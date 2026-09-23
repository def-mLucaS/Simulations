from ..Componentes.AbstractComponenteRetangular import ComponenteRetangular
from ..Default.Default import tempo_processamento


class Gravidade(ComponenteRetangular):
    def __init__(self, comprimento, largura, altura, massa):
        # informacoes para o construtor da classe base
        info_componente = {
            # informações da gravidade
            "comprimento": comprimento,                     # [m]
            "largura": largura,                             # [m]
            "altura": altura,                               # [m]
            "massa": massa,                                 # [t]
            # [True | False]    - TODO: Normalmente transportada com a base no deck, uma vez que são instaladas nessa posição
            "with_armazenamento_horizontal": False,
            # [True | False]    - TODO: Transportar a gravidade deitada exige uma estrutura de suporte especial e aumenta o risco de danos à gravidade.
            "with_armazenamento_vertical": True,
            # [True | False]     - TODO: Um tanto improvável o empilhamento por conta do peso e dimensões
            "is_empilhavel": False
        }
        super().__init__(**info_componente)
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_gravidade"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento[
            "tempo_liberacao_deck_gravidade"]

    def getAreaOcupada(self):
        return self._area_ocupada_vertical

    def getDensidadeArea(self):
        return self._densidade_area_vertical

    def getTempoFixacaoDeck(self):
        return self._tempo_fixacao_deck_embarcacao

    def setTempoFixacaoDeck(self, tempo):
        self._tempo_fixacao_deck_embarcacao = tempo

    def getTempoLiberacaoDeck(self):
        return self._tempo_liberacao_deck_embarcacao

    def setTempoLiberacaoDeck(self, tempo):
        self._tempo_liberacao_deck_embarcacao = tempo

    def getTipoComponente(self):
        return "gravidade"
