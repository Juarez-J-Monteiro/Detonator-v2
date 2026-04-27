import tkinter as tk
from src.game.jogo import Jogo


class Partida(tk.Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=0)
        # Canvas
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Instancia do motor do jogo
        self.jogo = Jogo()

        # Barra de Informações
        self.barra1 = tk.Frame(self, bg="black", height=60)
        self.barra1.grid(row=1, column=0, sticky="ew")
        self.label_turno = tk.Label(self.barra1, text="Turno: 0/0", fg="white", bg="black", font=("Impact", 18))
        self.label_turno.pack(side="left", padx=10)

        self.barra2 = tk.Frame(self, bg="black", height=60)
        self.barra2.grid(row=2, column=0, sticky="ew")
        self.label_alcanceBombas = tk.Label(self.barra2, text="Alcance da Bomba: " + str(self.jogo.alcanceBomba), 
                                            fg="white", bg="black", font=("Impact", 18))
        self.label_alcanceBombas.pack(side="left", padx=10)
        self.label_tempoDetonacao = tk.Label(self.barra2, text="Tempo de detonação: " + str(self.jogo.tempoDetonacao), 
                                            fg="white", bg="black", font=("Impact", 18))
        self.label_tempoDetonacao.pack(side="left", padx=10)

        self.barra3 = tk.Frame(self, bg="black", height=60)
        self.barra3.grid(row=3, column=0, sticky="ew")
        self.label_proximaDetonacao = tk.Label(self.barra3, 
                                            text="Não há bombas posicionadas", 
                                            fg="white", bg="black", font=("Impact", 18))
        self.label_proximaDetonacao.pack(side="left", padx=10)

        
        # Tamanho
        self.linhas = 13
        self.colunas = 13

        # Posição do jogador
        self.player = [self.jogo.jogador.linhaAtual, self.jogo.jogador.colunaAtual]

        # Input
        self.master.bind("<Key>", self.on_key)

        # Redimensionar
        # self.canvas.bind("<Configure>", self.on_resize)

        self.loop()

    # Input
    def on_key(self, event):
        if event.keysym == "Up":
            self.jogo.atualizarPartida('w')
        elif event.keysym == "Down":
            self.jogo.atualizarPartida('s')
        elif event.keysym == "Left":
            self.jogo.atualizarPartida('a')
        elif event.keysym == "Right":
            self.jogo.atualizarPartida('d')
        elif event.keysym == "b":
            self.jogo.atualizarPartida('b')

    # Atualiza tudo
    def update(self):
        self.label_turno.config(text=f"Turno: {self.jogo.turnos}/{self.jogo.maxTurnos}")
        if len(self.jogo.listaBombas) != 0:
            self.label_proximaDetonacao.config(text=f"Próxima bomba explode em: {self.jogo.listaBombas[0].tempoDetonacao} turnos")
        else:
            self.label_proximaDetonacao.config(text="Não há bombas posicionadas")

    # Renderização
    def desenharMapa(self):
        self.canvas.delete("all")

        largura = self.canvas.winfo_width()
        altura = self.canvas.winfo_height()

        # tamanho do bloco (mantém quadrado)
        tam = min(largura // self.colunas, altura // self.linhas)

        for i in range(self.linhas):
            for j in range(self.colunas):
                x1 = j * tam
                y1 = i * tam
                x2 = x1 + tam
                y2 = y1 + tam

                if self.jogo.mapa.grade[i][j] == '.':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="gray"
                    )
                if self.jogo.mapa.grade[i][j] == '#':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="black"
                    )
                if self.jogo.mapa.grade[i][j] == '$':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="blue"
                    )
                if self.jogo.mapa.grade[i][j] == 'J':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="yellow"
                    )
                if self.jogo.mapa.grade[i][j] == 'I':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="red"
                    )
                if self.jogo.mapa.grade[i][j] == 'B':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="magenta"
                    )
                if self.jogo.mapa.grade[i][j] == 'X':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="white"
                    )

    # Loop
    def loop(self):
        self.update()
        if self.jogo.ehVivo:
            self.desenharMapa()

        # ~60 FPS (16ms)
        self.master.after(16, self.loop)