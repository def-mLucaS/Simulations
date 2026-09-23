import numpy as np
import pandas as pd
from .lineModelsHVAC import getAABBstep1, getAABBstep2


def lineParameters(R, L, C, omega, Zbase, Ybase, NcbAC):
    """
    Calculate the impedance and the admittance of conductor in per unit length
    :param R: float - resistance in ohm/km
    :param L: float - inductance in mH/km
    :param C: float - capacitance in microF/km
    :param omega: float - Angular frequency in rad/s
    :param Zbase, Ybase: float - base impedance and admitance to calculate the per unit parameters, in ohm and siemens
    :param NcbAC: integer - quantity of cables AC to calculate the paralel circuit
    :return Z and Y: float - the impedance and the admittance of conductor in per unit length
    """
    Z = R + (omega * L * 1e-3) * 1j
    Y = 0 + (omega * C * 1e-6) * 1j
    Z = Z/Zbase
    Y = Y/Ybase
    Z = Z/NcbAC
    Y = NcbAC*Y

    return Z, Y


def characteristicLine(Z, Y, l):
    """
    Calculate the characteristic impedance and the characteristic angle
    :param Z: float - impedance in per unit length
    :param Y: float - admittance in per unit length
    :param l: float - length in km
    :return Zc and theta: float - the characteristic impedance and the characteristic angle in per unit
    """
    Zc = np.sqrt(Z/Y)
    theta = l * np.sqrt(Z*Y)

    return Zc, theta


def piLine(Zc, theta):
    """
    Calculate the impedance and the admittance of pi model
    :param Zc: float - characteristic impedance in per unit
    :param theta: characteristic angle in rad
    :return Zpi and Ypi: float - the impedance and the admittance pi model
    """
    Zpi = Zc * np.sinh(theta)
    Ypi = np.tanh(theta/2) / Zc

    return Zpi, Ypi


def impedanceTrafoParameters(PlossCu, Urtr, Srtr, uk):
    """
    Calculate the resistance and the indutive reatance 
    :param PlossCu: float - copper losses in kW
    :param Urtr: float - rated voltage of the transformer at the transmission system side in kV
    :param Srtr:  float - rated power of the transformer in MVA
    :param uk:  float -  short circuit voltage in per unit
    :return Rtr and Xtr: float - resistance and inductive impedance, in ohm
    """
    Rtr = PlossCu * 1e3 * ((Urtr / (Srtr * 1e3))**2)
    Xtr = np.sqrt((uk*(((Urtr)**2) / Srtr))**2 - (Rtr**2))

    return Rtr, Xtr


def admitanceTrafoParameters(PlossFe, Urtr, Srtr, io):
    """
    Calculate the Conductance and the susceptance
    :param PlossFe: float - iron losses in MW
    :param Urtr: float - rated voltage of the transformer at the transmission system side in kV
    :param Srtr:  float - rated power of the transformer in MVA
    :param io:  float - open circuit current in per unit
    :return Gtr and Btr: float - Conductance and susceptance, in siemens
    """
    Gtr = PlossFe / ((Urtr**2)*1e3)
    Btr = io * (Srtr / (Urtr**2))

    return Gtr, Btr


def trafoParameters(Rtr, Xtr, Gtr, Btr, Ntr, Zbase, Ybase):
    """
    Calculate the impedance and the admittance of transformer in per unit
    :param Rtr: float - resistance of transformer in ohm
    :param Xtr: float - inductance of transformer in ohm
    :param Gtr: float - conductance of transformer in siemens
    :param Btr: float - susceptance of transformer in siemens
    :param Ntr: int - number of transformer in parallel
    :param Zbase, Ybase: float - base impedance and admitance to calculate the per unit parameters, in ohm and siemens
    :return Ztr and Ytr: float - the impedance and the admittance of transformer in per unit
    """
    Ztr = Rtr + Xtr * 1j
    Ytr = Gtr - Btr * 1j
    Ztr = Ztr/(Ntr*Zbase)
    Ytr = (Ytr*Ntr)/Ybase

    return Ztr, Ytr


