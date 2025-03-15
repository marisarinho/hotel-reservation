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
                codigo = "400"  # Código de erro por padrão
                mensagem = "Comando inválido."

                if comando[0] == "RESERVAR" and len(comando) >= 5:
                    cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    try:
                        self.gerenciador.realizar_reserva(cpf, num_quarto, data_entrada, data_saida)
                        codigo = "200"
                        mensagem = f" Reserva confirmada para CPF {cpf}, Quarto {num_quarto}, de {data_entrada} a {data_saida}."
                    except ErroDeReserva as e:
                        codigo = "409"
                        mensagem = f"⚠ Conflito: {str(e)}"

                elif comando[0] == "CANCELAR" and len(comando) >= 5:
                    cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    try:
                        self.gerenciador.cancelar_reserva(cpf, num_quarto, data_entrada, data_saida)
                        codigo = "200"
                        mensagem = f" Reserva do Quarto {num_quarto} para CPF {cpf} cancelada."
                    except ErroDeReserva as e:
                        codigo = "404"
                        mensagem = f"⚠ Reserva não encontrada: {str(e)}"

                elif comando[0] == "CONSULTAR" and len(comando) >= 2:
                    cpf = comando[1]
                    usuario = self.gerenciador.buscar_usuario(cpf)
                    if not usuario:
                        codigo = "404"
                        mensagem = " Nenhum usuário encontrado com este CPF."
                    else:
                        reservas = self.gerenciador.consultar_reserva(cpf)
                        if not reservas:
                            codigo = "200"
                            mensagem = f" Usuário {usuario.nome} (CPF: {cpf}) não possui reservas."
                        else:
                            codigo = "200"
                            mensagem = f" Reservas para {usuario.nome} (CPF: {cpf}):\n"
                            for reserva in reservas:
                                mensagem += f"- Quarto {reserva.quarto.get_num_quarto()}, Entrada: {reserva.data_entrada}, Saída: {reserva.data_saida}\n"

                elif comando[0] == "SAIR":
                    codigo = "200"
                    mensagem = "🔌 Conexão encerrada pelo cliente."
                    conexao.send(f"{codigo}|{mensagem}".encode())
                    conexao.close()
                    return

                conexao.send(f"{codigo}|{mensagem}".encode())
            
            except Exception as e:
                conexao.send(f"500| Erro interno: {str(e)}".encode())


if __name__ == "__main__":
    if len(sys.argv)>1:
        porta = int(sys.argv[1])
        Servidor(porta=porta).start()
    else:
        Servidor().start()
    
