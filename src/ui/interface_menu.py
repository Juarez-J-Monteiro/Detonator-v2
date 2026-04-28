import tkinter as tk

class Menu(tk.Frame):
    def __init__(self, master, ir_para_jogo, ir_para_estatisticas):
        super().__init__(master, bg="#262626")

        self.titulo = tk.Label(self, text="DETONATOR", font=("Arial Black", 40), fg="white", bg="#262626")
        self.titulo.pack(pady=40)

        self.botaoJogar = tk.Button(self, text="Jogar", font=("Arial Black", 20),
                  command=ir_para_jogo, bg="white", fg="black")
        self.botaoJogar.pack(pady=10)
        
        self.botaoStats = tk.Button(self, text="Estatísticas", font=("Arial Black", 20),
                  command=ir_para_estatisticas, bg="white", fg="black")
        self.botaoStats.pack(pady=10)

        self.botaoSair = tk.Button(self, text="Sair", font=("Arial Black", 20),
                  command=master.destroy, bg="white", fg="black")
        self.botaoSair.pack(pady=10)

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        largura = event.width
        altura = event.height

        escala = min(largura / 640, altura / 600)

        novoFlexFontBotao = int(20 * escala)
        novoFlexFontTitulo = int(40 * escala)

        # evita fonte muito pequena
        novoFlexFontBotao = max(10, novoFlexFontBotao)
        novoFlexFontTitulo = max(20, novoFlexFontTitulo)

        self.botaoJogar.config(font=("Impact", novoFlexFontBotao))
        self.botaoStats.config(font=("Impact", novoFlexFontBotao))
        self.botaoSair.config(font=("Impact", novoFlexFontBotao))
        self.titulo.config(font=("Impact", novoFlexFontTitulo))