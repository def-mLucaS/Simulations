from ..Componentes.AbstractComponenteCilindrico import ComponenteCilindrico
from ..Default.Default import tempo_processamento

class PecaTransicao(ComponenteCilindrico):
    def __init__(self, diametro, altura, massa):
        # informacoes para o construtor da classe base
        info_componente = {
            # informações da peca de transicao
            "comprimento": diametro,                        # [m]                - TODO: Se for diametro duas informacoes terão o mesmo valor
            "largura": diametro,                            # [m]
            "altura": altura,                               # [m]
            "massa": massa,                                 # [t]
            "with_armazenamento_horizontal": False,         # [True | False]
            "with_armazenamento_vertical": True,            # [True | False]    - TODO: Normalmente transportada na vertical
            "is_empilhavel": False                          # [True | False]
        }
        super().__init__(**info_componente)
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_peca_transicao"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento["tempo_liberacao_deck_peca_transicao"]

    def getAreaOcupada(self):
        return self._area_ocupada_vertical

    def getDensidadeArea(self):
        return self._densidade_area_vertical

    def getTempoFixacaoDeck(self):
        return self._tempo_fixacao_deck_embarcacao

    def setTempoFixacaoDeck(self,tempo):
        self._tempo_fixacao_deck_embarcacao = tempo

    def getTempoLiberacaoDeck(self):
        return self._tempo_liberacao_deck_embarcacao

    def setTempoLiberacaoDeck(self,tempo):
        self._tempo_liberacao_deck_embarcacao = tempo

    def getTipoComponente(self):
        return "peca de transicao"

    def getDiametro(self):
        return self._comprimento