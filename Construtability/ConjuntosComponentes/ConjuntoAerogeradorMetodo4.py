from ..ConjuntosComponentes.Interfaces.IConjuntoAerogerador import IConjuntoAerogerador
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoSecoesTorre import IPadraoInstalacaoSecoesTorre
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoOrelhaCoelhoNacele import IPadraoInstalacaoOrelhaCoelhoNacele
from .Interfaces.IPadraoInstalacaoPa import IPadraoInstalacaoPa


class ConjuntoAerogeradorMetodo4(IConjuntoAerogerador, IPadraoInstalacaoSecoesTorre, IPadraoInstalacaoOrelhaCoelhoNacele, IPadraoInstalacaoPa):
    def __init__(self, id, secoes_torre, orelha_coelho, pa):
        IPadraoInstalacaoSecoesTorre.__init__(self, secoes_torre)
        IPadraoInstalacaoOrelhaCoelhoNacele.__init__(self, orelha_coelho)
        IPadraoInstalacaoPa.__init__(self, pa)
        IConjuntoAerogerador.__init__(self, id)

    def __criarComponentes__(self):
        args = (self._orelha_coelho, self._pa)
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
