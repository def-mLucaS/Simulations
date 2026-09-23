from enum import Enum


class TipoMicroatividade(Enum):
    PORTO = 'Atividades no porto'
    TRANSPORTE_FRETE = 'Frete do porto ao parque'
    TRANSPORTE_INSTALACAO = 'Deslocamento para instalação'
    TRANSPORTE_CARREGAMENTO = 'Deslocamento do parque até o porto para carregar'
    TRANSBORDO = 'Transbordo entre embarcações'
    INTERRUPCAO_DE_OPERACAO = 'Ação realizada por condições climáticas severas'
    INSTALACAO_ENROCAMENTO = 'Instalação do enrocamento'
    INSTALACAO_FUNDACAO = 'Instalação de fundação'
    INSTALACAO_AEROGERADOR = 'Instalação de aerogerador'
    INSTALACAO_SUBESTACAO = 'Instalação da caixa da subestação offshore'
    INSTALACAO_SISTEMA_ARRAY = 'Instalação de cabos do sistema array'
    INSTALACAO_CABOS_EXPORTACAO = 'Instalação dos cabos de exportação'
    ESPERA = 'Em espera'
