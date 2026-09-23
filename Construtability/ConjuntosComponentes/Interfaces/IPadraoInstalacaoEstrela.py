from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.Derivados.Estrela import Estrela


class IPadraoInstalacaoEstrela:
    def __init__(self, estrela):
        self.__validarEstrela__(estrela)
        self._estrela = estrela
        self._tempo_anexar_estrela_na_subestrutura = tempo_processamento[
            "tempo_anexar_estrela_na_nacele_offshore"]
        self._liberar_estrela_deck = tempo_processamento["tempo_liberacao_deck_estrela"]

    def __validarEstrela__(self, estrela):
        if not isinstance(estrela, Estrela):
            raise KeyError("A classe derivativa deve ser do tipo Estrela.")

    def setTempoLiberarEstrelaDeck(self, valor):
        self._liberar_estrela_deck = valor

    def getTempoLiberarEstrelaDeck(self):
        return self._liberar_estrela_deck

    def getTempoElevarEstrelaVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarEstrelaNaNacele(self):
        return self._tempo_anexar_estrela_na_nacele

    def setTempoAnexarEstrelaNaNacele(self, valor):
        self._tempo_anexar_estrela_na_nacele = valor

    def criarTarefasInstalacaoEstrela(self, nomeMacroatividade, cronograma, embarcacao, altura):
        nomeTarefa = embarcacao.nomeTarefa()
        tarefa0 = "Liberar a estrela do deck da embarcacao"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa0,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_estrela_deck)
        tarefa1 = "Elevar a estrela na posição vertical "
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self.getTempoElevarEstrelaVertical(embarcacao, altura))
        tarefa2 = "Anexar estrela na nacele"
        cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa2,
                                           TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_estrela_na_subestrutura)
