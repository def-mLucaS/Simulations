import datetime
import pandas as pd
import plotly.express as px
import textwrap
from dateutil.relativedelta import relativedelta
from ....utils.utils import temp_file


def corrigirCronograma(cronograma, tempo_indisp):
    lista_cron = cronograma
    data_inicial = lista_cron[0]["Start"]
    data_final = lista_cron[-1]["Finish"]
    mes_inicial = data_inicial.month

    numero_meses = (data_final.year - data_inicial.year) * \
        12 + data_final.month - data_inicial.month
    mes_inicial = datetime.datetime(
        lista_cron[0]["Start"].year, lista_cron[0]["Start"].month, 1)

    lista_meses = []

    i = 0
    while i <= numero_meses:
        i += 1
        lista_meses.append(
            [mes_inicial + relativedelta(months=i-1), mes_inicial + relativedelta(months=i)])

    lista_meses[0][0] = data_inicial

    lista_emb = []
    for tarefa in lista_cron:
        string_emb = tarefa["Tarefa"].split(" ")
        lista_emb.append(string_emb[0])

    lista_emb = list(set(lista_emb))

    for tarefa in lista_cron:
        dif_tempo = tarefa['Finish'] - tarefa['Start']
        tarefa["Tempo da Tarefa"] = dif_tempo

    tempo_disponivel_mes = []
    for key, mes in enumerate(lista_meses):

        tempo_disponivel = mes[1] - mes[0] - \
            datetime.timedelta(days=tempo_indisp[mes[0].month-1])
        tempo_disponivel_mes.append(tempo_disponivel)

    dict_emb = {}
    for emb in lista_emb:
        lista_tarefas_emb = []
        for tarefa in lista_cron:
            string_emb = tarefa["Tarefa"].split(" ")
            if emb == string_emb[0]:
                lista_tarefas_emb.append(tarefa)
        dict_emb[emb] = sorted(lista_tarefas_emb, key=lambda d: d['Start'])

    dict_emb_mes = {}
    for emb in dict_emb:
        dict_emb_mes[emb] = {}

    for emb in dict_emb:
        i = 0
        for mes in lista_meses:
            lista_tarefas_mes = [d for d in dict_emb[emb] if d['Start'].month ==
                                 mes[0].month and d['Start'].year == mes[0].year]
            dict_emb_mes[emb][mes_inicial.month+i] = lista_tarefas_mes
            i += 1

    lista_delete = []
    for emb in dict_emb_mes:
        for mes in dict_emb_mes[emb]:
            if dict_emb_mes[emb][mes] == []:
                lista_delete.append([emb, mes])

    for i in lista_delete:
        del dict_emb_mes[i[0]][i[1]]

    lista_clima = []
    for emb in dict_emb_mes:
        num_meses_emb = len(dict_emb_mes[emb].keys())
        for mes in dict_emb_mes[emb]:
            tempo_disponivel_mes_modificado = tempo_disponivel_mes.copy()
            for key, tarefa in enumerate(dict_emb_mes[emb][mes]):
                tempo_disponivel_mes_modificado[mes -
                                                mes_inicial.month] -= tarefa["Tempo da Tarefa"]
                if tempo_disponivel_mes_modificado[mes - mes_inicial.month] < datetime.timedelta(days=0):
                    start_clima = tarefa["Finish"]
                    if (mes - mes_inicial.month) < num_meses_emb-1:
                        tempo_diff = lista_meses[mes -
                                                 mes_inicial.month + 1][0] - tarefa["Finish"]
                    else:
                        tempo_diff = datetime.timedelta(days=0)
                    tempo_tarefa_desloc = tarefa["Tempo da Tarefa"]
                    tempo_desloc = tempo_diff + tempo_tarefa_desloc
                    finish_clima = tarefa["Finish"] + tempo_desloc
                    t = tarefa["Tarefa"]
                    lista_clima.append([start_clima, finish_clima, t])
                    ponto_desloc = key
                    break
                if key == len(dict_emb_mes[emb][mes])-1:
                    if (mes - mes_inicial.month) < num_meses_emb-1:
                        start_clima = tarefa["Finish"]
                        if (mes - mes_inicial.month) < num_meses_emb-1:
                            tempo_diff = lista_meses[mes -
                                                     mes_inicial.month + 1][0] - tarefa["Finish"]
                        else:
                            tempo_diff = datetime.timedelta(days=0)
                        tempo_tarefa_desloc = tarefa["Tempo da Tarefa"]
                        tempo_desloc = tempo_diff + tempo_tarefa_desloc
                        finish_clima = tarefa["Finish"] + tempo_desloc
                        t = tarefa["Tarefa"]
                        lista_clima.append([start_clima, finish_clima, t])
                        ponto_desloc = key
                    else:
                        pass
                else:
                    pass

            if (mes - mes_inicial.month) < num_meses_emb-1:
                for mes_tarefa in dict_emb_mes[emb]:
                    for key_lista, tarefa_lista in enumerate(dict_emb_mes[emb][mes_tarefa]):
                        if mes_tarefa == mes and key_lista > ponto_desloc:
                            tarefa_lista["Start"] += tempo_desloc
                            tarefa_lista["Finish"] += tempo_desloc
                        if mes_tarefa > mes:
                            tarefa_lista["Start"] += tempo_desloc
                            tarefa_lista["Finish"] += tempo_desloc
                        else:
                            pass

                lista_mes_modificado = []
                for emb_nova in dict_emb_mes:
                    for mes_nova in dict_emb_mes[emb_nova]:
                        for tarefa_modificada in dict_emb_mes[emb_nova][mes_nova]:
                            lista_mes_modificado.append(tarefa_modificada)

                dict_emb2 = {}
                for emb2 in lista_emb:
                    lista_tarefas_emb = []
                    for tarefa2 in lista_mes_modificado:
                        string_emb = tarefa2["Tarefa"].split(" ")
                        if emb2 == string_emb[0]:
                            lista_tarefas_emb.append(tarefa2)
                    dict_emb2[emb2] = sorted(
                        lista_tarefas_emb, key=lambda d: d['Start'])

                dict_emb_mes = {}
                for emb_lista in dict_emb:
                    dict_emb_mes[emb_lista] = {}

                for emb_lista in dict_emb:
                    i = 0
                    for mes_lista in lista_meses:
                        lista_tarefas_mes = [d for d in dict_emb2[emb_lista] if d['Start'].month ==
                                             mes_lista[0].month and d['Start'].year == mes_lista[0].year]
                        dict_emb_mes[emb_lista][mes_inicial.month +
                                                i] = lista_tarefas_mes
                        i += 1

                num_meses_emb = len(dict_emb_mes[emb].keys())

    lista_cron = []
    for emb in dict_emb_mes:
        for mes in dict_emb_mes[emb]:
            for tarefa in dict_emb_mes[emb][mes]:
                lista_cron.append(tarefa)

    for tarefa in lista_clima:
        tarefa_indisp = {
            "Finish": tarefa[1],
            "Macroatividade": "Atividades Suspensas por conta do clima",
            "Microatividade": "Atividades Suspensas por conta do clima",
            "Start": tarefa[0],
            "Tarefa": tarefa[2],
            "Tempo da Tarefa": 0,
            "Tipo": "Clima"
        }
        lista_cron.append(tarefa_indisp)

    for tarefa in lista_cron:
        if "Tempo da Tarefa" in tarefa:
            del tarefa["Tempo da Tarefa"]

    return lista_cron


