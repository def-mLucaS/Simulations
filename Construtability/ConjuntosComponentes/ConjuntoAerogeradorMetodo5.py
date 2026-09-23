from ..ConjuntosComponentes.Interfaces.IConjuntoAerogerador import IConjuntoAerogerador
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoTorre import IPadraoInstalacaoTorre
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoOrelhaCoelhoNacele import IPadraoInstalacaoOrelhaCoelhoNacele
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoPa import IPadraoInstalacaoPa


class ConjuntoAerogeradorMetodo5(IConjuntoAerogerador, IPadraoInstalacaoTorre, IPadraoInstalacaoOrelhaCoelhoNacele, IPadraoInstalacaoPa):
    def __init__(self, id, torre, orelha_coelho, pa):
        IPadraoInstalacaoTorre.__init__(self, torre)
        IPadraoInstalacaoOrelhaCoelhoNacele.__init__(self, orelha_coelho)
        IPadraoInstalacaoPa.__init__(self, pa)
        IConjuntoAerogerador.__init__(self, id)

    def __criarComponentes__(self):
        args = (self._torre, self._orelha_coelho, self._pa)
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
        self.criarTarefasInstalacaoOrelhaCoelho(
            nomeMacroatividade, cronograma, embarcacao, altura)
        self.criarTarefasInstalacaoPa(
            nomeMacroatividade, cronograma, embarcacao, altura)
        # Executando
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao
