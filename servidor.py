import socket
import threading
import sys
from gerenciamento import GerenciadorReservas
from exception import ErroDeReserva


class Servidor:

    def __init__(self, host='0.0.0.0', porta=12345):
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
                dados = conexao.recv(1024).decode().strip("\r\n")
                if not dados:
                    break
                
                comando = dados.split()
                resposta = "Comando inválido."

                if comando[0] == "RESERVAR" and len(comando) >= 4:
                    cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    resposta = self.gerenciador.realizar_reserva(cpf, num_quarto, data_entrada, data_saida)
                
                elif comando[0] == "CANCELAR" and len(comando) >= 4:
                    cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    resposta = self.gerenciador.cancelar_reserva(cpf, num_quarto, data_entrada, data_saida)
                
                elif comando[0] == "CONSULTAR" and len(comando) >= 1:
                    cpf = comando[1]
                    usuario = self.gerenciador.buscar_usuario(cpf)
                    if not usuario:
                        resposta = '0'
                    else:
                        reservas = self.gerenciador.consultar_reserva(cpf)
                        if not reservas:
                            resposta = "Sem reservas"
                        else:
                            resposta = f"Usuário: {usuario.cpf}, Nome: {usuario.nome}, Telefone: {usuario.telefone}, Reservas: \n"
                            for reserva in reservas:
                                resposta +=  f"Quarto: {reserva.quarto.get_num_quarto()}, Data de entrada: {reserva.data_entrada}, Data de saída: {reserva.data_saida} \n"
                
                elif comando[0] == "SAIR":
                    conexao.close()
                    return
                
                conexao.send(resposta.encode())
            except Exception as e:
                conexao.send(f"Erro: {str(e)}".encode())


if __name__ == "__main__":
    if len(sys.argv)>1:
        porta = int(sys.argv[1])
        Servidor(porta=porta).start()
    else:
        Servidor().start()
    
