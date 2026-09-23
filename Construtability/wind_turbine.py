from PyQt5.QtWidgets import QMessageBox
import math
from .Componentes.SecaoTorre import SecaoTorre
from .Componentes.Hub import Hub
from .Componentes.Nacele import Nacele
from .Componentes.Pa import Pa
from .Componentes.Derivados.Torre import Torre
from .Componentes.Derivados.Estrela import Estrela
from .Componentes.Derivados.OrelhaCoelhoNacele import OrelhaCoelhoNacele
from .Componentes.Derivados.AerogeradorCompleto import AerogeradorCompleto
from .ConjuntosComponentes.ConjuntoAerogeradorMetodo1 import ConjuntoAerogeradorMetodo1
from .ConjuntosComponentes.ConjuntoAerogeradorMetodo2 import ConjuntoAerogeradorMetodo2
from .ConjuntosComponentes.ConjuntoAerogeradorMetodo3 import ConjuntoAerogeradorMetodo3
from .ConjuntosComponentes.ConjuntoAerogeradorMetodo4 import ConjuntoAerogeradorMetodo4
from .ConjuntosComponentes.ConjuntoAerogeradorMetodo5 import ConjuntoAerogeradorMetodo5
from .ConjuntosComponentes.ConjuntoAerogeradorMetodo6 import ConjuntoAerogeradorMetodo6
from .Instalacao.SimulacaoInstalacaoAerogerador import SimulacaoInstalacaoAerogerador
from .Clima.Previsao import previsaoClima
from .Clima.CorrigirCronograma import corrigirCronograma, gerarCronogramaCorrigido
from ...utils.utils import str_to_float


