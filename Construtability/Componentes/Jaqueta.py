from ..Componentes.AbstractComponenteCilindrico import ComponenteCilindrico
from ..Default.Default import tempo_processamento, parametros

class Jaqueta(ComponenteCilindrico):
    def __init__(self, diametro, altura, massa):
        # informacoes para o construtor da classe base
        info_componente = {
            # informações da jaqueta
            "comprimento": diametro,                        # [m]                - TODO: Se for diametro duas informacoes terão o mesmo valor
            "largura": diametro,                            # [m]
            "altura": altura,                               # [m]
            "massa": massa,                                 # [t]
            "with_armazenamento_horizontal": False,         # [True | False]    - TODO: Normalmente transportada com a base no deck, uma vez que são instaladas nessa posição
            "with_armazenamento_vertical": True,            # [True | False]    - TODO: Transportar a jaqueta deitada exige uma estrutura de suporte especial e aumenta o risco de danos à jaqueta.
            "is_empilhavel": False                          # [True | False]     - TODO: Um tanto improvável o empilhamento por conta do peso e dimensões
        }
        super().__init__(**info_componente)
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_jaqueta"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento["tempo_liberacao_deck_jaqueta"]
        self._numero_estacas = parametros["numero_estacas_jaqueta"]

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

    def getNumeroEstacas(self):
        return self._numero_estacas

    def setNumeroEstacas(self,numero):
        self._numero_estacas = numero

    def getTipoComponente(self):
        return "jaqueta"

    def getDiametro(self):
        return self._comprimento