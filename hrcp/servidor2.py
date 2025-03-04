import socket
import threading
from avl import AVLTree
from hashTable import HashTable
from fila import Fila
from datetime import datetime

class User:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def __str__(self):
        return f"{self.nome} {self.cpf} {self.telefone}"
        
class Quarto:
    def __init__(self, num_quarto, preco, camas):
        self.num_quarto = num_quarto
        self.disponibilidade = True
        self.preco = preco
        self.camas = camas

    @staticmethod
    def gerar_quartos(hash_table, quantidade=20):
        for i in range(1, quantidade + 1):
            num_quarto = 100 + i
            preco = 150 + (i % 3) * 50  # Alterna preços automaticamente
            camas = (i % 3) + 1  # Alterna entre 1, 2 e 3 camas
            hash_table.insert(num_quarto, Quarto(num_quarto, preco, camas))

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
        Quarto.gerar_quartos(self.hash_quartos)  # Corrigido: agora passa uma instância

    def realizar_reserva(self, cpf, num_quarto, periodo):
        # usuario = self.hash_usuarios.get(cpf) 
        # if not usuario:
        #     usuario = User(nome="Usuário Padrão", cpf=cpf, telefone="0000-0000")
        #     self.hash_usuarios.insert(cpf, usuario)

        # quarto = self.hash_quartos.get(num_quarto)
        # if not quarto:
        #     raise ValueError("Quarto não encontrado!")

        # reservas_existentes = self.arvore_avl_reservas.search(num_quarto) 
        # if reservas_existentes:
        #     for reserva in reservas_existentes:
        #         if reserva.periodo_conflita(Reserva(quarto, periodo, usuario)):
        #             raise ValueError(f"O quarto {num_quarto} já está reservado para o período solicitado!")
        
        # reserva = Reserva(quarto, periodo, usuario)
        # self.arvore_avl_reservas.add(reserva)
        # quarto.disponibilidade = False 
        # return f"Reserva realizada com sucesso para o quarto {num_quarto}!"
        usuario = None
        if self.hash_usuarios.size != 0:
            usuario = self.hash_usuarios.get(cpf)
        if usuario == None:
            usuario = User(nome="Usuário Padrão", cpf=cpf, telefone="0000-0000")
            self.hash_usuarios.insert(cpf, usuario)
        quarto = None
        if self.hash_quartos.size != 0:
            quarto = self.hash_quartos.get(num_quarto)
        if  quarto == None:
            raise ValueError("Quarto não encontrado!")
        reservas_existentes = self.arvore_avl_reservas.search(num_quarto) 
        if reservas_existentes:
            for reserva in reservas_existentes:
                if reserva.periodo_conflita(Reserva(quarto, periodo, usuario)):
                    raise ValueError(f"O quarto {num_quarto} já está reservado para o período solicitado!")

        reserva = Reserva(quarto, periodo, usuario)
        self.arvore_avl_reservas.add(reserva)
        quarto.disponibilidade = False 
        return f"Reserva realizada com sucesso para o quarto {num_quarto}!"

    def cancelar_reserva(self, cpf, num_quarto, periodo):
        reservas_existentes = self.arvore_avl_reservas.search(num_quarto)
        if reservas_existentes:
            for reserva in reservas_existentes:
                if reserva.user.cpf == cpf and reserva.periodo == periodo:
                    self.arvore_avl_reservas.delete(reserva)
                    quarto = self.hash_quartos.get(num_quarto)
                    if quarto:
                        quarto.disponibilidade = True
                    return f"Reserva do quarto {num_quarto} cancelada com sucesso."
        return f"Nenhuma reserva encontrada para o CPF {cpf} no quarto {num_quarto}."

    def consultar_reserva(self, cpf):
        reservas = [r for r in self.arvore_avl_reservas if r.user.cpf == cpf]
        if reservas:
            return [f"Quarto {r.quarto.num_quarto} reservado de {r.periodo[0]} até {r.periodo[1]}" for r in reservas]
        return ["Não há reservas para este CPF."]

    def start(self):
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.bind((self.host, self.porta))
        servidor_socket.listen(5)
        print("Servidor iniciado.")

        while True:
            conexao, endereco = servidor_socket.accept()
            print(f"Cliente conectado: {endereco}")
            thread_cliente = threading.Thread(target=self.lidar_com_cliente, args=(conexao,))
            thread_cliente.start()

    def lidar_com_cliente(self, conexao):
        while True:
            try:
                dados = conexao.recv(1024).decode()
                if not dados:
                    break

                dados = dados.strip("\r\n")
                
                comando = dados.split()
                resposta = "Comando inválido."

                if comando[0] == "RESERVAR" and len(comando) >= 4:
                    cpf, num_quarto, periodo = comando[1], int(comando[2]), comando[3]
                    resposta = self.realizar_reserva(cpf, num_quarto, periodo)
                elif comando[0] == "CANCELAR" and len(comando) >= 4:
                    cpf, num_quarto, periodo = comando[1], int(comando[2]), comando[3]
                    resposta = self.cancelar_reserva(cpf, num_quarto, periodo)
                elif comando[0] == "CONSULTAR" and len(comando) >= 2:
                    cpf = comando[1]
                    resposta = "\n".join(self.consultar_reserva(cpf))
                elif comando[0] == "SAIR":
                    conexao.close()
                    return
                
                conexao.send(resposta.encode())
            except Exception as e:
                conexao.send(f"Erro: {str(e)}".encode())



if __name__ == "__main__":
    porta = int(input("Digite a porta para o servidor: "))  # Pergunta ao usuário a porta desejada
    Servidor(porta=porta).start()
