import os
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from Routines.TkinterRoutines import OpenFolder, ClickBtn, ChooseAero, Aerodt


app = Tk()
app.title("CPE-OFFSHORE")
app.geometry("1920x1080")
app.iconbitmap("cpe.ico")

frame_esquerda = ttk.Frame(app)
frame_esquerda.pack(side='left', fill='y', padx=20, pady=20)

ttk.Label(frame_esquerda, text='Escolha a localidade da planta eólica offshore', foreground="black", font=("Arial", 10, "bold")).pack(anchor='w', pady=2)
btn_search = ttk.Button(frame_esquerda, text='Procurar KML...', command=lambda: OpenFolder(planta_var))
btn_search.pack(anchor='w', pady=2)

ttk.Label(frame_esquerda, text='Informe a quantidade de produção de energia (GW):', foreground="black", font=("Arial", 10, "bold")).pack(anchor='w', pady=2)
PE = Entry(frame_esquerda, width=33)
PE.pack(anchor='w', pady=2)

ttk.Label(frame_esquerda, text='Escolha o layout do parque:', foreground="black", font=("Arial", 10, "bold")).pack(anchor='w', pady=2)
opcoes_layout = ['Triangulo', 'Quadrado']
layout = ttk.Combobox(frame_esquerda, values=opcoes_layout, font=("Arial", 10), width=33, state='readonly')
layout.pack(anchor='w', pady=2)
layout.set(opcoes_layout[0])

ttk.Label(frame_esquerda, text='Direção dos ventos', foreground="black", font=("Arial", 10, "bold")).pack(anchor='w', pady=2)
direct_winds = ['Norte', 'Nordeste', 'Leste', 'Sudeste', 'Sul', 'Sudoeste', 'Oeste', 'Noroeste']
winds = ttk.Combobox(frame_esquerda, values=direct_winds, foreground="black", font=("Arial", 10), width=33, state='readonly')
winds.pack(anchor='w', pady=2)
winds.set(direct_winds[0])

planta_var = StringVar()
resultado_localidade = StringVar()
resultado_PE = StringVar()

botao = ttk.Button(frame_esquerda, text='Confirmar', command= lambda: ClickBtn(resultado_PE, resultado_localidade ,planta_var, PE))
botao.pack(anchor='w', pady=2)

# --- 1. Rótulo para mostrar a localidade escolhida ---
label_resultado_planta = ttk.Label(
    frame_esquerda, 
    textvariable=planta_var, 
    font=("Arial", 10, "bold"), 
    foreground="#004080"
)
label_resultado_planta.pack(anchor='w', pady=2)


# --- 2. Rótulo para mostrar o porto escolhido ---
label_resultado_localidade = ttk.Label(
    frame_esquerda, 
    textvariable=resultado_localidade, 
    font=("Arial", 10, "bold"), 
    foreground="#004080"
)
label_resultado_localidade.pack(anchor='w', pady=2)

# --- 3. Rótulo para mostrar a energia informada ---
label_resultado_pe = ttk.Label(
    frame_esquerda, 
    textvariable=resultado_PE, 
    font=("Arial", 10, "bold"), 
    foreground="#004080"
)
label_resultado_pe.pack(anchor='w', pady=2)

ttk.Label(frame_esquerda, text='Escolher Aerogerador').pack(anchor='w', pady=15)
aero_btn = ttk.Button(frame_esquerda, text='Escolher', command = lambda: Aerodt(PE,planta_var, container_tabela, frame_botao_direita, tabela))
aero_btn.pack(anchor='w', pady=2)


frame_direita = ttk.Frame(app)
frame_direita.pack(side='right', fill='both',expand=True, padx=20, pady=20, anchor='n')

estilo = ttk.Style(app)
estilo.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

container_tabela = ttk.Frame(frame_direita)
colunas_tabela = ("Modelo", "Quantidade Minima de  Aerogeradores", "Quantidade Maxima de espaço","Custo_Unitario_USD", "Transmissao")
tabela = ttk.Treeview(container_tabela, columns=colunas_tabela, show="headings", height=53)

tabela.heading("Modelo", text="Modelo")
tabela.heading("Numero de Aerogeradores Necessarios", text='Numero de Aerogeradores Necessarios')
tabela.heading("Quantidade Maxima de espaço", text='Quantidade Maxima de espaço')
tabela.heading("Custo_Unitario_USD", text="Custo_Unitario_USD")
tabela.heading("Transmissao", text='Transmissao')

# Configurar a largura e o alinhamento de cada coluna para melhor visualização
tabela.column("Modelo", width=130, anchor="w")
tabela.column("Numero de Aerogeradores Necessarios",width=130, anchor='center')
tabela.column("Quantidade Maxima de espaço", width=130, anchor='center')
tabela.column("Custo_Unitario_USD", width=130, anchor="center")
tabela.column("Transmissao", width=130, anchor='center')

scrollbar = ttk.Scrollbar(frame_direita, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)

tabela.pack(side='left', fill='both', expand=True)
scrollbar.pack(side="right", fill='y')

frame_botao_direita = ttk.Frame(frame_direita)
btn_choose = ttk.Button(
    frame_botao_direita,
    text='Escolher',
    command = lambda: ChooseAero(tabela)
)
btn_choose.pack(side='right', pady=5)

app.mainloop()