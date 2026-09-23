from ...Componentes.AbstractComponenteCilindrico import ComponenteCilindrico
from ...Componentes.SecaoTorre import SecaoTorre
from ...Default.Default import tempo_processamento


class Torre(ComponenteCilindrico):
    def __init__(self, secoes_torre):
        self.validar_lista(secoes_torre)
        self._secoes_torre = secoes_torre
        # informacoes para o construtor da classe base
        diametro = self.__calculaDiametroDaBase__(secoes_torre)
        altura = self.__calculaAlturaDaTorre__(secoes_torre)
        massa = self.__calculaMassaDaTorre__(secoes_torre)
        info_componente = {
            # informações da monopile
            # [m]                - TODO: Se for diametro duas informacoes terão o mesmo valor
            "comprimento": diametro,
            "largura": diametro,                            # [m]
            "altura": altura,                               # [m]
            "massa": massa,                                 # [t]
            # [True | False]    - TODO: Normalmente transportada com a base no deck, uma vez que são instaladas nessa posição
            "with_armazenamento_horizontal": False,
            # [True | False]    - TODO: Transportar a monopile deitada exige uma estrutura de suporte especial e aumenta o risco de danos à monopile.
            "with_armazenamento_vertical": True,
            # [True | False]     - TODO: Um tanto improvável o empilhamento por conta do peso e dimensões
            "is_empilhavel": False
        }
        super().__init__(**info_componente)
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_torre"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento["tempo_liberacao_deck_torre"]

    def validar_lista(self, secoes_torre):
        if not (isinstance(secoes_torre, list) and all(isinstance(item, SecaoTorre) for item in secoes_torre)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe SecaoTorre")

    def setTempoAnexarSecaoTorre(self, tempo):
        self._tempo_anexar_secao_torre = tempo

    def getTempoAnexarSecaoTorre(self):
        return self._tempo_anexar_secao_torre

    def __calculaTempoPreMontarTorre__(self):
        tempo = 0
        numeroSecoes = len(self._secoes_torre)
        tempo = (numeroSecoes-1)*self._tempo_anexar_secao_torre
        return tempo

    def __calculaDiametroDaBase__(self, secoes_torre):
        diametro = 0
        for secao in secoes_torre:
            diametro = max(secao.getLargura(), diametro)
        return diametro

    def __calculaAlturaDaTorre__(self, secoes_torre):
        altura_torre = 0
        for secao in secoes_torre:
            altura_torre += secao.getAltura()
        return altura_torre

    def __calculaMassaDaTorre__(self, secoes_torre):
        massa_torre = 0
        for secao in secoes_torre:
            massa_torre += secao.getMassa()
        return massa_torre

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
        return "torre"

    def getTempoPreMontarOnshore(self):
        return self.__calculaTempoPreMontarTorre__()
