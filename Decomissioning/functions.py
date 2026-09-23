
import numpy as np
import matplotlib.pyplot as plt
from ...utils.utils import temp_file

global alpha
alpha = 1
global beta
beta = 1

#   CUSTO DE REMOÇÃO DA TURBINA


def Wt_cost1(c_mob_juv, alpha, beta, c_mob_bv, cd_juv, cd_bv, cd_tb, tw):

    cost_wt = c_mob_juv + alpha*c_mob_bv + \
        (cd_juv + alpha*cd_bv + beta*cd_tb)*(tw)
    print("Hello!")

    return cost_wt[0]


def Wt_cost2(tw, cd_wtiv, mob_wtiv):
    # /2 because is divided with the foundation removal
    cost_wt = tw*cd_wtiv + mob_wtiv/2

    return cost_wt[0]


def Wt_cost3(tw, cd_wtiv, mob_wtiv):
    # /2 because is divided with the foundation removal
    cost_wt = tw*(2*cd_wtiv) + 2*mob_wtiv/2

    return cost_wt[0]

# TEMPO DE REMOÇÃO DA TURBINA


def Tw1(n_t, t_pos_juv, t_up_juv, t_b_n, t_t, t_down_juv, weather_delay):

    tw = n_t*(t_pos_juv + t_up_juv + t_b_n + t_t + t_down_juv)*weather_delay

    return tw/24


def Tw2(d_port, wtiv_speed, wtiv_capacity_wt, t_blades, t_nacelle, t_ut, t_lt, t_up_l, t_pos, t_down, t_offload, w, n_t):

    t_travel = 2*d_port/wtiv_speed
    t_remove_t = wtiv_capacity_wt*(t_blades + t_nacelle + t_ut + t_lt)
    t_load_t = wtiv_capacity_wt*(t_up_l)
    t_move_t = wtiv_capacity_wt*(t_pos)
    t_offload_t = wtiv_capacity_wt*(t_down + t_offload)
    t_trip_t = t_travel + t_remove_t + t_load_t + t_move_t + t_offload_t
    t_weather_t = t_trip_t*w
    n_trips_t = n_t / wtiv_capacity_wt
    tw = t_weather_t*n_trips_t

    return tw/24


def Tw3(d_port, wtiv_speed, wtiv_capacity_wt, t_blades, t_nacelle, t_ut, t_lt, t_up_l, t_pos, t_down, t_offload, w, n_t):

    t_travel = 2*d_port/wtiv_speed
    t_remove_t = wtiv_capacity_wt*(t_blades + t_nacelle + t_ut + t_lt)
    t_load_t = wtiv_capacity_wt*(t_up_l)
    t_move_t = wtiv_capacity_wt*(t_pos)
    t_offload_t = wtiv_capacity_wt*(t_down + t_offload)
    t_trip_t = t_travel + t_remove_t + t_load_t + t_move_t + t_offload_t
    t_weather_t = t_trip_t*w
    n_trips_t = n_t / wtiv_capacity_wt
    tw = t_weather_t*n_trips_t

    return tw/24 / 2


# CUSTO DE REMOÇÃO DA FUNDAÇÃO
def Foundation_cost1(c_mob_juv, alpha, beta, c_mob_bv, c_mob_rov, cd_osv, cd_juv, cd_bv, cd_tb, cd_rov, n_t,
                     t_pos_osv, t_move_osv, t_p, t_c, t_pos_juv, t_up_juv, t_l_juv, t_down_juv, weather_delay):

    t_total_juv = n_t*(t_pos_juv + t_up_juv + t_l_juv +
                       t_down_juv)*weather_delay/24
    t_total_osv = n_t*(t_pos_osv + t_p + t_c + t_move_osv)*weather_delay/24
    if t_pos_osv == 0:
        t_total_osv = 0
    cost_foundation = c_mob_juv + alpha*c_mob_bv + c_mob_rov + cd_osv*t_total_osv + \
        (cd_juv + alpha*cd_bv + beta*cd_tb) * \
        t_total_juv + cd_rov*(t_total_osv+t_total_juv)

    return cost_foundation


def Foundation_cost2(t_decom_f, cd_wtiv, mob_wtiv):
    decom_cost_f = t_decom_f*cd_wtiv + mob_wtiv/2

    return decom_cost_f


def Foundation_cost3(t_decom_f, cd_wtiv, mob_wtiv):
    decom_cost_f = t_decom_f*(2*cd_wtiv) + 2*mob_wtiv/2

    return decom_cost_f


