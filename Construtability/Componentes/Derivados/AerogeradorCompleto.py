from ...Componentes.AbstractComponenteCilindrico import ComponenteCilindrico
from ...Componentes.SecaoTorre import SecaoTorre
from ...Componentes.Nacele import Nacele
from ...Componentes.Hub import Hub
from ...Componentes.Pa import Pa
from ...Default.Default import tempo_processamento


class AerogeradorCompleto(ComponenteCilindrico):
    def __init__(self, secoes_torre, hub, nacele, pa1, pa2, pa3):
        self.__validarDados__(secoes_torre, hub, nacele, pa1, pa2, pa3)
        self._secoes_torre = secoes_torre
        self._hub = hub
        self._nacele = nacele
        self._pa1 = pa1
        self._pa2 = pa2
        self._pa3 = pa3
        # informacoes para o construtor da classe base
        diametro = self.__calcularDiametroDaBase__(secoes_torre)
        altura = self.__calcularAltura__(secoes_torre, nacele)
        massa = self.__calcularMassa__(
            secoes_torre, hub, nacele, pa1, pa2, pa3)
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

    def __validarDados__(self, secoes_torre, hub, nacele, pa1, pa2, pa3):
        if not (isinstance(secoes_torre, list) and all(isinstance(item, SecaoTorre) for item in secoes_torre)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe SecaoTorre.")
        if not (isinstance(hub, Hub)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe Hub.")
        if not (isinstance(nacele, Nacele)):
            raise KeyError(
                "Deve ser dada uma lista com objetos da classe Nacele.")
        if not (isinstance(pa1, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")
        if not (isinstance(pa2, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")
        if not (isinstance(pa3, Pa)):
            raise KeyError("Deve ser dada uma lista com objetos da classe Pa.")

    def setTempoAnexarSecaoTorre(self, tempo):
        self._tempo_anexar_secao_torre = tempo

    def getTempoAnexarSecaoTorre(self, tempo):
        return self._tempo_anexar_secao_torre

    def getTempoAnexarHubNacele(self):
        return self._tempo_anexar_hub_nacele

    def setTempoAnexarHubNacele(self, tempo):
        self._tempo_anexar_hub_nacele = tempo

    def getTempoAnexarPaHub(self):
        return self._tempo_anexar_pa_hub

    def setTempoAnexarPaHub(self, tempo):
        self._tempo_anexar_pa_hub = tempo

    def __calculaTempoPreMontarAerogeradorCompleto__(self):
        tempo = 0
        # torre
        numeroSecoes = len(self._secoes_torre)
        tempo = (numeroSecoes-1)*self._tempo_anexar_secao_torre
        # nacele
        tempo += self._tempo_anexar_nacele_torre
        # hub
        tempo += self._tempo_anexar_hub_nacele
        # pas
        tempo += 3*self._tempo_anexar_pa_hub
        return tempo

    def __calcularDiametroDaBase__(self, secoes_torre):
        diametro = 0
        for secao in secoes_torre:
            diametro = max(secao.getLargura(), diametro)
        return diametro

    def __calcularAltura__(self, secoes_torre, nacele):
        altura = 0
        for secao in secoes_torre:
            altura += secao.getAltura()
        altura += nacele.getAltura()
        return altura

    def __calcularMassa__(self, secoes_torre, hub, nacele, pa1, pa2, pa3):
        massa = 0
        for secao in secoes_torre:
            massa += secao.getMassa()
        massa += hub.getMassa() + nacele.getMassa() + pa1.getMassa() + \
            pa2.getMassa() + pa3.getMassa()
        return massa

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
        return "aerogerador_completo"

    def getTempoPreMontarOnshore(self):
        return self.__calculaTempoPreMontarAerogeradorCompleto__()
