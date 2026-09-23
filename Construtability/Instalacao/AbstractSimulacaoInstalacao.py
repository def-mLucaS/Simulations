import math
from datetime import timedelta

from ..Entidades.Porto import Porto
from ..Entidades.Parque import Parque
from ..ConjuntosComponentes.ConjuntoComponentes import ConjuntoComponentes
from ..MovimentacaoComponente.SolucaoEmbarcacao import SolucaoEmbarcacao
from ..Instalacao.EtapaInstalacao import EtapaInstalacao
from ..Ferramentas.Distancia import calcularDistanciaQuilometrosCoordenadas


class AbstractSimulacaoInstalacao:
    def __init__(self, dataInicio, etapaInstalacao, parque, porto, planta, kitsComponentes, solucaoEmbarcacao):
        self.__validar__(etapaInstalacao, parque, porto,
                         kitsComponentes, solucaoEmbarcacao)
        self._parque = parque
        self._porto = porto
        self._kitsComponentes = kitsComponentes
        self._solucaoEmbarcacao = solucaoEmbarcacao
        self._planta = planta
        self.dataInicioInstalacao = dataInicio
        self._dataAtual = dataInicio
        self._etapaInstalacao = etapaInstalacao

    def __validar__(self, etapaInstalacao, parque, porto, kitsComponentes, solucaoEmbarcacao):
        if not isinstance(etapaInstalacao, EtapaInstalacao):
            raise KeyError("A classe derivativa deve ser EtapaInstalacao.")
        if not isinstance(parque, Parque):
            raise KeyError("A classe derivativa deve ser Parque.")
        if not isinstance(porto, Porto):
            raise KeyError("A classe derivativa deve ser Porto.")
        if not isinstance(kitsComponentes, dict) or not all(isinstance(item, ConjuntoComponentes) for item in kitsComponentes.values()):
            raise KeyError("A classe derivativa deve ser ConjuntoComponentes.")
        if not isinstance(solucaoEmbarcacao, SolucaoEmbarcacao):
            raise KeyError("A classe derivativa deve ser SolucaoEmbarcacao.")

    def executarInstalacao(self, cronograma):
        if len(self._kitsComponentes) != 0:
            self.instalarComFluxoAlimentadoraInstaladora(
                cronograma, self._etapaInstalacao, self._kitsComponentes)
        pass

    def instalarComFluxoAlimentadoraInstaladora(self, cronograma, etapa, conjuntos):
        print("Iniciando o processo de instalacao dos conjuntos da etapa: " + etapa.name)
        instalouTudo = False
        while (not instalouTudo):
            for chaveAlimentadora in self._solucaoEmbarcacao._listaAlimentadoras:
                if (self._planta.temPontosNaoIniciadosNaEtapa(etapa)):
                    if (self.deckEmbarcacaoEstaVazio(chaveAlimentadora)):
                        # Desloca embarcacao para o porto
                        self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].deslocarParaPorto(
                            cronograma, self._porto)
                        # Carrega embarcacao
                        self.executarCarregamentoNoPortoCriterioPontosMaisProximos(
                            conjuntos, etapa, cronograma, chaveAlimentadora, self._planta)
                        # Escolhe a primeira turbina em que a embarcacao ira se dirigir
                        conjuntosTransportados = self._solucaoEmbarcacao.embarcacoes[
                            chaveAlimentadora].conjuntosTransportados
                        idTurbina = self._planta.getPosicaoPontoMaisLongePorto(
                            self._porto, conjuntosTransportados.keys())
                        # desloca ate turbina escolhida
                        self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].deslocarCarregadoPortoParaTurbina(
                            cronograma, self._planta, idTurbina)
            for chaveInstaladora in self._solucaoEmbarcacao._listaInstaladoras:
                if (not self._planta.isEtapaConcluida(etapa)):
                    if self.deckEmbarcacaoEstaVazio(chaveInstaladora):
                        if self._solucaoEmbarcacao.temAlimentador():
                            # Define a barcaca mais proxima com componentes no deck para serem instalados
                            chaveAlimentadora = self.getAlimentadoraMaisProximaDisponivel(
                                chaveInstaladora)
                            # Se não houver alimentadora disponível vai para a próxima
                            if chaveAlimentadora is None:
                                continue
                            # Define a turbina mais proxima da barcaca (ela ja vai estar em uma posição de uma turbina)
                            idTurbina = self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].getTurbinaMaisProxima(
                                self._planta)
                            # Desloca instalador ate a turbina
                            if (not self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].getDataAtual()):
                                # calcula data anterior para deslocamento
                                instaladora = self._solucaoEmbarcacao.embarcacoes[chaveInstaladora]
                                distancia = calcularDistanciaQuilometrosCoordenadas(
                                    self._planta.getCoordenadas(idTurbina), instaladora.getPosicao())
                                duracao = instaladora.calculaTempoDeslocamento(
                                    distancia)
                                dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].getDataAtual(
                                ) - timedelta(hours=duracao)
                                self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].setDataAtual(
                                    dataInicio)
                            if (not self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].getNumeroViagem()):
                                self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].setNumeroViagem(
                                    1)
                                self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].setNumeroViagemAtividade(
                                    1)
                                self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].setDataInicio(
                                    dataInicio)
                            else:
                                numeroViagens = self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].getNumeroViagem(
                                )
                                self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].setNumeroViagem(
                                    numeroViagens + 1)
                                self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].setNumeroViagemAtividade(
                                    numeroViagens + 1)

                            #  Desloca instaladora para turbina
                            self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].deslocarParaTurbina(
                                cronograma, self._planta, idTurbina)
                            # Desloca alimentador ate a turbina (só para ter certeza)
                            self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].deslocarParaTurbina(
                                cronograma, self._planta, idTurbina)
                            # Transfere os componentes da barcaca para wtiv
                            self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].transferirComponentesParaOutraEmbarcacao(self._planta,
                                                                                                                            self._solucaoEmbarcacao.embarcacoes[chaveInstaladora], cronograma)
                            print("Data atual externa " + str(
                                self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].getDataAtual()))
                    else:  # deck com conteudo -> realiza instalacao
                        idTurbina = self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].getTurbinaMaisProxima(
                            self._planta)
                        self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].deslocarParaTurbina(cronograma,
                                                                                                  self._planta, idTurbina)
                        dataInicio = self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].getDataAtual(
                        )
                        dataFim = self._executarInstalacao(
                            cronograma, chaveInstaladora, dataInicio, idTurbina)
                        self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].setDataAtual(
                            dataFim)
                        # Muda status da turbina instalada
                        self._planta.setFinalizouEtapa(
                            etapa, idTurbina, dataFim)
                        # Exclui id da lista de componentes no deck
                        del self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].deck[idTurbina]
                        del self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].conjuntosTransportados[idTurbina]
                        self._solucaoEmbarcacao.embarcacoes[chaveInstaladora].turbinasDeck.remove(
                            idTurbina)

            # Critério de parada
            if (self._planta.isEtapaConcluida(etapa)):
                instalouTudo = True

    def executarCarregamentoNoPortoCriterioPontosMaisProximos(self, conjuntos, etapa, cronograma, chaveEmbarcacao, planta):
        conjuntosNoPorto = self.getKitsNoPorto(conjuntos, etapa)
        numeroKits = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].calculaNumeroConjuntosCarregaveis(
            conjuntosNoPorto)
        if (numeroKits == 0):
            raise ValueError("A embarcação não suporta o kit de instalação.")
        print("Quantidade de kits no porto: ", len(conjuntosNoPorto))
        print("Quantidade sendo carregada no navio: ", numeroKits)

        # ID turbinas escolhidas que serao instaladas na etapa (criterio de distancia entre elas)
        turbinasDeck = self._planta.getPontosProximosNaoIniciadosNaEtapa(
            etapa, numeroKits)
        print("Turbinas escolhidas para serem carregadas na embarcacao: ")
        print(turbinasDeck)

        # Extrai os conjuntos que serao transportados a partir da lista de turbinas escolhidas
        conjuntosTransportados = self.extraiKits(turbinasDeck, conjuntos)
        print("ID dos kits transportados: ")
        print(conjuntosTransportados.keys())

        # Atualizando a data de início da embarcação
        if (self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual() is None):
            self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].setDataAtual(
                self.dataInicioInstalacao)

        # Para cada turbina que está no deck inicia a etapa
        for idTurbina in turbinasDeck:
            planta.setIniciouEtapa(etapa,
                                   idTurbina,
                                   self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual())
            print("No ponto de instalação ", idTurbina,
                  "iniciou-se a etapa de ", etapa.name)

         # Carregar embarcacao
        print("Data atual: ",
              self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual())
        print("Inicia o processo de carregamento da embarcacao alimentadora")
        self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].carregarConjuntoComponentes(
            cronograma, conjuntosTransportados, turbinasDeck)

    def extraiKits(self, listaTurbinas, conjuntos):
        kits = {chave: valor for chave, valor in conjuntos.items()
                if chave in listaTurbinas}
        return kits

    def getKitsNoPorto(self, conjuntos, etapa):
        listaTurbinasPorto = self._planta.getPontosNaoIniciadosNaEtapa(etapa)
        kits = self.extraiKits(listaTurbinasPorto, conjuntos)
        return kits

    def deckEmbarcacaoEstaVazio(self, chaveEmbarcacao):
        if (len(self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].deck) == 0):
            return True
        else:
            return False

    def getAlimentadoraMaisProximaDisponivel(self, chaveEmbarcacao):
        posicaoInstaladora = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getPosicao(
        )
        dataAtualInstaladora = self._solucaoEmbarcacao.embarcacoes[chaveEmbarcacao].getDataAtual(
        )
        menorDistancia = math.inf
        menorDistanciaDisponivel = math.inf
        alimentadoraMaisProxima = None

        alimentadoraMaisProximaDisponivel = None
        for chaveAlimentadora in self._solucaoEmbarcacao._listaAlimentadoras:
            if not self.deckEmbarcacaoEstaVazio(chaveAlimentadora):
                posicaoAlimentadora = self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].getPosicao(
                )
                distancia = calcularDistanciaQuilometrosCoordenadas(
                    posicaoInstaladora, posicaoAlimentadora)
                if (distancia < menorDistancia):
                    menorDistancia = distancia
                    alimentadoraMaisProxima = chaveAlimentadora

                if dataAtualInstaladora != None:
                    if dataAtualInstaladora >= self._solucaoEmbarcacao.embarcacoes[chaveAlimentadora].getDataAtual():
                        if (distancia < menorDistanciaDisponivel):
                            menorDistanciaDisponivel = distancia
                            alimentadoraMaisProximaDisponivel = chaveAlimentadora

        if alimentadoraMaisProximaDisponivel != None:
            alimentadoraMaisProxima = alimentadoraMaisProximaDisponivel

        return alimentadoraMaisProxima

    def _executarInstalacao(self, cronograma, chaveEmbarcacao, dataInicio, idTurbina):
        pass

    def calcularCustoEmbarcacoes(self):
        custo_total = 0
        custo_embarcacoes = {}
        print("Calculando custo de uso das embarcacoes")
        for chaveEmbarcacao, embarcacao in self._solucaoEmbarcacao.getDicionarioEmbarcacoes().items():

            if embarcacao.getNumeroViagem() > 0:
                dataInicio = embarcacao.getDataInicio()
                dataFim = embarcacao.getDataAtual()
                # Calcula a duração em horas
                duracaoHoras = (dataFim - dataInicio).total_seconds() / 3600
                duracaoDias = duracaoHoras / 24  # Converte a duração de horas para dias
                taxa = embarcacao.getTaxaDiaria()
                custo_total += duracaoDias * taxa
                custo_embarcacao = {}
                custo_embarcacao["embarcacao"] = chaveEmbarcacao
                custo_embarcacao["viagens"] = embarcacao.getNumeroViagemAtividade()
                custo_embarcacao["data_inicio"] = dataInicio
                custo_embarcacao["data_fim"] = dataFim
                custo_embarcacao["total_dias"] = duracaoDias
                custo_embarcacao["taxa"] = taxa
                custo_embarcacao["custo"] = duracaoDias * taxa
                custo_embarcacao["area_total_transportada"] = embarcacao.getAreaTotalTransportada(
                )
                custo_embarcacao["taxa_mobilizacao"] = embarcacao.getTaxaMobilizacao(
                )

                custo_embarcacoes[chaveEmbarcacao] = custo_embarcacao

                print("-----------")
                print("Embarcação " + chaveEmbarcacao)
                print("Data início de uso " + str(dataInicio))
                print("Data fim de uso " + str(dataFim))
                print("Total de dias " + str(duracaoDias))
                print("Taxa " + str(taxa))
                print("Custo " + str(duracaoDias * taxa))
        print("Custo total de todas as embarcações " + str(custo_total))

        return custo_embarcacoes

    def calcularCustoEmbarcacoes_clima(self, lista_tarefas, fp):
        custo_embarcacao = dict()
        custo_embarcacoes = {}

        fallpipe_vessels = fp.embarcacoes

        datas = dict()

        # 'Tarefa': f'Fallpipe{int(emb)+1} - Viagem {sub}'
        for e in fallpipe_vessels:
            lista_datas = []
            for tarefa in lista_tarefas:
                string_emb = tarefa['Tarefa'].split(" ")
                if string_emb[0] == e:
                    lista_datas.append(tarefa)
            datas[e] = sorted(lista_datas, key=lambda d: d['Start'])

        for e in fallpipe_vessels:
            custo_embarcacao = {}
            string_emb = datas[e][-1]['Tarefa'].split(" ")
            custo_embarcacao["viagens"] = int(string_emb[3])
            custo_embarcacao["data_inicio"] = datas[e][0]['Start']
            custo_embarcacao["data_fim"] = datas[e][-1]['Finish']
            dataInicio = datas[e][0]['Start']
            dataFim = datas[e][-1]['Finish']
            duracaoHoras = (dataFim - dataInicio).total_seconds() / 3600
            duracaoDias = duracaoHoras / 24
            custo_embarcacao["total_dias"] = math.ceil(duracaoDias)
            custo_embarcacao["taxa"] = fallpipe_vessels[e].getTaxaDiaria()
            taxa = fallpipe_vessels[e].getTaxaDiaria()
            custo_embarcacao["custo"] = math.ceil(
                duracaoDias) * fallpipe_vessels[e].getTaxaDiaria()
            custo_embarcacao["area_total_transportada"] = 0
            custo_embarcacao["taxa_mobilizacao"] = fallpipe_vessels[e].getTaxaMobilizacao(
            )
            custo_embarcacao['embarcacao'] = e

            print("-----------")
            print("Embarcação " + e)
            print("Data início de uso " + str(dataInicio))
            print("Data fim de uso " + str(dataFim))
            print("Total de dias " + str(duracaoDias))
            print("Taxa " + str(taxa))
            print("Custo " + str(duracaoDias * taxa))

            custo_embarcacoes[e] = custo_embarcacao
            print(custo_embarcacoes)
        return custo_embarcacoes

    def get_lista_tarefas(self, lista_tarefas):
        return lista_tarefas

    def calcularCustoEmbarcacoes_enrocamento(self, lista_tarefas, fp):
        custo_embarcacao = dict()
        custo_embarcacoes = {}

        fallpipe_vessels = fp.embarcacoes
        datas = dict()

        # 'Tarefa': f'Fallpipe{int(emb)+1} - Viagem {sub}'
        for e in fallpipe_vessels:
            lista_datas = []
            for tarefa in lista_tarefas:
                string_emb = tarefa['Tarefa'].split(" ")
                if tarefa['Tipo'] == 'Instalação do enrocamento'\
                        and string_emb[0] == e:
                    lista_datas.append(tarefa)
            datas[e] = lista_datas

        for e in fallpipe_vessels:
            custo_embarcacao = {}
            string_emb = datas[e][-1]['Tarefa'].split(" ")
            custo_embarcacao["viagens"] = int(string_emb[3])
            custo_embarcacao["data_inicio"] = datas[e][0]['Start']
            custo_embarcacao["data_fim"] = datas[e][-1]['Finish']
            dataInicio = datas[e][0]['Start']
            dataFim = datas[e][-1]['Finish']
            duracaoHoras = (dataFim - dataInicio).total_seconds() / 3600
            duracaoDias = duracaoHoras / 24
            custo_embarcacao["total_dias"] = math.ceil(duracaoDias)
            custo_embarcacao["taxa"] = fallpipe_vessels[e].getTaxaDiaria()
            taxa = fallpipe_vessels[e].getTaxaDiaria()
            custo_embarcacao["custo"] = math.ceil(
                duracaoDias) * fallpipe_vessels[e].getTaxaDiaria()
            custo_embarcacao["area_total_transportada"] = 0
            custo_embarcacao["taxa_mobilizacao"] = fallpipe_vessels[e].getTaxaMobilizacao(
            )
            custo_embarcacao['embarcacao'] = e

            print("-----------")
            print("Embarcação " + e)
            print("Data início de uso " + str(dataInicio))
            print("Data fim de uso " + str(dataFim))
            print("Total de dias " + str(duracaoDias))
            print("Taxa " + str(taxa))
            print("Custo " + str(duracaoDias * taxa))

            custo_embarcacoes[e] = custo_embarcacao
            print(custo_embarcacoes)
        return custo_embarcacoes

    def get_data_fim(self):
        print("Calculando custo de uso das embarcacoes")
        dataFim = 0
        for chaveEmbarcacao, embarcacao in self._solucaoEmbarcacao.getDicionarioEmbarcacoes().items():
            if embarcacao.getNumeroViagem() > 0:
                if dataFim == 0:
                    dataFim = embarcacao.getDataAtual()
                elif embarcacao.getDataAtual() > dataFim:
                    dataFim = embarcacao.getDataAtual()

        return dataFim

    def get_lista_tarefas(self, lista_tarefas):
        return lista_tarefas
