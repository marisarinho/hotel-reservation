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
                mensagem = "Comando inválido."

                # if comando[0] == "CADASTRAR" and len(comando) >= 4:
                #     cpf, nome, telefone = comando[1], comando[2], comando[3]
                #     try:
                #         resposta = self.gerenciador.add_hospede(cpf, nome, telefone)
                #         # mensagem = f"\nHóspede {nome} cadastrado com sucesso!"
                #         mensagem = f'200 OK ({self.gerenciador.mostrar_hospede()}'
                #     except Exception as e:
                #         mensagem = f"Erro- 500\n ao cadastrar hóspede: {str(e)}"
                
                if comando[0] == "CADASTRAR" and len(comando) >= 4:
                    cpf, nome, telefone = comando[1], comando[2], comando[3]
                    print(f"Chamando add_hospede com CPF: {cpf}, Nome: {nome}, Telefone: {telefone}")

                    try:    
                    
                            resposta = self.gerenciador.add_hospede(cpf, nome, telefone)
                            # Agora mostramos os hóspedes cadastrados corretamente
                            mensagem = f"200 OK\nHóspede {nome} cadastrado com sucesso!\n{self.gerenciador.mostrar_hospede()}"
                    except Exception as e:
                            mensagem = f"Erro- 500\nAo cadastrar hóspede: {str(e)}"

                
                elif comando[0] == "RESERVAR" and len(comando) >= 5:
                    cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    try:
                        self.gerenciador.realizar_reserva(cpf, num_quarto, data_entrada, data_saida)
                        mensagem = f"200 OK\n Reserva confirmada para CPF {cpf}, Quarto {num_quarto}, de {data_entrada} a {data_saida}."
                    except ErroDeReserva as e:
                        mensagem = f"ERRO- 409\n {str(e)}"

                elif comando[0] == "CANCELAR" and len(comando) >= 5:
                    cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    try:
                        self.gerenciador.cancelar_reserva(cpf, num_quarto, data_entrada, data_saida)
                        mensagem = f"200 OK\n Reserva do Quarto {num_quarto} para CPF {cpf} cancelada."
                    except ErroDeReserva as e:
                        mensagem = f"ERRO- 404\n Reserva não encontrada: {str(e)}"
            
                elif comando[0] == "ADICIONAR" and len(comando)>=4:
                    num_quarto,preco,cama = int(comando[1]),comando[2],comando[3]
                    self.gerenciador.adicionar_quarto(num_quarto,preco,cama)
                    mensagem = f'({self.gerenciador.mostrar_quartos()}'

                elif comando[0] == "CONSULTAR" and len(comando) >= 3:
                    cpf = comando[1]
                    ano = int(comando[2])  
                    usuario = self.gerenciador.buscar_usuario(cpf)

                    if not usuario:
                        mensagem = "ERRO- 404\n Nenhum usuário encontrado com este CPF."
                    else:
                        try:
                            reservas = self.gerenciador.consultar_reserva(cpf, ano)
                            if not reservas:
                                raise ErroDeReserva(f"Usuário {usuario.nome} (CPF: {cpf}) está cadastrado, mas não possui reservas.")
                            
                            mensagem = f"200 OK\n Reservas para {usuario.nome} (CPF: {cpf}):\n"
                            for reserva in reservas:
                                mensagem += f"- Quarto {reserva.quarto.get_num_quarto()}, Entrada: {reserva.data_entrada}, Saída: {reserva.data_saida}\n"

                        except ErroDeReserva as e:
                            mensagem = f"ERRO- 404\n {str(e)}"

                elif comando[0] == "SAIR":
                    mensagem = "🔌 Conexão encerrada pelo cliente."
                    conexao.send(mensagem.encode())
                    conexao.close()
                    return

                conexao.send(mensagem.encode())
            
            except Exception as e:
                conexao.send(f"500| Erro interno: {str(e)}".encode())

if __name__ == "__main__":
    if len(sys.argv)>1:
        porta = int(sys.argv[1])
        Servidor(porta=porta).start()
    else:
        Servidor().start()
    
