from datetime import datetime
from hrcp.gerenciamento.quarto import Quarto

class Reserva:
    def __init__(self, quarto: Quarto, data_entrada, data_saida:datetime, user: User):
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.user = user

    def __lt__(self, other):
        return self.periodo < other.periodo
    
    def __eq__(self, other):
        return self.periodo == other.periodo
    
    def __str__(self):
        return f"Reserva(quarto={self.quarto}, periodo={self.periodo}, user={self.user})"
    
    def __repr__(self):
        return self.__str__()
    
    def periodo_conflita(self, outra_reserva):
      return not (self.periodo_fim < outra_reserva.periodo_inicio or self.periodo_inicio > outra_reserva.periodo_fim)