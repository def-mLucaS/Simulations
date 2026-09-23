"""
Configurações de Descomissionamento
"""
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QScrollArea, QWidget, QVBoxLayout
from PyQt5.QtGui import QGuiApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ...utils.utils import *
from .vessel_deco_partial import VesselDecoPartial
from .vessel_deco_complete import VesselDecoComplete
from .simulation import run_simulation, plot_graphics

cfg = __import__(str(__name__).split('.')[0] + '.utils.config', fromlist=[''])


class Decommissioning(QtWidgets.QMainWindow):

    def __init__(self, ui):
        super(Decommissioning, self).__init__()

        self.ui = ui

        self.format_tables()
        self.init_chart_layouts()
        self.clear_results()

        # Default: Tipo de Cenário default - Descomissionamento parcial
        self.ui.rdbDecoPartial.setChecked(True)
        self.select_scenarios()

        # Embarcações
        self.table_vessels = {}

        # Eventos Aba - Soluções de Embarcações
        self.ui.btnVesselsDecoPartialAdd.clicked.connect(
            self.add_vessels_partial)
        self.ui.btnVesselsDecoPartialDelete.clicked.connect(
            self.del_vessels_partial)
        self.ui.btnVesselsDecoCompleteAdd.clicked.connect(
            self.add_vessels_complete)
        self.ui.btnVesselsDecoCompleteDelete.clicked.connect(
            self.del_vessels_complete)
        self.ui.rdbDecoPartial.clicked.connect(self.select_scenarios)
        self.ui.rdbDecoComplete.clicked.connect(self.select_scenarios)
        self.ui.btnDecoVesselsNext.clicked.connect(self.next_visible_tab)

        # Eventos Aba - Parâmentros - Descomissionamento parcial
        self.ui.btnDecoParamDefaultPartial.clicked.connect(
            self.default_params_partial)
        self.ui.btnDecoPartialRun.clicked.connect(self.run_partial)
        self.ui.btnDecoExportPartial.clicked.connect(lambda: self.export(0))

        # Eventos Aba - Parâmentros - Descomissionamento complete
        self.ui.btnDecoParamDefaultComplete1.clicked.connect(
            self.default_params_complete1)
        self.ui.btnDecoParamDefaultComplete2.clicked.connect(
            self.default_params_complete2)
        self.ui.btnDecoParamsNext.clicked.connect(self.next_visible_tab)
        self.ui.btnDecoCompleteRun.clicked.connect(self.run_complete)
        self.ui.btnDecoExportComplete.clicked.connect(lambda: self.export(1))

    def next_visible_tab(self):
        current_index = self.ui.tabsDeco.currentIndex()
        total_tabs = self.ui.tabsDeco.count()

        # Loop através das abas
        for i in range(1, total_tabs):
            next_index = (current_index + i) % total_tabs
            if self.ui.tabsDeco.isTabVisible(next_index):
                self.ui.tabsDeco.setCurrentIndex(next_index)
                break

    def clear_results(self):
        """Limpa as variáveis com os resultados e a lista."""

        # Inicializa
        self.init_params()

        # Default
        self.ui.tabsDeco.setCurrentIndex(0)

        # Desabilita se não é possível usar a metodologia
        self.ui.tabDecoParamC1.setEnabled(False)
        self.ui.tabDecoParamC2.setEnabled(False)
        self.ui.tabDecoParamP.setEnabled(False)
        self.ui.tabDecoResultsC.setEnabled(False)
        self.ui.tabDecoResultsP.setEnabled(False)

        self.default_params_partial()
        self.default_params_complete1()
        self.default_params_complete2()

        self.ui.treeVesselsDecoPartial.clear()
        self.ui.treeVesselsDecoComplete.clear()

        self.clear_table_results()
        self.clear_graphics()

    def init_params(self):
        """Inicializa os parâmetros de resultados."""
        # Geral
        self.scour_volume_wt = 0
        self.scour_volume_os = 0
        self.simulation_result = {}
        self.params_electric = {}
        self.dict_format_partial = {}
        self.dict_format_complete = {}

    def clear_table_results(self):
        for r in range(4):
            clear = QTableWidgetItem('')
            self.ui.tableDecoPartialResults.setItem(r, 0, clear)
            self.ui.tableDecoPartialResults.setItem(r, 1, clear)

        for r in range(6):
            clear = QTableWidgetItem('')
            self.ui.tableDecoCompleteResults.setItem(r, 0, clear)
            self.ui.tableDecoCompleteResults.setItem(r, 1, clear)

    def format_tables(self):
        """Formata as tabelas."""

        # Tabelas solução de embarcação - simulação completa
        self.ui.treeVesselsDecoComplete.header().setFixedHeight(50)
        self.ui.treeVesselsDecoComplete.header().setDefaultAlignment(
            Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))

        # Tabelas solução de embarcação - simulação parcial
        self.ui.treeVesselsDecoPartial.header().setFixedHeight(50)
        self.ui.treeVesselsDecoPartial.header().setDefaultAlignment(
            Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))

        # Tables Results - simulação completa
        self.ui.tableDecoCompleteResults.verticalHeader().setFixedWidth(200)
        self.ui.tableDecoCompleteResults.verticalHeader().setDefaultSectionSize(35)
        self.ui.tableDecoCompleteResults.verticalHeader().setDefaultAlignment(
            Qt.AlignVCenter | Qt.Alignment(Qt.TextWordWrap))

        # Tables Results - simulação parcial
        self.ui.tableDecoPartialResults.verticalHeader().setFixedWidth(200)
        self.ui.tableDecoPartialResults.verticalHeader().setDefaultSectionSize(35)
        self.ui.tableDecoPartialResults.verticalHeader().setDefaultAlignment(
            Qt.AlignVCenter | Qt.Alignment(Qt.TextWordWrap))

    def init_chart_layouts(self):
        """Generate charts layouts Partial"""
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setMinimumSize(400, 380)

        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setMinimumSize(400, 380)

        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)
        self.canvas3.setMinimumSize(400, 380)

        canvas_scrollarea = QScrollArea(widgetResizable=True)
        canvas_container = QWidget()
        canvas_scrollarea.setWidget(canvas_container)
        canvas_layout = QVBoxLayout(canvas_container)

        canvas_layout.addWidget(self.canvas1)
        self.view_chart1 = QtWidgets.QPushButton("Visualizar gráfico")
        self.view_chart1.setEnabled(False)
        self.view_chart1.clicked.connect(
            lambda: self.build_charts_partial(plot_window=True, chart_number=1)
        )
        canvas_layout.addWidget(self.view_chart1)

        canvas_layout.addWidget(self.canvas2)
        self.view_chart2 = QtWidgets.QPushButton("Visualizar gráfico")
        self.view_chart2.setEnabled(False)
        self.view_chart2.clicked.connect(
            lambda: self.build_charts_partial(plot_window=True, chart_number=2)
        )
        canvas_layout.addWidget(self.view_chart2)

        canvas_layout.addWidget(self.canvas3)
        self.view_chart3 = QtWidgets.QPushButton("Visualizar gráfico")
        self.view_chart3.setEnabled(False)
        self.view_chart3.clicked.connect(
            lambda: self.build_charts_partial(plot_window=True, chart_number=3)
        )
        canvas_layout.addWidget(self.view_chart3)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(canvas_scrollarea)
        self.ui.widgetDecoPartialResults.setLayout(layout)

        """Generate charts layouts Complete"""
        self.figure4 = Figure()
        self.canvas4 = FigureCanvas(self.figure4)
        self.canvas4.setMinimumSize(400, 380)

        self.figure5 = Figure()
        self.canvas5 = FigureCanvas(self.figure5)
        self.canvas5.setMinimumSize(400, 380)

        self.figure6 = Figure()
        self.canvas6 = FigureCanvas(self.figure6)
        self.canvas6.setMinimumSize(400, 380)

        canvas_scrollarea = QScrollArea(widgetResizable=True)
        canvas_container = QWidget()
        canvas_scrollarea.setWidget(canvas_container)
        canvas_layout = QVBoxLayout(canvas_container)

        canvas_layout.addWidget(self.canvas4)
        self.view_chart4 = QtWidgets.QPushButton("Visualizar gráfico")
        self.view_chart4.setEnabled(False)
        self.view_chart4.clicked.connect(
            lambda: self.build_charts_complete(
                plot_window=True, chart_number=1)
        )
        canvas_layout.addWidget(self.view_chart4)

        canvas_layout.addWidget(self.canvas5)
        self.view_chart5 = QtWidgets.QPushButton("Visualizar gráfico")
        self.view_chart5.setEnabled(False)
        self.view_chart5.clicked.connect(
            lambda: self.build_charts_complete(
                plot_window=True, chart_number=2)
        )
        canvas_layout.addWidget(self.view_chart5)

        canvas_layout.addWidget(self.canvas6)
        self.view_chart6 = QtWidgets.QPushButton("Visualizar gráfico")
        self.view_chart6.setEnabled(False)
        self.view_chart6.clicked.connect(
            lambda: self.build_charts_complete(
                plot_window=True, chart_number=3)
        )
        canvas_layout.addWidget(self.view_chart6)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(canvas_scrollarea)
        self.ui.widgetDecoCompleteResults.setLayout(layout)

    def clear_graphics(self):
        """Limpa os dados de gráficos."""
        self.canvas1.figure.clear()
        self.canvas2.figure.clear()
        self.canvas3.figure.clear()
        self.canvas4.figure.clear()
        self.canvas5.figure.clear()
        self.canvas6.figure.clear()
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
        self.canvas4.draw()
        self.canvas5.draw()
        self.canvas6.draw()
        self.view_chart1.setEnabled(False)
        self.view_chart2.setEnabled(False)
        self.view_chart3.setEnabled(False)
        self.view_chart4.setEnabled(False)
        self.view_chart5.setEnabled(False)
        self.view_chart6.setEnabled(False)

    def select_scenarios(self):
        """Habilita opções dependendo do tipo de cenário de simulação selecionado"""

        # Exibir abas 1, 2, 3 e ocultar 4, 5 ou Exibir abas 4, 5 e ocultar 1, 2, 3
        self.ui.tabsDeco.tabBar().setTabVisible(1, self.ui.rdbDecoComplete.isChecked())
        self.ui.tabsDeco.tabBar().setTabVisible(2, self.ui.rdbDecoComplete.isChecked())
        self.ui.tabsDeco.tabBar().setTabVisible(3, self.ui.rdbDecoComplete.isChecked())
        self.ui.tabsDeco.tabBar().setTabVisible(4, self.ui.rdbDecoPartial.isChecked())
        self.ui.tabsDeco.tabBar().setTabVisible(5, self.ui.rdbDecoPartial.isChecked())

        # Forçar ajuste de tamanho
        self.ui.tabsDeco.adjustSize()

        if self.ui.rdbDecoPartial.isChecked():
            self.ui.stackedVesselsDeco.setCurrentIndex(0)
        else:
            self.ui.stackedVesselsDeco.setCurrentIndex(1)

    def default_params_partial(self):
        """Parâmetros default para a simulação parcial"""

        self.ui.spbT_Blades.setValue(10)
        self.ui.spbT_Nacele.setValue(6)
        self.ui.spbT_UT.setValue(6)
        self.ui.spbT_LT.setValue(6)
        self.ui.spbWTIV_Capacity_Wt.setValue(3)
        self.ui.spbT_TP.setValue(7)
        self.ui.spbT_F.setValue(15)
        self.ui.spbWTIV_Capacity_F.setValue(3)
        self.ui.spbT_Pos.setValue(8)
        self.ui.spbT_UP_L.setValue(10)
        self.ui.spbT_Down.setValue(4)
        self.ui.spbT_Offload.setValue(4)
        self.ui.spb_W.setValue(20)

    def default_params_complete1(self):
        """Parâmetros default para a simulação complete 1"""

        self.ui.spbT_Blade_C.setValue(10)
        self.ui.spbT_Nacele_C.setValue(6)
        self.ui.spbT_UT_C.setValue(6)
        self.ui.spbT_LT_C.setValue(6)
        self.ui.spbN_Cycle_WT.setValue(3)
        self.ui.spbR_I.setValue(0.6)
        self.ui.spbR_E.setValue(1.4)
        self.ui.spbIF_I.setValue(3)
        self.ui.spbIF_E.setValue(2)
        self.ui.spbT_C.setValue(50)
        self.ui.spbT_P.setValue(0.78)
        self.ui.spbT_L_JUV.setValue(5.85)
        self.ui.spbN_Cycle_F.setValue(3)
        self.ui.spbT_C_OS.setValue(58.13)
        self.ui.spbT_L_Top_OS.setValue(3)

    def default_params_complete2(self):
        """Parâmetros default para a simulação complete 2"""

        self.ui.spbR_Ret.setValue(144)
        self.ui.spbRD.setValue(8)
        self.ui.spbT_Pos_DCBV.setValue(6)
        self.ui.spbT_A_DCBV.setValue(8)
        self.ui.spbT_Pos_JUV.setValue(3)
        self.ui.spbT_UP_JUV.setValue(6)
        self.ui.spbT_Down_JUV.setValue(1)
        self.ui.spbT_Pos_OSV.setValue(0.25)
        self.ui.spbT_Move_OSV.setValue(0.25)
        self.ui.spbWeather_Delay.setValue(20)

    def load_vessels(self):
        """Carrega arquivo de embarcações"""
        try:
            if self.table_vessels == {}:
                self.table_vessels["wtiv"] = load_data(
                    "vessel_wtiv.xlsx", "wtiv")
                self.table_vessels["heavy_lift"] = load_data(
                    "vessel_heavy_lift.xlsx", "heavy lift")
                self.table_vessels["cable_vessel"] = load_data(
                    "vessel_cable.xlsx", "cable vessel")
                self.table_vessels["barcaca"] = load_data(
                    "vessel_barcaca.xlsx", "barcaça")
                self.table_vessels["rebocador"] = load_data(
                    "vessel_rebocador.xlsx", "rebocador")
                self.table_vessels["rov"] = load_data(
                    "vessel_rov.xlsx", "rov")
                self.table_vessels["osv"] = load_data(
                    "vessel_osv.xlsx", "osv")
                self.table_vessels["dcbv"] = load_data(
                    "vessel_dcbv.xlsx", "dcbv")
                self.table_vessels["fallpipe_vessel"] = load_data(
                    "vessel_fallpipe.xlsx", "fallpipe_vessel")
        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar os arquivos de embarcações.\n\n'
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

    def add_vessels_partial(self):
        """
        Adiciona embarcações para a simulação parcial.
        As soluções de embarcações para este modelo devem incluir uma embarcação.
        """
        try:
            self.load_vessels()

            # Define a classe responsável pelas embarcações
            vessel_deco_partial = VesselDecoPartial(ui=self.ui)
            vessel_deco_partial.define_vessels(self.table_vessels)

            if self.ui.vesselSelectionDialog.exec_() == QDialog.Accepted:
                self.ui.treeVesselsDecoPartial.clear()
                df = vessel_deco_partial.get_vessels_df()
                self.dataframe_to_tree(df, self.ui.treeVesselsDecoPartial)
                self.ui.treeVesselsDecoPartial.expandAll()

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível definir as embarcações.\n\n'
                                 f'Problema: {ex}')

    def del_vessels_partial(self):
        """Exclui embarcações para a simulação parcial."""
        selected_item = self.ui.treeVesselsDecoPartial.currentItem()
        if selected_item is not None:
            index = self.ui.treeVesselsDecoPartial.indexOfTopLevelItem(
                selected_item)
            self.ui.treeVesselsDecoPartial.takeTopLevelItem(index)

    def get_params_partial(self, filtered_vessels):
        """Preenche a estrutura com os dados dos parâmetros da simulação parcial"""

        try:
            WT_P = str_to_float(self.ui.edtCapacity.text()) * 1000
            d_port = str_to_float(self.ui.edtL_shore.text())
            n_t = str_to_float(self.ui.edtTurbinesNumber.text())
            n_f = str_to_float(self.ui.edtTurbinesNumber.text())
            t_blades = self.ui.spbT_Blades.value()
            t_nacele = self.ui.spbT_Nacele.value()
            t_ut = self.ui.spbT_UT.value()
            t_lt = self.ui.spbT_LT.value()
            t_tp = self.ui.spbT_TP.value()
            t_f = self.ui.spbT_F.value()
            t_pos = self.ui.spbT_Pos.value()
            t_up_l = self.ui.spbT_UP_L.value()
            t_down = self.ui.spbT_Down.value()
            t_offload = self.ui.spbT_Offload.value()
            wtiv_speed = filtered_vessels['wtiv']["Velocidade carregado (kt)"].iloc[0]
            wtiv_capacity_wt = self.ui.spbWTIV_Capacity_Wt.value()
            wtiv_capacity_f = self.ui.spbWTIV_Capacity_F.value()
            cd_wtiv = filtered_vessels['wtiv']["Taxa diária (US$)"].iloc[0]
            mob_wtiv = filtered_vessels['wtiv']["Taxa de mobilização (US$)"].iloc[0]
            w = self.ui.spb_W.value() / 100 + 1
            n_os = str_to_float(self.ui.edtSubstationNumber.text())
            n_mm = 0
            return {
                'WT_P': WT_P,
                'd_port': d_port,
                'n_t': n_t,
                'n_f': n_f,
                't_blades': t_blades,
                't_nacelle': t_nacele,
                't_ut': t_ut,
                't_lt': t_lt,
                't_tp': t_tp,
                't_f': t_f,
                't_pos': t_pos,
                't_up_l': t_up_l,
                't_down': t_down,
                't_offload': t_offload,
                'wtiv_speed': wtiv_speed,
                'wtiv_capacity_wt': wtiv_capacity_wt,
                'wtiv_capacity_f': wtiv_capacity_f,
                'cd_wtiv': cd_wtiv,
                'mob_wtiv': mob_wtiv,
                'w': w,
                'n_os': n_os,
                'n_mm': n_mm
            }

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar os parâmetros de descomissionamento parcial.\n\n'
                                 f'Problema: {ex}')

    def set_data_foundations_wt(self, scour_volume):
        """Atribui para descomissionamento os dados calculados e definidos por estruturas"""
        self.scour_volume_wt = scour_volume

    def set_data_foundations_os(self, scour_volume):
        """Atribui para o descomissionamento os dados calculados e definidos por estruturas"""
        self.scour_volume_os = scour_volume

    def set_data_electric(self, export_length, inter_array_length):
        """Carrega aerogeradores do módulo de cabos e subestações"""
        self.params_electric["export"] = export_length
        self.params_electric["inter_array"] = inter_array_length

    def run_partial(self):
        """Preenche a estrutura com os dados dos parâmetros da simulação parcial"""

        try:
            self.select_scenarios()
            filtered_vessels = self.filtered_vessels()

            if filtered_vessels != {}:

                params = self.get_params_partial(filtered_vessels)

                if params is not None:
                    QGuiApplication.setOverrideCursor(Qt.WaitCursor)

                    if len(filtered_vessels["wtiv"]) == 1:
                        scenario = 2
                    else:
                        scenario = 3

                    self.simulation_result = run_simulation(params, scenario)

                    # Mostra os resultados na aba de resultados
                    self.fill_data_partial(self.simulation_result)

                    self.build_charts_partial(False)

                    self.ui.tabDecoResultsP.setEnabled(True)

                    self.next_visible_tab()
                    QGuiApplication.restoreOverrideCursor()

                    # Registra ação
                    cfg.cfg_run_deco_partial = True
                    cfg.cfg_run_deco_complete = False

        except Exception as ex:
            cfg.cfg_run_deco_partial = False
            QGuiApplication.restoreOverrideCursor()
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível fazer a simulação parcial do descomissionamento.\n'
                                 'Verifique os dados e tente novamente.\n\n'
                                 f'Problema: {ex}')

    def add_vessels_complete(self):
        """
        Adiciona embarcações para a simulação completa.
        As soluções de embarcações para este modelo devem incluir uma embarcação.
        """
        try:
            self.load_vessels()

            # Define a classe responsável pelas embarcações
            vessel_deco_complete = VesselDecoComplete(ui=self.ui)
            vessel_deco_complete.define_vessels(self.table_vessels)

            if self.ui.vesselSelectionDialog.exec_() == QDialog.Accepted:
                self.ui.treeVesselsDecoComplete.clear()
                df = vessel_deco_complete.get_vessels_df()
                self.dataframe_to_tree(df, self.ui.treeVesselsDecoComplete)
                self.ui.treeVesselsDecoComplete.expandAll()

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível definir as embarcações.\n\n'
                                 f'Problema: {ex}')

    def del_vessels_complete(self):
        """Exclui embarcações para a simulação completa."""
        selected_item = self.ui.treeVesselsDecoComplete.currentItem()
        if selected_item is not None:
            index = self.ui.treeVesselsDecoComplete.indexOfTopLevelItem(
                selected_item)
            self.ui.treeVesselsDecoComplete.takeTopLevelItem(index)

    def filtered_vessels(self):
        """ Filtra a embarcação para a metodologia"""

        filter = {}

        if self.ui.rdbDecoPartial.isChecked():
            selected_vessels = tree_with_child_to_dataframe(
                self.ui.treeVesselsDecoPartial)
        else:
            selected_vessels = tree_with_child_to_dataframe(
                self.ui.treeVesselsDecoComplete)

        def format_to_float(value):
            """ Função para converter os dados do formato "390.000,00" para float """
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
        filter["barcaca"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Barcaça'")
        filter["rebocador"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Rebocador'")
        filter["rov"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'ROV'")
        filter["osv"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'OSV'")
        filter["dcbv"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'DCBV'")
        filter["fallpipe_vessel"] = selected_vessels.query(
            "`Parent` == 1 and `Tipo` == 'Fallpipe Vessel'")

        if self.ui.rdbDecoPartial.isChecked():
            if filter["wtiv"].empty:
                QMessageBox.warning(None,
                                    'Erro',
                                    f'Defina uma solução de embaracação válida para a simulação parcial.')
                self.ui.tabsDeco.setCurrentIndex(0)
                return {}
        else:
            if filter["heavy_lift"].empty or filter["cable_vessel"].empty or filter["barcaca"].empty or filter["rebocador"].empty or filter["rov"].empty or filter["osv"].empty or filter["dcbv"].empty or filter["fallpipe_vessel"].empty:
                QMessageBox.warning(None,
                                    'Erro',
                                    'Defina uma solução de embaracação válida para a simulação completa.')
                self.ui.tabsDeco.setCurrentIndex(1)
                return {}

        return filter

    def build_charts_partial(self, plot_window=False, chart_number=0):
        """Plotagem dos gráficos"""
        if plot_window:
            plot_graphics(self.simulation_result, chart_number)
        else:
            plot_graphics(self.simulation_result, chart_number, self.canvas1,
                          self.canvas2, self.canvas3)

        self.view_chart1.setEnabled(True)
        self.view_chart2.setEnabled(True)
        self.view_chart3.setEnabled(True)

    def build_charts_complete(self, plot_window=False, chart_number=0):
        """Plotagem dos gráficos"""
        if plot_window:
            plot_graphics(self.simulation_result, chart_number)
        else:
            plot_graphics(self.simulation_result, chart_number, self.canvas4,
                          self.canvas5, self.canvas6)

        self.view_chart4.setEnabled(True)
        self.view_chart5.setEnabled(True)
        self.view_chart6.setEnabled(True)

    def fill_data_partial(self, simulation):
        """
        Mostrar os dados de custos
        """

        # Aerogeradores
        data = QTableWidgetItem(float_to_str(simulation["Wt_cost"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoPartialResults.setItem(0, 0, data)
        total = simulation["Wt_cost"]

        data = QTableWidgetItem(float_to_str(simulation["Tw"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoPartialResults.setItem(0, 1, data)
        total_time = simulation["Tw"]

        # Fundações aerogeradores
        data = QTableWidgetItem(float_to_str(
            simulation["Foundation_cost"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoPartialResults.setItem(1, 0, data)
        total += simulation["Foundation_cost"]

        data = QTableWidgetItem(float_to_str(
            simulation["Foundation_time"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoPartialResults.setItem(1, 1, data)
        total_time += simulation["Foundation_time"]

        # Fundações subestação
        data = QTableWidgetItem(float_to_str(simulation["Os_cost"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoPartialResults.setItem(2, 0, data)
        total += simulation["Os_cost"]

        data = QTableWidgetItem(float_to_str(simulation["T_total_os"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoPartialResults.setItem(2, 1, data)
        total_time += simulation["T_total_os"]

        total = total / 1000000

        # Total valor
        data = QTableWidgetItem(float_to_str(total))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        set_bold_font_data(data)
        self.ui.tableDecoPartialResults.setItem(3, 0, data)

        # Total tempo
        data = QTableWidgetItem(float_to_str(total_time))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        set_bold_font_data(data)
        self.ui.tableDecoPartialResults.setItem(3, 1, data)

        self.dict_format_partial = {}

        self.dict_format_partial["Valor (milhões de US$)"] = {
            "Aerogeradores": (simulation["Wt_cost"]/1000000),
            "Fundações": (simulation["Foundation_cost"]/1000000),
            "Subestação": (simulation["Os_cost"]/1000000),
            "TOTAL": total
        }

        self.dict_format_partial["Tempo (dias)"] = {
            "Aerogeradores": simulation["Tw"],
            "Fundações": simulation["Foundation_time"],
            "Subestação": (simulation["T_total_os"]/1000000),
            "TOTAL": total_time
        }

        self.ui.edtDecoTotal.setText(float_to_str(total))
        if cfg.cfg_run_lcoe:
            self.ui.lcoe.run()

    def fill_data_complete(self, simulation):
        """
        Mostrar os dados de custos
        """
        # Aerogeradores
        data = QTableWidgetItem(float_to_str(simulation["Wt_cost"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(0, 0, data)
        total = simulation["Wt_cost"]

        data = QTableWidgetItem(float_to_str(simulation["Tw"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(0, 1, data)
        total_time = simulation["Tw"]

        # Fundações aerogeradores
        data = QTableWidgetItem(float_to_str(
            simulation["Foundation_cost"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(1, 0, data)
        total += simulation["Foundation_cost"]

        data = QTableWidgetItem(float_to_str(simulation["Foundation_time"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(1, 1, data)
        total_time += simulation["Foundation_time"]

        # Subestação
        data = QTableWidgetItem(float_to_str(simulation["Os_cost"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(2, 0, data)
        total += simulation["Os_cost"]

        data = QTableWidgetItem(float_to_str(simulation["T_total_os"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(2, 1, data)
        total_time += simulation["T_total_os"]

        # Cabos
        data = QTableWidgetItem(float_to_str(
            simulation["Cables_cost"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(3, 0, data)
        total += simulation["Cables_cost"]

        data = QTableWidgetItem(float_to_str(simulation["T_total_cables"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(3, 1, data)
        total_time += simulation["T_total_cables"]

        # Limpeza do solo
        data = QTableWidgetItem(float_to_str(
            simulation["Seabed_clearance"]/1000000))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(4, 0, data)
        total += simulation["Seabed_clearance"]

        data = QTableWidgetItem(float_to_str(simulation["T_total_seabed"]))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.ui.tableDecoCompleteResults.setItem(4, 1, data)
        total_time += simulation["T_total_seabed"]

        total = total / 1000000

        # Total valor
        data = QTableWidgetItem(float_to_str(total))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        set_bold_font_data(data)
        self.ui.tableDecoCompleteResults.setItem(5, 0, data)

        # Total tempo
        data = QTableWidgetItem(float_to_str(total_time))
        data.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
        set_bold_font_data(data)
        self.ui.tableDecoCompleteResults.setItem(5, 1, data)

        self.dict_format_complete = {}

        self.dict_format_complete["Valor (milhões de US$)"] = {
            "Aerogeradores": (simulation["Wt_cost"]/1000000),
            "Fundações": (simulation["Foundation_cost"]/1000000),
            "Subestação": (simulation["Os_cost"]/1000000),
            "Cabos": (simulation["Cables_cost"]/1000000),
            "Limpeza do solo": (simulation["Seabed_clearance"]/1000000),
            "TOTAL": total
        }

        self.dict_format_complete["Tempo (dias)"] = {
            "Aerogeradores": simulation["Tw"],
            "Fundações": simulation["Foundation_time"],
            "Subestação": simulation["T_total_os"],
            "Cabos": simulation["T_total_cables"],
            "Limpeza do solo": simulation["T_total_seabed"],
            "TOTAL": total_time
        }

        self.ui.edtDecoTotal.setText(float_to_str(total))
        if cfg.cfg_run_lcoe:
            self.ui.lcoe.run()

    def get_params_complete(self, filtered_vessels):
        """Preenche a estrutura com os dados dos parâmetros da simulação parcial"""

        try:
            '''l_i = 34  
            l_e = 9  
            r_i = 0.6
            r_e = 1.4
            if_i = 3
            if_e = 2
            t_c = 50
            t_p = 0.78
            t_l_juv = 5.85
            n_juv_f = 1
            n_bv_f = 2
            n_tb_f = 2
            n_rov_f = 1
            n_cycle_f = 5
            t_l_top_mm = 3
            t_c_mm = 40.2
            n_juv_mm = 1  # não tem estação metereológica
            n_bv_mm = 1  # não tem estação metereológica
            n_tb_mm = 1  # não tem estação metereológica
            n_rov_mm = 1  # não tem estação metereológica
            t_c_os = 58.13
            t_l_top_os = 3
            n_juv_os = 1
            n_bv_os = 1
            n_tb_os = 1
            n_rov_os = 1
            cd_juv = 100
            cd_bv = 12.9
            cd_tb = 8.6
            cd_rov = 3.45
            cd_clv_i = 40
            cd_clv_e = 40
            cd_dcbv = 50
            cd_rdv = 11.9
            cd_osv = 3.9
            c_mob_juv = 400
            c_mob_bv = 172.4
            c_mob_tb = 0
            c_mob_rov = 34.48
            c_mob_clv_i = 445
            c_mob_clv_e = 445
            c_mob_dcbv = 100
            c_mob_rdv = 10.6
            c_mov_osv = 0
            v_i_wt = 575  # TODO Proteção de erosão para aerogeradores
            v_i_os = 575  # TODO Proteção de erosão para subestação
            v_i_mm = 575  # não tem estação metereológica
            r_ret = 144
            r_rd = 8
            t_pos_dcbv = 6
            t_a_dcbv = 8
            t_pos_juv = 3
            t_up_juv = 6
            t_down_juv = 1
            t_pos_osv = 0.25
            t_move_osv = 0.25
            weather_delay = 1.2
            d_port = 8.5
            n_t = 48
            n_os = 1
            n_mm = 1  # não tem estação metereológica
            WT_P = 172.8
            t_b_n = 8.5
            t_t = 6
            n_juv_wt = 1
            n_bv_wt = 2
            n_tb_wt = 2
            n_cycle_wt = 2'''

            l_i = self.params_electric["inter_array"]
            l_e = self.params_electric["export"]
            r_i = self.ui.spbR_I.value()
            r_e = self.ui.spbR_E.value()
            if_i = self.ui.spbIF_I.value()
            if_e = self.ui.spbIF_E.value()
            t_c = self.ui.spbT_C.value()
            t_p = self.ui.spbT_P.value()
            t_l_juv = self.ui.spbT_L_JUV.value()
            n_juv_f = len(filtered_vessels['heavy_lift'])
            n_bv_f = len(filtered_vessels['barcaca'])
            n_tb_f = len(filtered_vessels['rebocador'])
            n_rov_f = len(filtered_vessels['rov'])
            n_cycle_f = self.ui.spbN_Cycle_F.value()
            t_l_top_mm = 0  # não tem estação metereológica
            t_c_mm = 0  # não tem estação metereológica
            n_juv_mm = 0  # não tem estação metereológica
            n_bv_mm = 0  # não tem estação metereológica
            n_tb_mm = 0  # não tem estação metereológica
            n_rov_mm = 0  # não tem estação metereológica
            t_c_os = self.ui.spbT_C_OS.value()
            t_l_top_os = self.ui.spbT_L_Top_OS.value()
            n_juv_os = len(filtered_vessels['heavy_lift'])
            n_bv_os = len(filtered_vessels['barcaca'])
            n_tb_os = len(filtered_vessels['rebocador'])
            n_rov_os = len(filtered_vessels['rov'])
            cd_juv = filtered_vessels['heavy_lift']["Taxa diária (US$)"].iloc[0]
            cd_bv = filtered_vessels['barcaca']["Taxa diária (US$)"].iloc[0]
            cd_tb = filtered_vessels['rebocador']["Taxa diária (US$)"].iloc[0]
            cd_rov = filtered_vessels['rov']["Taxa diária (US$)"].iloc[0]
            cd_clv_i = filtered_vessels['cable_vessel']["Taxa diária (US$)"].iloc[0]
            cd_clv_e = cd_clv_i
            cd_dcbv = filtered_vessels['dcbv']["Taxa diária (US$)"].iloc[0]
            cd_rdv = filtered_vessels['fallpipe_vessel']["Taxa diária (US$)"].iloc[0]
            cd_osv = filtered_vessels['osv']["Taxa diária (US$)"].iloc[0]
            c_mob_juv = filtered_vessels['heavy_lift'][
                "Taxa de mobilização (US$)"].iloc[0]
            c_mob_bv = filtered_vessels['barcaca']["Taxa de mobilização (US$)"].iloc[0]
            c_mob_tb = filtered_vessels['rebocador']["Taxa de mobilização (US$)"].iloc[0]
            c_mob_rov = filtered_vessels['rov']["Taxa de mobilização (US$)"].iloc[0]
            c_mob_clv_i = filtered_vessels['cable_vessel'][
                "Taxa de mobilização (US$)"].iloc[0]
            c_mob_clv_e = c_mob_clv_i
            c_mob_dcbv = filtered_vessels['dcbv']["Taxa de mobilização (US$)"].iloc[0]
            c_mob_rdv = filtered_vessels['fallpipe_vessel']["Taxa de mobilização (US$)"].iloc[
                0]
            c_mov_osv = filtered_vessels['osv']["Taxa de mobilização (US$)"].iloc[0]
            v_i_wt = self.scour_volume_wt
            v_i_os = self.scour_volume_os
            v_i_mm = 0  # não tem estação metereológica
            r_ret = self.ui.spbR_Ret.value()
            r_rd = self.ui.spbRD.value()
            t_pos_dcbv = self.ui.spbT_Pos_DCBV.value()
            t_a_dcbv = self.ui.spbT_A_DCBV.value()
            t_pos_juv = self.ui.spbT_Pos_JUV.value()
            t_up_juv = self.ui.spbT_UP_JUV.value()
            t_down_juv = self.ui.spbT_Down_JUV.value()
            t_pos_osv = self.ui.spbT_Pos_OSV.value()
            t_move_osv = self.ui.spbT_Move_OSV.value()
            weather_delay = self.ui.spbWeather_Delay.value()
            d_port = str_to_float(self.ui.edtL_shore.text())
            n_t = str_to_float(self.ui.edtTurbinesNumber.text())
            n_os = str_to_float(self.ui.edtSubstationNumber.text())
            n_mm = 0  # não tem estação metereológica
            WT_P = str_to_float(self.ui.edtCapacity.text()) * 1000
            t_b_n = self.ui.spbT_Blade_C.value() + self.ui.spbT_Nacele_C.value()
            t_t = self.ui.spbT_UT_C.value() + self.ui.spbT_LT_C.value()
            n_juv_wt = len(filtered_vessels['heavy_lift'])
            n_bv_wt = len(filtered_vessels['barcaca'])
            n_tb_wt = len(filtered_vessels['rebocador'])
            n_cycle_wt = self.ui.spbN_Cycle_WT.value()
            return {
                'WT_P': WT_P,
                'l_i': l_i,
                'l_e': l_e,
                'r_i': r_i,
                'r_e': r_e,
                'if_i': if_i,
                'if_e': if_e,
                't_c': t_c,
                't_p': t_p,
                't_l_juv': t_l_juv,
                'n_juv_f': n_juv_f,
                'n_bv_f': n_bv_f,
                'n_tb_f': n_tb_f,
                'n_rov_f': n_rov_f,
                'n_cycle_f': n_cycle_f,
                't_l_top_mm': t_l_top_mm,
                't_c_mm': t_c_mm,
                'n_juv_mm': n_juv_mm,
                'n_bv_mm': n_bv_mm,
                'n_tb_mm': n_tb_mm,
                'n_rov_mm': n_rov_mm,
                't_c_os': t_c_os,
                't_l_top_os': t_l_top_os,
                'n_juv_os': n_juv_os,
                'n_bv_os': n_bv_os,
                'n_tb_os': n_tb_os,
                'n_rov_os': n_rov_os,
                'cd_juv': cd_juv,
                'cd_bv': cd_bv,
                'cd_tb': cd_tb,
                'cd_rov': cd_rov,
                'cd_clv_i': cd_clv_i,
                'cd_clv_e': cd_clv_e,
                'cd_dcbv': cd_dcbv,
                'cd_rdv': cd_rdv,
                'cd_osv': cd_osv,
                'c_mob_juv': c_mob_juv,
                'c_mob_bv': c_mob_bv,
                'c_mob_tb': c_mob_tb,
                'c_mob_rov': c_mob_rov,
                'c_mob_clv_i': c_mob_clv_i,
                'c_mob_clv_e': c_mob_clv_e,
                'c_mob_dcbv': c_mob_dcbv,
                'c_mob_rdv': c_mob_rdv,
                'c_mov_osv': c_mov_osv,
                'v_i_wt': v_i_wt,
                'v_i_os': v_i_os,
                'v_i_mm': v_i_mm,
                'r_ret': r_ret,
                'r_rd': r_rd,
                't_pos_dcbv': t_pos_dcbv,
                't_a_dcbv': t_a_dcbv,
                't_pos_juv': t_pos_juv,
                't_up_juv': t_up_juv,
                't_down_juv': t_down_juv,
                't_pos_osv': t_pos_osv,
                't_move_osv': t_move_osv,
                'weather_delay': weather_delay,
                'd_port': d_port,
                'n_t': n_t,
                'n_os': n_os,
                'n_mm': n_mm,
                'WT_P': WT_P,
                't_b_n': t_b_n,
                't_t': t_t,
                'n_juv_wt': n_juv_wt,
                'n_bv_wt': n_bv_wt,
                'n_tb_wt': n_tb_wt,
                'n_cycle_wt': n_cycle_wt
            }

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível carregar os parâmetros de descomissionamento completo.\n\n'
                                 f'Problema: {ex}')

    def run_complete(self):
        """Preenche a estrutura com os dados dos parâmetros da simulação completa"""

        try:
            self.select_scenarios()
            filtered_vessels = self.filtered_vessels()

            if filtered_vessels != {}:

                params = self.get_params_complete(filtered_vessels)

                if params is not None:
                    QGuiApplication.setOverrideCursor(Qt.WaitCursor)
                    self.simulation_result = run_simulation(params, 1)

                    # Mostra os resultados na aba de resultados
                    self.fill_data_complete(self.simulation_result)

                    self.build_charts_complete(False)

                    self.ui.tabDecoResultsC.setEnabled(True)

                    self.next_visible_tab()
                    QGuiApplication.restoreOverrideCursor()

                    # Registra ação
                    cfg.cfg_run_deco_complete = True
                    cfg.cfg_run_deco_partial = False
                

        except Exception as ex:
            cfg.cfg_run_deco_complete = False
            QGuiApplication.restoreOverrideCursor()
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível fazer a simulação completa do descomissionamento.\n'
                                 'Verifique os dados e tente novamente.\n\n'
                                 f'Problema: {ex}')

    def export(self, type):
        """
        Salvar simulação do Descomissionamento Parcial   
        """

        if type == 0:
            dict_format = self.dict_format_partial
        else:
            dict_format = self.dict_format_complete

        try:
            if (dict_format is None):
                QMessageBox.warning(None,
                                    'Erro',
                                    'Não há dados para serem salvos.\n'
                                    'Faça a simulação e tente novamente.')
                return

            filename, _filter = QFileDialog.getSaveFileName(
                directory=cfg.dir_results,
                caption='Exportar resultados de descomissionamento',
                filter='XLS (*.xlsx)')

            if filename is not None and filename != '':
                # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')

                # Descomissionamento
                df = pd.DataFrame.from_dict(dict_format)
                df.to_excel(writer, sheet_name='Descomissionamento')

                workbook = writer.book

                worksheet = workbook.add_worksheet('Gráficos')
                if os.path.exists(temp_file('deco1.png')):
                    worksheet.insert_image(
                        "A1", temp_file('deco1.png'), {
                            "x_offset": 15, "y_offset": 10}
                    )
                if os.path.exists(temp_file('deco2.png')):
                    worksheet.insert_image(
                        "L1", temp_file('deco2.png'), {
                            "x_offset": 15, "y_offset": 10}
                    )
                if os.path.exists(temp_file('deco3.png')):
                    worksheet.insert_image(
                        "A26",
                        temp_file('deco3.png'),
                        {"x_offset": 15, "y_offset": 10},
                    )

                # Fecha o ExcelWriter e gera o arquivo .xlsx
                writer.close()

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Não foi possível gerar o arquivo de resultados.\n'
                                 'Execute novamente a simulação e tente novamente.\n\n'
                                 f'Problema: {ex}')
