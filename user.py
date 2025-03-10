class User:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def __str__(self):
        return f"{self.nome} {self.cpf} {self.telefone}"
        