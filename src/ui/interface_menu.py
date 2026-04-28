import tkinter as tk

class Menu(tk.Frame):
    def __init__(self, master, ir_para_jogo, ir_para_estatisticas):
        super().__init__(master, bg="#262626")

        tk.Label(self, text="DETONATOR", font=("Arial Black", 40), fg="white", bg="#262626").pack(pady=40)

        tk.Button(self, text="Jogar", font=("Arial Black", 20),
                  command=ir_para_jogo, bg="white", fg="black").pack(pady=10)
        
        tk.Button(self, text="Estatísticas", font=("Arial Black", 20),
                  command=ir_para_estatisticas, bg="white", fg="black").pack(pady=10)

        tk.Button(self, text="Sair", font=("Arial Black", 20),
                  command=master.destroy, bg="white", fg="black").pack(pady=10)