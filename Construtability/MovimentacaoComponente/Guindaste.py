from ..Default.Default import guindaste
from ....utils.utils import temp_file


class Guindaste:
    def __init__(self, velocidade=guindaste["velocidade_media_guindaste"], maxima_capacidade=guindaste["maxima_capacidade_guindaste"], maxima_altura=guindaste["altura_maxima_guidaste"], maximo_vento=guindaste["velocidade_maxima_vento_guindaste"]):
        self.velocidade = velocidade  # velocidade do guindaste [m/min]
        self.maxima_altura = maxima_altura  # maxima altura de elevacao [m]
        self.maxima_capacidade = maxima_capacidade  # maxima carga suporta [t]
        # velocidade maxima de vento para operacao [m/s]
        self.maximo_vento = maximo_vento

    def __update__(self, configuracao, **kwargs):
        configuracao.update(**kwargs)
        # self.validar(configuracao)

    def verifica_limite_capacidade(self, massa):
        if not (massa <= self.maxima_capacidade):
            temp = temp_file('limites_operacionais_violados.txt')
            with open(temp, 'a') as f:
                f.write(
                    f"O guindaste nao pode suportar a massa de {massa} toneladas \n")
            return False
        else:
            return True

    def verifica_limite_altura(self, altura):
        if not (altura <= self.maxima_altura):
            temp = temp_file('limites_operacionais_violados.txt')
            with open(temp, 'a') as f:
                f.write(
                    f"O guindaste nao pode suportar a elevacao de {altura} metros \n")
            return False
        else:
            return True

    def verifica_limite_altura_componente(self, componente):
        if not (componente.altura <= self.maxima_altura):
            temp = temp_file('limites_operacionais_violados.txt')
            with open(temp, 'a') as f:
                f.write(
                    f"O guindaste nao pode suportar a elevacao de {componente.altura} metros \n")
            return False
        else:
            return True

    def verifica_limite_velocidade_vento(self, velocidade_vento):
        if not (velocidade_vento <= self.maximo_vento):
            temp = temp_file('limites_operacionais_violados.txt')
            with open(temp, 'a') as f:
                f.write(
                    f"O guindaste nao pode operar com uma velocidade de vento {velocidade_vento} metros por segundo \n")
            return False
        else:
            return True

    def calcular_tempo_movimentacao(self, altura):
        # assume que o tempo de levantar é igual ao tempo de abaixar
        self.verifica_limite_altura(altura)
        if (self.velocidade != 0):
            tempo_movimento = (altura / self.velocidade)/60
        else:
            tempo_movimento = 0
        return tempo_movimento
