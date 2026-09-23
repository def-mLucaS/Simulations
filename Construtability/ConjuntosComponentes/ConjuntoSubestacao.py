from ..ConjuntosComponentes.ConjuntoComponentes import ConjuntoComponentes
from ..Componentes.SubestacaoOffshore import SubestacaoOffshore
from ..Cronograma.Cronograma import TipoMicroatividade


class ConjuntoSubestacao(ConjuntoComponentes):
    def __init__(self, id, subestacao):
        self._id = id
        args = (subestacao,)
        self._subestacao = subestacao
        # tem que fazer um assert se o tipo é subestacao
        super().__init__(*args)

    def executarInstalacao(self, cronograma, embarcacao, dataInicio):
        nomeTarefa = embarcacao.nomeTarefa()
        nomeMacroatividade = "Instalação caixa da subestação offshore de id " + \
            str(self._id) + " relativa a viagem " + \
            str(embarcacao.getNumeroViagem())
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacroatividade)
        # Inserindo microatividades
        #
        tarefa1 = "Liberar a caixa da subestação do deck da embarcacao"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_SUBESTACAO, self._subestacao.getTempoLiberacaoDeck())
        #
        tarefa2 = "Elevar a caixa da subestação na posição vertical"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_SUBESTACAO, self._subestacao.getTempoElevarSubestacaoVertical(embarcacao))
        #
        tarefa3 = "Fixar a caixa da subestação na fundação"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa3,
                                           TipoMicroatividade.INSTALACAO_SUBESTACAO, self._subestacao.getTempoAnexarSubestacaoNaFundacao())
        #
        cronograma.executarMacroatividade(
            nomeTarefa, nomeMacroatividade, dataInicio)

        dataFimExecucao = cronograma.getDataFimMacroatividade(
            nomeTarefa, nomeMacroatividade)

        return dataFimExecucao

    def getId(self):
        return self._id
