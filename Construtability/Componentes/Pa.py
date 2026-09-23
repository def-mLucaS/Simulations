from ..Componentes.AbstractComponenteCilindricoEmpilhavel import ComponenteCilindricoEmpilhavel
from ..Default.Default import tempo_processamento


class Pa(ComponenteCilindricoEmpilhavel):
    def __init__(self, id, diametro, altura, massa, capacidade_empilhamento, numero_camadas_empilhamento):
        # informacoes para o construtor da classe base
        info_componente = {
            # informações da monopile
            # [m]                - TODO: Se for diametro duas informacoes terão o mesmo valor
            "comprimento": diametro,
            "largura": diametro,                            # [m]
            "altura": altura,                               # [m]
            "massa": massa,                                 # [t]
            # [True | False]    - TODO: Normalmente transportada com a base no deck, uma vez que são instaladas nessa posição
            "with_armazenamento_horizontal": True,
            # [True | False]    - TODO: Transportar a monopile deitada exige uma estrutura de suporte especial e aumenta o risco de danos à monopile.
            "with_armazenamento_vertical": True,
            # [True | False]     - TODO: Um tanto improvável o empilhamento por conta do peso e dimensões
            "is_empilhavel": True,
            # [t]                - TODO: Ver o caso do rack! Declarar pelo menos esta ou a informação abaixo
            "capacidade_empilhamento": capacidade_empilhamento,
            # [unidades]
            "maximo_numero_camadas_empilhamento": numero_camadas_empilhamento
        }
        super().__init__(**info_componente)
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_pa"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento["tempo_liberacao_deck_pa"]
        self._id = id

    def getAreaOcupada(self):
        return self._area_ocupada_vertical

    def getDensidadeArea(self):
        return self._densidade_area_vertical

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
        return "pa " + str(self.getId())

    def getDiametro(self):
        return self._comprimento

    def getId(self):
        return self._id
