import tkinter as tk
from src.game.jogo import Jogo


class Partida(tk.Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master, bg="#262626")
        
        # Instancia do motor do jogo
        self.jogo = Jogo()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=0)
        # Canvas
        self.canvas = tk.Canvas(self, bg="#262626")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.estadoExecucao = 'Executando' #'Excutando', 'Pausa' ou 'Finalizado'.

        # Tamanho das fontes
        flexFontLegenda = 16
        flexFontInfo = 18
        flexFontBotao = 18
        flexFontMenu = 26
        flexFontStatus = 22

        # Barra inferior de informações
        self.barra1 = tk.Frame(self, bg="#262626", height=60)
        self.barra1.grid(row=1, column=0, sticky="ew")
        self.label_turno = tk.Label(self.barra1, text="Turno: 0/0", fg="white", bg="#262626", font=("Impact", flexFontInfo))
        self.label_turno.pack(side="left", padx=4)
        self.quadradoBomba = tk.Label(self.barra1, bg="magenta", width=2, height="1")
        self.quadradoBomba.pack(side="right", padx=5)
        self.textoBomba = tk.Label(self.barra1, font=("Impact", flexFontLegenda), text="Bomba", fg="white", bg="#262626")
        self.textoBomba.pack(side="right", padx=2)


        self.barra2 = tk.Frame(self, bg="#262626", height=60)
        self.barra2.grid(row=2, column=0, sticky="ew")
        self.label_inimigosRestantes = tk.Label(self.barra2, text="0 inimigo(s) restante(s)",fg="white", bg="#262626", font=("Impact", flexFontInfo))
        self.label_inimigosRestantes.pack(side="left", padx=8)
        self.quadradoLocalMorte = tk.Label(self.barra2, bg="white", width=2, height="1")
        self.quadradoLocalMorte.pack(side="right", padx=5)
        self.textoLocalMorte = tk.Label(self.barra2, font=("Impact", flexFontLegenda), text="Local de Morte", fg="white", bg="#262626")
        self.textoLocalMorte.pack(side="right", padx=2)

        self.barra3 = tk.Frame(self, bg="#262626", height=60)
        self.barra3.grid(row=3, column=0, sticky="ew")
        self.label_alcanceBombas = tk.Label(self.barra3, fg="white", bg="#262626", font=("Impact", flexFontInfo))
        self.label_alcanceBombas.pack(side="left", padx=4) # Também usado para causa do término
        self.label_tempoDetonacao = tk.Label(self.barra3, fg="white", bg="#262626", font=("Impact", flexFontInfo))
        self.label_tempoDetonacao.pack(side="left", padx=4)

        self.barra4 = tk.Frame(self, bg="#262626", height=60)
        self.barra4.grid(row=4, column=0, sticky="ew")
        self.label_proximaDetonacao = tk.Label(self.barra4, text="Não há bombas posicionadas", 
                                            fg="white", bg="#262626", font=("Impact", flexFontInfo))
        self.label_proximaDetonacao.pack(side="left", padx=8)

        # Barra lateral de menu e status de execução
        self.barraLateral1 = tk.Frame(self, bg="#262626")
        self.barraLateral1.grid(row=0, column=1, sticky="nsew")
        self.label_MiniMenu = tk.Label(self.barraLateral1, text="Menu", fg="white", bg="#262626", font=("Impact", flexFontMenu))
        self.label_MiniMenu.pack(side="top", pady=5, padx=48)

        self.barraLateral2 = tk.Frame(self, bg="#262626")
        self.barraLateral2.grid(row=1, column=1, sticky="nsew")
        self.quadradoJogador = tk.Label(self.barraLateral2, bg="green", width=2, height=1)
        self.quadradoJogador.pack(side="left")
        self.textoJogador = tk.Label(self.barraLateral2, font=("Impact", flexFontLegenda), text="Jogador", fg="white", bg="#262626")
        self.textoJogador.pack(side="left", padx=10)

        self.barraLateral3 = tk.Frame(self, bg="#262626")
        self.barraLateral3.grid(row=2, column=1, sticky="nsew")
        self.quadradoInimigo = tk.Label(self.barraLateral3, bg="red", width=2, height=1)
        self.quadradoInimigo.pack(side="left")
        self.textoInimigo = tk.Label(self.barraLateral3, font=("Impact", flexFontLegenda), text="Inimigo", fg="white", bg="#262626")
        self.textoInimigo.pack(side="left", padx=10)

        self.barraLateral4 = tk.Frame(self, bg="#262626")
        self.barraLateral4.grid(row=3, column=1, sticky="nsew")
        self.quadradoDestrutivel = tk.Label(self.barraLateral4, bg="blue", width=2, height=1)
        self.quadradoDestrutivel.pack(side="left")
        self.textoDestrutivel = tk.Label(self.barraLateral4, font=("Impact", flexFontLegenda), text="Destrutível", fg="white", bg="#262626")
        self.textoDestrutivel.pack(side="left", padx=10)

        self.barraLateral5 = tk.Frame(self, bg="#262626")
        self.barraLateral5.grid(row=4, column=1, sticky="nsew")
        self.quadradoIndestrutivel = tk.Label(self.barraLateral5, bg="black", width=2, height="1")
        self.quadradoIndestrutivel.pack(side="left")
        self.textoIndestrutivel = tk.Label(self.barraLateral5, font=("Impact", flexFontLegenda), text="Indestrutível", fg="white", bg="#262626")
        self.textoIndestrutivel.pack(side="left", padx=10)

        self.label_Status = tk.Label(self.barraLateral1, text="Executando", fg="black", bg="white", font=("Impact", flexFontStatus))
        self.label_Status.pack(side="bottom", pady=5, padx=15)

        self.botaoPausa = tk.Button(self.barraLateral1, text="Pausar", state="active", font=("Impact", flexFontBotao), 
                                    command=self.atualizarEstadoExecucao)
        self.botaoPausa.pack(side="top", pady=15, padx=20)
        self.botaoVoltar = tk.Button(self.barraLateral1, text="Voltar", fg="white", bg="gray", font=("Impact", flexFontBotao), command=voltar_callback, state="disabled")
        self.botaoVoltar.pack(side="top", pady=15)

        # Tamanho
        self.linhas = 13
        self.colunas = 13

        # Posição do jogador
        self.player = [self.jogo.jogador.linhaAtual, self.jogo.jogador.colunaAtual]

        # Input
        self.master.bind("<Key>", self.on_key)

        self.bind("<Configure>", self.on_resize)
        
        self.loop()
    
    def on_resize(self, event):
        # Altera o tamanho das fontes conforme o tamanho da janela
        largura = event.width
        altura = event.height

        escala = min(largura / 640, altura / 600)

        novoflexFontLegenda = int(16 * escala)
        novoflexFontInfo = int(18 * escala)
        novoflexFontBotao = int(18 * escala)
        novoflexFontMenu = int(26 * escala)
        novoflexFontStatus = int(22 * escala)

        # evita fonte muito pequena
        novoflexFontLegenda = max(6, novoflexFontLegenda)
        novoflexFontInfo = max(8, novoflexFontInfo)
        novoflexFontBotao = max(8, novoflexFontBotao)
        novoflexFontMenu = max(16, novoflexFontMenu)
        novoflexFontStatus = max(12, novoflexFontStatus)

        self.textoBomba.config(font=("Impact", novoflexFontLegenda))
        self.textoDestrutivel.config(font=("Impact", novoflexFontLegenda))
        self.textoIndestrutivel.config(font=("Impact", novoflexFontLegenda))
        self.textoInimigo.config(font=("Impact", novoflexFontLegenda))
        self.textoJogador.config(font=("Impact", novoflexFontLegenda))
        self.textoLocalMorte.config(font=("Impact", novoflexFontLegenda))
        self.label_alcanceBombas.config(font=("Impact", novoflexFontInfo))
        self.label_inimigosRestantes.config(font=("Impact", novoflexFontInfo))
        self.label_MiniMenu.config(font=("Impact", novoflexFontMenu))
        self.label_proximaDetonacao.config(font=("Impact", novoflexFontInfo))
        self.label_Status.config(font=("Impact", novoflexFontStatus))
        self.label_tempoDetonacao.config(font=("Impact", novoflexFontInfo))
        self.label_turno.config(font=("Impact", novoflexFontInfo))
        self.botaoPausa.config(font=("Impact", novoflexFontBotao))
        self.botaoVoltar.config(font=("Impact", novoflexFontBotao))

    def atualizarEstadoExecucao(self):
        if self.estadoExecucao == 'Executando':
            self.estadoExecucao = 'Pausa'
            self.label_Status.config(text="Pausado", fg="orange", padx=21)
            self.botaoPausa.config(text="Retomar")
        else:
            self.estadoExecucao = 'Executando'
            self.label_Status.config(text="Executando", fg="black", padx=2)
            self.botaoPausa.config(text="Pausar")

    def iniciarJogo(self):
        self.jogo = Jogo()

        self.estadoExecucao = 'Executando'
        self.label_Status.config(text=self.estadoExecucao, fg="black", bg="white")
        # reset visual
        self.botaoPausa.configure(state="active")
        self.label_alcanceBombas.config(fg="white")
        self.botaoVoltar.config(state="disabled")

        self.update()
        self.desenharMapa()

    # Input
    def on_key(self, event):
        if self.jogo.causaTerminoAtual == '' and self.estadoExecucao == 'Executando':
            if event.keysym == "Up":
                self.jogo.atualizarPartida('w')
            elif event.keysym == "Down":
                self.jogo.atualizarPartida('s')
            elif event.keysym == "Left":
                self.jogo.atualizarPartida('a')
            elif event.keysym == "Right":
                self.jogo.atualizarPartida('d')
            elif event.keysym == "b" or  event.keysym == "B":
                self.jogo.atualizarPartida('b')

    # Atualiza tudo
    def update(self):
        self.label_turno.config(text=f"{self.jogo.maxTurnos - self.jogo.turnos} turnos restantes")
        self.label_inimigosRestantes.config(text=f"{len(self.jogo.listaInimigos)} inimigo(s) restante(s)")
        if len(self.jogo.listaBombas) != 0:
            self.label_proximaDetonacao.config(text=f"Próxima bomba explode em: {self.jogo.listaBombas[0].tempoDetonacao} turno(s)")
        else:
            self.label_proximaDetonacao.config(text="Não há bombas posicionadas")
        self.label_tempoDetonacao.config(text="Tempo de detonação: " + str(self.jogo.tempoDetonacao))
        self.label_alcanceBombas.config(text="Alcance da Bomba: " + str(self.jogo.alcanceBomba))

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
                        fill="gray",
                        outline="white"
                    )
                if self.jogo.mapa.grade[i][j] == '#':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="black",
                        outline="white"
                    )
                if self.jogo.mapa.grade[i][j] == '$':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="blue",
                        outline="white"
                    )
                if self.jogo.mapa.grade[i][j] == 'J':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="green",
                        outline="white"
                    )
                if self.jogo.mapa.grade[i][j] == 'I':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="red",
                        outline="white"
                    )
                if self.jogo.mapa.grade[i][j] == 'B':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="magenta",
                        outline="white"
                    )
                if self.jogo.mapa.grade[i][j] == 'X':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="white",
                        outline="white"
                    )

    # Loop
    def loop(self):
        self.update()
        if self.jogo.ehVivo:
            self.desenharMapa()
        else:
            self.desenharMapa()
            if self.jogo.causaTerminoAtual == 'Jogador sobreviveu todos os turnos':
                self.label_alcanceBombas.config(fg="green", text=self.jogo.mensagens[self.jogo.causaTerminoAtual])
            else:
                self.label_alcanceBombas.config(fg="red", text=self.jogo.mensagens[self.jogo.causaTerminoAtual])
            self.label_tempoDetonacao.config(text="")
            self.botaoVoltar.configure(state="active", bg="gray")
            self.botaoPausa.configure(state="disabled")
            self.estadoExecucao = 'Finalizado'
            self.label_Status.config(text="Finalizado", fg="red")
        # ~60 FPS (16ms)
        self.after(16, self.loop)