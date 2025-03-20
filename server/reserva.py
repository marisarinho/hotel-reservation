from datetime import datetime
from quarto import Quarto
from hospede import Hospede

class Reserva:
    def __init__(self, quarto: Quarto, data_entrada: datetime, data_saida: datetime, hospede: Hospede):
        self.__quarto = quarto
        self.__data_entrada:datetime = data_entrada
        self.__data_saida = data_saida
        self.__hospede = hospede
    
    def __lt__(self, other: "Reserva") -> bool:
        return self.__data_entrada < other.data_entrada  # Ordenação apenas pela data de entrada
            
    def __eq__(self, other: "Reserva") -> bool:
        return self.__data_entrada == other.data_entrada  # Igualdade apenas pela data de entrada
    
    def __str__(self) -> str:
        return f"Reserva(quarto={self.__quarto}, periodo = {self.__data_entrada} ate {self.__data_saida}, user={self.__hospede})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def data_entrada(self) -> datetime:
        return self.__data_entrada
    
    @property
    def data_saida(self) -> datetime:
        return self.__data_saida
    
    @property
    def hospede(self) -> Hospede:
        return self.__hospede
    
    @property
    def ano(self) -> int:
        return self.__data_entrada.year
    
    @property
    def quarto(self) -> Quarto:
        return self.__quarto