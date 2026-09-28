"""
Created on Thu Mar 30 14:33:56 2023
Funções para calcular o coeficiente de potência (cp_f); calcular a curva
(power_curve_generator);
e plotar a curva (plot_power_curve)

"""
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd


def cp_f(v_r_max, v_r_min, V_ws, D_rotor):
    """_summary_ Calcula o coeficiente de potência

    Args:
        v_r_max (_type_): _description_
        v_r_min (_type_): _description_
        V_ws (_type_): _description_
        D_rotor (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        # 2.coeficiente potencia
        # 2.1 COEFICIENTE DE ÂNCGULO DE PASSO DA PÁ (beta)
        beta = 0.0  # [-]

        # 2.2 COEFICIENTE DA RELAÇÃO TIP-SPEED (lambda)
        # 2.2.1 RELAÇÃO TIP-SPEED OTIMIZADA
        # Coefficients parameterisation of C_p - Table A.2 - pg27
        c_1 = 0.22  # [-]
        c_2 = 120.0  # [-]
        c_3 = 0.4  # [-]
        c_4 = 0.0  # [-]
        c_5 = 0.0  # [-]
        c_6 = 5.0  # [-]
        c_7 = 12.5  # [-]
        c_8 = 0.0  # [-]
        c_9 = 0.08  # [-]
        c_10 = 0.035  # [-]
        x = 0.0  # [-]

        omega_max = v_r_max * (
            2 * np.pi / 60
        )  # [rad/s]  - Velocidade de rotação máxima
        omega_min = v_r_min * (
            2 * np.pi / 60
        )  # [rad/s]  - Velocidade de rotação mínima

        # 2.3. COEFICIENTE DE POTÊNCIA
        def lambda_i(lambda_):  # Cálculo do lambda_i
            return 1.0 / ((1.0 / lambda_) - c_10)

        def C_p(lambda_i, lambda_):  # Cálculo do C_p
            return (
                c_1
                * (
                    c_2 / lambda_i
                    - c_3 * beta
                    - c_4 * lambda_i * beta
                    - c_5 * beta ** (1.0)
                    - c_6
                )
                * np.e ** (-c_7 / lambda_i)
                + c_8 * lambda_
            )

        def g(
            lambda_i,
        ):  # CALCULO DO lambda_i_opt PELA EQUAÇÃO Cp UTILIZANDO C_p_max
            return (
                c_1 * (c_2 / lambda_i - c_6) * np.e ** (-c_7 / lambda_i)
                - C_p_max
            )

        ### FUNÇÃO: lambda_opt = argmaxC_p(lambda, beta)###
        Cp_i = []  # LISTA VAZIA DE Cp_i
        ws = np.arange(
            0, 30, 0.01
        )  # SEQUÊNCIA DE PONTOS PARA VELOCIDADE DE VENTO ws
        for n in ws:  # PREENCHIMENTO DE Cp_i COM VALORES DE cp
            if n == 0:
                cp = 0
            else:
                cp = c_1 * (c_2 / n - c_6) * np.e ** (-c_7 / n)
            Cp_i.append(cp)

        C_p_max = 0.0  # DETERMINAÇÃO DO PONTO MÁXIMO NA CURVA DE C_p_max
        for num in Cp_i:
            if C_p_max is None or num > C_p_max:
                C_p_max = num

        lambda_i_opt = fsolve(g, 0.05)
        lambda_opt = 1 / (lambda_i_opt ** (-1) + c_10)  # CÁLCULO DO lambda_opt

        # VELOCIDADE DE ROTAÇÃO DA PÁ:
        # omega = min(omega_max,max(omega_min,omega_opt))
        omega_opt = lambda_opt[0] * V_ws * 2 / D_rotor  # Calculo do omega_opt
        omega = min(omega_max, max(omega_min, omega_opt))  # Escolha do omega

        # RELAÇÃO TIP-SPEED: lambda_
        lambda_ = omega * D_rotor / (2 * V_ws)  # Cálculo do lambda
        lambda_i2 = lambda_i(lambda_)
        c_p = C_p(lambda_i2, lambda_)
        return c_p
    except Exception as ex:
        raise ex
        # print(f"Erro: {ex}")
        # QMessageBox.warning(None, "Erro", "Erro no cp_f")


def cp_f_temp(v_r_max, v_r_min, V_ws, D_rotor):
    """_summary_ Calcula o coeficiente de potência

    Args:
        v_r_max (_type_): _description_
        v_r_min (_type_): _description_
        V_ws (_type_): _description_
        D_rotor (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        # COEFICIENTE DE POTÊNCIA
        # COEFICIENTE DE ÂNCGULO DE PASSO DA PÁ (beta)
        beta = 0.0  # [-]
        # COEFICIENTE DA RELAÇÃO TIP-SPEED (lambda)
        # RELAÇÃO TIP-SPEED OTIMIZADA
        # Coefficients parameterisation of C_p - Table A.2 - pg27
        c_1 = 0.22  # [-]
        c_2 = 120.0  # [-]
        c_3 = 0.4  # [-]
        c_4 = .0  # [-]
        c_5 = .0  # [-]
        c_6 = 5.0  # [-]
        c_7 = 12.5  # [-]
        c_8 = .0  # [-]
        c_9 = .08  # [-]
        c_10 = .035  # [-]
        x = .0  # [-]

        ### FUNÇÃO: lambda_opt = argmaxC_p(lambda, beta) ###
        Cp_i = []                                    # LISTA VAZIA DE Cp_i
        # SEQUÊNCIA DE PONTOS PARA VELOCIDADE DE VENTO ws
        ws = np.arange(0, 35, 0.01)
        for n in ws:                                 # PREENCHIMENTO DE Cp_i COM VALORES DE cp
            if n == 0.00:
                cp_valor = 0
                Cp_i.append(cp_valor)
            else:
                cp_valor = c_1*(c_2/n - c_6)*np.e**(-c_7/n)
                Cp_i.append(cp_valor)

        # DETERMINAÇÃO DO PONTO MÁXIMO NA CURVA DE C_p_max
        C_p_max = 0.0
        for num in Cp_i:
            if (C_p_max is None or num > C_p_max):
                C_p_max = num

        # CALCULO DO lambda_i_opt PELA EQUAÇÃO Cp UTILIZANDO C_p_max
        def g(lambda_i):
            return c_1*(c_2/lambda_i - c_6)*np.e**(-c_7/lambda_i) - C_p_max

        lambda_i_opt = fsolve(g, 0.05)

        lambda_opt = 1/(lambda_i_opt**(-1) + c_10)   # CÁLCULO DO lambda_opt

        ### VELOCIDADE DE ROTAÇÃO DA PÁ: omega = min(omega_max,max(omega_min,omega_opt)) ###
        omega_opt = lambda_opt[0]*V_ws*2/D_rotor     # Calculo do omega_opt

        omega = min(v_r_max, max(v_r_min, omega_opt))   # Escolha do omega

        ### RELAÇÃO TIP-SPEED: lambda_ ###
        lambda_ = omega*D_rotor/(2*V_ws)             # Cálculo do lambda

        # COEFICIENTE DE POTÊNCIA
        def lambda_i(lambda_):                       # Cálculo do lambda_i
            return 1.0/((1.0/lambda_) - c_10)
        lambda_i = lambda_i(lambda_)

        def C_p(lambda_i, lambda_):                  # Cálculo do C_p
            return c_1*(c_2/lambda_i - c_3*beta - c_4*lambda_i*beta - c_5*beta**(1.0) - c_6)*np.e**(-c_7/lambda_i) + c_8*lambda_

        C_p = C_p(lambda_i, lambda_)

        return C_p

    except Exception as ex:
        raise ex
        # print(f"Erro: {ex}")
        # QMessageBox.warning(None, "Erro", "Erro no cp_f")

# 3. Model to generate power curve from nominale power and rotor dimension
# Fonction générant la power curve


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
    try:
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

        # pd.set_option('display.max_rows', None)
        # print(df_bpc)

        if normalized:
            df_bpc = df_bpc / (P * 1e-3)

        return df_bpc

    except Exception as ex:
        raise ex


# 5. VISUALIZAÇÃO DA CURVA DE POTÊNCIA COM EFEITOS ADVERSOS
def plot_power_curve(p_with_ti):
    """_summary_ Plotar curva de potência

    Args:
        p_with_ti (_type_): _description_
    """

    plt.style.use("ggplot")
    # %matplotlib inline
    fig, ax = plt.subplots(figsize=(18, 9))
    p_with_ti.plot(ax=ax)
    plt.grid(color="black")
    ax.set_facecolor("white")
    plt.title("Modelo da curva de potência")
    plt.ylabel("Potência (kW)")
    plt.xlabel("Velocidade do vento (m/s)")
    plt.show()
