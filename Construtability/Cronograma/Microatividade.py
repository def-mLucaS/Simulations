from datetime import datetime

class Microatividade:
    def __init__(self, nomeMicroatividade, tipo, duracao):
        self.nome = nomeMicroatividade
        self.duracao = float(duracao)
        self.tipo = tipo
        self.dataInicio = None
        self.dataFim = None

    def setDataInicio(self, dataInicio):
        if not isinstance(dataInicio, datetime):
            raise KeyError("A dataInicio nao é do tipo datetime.")
        self.dataInicio = dataInicio

    def setDataFim(self, dataFim):
        self.dataFim = dataFim

    def setTipo(self,tipo):
        self.tipo = tipo
