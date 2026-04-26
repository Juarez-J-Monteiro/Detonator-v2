import random

class Inimigo:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.sofreuColisao = False
        self.simbolo = 'I'

    def mover(self, mapa, jogador):

        direcoes = ['w','a','s','d']

        while len(direcoes) != 0:
            novaLinha = self.linha
            novaColuna = self.coluna

            direcaoSorteada = random.choices(direcoes)
        
            if direcaoSorteada[0] == 'w':
                novaLinha -= 1
            elif direcaoSorteada[0] == 's':
                novaLinha += 1
            elif direcaoSorteada[0] == 'a':
                novaColuna -= 1
            elif direcaoSorteada[0] == 'd':
                novaColuna += 1

            if not(mapa.dentroLimite(novaLinha, novaColuna)): # Garante que inimigo se mova dentro dos limites do mapa
                direcoes.remove(direcaoSorteada[0]) # Remove direção inválida
                continue 
            elif mapa.grade[novaLinha][novaColuna] in (mapa.INDESTRUTIVEL, mapa.DESTRUTIVEL, self.simbolo):
                direcoes.remove(direcaoSorteada[0]) # Remove movimento onde há obstáculo ou inimigo
            elif novaLinha == jogador.linhaAtual and novaColuna == jogador.colunaAtual:
                return novaLinha, novaColuna, False
            else:
                return novaLinha, novaColuna, True
            
        return self.linha, self.coluna, True # Se tiver preso, não se move.