def Foundation_time1(n_t, t_pos_osv, t_move_osv, t_p, t_c, t_pos_juv, t_up_juv, t_l_juv, t_down_juv, n_juv, weather_delay):

    # JUV
    t_total_juv = n_t*(t_pos_juv + t_up_juv + t_l_juv + t_down_juv)

    # OSV
    t_total_osv = n_t*(t_pos_osv + t_p + t_c + t_move_osv)  # COM OSV

    t_total = (t_total_juv + t_total_osv)*weather_delay/24

    return t_total


def Foundation_time2(d_port, wtiv_speed, wtiv_capacity_f, t_tp, t_f, t_up_l, t_pos, t_down, t_offload, w, n_f):
    t_travel = 2*d_port/wtiv_speed
    t_remove_f = wtiv_capacity_f*(t_tp + t_f)
    t_load_f = wtiv_capacity_f*(t_up_l)
    t_move_f = wtiv_capacity_f*(t_pos)
    t_offload_f = wtiv_capacity_f*(t_down + t_offload)
    t_trip_f = t_travel + t_remove_f + t_load_f + t_move_f + t_offload_f
    t_weather_f = t_trip_f*w
    n_trips_f = n_f/wtiv_capacity_f
    t_decom_f = t_weather_f*n_trips_f/24

    return t_decom_f


def Foundation_time3(d_port, wtiv_speed, wtiv_capacity_f, t_tp, t_f, t_up_l, t_pos, t_down, t_offload, w, n_f):

    t_decom_f = Foundation_time2(
        d_port, wtiv_speed, wtiv_capacity_f, t_tp, t_f, t_up_l, t_pos, t_down, t_offload, w, n_f)/2

    return t_decom_f


# CUSTO DE REMOÇÃO DA OS
def T_total_os1(n_os, t_pos_juv, t_up_juv, t_c_os, t_l_top_os, t_p, t_l_juv, t_down_juv, weather_delay):

    t_total_os = n_os*(t_pos_juv + t_up_juv + t_c_os +
                       t_l_top_os + t_p + t_l_juv + t_down_juv)*weather_delay

    return t_total_os/24


def T_total_os2(wtiv_capacity_f, t_tp, t_f, t_up_l, t_pos, t_down, t_offload, d_port, wtiv_speed, w, n_os):

    t_travel = 2*d_port/wtiv_speed
    t_remove_os = n_os*(t_tp + t_f)
    t_load_os = n_os*(t_up_l)
    t_move_os = n_os*(t_pos)
    t_offload_os = n_os*(t_down + t_offload)
    t_trip_os = t_travel + t_remove_os + t_load_os + t_move_os + t_offload_os
    t_weather_os = t_trip_os*w
    n_trips_os = np.ceil(n_os/wtiv_capacity_f)
    t_decom_os = t_weather_os*n_trips_os/24

    return t_decom_os


def T_total_os3():
    return 0


def Os_cost1(c_mob_juv, c_mob_rov, c_mob_bv, cd_juv, cd_osv, cd_rov, alpha, beta, cd_bv, cd_tb, t_total_os):

    cost_os = c_mob_juv + c_mob_rov + c_mob_bv + \
        (cd_juv + cd_osv + cd_rov + alpha*cd_bv + beta*cd_tb) * t_total_os

    return cost_os


def Os_cost2(t_decom_os, cd_wtiv):
    decom_cost_mm = t_decom_os*cd_wtiv

    return decom_cost_mm


def Os_cost3():
    return 0

# CUSTO DE REMOÇÃO DA MM


def T_total_mm1(n_mm, t_pos_juv, t_up_juv, t_c_mm, t_l_top_mm, t_p, t_l_juv, t_down_juv, weather_delay):

    t_total_mm = n_mm*(t_pos_juv + t_up_juv + t_c_mm +
                       t_l_top_mm + t_p + t_l_juv + t_down_juv)*weather_delay

    return t_total_mm/24


def T_total_mm2(wtiv_capacity_f, t_tp, t_f, t_up_l, t_pos, t_down, t_offload, d_port, wtiv_speed, w, n_mm):

    t_travel = 2*d_port/wtiv_speed
    t_remove_mm = n_mm*(t_tp + t_f)
    t_load_mm = n_mm*(t_up_l)
    t_move_mm = n_mm*(t_pos)
    t_offload_mm = n_mm*(t_down + t_offload)
    t_trip_mm = t_travel + t_remove_mm + t_load_mm + t_move_mm + t_offload_mm
    t_weather_mm = t_trip_mm*w
    n_trips_mm = np.ceil(n_mm/wtiv_capacity_f)
    t_decom_mm = t_weather_mm*n_trips_mm/24

    return t_decom_mm


