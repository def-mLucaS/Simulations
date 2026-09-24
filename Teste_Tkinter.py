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

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('cpe.offshore.app.1')
except:
    pass


app = Tk()
app.title("CPE-OFFSHORE")
app.geometry("1920x1080")
app.iconbitmap("cpe.ico")

frame_esquerda = ttk.Frame(app)
frame_esquerda.pack(side='left', fill='y', padx=20, pady=20)

ttk.Label(frame_esquerda, text='Escolha a localidade da planta eólica offshore:').pack(anchor='w', pady=2)
opcoes_planta = ['📍 Piedade', '📍 Aracatu', '📍 Mostardas']
planta = ttk.Combobox(frame_esquerda, values=opcoes_planta, width=33, state='readonly')
planta.pack(anchor='w', pady=2)
planta.set(opcoes_planta[0])

ttk.Label(frame_esquerda, text='Informe a quantidade de produção de energia (GW):').pack(anchor='w', pady=2)
PE = Entry(frame_esquerda, width=33)
PE.pack(anchor='w', pady=2)

ttk.Label(frame_esquerda, text='Escolha o laytou do parque:').pack(anchor='w', pady=2)
opcoes_layout = ['Triangulo', 'Quadrado']
layout = ttk.Combobox(frame_esquerda, values=opcoes_layout, width=33, state='readonly')
layout.pack(anchor='w', pady=2)
layout.set(opcoes_layout[0])

botao = ttk.Button(frame_esquerda, text='Escolher', command= lambda: ao_clicar_botao())
botao.pack(anchor='w', pady=2)

resultado_localidade = StringVar()
resultado_PE = StringVar()


label_resultado_planta = ttk.Label(frame_esquerda, textvariable=resultado_localidade, foreground="blue", font=("Arial", 10, "bold"))
label_resultado_planta.pack(anchor = 'w', pady=2)

label_resultado_PE = ttk.Label(frame_esquerda, textvariable=resultado_PE, foreground='blue', font=('Arial', 10, 'bold'))
label_resultado_PE.pack(anchor = 'w', pady=2)


frame_direita = ttk.Frame(app)
frame_direita.pack(side='right', fill='both',expand=True, padx=20, pady=20)

app.mainloop()