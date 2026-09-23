from ..ConjuntosComponentes.Interfaces.IConjuntoAerogerador import IConjuntoAerogerador
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoTorre import IPadraoInstalacaoTorre
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoHubNacele import IPadraoInstalacaoHubNacele
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoPas import IPadraoInstalacaoPas


class ConjuntoAerogeradorMetodo2(IConjuntoAerogerador, IPadraoInstalacaoTorre, IPadraoInstalacaoHubNacele, IPadraoInstalacaoPas):
    def __init__(self, id, torre, nacele, hub, pa1, pa2, pa3):
        IPadraoInstalacaoTorre.__init__(self, torre)
        IPadraoInstalacaoHubNacele.__init__(self, hub, nacele)
        IPadraoInstalacaoPas.__init__(self, pa1, pa2, pa3)
        IConjuntoAerogerador.__init__(self, id)

    def __criarComponentes__(self):
        args = (self._torre, self._hubNacele,
                self._pas[0], self._pas[1], self._pas[2])
        return args

    def executarInstalacao(self, cronograma, dataInicio, embarcacao):
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação aerogerador de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        self.criarTarefasInstalacaoTorre(
            nomeMacroatividade, cronograma, embarcacao)
        altura = self.getAlturaTorre()
        self.criarTarefasInstalacaoHubNacele(
            nomeMacroatividade, cronograma, embarcacao, altura)
        self.criarTarefasInstalacaoPas(
            nomeMacroatividade, cronograma, embarcacao, altura)
        # Executando
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao
