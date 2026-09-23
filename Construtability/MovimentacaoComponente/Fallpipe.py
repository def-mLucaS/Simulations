from .Embarcacao import Embarcacao


class Fallpipe(Embarcacao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        configuracao = {
            "capacidade_max": None,              # [m³]
            "capacidade_instalacao": None,       # [t/h]
            "tempo_tacar_pedra": None,
            "lista_tempo_deslocamento": None
        }
        super().__init__(**kwargs)
        configuracao.update(**kwargs)
        self.capacidade_max = configuracao["capacidade_max"]
        self.capacidade_instalacao = configuracao["capacidade_instalacao"]
        self.tempo_tacar_pedra = configuracao["tempo_tacar_pedra"]
        self.lista_tempo_deslocamento = configuracao["lista_tempo_deslocamento"]

    def getCapacidadeMax(self):
        return self.capacidade_max

    def getCapacidadeInstalacao(self):
        return self.capacidade_instalacao

    def setCapacidadeInstalacao(self, capacidade_instalacao):
        self.capacidade_instalacao = capacidade_instalacao

    def getTempoTacarPedra(self):
        return self.tempo_tacar_pedra

    def getListaTempoDeslocamento(self):
        return self.lista_tempo_deslocamento

    def setListaTempoDeslocamento(self, lista_tempo_deslocamento):
        self.lista_tempo_deslocamento = lista_tempo_deslocamento