def gerarCronogramaCorrigido(config, nomeArquivo):
    df = config[0]
    colors = config[1]
    colors.append('red')  # Adiciona cor Clima
    nomeProjeto = config[2]

    df = pd.DataFrame(df)
    df = df.rename({"Tarefa": "Viagens", "Tipo": "Tipo", "Macroatividade": "Macroatividade",
                    "Microatividade": "Microatividade", "Start": "Inicio", "Finish": "Fim"}, axis=1)

    fig = px.timeline(df, x_start="Inicio", x_end="Fim", y="Viagens", color="Tipo",
                      hover_name="Microatividade", color_discrete_sequence=colors,
                      custom_data=['Microatividade', 'Macroatividade'])

    # Adiciona informações extras à dica de ferramenta
    fig.update_layout(legend_title_text="Legenda")
    fig.update_traces(hovertemplate="Início: %{base}<br>"
                                    "Fim: %{x}<br>"
                                    "Microatividade: %{customdata[0]}<br>"
                                    "Macroatividade: %{customdata[1]}")
    # fig.data[0].hovertext = df['Microatividade']  # Define os valores de hovertext para cada ponto no gráfico
    # Limita o número de caracteres exibidos nos nomes da legenda
    # fig.for_each_trace(lambda t: t.update(text=df['Macroatividade']))
    caracteres_maximos = 20
    fig.for_each_trace(lambda t: t.update(
        name='<br>'.join(textwrap.wrap(t.name, caracteres_maximos, break_long_words=False))))

    # Quebra de linha nos nomes das tarefas
    caracteres_maximos_tarefa = 10
    # da errado esse trecho
    # nomes_tarefas = [textwrap.fill(t, caracteres_maximos_tarefa, break_long_words=False).replace('\n', '<br>') for t
    #                  in fig.data[0].y]
    # fig.update_yaxes(tickmode='array', tickvals=list(range(len(nomes_tarefas))), ticktext=nomes_tarefas)
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(title=nomeProjeto)
    file_name = temp_file(nomeArquivo)
    fig.write_html(file=file_name)

    return fig.to_html(include_plotlyjs='cdn')
