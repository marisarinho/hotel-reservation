import socket
import threading
from hrcp.estruturasDeDados.avl import AVLTree
from hrcp.estruturasDeDados.hashTable import HashTable
from hrcp.estruturasDeDados.fila import Fila
from hrcp.gerenciamento.user import User
from hrcp.gerenciamento.reserva import Reserva
from hrcp.gerenciamento.quarto import Quarto
from hrcp.gerenciamento.gerenciamento import GerenciadorReservas

    # @staticmethod
    # def gerar_quartos(hash_table, quantidade=20):
    #     for i in range(1, quantidade + 1):
    #         num_quarto = 100 + i
    #         preco = 150 + (i % 3) * 50  # Alterna preços automaticamente
    #         camas = (i % 3) + 1  # Alterna entre 1, 2 e 3 camas
    #         hash_table.insert(num_quarto, Quarto(num_quarto, preco, camas))
    #         # fila_reservas.enfileirar(Quarto)



class Servidor:

    def __init__(self, host='localhost', porta=12345):
        self.host = host
        self.porta = porta
        

            
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
                
                elif comando[0] == "CANCELAR" and len(comando) >= 3:
                    cpf, num_quarto, periodo = comando[1], int(comando[2]), comando[3]
                    resposta = self.cancelar_reserva(cpf, num_quarto, periodo)
                elif comando[0] == "CONSULTAR" and len(comando) >= 1:
                    cpf = comando[1]
                    resposta = "\n".join(self.consultar_reserva(cpf))

                # elif comando[0] == "LISTAR" and len(comando)>=1:
                    # reposta = self.listar_quartos(fila_reservas)
                elif comando[0] == "SAIR":
                    conexao.close()
                    return
                
                conexao.send(resposta.encode())
            except Exception as e:
                conexao.send(f"Erro: {str(e)}".encode())



if __name__ == "__main__":
    porta = int(input("Digite a porta para o servidor: ")) 
    Servidor(porta=porta).start()
