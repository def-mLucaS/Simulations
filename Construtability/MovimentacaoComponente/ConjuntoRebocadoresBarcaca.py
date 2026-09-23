import math
from ..MovimentacaoComponente.Guindaste import Guindaste
from .Embarcacao import Embarcacao
from .Rebocador import Rebocador
from .Barcaca import Barcaca


class ConjuntoRebocadoresBarcaca(Embarcacao):
    def __init__(self, nome, *args):
        self._rebocadores = dict()
        self._barcaca = None
        velocidade_locomocao_carregado, velocidade_locomocao_vazio, taxa_diaria, taxa_mobilizacao = self.__leitura__(
            *args)
        # criado guindaste fictício que nao altera o processo (conjunto de rebocadores nao usa guindaste)
        # (velocidade [m/min] , maxima_capacidade [t], maxima_altura [m])
        guindaste = Guindaste(0.0, 99999, 99999)
        configuracao = {
            "nome": nome,  # [m]
            "area_deck_livre": 99999,  # [m2]
            "maxima_capacidade_carga_deck": 99999,  # [t/m2]
            "taxa_diaria": taxa_diaria,  # [$]
            "taxa_mobilizacao": taxa_mobilizacao,  # [$]
            "velocidade_locomocao_carregado": velocidade_locomocao_carregado,
            "velocidade_locomocao_vazio": velocidade_locomocao_vazio,
            # limites operacionais
            "guindaste": guindaste
        }
        super().__init__(**configuracao)

    def __leitura__(self, *args):
        somaTaxaDiaria = 0.0
        somaTaxaMobilizacao = 0.0
        # velocidade minima no conjunto de rebocadores
        velocidadeMinimaCarregado = math.inf
        velocidadeMinimaVazio = math.inf  # velocidade minima no conjunto de rebocadores
        listaEmbarcacoes = args
        contaBarcaca = 0
        for item in listaEmbarcacoes:
            if isinstance(item, Rebocador):
                self._rebocadores[item.getId()] = item
                somaTaxaDiaria += item.getTaxaDiaria()
                somaTaxaMobilizacao += item.getTaxaMobilizacao()
                if (item.getVelocidadeCarregado() < velocidadeMinimaCarregado):
                    velocidadeMinimaCarregado = item.getVelocidadeCarregado()
                if (item.getVelocidadeVazio() < velocidadeMinimaVazio):
                    velocidadeMinimaVazio = item.getVelocidadeVazio()
            elif isinstance(item, Barcaca):
                self._barcaca = item
                somaTaxaDiaria += item.getTaxaDiaria()
                somaTaxaMobilizacao += item.getTaxaMobilizacao()
                if (item.getVelocidadeCarregado() < velocidadeMinimaCarregado):
                    velocidadeMinimaCarregado = item.getVelocidadeCarregado()
                if (item.getVelocidadeVazio() < velocidadeMinimaVazio):
                    velocidadeMinimaVazio = item.getVelocidadeVazio()
                contaBarcaca += 1
            else:
                raise KeyError(
                    "A classe derivativa deve ser Rebocador ou Barcaca.")
        if (contaBarcaca != 1):
            raise KeyError(
                "Deve ser incluida uma barcaca no construtor da classe.")
        if (len(self._rebocadores) == 0):
            raise KeyError(
                "Deve ser incluido ao menos um rebocador no construtor da classe.")
        return velocidadeMinimaCarregado, velocidadeMinimaVazio, somaTaxaDiaria, somaTaxaMobilizacao

    def calculaNumeroConjuntosCarregaveis(self, kits=None):
        return 1

    def calculaNumeroConjuntosSuportado(self, kits=None):
        return 1

    def getRebocadores(self):
        return self._rebocadores
