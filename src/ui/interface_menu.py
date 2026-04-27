import tkinter as tk

class Menu(tk.Frame):
    def __init__(self, master, ir_para_jogo, ir_para_estatisticas):
        super().__init__(master, bg="white")

        tk.Label(self, text="DETONATOR", font=("Arial Black", 40)).pack(pady=40)

        tk.Button(self, text="Jogar", font=("Arial Black", 20),
                  command=ir_para_jogo).pack(pady=10)
        
        tk.Button(self, text="Estatísticas", font=("Arial Black", 20),
                  command=ir_para_estatisticas).pack(pady=10)

        tk.Button(self, text="Sair", font=("Arial Black", 20),
                  command=master.destroy).pack(pady=10)