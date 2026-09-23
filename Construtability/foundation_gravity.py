from .Componentes.Gravidade import Gravidade
from .ConjuntosComponentes.ConjuntoGravidade import ConjuntoGravidade
from .Instalacao.SimulacaoInstalacaoGravidade import SimulacaoInstalacaoGravidade
from .Clima.Previsao import previsaoClima
from .Clima.CorrigirCronograma import corrigirCronograma, gerarCronogramaCorrigido
from ...utils.utils import str_to_float
from .Enrocamento.Enrocamento import Enrocamento


class FoundationGravity:
    def __init__(self, ui, webview, params_constrain, filtered_vessels, vessels, general):

        self.ui = ui
        self.webview = webview
        self.params_constrain = params_constrain
        self.filtered_vessels = filtered_vessels
        self.table_vessels = vessels
        self.general = general

        self.results = {}
        self.data_fim = None

        self.run()

    def run(self):
        """Executar construtibilidade fundação"""
        fundacao = "gravidade"
        parque = self.general.get_parque()
        porto = self.general.get_porto()
        kits_fundacoes = self.get_conjuntos_gravidade(parque)
        solucao_embarcacao = self.general.get_solucao_embarcacao_gravity(
            self.filtered_vessels, self.table_vessels)
        solucao_embarcacao_enroncamento = self.general.get_solucao_embarcacao_enrocamento(
            self.filtered_vessels, self.table_vessels)
        cronograma = self.general.get_cronograma(parque)

        instalacao = SimulacaoInstalacaoGravidade(
            parque, porto, kits_fundacoes, solucao_embarcacao)
        instalacao.executarInstalacao(cronograma)

        lista_tarefas = Enrocamento(porto,
                                    parque,
                                    str_to_float(
                                        self.ui.edtVolumeScourGravity.text()),
                                    cronograma,
                                    fundacao,
                                    solucao_embarcacao_enroncamento,
                                    solucao_embarcacao)

        html, lista_config = cronograma.obterGraficoGantt2(
            lista_tarefas, "Teste_Instalacao_Gravidade1.html")

        if not self.params_constrain["constrain"]:
            self.webview.setHtml(html)
            self.results = instalacao.calcularCustoEmbarcacoes()
            self.enrocamento = instalacao.calcularCustoEmbarcacoes_enrocamento(lista_tarefas,
                                                                               solucao_embarcacao_enroncamento)
        else:
            # Obtém o cronograma inicial
            lista_tarefas = lista_config[0]

            # Calcula o tempo disponível com base nas condições climáticas
            tempo_disp = previsaoClima(
                solucao_embarcacao, self.params_constrain)

            # Ajusta o cronograma com base no tempo disponível
            lista_tarefas = corrigirCronograma(lista_tarefas, tempo_disp)

            # Atualiza a lista de configurações com o cronograma corrigido
            lista_config[0] = lista_tarefas

            # Gera o HTML para o cronograma corrigido e atualiza a exibição
            html = gerarCronogramaCorrigido(
                lista_config, "Teste_Instalacao_Gravidade2.html")
            self.webview.setHtml(html)
            self.results = instalacao.calcularCustoEmbarcacoes_clima(
                lista_tarefas, solucao_embarcacao)
            self.enrocamento = instalacao.calcularCustoEmbarcacoes_enrocamento(lista_tarefas,
                                                                               solucao_embarcacao_enroncamento)

        self.data_fim = instalacao.get_data_fim()

    def get_conjuntos_gravidade(self, parque):
        """Define conjuntos de Gravidade"""
        conjuntos_gravidade = dict()
        parque = self.general.get_parque()
        turbinas = parque.getPlanta().getPontos()
        for id in turbinas:
            kit_gravidade = self.get_conjunto_gravidade(id)
            conjuntos_gravidade[id] = kit_gravidade
        return conjuntos_gravidade

    def get_conjunto_gravidade(self, id):
        """Define um conjunto de Gravidade"""
        # Criando uma fundação base de gravidade
        gravidade = Gravidade(str_to_float(self.ui.edtInfBase.text()), str_to_float(
            self.ui.edtInfBase.text()), str_to_float(self.ui.edtHeight.text()), str_to_float(self.ui.edtMoldVolumeMass.text()))  # (comprimento [m], largura [m], altura [m], massa [t])

        # Criando o kit base de gravidade
        conjunto_gravidade = ConjuntoGravidade(id, gravidade)

        # Dados que o usuário pode alterar se desejar (usar as funcoes sets para isso)
        # [h] >>> tempo de preparar o solo
        conjunto_gravidade.setTempoPreparacaoSolo(0)

        # [h] >>> tempo de pesquisar o fundo do mar com o ROV para definir exatamente o ponto de instalação
        conjunto_gravidade.setTempoPesquisaComRov(
            self.ui.spbJTempoPesquisaComRov.value())

        # [h] >>> tempo de posicionar
        conjunto_gravidade.setTempoPosicionar(self.ui.spbGPosicionar.value())

        # [h] >>> tempo para encher a fundacao com concreto ou outro material
        conjunto_gravidade.setTempoEnchimentoComLastro(
            self.ui.spbGEnchimentoLastro.value())

        # [h] >>> tempo para fixar a fundacao com argamassa
        conjunto_gravidade.setTempoFixarGravidadeComArgamassa(
            self.ui.spbGAplicarArgamassaConexao.value())

        return conjunto_gravidade

    def setTempoPosicionar(self, valor):
        self._posicionar = valor

    def setTempoEnchimentoComLastro(self, valor):
        self._enchimento_lastro = valor

    def setTempoFixarGravidadeComArgamassa(self, valor):
        self._tempo_fixar_gravidade_argamassa = valor
