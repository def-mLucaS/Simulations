from py_wake.site import XRSite

# from py_wake.site.shear import PowerShear
import xarray as xr
import numpy as np

from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.wind_turbines.generic_wind_turbines import GenericTIRhoWindTurbine


def cafc(K, A):
    # 1) dados entrada (USUÁRIO)
    K = [float(K)] * 24
    A = [float(A)] * 24

    # 2) Modelo de aerogerador
    my_wt, diameter = criar_modelos_de_turbinas()

    # 3) Distâncias entre aerogeradores (FIXO)
    # Define a distrib. do GRID, por exemplo "diamante", com aerogeradores
    # equidistantes:
    X = 10
    Y = 10
    n_aerogeradores = X * Y - np.floor(Y / 2)
    # print(n_aerogeradores)

    # Predefinição da magnitude dos afastamentos dos aerogeradores:
    AFT = [5.0, 7.5, 10.0, 12.5, 15.0]
    afastamentos = AFT

    # Lista que irão receber coordenadas das posições dos aerogeradores.
    x = [[], [], [], [], []]
    y = [[], [], [], [], []]

    all_distances = []

    for aft in AFT:
        dist = diameter * aft  # Distância entre os aerogeradores
        all_distances.append(aft)
        h_pq = ((dist) ** 2 - (dist / 2) ** 2) ** (
            1 / 2
        )  # Altura do triângulo equilátero

        xx = []  # Lista vazia das posições dos aerogeradores em x

        for xx_value in np.arange(
            0, X * dist - 0.5 * dist, 0.5 * dist
        ):  # Lista com todas as posições dos aerogeradores em x
            xx.append(xx_value)

        yy_array = np.arange(
            0, h_pq * Y, h_pq
        )  # Array com posições dos aerogeradoes em y
        yy = []  # Lista vazia das posições dos aerogeradores em y

        for (
            y_value
        ) in yy_array:  # Lista com todas as posições dos aerogeradores em y
            yy.append(y_value)

        for j in yy:  # Preenche as listas x e y com dados de xx e yy
            if (yy.index(j) % 2) == 0:
                for n in xx:
                    # print(xx.index(n))
                    if (xx.index(n) % 2) == 0:
                        x[AFT.index(aft)].append(n)
                        y[AFT.index(aft)].append(j)
            else:
                for n in xx:
                    # print(xx.index(n))
                    if (xx.index(n) % 2) != 0:
                        x[AFT.index(aft)].append(n)
                        y[AFT.index(aft)].append(j)

    # 5) Frequência de ventos por setor
    # Listas de zeros, para distribuição de ventos em formato de rosa dos
    # ventos, com 24 setores de vento:
    f_00, f_15, f_30, f_45, f_60 = (
        [0.0] * 24,
        [0.0] * 24,
        [0.0] * 24,
        [0.0] * 24,
        [0.0] * 24,
    )

    # Def. das listas para frências de ventos, em 100%, para ventos recebidos
    # a 0°, 15°, 30°, 45° e 60°:
    f_00[0], f_15[1], f_30[2], f_45[3], f_60[4] = 1.0, 1.0, 1.0, 1.0, 1.0
    wd = np.linspace(0, 360, len(f_60), endpoint=False)
    ti = 0.1

    # Definição das condições locais de vento para as direções de 0°, 15°, 30°, 45° e 60°:
    def site_maker(f_xx, A, K, ti, wd):
        result = XRSite(
            ds=xr.Dataset(  # xr.Dataset - banco de dados multidimensional
                data_vars={  # Um mapeamento de nomes de variáveis para objetos DataArray
                    "Sector_frequency": (
                        "wd",
                        f_xx,
                    ),  # wd: referência da direção do vento
                    "Weibull_A": ("wd", A),
                    "Weibull_k": ("wd", K),
                    "TI": ti,
                },
                coords={"wd": wd},
            )
        )
        return result

    site_15 = site_maker(f_15, A, K, ti, wd)

    # 6) Modelo de déficit de vigília
    # O modelo de déficit de vigília NOJDeficit e o modelo de déficit de vigília BastankhahGaussianDeficit
    # são modelos de simulação que estimam o impacto do efeito de sombreamento em um parque eólico em termos
    # de perda de energia devido ao déficit de vento.

    # %matplotlib inline

    from py_wake.literature.gaussian_models import Bastankhah_PorteAgel_2014 as BK

    # O modelo é derivado aplicando a conservação de massa e momento e assumindo uma distribuição gaussiana
    # para o déficit de velocidade na esteira. Este modelo simples requer apenas um parâmetro para determinar a
    # distribuição de velocidade na esteira. Os resultados mostram que o modelo prevê a energia extraída
    # por turbinas eólicas a favor do vento com mais precisão do que outros modelos analíticos comuns, alguns dos
    # quais são baseados em suposições menos precisas, como considerar uma forma de cartola para o déficit de velocidade.
    # DOI: 10.1016/j.renene.2014.01.002
    mod_15 = BK(site_15, my_wt, k=0.04)

    from py_wake.literature.noj import Jensen_1983

    # O modelo NOJDeficit usa a teoria de Jensen, que assume que o fluxo de ar é desviado ao redor de cada
    # turbina em uma zona de influência de raio igual a duas vezes o diâmetro do rotor, criando um déficit de
    # velocidade que se estende até o limite da zona de influência.
    # https://backend.orbit.dtu.dk/ws/portalfiles/portal/55857682/ris_m_2411.pdf
    mod_15 = Jensen_1983(site_15, my_wt)

    simulationResult_15_0 = mod_15(x[0], y[0])
    simulationResult_15_1 = mod_15(x[1], y[1])
    simulationResult_15_2 = mod_15(x[2], y[2])
    simulationResult_15_3 = mod_15(x[3], y[3])
    simulationResult_15_4 = mod_15(x[4], y[4])

    Distancias = ["5.0xD", "7.5xD", "10.0xD", "12.5xD", "15.0xD"]

    def plt_noj(i, j, Simulation_Result_XX, xy_value, EAP_value):
        # As plotagens foram suspendidas
        aep = Simulation_Result_XX.aep()
        aep_resultado = aep.sum(["wd", "ws"])
        aep_valor_maximo = aep_resultado.max().item()

        # fig, axs = plt.subplots(2,3, figsize=(14, 7))
        # #Plotando a scatter plot
        # scatter = axs[i,j].scatter(x[xy_value], y[xy_value], c=aep.sum(['wd','ws']), cmap='plasma', norm=colors.LogNorm(vmin=25, vmax=35))
        # # Definindo o título do subplot
        # axs[i,j].set_title(f'Total AEP {Distancias[xy_value]}: {"{:.2f}".format(np.array(Simulation_Result_XX.aep().sum()))} GWh')
        # Ajustando o layout dos subplots
        # plt.tight_layout()
        CAFC[EAP_value].append(
            float(
                "{:.2f}".format(
                    (np.array(aep.sum()))
                    * 100
                    / (aep_valor_maximo * n_aerogeradores)
                )
            )
        )
        # Adicionando a barra de cores compartilhada
        # if i == 1 and j == 2:
        #     fig.colorbar(scatter, ax=axs.ravel().tolist(), shrink=1.0, label='AEP [GWh]')
        #     scatter.set_clim(vmin=(25.0), vmax=(34.0))

    # 7) Comparação gráfica entre AEP por distâncias dos aerogeradores
    # Lista que recebe o Coeficiente de Ajuste de Fator de Capacidade calculado
    CAFC = [[], [], [], [], []]

    # Resultado para um vento a 0° (f_00):
    # fig, axs = plt.subplots(2,3, figsize=(14, 7))

    # Resultado para um vento a 15° (f_15):
    # fig, axs = plt.subplots(2,3, figsize=(14, 7)) 
    plt_noj(0, 0, simulationResult_15_0, 0, 1)
    plt_noj(0, 1, simulationResult_15_1, 1, 1)
    plt_noj(0, 2, simulationResult_15_2, 2, 1)
    plt_noj(1, 0, simulationResult_15_3, 3, 1)
    plt_noj(1, 1, simulationResult_15_4, 4, 1)

    # 8) Coef. de ajuste de capacidade (ni)
    # O resultado para ventos a 30° (f_30) deve ser o pior. Isso acontece por haver um maior sombreamento
    # dos aerogeradores. Os resultados para ventos de 15° (f_15) e 45° (f_45) devem ser iguais e apresentar
    # os melhores resultados. Isso se deve por haver um menor sombreamento nesta configuração de aerogeradores.
    # Conforme aumenta-se o afastamento entre os aerogeradores (AFT), o Coeficiente de Ajuste de Capacidade (CAC)
    # tende a 100%.
    # from scipy.interpolate import interp1d
    # fig, ax = plt.subplots(figsize = (9, 6))
    # for i in range(len(CAFC)):
    #     # criar uma função interpoladora para os pontos
    #     f = interp1d(AFT, CAFC[i], kind='cubic')

    #     # gerar pontos para a função interpolada
    #     xnew = np.linspace(min(AFT), max(AFT), num=100)
    #     # plotar a função interpolada
    #     ax.plot(xnew, f(xnew), label=f"{i*15}°")

    #     # plotar os pontos originais
    #     ax.scatter(AFT, CAFC[i])

    # ax.set_xlabel('AFT [-]')
    # ax.set_ylabel('Coef. de Ajuste de Capacidade [%]')
    # ax.legend(loc='lower right')
    # plt.grid()
    # plt.show()
    # print(CAFC) [[], [68.72, 89.01, 94.61, 96.83, 97.92, 98.52], [], [], []]

    return CAFC, all_distances, afastamentos


