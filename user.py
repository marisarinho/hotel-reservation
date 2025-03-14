class User:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome

        if not self.__validar_cpf(cpf):
            raise ErroDeReserva('CPF inválido')
            
        self.cpf = cpf
        self.telefone = telefone

    def __str__(self):
        return f"{self.nome} {self.cpf} {self.telefone}"

    def __validar_cpf(cpf)->bool:
        if len(cpf) != 11:
            return False

        for char in cpf:
            if char not in "0123456789":
                return False
        
        return True
        