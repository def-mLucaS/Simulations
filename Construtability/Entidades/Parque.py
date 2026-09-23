from datetime import datetime, timedelta


class Parque():
    def __init__(self, nome, dataInicioInstalacao, planta):
        if not isinstance(dataInicioInstalacao, datetime):
            raise KeyError("A dataInicio nao é do tipo datetime.")
        self._nome = nome
        self._dataInicioInstalacao = dataInicioInstalacao
        self._planta = planta

    def getNome(self):
        return self._nome

    def getDataInicioInstalacao(self):
        return self._dataInicioInstalacao

    def getPlanta(self):
        return self._planta
