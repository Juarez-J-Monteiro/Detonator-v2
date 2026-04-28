import tkinter as tk
from src.game.estado import EstadoPersistente  # ajusta o import

class Estatisticas(tk.Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master, bg="#262626")

        self.estado = EstadoPersistente()

        self.label = tk.Label(
            self,
            text=self.estado.exibir(),
            font=("Impact", 20),
            justify="left",
            bg="#262626",
            fg="white"
        )
        self.label.pack(pady=40)
        
        tk.Button(self, text="Voltar", command=voltar_callback, font=("Impact", 20)).pack()

    def atualizar(self):
        self.estado = EstadoPersistente()
        self.estado.carregar()
        self.label.config(text=self.estado.exibir())