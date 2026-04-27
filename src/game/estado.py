import json
import os

class EstadoPersistente:
    def __init__(self):
        
        # Garante execução correta em uma IDE (tive problemas ao salvar e carregar estado quando executado pelo vsCode)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.arquivo = os.path.join(base_dir, "estado.json")

        self.partidasJogadas = 0
        self.mediaTurnosVivos = 0
        self.mediaBombasPartida = 0
        self.causaTermino = ''
        self.numeroTurnoEliminado = 0
        self.taxaDestruicaoObstaculo = 0.0

        self.carregar()

    def exibir(self): # Exibi todo o estado persistente no terminal
        return (
            f"Partidas jogadas: {self.partidasJogadas}\n"
            f"Média de turnos sobrevividos: {self.mediaTurnosVivos}\n"
            f"Média de bombas por partida: {self.mediaBombasPartida}\n"
            f"Causa do término: {self.causaTermino}\n"
            f"Turno da eliminação (última partida): {self.numeroTurnoEliminado if self.numeroTurnoEliminado != -1 else "O jogador não foi eliminado"} \n"
            f"Taxa de destruição de obstáculos: {self.taxaDestruicaoObstaculo}"
        )

    def carregar(self): # Carrega as informações do estado persistente caso exista
        if not os.path.exists(self.arquivo):
            return
        try:
            with open(self.arquivo, "r") as f:
                dados = json.load(f)

            self.partidasJogadas = dados["partidasJogadas"]
            self.mediaTurnosVivos = dados["mediaTurnosVivos"]
            self.mediaBombasPartida = dados["mediaBombasPartida"]
            self.causaTermino = dados["causaTermino"]
            self.numeroTurnoEliminado = dados["numeroTurnoEliminado"]
            self.taxaDestruicaoObstaculo = dados["taxaDestruicaoObstaculo"]
        except (json.JSONDecodeError, OSError):
            print("Erro ao carregar estado. Usando valores padrão")

    def salvar(self): # Salva o estado persistente com novas informações.
        dados = {
            "partidasJogadas": self.partidasJogadas,
            "mediaTurnosVivos": self.mediaTurnosVivos,
            "mediaBombasPartida": self.mediaBombasPartida,
            "causaTermino": self.causaTermino,
            "numeroTurnoEliminado": self.numeroTurnoEliminado,
            "taxaDestruicaoObstaculo": self.taxaDestruicaoObstaculo,
        }

        try:
            with open(self.arquivo, "w") as f:
                json.dump(dados, f)
        except OSError:
            print("Não foi possível salvar o estado do jogo.")