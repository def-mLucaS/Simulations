import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import textwrap

from ..Cronograma.Tarefa import Tarefa
from ..Cronograma.TipoMicroatividade import TipoMicroatividade
from ....utils.utils import temp_file


class Cronograma:
    def __init__(self, nomeProjeto, dataInicio):
        if not isinstance(dataInicio, datetime):
            raise KeyError("A dataInicio não é do tipo datetime.")
        self.nomeProjeto = nomeProjeto
        self.dataInicio = dataInicio
        self.dataAtual = dataInicio
        self.tarefas = {}
        self.cores = self.setCores()

    def getTarefas(self):
        return self.tarefas

    def getListaTarefas(self):
        df = []
        colors = []
        tipos = list()
        for nomeTarefa in self.tarefas:
            tarefa = self.tarefas[nomeTarefa]
            macroatividades = self.getMacroatividades(nomeTarefa)
            for nomeMacroatividade in macroatividades:
                macroatividade = macroatividades[nomeMacroatividade]
                if not macroatividade.microatividades:
                    continue
                for microatividade in macroatividade.microatividades:
                    df.append(dict(Tarefa=nomeTarefa,
                                   Tipo=microatividade.tipo.value,
                                   Macroatividade=macroatividade.nome,
                                   Microatividade=microatividade.nome,
                                   Start=microatividade.dataInicio,
                                   Finish=microatividade.dataFim))
                    if microatividade.tipo not in tipos:
                        tipos.append(microatividade.tipo)
                        colors.append(self.cores[microatividade.tipo])
        return df

    def setDataAtual(self, dataAtual):
        self.dataAtual = dataAtual

    def getDataAtual(self):
        return self.dataAtual

    def adicionarTarefa(self, nomeTarefa):
        if nomeTarefa not in self.tarefas:
            self.tarefas[nomeTarefa] = Tarefa(nomeTarefa)

    def adicionarMacroatividade(self, nomeTarefa, nomeMacroatividade):
        if nomeTarefa in self.tarefas:
            self.tarefas[nomeTarefa].adicionarMacroatividade(
                nomeMacroatividade)
        else:
            raise KeyError("A chave consultada não está na lista de tarefas.")

    def adicionarMicroatividade(self, nomeTarefa, nomeMacroatividade, nomeMicroatividade, tipo, duracao):
        if not nomeTarefa in self.tarefas:
            raise KeyError("A chave consultada não está na lista de tarefas.")
        elif not nomeMacroatividade in self.getMacroatividades(nomeTarefa):
            raise KeyError(
                "A chave consultada não está na lista de macroatividades.")
        else:
            self.tarefas[nomeTarefa].macroatividades[nomeMacroatividade].adicionarMicroatividade(
                nomeMicroatividade, tipo, duracao)

    def getMacroatividades(self, nomeTarefa):
        if nomeTarefa in self.tarefas:
            return self.tarefas[nomeTarefa].macroatividades
        else:
            raise KeyError("A chave consultada não está na lista de tarefas.")

    def getDataFimMacroatividade(self, nomeTarefa, nomeMacroatividade):
        macroatividade = self.getMacroatividades(
            nomeTarefa)[nomeMacroatividade]
        return macroatividade.dataFim

    def executarMacroatividade(self, nomeTarefa, nomeMacroatividade, dataInicio):
        if not isinstance(dataInicio, datetime):
            raise KeyError("A dataInicio não é do tipo datetime.")
        if not nomeTarefa in self.tarefas:
            raise KeyError("A chave consultada não está na lista de tarefas.")
        elif not nomeMacroatividade in self.getMacroatividades(nomeTarefa):
            raise KeyError(
                "A chave consultada não esta na lista de macroatividades.")
        else:
            self.tarefas[nomeTarefa].macroatividades[nomeMacroatividade].executarAtividades(
                dataInicio)

    def setCores(self):
        colors = dict()
        # cinza escuro
        colors[TipoMicroatividade.TRANSPORTE_CARREGAMENTO] = "#DAA520"
        colors[TipoMicroatividade.PORTO] = "#1616A7"  # azul royal
        colors[TipoMicroatividade.TRANSPORTE_FRETE] = "#EB663B"
        colors[TipoMicroatividade.TRANSBORDO] = "black",
        colors[TipoMicroatividade.TRANSPORTE_INSTALACAO] = "#FD8686"
        colors[TipoMicroatividade.INTERRUPCAO_DE_OPERACAO] = 'red'
        colors[TipoMicroatividade.INSTALACAO_FUNDACAO] = "#FC0080"  # pink
        colors[TipoMicroatividade.INSTALACAO_AEROGERADOR] = 'green'
        colors[TipoMicroatividade.INSTALACAO_ENROCAMENTO] = '#862A16'
        # verde turquesa
        colors[TipoMicroatividade.INSTALACAO_SUBESTACAO] = "#00A08B",
        colors[TipoMicroatividade.INSTALACAO_SISTEMA_ARRAY] = 'purple'
        colors[TipoMicroatividade.INSTALACAO_CABOS_EXPORTACAO] = "#6C7C32"
        colors[TipoMicroatividade.ESPERA] = '#778AAE'

        # "#2E91E5", #azul
        # "#E15F99", #rosa
        # "#1CA71C", #verde grama
        # "#FB0D0D", #vermelho
        # "#FD8686", #vermelho suave
        # "#222A2A", #cinza escuro
        # "#750D86", #roxo
        # "#EB663B", #laranja claro
        # "#511CFB", #azul roxo
        # "#00A08B", #verde turquesa
        # "#FC0080", #pink
        # "#B2828D", #marrom claro
        # "#6C7C32", #verde musgo
        # "#778AAE", #cinza claro
        # "#862A16", #marrom escuro
        # "#620042", #vinho
        # "#1616A7", #azul royal
        # "#0D2A63", #azul escuro
        # "#AF0038"  #vermelho escuro
        # "#DAA520", "dourado"
        return colors

    def obterGraficoGantt(self, nomeArquivo):
        df = []
        cores = {}
        tipos = set()  # Usar um set para evitar duplicatas
        for nomeTarefa in self.tarefas:
            tarefa = self.tarefas[nomeTarefa]
            macroatividades = self.getMacroatividades(nomeTarefa)
            for nomeMacroatividade in macroatividades:
                macroatividade = macroatividades[nomeMacroatividade]
                if not macroatividade.microatividades:
                    continue
                for microatividade in macroatividade.microatividades:
                    df.append(dict(Tarefa=nomeTarefa,
                                   Tipo=microatividade.tipo.value,
                                   Macroatividade=macroatividade.nome,
                                   Microatividade=microatividade.nome,
                                   Start=microatividade.dataInicio,
                                   Finish=microatividade.dataFim))
                    if microatividade.tipo not in cores:
                        cores[microatividade.tipo.value] = self.cores[microatividade.tipo]
                        tipos.add(microatividade.tipo)

        lista_cron = df

        df = pd.DataFrame(df)
        df = df.rename({"Tarefa": "Viagens", "Tipo": "Tipo", "Macroatividade": "Macroatividade",
                        "Microatividade": "Microatividade", "Start": "Inicio", "Finish": "Fim"}, axis=1)

        # Ordena o DataFrame pela data de início (Inicio)
        df = df.sort_values(by="Inicio")

        # Define a coluna 'Viagens' como uma categoria ordenada de acordo com a data de início
        df['Viagens'] = pd.Categorical(
            df['Viagens'], categories=df['Viagens'].unique(), ordered=True)

        # Recria a lista de cores em ordem de tipos no DataFrame
        colors = [cores[tipo] for tipo in df['Tipo'].unique()]

        # Agora cria o gráfico Gantt com a ordenação correta
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
        fig.update_layout(title=self.nomeProjeto)
        file_name = temp_file(nomeArquivo)
        fig.write_html(file=file_name)

        # Agora cria o gráfico Gantt com a ordenação correta
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
        fig.update_layout(title=self.nomeProjeto)
        file_name = temp_file(nomeArquivo)
        fig.write_html(file=file_name)

        config = [lista_cron, colors, self.nomeProjeto]

        return fig.to_html(include_plotlyjs='cdn'), config

    def obterGraficoGantt2(self, df, nomeArquivo):
        colors = []
        tipos = list()
        for k in df:
            if k['Tipo'] not in tipos:
                for t in (TipoMicroatividade):
                    if k['Tipo'] == t.value:
                        tipos.append(k['Tipo'])
                        colors.append(self.cores[t])
                        
        lista_cron = df

        df = pd.DataFrame(df)
        # colors[2] = '#EB663B'
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
        fig.update_layout(title=self.nomeProjeto)
        file_name = temp_file(nomeArquivo)
        fig.write_html(file=file_name)

        config = [lista_cron, colors, self.nomeProjeto]

        return fig.to_html(include_plotlyjs='cdn'), config
