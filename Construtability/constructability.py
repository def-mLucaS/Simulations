"""
Configurações de Construtibilidade
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QDateTime, QTime
from PyQt5.QtWidgets import QDialog, QMessageBox, QTreeWidgetItem, QButtonGroup, QTableWidgetItem
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QGuiApplication
import pandas as pd
from .vessel_monopile_jacket import VesselMonopileJacket
from .vessel_gravity import VesselGravity
from .foundation_monopile import FoundationMonopile
from .foundation_jacket import FoundationJacket
from .foundation_gravity import FoundationGravity
from .wind_turbine import WindTurbine
from .electric import Electric
from .general import General
from ...utils.utils import *
from ...utils.convert_coord import convert_coord


cfg = __import__(str(__name__).split('.')[0] + '.utils.config', fromlist=[''])


class Constructability(QtWidgets.QMainWindow):

    def __init__(self, ui):
        super(Constructability, self).__init__()

        self.ui = ui

        self.init_results_layouts()
        self.clear_results()
        self.format_tables()

        self.ui.buttonGroup = QButtonGroup(self)
        self.ui.buttonGroup.addButton(self.ui.rdb1)
        self.ui.buttonGroup.addButton(self.ui.rdb2)
        self.ui.buttonGroup.addButton(self.ui.rdb3)
        self.ui.buttonGroup.addButton(self.ui.rdb4)
        self.ui.buttonGroup.addButton(self.ui.rdb5)
        self.ui.buttonGroup.addButton(self.ui.rdb6)

        # Aba Geral - Parâmentros
        self.ui.btnGeneralParamDefault.clicked.connect(
            self.default_params_general)
        self.ui.btnGeneralParamsNext.clicked.connect(self.next_general)

        # Aba Geral - Solução de embarcações
        self.ui.btnVesselsMonopileJacketAdd.clicked.connect(
            self.add_vessels_monopile_jacket)
        self.ui.btnVesselsMonopileJacketDelete.clicked.connect(
            self.del_selected_monopile_jacket)

        self.ui.btnVesselsGravityAdd.clicked.connect(
            self.add_vessels_gravity)
        self.ui.btnVesselsGravityDelete.clicked.connect(
            self.del_selected_gravity)

        self.ui.btnGeneralVesselsNext.clicked.connect(
            self.next_vessels)

        # Aba Fundação - Geral
        self.ui.btnContruFoundationsParamsRun.clicked.connect(
            self.run_foundations)
        self.ui.btnContruFoundationsParamsDefault.clicked.connect(
            self.default_params_foundations)
        self.ui.btnFoundationContruResultsExport.clicked.connect(
            lambda: self.export_html(0))
        self.ui.btnElectricContruResultsExport.clicked.connect(
            lambda: self.export_html(1))
        self.ui.btnWindTurbineContruResultsExport.clicked.connect(
            lambda: self.export_html(2))

        # Monopile
        self.ui.cbxMConnectionType.currentIndexChanged.connect(
            self.select_connection_type)
        # Jaqueta
        self.ui.cbxJConnectionType.currentIndexChanged.connect(
            self.select_connection_type)
        self.select_connection_type()

        # Aba Cabos e Subestações
        self.ui.btnConstruElectricParamsDefault.clicked.connect(
            self.default_params_electric)
        self.ui.btnConstruElectricParamsRun.clicked.connect(self.run_electric)

        # Aba Aerogerador
        self.ui.btnWindTurbineParamNext.clicked.connect(
            self.next_wind_turbine)
        self.ui.btnWindTurbineParamsDefault.clicked.connect(
            self.default_params_wind_turbine)
        self.ui.btnWindTurbineRun.clicked.connect(
            self.run_wind_turbine)

    def init_params(self):
        """Inicializa os parâmetros de resultados."""
        # Geral
        self.project = pd.DataFrame()
        self.general = General()

        # Embarcações
        self.table_vessels = {}

        # Aerogeradores
        self.site = []

        # Electric
        self.params_electric = {}

        # Restrições
        self.params_constrain = {}

        # Contrutibilidade
        self.custo_embarcacao = None
        self.total_costs = None

    def format_tables(self):
        """Formata as tabelas."""

        # Aba Geral - Parâmentros
        self.ui.treeVesselsMonopileJacket.header().setFixedHeight(50)
        self.ui.treeVesselsMonopileJacket.header().setDefaultAlignment(
            Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
        self.ui.treeVesselsGravity.header().setFixedHeight(50)
        self.ui.treeVesselsGravity.header().setDefaultAlignment(
            Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))

        # Aba Final
        self.ui.tableConstru.horizontalHeader().setFixedHeight(50)
        self.ui.tableConstru.horizontalHeader().setDefaultAlignment(
            Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
        self.ui.btnTimelineExport.clicked.connect(self.export_timeline)
        self.ui.btnTimelineRun.clicked.connect(self.run_timeline)

        # Tables Results
        self.ui.tableImplantation.verticalHeader().setFixedWidth(200)
        self.ui.tableImplantation.verticalHeader().setDefaultSectionSize(32)
        self.ui.tableImplantation.verticalHeader().setDefaultAlignment(
            Qt.AlignVCenter | Qt.Alignment(Qt.TextWordWrap))

        self.ui.tableInstallation.verticalHeader().setFixedWidth(200)
        self.ui.tableInstallation.verticalHeader().setDefaultSectionSize(32)
        self.ui.tableInstallation.verticalHeader().setDefaultAlignment(
            Qt.AlignVCenter | Qt.Alignment(Qt.TextWordWrap))

        self.ui.tableOthers.verticalHeader().setFixedWidth(200)
        self.ui.tableOthers.verticalHeader().setDefaultSectionSize(32)
        self.ui.tableOthers.verticalHeader().setDefaultAlignment(
            Qt.AlignVCenter | Qt.Alignment(Qt.TextWordWrap))

    def set_coord_polygon(self, points, polygon):
        """Atribui os pontos da seleção da área do polígono do projeto"""
        self.params_electric["point_central"] = points[0]
        self.params_electric["point_coast"] = points[1]
        self.params_electric["point_se"] = points[2]

        self.params_constrain["constrain"] = True
        self.params_constrain["point_coast"] = points[1]
        self.params_constrain["polygon"] = polygon

    def set_costs(self, cost, value):
        """Atribui custos calculados por outras metodologias"""
        if self.total_costs is None:
            self.total_costs = {}
        self.total_costs[cost] = value

    def set_wind_turbine_site(self, wind_coordinates, selected_wind_turbine):
        """Carrega aerogeradores do módulo de aerogeradores"""

        try:
            self.site = convert_coord(wind_coordinates, True, True)
            # Sessões da torre
            self.ui.edtTowerHeightConstru.setText(
                float_to_str(selected_wind_turbine["h_hub"].values[0]))
            self.ui.edtTowerWeightConstru.setText(float_to_str(
                selected_wind_turbine["aero_massas"].values[0][1]))

            # Dados da nacele
            self.ui.edtNaceleWeight.setText(float_to_str(
                selected_wind_turbine["aero_massas"].values[0][2]))

            # Dados do hub
            self.ui.edtHubWeight.setText(float_to_str(
                selected_wind_turbine["aero_massas"].values[0][3]))

            # Dados das pás
            self.ui.edtBladeRadiusContru.setText(float_to_str(
                selected_wind_turbine["r_rotor"].values[0]))
            self.ui.edtBladeWeight.setText(float_to_str(
                selected_wind_turbine["aero_massas"].values[0][4]))

            self.set_costs(
                "wind_turbines", selected_wind_turbine["custo"].values[0]*selected_wind_turbine["n_aero"].values[0])

            self.set_commissioning_cost()

            self.clear_table_results()

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar dados do aerogerador para contrutibilidade.\n\n'
                                 f'Problema: {ex}')

    def set_data_electric(self, substations_position, _dim, cables, costs, export_cable):
        """Carrega aerogeradores do módulo de aerogeradores"""

        try:
            self.params_electric["dim"] = _dim
            self.params_electric["clusters"] = substations_position
            self.params_electric["cables"] = cables.copy()
            self.params_electric["export_cable"] = export_cable

            self.set_costs("cables_substations", costs)

            self.clear_table_results()
        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar dados de cabos e subestações para contrutibilidade.\n\n'
                                 f'Problema: {ex}')

    def set_data_constru_structures(self, calculate_forces):
        """Atribui para a contrutibilidade os dados calculados e definidos por estruturas"""

        try:
            self.params_electric["bathymetry_local"] = str_to_float(
                self.ui.edtBathymetry.text())
            # Sessões da torre
            self.ui.edtTowerDiameterTopoConstru.setText(
                float_to_str(calculate_forces['tower_diameter_top']))
            self.ui.edtTowerDiameterBaseConstru.setText(
                float_to_str(calculate_forces['tower_diameter_base']))

            # Dados da nacele
            self.ui.edtNaceleLength.setText(float_to_str(
                calculate_forces['tower_diameter_top']*3.5))
            self.ui.edtNaceleWidth.setText(float_to_str(
                calculate_forces['tower_diameter_top']*1.2))
            self.ui.edtNaceleHeight.setText(float_to_str(
                calculate_forces['tower_diameter_top']*1.2))

            # Dados do hub
            self.ui.edtHubDiameter.setText(float_to_str(
                calculate_forces['tower_diameter_top']*1.2))
            self.ui.edtHubHeight.setText(float_to_str(
                calculate_forces['tower_diameter_top']*1.2))

            # Dados das pás
            self.ui.edtBladeWidth.setText(float_to_str(
                calculate_forces['tower_diameter_top']*0.9))

            if (self.ui.rdbGravityResult.isChecked()):
                self.ui.constructability.set_data_constru_foundations(0)
            elif (self.ui.rdbMonopileResult.isChecked()):
                self.ui.constructability.set_data_constru_foundations(1)
            elif (self.ui.rdbJacketResult.isChecked()):
                self.ui.constructability.set_data_constru_foundations(2)

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar dados dos estruturas para contrutibilidade.\n\n'
                                 f'Problema: {ex}')

    def set_data_constru_foundations(self, idx):
        """Atribui para a contrutibilidade os dados calculados e definidos por estruturas"""
        if self.ui.edtFoundation.text().strip():
            self.ui.stackedVessels.setEnabled(True)
            if (idx == 0):
                self.ui.stackedVessels.setCurrentIndex(0)
                self.ui.stackedFoundations.setCurrentIndex(0)
            elif (idx == 1):
                self.ui.stackedVessels.setCurrentIndex(1)
                self.ui.stackedFoundations.setCurrentIndex(1)
                self.ui.lblFoundationSelected.setText(
                    '<html><head/><body><p><span style=" font-weight:600;">Lista de soluções de embarcação para fundação </span><span style=" font-weight:600; font-style:italic;">Monopile</span></p></body></html>')
            elif (idx == 2):
                self.ui.stackedVessels.setCurrentIndex(1)
                self.ui.stackedFoundations.setCurrentIndex(2)
                self.ui.lblFoundationSelected.setText(
                    '<html><head/><body><p><span style=" font-weight:600;">Lista de soluções de embarcação para fundação tipo jaqueta</span></p></body></html>')
            self.clear_table_results()

    def clear_results(self):
        """Limpa as variáveis com os resultados e a lista."""

        # Inicializa
        self.init_params()

        # Default
        self.ui.tabsAreas.setCurrentIndex(0)
        self.ui.tabsGeneral.setCurrentIndex(0)
        self.ui.tabsFoundation.setCurrentIndex(0)
        self.ui.tabsCablesSubstation.setCurrentIndex(0)
        self.ui.tabsWindTurbine.setCurrentIndex(0)

        # Default
        self.ui.tabFoundationParam.setEnabled(False)
        self.ui.tabFoundationResult.setEnabled(False)
        self.ui.tabCablesSubstationParam.setEnabled(False)
        self.ui.tabCablesSubstationResult.setEnabled(False)
        self.ui.tabWindTurbineParam.setEnabled(False)
        self.ui.tabWindTurbineType.setEnabled(False)
        self.ui.tabWindTurbineResult.setEnabled(False)
        self.ui.tabTimeline.setEnabled(False)
        self.ui.stackedVessels.setEnabled(False)

        self.default_params_general()
        self.default_params_foundations()
        self.default_params_electric()
        self.default_params_wind_turbine()

        self.ui.treeVesselsMonopileJacket.clear()
        self.ui.treeVesselsGravity.clear()

        # Campos
        line_edits = [
            self.ui.edtContruPort,
            self.ui.edtContruPortLatitude,
            self.ui.edtContruPortLongitude,
            self.ui.edtTowerDiameterTopoConstru,
            self.ui.edtTowerDiameterBaseConstru,
            self.ui.edtTowerHeightConstru,
            self.ui.edtTowerWeightConstru,
            self.ui.edtNaceleLength,
            self.ui.edtNaceleWidth,
            self.ui.edtNaceleHeight,
            self.ui.edtNaceleWeight,
            self.ui.edtHubDiameter,
            self.ui.edtHubHeight,
            self.ui.edtHubWeight,
            self.ui.edtBladeRadiusContru,
            self.ui.edtBladeWidth,
            self.ui.edtBladeWeight,
        ]
        list(map(clear_lineEdit, line_edits))

        self.clear_table_results()

    def clear_table_results(self):
        self.ui.tableConstru.setRowCount(0)
        self.webview_foundation.setHtml("")
        self.webview_electric.setHtml("")
        self.webview_windturbine.setHtml("")
        # Tabela
        for r in range(6):
            clear = QTableWidgetItem('')
            self.ui.tableImplantation.setItem(r, 0, clear)

        for r in range(5):
            clear = QTableWidgetItem('')
            self.ui.tableInstallation.setItem(r, 0, clear)

        for r in range(3):
            clear = QTableWidgetItem('')
            self.ui.tableOthers.setItem(r, 0, clear)

        # Campos
        line_edits = [
            self.ui.edtTimelineTotal,
            self.ui.edtContruTotal
        ]
        list(map(clear_lineEdit, line_edits))

    def init_results_layouts(self):
        """Generate charts layouts"""

        self.webview_foundation = QWebView(
            self.ui.widgetFoundationResult)
        layout = QtWidgets.QVBoxLayout(
            self.ui.widgetFoundationResult)
        layout.addWidget(self.webview_foundation)

        self.webview_electric = QWebView(
            self.ui.widgetElectricResult)
        layout = QtWidgets.QVBoxLayout(
            self.ui.widgetElectricResult)
        layout.addWidget(self.webview_electric)

        self.webview_windturbine = QWebView(
            self.ui.widgetWindTurbineResult)
        layout = QtWidgets.QVBoxLayout(
            self.ui.widgetWindTurbineResult)
        layout.addWidget(self.webview_windturbine)

    def default_params_general(self):
        """Parâmentros default para a aba Geral"""

        future_datetime = QDateTime.currentDateTime().addDays(30)
        future_datetime.setTime(QTime(7, 0))
        self.ui.spbStockPort.setValue(10)
        self.ui.spdCostPort.setValue(1000)
        self.ui.edtProjectName.setText('Projeto 1')
        self.ui.mStartDate.setDateTime(future_datetime)
        self.ui.mStartTime.setDateTime(future_datetime)
        self.ui.spdCostCommissioning.setValue(595)
        self.ui.spbDPG.setValue(3)
        self.ui.spbContingency.setValue(15)

        self.set_commissioning_cost()

    def set_commissioning_cost(self):
        try:
            capacity_mb = str_to_float(self.ui.edtCapacity.text()) * 1000
            if capacity_mb <= 80:
                self.ui.spdCostCommissioning.setValue(392)
            elif capacity_mb <= 200:
                self.ui.spdCostCommissioning.setValue(483)
            elif capacity_mb <= 300:
                self.ui.spdCostCommissioning.setValue(593)
            elif capacity_mb <= 400:
                self.ui.spdCostCommissioning.setValue(472)
            elif capacity_mb <= 200:
                self.ui.spdCostCommissioning.setValue(595)
            self.ui.spbDPG.setValue(3)
            self.ui.spbContingency.setValue(15)
        except:
            self.ui.spdCostCommissioning.setValue(595)

    def default_params_foundations(self):
        """Parâmentros default para a aba Fundação"""

        # Monopile
        self.ui.cbxMConnectionType.setCurrentIndex(1)
        self.ui.spbMComprimentoIncorporacao.setValue(20)
        self.ui.spbMTempoPesquisaComRov.setValue(1)
        self.ui.spbMTempoLiberar.setValue(3)
        self.ui.spbMTempoPrepararEquipamentoConducao.setValue(1)
        self.ui.spbMTaxaConducao.setValue(20)
        self.ui.spbMTempoParafusarConexao.setValue(4)
        self.ui.spbMAplicarArgamassaConexao.setValue(2)
        self.ui.spbMCuraArgamassa.setValue(24)
        # Jacket
        self.ui.cbxJConnectionType.setCurrentIndex(1)
        self.ui.spbJComprimentoIncorporacao.setValue(20)
        self.ui.spbJTempoPesquisaComRov.setValue(1)
        self.ui.spbJTempoLiberar.setValue(3)
        self.ui.spbJTempoPrepararEquipamentoConducao.setValue(1)
        self.ui.spbJTaxaConducao.setValue(20)
        self.ui.spbJTempoParafusarConexao.setValue(4)
        self.ui.spbJAplicarArgamassaConexao.setValue(2)
        self.ui.spbJCuraArgamassa.setValue(24)
        # Gravidade
        self.ui.spbGTempoPesquisaComRov.setValue(1)
        self.ui.spbGPosicionar.setValue(5)
        self.ui.spbGEnchimentoLastro.setValue(12)
        self.ui.spbGAplicarArgamassaConexao.setValue(6)

    def default_params_electric(self):
        """Parâmentros default para a aba Cabos e Subestações"""

        # Fundação da subestação
        self.ui.spbCJComprimentoIncorporacao.setValue(20)
        self.ui.spbCJTempoPesquisaComRov.setValue(1)
        self.ui.spbCJTempoLiberar.setValue(3)
        self.ui.spbCJTempoPrepararEquipamentoConducao.setValue(1)
        self.ui.spbCJTempoPrepararEquipamentoElevacao.setValue(1)
        self.ui.spbCJTaxaConducao.setValue(20)

        # Subestação
        self.ui.spbSubstationFixar.setValue(6)
        self.ui.spbSubstationLiberar.setValue(2)
        self.ui.spbSubstationAnexar.setValue(12)

    def default_params_wind_turbine(self):
        """Parâmentros default para a aba Aerogerador"""

        self.ui.spbStackability.setValue(0)
        self.ui.spbStackabilityNumber.setValue(3)
        self.ui.rdb1.setChecked(True)

    def next_general(self):
        self.ui.tabsGeneral.setCurrentIndex(1)

    def next_vessels(self):
        self.ui.tabsAreas.setCurrentIndex(1)
        self.ui.tabsFoundation.setCurrentIndex(0)

    def next_wind_turbine(self):
        self.ui.tabsWindTurbine.setCurrentIndex(1)

    def start_project(self):
        """Inicia um projeto único com os dados de parque e porto"""

        try:
            if not self.ui.edtElectricSystem.text().strip():
                QMessageBox.warning(None,
                                    'Erro',
                                    'Defina o sistema elétrico a ser utilizado para o projeto.')
                self.ui.tabsMain.setCurrentIndex(1)
                return False

            if (not self.ui.edtContruPort.text().strip() or
                not self.ui.edtContruPortLatitude.text().strip() or
                    not self.ui.edtContruPortLongitude.text().strip()):
                QMessageBox.warning(None,
                                    'Erro',
                                    'Defina um porto a ser utilizado para o projeto.')
                self.ui.tabsMain.setCurrentIndex(2)
                return False

                # Verifica se a fundação foi selecionada
            if not self.ui.edtFoundation.text().strip():
                QMessageBox.warning(None,
                                    'Erro',
                                    'Selecione uma fundação a ser utilizada para o projeto.')
                self.ui.tabsMain.setCurrentIndex(4)
                self.ui.tabsStructuresFundations.setCurrentIndex(2)
                return

            if not self.ui.edtProjectName.text().strip():
                QMessageBox.warning(None,
                                    'Erro',
                                    'Defina um nome para o projeto.')
                self.ui.tabsAreas.setCurrentIndex(0)
                self.ui.tabsGeneral.setCurrentIndex(0)
                self.ui.edtProjectName.setFocus()
                return False

            # Verifica a data do projeto
            start_date = QDateTime(self.ui.mStartDate.date(),
                                   self.ui.mStartTime.time())

            if start_date < QDateTime.currentDateTime():
                QMessageBox.warning(None,
                                    'Erro',
                                    'Data de início do projeto anterior a data atual.')
                self.ui.tabsAreas.setCurrentIndex(0)
                self.ui.tabsGeneral.setCurrentIndex(0)
                self.ui.mStartDate.setFocus()
                return False

            self.general.set_parque(self.site,
                                    self.ui.edtProjectName.text(),
                                    start_date.toPyDateTime())
            self.general.set_porto(self.ui.edtContruPort.text(),
                                   self.ui.edtContruPortLatitude.text(),
                                   self.ui.edtContruPortLongitude.text())

            if self.ui.chbFlagConstrain.isChecked():
                self.params_constrain["constrain"] = True
            else:
                self.params_constrain["constrain"] = False

            self.load_vessels()

            return True
        except:
            self.project = pd.DataFrame()
            return False

    def filtered_vessels(self, type):
        """ Filtra a embarcação para a metodologia
            type = 0 >> Fundação
            type = 1 >> Cabos e subestação
            type = 2 >> Aerogerador
            type = 3 >> Proteção contra erosão - Enrocamento
            type = 4 >> Todas as etapas de contrução """

        filter = {}

        if self.ui.rdbMonopileResult.isChecked() or self.ui.rdbJacketResult.isChecked():
            selected_vessels = tree_with_child_to_dataframe(
                self.ui.treeVesselsMonopileJacket)
        else:
            selected_vessels = tree_with_child_to_dataframe(
                self.ui.treeVesselsGravity)

        # Função para converter os dados do formato "390.000,00" para float

        def format_to_float(value):
            try:
                if isinstance(value, str):
                    value = value.replace('.', '').replace(',', '.')
                return float(value)
            except:
                return 0

        # Aplica a função de conversão nas colunas 2, 3, 4 e 5
        selected_vessels.iloc[:, [2, 3, 4, 5]] = selected_vessels.iloc[:, [
            2, 3, 4, 5]].map(format_to_float)

        # Filtrando por uma coluna específica

        filter["wtiv"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'WTIV'")
        filter["heavy_lift"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Heavy Lift/Jack Up'")
        filter["cable_vessel"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Cable Vessel'")
        filter["fallpipe_vessel"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Fallpipe Vessel'")
        filter["barcaca"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Barcaça'")
        filter["rebocador"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Rebocador'")

        if type == 0 or type == 4:
            if self.ui.rdbMonopileResult.isChecked() or self.ui.rdbJacketResult.isChecked():
                if filter["wtiv"].empty:
                    if (self.ui.rdbMonopileResult.isChecked()):
                        vessel = "Monopile"
                    else:
                        vessel = "tipo Jaqueta"

                    QMessageBox.warning(None,
                                        'Erro',
                                        f'Defina ao menos uma solução de embaracação com uma embarcação WTIV para a instalação de fundação {vessel}.')
                    self.ui.tabsAreas.setCurrentIndex(0)
                    self.ui.tabsGeneral.setCurrentIndex(1)
                    return {}

            else:
                if filter["heavy_lift"].empty:
                    QMessageBox.warning(None,
                                        'Erro',
                                        'Defina ao menos uma solução de embaracação com uma embarcação Heavy Lift/Jack Up para a instalação de fundação tipo base de gravidade.')
                    self.ui.tabsAreas.setCurrentIndex(0)
                    self.ui.tabsGeneral.setCurrentIndex(1)
                    return {}

        if type == 1 or type == 4:
            if filter["cable_vessel"].empty or filter["heavy_lift"].empty:
                QMessageBox.warning(None,
                                    'Erro',
                                    f'Defina ao menos uma solução de embaracação com uma embarcação Cable Vessel e Heavy Lift/Jack Up para a instalação de cabos e subestações.')
                self.ui.tabsAreas.setCurrentIndex(0)
                self.ui.tabsGeneral.setCurrentIndex(1)
                return {}

        if type == 2 or type == 4:
            if filter["wtiv"].empty:
                QMessageBox.warning(None,
                                    'Erro',
                                    'Defina ao menos uma solução de embaracação com uma embarcação WTIV para a instalação dos aerogeradores.')
                self.ui.tabsAreas.setCurrentIndex(0)
                self.ui.tabsGeneral.setCurrentIndex(1)
                return {}

        if type == 3 or type == 4:
            if filter["fallpipe_vessel"].empty:
                QMessageBox.warning(None,
                                    'Erro',
                                    'Defina ao menos uma solução de embaracação com uma embarcação Fallpipe Vessel para a instalação da proteção contra erosão.')
                self.ui.tabsAreas.setCurrentIndex(0)
                self.ui.tabsGeneral.setCurrentIndex(1)
                return {}

        return filter

    def run_foundations(self):
        """Executar construtibilidade fundação"""

        try:

            if self.start_project():
                filtered_vessels = self.filtered_vessels(0)

                if filtered_vessels:
                    QGuiApplication.setOverrideCursor(Qt.WaitCursor)

                    if self.ui.rdbMonopileResult.isChecked() or self.ui.rdbJacketResult.isChecked():
                        if self.ui.rdbMonopileResult.isChecked():
                            FoundationMonopile(self.ui,
                                               self.webview_foundation,
                                               self.params_constrain,
                                               filtered_vessels,
                                               self.table_vessels,
                                               self.general)

                        else:
                            FoundationJacket(self.ui,
                                             self.webview_foundation,
                                             self.params_constrain,
                                             filtered_vessels,
                                             self.table_vessels,
                                             self.general)
                    else:
                        FoundationGravity(self.ui,
                                          self.webview_foundation,
                                          self.params_constrain,
                                          filtered_vessels,
                                          self.table_vessels,
                                          self.general)

                    self.ui.tabsFoundation.setCurrentIndex(1)
                    QGuiApplication.restoreOverrideCursor()

        except Exception as ex:
            QGuiApplication.restoreOverrideCursor()
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível fazer a simulação para fundações.\n'
                                 'Verifique os dados e tente novamente.\n\n'
                                 f'Problema: {ex}')

    def run_electric(self):
        """Executar simulação de instalação de Cabos e subestações"""

        try:
            if self.start_project():
                filtered_vessels = self.filtered_vessels(1)

                if filtered_vessels:
                    QGuiApplication.setOverrideCursor(Qt.WaitCursor)
                    Electric(self.ui,
                             self.webview_electric,
                             self.params_constrain,
                             self.project,
                             self.params_electric,
                             filtered_vessels,
                             self.table_vessels,
                             self.general)

                    self.ui.tabsCablesSubstation.setCurrentIndex(1)
                    QGuiApplication.restoreOverrideCursor()

        except Exception as ex:
            QGuiApplication.restoreOverrideCursor()
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível fazer a simulação para cabos e subestações.\n'
                                 'Verifique os dados e tente novamente.\n\n'
                                 f'Problema: {ex}')

    def run_wind_turbine(self):
        """Executar construtibilidade aerogerador"""

        try:
            if self.start_project():
                filtered_vessels = self.filtered_vessels(2)

                if filtered_vessels:
                    QGuiApplication.setOverrideCursor(Qt.WaitCursor)
                    WindTurbine(self.ui,
                                self.webview_windturbine,
                                self.params_constrain,
                                filtered_vessels,
                                self.table_vessels,
                                self.general)

                    self.ui.tabsWindTurbine.setCurrentIndex(2)
                    QGuiApplication.restoreOverrideCursor()

        except Exception as ex:
            QGuiApplication.restoreOverrideCursor()
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível fazer a simulação para os aerogeradores.\n'
                                 'Verifique os dados e tente novamente.\n\n'
                                 f'Problema: {ex}')

    def dataframe_to_tree(self, df, tree):
        """Adiciona embarcações na janela"""
        parent = QTreeWidgetItem(tree, ["Solução"])
        for index, row in df.iterrows():
            child_item = QTreeWidgetItem(
                parent, [row["Tipo"],
                         row["Embarcação"],
                         row["Taxa diária (US$)"],
                         row["Taxa de mobilização (US$)"],
                         row["Velocidade vazio (kt)"],
                         row["Velocidade carregado (kt)"],
                         row["Velocidade máxima do vento (m/s)"],
                         row["Altura máxima da onda (m)"]])
            set_bold_font(child_item, 0)

            # Alinhar alguns itens à direita
            child_item.setTextAlignment(2, Qt.AlignRight | Qt.AlignVCenter)
            child_item.setTextAlignment(3, Qt.AlignRight | Qt.AlignVCenter)
            child_item.setTextAlignment(4, Qt.AlignRight | Qt.AlignVCenter)
            child_item.setTextAlignment(5, Qt.AlignRight | Qt.AlignVCenter)
            child_item.setTextAlignment(6, Qt.AlignRight | Qt.AlignVCenter)
            child_item.setTextAlignment(7, Qt.AlignRight | Qt.AlignVCenter)

    def load_vessels(self):
        """Carrega arquivo de embarcações"""
        try:
            if not self.table_vessels:
                self.table_vessels["wtiv"] = load_data(
                    "vessel_wtiv.xlsx", "wtiv")
                self.table_vessels["heavy_lift"] = load_data(
                    "vessel_heavy_lift.xlsx", "heavy lift")
                self.table_vessels["cable_vessel"] = load_data(
                    "vessel_cable.xlsx", "cable vessel")
                self.table_vessels["fallpipe_vessel"] = load_data(
                    "vessel_fallpipe.xlsx", "fallpipe vessel")
                self.table_vessels["barcaca"] = load_data(
                    "vessel_barcaca.xlsx", "barcaça")
                self.table_vessels["rebocador"] = load_data(
                    "vessel_rebocador.xlsx", "rebocador")
        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar os arquivos de embarcações.\n\n'
                                 f'Problema: {ex}')

    def add_vessels_monopile_jacket(self):
        """
        Adiciona embarcações para fundações monopile e jaqueta
        """
        try:
            self.load_vessels()

            # Define a classe responsável pelas embarcações
            vessel_monopile_jacket = VesselMonopileJacket(ui=self.ui)
            vessel_monopile_jacket.define_vessels(self.table_vessels)

            if self.ui.vesselSelectionDialog.exec_() == QDialog.Accepted:
                self.ui.treeVesselsMonopileJacket.clear()
                df = vessel_monopile_jacket.get_vessels_df()
                self.dataframe_to_tree(df, self.ui.treeVesselsMonopileJacket)
                self.ui.treeVesselsMonopileJacket.expandAll()

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível definir as embarcações.\n\n'
                                 f'Problema: {ex}')

    def add_vessels_gravity(self):
        """Adiciona embarcações para fundação base de gravidade"""
        try:
            self.load_vessels()

            # Define a classe responsável pelas embarcações
            vessel_gravity = VesselGravity(ui=self.ui)
            vessel_gravity.define_vessels(self.table_vessels)

            if self.ui.vesselSelectionDialog.exec_() == QDialog.Accepted:
                self.ui.treeVesselsGravity.clear()
                df = vessel_gravity.get_vessels_df()
                self.dataframe_to_tree(df, self.ui.treeVesselsGravity)
                self.ui.treeVesselsGravity.expandAll()

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível definir as embarcações.\n\n'
                                 f'Problema: {ex}')

    def del_selected_monopile_jacket(self):
        """Exclui embarcações para Fundação Monopile e Jaqueta"""
        selected_item = self.ui.treeVesselsMonopileJacket.currentItem()
        if selected_item is not None:
            index = self.ui.treeVesselsMonopileJacket.indexOfTopLevelItem(
                selected_item)
            self.ui.treeVesselsMonopileJacket.takeTopLevelItem(index)

    def del_selected_gravity(self):
        """Exclui embarcações para Fundação Base de Gravidade"""
        selected_item = self.ui.treeVesselsGravity.currentItem()
        if selected_item is not None:
            index = self.ui.treeVesselsGravity.indexOfTopLevelItem(
                selected_item)
            self.ui.treeVesselsGravity.takeTopLevelItem(index)

    def select_connection_type(self):
        """Habilita opções dependendo do tipo de conexão entre a peça de transição e a fundação"""

        parafuso = (self.ui.cbxMConnectionType.currentIndex()
                    == 0)  # Parafuso para Monopile

        self.ui.lblMTempoParafusarConexao.setVisible(parafuso)
        self.ui.spbMTempoParafusarConexao.setVisible(parafuso)
        self.ui.lblMAplicarArgamassaConexao.setVisible(not parafuso)
        self.ui.spbMAplicarArgamassaConexao.setVisible(not parafuso)
        self.ui.lblMCuraArgamassa.setVisible(not parafuso)
        self.ui.spbMCuraArgamassa.setVisible(not parafuso)

        parafuso = (self.ui.cbxJConnectionType.currentIndex()
                    == 0)  # Parafuso para tipo Jaqueta

        self.ui.lblJTempoParafusarConexao.setVisible(parafuso)
        self.ui.spbJTempoParafusarConexao.setVisible(parafuso)
        self.ui.lblJAplicarArgamassaConexao.setVisible(not parafuso)
        self.ui.spbJAplicarArgamassaConexao.setVisible(not parafuso)
        self.ui.lblJCuraArgamassa.setVisible(not parafuso)
        self.ui.spbJCuraArgamassa.setVisible(not parafuso)

    def run_timeline(self):
        """Executa todos os módulos para a simulação da construtibilidade"""

        try:

            if self.start_project():

                # Totalização dos Custos
                foundation_wind_turbine = 0
                filtered_vessels = self.filtered_vessels(4)
                if filtered_vessels:
                    QGuiApplication.setOverrideCursor(Qt.WaitCursor)

                    if self.ui.rdbMonopileResult.isChecked() or self.ui.rdbJacketResult.isChecked():
                        if self.ui.rdbMonopileResult.isChecked():
                            foundation = FoundationMonopile(self.ui,
                                                            self.webview_foundation,
                                                            self.params_constrain,
                                                            filtered_vessels,
                                                            self.table_vessels,
                                                            self.general)
                            self.set_costs("scour", str_to_float(
                                self.ui.edtCostScourMonopile.text()))
                            foundation_wind_turbine = str_to_float(
                                self.ui.edtCostSteelMonopile.text())
                        else:
                            foundation = FoundationJacket(self.ui,
                                                          self.webview_foundation,
                                                          self.params_constrain,
                                                          filtered_vessels,
                                                          self.table_vessels,
                                                          self.general)
                            self.set_costs("scour", str_to_float(
                                self.ui.edtCostScourJacket.text()))
                            foundation_wind_turbine = str_to_float(
                                self.ui.edtCostSteelJacket.text())
                    else:
                        foundation = FoundationGravity(self.ui,
                                                       self.webview_foundation,
                                                       self.params_constrain,
                                                       filtered_vessels,
                                                       self.table_vessels,
                                                       self.general)
                        self.set_costs("scour", str_to_float(
                            self.ui.edtCostScourGravity.text()))
                        foundation_wind_turbine = (str_to_float(self.ui.edtCostConcreteGravity.text(
                        )) + str_to_float(self.ui.edtCostGravelGravity.text()))

                    foundation_substation = (str_to_float(self.ui.edtCostSteelSubstation.text(
                    )) + str_to_float(self.ui.edtCostScourJacketSubstation.text()))/1000000

                    self.set_costs("foundation_wind_turbine",
                                   foundation_wind_turbine)
                    self.set_costs("foundation_substation",
                                   foundation_substation)

                    electric = Electric(self.ui,
                                        self.webview_electric,
                                        self.params_constrain,
                                        self.project,
                                        self.params_electric,
                                        filtered_vessels,
                                        self.table_vessels,
                                        self.general, foundation.data_fim)

                    wind_turbine = WindTurbine(self.ui,
                                               self.webview_windturbine,

                                               self.params_constrain,
                                               filtered_vessels,
                                               self.table_vessels,
                                               self.general, electric.data_fim)

                    self.custo_embarcacao = {}
                    self.custo_embarcacao["Fundação"] = foundation.results
                    self.custo_embarcacao["Enrocamento da fundação"] = foundation.enrocamento
                    self.custo_embarcacao.update(electric.results)
                    self.custo_embarcacao["Enrocamento da fundação da subestação"] = electric.enrocamento
                    self.custo_embarcacao["Aerogerador"] = wind_turbine.results

                    self.fill_data()

                    rt_ac = sum(value['total_dias'] for value in self.custo_embarcacao["Sistema array"].values(
                    ) if 'total_dias' in value)
                    cost_vessel_ac = sum(value['custo'] for value in self.custo_embarcacao["Sistema array"].values(
                    ) if 'custo' in value)

                    rt_ec = sum(
                        value['total_dias']
                        for key in ["Cabo exportação offshore"]
                        for value in self.custo_embarcacao[key].values()
                        if 'total_dias' in value
                    )

                    cost_vessel_ec = sum(
                        value['custo']
                        for key in ["Cabo exportação offshore"]
                        for value in self.custo_embarcacao[key].values()
                        if 'custo' in value
                    )

                    # Habilita O&M somente depois de executar a contrutibilidade
                    # Parâmetro para o O&M
                    self.ui.oem.set_data_constructability(rt_ac,
                                                          cost_vessel_ac/1000000,
                                                          rt_ec,
                                                          cost_vessel_ec/1000000)
                    self.ui.tabsOper.setEnabled(True)
                    self.ui.tabsMaint.setEnabled(True)
                    self.ui.tabsResults.setEnabled(True)

                    QGuiApplication.restoreOverrideCursor()

                    # Registra ação
                    cfg.cfg_run_constru = True

        except Exception as ex:
            cfg.cfg_run_constru = False
            QGuiApplication.restoreOverrideCursor()
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível fazer a simulação completa.\n'
                                 'Verifique os dados e tente novamente.\n\n'
                                 f'Problema: {ex}')

    def fill_data(self):
        """
        Mostrar os dados do resultado da simulação na tabela
        :param dados: dicionário contento os resultados da simulação
        """

        total = 0
        for sub_data in self.custo_embarcacao.values():
            total += len(sub_data)

        self.ui.tableConstru.setRowCount(0)
        self.ui.tableConstru.setRowCount(total)

        id = 0
        total = 0
        total_mobilizacao = 0
        embarcacoes = []
        area_total_transportada = 0
        for task, process in self.custo_embarcacao.items():
            for row in process:
                self.ui.tableConstru.setItem(id, 0, QTableWidgetItem(task))
                self.ui.tableConstru.setItem(
                    id, 1, QTableWidgetItem(process[row]["embarcacao"]))

                viagens = QTableWidgetItem(
                    float_to_str(process[row]["viagens"], 1))
                viagens.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                self.ui.tableConstru.setItem(id, 2, viagens)

                data_inicio = QTableWidgetItem(
                    process[row]["data_inicio"].strftime("%d/%m/%Y - %H:%M"))
                data_inicio.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
                self.ui.tableConstru.setItem(id, 3, data_inicio)

                data_fim = QTableWidgetItem(
                    process[row]["data_fim"].strftime("%d/%m/%Y - %H:%M"))
                data_fim.setTextAlignment(Qt.AlignCenter | Qt.AlignCenter)
                self.ui.tableConstru.setItem(id, 4, data_fim)

                total_dias = QTableWidgetItem(
                    float_to_str(process[row]["total_dias"], 1))
                total_dias.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                self.ui.tableConstru.setItem(id, 5, total_dias)

                taxa = QTableWidgetItem(
                    float_to_str(process[row]["taxa"]))
                taxa.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                self.ui.tableConstru.setItem(id, 6, taxa)

                custo = QTableWidgetItem(
                    float_to_str(process[row]["custo"]/1000000))
                custo.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                self.ui.tableConstru.setItem(id, 7, custo)

                self.ui.tableConstru.resizeColumnsToContents()

                total += process[row]["custo"]/1000000
                area_total_transportada += process[row]["area_total_transportada"]/1000000

                if process[row]["embarcacao"] not in embarcacoes:
                    embarcacoes.append(process[row]["embarcacao"])
                    total_mobilizacao += process[row]["taxa_mobilizacao"]

                id += 1

        self.ui.edtTimelineTotal.setText(float_to_str(total))
        self.set_costs("vessels_daily", total)
        self.set_costs("vessels_mobilization", total_mobilizacao/1000000)
        custo_armazenamento_porto = (((process[row]["area_total_transportada"] *
                                       self.ui.spbStockPort.value()) / 100) * self.ui.spdCostPort.value())/1000000
        self.set_costs("port_storage_cost",
                       custo_armazenamento_porto)
        self.set_costs("commissioning", (str_to_float(
            self.ui.edtCapacity.text()) * 1000 * self.ui.spdCostCommissioning.value())/1000000)
        self.fill_data_total()

    def fill_data_total(self):
        """
        Mostrar os dados de custos
        """
        # Aerogeradores
        data = QTableWidgetItem(float_to_str(
            self.total_costs["wind_turbines"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableImplantation.setItem(0, 0, data)
        total_1 = self.total_costs["wind_turbines"]

        # Fundações aerogeradores
        data = QTableWidgetItem(float_to_str(
            self.total_costs["foundation_wind_turbine"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableImplantation.setItem(1, 0, data)
        total_1 += self.total_costs["foundation_wind_turbine"]

        # Fundações subestação
        data = QTableWidgetItem(float_to_str(
            self.total_costs["foundation_substation"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableImplantation.setItem(2, 0, data)
        total_1 += self.total_costs["foundation_substation"]

        # Cabos e subestações (CA ou CC)
        data = QTableWidgetItem(float_to_str(
            self.total_costs["cables_substations"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableImplantation.setItem(3, 0, data)
        total_1 += self.total_costs["cables_substations"]

        # Proteção de erosão
        data = QTableWidgetItem(float_to_str(
            self.total_costs["scour"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableImplantation.setItem(4, 0, data)
        total_1 += self.total_costs["scour"]

        # TOTAL
        data = QTableWidgetItem(float_to_str(total_1))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        set_bold_font_data(data)
        self.ui.tableImplantation.setItem(5, 0, data)

        # Embarcações - diárias
        data = QTableWidgetItem(float_to_str(
            self.total_costs["vessels_daily"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableInstallation.setItem(0, 0, data)
        total_2 = self.total_costs["vessels_daily"]

        # Embarcações - mobilização
        data = QTableWidgetItem(float_to_str(
            self.total_costs["vessels_mobilization"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableInstallation.setItem(1, 0, data)
        total_2 += self.total_costs["vessels_mobilization"]

        # Custo de armazenamento no porto
        data = QTableWidgetItem(float_to_str(
            self.total_costs["port_storage_cost"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableInstallation.setItem(2, 0, data)
        total_2 += self.total_costs["port_storage_cost"]

        # Comissionamento
        data = QTableWidgetItem(float_to_str(
            self.total_costs["commissioning"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableInstallation.setItem(3, 0, data)
        total_2 += self.total_costs["commissioning"]

        # TOTAL
        data = QTableWidgetItem(float_to_str(total_2))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        set_bold_font_data(data)
        self.ui.tableInstallation.setItem(4, 0, data)

        pDPG = self.ui.spbDPG.value()/100
        pC = self.ui.spbContingency.value()/100

        valor_total = (total_1 + total_2) / (1 - pDPG - pC)

        self.set_costs("dpg", valor_total * pDPG)
        self.set_costs("contingencia", valor_total * pC)

        # Desenvolvimento, planejamento e gerenciamento
        data = QTableWidgetItem(float_to_str(self.total_costs["dpg"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableOthers.setItem(0, 0, data)

        # Contingência
        data = QTableWidgetItem(float_to_str(
            self.total_costs["contingencia"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableOthers.setItem(1, 0, data)

        total_3 = self.total_costs["dpg"] + self.total_costs["contingencia"]

        # TOTAL
        data = QTableWidgetItem(float_to_str(total_3))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        set_bold_font_data(data)
        self.ui.tableOthers.setItem(2, 0, data)

        self.ui.edtContruTotal.setText(
            float_to_str(total_1 + total_2 + total_3))

    def export_timeline(self):
        """
        Salvar simulação dos dados EL    
        """

        try:
            if self.custo_embarcacao is None or self.total_costs is None:
                QMessageBox.warning(None,
                                    'Erro',
                                    'Não há dados para serem salvos.\n'
                                    'Faça a simulação e tente novamente.')
                return

            filename, _filter = QFileDialog.getSaveFileName(
                directory=cfg.dir_results,
                caption='Exportar cronograma de instalação',
                filter='XLS (*.xlsx)')

            if filename is not None and filename != '':
                # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')

                # Armazena cada df em uma planilha diferente do mesmo arquivo
                # Flatten the dictionary
                flattened_data = []
                for key1, subdict in self.custo_embarcacao.items():
                    for key2, details in subdict.items():
                        flat_row = {'Category': key1, 'Subcategory': key2}
                        flat_row.update(details)
                        flattened_data.append(flat_row)

                df = pd.DataFrame(flattened_data)
                df.to_excel(writer, sheet_name='Cronograma de instalação')
                df = pd.DataFrame(self.total_costs, index=[0])
                df.to_excel(writer, sheet_name='Custos totais')

                # Fecha o ExcelWriter e gera o arquivo .xlsx
                writer.close()

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível gerar o arquivo de resultados.\n'
                                 'Execute novamente a simulação e tente novamente.\n\n'
                                 f'Problema: {ex}')

    def check_html_content(self, obj):
        # Usando o toHtml para pegar o conteúdo HTML e passar para o callback
        return obj.page().mainFrame().toHtml()

    def export_html(self, type):
        # Salva em arquivo o cronograma
        try:
            if type == 0:
                html = self.check_html_content(
                    self.webview_foundation)
            elif type == 1:
                html = self.check_html_content(
                    self.webview_electric)
            else:
                html = self.check_html_content(
                    self.webview_windturbine)

            if not html.strip():
                QMessageBox.warning(
                    None, 'Erro', 'Execute a simulação para gerar o cronograma.')
                return

            filename, _filter = QFileDialog.getSaveFileName(
                directory=cfg.dir_results,
                caption='Exportar cronograma',
                filter='HTML (*.html)')

            if filename is not None and filename != '':
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(html)

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível gerar o arquivo de resultados.\n'
                                 'Execute novamente a simulação e tente novamente.\n\n'
                                 f'Problema: {ex}')
