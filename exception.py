from datetime import datetime

class ErroDeReserva(Exception):

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem

    def __str__(self):
        return f"ErroDeReserva: {self.mensagem}"

def validar_cpf(cpf):
    if len(cpf) != 11:
        raise ErroDeReserva("CPF inválido! Deve conter exatamente 11 dígitos numéricos.")

    for char in cpf:
        if char not in "0123456789":
            raise ErroDeReserva("CPF inválido! Deve conter apenas números.")
        
def validar_numero_quarto(num_quarto):
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