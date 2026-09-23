import numpy as np


def resistanceAC(f, Dins, d_c, R0):
    """
    Calculate the resistance AC
    :param f: float - frequence in Hz
    :param d_c: é o diâmetro do condutor (mm)
    :param R0: é a resistência máxima DC do condutor de cobre na temperatura de 20oC (ohm/km)
    :return R: float - ohm/km
    """

    # Auxiliary variable
    alpha20 = 0.00393  # in IEC 60287-1-1 cooper, temperature coeficiente at 20 °
    thetaABB = 90  # ABB maximum temperature °C
    sAABB = Dins.copy()  # Conductor diameter over insulation in mm
    k_s = 1  # k_s value for copper round, stranded, extruded - from Table 2 of IEC 60287-1-1
    k_p = 1  # k_p value for copper round, stranded, extruded - from Table 2 of IEC 60287-1-1

    # Adjust the resistance value to the maximum operative temperature
    # R1 = resistance DC at max temperature in ohm/m
    R1 = R0 * (1 + alpha20 * (thetaABB - 20))/1e3

    # Define the skin factor value ys based on IEC 60287-1-1
    x_s_2 = ((8 * np.pi * f) / R1) * (10**(-7)) * k_s
    x_s = np.sqrt(x_s_2)

    if (0 < x_s <= 2.8):
        y_s = (x_s_2**2) / (192 + (0.8 * (x_s_2**2)))
    elif (2.8 < x_s <= 3.8):
        y_s = -0.136 - (0.0177*x_s) + (0.0563*x_s_2)
    elif (x_s >= 3.8):
        y_s = (0.354*x_s) - 0.733

    # Define the proximity factor value yp based on IEC 60287-1-1
    x_p_2 = ((8 * np.pi * f)/R1) * (10**(-7)) * k_p

    Ayp = (x_p_2**2) / (192 + (0.8 * (x_p_2**2)))
    Byp = (d_c / sAABB)**2
    Cyp = 0.312 * Byp
    y_p = Ayp * Byp * (Cyp + (1.18 / (Ayp + 0.27)))

    # Define the AC resistance for pipe-type cables
    R = R1 * (1+1.5*(y_s+y_p)) * 1e3  # R = Resistance AC in ohm/km

    return R


def getAABBstep1(S, U, Irated, df):
    """
    Get current rating and section area from AABB guide, calculate quantity of cables
    :param S: float - power of cable in MVA
    :param U: float - voltage rating of circuit in kV
    :return Ir, section, Ncb: - A, mm2, integer
    """
    I = (1000 * S)/(U*np.sqrt(3))  # A

    # Current rating for three-core submarine cables with steel wire armour
    # AABB Table 33
    # 10-90 kV XLPE 3-core cables
    # Copeer conductor
    # Table 34
    # 100-300 kV XLPE 3-core cables

    sectionMatrix = df.to_numpy()
    U_available = np.unique(sectionMatrix[:, 0])
    U_select = U_available[U_available >= U]
    if U_select.any():
        Uselect_min = np.min(U_select)
        Uselect = sectionMatrix[sectionMatrix[:, 0] == Uselect_min]
    else:
        raise Exception(
            f"Não existe cabo AC cadastrado para o nível de tensão especificado de {U} kV para o sistema de exportação. Verifique o cadastro ou altere o nível de tensão.")

    Iselect = Uselect[Uselect[:, 6] > I]

    if Iselect.any():
        Ir, section = Iselect[0, 6], Iselect[0, 1]
        Ncb = 1
    else:
        Ncb = 100
        for i in range(len(Uselect)):
            Ir, section = Uselect[-(i+1), 6], Uselect[-(i+1), 1]
            Ncb_new = np.ceil(I/Ir)
            if Ncb_new <= Ncb:
                Ncb = Ncb_new
            else:
                Ir, section = Uselect[-i, 6], Uselect[-i, 1]
                break

    Imax = Ncb * Ir * Irated / I
    Sr = Ir * U * np.sqrt(3) / 1e3

    return I, Ir, Sr, section, Ncb, Imax


def getAABBstep2(U, section, df):
    """
    Get current rating and section area from AABB guide, calculate quantity of cables
    :param S: float - power of cable in MVA
    :param U: float - voltage rating of circuit in kV
    :return Ir, section, Ncb: - A, mm2, integer
    """

    parametersMatrix = df.to_numpy()
    Uselect = parametersMatrix[parametersMatrix[:, 0] == U]
    if not Uselect.any():
        Uselect = parametersMatrix[parametersMatrix[:, 0] > U]
        if not Uselect.any():
            raise Exception(
                f"Não existe parâmetros de cabo cadastrado para o nível de tensão especificado de {U} kV. Verifique o cadastro.")

    Sselect = Uselect[Uselect[:, 1] == section]

    if Sselect.any():
        w, C, L, Dins, d, d_c, R0 = Sselect[0, 2], Sselect[0, 3], Sselect[0,
                                                                          4], Sselect[0, 5], Sselect[0, 7], Sselect[0, 8], Sselect[0, 9]
    else:
        raise Exception(
            f"Não existe parâmetros de cabo cadastrado para a bitola especificada de {section} mm2. Verifique o cadastro.")

    return w, C, L, Dins, d, d_c, R0
