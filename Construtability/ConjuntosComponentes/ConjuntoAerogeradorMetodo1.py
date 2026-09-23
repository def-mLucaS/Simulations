from ..ConjuntosComponentes.Interfaces.IConjuntoAerogerador import IConjuntoAerogerador
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoSecoesTorre import IPadraoInstalacaoSecoesTorre
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoHubNacele import IPadraoInstalacaoHubNacele
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoPas import IPadraoInstalacaoPas


class ConjuntoAerogeradorMetodo1(IConjuntoAerogerador, IPadraoInstalacaoSecoesTorre, IPadraoInstalacaoHubNacele, IPadraoInstalacaoPas):
    def __init__(self, id, secoes_torre, nacele, hub, pa1, pa2, pa3):
        IPadraoInstalacaoSecoesTorre.__init__(self, secoes_torre)
        IPadraoInstalacaoHubNacele.__init__(self, hub, nacele)
        IPadraoInstalacaoPas.__init__(self, pa1, pa2, pa3)
        IConjuntoAerogerador.__init__(self, id)

    def __criarComponentes__(self):
        args = (self._hubNacele, self._pas[0], self._pas[1], self._pas[2])
        for secao in self._secoes_torre:
            args += (secao,)  # Adiciona a secao a tupla args
        return args

    def executarInstalacao(self, cronograma, dataInicio, embarcacao):
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação aerogerador de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        self.criarTarefasInstalacaoSecoesTorre(
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
