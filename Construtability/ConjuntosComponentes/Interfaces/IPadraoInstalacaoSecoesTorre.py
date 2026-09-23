from ...Default.Default import tempo_processamento
from ...Cronograma.Cronograma import TipoMicroatividade
from ...Componentes.SecaoTorre import SecaoTorre


class IPadraoInstalacaoSecoesTorre:
    def __init__(self, secoes_torre):
        self.__validarSecoesTorre__(secoes_torre)
        self._secoes_torre = self.__ordenarSecoesTorre__(secoes_torre)
        self._tempo_anexar_secao_torre_na_subestrutura = tempo_processamento[
            "tempo_anexar_secao_torre_na_subestrutura_offshore"]
        self._tempo_anexar_secao_torre = tempo_processamento[
            "tempo_anexar_secao_torre_na_torre_offshore"]
        self._liberar_secao_torre_deck = tempo_processamento["tempo_liberacao_deck_secao_torre"]

    def __validarSecoesTorre__(self, secoes_torre):
        if not isinstance(secoes_torre, list) and all(isinstance(item, SecaoTorre) for item in secoes_torre):
            raise KeyError(
                "A classe derivativa deve do tipo list[SecaoTorre].")

    def __ordenarSecoesTorre__(self, secoes_torre):
        # Ordenar a lista com base no diametro usando a função sorted e a função lambda
        # do maior para o menor
        return sorted(secoes_torre, key=lambda x: x.getDiametro(), reverse=True)

    def setTempoLiberarSecaoTorreDeck(self, valor):
        self._liberar_secao_torre_deck = valor

    def getTempoLiberarSecaoTorreDeck(self):
        return self._liberar_secao_torre_deck

    def getTempoElevarSecaoTorreVertical(self, embarcacao, altura):
        return embarcacao.getGuindaste().calcular_tempo_movimentacao(altura)

    def getTempoAnexarSecaoTorreNaSubestrutura(self):
        return self._tempo_anexar_secao_torre_na_subestrutura

    def setTempoAnexarSecaoTorreNaSubestrutura(self, valor):
        self._tempo_anexar_secao_torre_na_subestrutura = valor

    def setTempoAnexarSecaoTorre(self, tempo):
        self._tempo_anexar_secao_torre = tempo

    def getTempoAnexarSecaoTorre(self):
        return self._tempo_anexar_secao_torre

    def criarTarefasInstalacaoSecoesTorre(self, nomeMacroatividade, cronograma, embarcacao):
        nomeTarefa = embarcacao.nomeTarefa()
        numeroSecao = 0
        alturaElevacao = 0
        for secao_torre in self._secoes_torre:
            numeroSecao += 1
            tarefa0 = "Liberar a seção de torre " + \
                str(numeroSecao) + " do deck da embarcacao"
            cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa0,
                                               TipoMicroatividade.INSTALACAO_AEROGERADOR, self._liberar_secao_torre_deck)
            tarefa1 = "Elevar a secao de torre " + \
                str(numeroSecao) + " na posição vertical "
            alturaElevacao += secao_torre.getAltura()
            cronograma.adicionarMicroatividade(nomeTarefa, nomeMacroatividade, tarefa1, TipoMicroatividade.INSTALACAO_AEROGERADOR,
                                               self.getTempoElevarSecaoTorreVertical(embarcacao, alturaElevacao))
            if (numeroSecao == 1):
                tarefa2 = "Anexar seção de torre " + \
                    str(numeroSecao) + " na subestrutura"
                cronograma.adicionarMicroatividade(
                    nomeTarefa, nomeMacroatividade, tarefa2, TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_secao_torre_na_subestrutura)
            else:
                tarefa2 = "Anexar seção de torre " + \
                    str(numeroSecao) + " na torre"
                cronograma.adicionarMicroatividade(
                    nomeTarefa, nomeMacroatividade, tarefa2, TipoMicroatividade.INSTALACAO_AEROGERADOR, self._tempo_anexar_secao_torre)

    def getSecoesTorre(self):
        return self._secoes_torre

    def getAlturaTorre(self):
        altura = 0
        for secao_torre in self._secoes_torre:
            altura += secao_torre.getAltura()
        return altura
