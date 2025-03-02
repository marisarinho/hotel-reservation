import socket
from threading import Thread
import json
from avl import AVLTree
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


class Reserva:
    def __init__(self, quarto: Quarto, periodo, user: User):
        self.quarto = quarto
        self.periodo = periodo
        self.user = user

    def __lt__(self, other):
        return self.periodo < other.periodo
    
    def __eq__(self, other):
        return self.periodo == other.periodo


class Servidor:
    def __init__(self):
        self.host = socket.gethostname()
        self.porta = 10000
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reservas = AVLTree()
        self.quartos = {}
        self.quartos_disponiveis = []

        reserva = Reserva(101, range(2, 6), 1)
        self.reservas.add(reserva)
        self.reservas.search(Reserva(0, range(2, 6), 0))

    def start(self):
        self.servidor_socket.bind((self.host, self.porta))
        self.servidor_socket.listen(5)


        print(f"Servidor rodando em {self.host}:{self.porta}")

        while True:
            conexao, endereco = self.servidor_socket.accept()
            thread_cliente = Thread(target=self.lidar_com_cliente, args=(conexao, endereco))
            thread_cliente.start()

    def quartos_diponiveis(self,periodo) -> list:
        ... # listar os quartos disponiveis - percorredo a avl reserva 

    def Cancelar():
        pass 
        
    def consultar_reserva(self,avl, cpf):
        user = User()
        resultado = AVLTree.search(user.cpf)  
    
        if resultado:
            print("Reserva encontrada:", resultado)
        else:
            print("Reserva não encontrada.")


    def lidar_com_cliente(self, conexao, endereco):
        print(f"Cliente conectado: {endereco}")


        while True:
            try:
                mensagem = conexao.recv(1024).decode()
                mari = User(**json.loads(mensagem.split("__")[1]))
                print(mari)
                if not mensagem:
                    break

                comando = mensagem.split()
                resposta = "40 ERRO Comando inválido"  # Padrão de erro

                if comando[0] == "HRCP":
                    if comando[1] == "CHECK":
                        id_quarto = comando[2]
                        if id_quarto in self.quartos_disponiveis and not self.reservas.buscar(id_quarto):
                            resposta = f"20 OK DISPONIVEL {id_quarto}"
                        else:
                            resposta = f"40 ERRO RESERVADO {id_quarto}"

                    elif comando[1] == "RESERVE":
                        id_quarto = comando[2]
                        nome_cliente = comando[3]

                        if id_quarto in self.quartos_disponiveis:
                            if self.reservas.add(Reserva(id_quarto, range(10), nome_cliente)):
                                resposta = f"20 OK Reservation Done"
                            else:
                                resposta = f"40 ERRO Could not reserve"
                        else:
                            resposta = "40 ERRO Invalid room number"

                    elif comando[1] == "CANCEL":
                        id_quarto = comando[2]

                        if self.reservas.remover(id_quarto):
                            resposta = f"20 OK Reservation Canceled"
                        else:
                            resposta = f"40 ERRO Reservation Not Found"

                    elif comando[1] == "LIST":
                        todas_reservas = self.reservas.listar_todos()
                        resposta = "20 OK LISTA " + " | ".join(f"{k}: {v}" for k, v in todas_reservas.items()) if todas_reservas else "40 ERRO No Reservations Found"

                conexao.send(resposta.encode())

            except Exception as e:
                print(f"Erro: {e}")
                conexao.close()
                break

if __name__ == '__main__':
    Servidor().start()
