from datetime import datetime
from quarto import Quarto
from hospede import Hospede

class Reserva:
    def __init__(self, quarto: Quarto, data_entrada, data_saida:datetime, hospede:Hospede):
        self.__quarto = quarto
        self.__data_entrada = data_entrada
        self.__data_saida = data_saida
        self.__hospede = hospede
    
    def __lt__(self, other):
        return self.__data_entrada < other.data_entrada  # Ordenação apenas pela data de entrada
            
    def __eq__(self, other):
        return self.__data_entrada == other.data_entrada  # Igualdade apenas pela data de entrada
    
    
    def __str__(self):
        return f"Reserva(quarto={self.__quarto}, periodo = {self.__data_entrada} ate {self.__data_saida}, user={self.__hospede})"
    
    def __repr__(self):
        return self.__str__()
    
    def get_quarto(self):
        return self.__quarto

    def get_data_entrada(self):
        return self.__data_entrada

    def get_data_saida(self):
        return self.__data_saida

    def get_hospede(self):
        return self.__hospede

    
 