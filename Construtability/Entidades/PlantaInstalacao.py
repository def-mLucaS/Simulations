from ..Ferramentas.Distancia import calcularDistanciaMetrosCoordenadas
from ..Instalacao.StatusInstalacao import StatusInstalacao
import math


class PlantaInstalacao():
    def __init__(self, dictPontoInstalacao):
        self._pontos = dictPontoInstalacao
        self.__inicializar__()

    def __inicializar__(self):
        for chavePonto, ponto in self._pontos.items():
            ponto.setStatusInstalacao(StatusInstalacao.NAO_INICIOU)
        self.calculaMatrizDistancia()

    def setStatusInstalacao(self, idPonto, status):
        if idPonto in self._Ponto:
            self._pontos[idPonto].setStatusInstalacao(status)
        else:
            raise KeyError("ID nao existe.")

    def getCoordenadas(self, idPonto):
        if idPonto in self._pontos:
            return self._pontos[idPonto].getCoordenadas()
        else:
            raise KeyError("ID nao existe.")

    def getProfundidade(self, idPonto):
        if idPonto in self._pontos:
            return self._pontos[idPonto].getProfundidade()
        else:
            raise KeyError("ID nao existe.")

    def getPontos(self):
        return self._pontos

    def getPonto(self, id):
        return self._pontos[id]

    def getPontosNaoIniciadosNaEtapa(self, etapa):
        listaPontos = []
        statusNaEtapa = StatusInstalacao.getStatusNaoIniciouEtapa(etapa)
        for id in self._pontos:
            if self._pontos[id].getStatusInstalacao() == statusNaEtapa:
                listaPontos.append(id)
        return listaPontos

    def getPontosConcluidasNaEtapa(self, etapa):
        listaPontos = []
        statusNaEtapa = StatusInstalacao.getStatusFinalizouEtapa(etapa)
        for id in self._pontos:
            if self._pontos[id].getStatusInstalacao() == statusNaEtapa:
                listaPontos.append(id)
        return listaPontos

    def isEtapaConcluida(self, etapa):
        pontosConcluidas = self.getPontosConcluidasNaEtapa(etapa)
        numeroPontosConcluidas = len(pontosConcluidas)
        numeroPontos = len(self._pontos)
        return len(pontosConcluidas) == len(self._pontos)

    def temPontosNaoIniciadosNaEtapa(self, etapa):
        numeroPontosNaoIniciados = len(
            self.getPontosNaoIniciadosNaEtapa(etapa))
        return numeroPontosNaoIniciados > 0

    def setIniciouEtapa(self, etapa, idPonto, dataInicio):
        self._pontos[idPonto].setIniciouEtapa(etapa, dataInicio)

    def setFinalizouEtapa(self, etapa, idPonto, dataFim):
        self._pontos[idPonto].setFinalizouEtapa(etapa, dataFim)

    def getPontosProximosNaoIniciadosNaEtapa(self, etapa, n):
        naoIniciadas = self.getPontosNaoIniciadosNaEtapa(etapa)
        if n > len(naoIniciadas):
            raise ValueError(
                "Número de pontos solicitado maior do que o disponível")

        # Encontra a primeira ponto, a que tem a maior soma das distâncias em relação a todas as outras pontos
        primeiraPonto = naoIniciadas[0]
        max_distancia = 0
        for ponto in naoIniciadas:
            distancias = self.matrizDistancias[ponto]
            soma_distancias = sum(distancias[t]
                                  for t in naoIniciadas if t != ponto)
            if soma_distancias > max_distancia:
                primeiraPonto = ponto
                max_distancia = soma_distancias

        # Encontra as demais pontos
        pontosSelecionadas = [primeiraPonto]
        for i in range(n - 1):
            naoSelecionadas = list(
                filter(lambda t: t not in pontosSelecionadas, naoIniciadas))
            maisProxima = min(
                naoSelecionadas, key=lambda t: self.matrizDistancias[pontosSelecionadas[-1]][t])
            pontosSelecionadas.append(maisProxima)
        return pontosSelecionadas

    def distanciaEntrePontos(self, id1, id2):
        return self.matrizDistancias[id1][id2]

    def calculaMatrizDistancia(self):
        matriz = {}
        for id1 in self._pontos:
            matriz[id1] = {}
            for id2 in self._pontos:
                if id1 == id2:
                    matriz[id1][id2] = 0
                else:
                    coordenadas1 = self.getCoordenadas(id1)
                    coordenadas2 = self.getCoordenadas(id2)
                    distancia = math.sqrt(
                        (coordenadas1[0] - coordenadas2[0]) ** 2 + (coordenadas1[1] - coordenadas2[1]) ** 2)
                    matriz[id1][id2] = distancia
        self.matrizDistancias = matriz

    def getPosicaoPontoMaisLongePorto(self, porto, conjuntoPontos):
        # Criterio de mais distante do parque
        coordenadaPorto = porto.getCoordenadas()
        distanciaMaior = 0
        idDistante = None
        for id in conjuntoPontos:
            coordenadaPonto = self._pontos[id].getCoordenadas()
            distanciaNova = calcularDistanciaMetrosCoordenadas(
                coordenadaPorto, coordenadaPonto)
            if (distanciaNova > distanciaMaior):
                idDistante = id
                distanciaMaior = distanciaNova
        return idDistante

    def getListaOrdenadaPontoMaisProximos(self, coordenada, conjuntoPontos):
        # Criterio de mais distante do parque
        distancias = {}
        for id in conjuntoPontos:
            coordenadaPonto = self._pontos[id].getCoordenadas()
            distancias[id] = calcularDistanciaMetrosCoordenadas(
                coordenada, coordenadaPonto)

        idsOrdenados = sorted(distancias, key=distancias.get)

        return idsOrdenados
