from ...Componentes.AbstractComponenteRetangular import ComponenteRetangular
from ...Componentes.Hub import Hub
from ...Componentes.Nacele import Nacele
from ...Default.Default import tempo_processamento


class HubNacele(ComponenteRetangular):
    def __init__(self, hub, nacele):
        self._nacele = nacele
        self._hub = hub
        self.__validarDados__(hub, nacele)
        # informacoes para o construtor da classe base
        comprimento = nacele.getComprimento()
        largura = nacele.getLargura()
        altura = nacele.getAltura() + hub.getAltura()
        massa = nacele.getMassa() + hub.getMassa()
        info_componente = {
            # informações da monopile
            # [m]                - TODO: Se for diametro duas informacoes terão o mesmo valor
            "comprimento": comprimento,
            "largura": largura,                            # [m]
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
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_hub_nacele"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento[
            "tempo_liberacao_deck_hub_nacele"]

    def __validarDados__(self, hub, nacele):
        if not (isinstance(nacele, Nacele)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe Nacele.")
        if not (isinstance(hub, Hub)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe Hub.")

    def getTempoFixacaoDeck(self):
        return self._tempo_fixacao_deck_embarcacao

    def setTempoFixacaoDeck(self, tempo):
        self._tempo_fixacao_deck_embarcacao = tempo

    def getTempoLiberacaoDeck(self):
        return self._tempo_liberacao_deck_embarcacao

    def setTempoLiberacaoDeck(self, tempo):
        self._tempo_liberacao_deck_embarcacao = tempo

    def getTipoComponente(self):
        return "hub + nacele"

    def getTempoAnexarHubNacele(self):
        return self._tempo_anexar_hub_nacele

    def setTempoAnexarHubNacele(self, tempo):
        self._tempo_anexar_hub_nacele = tempo

    def getNacele(self):
        return self._nacele

    def getHub(self):
        return self._hub

    def getTempoPreMontarOnshore(self):
        tempo = self._tempo_anexar_hub_nacele
        return tempo
