from ...utils.utils import str_to_float
from .Componentes.Jaqueta import Jaqueta
from .Componentes.PecaTransicao import PecaTransicao
from .ConjuntosComponentes.ConjuntoJaqueta import ConjuntoJaqueta, TipoConexao
from .Instalacao.SimulacaoInstalacaoFundacaoSubestacaoOffshore import SimulacaoInstalacaoFundacaoSubestacaoOffshore
from .Instalacao.SimulacaoInstalacaoSubestacao import SimulacaoInstalacaoSubestacao
from .Componentes.SubestacaoOffshore import SubestacaoOffshore
from .ConjuntosComponentes.ConjuntoSubestacao import ConjuntoSubestacao
from .Entidades.PontoInstalacao import PontoInstalacao
from .Entidades.PlantaSubestacao import PlantaSubestacao
from .Entidades.PlantaRoteamentoCabos import PlantaRoteamentoCabos
from .Componentes.SecaoCabo import SecaoCabo
from .Entidades.PlantaRoteamentoCabos import PlantaRoteamentoCabos
from .Entidades.Turbina import Turbina
from .ConjuntosComponentes.ConjuntoSecaoCabo import ConjuntoSecaoCabo
from .ConjuntosComponentes.ConjuntoSecaoCaboExportacaoOnshore import ConjuntoSecaoCaboExportacaoOnshore
from .Instalacao.SimulacaoInstalacaoSistemaArray import SimulacaoInstalacaoSistemaArray
from .Instalacao.SimulacaoInstalacaoCaboExportacaoOnshore import SimulacaoInstalacaoCaboExportacaoOnshore
from .Instalacao.SimulacaoInstalacaoCaboExportacaoOffshore import SimulacaoInstalacaoCaboExportacaoOffshore
from .Entidades.PlantaCabosExportacaoOnshore import PlantaCabosExportacaoOnshore
from .Entidades.PlantaCabosExportacaoOffshore import PlantaCabosExportacaoOffshore
from .ConjuntosComponentes.ConjuntoSecaoCaboExportacaoOffshore import ConjuntoSecaoCaboExportacaoOffshore
from .Clima.Previsao import previsaoClima
from .Clima.CorrigirCronograma import corrigirCronograma, gerarCronogramaCorrigido
from .Enrocamento.Enrocamento import Enrocamento