def gridParameters(SCR, Xg_Rg, SowfN_pu, Ug):
    """
    Calculate the equivalent Thevenin impedance of the grid
    :param SCR: int - short circuit ratio
    :param Xg_Rg: int - X/R ratio
    :param SowfN_pu: float - OWPP aparent power in pu
    :param Ug: complex - Equivalent Thevenin voltage of the grid
    :return Zg: complex - the equivalent Thevenin impedance of the grid in pu
    """
    Ssc = SCR * SowfN_pu
    Zmod = (np.abs(Ug)**2)/Ssc
    theta = np.arctan(Xg_Rg)
    Rg = Zmod * np.cos(theta)
    Xg = Zmod * np.sin(theta)
    Zg = Rg + Xg * 1j

    return Zg


def powerFlow(Ug, Zg, PowfN_pu, QowfN_pu, Ztr, Ytr, Yl1, Yl2, Yl3, Yl4, Yl5, Zpi1, Ypi1, Zpi2, Ypi2):
    """
    Calculate power flow by forward backward sweep
    :param Ug: Equivalent thevenin reference voltage of onshore grid 
    :param Zg: Equivalent thevenin impedance of onshore grid
    :param PowfN_pu: active power coming from the OWPP in pu
    :param QowfN_pu: reactive power coming from the OWPP in pu
    :param Ztr: complex - impedance of transformer in pu
    :param Ytr: complex - admitance of transformer in pu
    :param Yl1, Yl2, Yl3, Yl4, Yl5: complex - admitance of reactors in pu
    :param Zpi1 and Zpi2: complex - impedance of line in pi model before and after mid-cable in pu
    :param Ypi1 and Ypi2: complex - admitance of line in pi model in pu    
    :return flag_conv, U5, Ig: powerflow result flag, voltage and current at PCC
    """
    # Initial conditions
    SowfN = PowfN_pu + QowfN_pu * 1j
    tol, niter, itermax, U1, U2, U3, U4, U5, I1, I2, I3, I4, I5, Ig = 1e-6, 0, 500, Ug, Ug, Ug, Ug, Ug, 0, 0, 0, 0, 0, 0
    Uold = np.array([U1, U2, U3, U4, U5, Ug], dtype=complex)
    norminf = np.abs(Ug)/np.abs(Ug)

    while (norminf > tol) and (niter < itermax):
        # backward sweep procces
        I1 = np.conj(SowfN/U1)
        I2 = I1 - (Ytr + Yl1) * U1
        I3 = I2 - (Ypi1 + Yl2) * U2
        I4 = I3 - (Ypi1 + Yl3 + Ypi2) * U3
        I5 = I4 - (Ypi2 + Yl4) * U4
        Ig = I5 - (Ytr + Yl5) * U5
        # forward sweep procces
        U5 = Ug + Zg * Ig
        U4 = U5 + Ztr * I5
        U3 = U4 + Zpi2 * I4
        U2 = U3 + Zpi1 * I3
        U1 = U2 + Ztr * I2

        Unew = np.array([U1, U2, U3, U4, U5, Ug], dtype=complex)

        Inew = np.array([I1, I2, I3, I4, I5, Ig], dtype=complex)

        error = Unew - Uold

        norminf = np.linalg.norm(error, np.inf)

        Uold = Unew

        niter = niter + 1

    if norminf > tol or np.isnan(norminf) or np.isinf(norminf):
        # raise Exception(f"O fluxo de potência não convergiu considerando tolerância {tol} e {itermax} iterações máxima. Verifique os dados de entrada!")
        flag_conv = False
    else:
        flag_conv = True

    return flag_conv, Unew, Inew


def acLosses(Powf, U5, Ig, Sb):
    """
    Calculate AC active power losses 
    :param Powf: float - active power generated by the OWPP in pu
    :param U5: complex - voltage at PCC
    :param Ig: complex - grid current
    :param Sb: int - base power value in MVA
    :return PlossAC: float - AC power losses in MW
    """
    PlossAC = (Powf - np.real(U5 * np.conj(Ig))) * Sb

    return PlossAC


