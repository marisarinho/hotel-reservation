from exception import ErroDeReserva

class Hospede:
    def __init__(self, nome:str, cpf:str, telefone:int):
        self.nome = nome

        # if not self.__cpf_valido(cpf):
        #     raise ErroDeReserva('CPF inválido')
            
        self.cpf = cpf
        self.telefone = telefone

    def __str__(self):
        return f"{self.nome} {self.cpf} {self.telefone}"

    def __cpf_valido(self, cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False

        # Digito 1
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        digito1 = 0 if resto == 10 else resto

        # Digito 2
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        digito2 = 0 if resto == 10 else resto

        if int(cpf[9]) != digito1 or int(cpf[10]) != digito2:
            # print(f"Erro: CPF {cpf} com dígitos verificadores inválidos.") #testando
            return False

        return True