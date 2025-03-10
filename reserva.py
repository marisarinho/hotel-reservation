from datetime import datetime
from quarto import Quarto

class Reserva:
    def __init__(self, quarto: Quarto, data_entrada, data_saida:datetime, user):
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.user = user
    
    
    def __lt__(self, other):
        return self.data_entrada < other.data_entrada  # Ordenação apenas pela data de entrada
            
    def __eq__(self, other):
        return self.data_entrada == other.data_entrada  # Igualdade apenas pela data de entrada
    
    
    def __str__(self):
        return f"Reserva(quarto={self.quarto}, periodo = {self.data_entrada} ate {self.data_saida}, user={self.user})"
    
    def __repr__(self):
        return self.__str__()
    
 