def lossesCost(Towf, Ce, PlossAC):
    """
    Calculate cost of AC power losses 
    :param Towf: integer - life time of the WOPP in years 
    :param Ce: float - cost of energy in u.m./MWh
    :param PlossAC: float - AC power losses in MW
    :return ClossAC: float - cost of AC power losses in u.m.ano
    """
    ClossAC = 8760 * Towf * Ce * PlossAC

    return ClossAC


def acCablesCost(A, B, C, D, E, Srcb, n, l):
    """
    Calculate cost of AC cables
    :param A, B, C, D, E: constants of Table I from Dakic et al. (2021)
    :param Srcb: float - rated apparent power of the cable in MVA
    :param N: integer - quantity of cables in paralel
    :param l: float - cable length in km
    :return CcbAC: float - cost of AC cables
    """
    x1 = np.exp(C * Srcb)
    x2 = B * 1e6 * x1
    x = (A * 1e6 + x2 + D)
    y = ((9*n)+1)
    z = (10*E)
    CcbAC = l * x * y / z

    return CcbAC


def switchgearsCost(UACN, nSub, nTrafos):
    """
    Calculate cost of switchgears
    :param UACN: float - nominal transmission voltage in kV
    :return CcbAC: float - cost of switchgears
    """
    CgisAC_unit = ((0.0117 * UACN) + 0.0231)
    CgisAC = CgisAC_unit*nSub*nTrafos

    return CgisAC_unit, CgisAC


def trafosCost(Srtr, nSub, nTrafos):
    """
    Calculate cost of transformers
    :param Srtr: float - rated power of the transformer in MVA
    :return Ctr: float - cost of transformers
    """
    Ctr_unit = (0.0427 * (Srtr**0.7513))
    Ctr = Ctr_unit*nSub*nTrafos
    return Ctr_unit, Ctr


def reactCost(Yl, Sb, K, P):
    """
    Calculate the reactive power compensated by the reactors and the cost of reactors
    :param U2: float - voltage at substation offshore
    :param Ka and P: float - the constant values defined in Table II
    :param Yl: admitance of reactors
    :return Creact: float - reactive power compensated by the reactors and cost of reactors
    """
    Ql = abs(Yl) * Sb
    Creact = (K * Ql) + P
    return Ql, Creact


def substationCost(PowfN):
    """
    Calculate cost of substation AC platform 
    :param PowfN: nominal power of the offshore wind power plant in MW
    :return CssAC: float - cost of substation AC platform
    """
    CssAC = 2.534 + (0.0887 * PowfN)

    return CssAC


def table1(VcbAC):  # From Dakic et al. (2021)
    """
    COEFFICIENTS FOR XLPE SUBMARINE AC CABLES 
    :param VcbAC: int - rated voltage of AC cable in kV
    :return A, B, C, D, E: float - coeficients
    """
    if VcbAC <= 30:
        A, B, C, D, E = 0.411, 0.596, 0.041, 170000, 8.98
    elif 30 < VcbAC <= 70:
        A, B, C, D, E = 0.688, 0.625, 0.0205, 170000, 8.98
    elif 70 < VcbAC <= 150:
        A, B, C, D, E = 1.971, 0.209, 0.0166, 170000, 8.98
    elif 150 < VcbAC <= 220:
        A, B, C, D, E = 3.181, 0.11, 0.0116, 170000, 8.98
    elif 220 < VcbAC <= 400:
        A, B, C, D, E = 5.8038, 0.044525, 0.0072, 170000, 8.98
    else:
        raise Exception(
            f"Não existem coeficientes de custo de cabos XLPE previstos para tensão de {VcbAC} kV. Verifique os dados de entrada.")
    return A, B, C, D, E


