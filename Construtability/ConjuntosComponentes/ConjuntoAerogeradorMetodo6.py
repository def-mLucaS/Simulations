from ..ConjuntosComponentes.Interfaces.IConjuntoAerogerador import IConjuntoAerogerador
from ..ConjuntosComponentes.Interfaces.IPadraoInstalacaoAerogedorCompleto import IPadraoInstalacaoAerogeradorCompleto


class ConjuntoAerogeradorMetodo6(IConjuntoAerogerador, IPadraoInstalacaoAerogeradorCompleto):
    def __init__(self, id, aerogerador_completo):
        IPadraoInstalacaoAerogeradorCompleto.__init__(
            self, aerogerador_completo)
        IConjuntoAerogerador.__init__(self, id)

    def __criarComponentes__(self):
        args = (self._aerogerador_completo,)
        return args

    def executarInstalacao(self, cronograma, dataInicio, embarcacao):
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação aerogerador de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        self.criarTarefasInstalacaoAerogeradorCompleto(
            nomeMacroatividade, cronograma, embarcacao)
        # Executando
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)
        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)
        return dataFimExecucao