def T_total_mm3():
    return 0


def Mm_cost1(c_mob_juv, c_mob_rov, c_mob_bv, cd_juv, cd_osv, cd_rov, alpha, beta, cd_bv, cd_tb, t_total_mm):

    cost_mm = (cd_juv + cd_osv + cd_rov + alpha *
               cd_bv + beta*cd_tb) * t_total_mm

    return cost_mm


def Mm_cost2(t_decom_mm, cd_wtiv, mob_wtiv):

    if t_decom_mm == 0:
        decom_cost_mm = 0
    else:
        decom_cost_mm = t_decom_mm*cd_wtiv + mob_wtiv/2

    return decom_cost_mm


def Mm_cost3():
    return 0


# CUSTO DE REMOÇÃO DOS CABOS
def T_total_cables1(l_i, r_i, if_i, l_e, r_e, if_e, weather_delay):
    t_i = l_i/(r_i*if_i)*weather_delay
    t_e = l_e/(r_e*if_e)*weather_delay

    return (t_i + t_e)


def T_total_cables2():

    return 0


def T_total_cables3():

    return 0


def Cables_cost1(c_mob_clv_i, c_mob_clv_e, c_mob_rov, cd_clv_i, cd_rov, t_i_e):

    cost_cables = c_mob_clv_i + c_mob_clv_e + \
        c_mob_rov + (cd_rov)*(t_i_e) + cd_clv_i*t_i_e

    return cost_cables


def Cables_cost2():
    return 0


def Cables_cost3():
    return 0


# CUSTO DE LIMPEZA DO SOLO
def T_total_seabed1(n_t, n_os, t_pos_dcbv, t_a_dcbv, v_i_wt, r_ret, v_i_os, v_i_mm, r_rd,  weather_delay):
    t_total_sp = ((n_t + n_os + 1)*(t_pos_dcbv + t_a_dcbv) + (n_t*v_i_wt/r_ret) +
                  (n_os*v_i_os/r_ret) + (n_os*v_i_mm/r_ret)) / 24 * weather_delay
    t_total_rd = ((n_t + n_os + 1)/r_rd) / 24 * weather_delay

    t_total = t_total_rd + t_total_sp

    return t_total


def T_total_seabed2():
    return 0


def T_total_seabed3():
    return 0


def Seabed_clearance_cost1(n_t, n_os, t_pos_dcbv, t_a_dcbv, v_i_wt, r_ret, v_i_os, v_i_mm, c_mob_dcbv, c_mob_bv, c_mob_rov, cd_dcbv, cd_bv, cd_tb, cd_rov, r_rd, c_mob_rdv, cd_rdv, weather_delay):

    # ASSUME VOLUME DE SCOUR PROTECTION IGUAL EM TODAS AS TURBINAS
    t_total_sp = ((n_t + n_os + 1)*(t_pos_dcbv + t_a_dcbv) + (n_t*v_i_wt/r_ret) +
                  (n_os*v_i_os/r_ret) + (n_os*v_i_mm/r_ret)) / 24 * weather_delay
    cost_seabed_sp = c_mob_dcbv + c_mob_bv + alpha*c_mob_rov + \
        (cd_dcbv + alpha*cd_bv + beta*cd_tb + cd_rov)*t_total_sp

    t_total_rd = ((n_t + n_os + 1)/r_rd)/24 * weather_delay
    cost_seabed_rd = c_mob_rdv + c_mob_rov + (cd_rdv + cd_rov)*t_total_rd

    cost_seabed_clearance = cost_seabed_sp + cost_seabed_rd

    return cost_seabed_clearance


def Seabed_clearance_cost2():
    return 0


def Seabed_clearance_cost3():
    return 0


def Plot(canvas, Costs_type, Values, Values_list, values_ref):
    num_bars = len(Values[0])  # Número de conjuntos de valores
    largura = 0.8 / num_bars  # Ajustar a largura das barras para caber no gráfico

    # Configurações do gráfico
    x = np.arange(len(Costs_type))  # Localização das barras

    if canvas is None:
        ax = plt.subplots()
    else:
        ax = canvas.figure.add_subplot(111)

        legenda_adicionada = False

        for i in range(num_bars):
            valores = [value[i] for value in Values]
            ax.bar(x + i * largura - (num_bars - 1) * largura /
                   2, valores, largura, label=Values_list[i])
            if len(values_ref) > 1:
                valores_ref = [value[i] for value in values_ref]

                if not legenda_adicionada:
                    ax.scatter(x + i * largura - (num_bars - 1) * largura / 2, valores_ref,
                               color='red', marker='x', zorder=5, label='Jalili et al (2022)')
                    legenda_adicionada = True
                else:

                    ax.scatter(x + i * largura - (num_bars - 1) * largura / 2,
                               valores_ref, color='red', marker='x', zorder=5)

        ax.set_xlabel('Tipos de custos')
        ax.set_ylabel('Custos [US$]')
        ax.set_title('Custos')
        ax.set_xticks(x)
        ax.set_xticklabels(Costs_type)
        ax.legend()

        if canvas is None:
            plt.show()
        else:
            canvas.figure.tight_layout()
            canvas.draw()
            canvas.figure.savefig(temp_file('cs1.png'))


