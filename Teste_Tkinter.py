import os
import geopandas as gpd
import pandas as pd
import numpy as np
import ctypes
from tkinter import *
from tkinter import ttk
from scipy.spatial import cKDTree
from Routines.KML import LoadKML, NearestPort

def ao_clicar_botao():
    # 1. Pega o valor da energia digitado e atualiza a segunda frase azul
    valor_pe = PE.get()
    resultado_PE.set(f"Produção de energia em(GW): {valor_pe}")
    
    # 2. Executa o cálculo do porto mais próximo
    NearestPort(LoadKML(planta.get()))

app = Tk()
app.title("CPE-OFFSHORE")
app.geometry("1920x1080")
app.iconbitmap("cpe.ico")

frame_esquerda = ttk.Frame(app)
frame_esquerda.pack(side='left', fill='y', padx=20, pady=20)

ttk.Label(frame_esquerda, text='Escolha a localidade da planta eólica offshore:').pack(anchor='w', pady=2)
opcoes_planta = ['CE-26 Piedade.kml', 'RJ-02 Aracatu', 'RS-26 Mostardas']
planta = ttk.Combobox(frame_esquerda, values=opcoes_planta, width=33, state='readonly')
planta.pack(anchor='w', pady=2)
planta.set(opcoes_planta[0])

ttk.Label(frame_esquerda, text='Informe a quantidade de produção de energia (GW):').pack(anchor='w', pady=2)
PE = Entry(frame_esquerda, width=33)
PE.pack(anchor='w', pady=2)

ttk.Label(frame_esquerda, text='Escolha o layout do parque:').pack(anchor='w', pady=2)
opcoes_layout = ['Triangulo', 'Quadrado']
layout = ttk.Combobox(frame_esquerda, values=opcoes_layout, width=33, state='readonly')
layout.pack(anchor='w', pady=2)
layout.set(opcoes_layout[0])

ttk.Label(frame_esquerda, text='Direção dos ventos').pack(anchor='w', pady=2)
direct_winds = ['Norte', 'Nordeste', 'Leste', 'Sudeste', 'Sul', 'Sudoeste', 'Oeste', 'Noroeste']
winds = ttk.Combobox(frame_esquerda, values=direct_winds, width=33, state='readonly')
winds.pack(anchor='w', pady=2)
winds.set(direct_winds[0])

botao = ttk.Button(frame_esquerda, text='Confirmar', command= lambda: ao_clicar_botao())
botao.pack(anchor='w', pady=2)

resultado_localidade = StringVar()
resultado_PE = StringVar()


label_resultado_planta = ttk.Label(frame_esquerda, textvariable=resultado_localidade, foreground="black", font=("Arial", 10, "bold"))
label_resultado_planta.pack(anchor = 'w', pady=2)

label_resultado_PE = ttk.Label(frame_esquerda, textvariable=resultado_PE, foreground="black", font=('Arial', 10, 'bold'))
label_resultado_PE.pack(anchor = 'w', pady=2)

frame_direita = ttk.Frame(app)
frame_direita.pack(side='right', fill='both',expand=True, padx=20, pady=20, anchor='n')

colunas_tabela = ("Modelo", "Custo_Unitario_USD", "Transmissao")

container_tabela = ttk.Frame(frame_direita)

tabela = ttk.Treeview(container_tabela, columns=colunas_tabela, show="headings", height=15)

tabela.heading("Modelo", text="Modelo")
tabela.heading("Custo_Unitario_USD", text="Custo_Unitario_USD")
tabela.heading("Transmissao", text='Transmissao')

# Configurar a largura e o alinhamento de cada coluna para melhor visualização
tabela.column("Modelo", width=180, anchor="w")
tabela.column("Custo_Unitario_USD", width=180, anchor="center")
tabela.column("Transmissao", width=180, anchor='center')

scrollbar = ttk.Scrollbar(frame_direita, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)


tabela.pack(side='left', fill='both', expand=True)
scrollbar.pack(side="right", fill='y')

def Aerodt(aero_dt):

    container_tabela.pack(fill="both", expand=True, pady=5)

    for item in tabela.get_children():
        tabela.delete(item)
        
    # Inserir cada linha calculada do DataFrame na tabela do Tkinter
    for _, row in aero_dt.iterrows():
        tabela.insert(
            "", 
            "end", 
            values=(
                row["Modelo"], 
                row["Custo_Unitario_USD"],
                row['Transmissao'] 
            )
        )

pt = pd.read_csv("C:\\Users\\l08769\\Downloads\\aerogeradores_tratado_com_custo.csv")

ttk.Label(frame_esquerda, text='Escolher Aerogerador').pack(anchor='w', pady=(0,2))
aero_btn = ttk.Button(frame_esquerda, text='Escolher', command = lambda: Aerodt(pt))
aero_btn.pack(anchor='w', pady =2)


app.mainloop()