class Quarto:
    def __init__(self, num_quarto: int, preco: float, camas: int):
        self.__num_quarto = num_quarto
        self.__preco = preco  
        self.__camas = camas  
    
    def __eq__(self, other):
        return self.__num_quarto == other.__num_quarto
    
    @property
    def num_quarto(self):
        return self.__num_quarto
    
    @property
    def preco(self):
        return self.__preco
    
    @property
    def camas(self):
        return self.__camas