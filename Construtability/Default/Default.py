import yaml
import os

# Obtém o diretório do arquivo Default.py
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

caminho_custo = os.path.join(diretorio_atual, 'Custos.yaml')
with open(caminho_custo) as file:
    custos = yaml.load(file, Loader=yaml.FullLoader)

caminho_parametros_gerais = os.path.join(diretorio_atual, 'ParametrosGerais.yaml')
with open(caminho_parametros_gerais) as file:
    parametros = yaml.load(file, Loader=yaml.FullLoader)

caminho_tempo_processamento = os.path.join(diretorio_atual, 'TempoProcessamento.yaml')
with open(caminho_tempo_processamento) as file:
    tempo_processamento = yaml.load(file, Loader=yaml.FullLoader)

caminho_guindaste = os.path.join(diretorio_atual, 'Guindaste.yaml')
with open(caminho_guindaste) as file:
    guindaste = yaml.load(file, Loader=yaml.FullLoader)

caminho_embarcacao = os.path.join(diretorio_atual, 'Embarcacao.yaml')
with open(caminho_embarcacao) as file:
    embarcacao = yaml.load(file, Loader=yaml.FullLoader)