import random

class Mapa:
    VAZIO = '.'
    INDESTRUTIVEL = '#'
    DESTRUTIVEL = '$'

    def __init__(self, linhas, colunas, proporcaoDestrutiveis):
        self.linhas = linhas
        self.colunas = colunas
        self.totalObstaculosDestrutiveis = 0
        self.proporcaoDestrutiveis = proporcaoDestrutiveis
        self.grade = self.construirMapa(self.proporcaoDestrutiveis)

    def construirMapa(self, proporcaoDestrutiveis):
        gradeTemporaria = [[self.VAZIO for _ in range(self.colunas)] for _ in range(self.linhas)]
        for i in range(self.linhas):
            for j in range(self.colunas):
                # Proporção de obstáculos sempre fixa, permitindo variação somente dos destrutíveis 
                if random.random() < 0.3: # Chance de destrutível = 0.2 * proporcaoDestrutiveis
                    if random.random() < proporcaoDestrutiveis:
                        gradeTemporaria[i][j] = self.DESTRUTIVEL
                        self.totalObstaculosDestrutiveis += 1
                    else:
                        gradeTemporaria[i][j] = self.INDESTRUTIVEL
        return gradeTemporaria
    
    def limpar(self, simbolo):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.grade[i][j] == simbolo:
                    self.grade[i][j] = self.VAZIO

    def exibir(self):
        print('\n')
        for linha in self.grade:
            print(' '.join(linha))

    def dentroLimite(self, linha, coluna):
        return 0 <= linha < self.linhas and 0 <= coluna < self.colunas