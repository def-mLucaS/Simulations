import numpy as np
from .hvacModels import table1, table2, table4, getAABBstep1, getAABBstep2, lineParameters, impedanceTrafoParameters, trafoParameters, admitanceTrafoParameters, gridParameters, characteristicLine, piLine, powerFlow, acLosses, lossesCost, reactCost
from .lineModelsHVAC import resistanceAC
from .hvacOptimizationSLSQP import reactorPlacement as reactorPlacementSLSQP
from .hvacOptimizationTRUST import reactorPlacement as reactorPlacementTRUST, identify_x
from .generationModel import generationProfile
import warnings


def setupHVAC(exportPar, ratedPower, cabosEXP, cambio):

    flag_overload = exportPar['flag_overload']
    flag_method = exportPar['flag_method']  # Trust-region = 1 SLSQP = 2

    # Reactors combination to be evaluated
    # number of reactors to place. 0 - all combinations
    n_reac = exportPar['Nreact']
    flag_mid = exportPar['flag_midCable']
    flag_opt = exportPar['flag_combOpt']

    """
    MELHORES COMBINAÇÕES DE C0 A C30 ESCOLHIDAS COM BASE NOS ESTUDOS DE SENSIBILIDADE
    1 REATOR C2, C3 e C4
    2 REATORES C9 C10 C11 C12 e C13
    3 REATORES C16 C17 C21 C22 E C23
    4 REATORES C26 C27 C29
    5 REATORES C30
    """
    if n_reac == 0:
        if flag_mid:
            reac_comb = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1],
                                  [1, 1, 0, 0, 0], [1, 0, 1, 0, 0], [1, 0, 0, 1, 0], [
                                      1, 0, 0, 0, 1], [0, 1, 1, 0, 0],
                                  [0, 1, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 1, 1, 0], [
                                      0, 0, 1, 0, 1], [0, 0, 0, 1, 1],
                                  [1, 1, 1, 0, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [
                1, 0, 1, 1, 0], [1, 0, 1, 0, 1],
                [1, 0, 0, 1, 1], [0, 1, 1, 1, 0], [0, 1, 1, 0, 1], [
                    0, 1, 0, 1, 1], [0, 0, 1, 1, 1],
                [1, 1, 1, 1, 0], [1, 1, 1, 0, 1], [1, 1, 0, 1, 1], [
                    1, 0, 1, 1, 1], [0, 1, 1, 1, 1],
                [1, 1, 1, 1, 1]], dtype=bool)
        else:
            reac_comb = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 1, 0, 0, 0],
                                  [1, 0, 0, 1, 0], [1, 0, 0, 0, 1], [0, 1, 0, 1, 0], [
                                      0, 1, 0, 0, 1], [0, 0, 0, 1, 1],
                                  [1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [1, 0, 0, 1, 1], [0, 1, 0, 1, 1], [1, 1, 0, 1, 1]], dtype=bool)
    elif n_reac == 1:
        if flag_opt:
            if flag_mid:
                #                           C2               C3              C4
                reac_comb = np.array(
                    [[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype=bool)
            else:
                #                          C1                C3               C4
                reac_comb = np.array(
                    [[0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype=bool)
        else:
            if flag_mid:
                #                          C0                C1                C2               C3              C4
                reac_comb = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [
                                     0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype=bool)
            else:
                #                          C0                C1                C3               C4
                reac_comb = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [
                                     0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype=bool)
    elif n_reac == 2:
        if flag_opt:
            if flag_mid:
                #                            C9               C10              C11              C12             C13
                reac_comb = np.array([[0, 1, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1], [
                                     0, 0, 1, 1, 0], [0, 0, 1, 0, 1]], dtype=bool)
            else:
                #                            C8              C10              C11
                reac_comb = np.array(
                    [[1, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1]], dtype=bool)
        else:
            if flag_mid:
                #                          C5/C10           C6/C11           C7/C12         C8/C13             C9/C14
                reac_comb = np.array([[1, 1, 0, 0, 0], [1, 0, 1, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 1], [0, 1, 1, 0, 0],
                                      [0, 1, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 1, 1, 0], [0, 0, 1, 0, 1], [0, 0, 0, 1, 1]], dtype=bool)
            else:
                #                         C5/C10           C7/C11            C8/C14
                reac_comb = np.array([[1, 1, 0, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 1],
                                      [0, 1, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 0, 1, 1]], dtype=bool)
    elif n_reac == 3:
        if flag_opt:
            if flag_mid:
                #                           C16          C17                   C21             C22              C23
                reac_comb = np.array([[1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [0, 1, 1, 1, 0], [
                                     0, 1, 1, 0, 1], [0, 1, 0, 1, 1]], dtype=bool)
            else:
                #                          C16               C17              C20               C23
                reac_comb = np.array([[1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [
                                     1, 0, 0, 1, 1], [0, 1, 0, 1, 1]], dtype=bool)
        else:
            if flag_mid:
                #                          C15/C20         C16/C21          C17/C22          C18/C23          C19/C24
                reac_comb = np.array([[1, 1, 1, 0, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [1, 0, 1, 1, 0], [1, 0, 1, 0, 1],
                                      [1, 0, 0, 1, 1], [0, 1, 1, 1, 0], [0, 1, 1, 0, 1], [0, 1, 0, 1, 1], [0, 0, 1, 1, 1]], dtype=bool)
            else:
                #                          C16               C17              C20               C23
                reac_comb = np.array([[1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [
                                     1, 0, 0, 1, 1], [0, 1, 0, 1, 1]], dtype=bool)
    elif n_reac == 4:
        if flag_opt:
            if flag_mid:
                #                          C26               C27              C29
                reac_comb = np.array(
                    [[1, 1, 1, 0, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 1]], dtype=bool)
            else:
                #                           C27
                reac_comb = np.array([[1, 1, 0, 1, 1]], dtype=bool)
        else:
            if flag_mid:
                #                          C25               C26              C27               C28              C29
                reac_comb = np.array([[1, 1, 1, 1, 0], [1, 1, 1, 0, 1], [1, 1, 0, 1, 1], [
                                     1, 0, 1, 1, 1], [0, 1, 1, 1, 1]], dtype=bool)
            else:
                #                           C27
                reac_comb = np.array([[1, 1, 0, 1, 1]], dtype=bool)
    elif n_reac == 5:
        #                           C30
        reac_comb = np.array([[1, 1, 1, 1, 1]], dtype=bool)
        if not flag_mid:
            raise Exception(
                "A compensação reativa com 5 reatores requer a alocação de um reator no barramento no meio do cabo de exportação.")
    else:
        raise Exception(
            f"Quantidade de {n_reac} reatores informado está inválido. Escolha um valor entre 1 e 5.")

    n_comb = reac_comb.shape[0]

    # Offshore project definition
    Sproj = ratedPower  # OWPP nominal power [MVA]. Defined by the user
    # OWPP export system voltage [kV]. Defined by the user
    Urtr = exportPar['Urtr']
    # km # total export system length [km]. Defined by the user
    l = 2 * exportPar['dr'] + (exportPar['l_shore']
                               * (1+exportPar['exclusion']))
    f = exportPar['freq']  # nominal system frequency [Hz]. System default
    omega = 2*np.pi*f  # angular frquency [rad/s]

    # total trafo power/Sproj. Defined by the user
    RatioTR = exportPar['RatioTR']
    Ntr = exportPar['Ntr']  # transformers parallel. Defined by the user
    Stra = RatioTR * Sproj / Ntr  # transformer nominal power definition [MVA]

    # Offshore generation profile
    n_w, pw, PowfN, QowfN = generationProfile(Sproj, exportPar, 'AC')

    # System base definition
    Sbase = Sproj  # apparent power base
    Ubase = Urtr  # voltage base at export system
    Zbase = (Ubase**2)/Sbase  # impedance base
    Ybase = 1/Zbase  # admittance base
    PowfN_pu = PowfN/Sbase
    QowfN_pu = QowfN/Sbase

    # optimization variables definition
    wl = 5  # losses cost weight value. Defined by effort x impact matrix
    wr = 1  # reactor cost weight value. Defined by effort x impact matrix
    # maximum voltage magnitude of the buses [pu]. Defined by the user
    Vmax = exportPar['Vmax']
    # minimum voltage magnitude of the buses [pu]. Defined by the user
    Vmin = exportPar['Vmin']
    # maximum voltage angle of the buses [rad]. System default
    thetamax = np.pi
    # minimum voltage angle of the buses [rad]. System default
    thetamin = -np.pi
    # maximum power factor at the PAC expressed as tan(Q/P) [rad]. Defined by the user as power factor
    Tan_QPmax = np.tan(np.arccos(exportPar['FP_LT']))
    # minimum power factor at the PAC expressed as tan(Q/P) [rad]. Defined by the user as power factor
    Tan_QPmin = -np.tan(np.arccos(exportPar['FP_LT']))
    Ymax = 0  # maximum reactor value [pu]. System default
    Ymin = -10  # minimum reactor [pu]. System default

    if flag_overload:
        Irated = 1.1
    else:
        Irated = 1

    # Auxiliary data from Dakic et al. (2021)
    A, B, C, D, E = table1(Urtr)
    Koff, Poff = table2('offshore')
    Kmid, Pmid = table2('middle')
    Kon, Pon = table2('onshore')
    PlossCu, PlossFe, uk, io = table4(Stra)
    SCR, Xg_Rg, Towf, Ce = exportPar['SCR'], exportPar['Xg_Rg'], exportPar['Towf'], exportPar['Ce']/cambio

    # Export cable modeling
    # Define the nominal Section and number of parallel circuits
    I, Ir, Sr, section, NcbAC, Imax = getAABBstep1(
        Sproj, Urtr, Irated, cabosEXP)
    Imax = np.array([[Imax, Imax, Imax, Imax, Imax, Imax]])
    Imin = -Imax*0.9  # minimum line current [pu]. System default
    w, Cl, L, Dins, d, d_c, R0 = getAABBstep2(
        Urtr, section, cabosEXP)  # Retrieve the cable electrical data
    # Adjust the cable resistance
    R = resistanceAC(f, Dins, d_c, R0)
    # Define the equivalent regular cable impedance and admittance in pu
    Z, Y = lineParameters(R, L, Cl, omega, Zbase, Ybase, NcbAC)
    # Define the cable charecteristic impedance
    Zc, theta = characteristicLine(Z, Y, l/2)
    # Define the cable impedance and admittance for long-line modeling
    Zpi, Ypi = piLine(Zc, theta)

    # Transformer modeling
    # Define the transformer resistance and reactance in ohms
    Rtr, Xtr = impedanceTrafoParameters(PlossCu, Urtr, Stra, uk)
    # Define the transformer conductance and susceptance in siemens
    Gtr, Btr = admitanceTrafoParameters(PlossFe, Urtr, Stra, io)
    # Define the transformer impedance and admittance in pu
    Ztr, Ytr = trafoParameters(Rtr, Xtr, Gtr, Btr, Ntr, Zbase, Ybase)

    # Equivalent grid modeling (PAC)
    Ug = 1.0 * np.exp(0*1j)  # Grid Thevenin voltage in pu
    # Define the grid equivalent Thevenin impedance
    Zg = gridParameters(SCR, Xg_Rg, Sproj/Sbase, Ug)

    # Optimization auxiliary variables initialization
    Zpi1, Ypi1, Zpi2, Ypi2 = Zpi, Ypi, Zpi, Ypi
    Creac_max_vec = np.array([-(Koff * Ymin * Sbase) + Poff,
                              -(Koff * Ymin * Sbase) + Poff,
                              -(Kmid * Ymin * Sbase) + Pmid,
                              -(Kon * Ymin * Sbase) + Pon,
                              -(Kon * Ymin * Sbase) + Pon])
    result = np.empty(n_comb, dtype=object)
    xj_len = np.zeros(n_comb, dtype=int)
    flag_x0_success = np.zeros(n_comb, dtype=int)
    n_Y = np.count_nonzero(reac_comb == True, 1)
    ClossAC = np.zeros(n_w)
    of_result = np.zeros(n_comb)
    total_cost = np.zeros(n_comb)
    flag_placement = False
    flag_loss = False
    flag_pfInit = True

    # Creac_max = np.zeros(n_comb)

    # for comb in range(n_comb):
    #     comb_test = reac_comb[comb,0:]
    #     Creac_max[comb] = np.sum(Creac_max_vec[comb_test])

    # Creac_max = np.max(Creac_max)

    Creac_max = np.sum(Creac_max_vec)

   # Optimization loop for each reactor combination
    for comb in range(n_comb):
        comb_test = reac_comb[comb, 0:]
        flag_Y = np.zeros((n_w), dtype=bool)
        U_init = np.zeros((n_w, 6), dtype=complex)
        I_init = np.zeros((n_w, 6), dtype=complex)
        Y_init = np.zeros((n_w, len(comb_test)), dtype=complex)
        if flag_pfInit:
            flag_x0 = exportPar['flag_x0']
        # Creac_max = np.sum(Creac_max_vec[comb_test])

        # While loop to calculate the losses cost before reactor placement and define x0
        while not np.all(flag_Y == True) and flag_pfInit == True:
            if isinstance(PowfN_pu, np.ndarray):
                for n_Pg in range(n_w):
                    if not flag_Y[n_Pg]:
                        flag_conv, U, I = powerFlow(Ug, Zg, PowfN_pu[n_Pg], QowfN_pu[n_Pg], Ztr, Ytr, Y_init[n_Pg, 0],
                                                    Y_init[n_Pg, 1], Y_init[n_Pg, 2], Y_init[n_Pg, 3], Y_init[n_Pg, 4], Zpi1, Ypi1, Zpi2, Ypi2)
                        if not flag_conv:
                            if not flag_loss:
                                warnings.warn(
                                    "O fluxo de potência inicial não convergiu. Seguindo para otimização com normalização aproximada. Verifique os dados de entrada.")
                                flag_x0 = False
                                flag_pfInit = False
                                ClossAC[n_Pg] = lossesCost(
                                    Towf, Ce, PowfN_pu[n_Pg] * Sbase * pw[n_Pg] * 0.5)
                            else:
                                flag_x0 = False
                                break
                        else:
                            if not flag_loss:
                                PlossAC = acLosses(
                                    PowfN_pu[n_Pg], U[4], I[5], Sbase) * pw[n_Pg]
                                ClossAC[n_Pg] = lossesCost(Towf, Ce, PlossAC)
                            if flag_x0:
                                check_vmax = np.abs(U) <= Vmax
                                check_vmin = np.abs(U) >= Vmin
                                check_imax = np.abs(I) <= Imax
                                check_imin = np.abs(I) >= Imin
                                check_ymin = np.imag(Y_init) >= Ymin
                                if np.all(check_vmax == True) and np.all(check_vmin == True) and np.all(check_imax == True) and np.all(check_imin == True) and np.all(check_ymin == True):
                                    U_init[n_Pg, 0:] = U
                                    I_init[n_Pg, 0:] = I
                                    flag_Y[n_Pg] = True
                                else:
                                    if np.all(check_ymin == True):
                                        Y_init[n_Pg, comb_test] = Y_init[n_Pg,
                                                                         comb_test] - 0.01 * 1j
                                    else:
                                        flag_x0 = False
                                        break
                if not flag_loss:
                    Closs_max = np.sum(ClossAC)
                    flag_loss = True
                if not flag_x0:
                    break
            else:
                flag_conv, U, I = powerFlow(Ug, Zg, PowfN_pu, QowfN_pu, Ztr, Ytr,
                                            Y_init[0, 0], Y_init[0, 1], Y_init[0, 2], Y_init[0, 3], Y_init[0, 4], Zpi1, Ypi1, Zpi2, Ypi2)
                if not flag_conv:
                    if not flag_loss:
                        raise Exception(
                            "O fluxo de potência não convergiu. Verifique os dados de entrada.")
                    else:
                        flag_x0 = False
                else:
                    if not flag_loss:
                        PlossAC = acLosses(PowfN_pu, U[4], I[5], Sbase) * pw
                        Closs_max = lossesCost(Towf, Ce, PlossAC)
                        flag_loss = True
                    if flag_x0:
                        check_vmax = np.abs(U) <= Vmax
                        check_vmin = np.abs(U) >= Vmin
                        check_imax = np.abs(I) <= Imax
                        check_imin = np.abs(I) >= Imin
                        check_ymin = np.imag(Y_init) >= Ymin
                        if np.all(check_vmax == True) and np.all(check_vmin == True) and np.all(check_imax == True) and np.all(check_imin == True) and np.all(check_ymin == True):
                            U_init = U
                            I_init = I
                            flag_Y[0] = True
                        else:
                            if np.all(check_ymin == True):
                                Y_init[n_Pg, comb_test] = Y_init[n_Pg,
                                                                 comb_test] - 0.01 * 1j
                            else:
                                flag_x0 = False
                                break
                if not flag_x0:
                    break

        if flag_method == 1:  # Optimize with Trust-Const method
            result[comb], xj_len[comb], flag_x0_success[comb] = reactorPlacementTRUST(flag_x0, U_init, I_init, Y_init, Ug, Zg, PowfN_pu, QowfN_pu, Ztr, Ytr, Zpi1, Ypi1, Zpi2, Ypi2, Sbase,
                                                                                      Towf, Ce, Koff, Poff, Kmid, Pmid, Kon, Pon, Vmax, Vmin, thetamax, thetamin,
                                                                                      Imax, Imin, Tan_QPmax, Tan_QPmin, Ymax, Ymin, pw, comb_test, Closs_max, Creac_max, n_w, n_Y[comb], wl, wr)
        elif flag_method == 2:  # Optimize with SLSQP method
            result[comb], xj_len[comb], flag_x0_success[comb] = reactorPlacementSLSQP(flag_x0, U_init, I_init, Y_init, Ug, Zg, PowfN_pu, QowfN_pu, Ztr, Ytr, Zpi1, Ypi1, Zpi2, Ypi2, Sbase,
                                                                                      Towf, Ce, Koff, Poff, Kmid, Pmid, Kon, Pon, Vmax, Vmin, thetamax, thetamin,
                                                                                      Imax, Imin, Tan_QPmax, Tan_QPmin, Ymax, Ymin, pw, comb_test, Closs_max, Creac_max, n_w, n_Y[comb], wl, wr)
        if result[comb].success:  # Check the optimization convergence
            of_result[comb] = result[comb].fun
            flag_placement = True

            Umod, Utheta, Imod, Itheta, Yl_x, Yreac_x = identify_x(
                result[comb].x, n_w, xj_len[comb], n_Y[comb])
            U = Umod * np.exp(Utheta * 1j)
            I = Imod * np.exp(Itheta * 1j)

            U5 = U[0:, 4]
            Ig = I[0:, 5]
            PlossAC = np.sum(acLosses(PowfN_pu, U5, Ig, Sbase) * pw)
            ClossAC = lossesCost(Towf, Ce, PlossAC) / 1e6

            Yreac = np.zeros(len(reac_comb[comb]))
            Yreac[reac_comb[comb]] = Yreac_x

            if Yreac[0] != 0:
                Creact1 = -(Koff * Yreac[0] * Sbase) + Poff
            else:
                Creact1 = 0
            if Yreac[1] != 0:
                Creact2 = -(Koff * Yreac[1] * Sbase) + Poff
            else:
                Creact2 = 0
            if Yreac[2] != 0:
                Creact3 = -(Kmid * Yreac[2] * Sbase) + Pmid
            else:
                Creact3 = 0
            if Yreac[3] != 0:
                Creact4 = -(Kon * Yreac[3] * Sbase) + Pon
            else:
                Creact4 = 0
            if Yreac[4] != 0:
                Creact5 = -(Kon * Yreac[4] * Sbase) + Pon
            else:
                Creact5 = 0

            total = ClossAC + Creact1 + Creact2 + Creact3 + Creact4 + Creact5

            total_cost[comb] = total.round(decimals=2)
        else:
            of_result[comb] = 1e100
            total_cost[comb] = 1e100

    if flag_placement:  # Evaluate the best reactor combination
        best_result = of_result.argmin()
        best_cost = total_cost.argmin()
        Umod, Utheta, Imod, Itheta, Yl_x, Yreac_x = identify_x(
            result[best_result].x, n_w, xj_len[best_result], n_Y[best_result])
        Yreac = np.zeros(len(reac_comb[best_result]))
        Yreac[reac_comb[best_result]] = Yreac_x
        Yl = np.zeros((n_w, len(reac_comb[best_result])))
        Yl[:, reac_comb[best_result]] = Yl_x
    else:
        if np.all(Y_init == 0) and flag_pfInit == True:
            warnings.warn("Não foi possível alocar nenhuma combinação de reator no sistema definido para atender o limite de fator de potência especificado na LT, mas a operação sem reator atende aos limites de tensão e corrente do sistema.")
            best_result = 0
            best_cost = 0
            Umod = np.abs(U_init[:, 0:5])
            Utheta = np.angle(U_init[:, 0:5])
            Imod = np.abs(I_init)
            Itheta = np.angle(I_init)
            Yl = np.imag(Y_init)
            Yreac = np.zeros(5)
        else:
            raise Exception(
                "Não foi possível alocar nenhuma combinação de reator no sistema definido para atender os limites especificados. Verifique os dados de entrada!")

    U = Umod * np.exp(Utheta * 1j)
    I = Imod * np.exp(Itheta * 1j)

    U = np.append(U, np.ones((n_w, 1))*Ug, 1)

    # AC costs calculation
    U5 = U[0:, 4]
    Ig = I[0:, 5]

    PlossAC = np.sum(acLosses(PowfN_pu, U5, Ig, Sbase) * pw)
    ClossAC = lossesCost(Towf, Ce, PlossAC) / 1e6

    setupResultsBest = [Yreac[0], Yreac[1], Yreac[2], Yreac[3],
                        Yreac[4], ClossAC, PowfN_pu, QowfN_pu, U, I, Yl]

    if best_result == best_cost:
        setupResultsCost = setupResultsBest
    else:
        Umod, Utheta, Imod, Itheta, Yl_x, Yreac_x = identify_x(
            result[best_cost].x, n_w, xj_len[best_cost], n_Y[best_cost])
        Yreac = np.zeros(len(reac_comb[best_cost]))
        Yreac[reac_comb[best_cost]] = Yreac_x
        Yl = np.zeros((n_w, len(reac_comb[best_cost])))
        Yl[:, reac_comb[best_cost]] = Yl_x

        U = Umod * np.exp(Utheta * 1j)
        I = Imod * np.exp(Itheta * 1j)

        U = np.append(U, np.ones((n_w, 1))*Ug, 1)

        # AC costs calculation
        U5 = U[0:, 4]
        Ig = I[0:, 5]

        PlossAC = np.sum(acLosses(PowfN_pu, U5, Ig, Sbase) * pw)
        ClossAC = lossesCost(Towf, Ce, PlossAC) / 1e6

        setupResultsCost = [Yreac[0], Yreac[1], Yreac[2], Yreac[3],
                            Yreac[4], ClossAC, PowfN_pu, QowfN_pu, U, I, Yl]

    return setupResultsBest, setupResultsCost
