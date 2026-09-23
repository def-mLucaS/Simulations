from ..ConjuntosComponentes.Interfaces.IConjuntoAerogerador import IConjuntoAerogerador
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoSecoesTorre import IPadraoInstalacaoSecoesTorre
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoNacele import IPadraoInstalacaoNacele
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoEstrela import IPadraoInstalacaoEstrela


class ConjuntoAerogeradorMetodo3(IConjuntoAerogerador, IPadraoInstalacaoSecoesTorre, IPadraoInstalacaoNacele, IPadraoInstalacaoEstrela):
    def __init__(self, id, secoes_torre, nacele, estrela):
        IPadraoInstalacaoSecoesTorre.__init__(self, secoes_torre)
        IPadraoInstalacaoNacele.__init__(self, nacele)
        IPadraoInstalacaoEstrela.__init__(self, estrela)
        IConjuntoAerogerador.__init__(self, id)

    def __criarComponentes__(self):
        args = (self._nacele, self._estrela)
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
        self.criarTarefasInstalacaoNacele(
            nomeMacroatividade, cronograma, embarcacao, altura)
        self.criarTarefasInstalacaoEstrela(
            nomeMacroatividade, cronograma, embarcacao, altura)
        # Executando
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao
