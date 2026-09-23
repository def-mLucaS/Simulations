from enum import Enum
from ..Instalacao.EtapaInstalacao import EtapaInstalacao


class StatusInstalacao(Enum):
    NAO_INICIOU = 0
    INICIOU_FUNDACAO = 1
    TERMINOU_FUNDACAO = 2
    INICIOU_SUBESTACAO_FUNDACAO = 3
    TERMINOU_SUBESTACAO_FUNDACAO = 4
    INICIOU_SUBESTACAO_CAIXA = 5
    TERMINOU_SUBESTACAO_CAIXA = 6
    INICIOU_SISTEMA_ARRAY = 7
    TERMINOU_SISTEMA_ARRAY = 8
    INICIOU_CABO_EXPORTACAO_ONSHORE = 9
    TERMINOU_CABO_EXPORTACAO_ONSHORE = 10
    INICIOU_CABO_EXPORTACAO_OFFSHORE = 11
    TERMINOU_CABO_EXPORTACAO_OFFSHORE = 12
    INICIOU_AEROGERADOR = 13
    TERMINOU_AEROGERADOR = 14

    @staticmethod
    def getStatusNaoIniciouEtapa(etapa):
        if etapa == EtapaInstalacao.FUNDACAO:
            return StatusInstalacao.NAO_INICIOU
        elif etapa == EtapaInstalacao.SUBESTACAO_FUNDACAO:
            return StatusInstalacao.TERMINOU_FUNDACAO
        elif etapa == EtapaInstalacao.SUBESTACAO_CAIXA:
            return StatusInstalacao.TERMINOU_SUBESTACAO_FUNDACAO
        elif etapa == EtapaInstalacao.SISTEMA_ARRAY:
            return StatusInstalacao.TERMINOU_SUBESTACAO_CAIXA
        elif etapa == EtapaInstalacao.CABO_EXPORTACAO_ONSHORE:
            return StatusInstalacao.TERMINOU_SISTEMA_ARRAY
        elif etapa == EtapaInstalacao.CABO_EXPORTACAO_OFFSHORE:
            return StatusInstalacao.TERMINOU_CABO_EXPORTACAO_ONSHORE
        elif etapa == EtapaInstalacao.AEROGERADOR:
            return StatusInstalacao.TERMINOU_CABO_EXPORTACAO_OFFSHORE

    @staticmethod
    def getStatusIniciouEtapa(etapa):
        if etapa == EtapaInstalacao.FUNDACAO:
            return StatusInstalacao.INICIOU_FUNDACAO
        elif etapa == EtapaInstalacao.SUBESTACAO_FUNDACAO:
            return StatusInstalacao.INICIOU_SUBESTACAO_FUNDACAO
        elif etapa == EtapaInstalacao.SUBESTACAO_CAIXA:
            return StatusInstalacao.INICIOU_SUBESTACAO_CAIXA
        elif etapa == EtapaInstalacao.SISTEMA_ARRAY:
            return StatusInstalacao.INICIOU_SISTEMA_ARRAY
        elif etapa == EtapaInstalacao.CABO_EXPORTACAO_ONSHORE:
            return StatusInstalacao.INICIOU_CABO_EXPORTACAO_ONSHORE
        elif etapa == EtapaInstalacao.CABO_EXPORTACAO_OFFSHORE:
            return StatusInstalacao.INICIOU_CABO_EXPORTACAO_OFFSHORE
        elif etapa == EtapaInstalacao.AEROGERADOR:
            return StatusInstalacao.INICIOU_AEROGERADOR

    @staticmethod
    def getStatusFinalizouEtapa(etapa):
        if etapa == EtapaInstalacao.FUNDACAO:
            return StatusInstalacao.TERMINOU_FUNDACAO
        elif etapa == EtapaInstalacao.SUBESTACAO_FUNDACAO:
            return StatusInstalacao.TERMINOU_SUBESTACAO_FUNDACAO
        elif etapa == EtapaInstalacao.SUBESTACAO_CAIXA:
            return StatusInstalacao.TERMINOU_SUBESTACAO_CAIXA
        elif etapa == EtapaInstalacao.SISTEMA_ARRAY:
            return StatusInstalacao.TERMINOU_SISTEMA_ARRAY
        elif etapa == EtapaInstalacao.CABO_EXPORTACAO_ONSHORE:
            return StatusInstalacao.TERMINOU_CABO_EXPORTACAO_ONSHORE
        elif etapa == EtapaInstalacao.CABO_EXPORTACAO_OFFSHORE:
            return StatusInstalacao.TERMINOU_CABO_EXPORTACAO_OFFSHORE
        elif etapa == EtapaInstalacao.AEROGERADOR:
            return StatusInstalacao.TERMINOU_AEROGERADOR
