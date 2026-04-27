import tkinter as tk

from src.ui.interface_menu import Menu
from src.ui.interface_partida import Partida

root = tk.Tk()
root.geometry("800x600")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# funções de troca de tela
def ir_para_jogo():
    menu.pack_forget()
    partida.pack(fill="both", expand=True)

def voltar_menu():
    partida.pack_forget()
    menu.pack(fill="both", expand=True)

# cria as telas
menu = Menu(root, ir_para_jogo)
partida = Partida(root, voltar_menu)

# começa pelo menu
menu.pack(fill="both", expand=True)

root.mainloop()