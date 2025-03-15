from datetime import datetime

class ErroDeReserva(Exception):

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem

    def __str__(self):
        return f"ErroDeReserva: {self.mensagem}"


    #pq aqui n ta funcionando duas underlines
    # def __validar_cpf(self,cpf:str):
        
    #     cpf = ''.join(filter(str.isdigit, cpf))

    #     if len(cpf) != 11:
    #         raise ErroDeReserva("CPF inválido! Deve conter exatamente 11 dígitos numéricos.")
    #     if cpf == cpf[0] * 11:
    #         raise ErroDeReserva("CPF inválido! Não pode conter todos os dígitos iguais.")
    
    #     soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    #     resto = (soma * 10) % 11
    #     digito1 = 0 if resto == 10 else resto

    #     soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    #     resto = (soma * 10) % 11
    #     digito2 = 0 if resto == 10 else resto

    #     if int(cpf[9]) != digito1 or int(cpf[10]) != digito2:
    #         raise ErroDeReserva("CPF inválido! Dígitos verificadores não conferem.")

    #     return True 
        
    def validar_numero_quarto(self,num_quarto:int):
        try:
            num_quarto = int(num_quarto)  
            if num_quarto <= 0:
                resposta = ErroDeReserva("Número de quarto inválido! Deve ser um número inteiro positivo.")
        except ValueError:
            resposta = ErroDeReserva("Número de quarto inválido! Deve ser um número inteiro positivo.")


# nao pode usar assim:
# raise ErroDeReserva("deu erro...")
# pq isso levanta a excecao e para o programa (para o servidor todo)
# no maximo pode usar assim:
resposta = ErroDeReserva("Deu erro")
# print(resposta)
# mas não faz sentido
# praticamente a mesma coisa