def table2(location):  # From Dakic et al. (2021)
    """
    COEFFICIENTS FOR reactor cost
    :param location: str - reactor placement
    :return K, P: float - coeficients
    """
    if location == "onshore":
        K, P = 0.01049, 0.8312
    elif location == "offshore":
        K, P = 0.01576, 1.244
    elif location == "middle":
        K, P = 0.01576, 12.44
    else:
        raise Exception(
            f"Não existem coeficientes de custo de reatores shunt previstos para localização {location}. Verifique os dados de entrada.")
    return K, P


def table4(Stra):  # From Dakic et al. (2021)
    """
    System parameters
    :param Stra: float - rated power of the transformer in MVA
    :return PlossCu: integer - Copper lossess in kW
    :return PlossFe: integer - Iron lossess in kW
    :return uk: float - Short circuit voltage in per unit
    :return io: float - Open circuit current in per unit
    """
    if Stra <= 1:
        return 6.75, 1.05, 0.06, 0.005  # transformador de distribuição
    elif 1 < Stra <= 10:
        return 56.2, 9.8, 0.08, 0.008
    elif 10 < Stra <= 100:
        return 66, 14, 0.1, 0.008
    elif 100 < Stra <= 350:
        return 165, 35, 0.125, 0.009
    elif 350 < Stra <= 600:
        return 260, 60, 0.15, 0.01
    else:
        return 400, 90, 0.18, 0.012


def cableExportAC(nclusters, exportpar, setupRes, cabosEXP):

    n_exportLines = nclusters

    [Y1, Y2, Y3, Y4, Y5, Closs, PowfN_pu, QowfN_pu, U, I, Yl] = setupRes

    Sbase = exportpar['PowfN'] / n_exportLines
    Ubase = exportpar['Urtr']

    l_total = 2 * exportpar['dr'] + \
        (exportpar['l_shore'] * (1+exportpar['exclusion']))

    # Sistema 3 - Cabeamento AC
    # *******************************************************************************

    if exportpar['flag_overload']:
        Irated = 1.1
    else:
        Irated = 1

    Itotal, Ir, Sr, section, NcbAC, Imax = getAABBstep1(
        Sbase, exportpar['Urtr'], Irated, cabosEXP)

    # equipement AC cost
    A, B, C, D, E = table1(exportpar['Urtr'])
    CcbAC = acCablesCost(A, B, C, D, E, Sr, NcbAC, l_total)

    # cost_parameter = 863/300 # valor em euros por metro por MVA (ENTSOE, 2012)
    # CcbAC = cost_parameter*Sbase*l_total*1000

    w, Cl, L, Dins, out_d, d_c, R0 = getAABBstep2(Ubase, section, cabosEXP)

    cable_type = 'AC XLPE three-core (ABB)'
    cable_conductor = 'copper'

    labels3 = ['Total Current', 'Cable Type', 'Conductor', 'Rated Voltage', 'Cross section', 'Outer Diameter',
               'Rated Current per Cable', 'Number of cables', 'Weight per cable', 'Length per cable', 'Cost', 'Losses Cost']
    series3 = [Itotal, cable_type, cable_conductor, exportpar['Urtr'], section, out_d, 
               Ir, NcbAC, w*l_total, l_total, CcbAC/(10**6), Closs]

    RESULT_System3 = pd.DataFrame({'Description': labels3})

    for i in range(nclusters):

        pd_right = pd.DataFrame({'Export Cable'+str(i+1): series3})

        RESULT_System3 = RESULT_System3.join(pd_right)

    RESULT_System3['Export Total'] = np.nan
    RESULT_System3.loc[10, 'Export Total'] = nclusters*CcbAC/(10**6)
    RESULT_System3.loc[11, 'Export Total'] = nclusters*Closs
    RESULT_System3['Units'] = ['A', cable_type, cable_conductor,
                               'kV', 'mm2', 'mm', 'A', 'un', 't', 'km', 'M USD', 'M USD']

    return RESULT_System3


