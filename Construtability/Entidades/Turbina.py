from ..Entidades.PontoInstalacao import PontoInstalacao


class Turbina(PontoInstalacao):
    def __init__(self, id, latitude, longitude, profundidade):
        super().__init__(id, latitude, longitude, profundidade)
