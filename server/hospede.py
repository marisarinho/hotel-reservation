from exception import ErroDeReserva

class Hospede:
    def __init__(self, nome :str, cpf: str, telefone: str, senha: str):
        self.__nome = nome

        if not self.__cpf_valido(cpf):
            raise ErroDeReserva('CPF inválido')
            
        self.__cpf = cpf
        self.__telefone = telefone
        self.__senha = senha

    def __str__(self):
        return f"{self.__nome} {self.__cpf} {self.__telefone}"

    @property
    def nome(self) -> str:
        return self.__nome
    
    @property
    def cpf(self) -> str:
        return self.__cpf
    
    @property
    def telefone(self) -> str:
        return self.__telefone
    
    @property
    def senha(self) -> str:
        return self.__senha

    def __cpf_valido(self, cpf: str) -> bool:
        """ 
        Método que verifica se um cpf é válido.

        Parametros
        -----------
        cpf (str): o CPF do hóspede

        Retorno
        ------------
        Valor booleano (True ou False)

        Raises
        -------------
        Nenhuma exceção
        """
        
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
            return False

        return True