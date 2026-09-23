from ...constraint.constraint import find_availability


def previsaoClima(solucaoEmbarcacao, params_constrain):

    resultado_dict = {}

    for key, embarcacao in solucaoEmbarcacao.getDicionarioEmbarcacoes().items():
        resultado_dict[embarcacao.getNome()] = {
            "ondas": embarcacao.getMaxAlturaOnda(),
            "vento": embarcacao.getMaxVelocidadeVento()
        }

    resumo, _ = find_availability(params_constrain["point_coast"],
                                  params_constrain["polygon"][0],
                                  resultado_dict)

    dict_resumo = {}
    for emb in resumo:
        lista_horas = []
        for mes in resumo[emb]:
            lista_horas.append(resumo[emb][mes])
        dict_resumo[emb] = lista_horas

    i = 0
    lista_mes = []
    while i < 12:
        lista_maior = []
        for emb in dict_resumo:
            lista_maior.append(dict_resumo[emb][i])
        dias_mes = max(lista_maior)
        lista_mes.append(dias_mes)
        i += 1

    resumo = lista_mes

    return resumo
