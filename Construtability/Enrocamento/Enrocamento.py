from haversine import haversine
import re
import math
from datetime import timedelta
import copy


def Enrocamento(porto, parque, volume, cronograma, fundacao, fallpipes, instaladoras):

    tipo_fundacao = fundacao

    fallpipe_vessels = fallpipes.embarcacoes
    lista_fallpipes = list(fallpipe_vessels.keys())

    lista_inst = instaladoras.getListaInstaladoras()
    lista_tarefas = cronograma.getListaTarefas()

    qtd_instaladoras = len(lista_inst)

    print(f'Volume Total Enrocamento: {volume}m³')

    coord_porto = (porto.getLatitude(), porto.getLongitude())
    densidade_cascalho_rocha_seco = 1.5  # t/m³

    qtd_fallpipe = len(fallpipe_vessels)

    if fundacao == "subestacao":

        qtd_sub = len(parque.getPontos())
        print(f'Número de Subestações: {qtd_sub}')
        print(
            f'Volume total de Cascalho para subestações: {volume*qtd_sub}m³')
        print(f'Volume de Cascalho por subestação: {volume}m³')
        volume_sub = volume
        v_por_emb = volume_sub/qtd_fallpipe

        lista_dict_ids = list()
        dict_ids = dict()
        for k in lista_tarefas:
            if tipo_fundacao == "subestacao":
                if k['Tipo'] == 'Instalação de fundação' \
                        and k['Microatividade'] == 'Reequipar o equipamento de elevação':
                    string_emb = k['Tarefa'].split(" ")
                    dict_ids = {
                        'Tarefa': string_emb[0],
                        'Macroatividade': k['Macroatividade'],
                        'Turbina Instalada': re.findall('\d+', k['Macroatividade'])[0],
                        'Viagem': re.findall('\d+', k['Macroatividade'])[1],
                        'Finish': k['Finish']
                    }
                    lista_dict_ids.append(dict_ids)

        lista_numturb = []
        for f in fallpipe_vessels:
            max_turb_emb = fallpipe_vessels[f].getCapacidadeMax()/volume_sub
            lista_numturb.append(math.floor(max_turb_emb))

    if fundacao == "monopile" or fundacao == "gravidade" or fundacao == "jaqueta":
        qtd_turbinas = len(parque.getPlanta().getPontos())
        lista_dict_ids = list()
        dict_ids = dict()
        for k in lista_tarefas:
            if tipo_fundacao == "gravidade":
                if k['Tipo'] == 'Instalação de fundação' \
                        and k['Microatividade'] == 'Fixar gravidade no fundo do mar com argamassa':
                    string_emb = k['Tarefa'].split(" ")
                    dict_ids = {
                        'Tarefa': string_emb[0],
                        'Macroatividade': k['Macroatividade'],
                        'Turbina Instalada': re.findall('\d+', k['Macroatividade'])[0],
                        'Viagem': re.findall('\d+', k['Macroatividade'])[1],
                        'Finish': k['Finish']
                    }
                    lista_dict_ids.append(dict_ids)

            if tipo_fundacao == "jaqueta" or tipo_fundacao == "monopile":
                if k['Tipo'] == 'Instalação de fundação' \
                    and (k['Microatividade'] == 'Cura da argamassa'
                         or k['Microatividade'] == 'Parafusar peça de transição na monopile'
                         or k['Microatividade'] == 'Parafusar peca de transição na jaqueta'):
                    string_emb = k['Tarefa'].split(" ")
                    dict_ids = {
                        'Tarefa': string_emb[0],
                        'Macroatividade': k['Macroatividade'],
                        'Turbina Instalada': re.findall('\d+', k['Macroatividade'])[0],
                        'Viagem': re.findall('\d+', k['Macroatividade'])[1],
                        'Finish': k['Finish']
                    }
                    lista_dict_ids.append(dict_ids)

        volume_turbina = volume/qtd_turbinas
        v_por_emb = volume_turbina/qtd_fallpipe

        # Calcular o número máximo de turbinas por fallpipe
        lista_numturb = []
        for f in fallpipe_vessels:
            max_turb_emb = fallpipe_vessels[f].getCapacidadeMax(
            )/volume_turbina
            lista_numturb.append(math.floor(max_turb_emb))

    # Lista com ordem das turbinas instaladas no lista_tarefas

    i = 0
    lista_ids_inst = []
    while i < qtd_instaladoras:
        lista_ids_inst.append(i)
        i += 1

    dict_turb = {}
    for i in range(len(lista_ids_inst)):
        dict_turb.update({lista_ids_inst[i]: []})

    i = 0
    while i < qtd_instaladoras:
        for k in lista_dict_ids:
            if k['Tarefa'] == lista_inst[i]:
                dict_turb[i].append(
                    int(re.findall('\d+', k['Macroatividade'])[0]))
        i += 1

    # Lista horários

    i = 0
    lista_ids_inst = []
    while i < qtd_instaladoras:
        lista_ids_inst.append(i)
        i += 1

    dict_tempos = {}
    for i in range(len(lista_ids_inst)):
        dict_tempos.update({lista_ids_inst[i]: []})

    i = 0
    while i < qtd_instaladoras:
        for k in lista_dict_ids:
            if k['Tarefa'] == lista_inst[i]:
                dict_tempos[i].append(k["Finish"])
        i += 1

    # Designa as turbinas-destino para cada fallpipe

    dict_destino = {}
    dict_tempos_fp = {}
    list_dict_tarefa = []

    if qtd_fallpipe > qtd_instaladoras:

        dict_destino = copy.deepcopy(dict_turb)
        dict_tempos_fp = copy.deepcopy(dict_tempos)

        fps_extras = qtd_fallpipe - qtd_instaladoras

        i = 0
        while i < fps_extras:
            viagem = 1
            fallpipe = lista_fallpipes[qtd_instaladoras + i]
            partida = "porto"
            destino = "porto"
            tipo = "espera"
            tempo_inicio = dict_tempos_fp[0][0]
            tempo_deslocamento = 0
            tempo_final = dict_tempos_fp[qtd_instaladoras-1][-1]

            list_dict_tarefa.append({
                "Viagem": viagem,
                "Fallpipe": fallpipe,
                "Partida": partida,
                "Destino": destino,
                "Tipo": tipo,
                "Tempo Início": tempo_inicio,
                "Tempo Deslocamento": tempo_deslocamento,
                "Tempo Final": tempo_final
            })
            i += 1

    if qtd_fallpipe == qtd_instaladoras:

        dict_destino = copy.deepcopy(dict_turb)
        dict_tempos_fp = copy.deepcopy(dict_tempos)

    if qtd_fallpipe < qtd_instaladoras:

        i = 0
        lista_ids_fp = []
        while i < qtd_fallpipe:
            lista_ids_fp.append(i)
            i += 1

        for i in range(len(lista_ids_fp)):
            dict_tempos_fp.update({lista_ids_fp[i]: []})

        for i in range(len(lista_ids_fp)):
            dict_destino.update({lista_ids_fp[i]: []})

        idx_range = math.floor(qtd_turbinas/qtd_fallpipe)
        resto = qtd_turbinas % qtd_fallpipe

        lista_tempos_fp = []
        lista_turbs_fp = []

        for k in dict_tempos:
            for tempo in dict_tempos[k]:
                lista_tempos_fp.append(tempo)

        for k in dict_turb:
            for turb in dict_turb[k]:
                lista_turbs_fp.append(turb)

        Y = lista_tempos_fp
        X = lista_turbs_fp

        lista_turbs_fp = [x for _, x in sorted(zip(Y, X))]
        lista_tempos_fp.sort()

        i = 0
        j = idx_range + resto
        for k in dict_tempos_fp:
            dict_tempos_fp[k] = lista_tempos_fp[i:j]
            i = idx_range + resto
            j = qtd_turbinas - i

        i = 0
        j = idx_range + resto
        for k in dict_destino:
            dict_destino[k] = lista_turbs_fp[i:j]
            i = idx_range + resto
            j = qtd_turbinas - i

    else:
        pass

    # Designa o momento de voltar ao porto para encher de pedra

    dict_destino_original = copy.deepcopy(dict_destino)

    for k in dict_destino:
        i = 0
        j = 0
        if lista_numturb[k] > 0:
            while i < len(dict_destino_original[k]):
                if i % lista_numturb[k] == (lista_numturb[k] - 1):
                    j += 1
                    dict_destino[k].insert(i+j, "porto")
                i += 1
        else:
            # erro
            pass

    # Designa Dict Partida

    dict_partida = {}
    lista_ids_tempos_inicio = []
    dict_partida = copy.deepcopy(dict_destino)
    for k in dict_destino:
        lista_ids_tempos_inicio.append(dict_partida[k][0])
        dict_partida[k].insert(0, "porto")
        dict_partida[k] = dict_partida[k][:-1]

    lista_tempos_inicio = []
    for id in lista_ids_tempos_inicio:
        for tarefa in lista_dict_ids:
            if id == int(tarefa["Turbina Instalada"]):
                lista_tempos_inicio.append(tarefa["Finish"])

    # Construir dicionário das tarefas

    for k in dict_partida:
        viagem = 0
        fallpipe = lista_fallpipes[k]
        vel_carregado = fallpipe_vessels[lista_fallpipes[k]
                                         ].getVelocidadeCarregado()
        vel_vazio = fallpipe_vessels[lista_fallpipes[k]].getVelocidadeVazio()
        fallpipe_vessels[lista_fallpipes[k]].tempo_tacar_pedra = (
            v_por_emb*densidade_cascalho_rocha_seco)/fallpipe_vessels[f].getCapacidadeInstalacao()

        tempo_inicio_lst = dict_tempos_fp[k][0]

        for idx, turb in enumerate(dict_destino[k]):
            partida = dict_partida[k][idx]
            destino = turb
            index = idx

            if partida == "porto":
                tipo = "porto para turbina"
                if tipo_fundacao == "subestacao":
                    dist_deslocamento = haversine(coord_porto,
                                                  parque.getCoordenadas(destino))
                else:
                    dist_deslocamento = haversine(coord_porto,
                                                  parque.getPlanta().getCoordenadas(destino))

                tempo_deslocamento = dist_deslocamento/vel_carregado

                if index == 0:
                    tempo_inicio = tempo_inicio_lst - \
                        timedelta(hours=tempo_deslocamento)
                else:
                    tempo_inicio = tempo_inicio_lst

                tempo_final = tempo_inicio + \
                    timedelta(hours=tempo_deslocamento)
                tempo_final_espera = tempo_final
                viagem += 1

            if destino == "porto":
                tipo = "turbina para porto"
                if tipo_fundacao == "subestacao":
                    dist_deslocamento = haversine(coord_porto,
                                                  parque.getCoordenadas(partida))
                else:
                    dist_deslocamento = haversine(parque.getPlanta().getCoordenadas(partida),
                                                  coord_porto)
                tempo_deslocamento = dist_deslocamento/vel_vazio
                tempo_inicio = tempo_inicio_lst
                tempo_final = tempo_inicio + \
                    timedelta(hours=tempo_deslocamento)

            if partida != "porto" and destino != "porto":
                tipo = "turbina para turbina"
                if tipo_fundacao == "subestacao":
                    dist_deslocamento = haversine(parque.getCoordenadas(partida),
                                                  parque.getCoordenadas(destino))
                else:
                    dist_deslocamento = haversine(parque.getPlanta().getCoordenadas(partida),
                                                  parque.getPlanta().getCoordenadas(destino))
                tempo_deslocamento = dist_deslocamento/vel_carregado
                tempo_inicio = tempo_inicio_lst
                tempo_final = tempo_inicio + \
                    timedelta(hours=tempo_deslocamento)
                tempo_final_espera = tempo_final

            list_dict_tarefa.append({
                "Viagem": viagem,
                "Fallpipe": fallpipe,
                "Partida": partida,
                "Destino": destino,
                "Tipo": tipo,
                "Tempo Início": tempo_inicio,
                "Tempo Deslocamento": tempo_deslocamento,
                "Tempo Final": tempo_final
            })

            if destino != "porto" and tempo_final_espera != dict_tempos_fp[k][dict_destino_original[k].index(turb)]:
                tipo = "espera"
                tempo_inicio = tempo_final_espera
                tempo_final = dict_tempos_fp[k][dict_destino_original[k].index(
                    turb)]
                tempo_deslocamento = 0
                partida = destino

                list_dict_tarefa.append({
                    "Viagem": viagem,
                    "Fallpipe": fallpipe,
                    "Partida": partida,
                    "Destino": destino,
                    "Tipo": tipo,
                    "Tempo Início": tempo_inicio,
                    "Tempo Deslocamento": tempo_deslocamento,
                    "Tempo Final": tempo_final
                })

            if destino != "porto":
                partida = destino
                tipo = "instalação"
                tempo_deslocamento = fallpipe_vessels[lista_fallpipes[k]].getTempoTacarPedra(
                )
                tempo_inicio = dict_tempos_fp[k][dict_destino_original[k].index(
                    turb)]
                tempo_final = tempo_inicio + \
                    timedelta(hours=tempo_deslocamento)

                list_dict_tarefa.append({
                    "Viagem": viagem,
                    "Fallpipe": fallpipe,
                    "Partida": partida,
                    "Destino": destino,
                    "Tipo": tipo,
                    "Tempo Início": tempo_inicio,
                    "Tempo Deslocamento": tempo_deslocamento,
                    "Tempo Final": tempo_final
                })

            else:
                pass

            tempo_inicio_lst = tempo_final

    # fazer lista_tarefas

    if tipo_fundacao == "subestacao":
        for tarefa in list_dict_tarefa:
            if tarefa["Tipo"] == "porto para turbina" or tarefa["Tipo"] == "turbina para turbina":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Deslocamento para instalação',
                    'Macroatividade': f'Deslocamento embarcação até a subestação {tarefa["Destino"]} para instalação',
                    'Microatividade': f'Deslocar ate a subestação {tarefa["Destino"]} na posição {parque.getCoordenadas(int(tarefa["Destino"]))}',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }

            if tarefa["Tipo"] == "espera":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Em espera',
                    'Macroatividade': f'Embarcação em espera desde {tarefa["Tempo Início"]}',
                    'Microatividade': f'Esperando término da instalação da fundação',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }

            if tarefa["Tipo"] == "instalação":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Instalação do enrocamento',
                    'Macroatividade': f'Instalação do enrocamento para a subestação de ID {tarefa["Destino"]}',
                    'Microatividade': 'Proteger o lastro com cascalho',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }
            if tarefa["Tipo"] == "turbina para porto":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Deslocamento do parque até o porto para carregar',
                    'Macroatividade': f'Instalação do enrocamento para a subestação de ID {tarefa["Partida"]}',
                    'Microatividade': f'Deslocar até o porto de coordenadas {coord_porto}',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }

            lista_tarefas.append(d)

    else:
        for tarefa in list_dict_tarefa:
            if tarefa["Tipo"] == "porto para turbina" or tarefa["Tipo"] == "turbina para turbina":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Deslocamento para instalação',
                    'Macroatividade': f'Deslocamento embarcação até a turbina {tarefa["Destino"]} para instalação',
                    'Microatividade': f'Deslocar ate a turbina {tarefa["Destino"]} na posição {parque.getPlanta().getCoordenadas(int(tarefa["Destino"]))}',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }

            if tarefa["Tipo"] == "espera":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Em espera',
                    'Macroatividade': f'Embarcação em espera desde {tarefa["Tempo Início"]}',
                    'Microatividade': f'Esperando término da instalação da fundação',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }

            if tarefa["Tipo"] == "instalação":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Instalação do enrocamento',
                    'Macroatividade': f'Instalação do enrocamento para a turbina de ID {tarefa["Destino"]}',
                    'Microatividade': 'Proteger o lastro com cascalho',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }
            if tarefa["Tipo"] == "turbina para porto":
                d = {
                    'Tarefa': f'{tarefa["Fallpipe"]} - Viagem {tarefa["Viagem"]}',
                    'Tipo': 'Deslocamento do parque até o porto para carregar',
                    'Macroatividade': f'Instalação do enrocamento para a turbina de ID {tarefa["Partida"]}',
                    'Microatividade': f'Deslocar até o porto de coordenadas {coord_porto}',
                    'Start': tarefa["Tempo Início"],
                    'Finish': tarefa["Tempo Final"]
                }

            lista_tarefas.append(d)

    return lista_tarefas
