from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os 
from Routines.KML import LoadKML, NearestPort


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

def ClickBtn(resultado_PE, planta_var):
    # 1. Pega o valor da energia digitado e atualiza a segunda frase azul
    valor_pe = PE.get()
    resultado_PE.set(f"Produção de energia em(GW): {valor_pe}")
    
    # 2. Executa o cálculo do porto mais próximo
    NearestPort(LoadKML(planta_var.get()))

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

def Aerodt(aero_dt, container, frame, tabela):

    container.pack(fill="both", expand=False, pady=5)
    frame.pack(fill='x', pady=5)

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