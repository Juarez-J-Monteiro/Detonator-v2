import tkinter as tk
from src.game.estado import EstadoPersistente  # ajusta o import

class Estatisticas(tk.Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master, bg="#262626")

        self.estado = EstadoPersistente()

        self.label = tk.Label(
            self,
            text=self.estado.exibir(),
            font=("Impact", 19),
            justify="left",
            bg="#262626",
            fg="white"
        )
        self.label.pack(pady=40)
        
        self.botaoVoltar = tk.Button(self, text="Voltar", command=voltar_callback, font=("Impact", 19))
        self.botaoVoltar.pack()

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        largura = event.width
        altura = event.height

        escala = min(largura / 640, altura / 600)

        novoFlexFontTexto = int(19 * escala)
        novoFlexFontBotao = int(19 * escala)

        # evita fonte muito pequena
        novoFlexFontTexto = max(8, novoFlexFontTexto)
        novoFlexFontBotao = max(9, novoFlexFontBotao)

        self.label.config(font=("Impact", novoFlexFontTexto))
        self.botaoVoltar.config(font=("Impact", novoFlexFontBotao))

    def atualizar(self):
        self.estado = EstadoPersistente()
        self.estado.carregar()
        self.label.config(text=self.estado.exibir())