class Electric:
    def __init__(self, ui, webview, params_constrain, project, params, filtered_vessels, vessels, general, data_inicio=None):

        self.ui = ui
        self.webview = webview
        self.params_constrain = params_constrain
        self.project = project
        self.params = params
        self.filtered_vessels = filtered_vessels
        self.table_vessels = vessels
        self.general = general
        self.data_inicio = data_inicio

        self.results = {}
        self.data_fim = None

        self.run()

    def run(self):
        """Executar construtibilidade aerogerador"""
        parque = self.general.get_parque()
        porto = self.general.get_porto()
        solucao_embarcacao_subestacao = self.general.get_solucao_embarcacao_fundacao_subestacao(
            self.filtered_vessels, self.table_vessels)

        solucao_embarcacao_cabos = self.general.get_solucao_embarcacao_cabos(
            self.filtered_vessels, self.table_vessels)

        solucao_embarcacao_enroncamento = self.general.get_solucao_embarcacao_enrocamento(
            self.filtered_vessels, self.table_vessels)

        if self.data_inicio == None:
            self.data_inicio = parque.getDataInicioInstalacao()

        cronograma = self.general.get_cronograma(parque, self.data_inicio)

        # 1º e 2º
        kits_fundacoes = self.get_conjuntos_subestacao(1)  # 1º
        planta_subestacao = self.get_planta_subestacao()  # 1º e 2º
        kits_subestacoes = self.get_conjuntos_subestacao(2)  # 2º

        # 3º
        kits_secoes_cabos = self.get_kits_secoes_cabos()  # 3º
        planta_roteamento = self.get_planta_roteamento_cabos()  # 3º

        # 4º Cabo de exportação offShore
        kits_secoes_cabos_exportacao_offshore = self.get_kits_secoes_cabos_exportacao_offshore()  # 4º
        planta_cabos_exportacao_offshore = self.get_planta_cabos_exportacao_offshore()

        # Primeiro - Fundação subestação
        fundacao = "subestacao"
        lista_tarefas = []
        instalacao = SimulacaoInstalacaoFundacaoSubestacaoOffshore(
            self.data_inicio, parque, porto, planta_subestacao, kits_fundacoes, solucao_embarcacao_subestacao)
        instalacao.executarInstalacao(cronograma)

        html, lista_config = cronograma.obterGraficoGantt(
            "1-Fundacao_Subestação1.html")

        data_fim = instalacao.get_data_fim()
        cronograma.setDataAtual(data_fim)

        if not self.params_constrain["constrain"]:
            self.webview.setHtml(html)
        else:
            # Obtém o cronograma inicial
            lista_cron = lista_config[0]

            # Calcula o tempo disponível com base nas condições climáticas
            tempo_disp = previsaoClima(
                solucao_embarcacao_subestacao, self.params_constrain)

            # Ajusta o cronograma com base no tempo disponível
            cron_corrigido = corrigirCronograma(lista_cron, tempo_disp)

            # Atualiza a lista de configurações com o cronograma corrigido
            lista_config[0] = cron_corrigido

            # Gera o HTML para o cronograma corrigido e atualiza a exibição
            html = gerarCronogramaCorrigido(
                lista_config, "1-Fundacao_Subestação2.html")
            self.webview.setHtml(html)

        self.results["Fundação da subestação"] = instalacao.calcularCustoEmbarcacoes()

        # Segundo - Subestação
        solucao_embarcacao_subestacao.limparEmbarcacoes(data_fim)
        instalacao = SimulacaoInstalacaoSubestacao(
            data_fim, parque, porto, planta_subestacao, kits_subestacoes, solucao_embarcacao_subestacao)
        instalacao.executarInstalacao(cronograma)
        data_fim = instalacao.get_data_fim()
        cronograma.setDataAtual(data_fim)

        html, lista_config = cronograma.obterGraficoGantt(
            "2-Subestação1.html")

        if not self.params_constrain["constrain"]:
            self.webview.setHtml(html)
        else:
            # Obtém o cronograma inicial
            lista_cron = lista_config[0]

            # Calcula o tempo disponível com base nas condições climáticas
            tempo_disp = previsaoClima(
                solucao_embarcacao_subestacao, self.params_constrain)

            # Ajusta o cronograma com base no tempo disponível
            cron_corrigido = corrigirCronograma(lista_cron, tempo_disp)

            # Atualiza a lista de configurações com o cronograma corrigido
            lista_config[0] = cron_corrigido

            # Gera o HTML para o cronograma corrigido e atualiza a exibição
            html = gerarCronogramaCorrigido(
                lista_config, "2-Subestação2.html")
            self.webview.setHtml(html)

        self.results["Subestação"] = instalacao.calcularCustoEmbarcacoes()

        # Terceiro - Sistema
        instalacao = SimulacaoInstalacaoSistemaArray(data_fim,
                                                     parque,
                                                     porto,
                                                     planta_roteamento,
                                                     kits_secoes_cabos,
                                                     solucao_embarcacao_cabos)
        instalacao.executarInstalacao(cronograma)
        data_fim = instalacao.get_data_fim()
        cronograma.setDataAtual(data_fim)

        html, lista_config = cronograma.obterGraficoGantt(
            "3-SistemaArray1.html")

        if not self.params_constrain["constrain"]:
            self.webview.setHtml(html)
        else:
            # Obtém o cronograma inicial
            lista_cron = lista_config[0]

            # Calcula o tempo disponível com base nas condições climáticas
            tempo_disp = previsaoClima(
                solucao_embarcacao_cabos, self.params_constrain)

            # Ajusta o cronograma com base no tempo disponível
            cron_corrigido = corrigirCronograma(lista_cron, tempo_disp)

            # Atualiza a lista de configurações com o cronograma corrigido
            lista_config[0] = cron_corrigido

            # Gera o HTML para o cronograma corrigido e atualiza a exibição
            html = gerarCronogramaCorrigido(
                lista_config, "3-SistemaArray2.html")
            self.webview.setHtml(html)

        self.results["Sistema array"] = instalacao.calcularCustoEmbarcacoes()

        # Quarto - Cabo de exportação OffShore
        solucao_embarcacao_cabos.limparEmbarcacoes(data_fim)
        instalacao = SimulacaoInstalacaoCaboExportacaoOffshore(data_fim,
                                                               parque,
                                                               porto,
                                                               planta_cabos_exportacao_offshore,
                                                               kits_secoes_cabos_exportacao_offshore,
                                                               solucao_embarcacao_cabos)
        instalacao.executarInstalacao(cronograma)

        lista_tarefas = Enrocamento(porto,
                                    planta_subestacao,
                                    str_to_float(
                                        self.ui.edtVolumeScourJacketSubstation.text()),
                                    cronograma,
                                    fundacao,
                                    solucao_embarcacao_enroncamento,
                                    solucao_embarcacao_subestacao)

        html, lista_config = cronograma.obterGraficoGantt2(
            lista_tarefas, "4-Cabo_Exportação_Offshore1.html")

        if not self.params_constrain["constrain"]:
            self.webview.setHtml(html)
        else:
            # Obtém o cronograma inicial
            lista_cron = lista_config[0]

            # Calcula o tempo disponível com base nas condições climáticas
            tempo_disp = previsaoClima(
                solucao_embarcacao_cabos, self.params_constrain)

            # Ajusta o cronograma com base no tempo disponível
            cron_corrigido = corrigirCronograma(lista_cron, tempo_disp)

            # Atualiza a lista de configurações com o cronograma corrigido
            lista_config[0] = cron_corrigido

            # Gera o HTML para o cronograma corrigido e atualiza a exibição
            html = gerarCronogramaCorrigido(
                lista_config, "5-Cabo_Exportação_Offshore2.html")
            self.webview.setHtml(html)

        self.enrocamento = instalacao.calcularCustoEmbarcacoes_enrocamento(lista_tarefas,
                                                                           solucao_embarcacao_enroncamento)

        self.results["Cabo exportação offshore"] = instalacao.calcularCustoEmbarcacoes()

        self.data_fim = instalacao.get_data_fim()

    def get_conjuntos_subestacao(self, tipo):
        """Define conjuntos de fundação de subestação ou de subestações
           tipo = 1 >> Fundação da Subestação
           tipo = 2 >> Subestação
        """
        conjuntos = dict()
        pontos_instalacao = self.params["clusters"]
        for id in pontos_instalacao:
            if tipo == 1:
                kit = self.get_conjunto_jaqueta_subestacao(id)
            if tipo == 2:
                kit = self.get_conjunto_subestacao(id)
            conjuntos[id] = kit
        return conjuntos

    def get_planta_subestacao(self):
        # id,latitude,longitude,profundidade
        conjuntos = dict()
        pontos_instalacao = self.params["clusters"]
        for id in pontos_instalacao:
            subestacao = PontoInstalacao(
                id, pontos_instalacao[id].y(), pontos_instalacao[id].x(), self.params["bathymetry_local"])
            conjuntos[subestacao.getId()] = subestacao

        planta = PlantaSubestacao(conjuntos)
        return planta

    def get_conjunto_jaqueta_subestacao(self, id):
        """Define um conjunto de fundação de subestação"""

        # Criando uma jaqueta diametro, altura, massa):
        jaqueta = Jaqueta(str_to_float(self.ui.edtDiameterJacketSubstation.text()), 
                          str_to_float(self.ui.edtHeightJacketSubstation.text()), 
                          str_to_float(self.ui.edtWeightJacketSubstation.text()))

        # Criando uma peca de transicao
        peca_transicao = PecaTransicao(0, 0, 0)

        # Criando o kit jaqueta
        tipo_conexao = TipoConexao.PARAFUSO

        conjunto_jaqueta = ConjuntoJaqueta(
            id, jaqueta, peca_transicao, tipo_conexao)

        # Dados que o usuário pode alterar se desejar (usar as funcoes sets para isso)
        # [h] >>> tempo de pesquisar o fundo do mar com o ROV para definir exatamente o ponto de instalação
        conjunto_jaqueta.setTempoPesquisaComRov(
            self.ui.spbCJTempoPesquisaComRov.value())

        # [h] >>> tempo de liberar a jaqueta do deck de uma embarcação
        conjunto_jaqueta.setTempoLiberarJaquetaDeck(
            self.ui.spbCJTempoLiberar.value())

        # [h] >>> tempo de reequipar o guindaste para conduzir a jaqueta
        conjunto_jaqueta.setTempoPrepararEquipamentoConducao(
            self.ui.spbCJTempoPrepararEquipamentoConducao.value())

        # [h] >>> tempo de reequipar o guindaste para elevar as pecas
        conjunto_jaqueta.setTempoPrepararEquipamentoElevacao(
            self.ui.spbCJTempoPrepararEquipamentoElevacao.value())

        # [m/h] >>> "velocidade" em que a jaqueta é cravada
        conjunto_jaqueta.setTaxaConducaoJaqueta(
            self.ui.spbCJTaxaConducao.value())

        # [h] >>> tempo para parafusar a peca de transicao com a jaqueta
        conjunto_jaqueta.setTempoParafusarConexao(0)

        # [h] >>> tempo para aplicar a armagasse entre a peca de transicao com a jaqueta
        conjunto_jaqueta.setTempoAplicarArgamassaConexao(0)

        # [h] >>> tempo para secagem da argamassa
        conjunto_jaqueta.setTempoCuraArgamassa(0)

        # [m] >>> comprimento de cravacao da jaqueta
        conjunto_jaqueta.setComprimentoIncorporacao(
            self.ui.spbCJComprimentoIncorporacao.value())

        return conjunto_jaqueta

    def get_conjunto_subestacao(self, id):
        """Define um conjunto de subestação"""

        # Criando um subestacao - comprimento, largura, altura, massa
        subestacao = SubestacaoOffshore(self.params["dim"]["length"],
                                        self.params["dim"]["width"],
                                        self.params["dim"]["height"],
                                        self.params["dim"]["weight"])

        # Criando o kit subestacao
        conjunto_subestacao = ConjuntoSubestacao(id, subestacao)

        # Dados que o usuário pode alterar se desejar (usar as funcoes sets para isso)
        # [h] >>> tempo de fixar a subestacao no deck de uma embarcacao
        subestacao.setTempoFixacaoDeck(self.ui.spbSubstationFixar.value())
        # [h] >>> tempo de liberar a subestacao do deck de uma embarcacao
        subestacao.setTempoLiberacaoDeck(self.ui.spbSubstationLiberar.value())
        # [h] >>> tempo de anexar a subestacao na fundacao
        subestacao.setTempoAnexarSubestacaoNaFundacao(
            self.ui.spbSubstationAnexar.value())

        return conjunto_subestacao

    def get_kits_secoes_cabos(self):
        """Define um kit de secões de cabos"""
        conjuntos_secao_cabo = dict()
        id = 0
        lines = self.params["cables"]
        for line in lines:
            for coord in line:
                # (diametro [mm], densidade [kg/m],comprimento)
                secao = SecaoCabo(coord[2], coord[3], coord[4])
                pontoInicio = Turbina(
                    id, coord[0].y(), coord[0].x(), self.params["bathymetry_local"])
                pontoFim = Turbina(
                    id+1, coord[1].y(), coord[1].x(), self.params["bathymetry_local"])
                kit_secao_cabo = ConjuntoSecaoCabo(
                    pontoInicio.getId(), pontoInicio, pontoFim, secao)
                conjuntos_secao_cabo[pontoInicio.getId()] = kit_secao_cabo
                id = id + 1

        return conjuntos_secao_cabo

    def get_planta_roteamento_cabos(self):
        """Define planta das turbinas"""
        roteamento = dict()
        parque = self.general.get_parque()
        turbinas = parque.getPlanta().getPontos()
        for id, turbina in turbinas.items():
            secao0 = PontoInstalacao(
                id, turbina._latitude, turbina._longitude, self.params["bathymetry_local"])
            roteamento[secao0.getId()] = secao0

        return PlantaRoteamentoCabos(roteamento)

    def get_kits_secoes_cabos_exportacao_offshore(self):
        """Define um kit de secões de cabos do ponto mais próximo da costa até o centro do polígono"""
        conjuntos_secao_cabo = dict()

        # (diametro [mm], densidade [kg/m],comprimento [m])
        secao = SecaoCabo(self.params["export_cable"]["diameter"],
                          self.params["export_cable"]["density"],
                          self.params["export_cable"]["length"])
        # id,latitude,longitude,profundidade
        ponto_costeiro = PontoInstalacao("PONTO_COSTEIRO", self.params["point_coast"].y(
        ), self.params["point_coast"].x(), 0)
        ponto_offshore = PontoInstalacao("SUB_B", self.params["point_central"].y(
        ), self.params["point_central"].x(), 0)

        conjuntos_secao_cabo[ponto_costeiro.getId()] = ConjuntoSecaoCaboExportacaoOffshore(
            ponto_costeiro.getId(), ponto_costeiro, ponto_offshore, secao)

        return conjuntos_secao_cabo

    def get_planta_cabos_exportacao_offshore(self):
        # id,latitude,longitude,profundidade
        ponto_costeiro = PontoInstalacao("PONTO_COSTEIRO", self.params["point_coast"].y(
        ), self.params["point_coast"].x(), 0)

        roteamento = dict()
        roteamento[ponto_costeiro.getId()] = ponto_costeiro

        return PlantaCabosExportacaoOffshore(roteamento)
