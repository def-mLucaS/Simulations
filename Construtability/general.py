from .Entidades.Turbina import Turbina
from .Entidades.Parque import Parque
from .Entidades.Planta import Planta
from .Entidades.Porto import Porto
from .MovimentacaoComponente.SolucaoEmbarcacao import SolucaoEmbarcacao
from .MovimentacaoComponente.Guindaste import Guindaste
from .MovimentacaoComponente.Wtiv import Wtiv
from .MovimentacaoComponente.HeavyLift import HeavyLift
from .MovimentacaoComponente.CableVessel import CableVessel
from .MovimentacaoComponente.Fallpipe import Fallpipe
from .MovimentacaoComponente.Barcaca import Barcaca
from .MovimentacaoComponente.Rebocador import Rebocador
from .MovimentacaoComponente.ConjuntoRebocadores import ConjuntoRebocadores
from .MovimentacaoComponente.ConjuntoRebocadoresBarcaca import ConjuntoRebocadoresBarcaca
from .Cronograma.Cronograma import Cronograma
from ...utils.utils import str_to_float


class General:

    def __init__(self):

        self.latitude = 0
        self.longitude = 0
        self.parque = 0
        self.porto = 0

    def set_parque(self, site, project_name, start_date):
        """Define o parque"""

        planta = self.get_planta(site)
        # (Nome parque/simulacao, data de inicio da instalacao, planta)
        self.parque = Parque(project_name, start_date, planta)

    def get_parque(self):
        return self.parque

    def set_porto(self, porto, latitude, logitude):
        """Define o porto"""

        self.latitude = float(latitude)
        self.longitude = float(logitude)

        self.porto = Porto(porto, self.latitude, self.longitude)

    def get_porto(self):
        return self.porto

    def get_planta(self, wind_coordinates):
        """Define a planta"""
        dict_turbinas = dict()
        idx = 0
        for coord in wind_coordinates:
            turbina = Turbina(idx, coord[0], coord[1], 15)
            dict_turbinas[idx] = turbina
            idx += 1

        planta = Planta(dict_turbinas)
        return planta

    def get_solucao_embarcacao(self, filtered_vessels, vessels):
        """Cria uma Solução de Embarcação"""

        _vessels = []
        solucao_embarcacao = []

        count_wtiv = 0
        count_barcaca = 0

        for index, row in filtered_vessels["wtiv"].iterrows():
            item_data = vessels["wtiv"].loc[vessels["wtiv"]["nome_embarcacao"]
                                            == row["Embarcação"]]
            if not item_data.empty:
                count_wtiv = count_wtiv + 1
                class_wtiv = self.get_wtiv(item_data, row, count_wtiv)
                _vessels.append(class_wtiv)

        for index, row in filtered_vessels["barcaca"].iterrows():
            item_data = vessels["barcaca"].loc[vessels["barcaca"]["nome_embarcacao"]
                                               == row["Embarcação"]]
            if not item_data.empty:
                count_barcaca = count_barcaca + 1
                class_barcaca = self.get_barcaca(item_data, row, count_barcaca)
                _vessels.append(class_barcaca)

        solucao_embarcacao = SolucaoEmbarcacao(*_vessels)
        return solucao_embarcacao

    def get_solucao_embarcacao_gravity(self, filtered_vessels, vessels):
        """Cria uma Solução de Embarcação"""

        _vessels = []
        _rebocadores = []
        _barcacas = []
        solucao_embarcacao = []

        count_heavy_lift = 0
        count_barcaca = 0
        count_rebocador = 0

        for index, row in filtered_vessels["heavy_lift"].iterrows():
            item_data = vessels["heavy_lift"].loc[vessels["heavy_lift"]["nome_embarcacao"]
                                                  == row["Embarcação"]]
            if not item_data.empty:
                count_heavy_lift = count_heavy_lift + 1
                class_heavy_lift = self.get_heavy_lift(
                    item_data, row, count_heavy_lift)
                _vessels.append(class_heavy_lift)

        for index, row in filtered_vessels["barcaca"].iterrows():
            item_data = vessels["barcaca"].loc[vessels["barcaca"]["nome_embarcacao"]
                                               == row["Embarcação"]]
            if not item_data.empty:
                count_barcaca = count_barcaca + 1
                class_barcaca = self.get_barcaca(
                    item_data, row,  count_barcaca)
                _barcacas.append(class_barcaca)

        for index, row in filtered_vessels["rebocador"].iterrows():
            item_data = vessels["rebocador"].loc[vessels["rebocador"]["nome_embarcacao"]
                                                 == row["Embarcação"]]
            if not item_data.empty:
                count_rebocador = count_rebocador + 1
                class_rebocador = self.get_rebocador(
                    item_data, row, count_rebocador)
                _rebocadores.append(class_rebocador)

        if len(_barcacas) > 0 and len(_rebocadores) > 0:

            # Agrupando as barcaças com os rebocadores
            sobra_barcacas = []
            sobra_rebocadores = []

            # Itera sobre as listas até que a menor seja esgotada
            idx = 1
            for barcaca, rebocador in zip(_barcacas, _rebocadores):
                agrupamento = ConjuntoRebocadoresBarcaca(
                    "RebocadoresBarcaca{}".format(idx), rebocador, barcaca)
                agrupamento.setPosicao((self.latitude, self.longitude))
                _vessels.append(agrupamento)
                idx += idx

            # Se houver sobras em barcacas
            if len(_barcacas) > len(_rebocadores):
                sobra_barcacas = _barcacas[len(_rebocadores):]
                _vessels.extend(sobra_barcacas)

            # Se houver sobras em rebocadores
            if len(_rebocadores) > len(_barcacas):
                sobra_rebocadores = _rebocadores[len(_barcacas):]
                conjunto = ConjuntoRebocadores(
                    "Rebocadores", *sobra_rebocadores)
                conjunto.setPosicao((self.latitude, self.longitude))
                _vessels.append(conjunto)

        else:
            if len(_barcacas) > 0:
                _vessels.extend(_barcacas)
            elif len(_rebocadores) > 0:
                conjunto = ConjuntoRebocadores("Rebocadores", *_rebocadores)
                conjunto.setPosicao((self.latitude, self.longitude))
                _vessels.append(conjunto)

        solucao_embarcacao = SolucaoEmbarcacao(*_vessels)
        return solucao_embarcacao

    def get_solucao_embarcacao_fundacao_subestacao(self, filtered_vessels, vessels):
        """Cria uma Solução de Embarcação para subestação"""

        _vessels = []
        solucao_embarcacao = []

        count_heavy_lift = 0

        for index, row in filtered_vessels["heavy_lift"].iterrows():
            item_data = vessels["heavy_lift"].loc[vessels["heavy_lift"]["nome_embarcacao"]
                                                  == row["Embarcação"]]
            if not item_data.empty:
                count_heavy_lift = count_heavy_lift + 1
                class_heavy_lift = self.get_heavy_lift(
                    item_data, row, count_heavy_lift)
                _vessels.append(class_heavy_lift)

        solucao_embarcacao = SolucaoEmbarcacao(*_vessels)
        return solucao_embarcacao

    def get_solucao_embarcacao_cabos(self, filtered_vessels, vessels):
        """Cria uma Solução de Embarcação para subestação"""

        _vessels = []
        solucao_embarcacao = []

        count_cable_vessel = 0

        for index, row in filtered_vessels["cable_vessel"].iterrows():
            item_data = vessels["cable_vessel"].loc[vessels["cable_vessel"]["nome_embarcacao"]
                                                    == row["Embarcação"]]
            if not item_data.empty:
                count_cable_vessel = count_cable_vessel + 1
                class_cable_vessel = self.get_cable_vessel(
                    item_data, row, count_cable_vessel)
                _vessels.append(class_cable_vessel)

        solucao_embarcacao = SolucaoEmbarcacao(*_vessels)
        return solucao_embarcacao

    def get_solucao_embarcacao_enrocamento(self, filtered_vessels, vessels):
        """Cria uma Solução de Embarcação para subestação"""

        _vessels = []
        solucao_embarcacao = []

        count_fallpipe_vessel = 0

        for index, row in filtered_vessels["fallpipe_vessel"].iterrows():
            item_data = vessels["fallpipe_vessel"].loc[vessels["fallpipe_vessel"]["nome_embarcacao"]
                                                       == row["Embarcação"]]
            if not item_data.empty:
                count_fallpipe_vessel = count_fallpipe_vessel + 1
                class_fallpipe_vessel = self.get_fallpipe_vessel(
                    item_data, row, count_fallpipe_vessel)
                _vessels.append(class_fallpipe_vessel)

        solucao_embarcacao = SolucaoEmbarcacao(*_vessels)
        return solucao_embarcacao

    def get_barcaca(self, df_barcaca, df_custom, idx):
        # (velocidade [m/min], maxima_capacidade [t], maxima_altura [m], maximo_vento [m/s]
        guindaste = Guindaste(4.0,
                              float(
                                  df_barcaca['capacidade_guindaste_(t)'].iloc[0]),
                              float(
                                  df_barcaca['altura_max_gancho_(m)'].iloc[0]),
                              float(df_barcaca['vel_max_vento_(m/s)'].iloc[0]))
        configuracao = {
            "nome": 'Barcaca{}'.format(idx),  # [m]
            # [m2]
            "area_deck_livre": float(df_barcaca['area_deck_livre_(m2)'].iloc[0]),
            # [t/m2]
            "maxima_capacidade_carga_deck": float(df_barcaca['max_cap_carga_deck_(t/m2)'].iloc[0]),
            "taxa_diaria": df_custom["Taxa diária (US$)"],
            "taxa_mobilizacao": df_custom["Taxa de mobilização (US$)"],
            "velocidade_locomocao_carregado": df_custom["Velocidade carregado (kt)"],
            "velocidade_locomocao_vazio": df_custom["Velocidade vazio (kt)"],
            # limites operacionais
            "guindaste": guindaste
        }
        barcaca = Barcaca(**configuracao)
        barcaca.setPosicao((self.latitude, self.longitude))

        return barcaca

    def get_wtiv(self, df_wtiv, df_custom, idx):

        # (velocidade [m/min], maxima_capacidade [t], maxima_altura [m], maximo_vento [m/s]
        guindaste = Guindaste(4.0,  # TODO DANI
                              float(
                                  df_wtiv['capacidade_guindaste_(t)'].iloc[0]),
                              float(df_wtiv['altura_max_gancho_(m)'].iloc[0]),
                              float(df_wtiv['vel_max_vento_(m/s)'].iloc[0]))
        configuracao = {
            "nome": "WTIV{}".format(idx),
            # [m2]
            "area_deck_livre": float(df_wtiv['area_deck_livre_(m2)'].iloc[0]),
            # [t/m2]
            "maxima_capacidade_carga_deck": float(df_wtiv['max_cap_carga_deck_(t/m2)'].iloc[0]),
            "taxa_diaria": df_custom["Taxa diária (US$)"],
            "taxa_mobilizacao": df_custom["Taxa de mobilização (US$)"],
            "velocidade_locomocao_carregado": df_custom["Velocidade carregado (kt)"],
            "velocidade_locomocao_vazio": df_custom["Velocidade vazio (kt)"],
            # limites operacionais
            # [m]
            "maxima_altura_onda": float(df_wtiv['alt_max_onda_(m)'].iloc[0]),
            "guindaste": guindaste,
            # [m]
            "comprimento_perna_wtiv": float(df_wtiv['comprimento_perna_(m)'].iloc[0]),
            # [m]
            "profundidade_maxima_wtiv": float(df_wtiv['prof_max_(m)'].iloc[0]),
            # [m/min]
            "velocidade_abaixo_profundidade_wtiv": float(df_wtiv['vel_abaixo_prof_(m/min)'].iloc[0]),
            # [m/min]
            "velocidade_acima_profundidade_wtiv": float(df_wtiv['vel_acima_prof_(m/min)'].iloc[0]),
        }
        wtiv = Wtiv(**configuracao)
        wtiv.setPosicao((self.latitude, self.longitude))
        return wtiv

    def get_heavy_lift(self, df_heavy_lift, df_custom, idx):

        # (velocidade [m/min], maxima_capacidade [t], maxima_altura [m], maximo_vento [m/s]
        guindaste = Guindaste(4.0,  # TODO DANI
                              float(
                                  df_heavy_lift['capacidade_guindaste_(t)'].iloc[0]),
                              float(
                                  df_heavy_lift['altura_max_gancho_(m)'].iloc[0]),
                              float(df_heavy_lift['vel_max_vento_(m/s)'].iloc[0]))
        configuracao = {
            "nome": "HeavyLift{}".format(idx),
            # [m2]
            "area_deck_livre": float(df_heavy_lift['area_deck_livre_(m2)'].iloc[0]),
            # [t/m2]
            "maxima_capacidade_carga_deck": float(df_heavy_lift['max_cap_carga_deck_(t/m2)'].iloc[0]),
            "taxa_diaria": df_custom["Taxa diária (US$)"],
            "taxa_mobilizacao": df_custom["Taxa de mobilização (US$)"],
            "velocidade_locomocao_carregado": df_custom["Velocidade carregado (kt)"],
            "velocidade_locomocao_vazio": df_custom["Velocidade vazio (kt)"],
            # limites operacionais
            "guindaste": guindaste
        }
        heavy_lift = HeavyLift(**configuracao)
        heavy_lift.setPosicao((self.latitude, self.longitude))
        return heavy_lift

    def get_cable_vessel(self, df_cable_vessel, df_custom, idx):

        configuracao = {
            "nome": "CableVessel{}".format(idx),
            "area_deck_livre": 100000000,  # [m2] Está ignorando essa análise
            "maxima_capacidade_carga_deck": float(df_cable_vessel['max_cap_carrossel_(t)'].iloc[0]),
            "taxa_diaria": df_custom["Taxa diária (US$)"],
            "taxa_mobilizacao": df_custom["Taxa de mobilização (US$)"],
            "velocidade_locomocao_carregado": df_custom["Velocidade carregado (kt)"],
            "velocidade_locomocao_vazio": df_custom["Velocidade vazio (kt)"],
        }
        cable_vessel = CableVessel(**configuracao)
        cable_vessel.setPosicao((self.latitude, self.longitude))
        return cable_vessel

    def get_fallpipe_vessel(self, df_fallpipe_vessel, df_custom, idx):

        configuracao = {
            "nome": "FallpipeVessel{}".format(idx),
            "capacidade_max": float(df_fallpipe_vessel['capacidade_max_(m3)'].iloc[0]),
            "capacidade_instalacao": float(df_fallpipe_vessel['capacidade_instalacao_(t/h)'].iloc[0]),
            "taxa_diaria": df_custom["Taxa diária (US$)"],
            "taxa_mobilizacao": df_custom["Taxa de mobilização (US$)"],
            "velocidade_locomocao_carregado": df_custom["Velocidade carregado (kt)"],
            "velocidade_locomocao_vazio": df_custom["Velocidade vazio (kt)"],
            "tempo_tacar_pedra": None,
            "lista_tempo_deslocamento": None
        }
        fallpipe_vessel = Fallpipe(**configuracao)
        fallpipe_vessel.setPosicao((self.latitude, self.longitude))
        return fallpipe_vessel

    def get_rebocador(self, df_rebocador, df_custom, idx):

        # (velocidade [m/min], maxima_capacidade [t], maxima_altura [m], maximo_vento [m/s]
        configuracao = {
            "nome": "Rebocador{}".format(idx),
            "taxa_diaria": df_custom["Taxa diária (US$)"],
            "taxa_mobilizacao": df_custom["Taxa de mobilização (US$)"],
            "velocidade_locomocao_carregado": df_custom["Velocidade carregado (kt)"],
            "velocidade_locomocao_vazio": df_custom["Velocidade vazio (kt)"],
        }
        rebocador = Rebocador(
            configuracao["nome"], configuracao["velocidade_locomocao_carregado"], configuracao["velocidade_locomocao_vazio"], configuracao["taxa_diaria"], configuracao["taxa_mobilizacao"])

        return rebocador

    def get_cronograma(self, parque, data=None):
        if data == None:
            data = parque.getDataInicioInstalacao()
        cronograma = Cronograma(parque.getNome(), data)
        return cronograma
