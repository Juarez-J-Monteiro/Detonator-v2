import tkinter as tk

from src.ui.interface_menu import Menu
from src.ui.interface_partida import Partida
from src.ui.interface_estatisticas import Estatisticas

root = tk.Tk()
root.geometry("640x600")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# funções de troca de tela
def ir_para_jogo():
    menu.pack_forget()
    partida.iniciarJogo()
    partida.pack(fill="both", expand=True)

def ir_para_estatisticas():
    menu.pack_forget()
    estatisticas.atualizar()
    estatisticas.pack(fill="both", expand=True)

def voltar_menu():
    partida.pack_forget()
    menu.pack(fill="both", expand=True)

def voltar_menu_estatisticas():
    estatisticas.pack_forget()
    menu.pack(fill="both", expand=True)

# cria as telas
menu = Menu(root, ir_para_jogo, ir_para_estatisticas)
partida = Partida(root, voltar_menu)
estatisticas = Estatisticas(root, voltar_menu_estatisticas)

# começa pelo menu
menu.pack(fill="both", expand=True)

root.mainloop()