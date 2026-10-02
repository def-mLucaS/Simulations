import pandas as pd
import numpy as np
import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from Routines.KML import LoadKML, NearestPort
from Wind_Turbines.Tasks import CountAero
from pathlib import Path


def OpenFolder(planta_var):

    global kml_path_selected

    user_home = os.path.expanduser("~")
    init_path = os.path.join(user_home,"Downloads", "DOWNLOADS - LUCAS", "PIBIT","Simulations", "Datasets")

    if not os.path.exists(init_path):
        messagebox.showerror("Error", "A pasta de dados com as localidades não existe")
    
    selected_archive = filedialog.askopenfilename(
        initialdir=init_path,
        title="Selecione a localidade",
        filetypes=[("Arquivos KML", "*.kml"), ("Todos os arquivos", '*.*')]
        )
    if selected_archive:
        archive_name = os.path.basename(selected_archive)
        planta_var.set(archive_name)
        global kml_path_selected
        kml_path_selected = selected_archive

def ClickBtn(resultado_PE, resultado_localidade, planta_var, PE):

    valor_pe = PE.get()
    nome_kml = planta_var.get()
    
    resultado_localidade.set(f"Localidade escolhida: {nome_kml}")
    resultado_PE.set(f"Produção de energia: {valor_pe} GW")

    NearestPort(LoadKML(planta_var.get()), resultado_localidade)

def ChooseAero(tabela, event=None):

    item_selected = tabela.selection()

    if not item_selected:
        return 

    dt_linha = tabela.item(item_selected, "values")

    if dt_linha == 'Modelo' or dt_linha == 'Custo_Unitario_USD' or dt_linha == 'Transmissao':
            return 

    resp = messagebox.askyesno("Confirmação",
            "Deseja selecionar o Aerogerador?\nEle será utilizado em todo o projeto.")
    if resp:
        messagebox("Aerogerador Selecionador")
        global aero_selected
        aero_selected = dt_linha
    else:
        print("Seleção Cancelada")

def Aerodt(energy_desired, planta_var, container, frame, tabela):

    valor_pe = energy_desired.get().replace(",", ".")
    valor_pe = float(valor_pe)

    coords = LoadKML(planta_var.get())

    if coords is None:
        messagebox.showerror("Erro", "A função LoadKML retornou Vazio (None). Verifique o conteúdo do arquivo KML selecionado.")
        return

    df_calc = CountAero(coords, valor_pe)
    
    # 3. Atualiza a interface (mostra o container e o frame)
    container.pack(fill="both", expand=False, pady=5)
    frame.pack(fill='x', pady=5)
    
    # 4. Limpa a tabela antiga
    for item in tabela.get_children():
        tabela.delete(item)
        
    # 5. Insere as linhas atualizadas
    for _, row in df_calc.iterrows():
        tabela.insert(
            "", 
            "end", 
            values=(
                row["Modelo"],
                row['Numero de Aerogeradores Necessarios'],
                row['Quantidade Maxima de espaço'],
                row["Custo_Unitario_USD"],
                row['Transmissao']
            )
        )