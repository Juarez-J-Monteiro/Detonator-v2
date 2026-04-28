from src.game.bomba import Bomba
from src.game.mapa import Mapa
from src.game.jogador import Jogador

from src.game.inimigo import Inimigo
from src.game.estado import EstadoPersistente

import random

class Jogo:
    def __init__(self):
        self.estado = EstadoPersistente()

        self.simboloInimigo = 'I'
        self.simboloBomba = 'B'
        self.msgErro = ""

        # Explosão no estilo "cruz", somente em linhas e colunas (sem diagonais).
        self.alcanceBomba, self.tempoDetonacao = self.calcularAlcanceTempoBomba()
        self.listaBombas = []
        self.contadorBombas = 0

        self.chanceInimigo = self.calcularChanceInimigo(self.estado) # Chance de surgir um inimigo.
        self.listaInimigos = []
        
        self.tamanhoMapa = 13 # Tamanho do mapa em linhas e colunas.

        self.obstaculosDestruidos = 0
        self.mapa = Mapa(self.tamanhoMapa, self.tamanhoMapa, self.calcularProporcaoDestrutiveis(self.estado))

        self.jogador = Jogador()
        self.ehVivo = True

        self.causaTerminoAtual = ''
        self.mensagens = {
                'Atingido por uma Bomba': "Uma bomba te atingiu.",
                'Inimigo matou': "Um inimigo te atingiu.",
                'Colidiu com inimigo': "Você colidiu com um inimigo."
            }

        self.emPartida = False
        self.turnos = 0
        self.maxTurnos = int(35 + (self.estado.mediaTurnosVivos // 5)) # Aumenta o limite de turnos quanto maior a média sobrevivida.

        qtdInimigos = 2 + int(self.estado.mediaTurnosVivos // 20) # Quantidade de inimigos iniciais com base no estado persistente
        for _ in range(qtdInimigos):
            self.geraInimigos(True)
        self.geraJogador()

    def explodir(self, bomba): # Explode a bomba em 4 direções

        def verificaJogador(i, j):
            # Jogador é abatido caso verdadeiro
            if i == self.jogador.linhaAtual and j == self.jogador.colunaAtual:
                self.ehVivo = False
                self.causaTerminoAtual = 'Atingido por uma Bomba'
                return True
            return False
        def verificaObstaculo(i, j):
            # Obstáculo DESTRUTIVEL é removido caso verdadeiro
            if self.mapa.grade[i][j] == self.mapa.DESTRUTIVEL:
                self.mapa.grade[i][j] = self.mapa.VAZIO
                self.obstaculosDestruidos += 1

        def verificaInimigo(i, j):
            # Inimigo é abatido caso verdadeiro
            if self.mapa.grade[i][j] == self.simboloInimigo:
                self.mapa.grade[i][j] = self.mapa.VAZIO

                novaLista = []
                for inimigo in self.listaInimigos:
                    if not (inimigo.linha == i and inimigo.coluna == j):
                        novaLista.append(inimigo)
                self.listaInimigos = novaLista

        # Garante explosão na posição da bomba
        verificaJogador(bomba.linha, bomba.coluna)
        verificaInimigo(bomba.linha, bomba.coluna)

        for i in range(1, bomba.alcance+1): # Verifica para cima
            linha = bomba.linha - i
            coluna = bomba.coluna

            # Limita a área de explosão apenas dentro mapa
            if linha < 0:
                break
            
            # Para a explosão imediatamente caso haja um obstáculo INDESTRUTÍVEL no caminho
            if self.mapa.grade[linha][coluna] == self.mapa.INDESTRUTIVEL:
                break

            if verificaJogador(linha, coluna):
                break

            verificaObstaculo(linha, coluna)
            verificaInimigo(linha, coluna)

        for i in range(1, bomba.alcance+1): # Verifica para baixo
            linha = bomba.linha + i
            coluna = bomba.coluna

            # Limita a área de explosão apenas dentro mapa
            if linha >= self.mapa.linhas:
                break

            # Para a explosão imediatamente caso haja um obstáculo INDESTRUTÍVEL no caminho
            if self.mapa.grade[linha][coluna] == self.mapa.INDESTRUTIVEL:
                break

            if verificaJogador(linha, coluna):
                break

            verificaObstaculo(linha, coluna)
            verificaInimigo(linha, coluna)
        
        for i in range(1, bomba.alcance+1): # Verifica a esquerda
            linha = bomba.linha
            coluna = bomba.coluna - i

            # Limita a área de explosão apenas dentro mapa
            if coluna < 0:
                break

            # Para a explosão imediatamente caso haja um obstáculo INDESTRUTÍVEL no caminho
            if self.mapa.grade[linha][coluna] == self.mapa.INDESTRUTIVEL:
                break

            if verificaJogador(linha, coluna):
                break

            verificaObstaculo(linha, coluna)
            verificaInimigo(linha, coluna)

        for i in range(1, bomba.alcance+1): # Verifica a direita
            linha = bomba.linha
            coluna = bomba.coluna + i

            # Limita a área de explosão apenas dentro mapa
            if coluna >= self.mapa.colunas:
                break
            
            # Para a explosão imediatamente caso haja um obstáculo INDESTRUTÍVEL no caminho
            if self.mapa.grade[linha][coluna] == self.mapa.INDESTRUTIVEL:
                break

            if verificaJogador(linha, coluna):
                break

            verificaObstaculo(linha, coluna)
            verificaInimigo(linha, coluna)

    def geraJogador(self): # Gera a posição do jogador
        # Jogador só é posicionado caso a coordenada seja um espaço VAZIO
        while True:
            linha = random.randint(0, self.mapa.linhas-1)   
            coluna = random.randint(0, self.mapa.colunas-1)

            if self.mapa.grade[linha][coluna] == self.mapa.VAZIO:
                
                # Garante espaço de surgimento para o jogador.
                comeco = [linha-1 if linha-1 >= 0 else 0, 
                          coluna-1 if coluna-1 >= 0 else 0]
                final = [linha+1 if linha+1 < self.mapa.linhas else self.mapa.linhas-1, 
                         coluna+1 if coluna+1 < self.mapa.colunas else self.mapa.colunas-1]

                for i in range(comeco[0], final[0]+1):
                    for j in range(comeco[1], final[1]+1):
                        if self.mapa.grade[i][j] in (self.mapa.INDESTRUTIVEL, self.mapa.DESTRUTIVEL):
                            if self.mapa.grade[i][j] == self.mapa.DESTRUTIVEL:
                                self.mapa.totalObstaculosDestrutiveis -= 1
                            if (i, j) != (linha, coluna): 
                                self.mapa.grade[i][j] = self.mapa.VAZIO

                self.mapa.grade[linha][coluna] = self.jogador.simbolo
                self.jogador.linhaAtual = linha
                self.jogador.colunaAtual = coluna
                return
            
    def calcularAlcanceTempoBomba(self): # Calcula o alcance da bomba na partida com base no estado persistente
        alcancePadrao = 3
        tempoPadrao = 3

        if self.estado.partidasJogadas < 3:
            return alcancePadrao, tempoPadrao
        
        if self.estado.mediaBombasPartida < 2:
            alcancePadrao += 1
        if self.estado.mediaBombasPartida > 5:
            tempoPadrao += 1
        if self.estado.taxaDestruicaoObstaculo < 0.3:
            alcancePadrao += 1
        if self.estado.taxaDestruicaoObstaculo > 0.7:
            alcancePadrao -= 1
            tempoPadrao -= 1
        
        if alcancePadrao > 4:
            alcancePadrao = 4
        elif alcancePadrao < 1:
            alcancePadrao = 1

        if tempoPadrao > 4:
            tempoPadrao = 4
        elif tempoPadrao < 3:
            tempoPadrao = 3

        return alcancePadrao, tempoPadrao
    
    def calcularChanceInimigo(self, estado): # Calcula a chance de inimigos com base no estado persistente
        chance = (0.09 + (estado.mediaTurnosVivos / 200) + (estado.partidasJogadas / 500) + (estado.taxaDestruicaoObstaculo / 5))
        return chance

    def calcularProporcaoDestrutiveis(self, estado): # Calcula a proporção dos destrutíveis com base no estado persistente
        proporcao = (0.5 - (estado.mediaTurnosVivos / 500) - (estado.partidasJogadas / 1000) - (estado.taxaDestruicaoObstaculo / 5))

        if proporcao < 0.2:
            proporcao = 0.2

        if proporcao > 0.7:
            proporcao = 0.7
        
        return proporcao

    def geraInimigos(self, ehQtdFixo): # Gera inimigos

        # Gera o inimigo independende da chance caso haja quantidade fixa a ser gerada. (vide __init__)
        if (random.random() < self.chanceInimigo) or ehQtdFixo:

            # Laço que garante espaço VAZIO para o inimigo surgir
            tentativas = 0
            while tentativas < 50:
                tentativas += 1

                linha = random.randint(0, self.mapa.linhas-1)
                coluna = random.randint(0, self.mapa.colunas-1)

                if self.mapa.grade[linha][coluna] == self.mapa.VAZIO:
                    comeco = [linha-1 if linha-1 >= 0 else 0, 
                        coluna-1 if coluna-1 >= 0 else 0]
                    final = [linha+1 if linha+1 < self.mapa.linhas else self.mapa.linhas-1, 
                        coluna+1 if coluna+1 < self.mapa.colunas else self.mapa.colunas-1]
                    
                    totalPontos = (final[0] - comeco[0] + 1) * (final[1] - comeco[1] + 1)
                    contaObstáculos = 0

                    for i in range(comeco[0], final[0]+1):
                        for j in range(comeco[1], final[1]+1):
                            if self.mapa.grade[i][j] in (self.mapa.INDESTRUTIVEL, self.mapa.DESTRUTIVEL):
                                contaObstáculos += 1

                    if contaObstáculos >= totalPontos-1:
                        continue
                    else:
                        inimigo = Inimigo(linha, coluna)
                        self.listaInimigos.append(inimigo)
                        self.mapa.grade[linha][coluna] = inimigo.simbolo
                        break
                else:
                    continue

    def atualizarInimigos(self): # Atualiza as posições dos inimigos de forma aleatória
        for inimigo in self.listaInimigos[:]:
            if inimigo.sofreuColisao:
                self.listaInimigos.remove(inimigo)
                continue

            novaLinha, novaColuna, inimigoMatou = inimigo.mover(self.mapa, self.jogador)

            if not inimigoMatou:
                self.ehVivo = False
                self.listaInimigos.remove(inimigo)
                self.causaTerminoAtual = 'Inimigo matou'
                return

            inimigo.linha = novaLinha
            inimigo.coluna = novaColuna
                
    def atualizarMapa(self): # Atualiza o mapa com todas as novas informações
        self.mapa.limpar(self.jogador.simbolo)
        self.mapa.limpar(self.simboloBomba)
        self.mapa.limpar(self.simboloInimigo)

        for bomba in self.listaBombas:
            self.mapa.grade[bomba.linha][bomba.coluna] = self.simboloBomba

        for inimigo in self.listaInimigos:
            self.mapa.grade[inimigo.linha][inimigo.coluna] = self.simboloInimigo
        
        self.mapa.grade[self.jogador.linhaAtual][self.jogador.colunaAtual] = self.jogador.simbolo

    def atualizarBombas(self): # Atualiza o estado das bombas
        for bomba in self.listaBombas[:]:
            bomba.tempoDetonacao -= 1
            if bomba.tempoDetonacao == 0: # Explode a bomba se o tempo de detonação esgotar
                self.explodir(bomba)
                self.mapa.grade[bomba.linha][bomba.coluna] = self.mapa.VAZIO
                self.listaBombas.remove(bomba)

    def atualizarRodada(self): # Faz a atualização do turno
        self.atualizarBombas()
        
        self.atualizarInimigos()

        self.geraInimigos(False)

        self.atualizarMapa()
    
    def finalizarPartida(self): # Finaliza a partida e salva o estado.
        partidasAntigas = self.estado.partidasJogadas
        partidasNovas = partidasAntigas + 1

        # Médias
        self.estado.mediaTurnosVivos = (
            (self.estado.mediaTurnosVivos * partidasAntigas) + self.turnos
            ) / partidasNovas
        
        self.estado.mediaBombasPartida = (
            (self.estado.mediaBombasPartida * partidasAntigas) + self.contadorBombas
            ) / partidasNovas

        # Causa
        self.estado.causaTermino = self.causaTerminoAtual

        # Turno eliminado
        if self.causaTerminoAtual in ('Atingido por uma Bomba', 'Inimigo matou', 'Colidiu com inimigo'):
            self.estado.numeroTurnoEliminado = self.turnos
        else:
            self.estado.numeroTurnoEliminado = -1

        # Taxa de destruição
        if self.mapa.totalObstaculosDestrutiveis > 0:
            taxaPartida = self.obstaculosDestruidos / self.mapa.totalObstaculosDestrutiveis
        else:
            taxaPartida = 0

        self.estado.taxaDestruicaoObstaculo = (
            (self.estado.taxaDestruicaoObstaculo * partidasAntigas) + taxaPartida
            ) / partidasNovas
        
        # Número de partidas
        self.estado.partidasJogadas = partidasNovas

        # Salvar o estado
        self.estado.salvar()
        

    def atualizarPartida(self, comando):
        # Finaliza a partida caso o jogador sobreviva todos os turnos
        if self.turnos == self.maxTurnos:
            self.causaTerminoAtual = 'Jogador sobreviveu todos os turnos'
            self.mapa.exibir()
            print("Turnos: " + str(self.turnos) + "\nVocê ganhou essa partida!")
            self.finalizarPartida()
        
        # self.mapa.exibir()
        
        # Exibi mensagem de erro de entrada. 
        if self.msgErro:
            print(self.msgErro)
            self.msgErro = "" # Reseta a mensagem após exibição

        # Exibi o turno atual, alcance e tempo de detonação padrão das bombas
        print("Turno: " + str(self.turnos) + "/" + str(self.maxTurnos))
        print("Alcance da bomba: " + str(self.alcanceBomba) + 
                " | Tempo de detonação: " + str(self.tempoDetonacao) + " turnos")
        
        # Exibi em quanto tempo a próxima bomba explodirá, caso exista.
        if len(self.listaBombas) != 0:
            print("Próxima bomba explode em: " + str(self.listaBombas[0].tempoDetonacao) + " turnos")

        # Recebe e verifica as entradas de comando
        # try:
        #     if self.turnos != 0:
        #         comando = str(input("Mover (w/a/s/d), posicionar bomba (b) ou (q) para sair: ")).lower()
        #     else:
        #         comando = str(input("Mover (w/a/s/d), posicionar bomba (b), \n(r) para resumo de todas as partidas ou (q) para sair: ")).lower()
        # except Exception:
        #     print("Erro na leitura do comando.")
        #     comando = ""

        # if comando not in ('w','a','s','d','q','r','b'):
        #     self.msgErro = 'Comando inválido!'
        #     continue # Pula direto pro próximo ciclo do while

        # # Encerra a execução quando solicitado, sem salvar o estado (partida inválida)
        # if comando == 'q':
        #     break
        
        # Trata os comando de locomoção
        if comando in ('w','a','s','d'):
            turnoAtual = self.turnos
            self.ehVivo, self.causaTerminoAtual, self.turnos = self.jogador.mover(comando, self.mapa, self.listaInimigos, self.turnos)
            if self.turnos > turnoAtual:
                self.atualizarRodada() # O turno só avança se houver ação do jogador

        # Trata o posicionamento de bomba
        if comando == 'b':
            def plantarBomba():
                # self.tempoDetonacao + 1 serve para corrigir o turno da bomba diminuindo no mesmo ciclo em que ela é criada.
                novaBomba = Bomba(self.jogador.linhaAtual, self.jogador.colunaAtual, self.alcanceBomba, self.tempoDetonacao+1)
                self.listaBombas.append(novaBomba)
                self.turnos += 1
                self.contadorBombas += 1
                self.atualizarRodada() # O turno só avança se houver ação do jogador

            for bomba in self.listaBombas:
                if bomba.linha == self.jogador.linhaAtual and bomba.coluna == self.jogador.colunaAtual:
                    self.msgErro = "Esse lugar já tem uma bomba!"
                    break
            else:
                plantarBomba()
        
        # if comando == 'r' and self.turnos == 0: # Por escolha de design, o resumo só pode ser visto no começo da execução.
        #     self.estado.exibir()
        #     break # Logo em seguida encerra o programa.
    
        # Trata as causas do término por morte
        if self.causaTerminoAtual in ('Atingido por uma Bomba', 'Inimigo matou', 'Colidiu com inimigo'):
            self.mapa.grade[self.jogador.linhaAtual][self.jogador.colunaAtual] = 'X'
            self.mapa.exibir()
            print(self.mensagens[self.causaTerminoAtual])
            self.finalizarPartida()