from ..Instalacao.AbstractSimulacaoInstalacao import AbstractSimulacaoInstalacao
from ..ConjuntosComponentes.ConjuntoFundacao import ConjuntoFundacao
from ..Instalacao.EtapaInstalacao import EtapaInstalacao


class SimulacaoInstalacaoFundacao(AbstractSimulacaoInstalacao):
    def __init__(self, parque, porto, kitsFundacao, solucaoEmbarcacao):
        self.__validarFundacao__(kitsFundacao)
        self._parque = parque
        self._porto = porto
        self._kitsFundacao = kitsFundacao
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = parque.getPlanta()
        dataInicio = parque.getDataInicioInstalacao()
        etapaInstalacao = EtapaInstalacao.FUNDACAO
        super().__init__(dataInicio, etapaInstalacao, parque, porto,
                         parque.getPlanta(), kitsFundacao, solucaoEmbarcacao)

    def __validarFundacao__(self, kitsFundacao):
        if not isinstance(kitsFundacao, dict) or not all(isinstance(item, ConjuntoFundacao) for item in kitsFundacao.values()):
            raise KeyError("A classe derivativa deve ser ConjuntoFundacao.")
