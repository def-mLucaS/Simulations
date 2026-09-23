from ..Cronograma.Macroatividade import Macroatividade


class Tarefa:
    def __init__(self, nome):
        self.nome = nome
        self.macroatividades = {}

    def adicionarMacroatividade(self, nome):
        if nome not in self.macroatividades:
            self.macroatividades[nome] = Macroatividade(nome)

    def getMacroatividade(self, nome):
        if nome in self.macroatividades:
            return self.macroatividades[nome]
        else:
            raise KeyError(
                "A chave consultada nao está na lista de macroatividades.")
