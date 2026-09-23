from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Instalacao.StatusInstalacao import StatusInstalacao


class PontoInstalacao():
    def __init__(self, id, latitude, longitude, profundidade):
        self._id = id
        self._latitude = latitude
        self._longitude = longitude
        self._profundidade = profundidade
        self._statusInstalacao = StatusInstalacao.NAO_INICIOU
        self._dataEtapasIniciadas = dict()
        self._dataEtapasFinalizadas = dict()

    def setStatusInstalacao(self, status):
        self._statusInstalacao = status

    def getStatusInstalacao(self):
        return self._statusInstalacao

    def getCoordenadas(self):
        return (self._latitude, self._longitude)

    def getId(self):
        return self._id

    def getProfundidade(self):
        return self._profundidade

    def getEtapasIniciadas(self):
        return self._dataEtapasIniciadas

    def getEtapasConcluidas(self):
        return self._dataEtapasFinalizadas

    def isEtapaConcluida(self, etapa):
        statusNaEtapa = StatusInstalacao.getStatusFinalizouEtapa(etapa)
        if self._statusInstalacao == statusNaEtapa:
            return True
        else:
            return False

    def isEtapaNaoIniciada(self, etapa):
        statusNaEtapa = StatusInstalacao.getStatusNaoIniciouEtapa(etapa)
        if self._statusInstalacao == statusNaEtapa:
            return True
        else:
            return False

    def isEtapaIniciada(self, etapa):
        statusNaEtapa = StatusInstalacao.getStatusIniciouEtapa(etapa)
        if self._statusInstalacao == statusNaEtapa:
            return True
        else:
            return False

    def setIniciouEtapa(self, etapa, dataInicio):
        if (etapa == EtapaInstalacao.FUNDACAO):
            self._statusInstalacao = StatusInstalacao.INICIOU_FUNDACAO
        elif (etapa == EtapaInstalacao.SUBESTACAO_FUNDACAO):
            self._statusInstalacao = StatusInstalacao.INICIOU_SUBESTACAO_FUNDACAO
        elif (etapa == EtapaInstalacao.SUBESTACAO_CAIXA):
            self._statusInstalacao = StatusInstalacao.INICIOU_SUBESTACAO_CAIXA
        elif (etapa == EtapaInstalacao.SISTEMA_ARRAY):
            self._statusInstalacao = StatusInstalacao.INICIOU_SISTEMA_ARRAY
        elif (etapa == EtapaInstalacao.CABO_EXPORTACAO_ONSHORE):
            self._statusInstalacao = StatusInstalacao.INICIOU_CABO_EXPORTACAO_ONSHORE
        elif (etapa == EtapaInstalacao.CABO_EXPORTACAO_OFFSHORE):
            self._statusInstalacao = StatusInstalacao.INICIOU_CABO_EXPORTACAO_OFFSHORE
        elif (etapa == EtapaInstalacao.AEROGERADOR):
            self._statusInstalacao = StatusInstalacao.INICIOU_AEROGERADOR

        self._dataEtapasIniciadas[etapa] = dataInicio

    def setFinalizouEtapa(self, etapa, dataFim):
        if (etapa == EtapaInstalacao.FUNDACAO):
            self._statusInstalacao = StatusInstalacao.TERMINOU_FUNDACAO
        elif (etapa == EtapaInstalacao.SUBESTACAO_FUNDACAO):
            self._statusInstalacao = StatusInstalacao.TERMINOU_SUBESTACAO_FUNDACAO
        elif (etapa == EtapaInstalacao.SUBESTACAO_CAIXA):
            self._statusInstalacao = StatusInstalacao.TERMINOU_SUBESTACAO_CAIXA
        elif (etapa == EtapaInstalacao.SISTEMA_ARRAY):
            self._statusInstalacao = StatusInstalacao.TERMINOU_SISTEMA_ARRAY
        elif (etapa == EtapaInstalacao.CABO_EXPORTACAO_ONSHORE):
            self._statusInstalacao = StatusInstalacao.TERMINOU_CABO_EXPORTACAO_ONSHORE
        elif (etapa == EtapaInstalacao.CABO_EXPORTACAO_OFFSHORE):
            self._statusInstalacao = StatusInstalacao.TERMINOU_CABO_EXPORTACAO_OFFSHORE
        elif (etapa == EtapaInstalacao.AEROGERADOR):
            self._statusInstalacao = StatusInstalacao.TERMINOU_AEROGERADOR

        self._dataEtapasFinalizadas[etapa] = dataFim
