import math
from ..MovimentacaoComponente.Guindaste import Guindaste
from ..MovimentacaoComponente.Embarcacao import Embarcacao
from ..MovimentacaoComponente.Rebocador import Rebocador


class ConjuntoRebocadores(Embarcacao):
    def __init__(self, nome, *args):
        self._rebocadores = dict()
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
        velocidadeMinimaVazio = math.inf
        listaRebocadores = args
        for rebocador in listaRebocadores:
            if isinstance(rebocador, Rebocador):
                self._rebocadores[rebocador.getId()] = rebocador
                if (rebocador.getVelocidadeCarregado() < velocidadeMinimaCarregado):
                    velocidadeMinimaCarregado = rebocador.getVelocidadeCarregado()
                if (rebocador.getVelocidadeVazio() < velocidadeMinimaVazio):
                    velocidadeMinimaVazio = rebocador.getVelocidadeVazio()
                somaTaxaDiaria += rebocador.getTaxaDiaria()
                somaTaxaMobilizacao += rebocador.getTaxaMobilizacao()
            else:
                raise KeyError("A classe derivativa deve ser Rebocador.")
        if (len(self._rebocadores) == 0):
            raise KeyError(
                "Deve ser incluído ao menos um rebocador no construtor da classe.")
        return velocidadeMinimaCarregado, velocidadeMinimaVazio, somaTaxaDiaria, somaTaxaMobilizacao

    def calculaNumeroConjuntosCarregaveis(self, kits=None):
        return 1

    def calculaNumeroConjuntosSuportado(self, kits=None):
        return 1

    def getRebocadores(self):
        return self._rebocadores
