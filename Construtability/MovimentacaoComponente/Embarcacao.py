import math
from ..MovimentacaoComponente.Guindaste import Guindaste
from ..Default.Default import custos, embarcacao
from ..Ferramentas.Distancia import calcularDistanciaQuilometrosCoordenadas
from ..Cronograma.Cronograma import TipoMicroatividade
from ....utils.utils import float_to_str


class Embarcacao:
    def __init__(self, **kwargs):
        configuracao = {
            "nome": None,  # [m]
            "area_deck_livre": None,  # [m2]
            "maxima_capacidade_carga_deck": None,  # [t/m2]
            "velocidade_locomocao_carregado": None,  # [nos]
            "velocidade_locomocao_vazio": None,
            "taxa_diaria": custos["taxa_diaria_embarcacao"],  # [$]
            "taxa_mobilizacao": custos["taxa_mobilizacao_embarcacao"],  # [$]
            # limites operacionais
            # [m]
            "maxima_altura_onda": embarcacao["maxima_altura_onda"],
            # [m/s]
            "maxima_velocidade_vento": embarcacao["maxima_velocidade_vento"],
            # [m]
            "maxima_profundidade_agua": embarcacao["maxima_profundidade_agua"],
            # guindaste da embarcação
            "guindaste": None
        }
        configuracao.update(**kwargs)

        self._nome = configuracao["nome"]
        self._area_deck = configuracao["area_deck_livre"]
        self._maxima_capacidade_carga_deck = configuracao["maxima_capacidade_carga_deck"]
        self._velocidade_locomocao_carregado = configuracao["velocidade_locomocao_carregado"]
        self._velocidade_locomocao_vazio = configuracao["velocidade_locomocao_vazio"]
        # infos default (modificaveis)
        self._taxa_diaria = configuracao["taxa_diaria"]
        self._taxa_mobilizacao = configuracao["taxa_mobilizacao"]
        self._maxima_altura_onda = configuracao["maxima_altura_onda"]
        self._maxima_velocidade_vento = configuracao["maxima_velocidade_vento"]
        self._maxima_profundidade_agua = configuracao["maxima_profundidade_agua"]
        self._guindaste = configuracao["guindaste"]
        # posição
        self._posicao = tuple()
        self.setNumeroViagem(0)
        self.setNumeroViagemAtividade(0)
        self.deck = dict()
        self.turbinasDeck = list()
        self.conjuntosTransportados = list()
        self._dataInicio = None
        self._dataAtual = None
        self._areaTotalTransportada = 0

    def __update__(self, configuracao, **kwargs):
        return configuracao.update(**kwargs)
        self.__validar__(configuracao)

    def __validar__(self):
        if ~isinstance(self._guindaste, Guindaste):
            raise KeyError("A classe derivativa deve ser GUINDASTE.")

    def contaViagem(self, cronograma):
        self._viagem += 1
        self._viagemAtividade += 1
        cronograma.adicionarTarefa(self.nomeTarefa())

    def custoOperacao(self, horas):
        return (self.configuracao_embarcacao["taxa_diaria"] / 24) * horas

    def calculaNumeroConjuntosSuportado(self, conjuntoComponentes):
        area = conjuntoComponentes.getAreaTotal()
        densidade_area = conjuntoComponentes.getDensidadeArea()
        numero_area = math.floor(self._area_deck/area)
        numero_densidade_area = math.floor(
            self._maxima_capacidade_carga_deck/densidade_area)
        if (numero_area == 0.0) and (numero_densidade_area == 0.0):
            raise ValueError(
                f'Não existe área e nem capacidade disponível para movimentar o conjunto de componentes na embarcação {self._nome}.\n\n'
                f'Área do deck da embarcação: {float_to_str(self._area_deck)} m²\n'
                f'Área do conjunto de componentes: {float_to_str(area)} m²\n\n'
                f'Máxima capacidade de carga da embarcação: {float_to_str(self._maxima_capacidade_carga_deck)} t/m²\n'
                f'Carga do conjunto de componentes: {float_to_str(densidade_area)} t/m²')
        elif numero_area == 0.0:
            raise ValueError(
                f'Não existe área disponível para movimentar o conjunto de componentes na embarcação {self._nome}.\n\n'
                f'Área do deck da embarcação: {float_to_str(self._area_deck)} m²\n'
                f'Área do conjunto de componentes: {float_to_str(area)} m²\n\n')
        elif numero_densidade_area == 0.0:
            raise ValueError(
                f'Não existe capacidade disponível para movimentar o conjunto de componentes na embarcação {self._nome}.\n\n'
                f'Máxima capacidade de carga da embarcação: {float_to_str(self._maxima_capacidade_carga_deck)} t/m²\n'
                f'Carga do conjunto de componentes: {float_to_str(densidade_area)} t/m²')
        self._areaTotalTransportada += area
        return min(numero_area, numero_densidade_area)

    def calculaNumeroConjuntosCarregaveis(self, kits):
        numeroKitsDisponiveis = len(kits)
        chaveKit = next(iter(kits))  # pega a primeira como modelo
        modeloKit = kits[chaveKit]
        return min(self.calculaNumeroConjuntosSuportado(modeloKit), numeroKitsDisponiveis)

    def calculaTempoDeslocamento(self, distancia):
        # Calcula tempo de deslocamento em HORAS até determinada distancia em km
        velocidade_km_h = self.converteNosEmKilometrosPorHora(
            self.getVelocidade())
        return (distancia/velocidade_km_h)

    def setPosicao(self, coordenadas):
        self._posicao = coordenadas

    def converteNosEmKilometrosPorHora(self, velocidade):
        km_h = velocidade*1.852
        return km_h

    def deslocarParaPorto(self, cronograma, porto):
        self.contaViagem(cronograma)
        # --------------------------
        nomeTarefa = self.nomeTarefa()
        nomeMacro = "Deslocar ate o porto " + str(self.getNumeroViagem())
        nomeMicro = "Deslocar ate o porto"
        tipo = TipoMicroatividade.TRANSPORTE_CARREGAMENTO
        # --------------------------
        cronograma.adicionarMacroatividade(self.nomeTarefa(), nomeMacro)
        posicaoAtual = self._posicao
        posicaoDestino = porto.getCoordenadas()
        distancia = calcularDistanciaQuilometrosCoordenadas(
            posicaoAtual, posicaoDestino)
        tempo = self.calculaTempoDeslocamento(distancia)
        if self._dataAtual is None:
            self._dataAtual = cronograma.getDataAtual()
        if (self.getNumeroViagem() == 1):
            self.setDataInicio(self._dataAtual)
        if (tempo > 0):
            cronograma.adicionarMicroatividade(
                nomeTarefa, nomeMacro, nomeMicro, tipo, tempo)
            dataInicio = self._dataAtual
            cronograma.executarMacroatividade(
                nomeTarefa, nomeMacro, dataInicio)
            dataFinal = cronograma.getDataFimMacroatividade(
                nomeTarefa, nomeMacro)
            self._posicao = posicaoDestino
            self._dataAtual = dataFinal
            print("Deslocando embarcação até o porto")
            print("Posicao inicial", posicaoAtual)
            print("Posicao de destino", posicaoDestino)
            print("Tempo total de deslocamento", tempo, " horas")
            print("Data de inicio da atividade: ", dataInicio)
            print("Data de fim da atividade: ", dataFinal)

    def deslocarCarregadoPortoParaTurbina(self, cronograma, parque, idTurbina):
        dataInicio = self._dataAtual
        posicaoAtual = self._posicao
        posicaoDestino = parque.turbinas[idTurbina]
        # Ir ate a posição de destino
        distancia = calcularDistanciaQuilometrosCoordenadas(
            posicaoAtual, posicaoDestino)
        tempo = self.calculaTempoDeslocamento(distancia)
        self.setPosicao(posicaoDestino)
        # cronograma
        nomeTarefa = self.nomeTarefa()
        nomeMacro = "Frete embarcação alimentadora do porto até parque "
        nomeMicro = "Deslocar até a turbina " + \
            str(idTurbina) + " na posição " + str(posicaoDestino)
        tipo = TipoMicroatividade.TRANSPORTE_FRETE
        cronograma.adicionarTarefa(nomeTarefa)
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacro)
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacro, nomeMicro, tipo, tempo)
        cronograma.executarMacroatividade(nomeTarefa, nomeMacro, dataInicio)
        dataFim = cronograma.getDataFimMacroatividade(nomeTarefa, nomeMacro)
        self._dataAtual = dataFim

    def deslocarCarregadoPortoParaTurbina(self, cronograma, planta, idTurbina):
        dataInicio = self._dataAtual
        posicaoAtual = self._posicao
        posicaoDestino = planta.getCoordenadas(idTurbina)
        # Ir ate a posição de destino
        distancia = calcularDistanciaQuilometrosCoordenadas(
            posicaoAtual, posicaoDestino)
        tempo = self.calculaTempoDeslocamento(distancia)
        self.setPosicao(posicaoDestino)
        # cronograma
        nomeTarefa = self.nomeTarefa()
        nomeMacro = "Frete embarcação alimentadora do porto até parque "
        nomeMicro = "Deslocar ate a turbina " + \
            str(idTurbina) + " na posição " + str(posicaoDestino)
        tipo = TipoMicroatividade.TRANSPORTE_FRETE
        cronograma.adicionarTarefa(nomeTarefa)
        cronograma.adicionarMacroatividade(nomeTarefa, nomeMacro)
        cronograma.adicionarMicroatividade(
            nomeTarefa, nomeMacro, nomeMicro, tipo, tempo)
        cronograma.executarMacroatividade(nomeTarefa, nomeMacro, dataInicio)
        dataFim = cronograma.getDataFimMacroatividade(nomeTarefa, nomeMacro)
        self._dataAtual = dataFim

    def deslocarParaTurbina(self, cronograma, planta, idTurbina):
        dataInicio = self._dataAtual
        posicaoAtual = self._posicao
        posicaoDestino = planta.getCoordenadas(idTurbina)
        # Ir ate a posição de destino
        distancia = calcularDistanciaQuilometrosCoordenadas(
            posicaoAtual, posicaoDestino)
        tempo = self.calculaTempoDeslocamento(distancia)
        if (tempo > 0):
            self.setPosicao(posicaoDestino)
            # cronograma
            nomeTarefa = self.nomeTarefa()
            nomeMacro = "Deslocamento embarcação até turbina  " + \
                str(idTurbina) + "  para instalacao "
            nomeMicro = "Deslocar ate a turbina " + \
                str(idTurbina) + " na posição " + str(posicaoDestino)
            tipo = TipoMicroatividade.TRANSPORTE_INSTALACAO
            cronograma.adicionarTarefa(nomeTarefa)
            cronograma.adicionarMacroatividade(nomeTarefa, nomeMacro)
            cronograma.adicionarMicroatividade(
                nomeTarefa, nomeMacro, nomeMicro, tipo, tempo)
            cronograma.executarMacroatividade(
                nomeTarefa, nomeMacro, dataInicio)
            dataFim = cronograma.getDataFimMacroatividade(
                nomeTarefa, nomeMacro)
            self._dataAtual = dataFim
            print(" ")
            print("Tarefa: ", nomeTarefa)
            print("Macroatividade: ", nomeMacro)
            print("Atividade: ", nomeMicro)
            print("Duração: ", tempo)
            print("Data início: ", dataInicio)
            print("Data fim: ", dataFim)

    def carregarComponente(self, cronograma, componente, idComponente, dataInicio):
        nomeMacro = "Carregar componente " + \
            str(componente.getTipoComponente()) + " - ID " + str(idComponente)
        cronograma.adicionarMacroatividade(self.nomeTarefa(), nomeMacro)
        nomeMicro1 = "Subir " + \
            str(componente.getTipoComponente()) + " para a embarcação"
        duracao1 = self._guindaste.calcular_tempo_movimentacao(
            componente.getAltura())
        cronograma.adicionarMicroatividade(
            self.nomeTarefa(), nomeMacro, nomeMicro1, TipoMicroatividade.PORTO, duracao1)
        print(" ")
        print("Tarefa: ", self.nomeTarefa())
        print("Macroatividade: ", nomeMacro)
        print("Atividade: ", nomeMicro1)
        print("Duração: ", duracao1)

        nomeMicro2 = "Fixar " + \
            str(componente.getTipoComponente()) + " no deck da embarcação"
        duracao2 = componente.getTempoFixacaoDeck()
        cronograma.adicionarMicroatividade(
            self.nomeTarefa(), nomeMacro, nomeMicro2, TipoMicroatividade.PORTO, duracao2)
        print(" ")
        print("Tarefa: ", self.nomeTarefa())
        print("Macroatividade: ", nomeMacro)
        print("Atividade: ", nomeMicro2)
        print("Duração: ", duracao2)

        cronograma.executarMacroatividade(
            self.nomeTarefa(), nomeMacro, dataInicio)
        dataFim = cronograma.getDataFimMacroatividade(
            self.nomeTarefa(), nomeMacro)
        print("Data início: ", dataInicio)
        print("Data fim: ", dataFim)

        self._dataAtual = dataFim

        return dataFim

    def carregarComponentes(self, cronograma, componentes, id, dataInicio):
        for componente in componentes:
            dataFim = self.carregarComponente(
                cronograma, componente, id, dataInicio)
            dataInicio = dataFim
        return dataFim

    def carregarConjuntoComponentes(self, cronograma, conjuntosTransportados, turbinasDeck):
        dataInicio = self._dataAtual
        # Carregar embarcação
        for id in conjuntosTransportados:
            print("Carregando na embarcação o componente ", id)
            self.addKitNoDeck(conjuntosTransportados[id])
            componentes = conjuntosTransportados[id].getListaComponentes()
            dataFim = self.carregarComponentes(
                cronograma, componentes, id, dataInicio)
            dataInicio = dataFim
        self.conjuntosTransportados = conjuntosTransportados
        self.turbinasDeck = turbinasDeck

        # Salva informacoes da embarcação alimentadora
        self._dataAtual = dataFim
        return dataFim

    def nomeMacroatividade(self):
        return "Viagem " + str(self.getNumeroViagem())

    def nomeTarefa(self):
        return self._nome + " - Viagem " + str(self.getNumeroViagem())

    def addKitNoDeck(self, kit):
        self.deck[kit.getId()] = kit

    def removeKitDoDeck(self, kit):
        del self.deck[kit.getId()]

    def getTurbinaMaisProxima(self, planta):
        turbinas = planta.getPontos()
        # a partir dos ids dos kits que estao no deck, define o mais próximo da posição da embarcação
        posicaoEmbarcacao = self._posicao
        menorDistancia = math.inf
        turbinaMaisProxima = None
        for chaveTurbina in self.conjuntosTransportados:
            posicaoTurbina = turbinas[chaveTurbina].getCoordenadas()
            distancia = calcularDistanciaQuilometrosCoordenadas(
                posicaoEmbarcacao, posicaoTurbina)
            if (distancia < menorDistancia):
                menorDistancia = distancia
                turbinaMaisProxima = chaveTurbina
        return turbinaMaisProxima

    def transferirComponentesParaOutraEmbarcacao(self, planta, embarcacaoDestino, cronograma):
        # Determinar conjuntos transferidos
        numeroKits = embarcacaoDestino.calculaNumeroConjuntosCarregaveis(
            self.conjuntosTransportados)

        # ID das turbinas escolhidas para transferencia (criterio as primeiras da lista)
        turbinasDeckAux = planta.getListaOrdenadaPontoMaisProximos(
            self._posicao, self.turbinasDeck)

        turbinasDeck = turbinasDeckAux[:numeroKits]
        conjuntosTransportados = {
            chave: self.conjuntosTransportados[chave] for chave in turbinasDeck}

        # Iguala tempos de inicio entre as duas embarcacoes
        dataInicio = max(self._dataAtual, embarcacaoDestino.getDataAtual())
        dataAnteriorEmbarcacao = self._dataAtual
        self._dataAtual = dataInicio

        # Adiciona tarefa ESPERA para a alimentadora
        duracao = (dataInicio - dataAnteriorEmbarcacao).total_seconds() / 3600
        if duracao > 0:
            nomeMacro = "Embarcação em espera " + \
                str(self._nome) + " desde " + dataAnteriorEmbarcacao.strftime(
                    '%d/%m/%y %H:%M:%S')
            cronograma.adicionarMacroatividade(self.nomeTarefa(), nomeMacro)

            nomeMicro = "Esperando instaladora estar disponível " + \
                str(embarcacaoDestino.getNome())

            cronograma.adicionarMicroatividade(
                self.nomeTarefa(), nomeMacro, nomeMicro, TipoMicroatividade.ESPERA, duracao)
            print(" ")
            print("Tarefa: ", self.nomeTarefa())
            print("Macroatividade: ", nomeMacro)
            print("Atividade: ", nomeMicro)
            print("Duração: ", duracao)

            cronograma.executarMacroatividade(
                self.nomeTarefa(), nomeMacro, dataAnteriorEmbarcacao)

        # Adiciona tarefa ESPERA para a instaladora
        duracao = (dataInicio - embarcacaoDestino.getDataAtual()
                   ).total_seconds() / 3600
        if duracao > 0:
            nomeMacro = "Embarcação em espera " + \
                str(embarcacaoDestino.getNome()) + \
                " desde " + embarcacaoDestino.getDataAtual().strftime('%d/%m/%y - %H:%M:%S')
            cronograma.adicionarMacroatividade(
                embarcacaoDestino.nomeTarefa(), nomeMacro)

            nomeMicro = "Esperando alimentadora estar disponível " + \
                str(self._nome)

            cronograma.adicionarMicroatividade(
                embarcacaoDestino.nomeTarefa(), nomeMacro, nomeMicro, TipoMicroatividade.ESPERA, duracao)
            print(" ")
            print("Tarefa: ", embarcacaoDestino.nomeTarefa())
            print("Macroatividade: ", nomeMacro)
            print("Atividade: ", nomeMicro)
            print("Duração: ", duracao)

            cronograma.executarMacroatividade(
                embarcacaoDestino.nomeTarefa(), nomeMacro,  embarcacaoDestino.getDataAtual())

        # Iniciar transferencia
        nomeTurbinas = '[' + ', '.join(map(str, turbinasDeck)) + ']'

        nomeMacro = "Transferindo kits " + nomeTurbinas + " para a embarcação " + \
            str(embarcacaoDestino.getNome())
        nomeMacroDestino = "Recebendo kits " + \
            nomeTurbinas + " da embarcação " + str(self._nome)

        cronograma.adicionarMacroatividade(self.nomeTarefa(), nomeMacro)
        cronograma.adicionarMacroatividade(
            embarcacaoDestino.nomeTarefa(), nomeMacroDestino)

        embarcacaoDestino.setDataAtual(dataInicio)
        for id in turbinasDeck:
            embarcacaoDestino.addKitNoDeck(conjuntosTransportados[id])
            self.removeKitDoDeck(conjuntosTransportados[id])
            componentes = conjuntosTransportados[id].getListaComponentes()
            for componente in componentes:
                infoComponente = "componente (" + \
                    componente.getTipoComponente() + " - ID " + str(id) + ")"
                nomeMicro = "Aguardando transferencia do " + infoComponente
                nomeMicroDestino = "Subir " + infoComponente + " para a embarcação"
                duracao = embarcacaoDestino.getGuindaste(
                ).calcular_tempo_movimentacao(componente.getAltura())
                cronograma.adicionarMicroatividade(
                    self.nomeTarefa(), nomeMacro, nomeMicro, TipoMicroatividade.TRANSBORDO, duracao)
                print(" ")
                print("Tarefa: ", self.nomeTarefa())
                print("Macroatividade: ", nomeMacro)
                print("Atividade: ", nomeMicro)
                print("Duração: ", duracao)

                cronograma.adicionarMicroatividade(embarcacaoDestino.nomeTarefa(
                ), nomeMacroDestino, nomeMicroDestino, TipoMicroatividade.TRANSBORDO, duracao)
                print(" ")
                print("Tarefa: ", embarcacaoDestino.nomeTarefa())
                print("Macroatividade: ", nomeMacroDestino)
                print("Atividade: ", nomeMicroDestino)
                print("Duracao: ", duracao)

        cronograma.executarMacroatividade(
            self.nomeTarefa(), nomeMacro, dataInicio)
        cronograma.executarMacroatividade(
            embarcacaoDestino.nomeTarefa(), nomeMacroDestino, dataInicio)
        dataFim = cronograma.getDataFimMacroatividade(
            self.nomeTarefa(), nomeMacro)
        dataFimDestino = cronograma.getDataFimMacroatividade(
            embarcacaoDestino.nomeTarefa(), nomeMacroDestino)
        print("Transferência executando para barcaça")
        print("Data início: ", dataInicio)
        print("Data fim: ", dataFim)
        print("Transferência executando para WTIV")
        print("Data início: ", dataInicio)
        print("Data fim: ", dataFimDestino)
        self._dataAtual = dataFim
        embarcacaoDestino.setDataAtual(dataFimDestino)
        embarcacaoDestino.conjuntosTransportados = conjuntosTransportados
        embarcacaoDestino.turbinasDeck = turbinasDeck

        for id in turbinasDeck:
            if id in self.conjuntosTransportados:
                del self.conjuntosTransportados[id]
            if id in self.turbinasDeck:
                self.turbinasDeck.remove(id)

    def executarInstalacao(self, cronograma, idTurbina, parque):
        profundidade = self.parque.profundidadeTurbina[idTurbina]
        conjunto = self.conjuntosTransportados[idTurbina]
        dataFim = conjunto.executarInstalacao(
            cronograma, self.solucaoEmbarcacao.wtiv, self._dataAtual, profundidade)

    def limparEmbarcacao(self, dataInicio):
        self.setDataInicio(dataInicio)
        self.setDataAtual(dataInicio)
        self.setNumeroViagemAtividade(0)

    def getNome(self):
        return self._nome

    def getAreaDeck(self):
        return self._area_deck

    def getMaximaCapacidadeCargaDeck(self):
        return self._maxima_capacidade_carga_deck

    def getVelocidadeCarregado(self):
        return self._velocidade_locomocao_carregado

    def getVelocidadeVazio(self):
        return self._velocidade_locomocao_vazio

    def getVelocidade(self):
        if len(self.deck) == 0:
            return self.getVelocidadeVazio()
        else:
            return self.getVelocidadeCarregado()

    def getTaxaDiaria(self):
        return self._taxa_diaria

    def getGuindaste(self):
        return self._guindaste

    def getPosicao(self):
        return self._posicao

    def getNumeroViagem(self):
        return self._viagem

    def setNumeroViagem(self, numero):
        self._viagem = numero

    def getNumeroViagemAtividade(self):
        return self._viagemAtividade

    def setNumeroViagemAtividade(self, numero):
        self._viagemAtividade = numero

    def getDataAtual(self):
        return self._dataAtual

    def setDataAtual(self, dataAtual):
        self._dataAtual = dataAtual

    def getDataInicio(self):
        return self._dataInicio

    def setDataInicio(self, dataInicio):
        self._dataInicio = dataInicio

    def getAreaTotalTransportada(self):
        return self._areaTotalTransportada

    def getTaxaMobilizacao(self):
        return self._taxa_mobilizacao
    
    def getMaxAlturaOnda(self):
        return self._maxima_altura_onda
    
    def getMaxVelocidadeVento(self):
        return self._maxima_velocidade_vento
