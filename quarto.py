class Quarto:
    def __init__(self, num_quarto, preco, camas):
        self.num_quarto = num_quarto
        self.disponibilidade = True
        self.preco = preco
        self.camas = camas

    def __repr__(self):
        return f'Quarto(num_quarto= {self.num_quarto}, disponibilidade={self.disponibilidade}, preço={self.preco})'

    def __eq__(self, other):
        return self.num_quarto == other.num_quarto