from servidor import *
from cliente import *
minha_avl = AVLTree()
cpf_procurado = input("Digite o CPF da reserva: ")
serve = Servidor()
serve.consultar_reserva(cpf_procurado)  # minha_avl é a instância da AVL que contém as reservas
print('oi')