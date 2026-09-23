import math
from ..Ferramentas.Area import areaCirculo, areaRetangulo
from ..Componentes.IComponente import Componente
# considera-se como premissa que o componente está deitado na extensao de sua altura
# logo:
# um componente na vertical possuirá uma altura igual a self._altura
# um componente na horizontal possuíra uma altura igual ao maximo entre comprimento e largura


class ComponenteCilindrico(Componente):
    def __init__(self, **kwargs):
        info_componente = {
            # ------------------------------------------------------------------------------------
            # obrigatorios:
            # ------------------------------------------------------------------------------------
            "comprimento": None,                             # [m]
            "largura": None,                                 # [m]
            "altura": None,                                  # [m]
            "massa": None,                                   # [t]
            # ------------------------------------------------------------------------------------
            # opcionais:
            # ------------------------------------------------------------------------------------
            # referente ao armazenamento na horizontal
            "with_armazenamento_horizontal": True,           # [True | False]
            "densidade_area_horizontal": None,               # [t/m2]
            "area_ocupada_horizontal": None,                 # [m2]
            # [m]              - Default: Sem limites (relativo ao comprimento)
            "limites_armazenamento_horizontal": {0, 999999},
            # referente ao armazenamento na vertical
            # [True | False]   - Default: True
            "with_armazenamento_vertical": True,
            # [t/m2]           - Default: Estimado se aplicável
            "densidade_area_vertical": None,
            # [m2]             - Default: Estimado se aplicável
            "area_ocupada_vertical": None,
            # [m]              - Default: Sem limites (relativo a altura)
            "limites_armazenamento_vertical": {0, 999999},
            # referente ao empilhamento
            # [True | False]   - Default: False
            "is_empilhavel": False,
            # [t]              - Default: Null se não empilhavel, caso contrário esse ou o proximo campo obrigatórios
            "capacidade_empilhamento": None,
            # [Integer]        - Default: Null se não empilhavel, caso contrário esse ou o campo anterior obrigatórios
            "maximo_numero_camadas_empilhamento": None
        }

        # atribuir valores das chaves a estrutura criada
        info_componente.update(**kwargs)
        # atualizar dados e fazer consistencia
        self.__update__(info_componente, **kwargs)
        # ----------------------------------------------
        # salvar informacoes nas variaveis:
        # ----------------------------------------------
        self._comprimento = info_componente["comprimento"]
        self._largura = info_componente["largura"]
        self._altura = info_componente["altura"]
        self._massa = info_componente["massa"]
        # ----------------------------------------------
        self._with_armazenamento_horizontal = info_componente["with_armazenamento_horizontal"]
        self._densidade_area_horizontal = info_componente["densidade_area_horizontal"]
        self._area_ocupada_horizontal = info_componente["area_ocupada_horizontal"]
        self._limites_armazenamento_horizontal = info_componente["limites_armazenamento_horizontal"]
        # ------------------------------------------------
        self._with_armazenamento_vertical = info_componente["with_armazenamento_vertical"]
        self._densidade_area_vertical = info_componente["densidade_area_vertical"]
        self._area_ocupada_vertical = info_componente["area_ocupada_vertical"]
        self._limites_armazenamento_vertical = info_componente["limites_armazenamento_vertical"]
        # ------------------------------------------------
        self._is_empilhavel = info_componente["is_empilhavel"]
        self._capacidade_empilhamento = info_componente["capacidade_empilhamento"]
        self._maximo_numero_camadas_empilhamento = info_componente[
            "maximo_numero_camadas_empilhamento"]
        # ------------------------------------------------------

    def __update__(self, info_componente, **kwargs):
        info_componente.update(kwargs)
        info_componente = self.__preencherValores__(info_componente)
        self.__validar__(info_componente)

    def __preencherValores__(self, info_componente):
        if (info_componente["with_armazenamento_horizontal"]):
            if (info_componente["densidade_area_horizontal"] == None):
                info_componente["densidade_area_horizontal"] = self.__estimarDensidadeArea__(
                    info_componente["massa"], info_componente["altura"], max(info_componente["comprimento"], info_componente["largura"]))
            if (info_componente["area_ocupada_horizontal"] == None):
                info_componente["area_ocupada_horizontal"] = self.__estimarAreaOcupada__(
                    info_componente["altura"], max(info_componente["comprimento"], info_componente["largura"]))
        if (info_componente["with_armazenamento_vertical"]):
            if (info_componente["densidade_area_vertical"] == None):
                info_componente["densidade_area_vertical"] = self.__estimarDensidadeArea__(
                    info_componente["massa"], info_componente["comprimento"], info_componente["largura"])
            if (info_componente["area_ocupada_vertical"] == None):
                info_componente["area_ocupada_vertical"] = self.__estimarAreaOcupada__(
                    info_componente["comprimento"], info_componente["largura"])
        return info_componente

    def __validar__(self, info_componente):
        for key, value in info_componente.items():
            if info_componente[key] is None:
                if key not in {"capacidade_empilhamento", "maximo_numero_camadas_empilhamento", "densidade_area_vertical", "area_ocupada_vertical", "densidade_area_horizontal", "area_ocupada_horizontal"}:
                    raise KeyError(
                        "A informação do parâmetro %s é obrigatória." % key)
        if (info_componente["is_empilhavel"] == True):
            if (info_componente["capacidade_empilhamento"] == None) and (info_componente["maximo_numero_camadas_empilhamento"] == None):
                raise KeyError(
                    "A declaração de pelo menos um dos parâmetros capacidade_empilhamento ou maximo_numero_camadas_empilhamento é obrigatória.")
            else:
                if (info_componente["capacidade_empilhamento"] == None):
                    info_componente["capacidade_empilhamento"] = 999999
                elif (info_componente["maximo_numero_camadas_empilhamento"] == None):
                    info_componente["maximo_numero_camadas_empilhamento"] = 999999
        else:
            info_componente["capacidade_empilhamento"] = 0.0
            info_componente["maximo_numero_camadas_empilhamento"] = 0

    def getNumeroComponentesEmpilhaveis(self):
        numero = 0
        if self._is_empilhavel:
            numeroComponentesPorCapacidade = math.floor(
                self._capacidade_empilhamento/self._massa)
            numero = min(numeroComponentesPorCapacidade,
                         self._maximo_numero_camadas_empilhamento)
        return numero

    @staticmethod
    def __estimarAreaOcupada__(comprimento1, comprimento2):
        if comprimento1 == comprimento2:  # componente é cilindrico
            # normalmente os componentes serão cilindricos!
            # calcula a area da base de um cilindro
            diametro = comprimento1
            raio = diametro / 2
            return areaCirculo(raio)
        else:
            return areaRetangulo(comprimento1, comprimento2)

    @staticmethod
    def __estimarDensidadeArea__(massa, comprimento1, comprimento2):
        area = ComponenteCilindrico.__estimarAreaOcupada__(
            comprimento1, comprimento2)
        return massa / area if area > 0 else 0

    def getAreaOcupada(self):
        pass

    def getDensidadeArea(self):
        pass

    def getTempoFixacaoDeck(self):
        pass

    def getAltura(self):
        return self._altura

    def getComprimento(self):
        return self._comprimento

    def getLargura(self):
        return self._largura

    def getMassa(self):
        return self._massa

    def getDiametro(self):
        return self._comprimento

    def admiteArmazenamentoHorizontal(self):
        return self._with_armazenamento_horizontal

    def admiteArmazenamentoVertical(self):
        return self._with_armazenamento_vertical

    def getTipoComponente(self):
        pass
