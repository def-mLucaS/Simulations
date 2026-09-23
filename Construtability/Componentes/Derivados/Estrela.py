import math
from ...Componentes.AbstractComponenteTriangular import ComponenteTriangular
from ...Componentes.Hub import Hub
from ...Componentes.Pa import Pa
from ...Default.Default import tempo_processamento, parametros


class Estrela(ComponenteTriangular):
    def __init__(self, hub, pa1, pa2, pa3, percentualPaContidaDeck=parametros["percentual_comprimento_pa_dentro_deck"]):
        self.__validarDados__(hub, pa1, pa2, pa3)
        self._hub = hub
        self._pa1 = pa1
        self._pa2 = pa2
        self._pa3 = pa3
        # informacoes para o construtor da classe base
        self.percentualPaContidaDeck = percentualPaContidaDeck
        altura = self.__calculaAlturaEstrela__(hub, pa1, pa2, pa3)
        massa = self.__calculaMassaEstrela__(hub, pa1, pa2, pa3)
        ladoTriangulo = self.__calculaLadoTriangulo__(
            hub, pa1, pa2, pa3, self.percentualPaContidaDeck)
        super().__init__(ladoTriangulo, ladoTriangulo, ladoTriangulo, altura, massa)
        self._tempo_fixacao_deck_embarcacao = tempo_processamento["tempo_fixacao_deck_estrela"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento["tempo_liberacao_deck_estrela"]

    def __validarDados__(self, hub, pa1, pa2, pa3):
        if not (isinstance(hub, Hub)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe Hub.")
        if not (isinstance(pa1, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")
        if not (isinstance(pa2, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")
        if not (isinstance(pa3, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")

    def __calculaLadoTriangulo__(self, hub, pa1, pa2, pa3, percentualPaContidaDeck):
        extensaoPa = percentualPaContidaDeck * \
            max(pa1.getAltura(), pa2.getAltura(), pa3.getAltura())
        extensaoHub = hub.getDiametro()/2
        raioTriangulo = extensaoPa+extensaoHub
        # Como as pas formam entre si angulos de 120 graus podemos deduzir a seguinte relacao
        ladoTriangulo = math.sqrt(3)*(raioTriangulo)
        return ladoTriangulo

    def __calculaAlturaEstrela__(self, hub, pa1, pa2, pa3):
        altura_estrela = hub.getAltura() + max(pa1.getDiametro(),
                                               pa2.getDiametro(), pa3.getDiametro())
        return altura_estrela

    def __calculaMassaEstrela__(self, hub, pa1, pa2, pa3):
        massa_estrela = hub.getMassa() + pa1.getMassa() + pa2.getMassa() + pa3.getMassa()
        return massa_estrela

    def getTempoFixacaoDeck(self):
        return self._tempo_fixacao_deck_embarcacao

    def setTempoFixacaoDeck(self, tempo):
        self._tempo_fixacao_deck_embarcacao = tempo

    def getTempoLiberacaoDeck(self):
        return self._tempo_liberacao_deck_embarcacao

    def setTempoLiberacaoDeck(self, tempo):
        self._tempo_liberacao_deck_embarcacao = tempo

    def getTipoComponente(self):
        return "estrela"

    def getTempoAnexarPaHub(self):
        return self._tempo_anexar_pa_hub

    def setTempoAnexarPaHub(self, tempo):
        self._tempo_anexar_pa_hub = tempo

    def getPercentualComprimentoPaDentroDeck(self):
        return self.percentualPaContidaDeck

    def getTempoPreMontarOnshore(self):
        tempo = 3*self._tempo_anexar_pa_hub
        return tempo
