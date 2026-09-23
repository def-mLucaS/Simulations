
class Rebocador:
    def __init__(self, id, velocidade_locomocao_carregado, velocidade_locomocao_vazio, taxaDiaria, _taxaMobilizacao):
        self._id = id
        self._velocidade_locomocao_carregado = velocidade_locomocao_carregado
        self._velocidade_locomocao_vazio = velocidade_locomocao_vazio
        self._taxaDiaria = taxaDiaria
        self._taxaMobilizacao = _taxaMobilizacao

    def getId(self):
        return self._id

    def getVelocidadeCarregado(self):
        return self._velocidade_locomocao_carregado

    def getVelocidadeVazio(self):
        return self._velocidade_locomocao_vazio

    def getTaxaDiaria(self):
        return self._taxaDiaria

    def getTaxaMobilizacao(self):
        return self._taxaMobilizacao
