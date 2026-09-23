from .Embarcacao import Embarcacao


class Wtiv(Embarcacao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        configuracao = {
            "comprimento_perna_wtiv": None,              # [m]
            "profundidade_maxima_wtiv": None,            # [m]
            "velocidade_abaixo_profundidade_wtiv": None,  # [m/min]
            "velocidade_acima_profundidade_wtiv": None,  # [m/min]
        }
        super().__init__(**kwargs)
        configuracao.update(**kwargs)
        self.comprimento_perna = configuracao["comprimento_perna_wtiv"]
        self.profundidade_maxima = configuracao["profundidade_maxima_wtiv"]
        self.velocidade_abaixo_profundidade = configuracao["velocidade_abaixo_profundidade_wtiv"]
        self.velocidade_acima_profundidade = configuracao["velocidade_acima_profundidade_wtiv"]

    def tempoElevacao(self, extensao, profundidade):
        """
        Calcula o tempo de elevação em HORAS para atingir uma determinada extensão
         a partir de uma profundidade.
        """
        if extensao > self.comprimento_perna:
            raise Exception(
                "Fornecida uma extensão de {} m que é maior que o comprimento da perna para a embarcação de {} m."
                .format(extensao, self.comprimento_perna)
            )

        elif profundidade > self.profundidade_maxima:
            raise Exception(
                "Fornecida uma produndidade de {} m  maior que a profundidade maxima permitida para a embarcação de {} m."
                .format(profundidade, self.profundidade_maxima)
            )

        elif profundidade > extensao:
            raise Exception("A extensão deve ser maior que a profundidade.")

        else:
            return (
                (profundidade/self.velocidade_abaixo_profundidade)
                + ((extensao-profundidade)/self.velocidade_acima__profundidade)
            ) / 60
