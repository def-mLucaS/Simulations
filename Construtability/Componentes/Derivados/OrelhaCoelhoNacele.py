import math
from ...Componentes.AbstractComponenteRetangular import ComponenteRetangular
from ...Componentes.Nacele import Nacele
from ...Componentes.Hub import Hub
from ...Componentes.Pa import Pa
from ...Default.Default import tempo_processamento, parametros


class OrelhaCoelhoNacele(ComponenteRetangular):
    # A orelha fica em pé formando um V, a area ocupada se refere ao comprimento no V no deck da embarcação
    # pela largura da soma do diametro da pa com a altura do hub e largura da nacele
    def __init__(self, hub, nacele, pa1, pa2, percentualPaContidaDeck=parametros["percentual_comprimento_pa_dentro_deck"]):
        self.__validarDados__(hub, nacele, pa1, pa2)
        self._nacele = nacele
        self._hub = hub
        self._pa1 = pa1
        self._pa2 = pa2
        # informacoes para o construtor da classe base
        self.percentualPaContidaDeck = percentualPaContidaDeck
        comprimento = self.__calcularComprimentoOrelhaCoelhoNacele__(
            hub, nacele, pa1, pa2, percentualPaContidaDeck)
        largura = self.__calcularLarguraOrelhaCoelhoNacele__(hub, nacele)
        # a altura de movimentacao considera é a da nacele
        altura = self._nacele.getAltura()
        massa = self.__calcularMassaOrelhaCoelhoNacele__(hub, nacele, pa1, pa2)
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
        self._tempo_fixacao_deck_embarcacao = tempo_processamento[
            "tempo_fixacao_deck_orelha_coelho_nacele"]
        self._tempo_liberacao_deck_embarcacao = tempo_processamento[
            "tempo_liberacao_deck_orelha_coelho_nacele"]

    def __validarDados__(self, hub, nacele, pa1, pa2):
        if not (isinstance(pa1, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")
        if not (isinstance(pa2, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")
        if not (isinstance(hub, Hub)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe Hub.")
        if not (isinstance(nacele, Nacele)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe Nacele.")

    def __calculaLadoTriangulo__(self, hub, pa1, pa2, percentualPaContidaDeck):
        extensaoPa = percentualPaContidaDeck * \
            max(pa1.getAltura(), pa2.getAltura())
        extensaoHub = hub.getDiametro() / 2
        raioTriangulo = extensaoPa + extensaoHub
        # Como as pas formam entre si angulos de 120 graus podemos deduzir a seguinte relacao
        # pode-se calcular o lado horizontal do triangulo com angulo de 30 graus
        ladoTriangulo = (math.sqrt(3)/2) * (raioTriangulo)
        return ladoTriangulo

    def __calcularLarguraOrelhaCoelhoNacele__(self, hub, nacele):
        largura = hub.getAltura()+nacele.getLargura()
        return largura

    def __calcularComprimentoOrelhaCoelhoNacele__(self, hub, nacele, pa1, pa2, percentualPaContidaDeck):
        ladoTriangulo = self.__calculaLadoTriangulo__(
            hub, pa1, pa2, percentualPaContidaDeck)
        comprimento = max(2*ladoTriangulo, nacele.getComprimento())
        return comprimento

    def __calcularMassaOrelhaCoelhoNacele__(self, hub, nacele, pa1, pa2):
        massa_orelha_coelho_nacele = hub.getMassa() + nacele.getMassa() + \
            pa1.getMassa() + pa2.getMassa()
        return massa_orelha_coelho_nacele

    def getTempoFixacaoDeck(self):
        return self._tempo_fixacao_deck_embarcacao

    def setTempoFixacaoDeck(self, tempo):
        self._tempo_fixacao_deck_embarcacao = tempo

    def getTempoLiberacaoDeck(self):
        return self._tempo_liberacao_deck_embarcacao

    def setTempoLiberacaoDeck(self, tempo):
        self._tempo_liberacao_deck_embarcacao = tempo

    def getTipoComponente(self):
        return "orelha_coelho_nacele"

    def getTempoAnexarHubNacele(self):
        return self._tempo_anexar_hub_nacele

    def setTempoAnexarHubNacele(self, tempo):
        self._tempo_anexar_hub_nacele = tempo

    def getTempoAnexarPaHub(self):
        return self._tempo_anexar_pa_hub

    def setTempoAnexarPaHub(self, tempo):
        self._tempo_anexar_pa_hub = tempo

    def getPercentualComprimentoPaDentroDeck(self):
        return self.percentualPaContidaDeck

    def getTempoPreMontarOnshore(self):
        tempo = self._tempo_anexar_hub_nacele + 2 * self._tempo_anexar_pa_hub
        return tempo
