class Jogador:

    def __init__(self, linhaAtual=0, colunaAtual=0):
        self.simbolo = 'J'
        self.linhaAtual = linhaAtual
        self.colunaAtual = colunaAtual
        
    def mover(self, direcao, mapa, inimigos, turno):
        novaLinha = self.linhaAtual
        novaColuna = self.colunaAtual

        if direcao == 'w':
            novaLinha -= 1
        elif direcao == 's':
            novaLinha += 1
        elif direcao == 'a':
            novaColuna -= 1
        elif direcao == 'd':
            novaColuna += 1

        if not(mapa.dentroLimite(novaLinha, novaColuna)):
            return True, '', turno
        
        if mapa.grade[novaLinha][novaColuna] in (mapa.INDESTRUTIVEL, mapa.DESTRUTIVEL):
            return True, '', turno
        
        for inimigo in inimigos:
            if inimigo.linha == novaLinha and inimigo.coluna == novaColuna:
                inimigo.sofreuColisao = True
                self.linhaAtual = novaLinha
                self.colunaAtual = novaColuna
                return False, 'Colidiu com inimigo', turno+1
        
        self.linhaAtual = novaLinha
        self.colunaAtual = novaColuna
        return True, '', turno+1
    