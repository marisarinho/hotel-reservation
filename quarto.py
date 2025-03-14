class Quarto:
    def __init__(self, num_quarto: int, preco: float, camas: int):
        self.__num_quarto = num_quarto  

        self.__preco = preco  
        self.__camas = camas  
    
    def get_num_quarto(self):
        return self.__num_quarto
    
    
    
    def get_preco(self):
        return self.__preco
    
    def get_camas(self):
        return self.__camas
    
    
    
    def __repr__(self):
        return f'Quarto(num_quarto={self.__num_quarto}, disponibilidade={self.__disponibilidade}, preco={self.__preco})'
    
    def __eq__(self, other):
        return self.__num_quarto == other.__num_quarto