def criar_modelos_de_turbinas(power=None):
    """Função para a criação das turbinas
    Obs. a função está criando para uma range de vento entre 0 e 14.5 m/s, isso deve ser corrigido até 34.5 m/s"""

    diameter_ = 164.0

    # Modelo de aerogerador pré-definido V164-9.5MW. (FIXO)
    # Calculo do Coeficiente de empuxo CT (coefficient trust):
    wt_ct = GenericTIRhoWindTurbine('WT_83.5_8MW',
                                    164.0,
                                    321.0,
                                    power_norm=8000.0,
                                    default_TI_eff=.1,
                                    default_Air_density=1.225)

    # Começa em 3.5 porque o ct começa ca partir dessa velocidade
    uu = np.arange(3.5, 14.5, .5)
    ct = [0.0]*6
    # O append a partir do elemento 7, pois os primeiros são zerados
    p, ct_valor = wt_ct.power_ct(uu, TI_eff=0.1)

    # Separa o ct do p calaculados no wt_ct:
    for i in ct_valor:
        ct.append(i)

    # Define intervalo de velocidade do vento:
    u = np.arange(.5, 14.5, .5)

    # Define a curva de potência se não estiver definida:
    if power is None:
        power = [0, 0, 0,   0,   0,   0, 115, 249, 430, 613, 900, 1226, 1600, 2030, 2570,
                 3123, 3784, 4444, 5170, 5900, 6600, 7299, 7960, 8601, 9080, 9272, 9410, 9500]

    if len(power) > 42:
        del power[-42:]

    # Cria o modelo de turbina my_wt:
    my_wt = WindTurbine(name='MyWT',
                        diameter=diameter_,
                        hub_height=321,
                        powerCtFunction=PowerCtTabular(u, power, 'kW', ct))
    return my_wt, diameter_