def ossExportAC(nclusters, Uoff1, exportpar, setupRes):

    [Y1, Y2, Y3, Y4, Y5, Closs, PowfN_pu, QowfN_pu, U, I, Yl] = setupRes

    CgisAC_unit, CgisAC = switchgearsCost(
        exportpar['Urtr'], nclusters, exportpar['Ntr'])

    Sbase = exportpar['PowfN'] / nclusters
    Srtr = exportpar['RatioTR']*exportpar['PowfN']/(exportpar['Ntr']*nclusters)

    Ctr_unit, Ctr = trafosCost(Srtr, nclusters, exportpar['Ntr'])

    CssAC = substationCost(Sbase)

    Koff, Poff = table2('offshore')
    Kmid, Pmid = table2('middle')

    Qoff1, CreactOff1 = reactCost(Y1, Sbase, Koff, Poff)
    Qoff2, CreactOff2 = reactCost(Y2, Sbase, Koff, Poff)
    Qmid, CreactMid = reactCost(Y3, Sbase, Kmid, Pmid)

    Cancillary = 6  # costs ancillary systems, million dollars ORBIT
    # em toneladas ORBIT - valor similar ao calculado 4C
    topside_mass = (2.6492*Srtr*exportpar['Ntr']) + 1497.5

    # Dados vindos do 4C - aproximação linear
    topside_length = 0.0216*Srtr*exportpar['Ntr'] + 28.76
    topside_width = 0.0128*Srtr*exportpar['Ntr'] + 22.74
    topside_height = 0.0008*Srtr*exportpar['Ntr'] + 21.61

    topside_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        topside_length, topside_width, topside_height)

    switchgear_weight = 7.5  # 8dn9 Siemens Catalog GIS Switchgear 245kV
    # 8dn9 Siemens Catalog GIS Switchgear 245kV
    switchgear_dimensions = '5.1 x 1.5 x 3.7 per bay'

    trafo_weight = 0.5137*Srtr + 40     # Large Power transformers Study (DOE)
    trafo_width = 0.0106*Srtr + 3.41  # Large Power transformers Study (DOE)
    trafo_length = 0.0228*Srtr + 1
    trafo_height = 0.0163*Srtr + 2

    trafo_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        trafo_length, trafo_width, trafo_height)

    # Large Power transformers Study (DOE)
    reactor_off1_weight = 0.5137*Qoff1 + 40
    # Large Power transformers Study (DOE)
    reactor_off1_width = 0.0106*Qoff1 + 3.41
    reactor_off1_length = 0.0228*Qoff1 + 1
    reactor_off1_height = 0.0163*Qoff1 + 2

    reactor_off1_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        reactor_off1_length, reactor_off1_width, reactor_off1_height)

    # Large Power transformers Study (DOE)
    reactor_off2_weight = 0.5137*Qoff2 + 40
    # Large Power transformers Study (DOE)
    reactor_off2_width = 0.0106*Qoff2 + 3.41
    reactor_off2_length = 0.0228*Qoff2 + 1
    reactor_off2_height = 0.0163*Qoff2 + 2

    reactor_off2_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        reactor_off2_length, reactor_off2_width, reactor_off2_height)

    # Large Power transformers Study (DOE)
    reactor_mid_weight = 0.5137*Qmid + 40
    # Large Power transformers Study (DOE)
    reactor_mid_width = 0.0106*Qmid + 3.41
    reactor_mid_length = 0.0228*Qmid + 1
    reactor_mid_height = 0.0163*Qmid + 2

    reactor_mid_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        reactor_mid_length, reactor_mid_width, reactor_mid_height)

    labels2 = ['Type', 'Rated Power', 'Rated Voltage', 'Quantity', 'Unitary Cost',
               'Total Cost', 'Unitary Weight', 'Total Weight', 'Dimensions [LxWxH]']

    RESULT_System2 = pd.DataFrame({'Description': labels2})

    RESULT_System2['Transformer'] = ['Oil Insulated', Srtr, f"{Uoff1}/{exportpar['Urtr']}", nclusters *
                                     exportpar['Ntr'], Ctr_unit, Ctr, trafo_weight, trafo_weight*nclusters*exportpar['Ntr'], trafo_dim]
    RESULT_System2['Switchgear'] = ['SF6 Insulated', Srtr, exportpar['Urtr'], nclusters*exportpar['Ntr'],
                                    CgisAC_unit, CgisAC, switchgear_weight, switchgear_weight*nclusters*exportpar['Ntr'], switchgear_dimensions]
    if Y1 == 0:
        RESULT_System2['Reactor Inter-Array'] = np.nan
        RESULT_System2.loc[4, 'Reactor Inter-Array'] = 0
        RESULT_System2.loc[5, 'Reactor Inter-Array'] = 0
    else:
        RESULT_System2['Reactor Inter-Array'] = ['Oil Insulated', Qoff1, Uoff1, nclusters, CreactOff1,
                                                 CreactOff1*nclusters, reactor_off1_weight, reactor_off1_weight*nclusters, reactor_off1_dim]
    if Y2 == 0:
        RESULT_System2['Reactor Export Offshore'] = np.nan
        RESULT_System2.loc[4, 'Reactor Export Offshore'] = 0
        RESULT_System2.loc[5, 'Reactor Export Offshore'] = 0
    else:
        RESULT_System2['Reactor Export Offshore'] = ['Oil Insulated', Qoff2, exportpar['Urtr'], nclusters,
                                                     CreactOff2, CreactOff2*nclusters, reactor_off2_weight, reactor_off2_weight*nclusters, reactor_off2_dim]
    RESULT_System2['Ancillary Systems'] = [np.nan, Sbase, exportpar['Urtr'],
                                           nclusters, Cancillary, Cancillary*nclusters, np.nan, np.nan, np.nan]
    RESULT_System2['Topside Platform'] = [np.nan, Sbase, exportpar['Urtr'], nclusters,
                                          CssAC, CssAC*nclusters, topside_mass, topside_mass*nclusters, topside_dim]
    if Y3 == 0:
        RESULT_System2['Reactor Mid-Cable'] = np.nan
        RESULT_System2.loc[4, 'Reactor Mid-Cable'] = 0
        RESULT_System2.loc[5, 'Reactor Mid-Cable'] = 0
    else:
        RESULT_System2['Reactor Mid-Cable'] = ['Oil Insulated', Qmid, exportpar['Urtr'], nclusters,
                                               CreactMid, CreactMid*nclusters, reactor_mid_weight, reactor_mid_weight*nclusters, reactor_mid_dim]
        # RESULT_System2['Platform Mid-Cable']  = [np.nan,Qmid,exportpar['Urtr'],nclusters,CssAC_mid,CssAC_mid*nclusters,topside_mid_mass,topside_mid_mass*nclusters,topside_mid_dim]

    RESULT_System2['Units'] = ['-', 'MVA', 'kV',
                               'un', 'M USD', 'M USD', 't', 't', 'm']

    return RESULT_System2


