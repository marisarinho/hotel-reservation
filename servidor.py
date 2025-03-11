import socket
import threading
from hashTable import HashTable
from user import User
from reserva import Reserva
from quarto import Quarto
from gerenciamento import GerenciadorReservas


class Servidor:

    def __init__(self, host='localhost', porta=12345):
        self.host = host
        self.porta = porta
        self.gerenciador = GerenciadorReservas()
        print(f"Gerenciador: {self.gerenciador}")
        
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
                    cpf, num_quarto, data_entrada , data_saida = comando[1], int(comando[2]), comando[3] , comando[4]
                    resposta = self.gerenciador.realizar_reserva(cpf, num_quarto,data_entrada,data_saida)
                
                elif comando[0] == "CANCELAR" and len(comando) >= 3:
                    cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    resposta = self.gerenciador.cancelar_reserva(cpf, num_quarto,data_entrada,data_saida)

                elif comando[0] == "CONSULTAR" and len(comando) >= 1:
                    cpf = comando[1]
                    resposta = self.gerenciador.consultar_reserva(cpf)

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