def plot_bar_chart(canvas, x_labels, values, file, title='Gráfico Barra', x_label='Categorias', y_label='Valores', color='blue'):
    """
    Plota um gráfico de barras com rótulos personalizados no eixo x.

    Parâmetros:
    - x_labels: Lista de strings para o eixo x.
    - values: Lista de valores numéricos para as barras.
    - title: Título do gráfico.
    - x_label: Rótulo para o eixo x.
    - y_label: Rótulo para o eixo y.
    - color: Cor das barras (padrão é azul).
    """

    # Verificar se as listas têm o mesmo tamanho
    if len(x_labels) != len(values):
        raise ValueError(
            "O número de rótulos (x_labels) deve ser igual ao número de valores (values).")

    # Criar ou usar o canvas existente
    if canvas is None:
        # Criar um novo gráfico de barras
        plt.figure(figsize=(10, 6))
        ax = plt.gca()  # Obtém o eixo atual

    else:
        ax = canvas.figure.add_subplot(111)  # Adiciona um subplot ao canvas

        # Limpar o conteúdo do eixo anterior
        ax.clear()

    # Criar o gráfico de barras no eixo `ax`
    ax.bar(x_labels, values, color=color)

    # Adicionar título e rótulos dos eixos
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Definir rótulos do eixo x e sua rotação
    # Ajustar os ticks do eixo x para cada rótulo
    ax.set_xticks(range(len(x_labels)))
    # Alinhamento à direita para melhor visualização
    ax.set_xticklabels(x_labels, rotation=45, ha='right')

    # Ajustar o layout para evitar sobreposição
    canvas.figure.tight_layout() if canvas else plt.tight_layout()

    # Desenhar no canvas ou mostrar a nova figura
    if canvas:
        canvas.draw()  # Atualiza o canvas
        # Salva a figura, se necessário
        canvas.figure.savefig(temp_file(file))
    else:
        plt.show()  # Exibe a nova figura


def plot_pizza_chart(canvas, array, labels, file):
    import numpy as np
    import matplotlib.pyplot as plt

    # Converte o array para numpy array, caso não seja
    array = np.array(array)

    # Filtra os valores e labels onde os valores são diferentes de zero
    filtered_array = array[array > 0]
    filtered_labels = np.array(labels)[array > 0]

    # Verifica se há valores a serem plotados
    if len(filtered_array) == 0:
        raise ValueError("Não há valores diferentes de zero para plotar.")

    # Calcula o total do array
    total = np.sum(filtered_array)

    # Calcula os percentuais
    percentuais = (filtered_array / total) * 100

    # Define um ângulo inicial para evitar que fatias pequenas fiquem próximas
    startangle = 140

    # Plota o gráfico de pizza sem rótulos
    if canvas is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    else:
        ax = canvas.figure.add_subplot(111)

     # Limpar o conteúdo do eixo anterior, se necessário
    ax.clear()

    # Removido o parâmetro autopct
    wedges, _ = ax.pie(percentuais, labels=None, startangle=startangle)

    # Ajusta a posição dos rótulos para que não se sobreponham
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = wedge.r * np.cos(np.radians(angle))
        y = wedge.r * np.sin(np.radians(angle))

        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(angle)

        # Adiciona o rótulo e o percentual ao lado
        label_with_percent = f"{filtered_labels[i]} ({percentuais[i]:.1f}%)"
        ax.annotate(label_with_percent, xy=(x, y), xytext=(1.5 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle))

    if canvas is None:
        # Ajusta o layout para melhorar a visualização
        plt.tight_layout()

        # Mostra o gráfico
        plt.show()
    else:
        # Ajusta o layout para melhorar a visualização
        canvas.figure.tight_layout()

        # Atualiza o canvas para refletir o gráfico
        canvas.draw()
        
        # Salva a figura, se necessário
        canvas.figure.savefig(temp_file(file))
