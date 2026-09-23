"""
Configurações de Construtibilidade
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QTableWidgetItem
from PyQt5.QtCore import Qt
from ...utils.utils import *


class VesselMonopileJacket(QtWidgets.QDialog):

    def __init__(self, ui):
        super(VesselMonopileJacket, self).__init__()

        self.ui_parent = ui
        self.ui = ui.vesselSelectionDialog.ui

        # Embarcações
        self.df_vessels = pd.DataFrame()
        self.table_vessels = {}

        # Tables Vessel
        self.ui.treeVessels.header().setFixedHeight(50)
        self.ui.treeVessels.header().setDefaultAlignment(
            Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))

        # Eventos janela de configuração de embarcação
        self.ui.btnFilter.clicked.connect(self.filter)
        self.ui.btnVesselsSelect.clicked.connect(self.select_vessel)
        self.ui.btnVesselsUpdate.clicked.connect(self.update_vessel)
        self.ui.btnVesselsDelete.clicked.connect(self.delete_vessel)
        self.ui.btnCancel.clicked.connect(self.cancel)
        self.ui.btnSave.clicked.connect(self.save)

        # Eventos janela de configuração da ebarcação
        self.ui_parent.configVesselDialog.ui.btnOK.clicked.connect(
            self.config_ok)
        self.ui_parent.configVesselDialog.ui.btnCancel.clicked.connect(
            self.config_cancel)

    def vessels_options(self):
        """Define as opções possíveis para as fundações monopile e jaqueta"""

        # Limpar itens anteriores
        self.ui.cbxVesselType.clear()
        self.ui.treeVessels.clear()

        # Adicionando vários itens de uma vez
        items = ["WTIV",
                 "Cable Vessel",
                 "Heavy Lift/Jack Up",
                 "Fallpipe Vessel",
                 "Barcaça"]
        self.ui.cbxVesselType.addItems(items)

    def define_vessels(self, vessels):
        """Define as embarcações"""

        self.df_vessels = pd.DataFrame()

        # Define as opções possíveis
        self.vessels_options()

        self.table_vessels = vessels
        self.filter()

    def get_vessels_df(self):
        """Define as embarcações listadas pela construtibilidade"""
        return self.df_vessels

    def filter(self):
        """Aplica filtros na tabela de embarcações"""
        try:
            vessel_type = self.ui.cbxVesselType.currentText()
            list_models = None
            if vessel_type == "WTIV":
                list_models = self.table_vessels["wtiv"]["nome_embarcacao"].values.tolist(
                )
                list_models.sort()
                self.add_list_vessels(
                    self.table_vessels["wtiv"], list_models, vessel_type)
            elif vessel_type == "Cable Vessel":
                list_models = self.table_vessels["cable_vessel"]["nome_embarcacao"].values.tolist(
                )
                list_models.sort()
                self.add_list_vessels(
                    self.table_vessels["cable_vessel"], list_models, vessel_type)
            elif vessel_type == "Heavy Lift/Jack Up":
                list_models = self.table_vessels["heavy_lift"]["nome_embarcacao"].values.tolist(
                )
                list_models.sort()
                self.add_list_vessels(
                    self.table_vessels["heavy_lift"], list_models, vessel_type)
            elif vessel_type == "Fallpipe Vessel":
                list_models = self.table_vessels["fallpipe_vessel"]["nome_embarcacao"].values.tolist(
                )
                list_models.sort()
                self.add_list_vessels(
                    self.table_vessels["fallpipe_vessel"], list_models, vessel_type)
            else:
                list_models = self.table_vessels["barcaca"]["nome_embarcacao"].values.tolist(
                )
                list_models.sort()
                self.add_list_vessels(
                    self.table_vessels["barcaca"], list_models, vessel_type)

        except ValueError as ex:
            print(ex)
            QMessageBox.warning(None, 'Erro', 'Valores inválidos nos filtros.')
            return

    def add_list_vessels(self, df_vessel, list_models, vessel_type):
        """
        Mostrar os dados de embarcações na tabela, com colunas dinâmicas dependendo do tipo de embarcação.
        Se o tipo for "Cable Vessel", as colunas de área do deck e capacidade de carga são substituídas por capacidade de carrossel.
        :param df_vessel: DataFrame contendo os dados das embarcações
        :param list_models: Lista de modelos de embarcações
        :param vessel_type: Tipo da embarcação (ex., "Cable Vessel")
        """

        # Definir colunas da tabela
        column_headers = [
            "Tipo", "Embarcação", "Área do deck (m²)", "Máxima capacidade de carga (t/m²)",
            "Máxima capacidade do carrossel (t)", "Capacidade instalação (t/h)", "Taxa diária(US$)", "Taxa de mobilização(US$)",
            "Velocidade vazio (kt)", "Velocidade carregado (kt)", "Velocidade máxima do vento (m/s)", "Altura máxima da onda (m)"]

        self.ui.tableListVessels.setRowCount(0)
        self.ui.tableListVessels.setRowCount(len(list_models))
        self.ui.tableListVessels.setColumnCount(
            len(column_headers))

        # Atualizar cabeçalhos
        self.ui.tableListVessels.setHorizontalHeaderLabels(column_headers)

        self.ui.tableListVessels.horizontalHeader().setFixedHeight(50)
        self.ui.tableListVessels.horizontalHeader().setDefaultAlignment(
            Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))

        # Função auxiliar para adicionar itens com alinhamento
        def add_item(row, col, value, alignment=None):
            item = QTableWidgetItem(value)
            if alignment != None:
                item.setTextAlignment(alignment)
            self.ui.tableListVessels.setItem(row, col, item)

        for r, vessel in enumerate(list_models):

            vessel_data = df_vessel.loc[df_vessel["nome_embarcacao"] == vessel]

            if vessel_data.empty:
                continue  # Se o filtro estiver vazio, pula a iteração

            # Preencher colunas comuns
            add_item(r, 0, vessel_type)  # Coluna "Tipo"
            # Coluna "Embarcação"
            add_item(r, 1, vessel_data["nome_embarcacao"].values[0])
            # Coluna "Taxa diária"
            add_item(r, 6, float_to_str(
                vessel_data["taxa_diaria_($)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
            # Coluna "Taxa de mobilização"
            add_item(r, 7, float_to_str(
                vessel_data["taxa_mobilizacao_($)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
            # Coluna "Velocidade vazio"
            add_item(r, 8, float_to_str(
                vessel_data["velocidade_locomocao_(kt)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
            # Coluna "Velocidade carregado"
            add_item(r, 9, float_to_str(
                vessel_data["velocidade_locomocao_carga_(kt)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
            # Coluna "Velocidade máxima do vento"
            add_item(r, 10, float_to_str(
                vessel_data["vel_max_vento_(m/s)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
            # Coluna "Velocidade carregado"
            add_item(r, 11, float_to_str(
                vessel_data["alt_max_onda_(m)"].values[0]), Qt.AlignRight | Qt.AlignCenter)

            if vessel_type != "Rebocador":
                # Diferenciação entre "Cable Vessel" e outros tipos de embarcação
                if vessel_type == "Cable Vessel":
                    # Coluna "Máx. Capacidade do Carrossel"
                    add_item(r, 4, float_to_str(
                        vessel_data["max_cap_carrossel_(t)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
                elif vessel_type == "Fallpipe Vessel":
                    # Coluna "Capacidade instalação (t/h)"
                    add_item(r, 5, float_to_str(
                        vessel_data["capacidade_instalacao_(t/h)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
                else:
                    # Coluna "Área do deck"
                    add_item(r, 2, float_to_str(
                        vessel_data["area_deck_livre_(m2)"].values[0]), Qt.AlignRight | Qt.AlignCenter)
                    # Coluna "Máx. Capacidade de Carga"
                    add_item(r, 3, float_to_str(
                        vessel_data["max_cap_carga_deck_(t/m2)"].values[0]), Qt.AlignRight | Qt.AlignCenter)

        # Dicionário que mapeia o tipo de embarcação para as colunas a serem removidas
        colunas_remover = {
            # Colunas correspondentes a "Área do deck (m²)", "Máxima capacidade de carga (t/m²)", "Capacidade instalação (t/h)"
            "Cable Vessel": [2, 3, 5],
            # Colunas correspondentes a "Área do deck (m²)", "Máxima capacidade de carga (t/m²)", "Máx. Capacidade do Carrossel (t)"
            "Fallpipe Vessel": [2, 3, 4],
            # Colunas correspondentes a "Área do deck (m²)", "Máxima capacidade de carga (t/m²)", "Máx. Capacidade do Carrossel (t)", "Capacidade instalação (t/h)"
            "Rebocador": [2, 3, 4, 5]
        }

        # Ajustar colunas com base no tipo de embarcação
        if vessel_type in colunas_remover:
            # Remover colunas de trás para frente para evitar problemas de índice
            for coluna in sorted(colunas_remover[vessel_type], reverse=True):
                self.ui.tableListVessels.removeColumn(coluna)
        else:
            # Caso não seja um tipo específico de embarcação, remover a coluna 4 (Máx. Capacidade do Carrossel)
            self.ui.tableListVessels.removeColumn(4)
            self.ui.tableListVessels.removeColumn(4)

    def select_vessel(self):
        """Adiciona embarcações na solução de embarcação"""

        try:
            selected_vessel = self.ui.tableListVessels.selectedIndexes()
            if not selected_vessel:
                QMessageBox.critical(None, 'Erro', 'Selecione uma embarcação.')
            else:

                vessel_type = self.ui.tableListVessels.item(
                    selected_vessel[0].row(), 0).text()

                vessel = self.ui.tableListVessels.item(
                    selected_vessel[0].row(), 1).text()

                if vessel is not None and vessel_type is not None:
                    # Definir o DataFrame correspondente ao tipo de embarcação
                    if vessel_type == "WTIV":
                        df_vessel = self.table_vessels["wtiv"]
                    elif vessel_type == "Cable Vessel":
                        df_vessel = self.table_vessels["cable_vessel"]
                    elif vessel_type == "Heavy Lift/Jack Up":
                        df_vessel = self.table_vessels["heavy_lift"]
                    elif vessel_type == "Fallpipe Vessel":
                        df_vessel = self.table_vessels["fallpipe_vessel"]
                    else:
                        df_vessel = self.table_vessels["barcaca"]

                    # Filtrar o DataFrame para encontrar a embarcação selecionada
                    filtro = df_vessel.loc[df_vessel["nome_embarcacao"] == vessel]

                    item = QTreeWidgetItem([vessel_type, filtro["nome_embarcacao"].values[0],
                                            float_to_str(
                                                filtro["taxa_diaria_($)"].values[0]),
                                            float_to_str(
                                                filtro["taxa_mobilizacao_($)"].values[0]),
                                            float_to_str(
                                                filtro["velocidade_locomocao_(kt)"].values[0]),
                                            float_to_str(
                                                filtro["velocidade_locomocao_carga_(kt)"].values[0]),
                                            float_to_str(
                                                filtro["vel_max_vento_(m/s)"].values[0]),
                                            float_to_str(filtro["alt_max_onda_(m)"].values[0])])

                    # Definir a primeira coluna como negrito
                    set_bold_font(item, 0)

                    # Alinhar alguns itens à direita
                    item.setTextAlignment(2, Qt.AlignRight | Qt.AlignVCenter)
                    item.setTextAlignment(3, Qt.AlignRight | Qt.AlignVCenter)
                    item.setTextAlignment(4, Qt.AlignRight | Qt.AlignVCenter)
                    item.setTextAlignment(5, Qt.AlignRight | Qt.AlignVCenter)
                    item.setTextAlignment(6, Qt.AlignRight | Qt.AlignVCenter)
                    item.setTextAlignment(7, Qt.AlignRight | Qt.AlignVCenter)

                    # Adicionar o item ao QTreeWidget
                    self.ui.treeVessels.addTopLevelItem(item)

        except Exception as ex:
            QMessageBox.critical(None,
                                 'Erro',
                                 'Erro ao adicionar a embarcação.\n\n'
                                 f'Problema: {ex}')

    def delete_vessel(self):
        """Exclui embarcação selecionada"""
        selected_item = self.ui.treeVessels.currentItem()
        if selected_item is not None:
            index = self.ui.treeVessels.indexOfTopLevelItem(selected_item)
            self.ui.treeVessels.takeTopLevelItem(index)

    def update_vessel(self):
        """Altera dados de custo e velocidade da embarcação selecionada"""

        selected_item = self.ui.treeVessels.currentItem()

        if selected_item is not None:
            # Atribui os dados da embarcação selecionada
            self.ui_parent.configVesselDialog.ui.spdTaxaDiaria.setValue(
                str_to_float(selected_item.text(2)))
            self.ui_parent.configVesselDialog.ui.spdTaxaMobilizacao.setValue(
                str_to_float(selected_item.text(3)))
            self.ui_parent.configVesselDialog.ui.spdVelVazio.setValue(
                str_to_float(selected_item.text(4)))
            self.ui_parent.configVesselDialog.ui.spdVelCarregado.setValue(
                str_to_float(selected_item.text(5)))
            self.ui_parent.configVesselDialog.ui.spdVelMaxVento.setValue(
                str_to_float(selected_item.text(6)))
            self.ui_parent.configVesselDialog.ui.spdAltMaxOnda.setValue(
                str_to_float(selected_item.text(7)))

            # Mostra a janela para o input dos dados
            self.ui_parent.configVesselDialog.show()

    def config_ok(self):
        """Fecha a janela de configuração de embarcações salvando os dados inseridos"""

        selected_item = self.ui.treeVessels.currentItem()

        if selected_item is not None:
            # Atribui os dados para a embarcação selecionada
            selected_item.setText(2, float_to_str(
                self.ui_parent.configVesselDialog.ui.spdTaxaDiaria.value(), 2))
            selected_item.setText(3, float_to_str(
                self.ui_parent.configVesselDialog.ui.spdTaxaMobilizacao.value(), 2))
            selected_item.setText(4, float_to_str(
                self.ui_parent.configVesselDialog.ui.spdVelVazio.value(), 2))
            selected_item.setText(5, float_to_str(
                self.ui_parent.configVesselDialog.ui.spdVelCarregado.value(), 2))
            selected_item.setText(6, float_to_str(
                self.ui_parent.configVesselDialog.ui.spdVelMaxVento.value(), 2))
            selected_item.setText(7, float_to_str(
                self.ui_parent.configVesselDialog.ui.spdAltMaxOnda.value(), 2))

            self.ui_parent.configVesselDialog.close()

    def config_cancel(self):
        """Fecha a janela de configuração de embarcações sem nenhuma ação"""
        self.ui_parent.configVesselDialog.close()

    def cancel(self):
        """Código para cancelar e fechar janela de criação de conjunto de embarcação"""
        self.ui_parent.vesselSelectionDialog.reject()

    def save(self):
        """Código para cancelar e salvar janela de criação de conjunto de embarcação"""

        df = tree_to_dataframe(self.ui.treeVessels)

        if df.empty:
            QMessageBox.warning(None,
                                'Erro',
                                'A lista de embarcações não foi definida.\n'
                                'Corrija para que seja possível salvar a lista.')
        else:
            is_wtiv = 'WTIV' in df['Tipo'].values
            is_cable_vessel = 'Cable Vessel' in df['Tipo'].values
            is_fallpipe_vessel = 'Fallpipe Vessel' in df['Tipo'].values
            is_heavy_lift = 'Heavy Lift/Jack Up' in df['Tipo'].values
            if (not is_wtiv) or (not is_cable_vessel) or (not is_heavy_lift) or (not is_fallpipe_vessel):
                QMessageBox.warning(None,
                                    'Erro',
                                    'As soluções de embarcações para essa configuração de parque deve ter no mínimo uma embarcação WTIV, um Cable Vessel, um Heavy Lift/Jack Up e um Fallpipe Vessel. \n'
                                    'Corrija para que seja possível salvar a lista.')
            else:
                # Itera sobre as linhas do DataFrame
                self.df_vessels = df
                self.ui_parent.vesselSelectionDialog.accept()
