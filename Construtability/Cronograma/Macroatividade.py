from datetime import datetime, timedelta
from ..Cronograma.Microatividade import Microatividade


class Macroatividade:
    def __init__(self, nome):
        self.nome = nome
        self.dataInicio = None
        self.dataAtual = None
        self.dataFim = None
        self.microatividades = []

    def adicionarMicroatividade(self, nome, tipo, duracao):
        self.microatividades.append(Microatividade(nome, tipo, duracao))

    def executarAtividades(self, dataInicio):
        if not isinstance(dataInicio, datetime):
            raise KeyError("A dataInicio não é do tipo datetime.")
        self.dataInicio = dataInicio
        self.dataAtual = self.dataInicio
        for microatividade in self.microatividades:
            microatividade.setDataInicio(self.dataAtual)
            if not isinstance(microatividade.duracao, (int, float)):
                raise ValueError("A duração deve ser um número (int ou float). Na microatividade " + str(
                    microatividade.nome) + " com valor " + str(microatividade.duracao) + ".")
            self.dataAtual += timedelta(hours=microatividade.duracao)
            microatividade.setDataFim(self.dataAtual)
        self.dataFim = self.dataAtual
