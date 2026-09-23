import math
from ..MovimentacaoComponente.Embarcacao import Embarcacao
from ..Default.Default import tempo_processamento
from ..Cronograma.Cronograma import TipoMicroatividade


class CableVessel(Embarcacao):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tempo_carregar_cabo_porto = tempo_processamento["tempo_carregar_cabo_porto"]

    def calculaNumeroConjuntosSuportado(self, conjuntoComponentes):
        # reescrevendo a funcao considerando apenas a capacidade de carga
        capacidadeCarga = self._maxima_capacidade_carga_deck * self._area_deck
        massaConjunto = conjuntoComponentes.getMassaTotal()
        numeroConjuntos = math.floor(capacidadeCarga / massaConjunto)
        if (numeroConjuntos == 0.0):
            raise ValueError(
                "Não existe capacidade disponível para movimentar o conjunto de componentes na embarcação " + self._nome + ". Capacidade da embarcação " + str(capacidadeCarga) + ". Massa do conjunto de componentes  " + str(massaConjunto) + ".")
        else:
            return numeroConjuntos

    def getTempoCarregarCaboPorto(self):
        return self._tempo_carregar_cabo_porto

    def setTempoCarregarCaboPorto(self, valor):
        self._tempo_carregar_cabo_porto = valor

    def carregarConjuntoComponentes(self, cronograma, conjuntosTransportados, turbinasDeck):
        dataInicio = self._dataAtual
        # Carregar embarcação
        for id in conjuntosTransportados:
            print("Carregando na embarcação o componente ", id)
            self.addKitNoDeck(conjuntosTransportados[id])
            componentes = conjuntosTransportados[id].getListaComponentes()
            # dataFim = self.carregarComponentes(cronograma,componentes,id, dataInicio)
            # dataInicio = dataFim
        self.conjuntosTransportados = conjuntosTransportados
        self.turbinasDeck = turbinasDeck
        #
        nomeMacro = "Carregar cabos no porto na embarcação " + \
            str(self.getNome()) + " - Viagem " + str(self.getNumeroViagem())
        cronograma.adicionarMacroatividade(self.nomeTarefa(), nomeMacro)
        nomeMicro1 = "Carregar cabos"
        duracao1 = self.getTempoCarregarCaboPorto()
        cronograma.adicionarMicroatividade(
            self.nomeTarefa(), nomeMacro, nomeMicro1, TipoMicroatividade.PORTO, duracao1)
        print(" ")
        print("Tarefa: ", self.nomeTarefa())
        print("Macroatividade: ", nomeMacro)
        print("Atividade: ", nomeMicro1)
        print("Duracao: ", duracao1)
        #
        cronograma.executarMacroatividade(
            self.nomeTarefa(), nomeMacro, dataInicio)
        dataFim = cronograma.getDataFimMacroatividade(
            self.nomeTarefa(), nomeMacro)
        print("Data inicio: ", dataInicio)
        print("Data fim: ", dataFim)
        #

        # Salva informacoes da embarcacao alimentadora
        dataInicio = dataFim
        self._dataAtual = dataFim
        return dataFim
