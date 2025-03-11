class ErroDeReserva(Exception):

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem

    def __str__(self):
        return f"ErroDeReserva: {self.mensagem}"


# nao pode usar assim:
# raise ErroDeReserva("deu erro...")
# pq isso levanta a excecao e para o programa (para o servidor todo)
# no maximo pode usar assim:
resposta = ErroDeReserva("Deu erro")
# print(resposta)
# mas não faz sentido
# praticamente a mesma coisa

 
"""
usuario: Quero cancelar:
*digita o cpf*

*digita o quarto*

-> servidor vai la e 
    1. verifica se o quarto é valido
        -> *Não é valido? retorna o erro pro cliente
    2. exclui o quarto da hash table
        -> Deu certo? retorna deu certo pro cliente

-> fim 

""" 