import pandas as pd
import numpy as np
from py_wake.wind_turbines.generic_wind_turbines import GenericTIRhoWindTurbine
from py_wake.site.xrsite import XRSite
from Wind_Turbines.CAFCS import cafc

def FactorCapacity():

    """
    Calcular o Fator de capacidade
    """
    df_len = len(df.iloc[0]["power_curve_ti"])
    vels = [v / 10 for v in range(df_len)]

    for index, row in self.df.iterrows():
        fc_sum = 0
        for i, value in enumerate(vels):
            if i == 0:
                dp = 1 - np.exp(-((vels[i] / row["c"]) ** row["k"]))
            else:
                dp = (
                    1 - np.exp(-((vels[i] / row["c"]) ** row["k"]))
                ) - (1 - np.exp(-((vels[i - 1] / row["c"]) ** row["k"])))

                fc = dp * row["power_curve_ti"].iloc[i]
                fc_sum = fc_sum + fc

            df.at[index, "fc_tot"] = fc_sum / row["p_nom_kw"]

        # 9) Obtenção do Fator de Capacidade pelo Coeficiente de Ajuste do Fator de Capacidade:
        k = df.iloc[0, self.df.columns.get_loc("k")]
        c = df.iloc[0, self.df.columns.get_loc("c")]
        # o ccafc é calculado somente para 15 graus e com 6 distâncias

        ccafcs, distancias, afastamentos = cafc(k, c)

    return distancias