class WindTurbine:
    def __init__(self, ui, webview, params_constrain, filtered_vessels, vessels, general, data_inicio=None):

        self.ui = ui
        self.webview = webview
        self.params_constrain = params_constrain
        self.filtered_vessels = filtered_vessels
        self.table_vessels = vessels
        self.general = general
        self.data_inicio = data_inicio

        self.params = {}
        self.results = {}
        self.data_fim = None

        self.run()

    def run(self):
        """Executar construtibilidade aerogerador"""
        self.params = self.get_params()
        parque = self.general.get_parque()
        porto = self.general.get_porto()
        kits_aerogeradores = self.get_conjuntos_aerogeradores(parque)
        solucao_embarcacao = self.general.get_solucao_embarcacao(
            self.filtered_vessels, self.table_vessels)

        if self.data_inicio == None:
            self.data_inicio = parque.getDataInicioInstalacao()

        cronograma = self.general.get_cronograma(parque, self.data_inicio)

        instalacao = SimulacaoInstalacaoAerogerador(
            self.data_inicio, parque, porto, kits_aerogeradores, solucao_embarcacao)
        instalacao.executarInstalacao(cronograma)

        html, lista_config = cronograma.obterGraficoGantt(
            "Teste_Instalacao_Aerogerador1.html")

        if not self.params_constrain["constrain"]:
            self.webview.setHtml(html)
            self.results = instalacao.calcularCustoEmbarcacoes()
        else:
            # Obtém o cronograma inicial
            lista_cron = lista_config[0]

            # Calcula o tempo disponível com base nas condições climáticas
            tempo_disp = previsaoClima(
                solucao_embarcacao, self.params_constrain)

            # Ajusta o cronograma com base no tempo disponível
            cron_corrigido = corrigirCronograma(lista_cron, tempo_disp)

            # Atualiza a lista de configurações com o cronograma corrigido
            lista_config[0] = cron_corrigido

            # Gera o HTML para o cronograma corrigido e atualiza a exibição
            html = gerarCronogramaCorrigido(
                lista_config, "Teste_Instalacao_Aerogerador2.html")
            self.webview.setHtml(html)
            self.results = instalacao.calcularCustoEmbarcacoes_clima(
                cron_corrigido, solucao_embarcacao)

        self.data_fim = instalacao.get_data_fim()

    def get_conjuntos_aerogeradores(self, parque):
        """Define conjuntos de Aerogerador"""
        conjuntos_aerogerador = dict()
        parque = self.general.get_parque()
        turbinas = parque.getPlanta().getPontos()
        for id in turbinas:
            if self.ui.rdb1.isChecked():
                kit_aerogerador = self.get_conjunto_aerogerador_metodo1(id)
            elif self.ui.rdb2.isChecked():
                kit_aerogerador = self.get_conjunto_aerogerador_metodo2(id)
            elif self.ui.rdb3.isChecked():
                kit_aerogerador = self.get_conjunto_aerogerador_metodo3(id)
            elif self.ui.rdb4.isChecked():
                kit_aerogerador = self.get_conjunto_aerogerador_metodo4(id)
            elif self.ui.rdb5.isChecked():
                kit_aerogerador = self.get_conjunto_aerogerador_metodo5(id)
            elif self.ui.rdb6.isChecked():
                kit_aerogerador = self.get_conjunto_aerogerador_metodo6(id)

            conjuntos_aerogerador[id] = kit_aerogerador
        return conjuntos_aerogerador

    def get_conjunto_aerogerador_metodo1(self, id):
        """Define um conjunto de Aerogerador para o Metódo 1"""

        secoes_torre = self.get_sessoes_torre()
        nacele = self.get_nacele()
        hub = self.get_hub()
        pa1 = self.get_pa(1)
        pa2 = self.get_pa(2)
        pa3 = self.get_pa(3)

        # Criando um kit aerogerador com metodo pre-montagem 1
        conjunto_aerogerador_metodo1 = ConjuntoAerogeradorMetodo1(
            id, secoes_torre, nacele, hub, pa1, pa2, pa3)

        return conjunto_aerogerador_metodo1

    def get_conjunto_aerogerador_metodo2(self, id):
        """Define um conjunto de Aerogerador para o Metódo 2"""

        torre = self.get_torre()
        nacele = self.get_nacele()
        hub = self.get_hub()
        pa1 = self.get_pa(1)
        pa2 = self.get_pa(2)
        pa3 = self.get_pa(3)

        # Criando um kit aerogerador com metodo pre-montagem 2
        conjunto_aerogerador_metodo2 = ConjuntoAerogeradorMetodo2(
            id, torre, nacele, hub, pa1, pa2, pa3)

        return conjunto_aerogerador_metodo2

    def get_conjunto_aerogerador_metodo3(self, id):
        """Define um conjunto de Aerogerador para o Metódo 3"""

        secoes_torre = self.get_sessoes_torre()
        nacele = self.get_nacele()
        estrela = self.get_estrela()

        # Criando um kit aerogerador com metodo pre-montagem 3
        conjunto_aerogerador_metodo3 = ConjuntoAerogeradorMetodo3(
            id, secoes_torre, nacele, estrela)

        return conjunto_aerogerador_metodo3

    def get_conjunto_aerogerador_metodo4(self, id):
        """Define um conjunto de Aerogerador para o Metódo 4"""

        secoes_torre = self.get_sessoes_torre()

        orelha_coelho = self.get_orelha_coelho_nacele()
        pa = self.get_pa(1)

        # Criando um kit aerogerador com metodo pre-montagem 4
        conjunto_aerogerador_metodo4 = ConjuntoAerogeradorMetodo4(
            id, secoes_torre, orelha_coelho, pa)

        return conjunto_aerogerador_metodo4

    def get_conjunto_aerogerador_metodo5(self, id):
        """Define um conjunto de Aerogerador para o Metódo 5"""

        torre = self.get_torre()
        orelha_coelho = self.get_orelha_coelho_nacele()
        pa = self.get_pa(1)

        # Criando um kit aerogerador com metodo pre-montagem 5
        conjunto_aerogerador_metodo5 = ConjuntoAerogeradorMetodo5(
            id, torre, orelha_coelho, pa)

        return conjunto_aerogerador_metodo5

    def get_conjunto_aerogerador_metodo6(self, id):
        """Define um conjunto de Aerogerador para o Metódo 6"""

        aerogerador_completo = self.get_aerogerador_completo()

        # Criando um kit aerogerador com metodo pre-montagem 6
        conjunto_aerogerador_metodo6 = ConjuntoAerogeradorMetodo6(
            id, aerogerador_completo)

        return conjunto_aerogerador_metodo6

    def get_sessoes_torre(self):
        """Define uma lista de sessões de torre"""
        # diametro, altura, massa

        tower_height = self.params["tower_height"]
        section_tower_height = self.params["tower_height"]/3
        tower_weight = self.params["tower_weight"]

        if (self.params["tower_diameter_top"] == self.params["tower_diameter_base"]):
            section_tower_diameter = self.params["tower_diameter_base"]
            section_tower_weight = self.params["tower_weight"]/3

            secao_torre1 = SecaoTorre(
                1, section_tower_diameter, section_tower_height, section_tower_weight)
            secao_torre2 = SecaoTorre(
                2, section_tower_diameter, section_tower_height, section_tower_weight)
            secao_torre3 = SecaoTorre(
                3, section_tower_diameter, section_tower_height, section_tower_weight)

        else:
            R = self.params["tower_diameter_base"]
            r = self.params["tower_diameter_top"]
            V = 1/3 * math.pi * tower_height * (R**2 + R*r + r**2)

            R_tronco1 = R
            r_tronco1 = R - (R-r)/3
            V_1 = 1/3 * math.pi * section_tower_height * \
                (R_tronco1**2 + R_tronco1*r_tronco1 + r_tronco1**2)
            M_1 = tower_weight * V_1/V

            R_tronco2 = R - (R-r)/3
            r_tronco2 = R - 2*(R-r)/3
            V_2 = 1/3 * math.pi * section_tower_height * \
                (R_tronco2**2 + R_tronco2*r_tronco2 + r_tronco2**2)
            M_2 = tower_weight * V_2/V

            R_tronco3 = R - 2*(R-r)/3
            r_tronco3 = r
            V_3 = 1/3 * math.pi * section_tower_height * \
                (R_tronco3**2 + R_tronco3*r_tronco3 + r_tronco3**2)
            M_3 = tower_weight * V_3/V

            secao_torre1 = SecaoTorre(1, R_tronco1, section_tower_height, M_1)
            secao_torre2 = SecaoTorre(2, R_tronco2, section_tower_height, M_2)
            secao_torre3 = SecaoTorre(3, R_tronco3, section_tower_height, M_3)

        lista_secoes = [secao_torre1, secao_torre2, secao_torre3]

        return lista_secoes

    def get_torre(self):
        """Cria uma torre"""
        lista_secoes = self.get_sessoes_torre()

        torre = Torre(lista_secoes)

        return torre

    def get_hub(self):
        """Cria uma hub"""
        # diametro, altura, massa
        hub = Hub(self.params["hub_diameter"],
                  self.params["hub_height"],
                  self.params["hub_weight"])
        return hub

    def get_nacele(self):
        """Cria uma nacele"""
        # comprimento, largura, altura, massa
        nacele = Nacele(self.params["nacele_length"],
                        self.params["nacele_width"],
                        self.params["nacele_height"],
                        self.params["nacele_weight"])
        return nacele

    def get_pa(self, id):
        """Cria uma pá"""
        # diametro, altura, massa, capacidade_empilhamento, numero_camadas_empilhamento
        pa = Pa(id,
                self.params["blade_width"],
                self.params["blade_radius"],
                self.params["blade_weight"],
                self.params["stackability"],
                self.params["stackability_number"])
        return pa

    def get_estrela(self):
        """Cria uma estrela"""
        pa1 = self.get_pa(1)
        pa2 = self.get_pa(2)
        pa3 = self.get_pa(3)
        hub = self.get_hub()

        estrela = Estrela(hub, pa1, pa2, pa3, 1)

        return estrela

    def get_orelha_coelho_nacele(self):
        """Cria uma orelha de coelho na Nacele"""
        pa1 = self.get_pa(1)
        pa2 = self.get_pa(2)
        nacele = self.get_nacele()
        hub = self.get_hub()

        orelha_coelho_nacele = OrelhaCoelhoNacele(hub, nacele, pa1, pa2)

        return orelha_coelho_nacele

    def get_aerogerador_completo(self):
        # Criando uma aerogeradorCompleto
        secoes_torre = self.get_sessoes_torre()
        pa1 = self.get_pa(1)
        pa2 = self.get_pa(2)
        pa3 = self.get_pa(3)
        nacele = self.get_nacele()
        hub = self.get_hub()

        aerogeradorCompleto = AerogeradorCompleto(
            secoes_torre, hub, nacele, pa1, pa2, pa3)

        return aerogeradorCompleto

    def get_params(self):
        """
        Preenche a estrutura com os dados do Sistema 1
        """
        try:
            # Sessões da torre
            tower_diameter_top = str_to_float(
                self.ui.edtTowerDiameterTopoConstru.text())
            tower_diameter_base = str_to_float(
                self.ui.edtTowerDiameterBaseConstru.text())
            tower_height = str_to_float(
                self.ui.edtTowerHeightConstru.text())
            tower_weight = str_to_float(
                self.ui.edtTowerWeightConstru.text())
            # Dados da nacele
            nacele_length = str_to_float(self.ui.edtNaceleLength.text())
            nacele_width = str_to_float(self.ui.edtNaceleWidth.text())
            nacele_height = str_to_float(self.ui.edtNaceleHeight.text())
            nacele_weight = str_to_float(self.ui.edtNaceleWeight.text())
            # Dados do hub
            hub_diameter = str_to_float(self.ui.edtHubDiameter.text())
            hub_height = str_to_float(self.ui.edtHubHeight.text())
            hub_weight = str_to_float(self.ui.edtHubWeight.text())
            # Dados das pás
            blade_radius = str_to_float(
                self.ui.edtBladeRadiusContru.text())
            blade_width = str_to_float(self.ui.edtBladeWidth.text())
            blade_weight = str_to_float(self.ui.edtBladeWeight.text())

            stackability = self.ui.spbStackability.value()
            stackability_number = self.ui.spbStackabilityNumber.value()

            return {
                # Sessões da torre
                'tower_diameter_top': tower_diameter_top,
                'tower_diameter_base': tower_diameter_base,
                'tower_height': tower_height,
                'tower_weight': tower_weight,
                # Dados da nacele
                'nacele_length': nacele_length,
                'nacele_width': nacele_width,
                'nacele_height': nacele_height,
                'nacele_weight': nacele_weight,
                # Dados do hub
                'hub_diameter': hub_diameter,
                'hub_height': hub_height,
                'hub_weight': hub_weight,
                # Dados das pás
                'blade_radius': blade_radius,
                'blade_width': blade_width,
                'blade_weight': blade_weight,
                'stackability': stackability,
                'stackability_number': stackability_number
            }
        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar dados o aerogerador.\n\n'
                                 f'Problema: {ex}')