def onExportAC(nclusters, Usin, exportpar, setupRes):

    [Y1, Y2, Y3, Y4, Y5, Closs, PowfN_pu, QowfN_pu, U, I, Yl] = setupRes

    CgisAC_unit, CgisAC = switchgearsCost(
        exportpar['Urtr'], nclusters, exportpar['Ntr'])

    Sbase = exportpar['PowfN'] / nclusters
    Srtr = exportpar['RatioTR']*exportpar['PowfN']/(exportpar['Ntr']*nclusters)

    Ctr_unit, Ctr = trafosCost(Srtr, nclusters, exportpar['Ntr'])

    Kon, Pon = table2('onshore')

    Qon1, CreactOn1 = reactCost(Y4, Sbase, Kon, Pon)
    Qon2, CreactOn2 = reactCost(Y5, Sbase, Kon, Pon)

    Cancillary = 6  # costs ancillary systems, million dollars ORBIT

    switchgear_weight = 7.5  # 8dn9 Siemens Catalog GIS Switchgear 245kV
    # 8dn9 Siemens Catalog GIS Switchgear 245kV
    switchgear_dimensions = '5.1 x 1.5 x 3.7 per bay'

    trafo_weight = 0.5137*Srtr + 40     # Large Power transformers Study (DOE)
    trafo_width = 0.0106*Srtr + 3.41  # Large Power transformers Study (DOE)
    trafo_length = 0.0228*Srtr + 1
    trafo_height = 0.0163*Srtr + 2

    trafo_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        trafo_length, trafo_width, trafo_height)

    # Large Power transformers Study (DOE)
    reactor_on1_weight = 0.5137*Qon1 + 40
    # Large Power transformers Study (DOE)
    reactor_on1_width = 0.0106*Qon1 + 3.41
    reactor_on1_length = 0.0228*Qon1 + 1
    reactor_on1_height = 0.0163*Qon1 + 2

    reactor_on1_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        reactor_on1_length, reactor_on1_width, reactor_on1_height)

    # Large Power transformers Study (DOE)
    reactor_on2_weight = 0.5137*Qon2 + 40
    # Large Power transformers Study (DOE)
    reactor_on2_width = 0.0106*Qon2 + 3.41
    reactor_on2_length = 0.0228*Qon2 + 1
    reactor_on2_height = 0.0163*Qon2 + 2

    reactor_on2_dim = "{:.1f} x {:.1f} x {:.1f}".format(
        reactor_on2_length, reactor_on2_width, reactor_on2_height)

    labels2 = ['Type', 'Rated Power', 'Rated Voltage', 'Quantity', 'Unitary Cost',
               'Total Cost', 'Unitary Weight', 'Total Weight', 'Dimensions']

    RESULT_System2 = pd.DataFrame({'Description': labels2})

    if exportpar['Urtr'] == Usin:
        RESULT_System2['Transformer'] = np.nan
        RESULT_System2.loc[4, 'Transformer'] = 0
        RESULT_System2.loc[5, 'Transformer'] = 0
    else:
        RESULT_System2['Transformer'] = ['Oil Insulated', Srtr, f"{exportpar['Urtr']}/{Usin}", nclusters *
                                         exportpar['Ntr'], Ctr_unit, Ctr, trafo_weight, trafo_weight*nclusters*exportpar['Ntr'], trafo_dim]
    RESULT_System2['Switchgear'] = ['SF6 Insulated', Srtr, exportpar['Urtr'], nclusters*exportpar['Ntr'],
                                    CgisAC_unit, CgisAC, switchgear_weight, switchgear_weight*nclusters*exportpar['Ntr'], switchgear_dimensions]
    RESULT_System2['Ancillary Systems'] = [np.nan, Sbase, exportpar['Urtr'],
                                           nclusters, Cancillary, Cancillary*nclusters, np.nan, np.nan, np.nan]
    if Y4 == 0:
        RESULT_System2['Reactor Export Onshore'] = np.nan
        RESULT_System2.loc[4, 'Reactor Export Onshore'] = 0
        RESULT_System2.loc[5, 'Reactor Export Onshore'] = 0
    else:
        RESULT_System2['Reactor Export Onshore'] = ['Oil Insulated', Qon1, exportpar['Urtr'], nclusters,
                                                    CreactOn1, CreactOn1*nclusters, reactor_on1_weight, reactor_on1_weight*nclusters, reactor_on1_dim]
    if Y5 == 0:
        RESULT_System2['Reactor SIN'] = np.nan
        RESULT_System2.loc[4, 'Reactor SIN'] = 0
        RESULT_System2.loc[5, 'Reactor SIN'] = 0
    else:
        RESULT_System2['Reactor SIN'] = ['Oil Insulated', Qon2, Usin, nclusters, CreactOn2,
                                         CreactOn2*nclusters, reactor_on2_weight, reactor_on2_weight*nclusters, reactor_on2_dim]

    RESULT_System2['Units'] = ['-', 'MVA', 'kV',
                               'un', 'M US$', 'M USD', 't', 't', 'm']

    return RESULT_System2
