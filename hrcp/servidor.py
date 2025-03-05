import socket
import threading
from avl import *
from hashTable import *
from fila import *
from datetime import datetime

#ao tentar enviar um obj por tcp(nao da)


class User:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def __str__(self):
        return f"{self.nome} {self.cpf} {self.telefone}"
        
class Quarto:
    def __init__(self,num_quarto,preco,camas):
        self.num_quarto = num_quarto
        self.disponibilidade = True
        self.preco = preco
        self.camas = camas

    @staticmethod
    def gerar_quartos(hash_table,quantidade = 20):
        for i in range(1, quantidade + 1):
            num_quarto = 100 + i
            preco = 150 + (i % 3) * 50  # Alterna preços automaticamente
            camas = (i % 3) + 1  # Alterna entre 1, 2 e 3 camas
            hash_quarto.insert(num_quarto, Quarto(num_quarto, preco, camas))


class Reserva:
    def __init__(self, quarto: Quarto, periodo, user: User):
        self.quarto = quarto
        self.periodo = periodo
        self.user = user

    def __lt__(self, other):
        return self.periodo < other.periodo
    
    def __eq__(self, other):
        return self.periodo == other.periodo

        def periodo_conflita(self, outra_reserva):
            return not (self.periodo[1] < outra_reserva.periodo[0] or self.periodo[0] > outra_reserva.periodo[1])

   

class Servidor:
    def __init__(self, host='localhost', porta=12345):
        self.host = host
        self.porta = porta
        self.hash_usuarios = HashTable(capacity=50)
        self.hash_quartos = HashTable(capacity=25)
        self.arvore_avl_reservas = AVLTree()
        self.fila_reservas = Fila()

    def realizar_reserva(self, cpf, num_quarto, periodo):
        usuario = self.usuario.get(cpf)
        if not usuario:
            raise ValueError("Usuário não encontrado!")

        tabela_quarto = self.hash_quarto.get(num_quarto)
        if not tabela_quarto:
            raise ValueError("Quarto não encontrado!")
        reservas_existentes = self.arvore_avl_reservas.search(num_quarto)  
        for reserva in reservas_existentes:
            if reserva.periodo_conflita(Reserva(usuario, num_quarto, periodo)):
                raise ValueError(f"O quarto {num_quarto} já está reservado para o período solicitado!")
        reserva = Reserva(usuario, num_quarto, periodo)


        self.arvore_avl_reservas.insert(reserva.num_quarto, reserva)

        quarto.disponibilidade = False 
        print(f"Reserva realizada com sucesso para o quarto {num_quarto}!")


    def cancelar(self, cpf, num_quarto, periodo):
        
        reservas_existentes = self.arvore_avl_reservas.buscar(num_quarto)
        for reserva in reservas_existentes:
            if reserva.usuario.cpf == cpf and reserva.periodo == periodo:
                # Remover a reserva da árvore AVL e marcar quarto como disponível
                self.arvore_avl_reservas.remover(num_quarto, reserva)
                tabela_quarto = self.hash_quartos.search(num_quarto)
                if tabela_quarto:
                    quarto.disponibilidade = True
                print(f"Reserva do quarto {num_quarto} cancelada com sucesso.")
                return
        print(f"Nenhuma reserva encontrada para o CPF {cpf} e quarto {num_quarto} no período especificado.")

    def consultar_reserva(self, cpf):
        # Consultar reservas do usuário
        reservas = self.arvore_avl_reservas.buscar_por_usuario(cpf)
        if reservas:
            for reserva in reservas:
                print(f"Quarto {reserva.num_quarto} reservado de {reserva.periodo[0]} até {reserva.periodo[1]}")
        else:
            print(f"Não há reservas encontradas para o CPF {cpf}.")

    def start(self):
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.bind((self.host, self.porta))
        servidor_socket.listen(5)
        print("Servidor iniciado.")
        Quarto.gerar_quartos(HashTable)

        while True:
            conexao, endereco = servidor_socket.accept()
            print(f"Cliente conectado: {endereco}")
            thread_cliente = threading.Thread(target=self.lidar_com_cliente, args=(conexao,))
            thread_cliente.start()

    def lidar_com_cliente(self, conexao):
        if comando[0] == "RESERVAR":
            cpf, num_quarto, periodo = comando[1], comando[2], comando[3]
            try:
                user = hash_usuarios.search(cpf) 
                self.realizar_reserva(cpf, num_quarto, periodo) 
            except KeyError:
                # Se o usuário não existe, cria automaticamente
                user = User(cpf=cpf, nome="Nome Padrão", telefone="0000-0000")
                self.usuarios.insert(cpf, user)  
                print(f"Usuário {cpf} cadastrado automaticamente.") 
                self.realizar_reserva(cpf, num_quarto, periodo) 
        elif comando[0] == "CANCELAR":
            cpf, num_quarto, periodo = comando[1], comando[2], comando[3]  # Passando parâmetros
            self.cancelar(cpf, num_quarto, periodo)
        elif comando[0] == "CONSULTAR":
            cpf = comando[1]
            self.consultar_reserva(cpf)


        elif comando[0] == "SAIR":
            conexao.close()

if __name__ == "__main__":
    Servidor().start()
