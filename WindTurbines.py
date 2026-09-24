import pandas as pd
import numpy as np
from py_wake.wind_turbines.generic_wind_turbines import GenericTIRhoWindTurbine
from py_wake.site.xrsite import XRSite


def sel_class_wind(v_ref):
        """Seleciona as classes de vento permitidas conforme o valor da
        velocidade de referencia do parque eólico

        :param v_ref - velocidade referência ajustada calculada com dados de
        vento do parque
        :return: Retorna as classes de vento
        """
        class_wind = []
        if v_ref > 50:
            class_wind = ["IEC S"]
        elif 50 >= v_ref > 42.5:
            class_wind = ["IEC S", "I"]
        elif 42.5 >= v_ref > 37.5:
            class_wind = ["IEC S", "I", "II"]
        elif v_ref <= 37.5:
            class_wind = ["IEC S", "I", "II", "III"]
        return class_wind

def power_curve_generator(
    potencia_nominal, R_rotor, TI, cut_in, cut_off, Cp, normalized=False
):
    """This function generate wind turbine power curve from nominal
    power and rotor dimension and turbulence intensity used to smooth the
    power curve (10% by default).
    List of parameters : P (rated power) expressed in kW, d (rotor diameter)
    expressed in m. Cut-in wind speed and cut-out wind speed can be adjusted,
    by default values are 3.5 m/s and 25 m/s. Cp value is set at 0.44
    corresponding to the mean value of a set of wind turbine model.

    Args:
        potencia_nominal (_type_): _description_
        R_rotor (_type_): _description_
        TI (_type_): _description_
        cut_in (_type_): _description_
        cut_off (_type_): _description_
        Cp (_type_): _description_
        normalized (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_ df_bpc['p_with_ti'] = Curva de potência com
        turbulência calculada
    """
 
    # Convertion from kW to W
    P = potencia_nominal * 1e3

    # Physical parameters
    rho = 1.225  # kg/m3, air density, could be calculated based on
    # temperature and altitude
    S = np.pi * (R_rotor) ** 2  # m², rotor area

    # Calculation parameters
    a = 5  # m/s, Truncature width of the Gaussian filter for turbulence
    # intensity
    speed_step = 0.1  # Step for wind power curve

    # Power calculation (P proportional to wind_speed^3)
    df_bpc = pd.DataFrame(
        index=np.arange(0, 40 + speed_step, speed_step),
        columns=["wind_speed"],
        )
    df_bpc["wind_speed"] = df_bpc.index
    df_bpc["p"] = 1 / 2 * rho * S * Cp * df_bpc.wind_speed**3
    # Saturation of the power output to the nominal value
    # Condição para função df_bpc['P'] calculada até P do modelo
    df_bpc.loc[df_bpc["p"] > P, "p"] = P
    # do aerogerador
    # Gaussian filter over w*(1-TI):w*(1+TI), TI being the turbulence
    # intensity
    df_bpc["p_with_ti"] = np.nan

    df_bpc.iloc[
        :: int(1 / speed_step), df_bpc.columns.get_loc("p_with_ti")
        ] = [
        df_bpc["p"]
        .rolling(
            window=int(a * TI * w / speed_step),
            win_type="gaussian",
            center=True,
            )
        .mean(std=int(TI * w / speed_step))
        .loc[w]
        for w in np.arange(0, 41)
        ]

    col_interpolated = df_bpc["p_with_ti"].interpolate(method="cubic")
    df_bpc["p_with_ti"] = col_interpolated
    df_bpc.loc[df_bpc["p_with_ti"] < 0, "p_with_ti"] = 0
    df_bpc.loc[df_bpc["wind_speed"] < (
    1 - 2 * TI) * cut_in, "p_with_ti"] = 0

    # Cut-in wind speed and cutout wind speed
    # Zera velocidades menores que cut_in
    df_bpc.loc[df_bpc["wind_speed"] < cut_in, "p"] = 0
    # Zera maiores que cut_off
    df_bpc.loc[df_bpc["wind_speed"] > cut_off, "p"] = 0
    # Zera maiores que cut_off
    df_bpc.loc[df_bpc["wind_speed"] > cut_off, "p_with_ti"] = 0

    del df_bpc["wind_speed"]
    df_bpc["p"] = df_bpc["p"] / 1e3
    df_bpc["p_with_ti"] = df_bpc["p_with_ti"] / 1e3
    df_bpc = df_bpc.replace(np.nan, 0)
    df_bpc.index.name = "Velocidade do vento"

    if normalized:
        df_bpc = df_bpc / (P * 1e-3)

    return df_bpc

def SpreadWindTurbines():
    pass