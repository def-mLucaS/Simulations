import numpy as np


def generationProfile(Sproj, exportPar, exportType):

    c = exportPar['ScaleFac']
    k = exportPar['ShapeFac']
    FPowfN = exportPar['FPowfN']
    flag_allWind = exportPar['flag_allWind']
    flag_zeroP = exportPar['flag_zeroP']
    Pshape = exportPar['Pshape']
    Pshape = Pshape / Pshape.max()

    wind_speed = np.interp(np.arange(0, len(Pshape)/2, 1),
                           np.arange(0, len(Pshape)/2, 0.5), exportPar['wind_speed'])

    if flag_allWind:
        pw = ((k/c)*(wind_speed/c)**(k-1)) * np.exp(-(wind_speed/c)**k)
        if exportType == 'AC':
            PowfN = np.interp(np.arange(0, len(
                Pshape)/2, 1), np.arange(0, len(Pshape)/2, 0.5), Pshape) * Sproj * np.abs(FPowfN)
        elif exportType == 'DC':
            PowfN = np.interp(np.arange(0, len(Pshape)/2, 1),
                              np.arange(0, len(Pshape)/2, 0.5), Pshape) * Sproj
        else:
            raise Exception(
                f"Tecnologia de exportação {exportType} inválida. Escolha entre tecnologia AC ou DC.")
    else:
        if exportType == 'AC':
            PowfN = np.array([0.026, 1]) * Sproj * np.abs(FPowfN)  # MW
        elif exportType == 'DC':
            PowfN = np.array([0.026, 1]) * Sproj
        else:
            raise Exception(
                f"Tecnologia de exportação {exportType} inválida. Escolha entre tecnologia AC ou DC.")
        if flag_zeroP:
            pw = np.array([0.137987, 0.194621])
        else:
            pw = np.array([0.0662844, 0.194621])

    if isinstance(PowfN, np.ndarray):
        aux_sort = np.argsort(PowfN, kind='mergesort')

        PowfN = PowfN[aux_sort]
        pw = pw[aux_sort]

        has_zero = PowfN == 0

        if flag_zeroP:
            zero_pw = np.sum(pw[has_zero])
        else:
            zero_pw = 0

        PowfN = np.delete(PowfN, has_zero)
        pw = np.delete(pw, has_zero)

        PowfN = PowfN.round(decimals=0)

        PowfN, aux_start, n_value = np.unique(
            PowfN, return_index=True, return_counts=True)

        n_w = len(PowfN)

        if exportType == 'AC':
            QowfN = PowfN * np.tan(np.arccos(FPowfN))  # Mvar
        elif exportType == 'DC':
            QowfN = PowfN * 0
        else:
            raise Exception(
                f"Tecnologia de exportação {exportType} inválida. Escolha entre tecnologia AC ou DC.")

        pw_new = np.zeros(len(PowfN))

        for rep in range(len(aux_start)):
            if n_value[rep] == 1:
                if rep == 0:
                    pw_new[rep] = pw[aux_start[rep]] + zero_pw
                else:
                    pw_new[rep] = pw[aux_start[rep]]
            else:
                pw_new[rep] = np.sum(
                    pw[aux_start[rep]:aux_start[rep]+n_value[rep]])

        pw = pw_new
    else:
        n_w = 1
        if exportType == 'AC':
            QowfN = PowfN * np.tan(np.arccos(FPowfN))  # Mvar
        elif exportType == 'DC':
            QowfN = PowfN * 0
        else:
            raise Exception(
                f"Tecnologia de exportação {exportType} inválida. Escolha entre tecnologia AC ou DC.")

    return n_w, pw, PowfN, QowfN
