import socket
import threading
import sys
from gerenciamento import GerenciadorReservas
from exception import ErroDeReserva

class Cliente:
    def __init__(self, socket: socket, address: tuple[str, int], nome="", cpf=""):
        self.socket = socket
        self.address = address
        self.nome = nome
        self.cpf = cpf

    def __eq__(self, other: "Cliente") -> bool:
        return self.cpf == other.cpf


class Servidor:

    def __init__(self, host='0.0.0.0', porta=12345):
        self.host = host
        self.porta = porta
        self.gerenciador = GerenciadorReservas()
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: list[Cliente] = []
    
    def start(self):
        self.servidor_socket.bind((self.host, self.porta))
        self.servidor_socket.listen(5)
        print("Servidor iniciado.")
        threading.Thread(target=self.__parar_servidor, daemon=True).start()
        while True:
            try:
                conexao, endereco = self.servidor_socket.accept()
                print(f"Cliente conectado: {endereco}")
                cliente = Cliente(conexao, endereco)
                self.clients.append(cliente)
                thread_cliente = threading.Thread(target=self.lidar_com_cliente, args=(cliente,))
                thread_cliente.start()
            except (OSError, KeyboardInterrupt):
                break


    def __parar_servidor(self) -> None:
        while True:
            print("Digite 'q' para encerrar o servidor.")
            try:
                command = input()
            except EOFError:
                command = 'q'
                
            if command.strip().lower() == 'q':
                print("Encerrando servidor...")
                break

        for client in self.clients:
            client.socket.close()
        self.servidor_socket.close()

    def lidar_com_cliente(self, cliente: Cliente):
        while True:
            try:
                dados = cliente.socket.recv(1024).decode().strip("\r\n")
            except ConnectionAbortedError:
                break
        
            if not dados:
                break
            
            try:
                comando = dados.split()
                mensagem = "Comando inválido."
                
                if comando[0] == "CADASTRAR" and len(comando) >= 4:
                    # cpf, nome, telefone = comando[1], comando[2], comando[3]
                    _, cpf, nome, telefone = comando
                    print(f"Chamando add_hospede com CPF: {cpf}, Nome: {nome}, Telefone: {telefone}")
                    try:    
                        if cliente.cpf != "" and cliente.nome != "":
                            raise ErroDeReserva("Hóspede (você) já cadastrado.")
                        
                        self.gerenciador.add_hospede(cpf, nome, telefone)
                        # Agora mostramos os hóspedes cadastrados corretamente
                        cliente.cpf = cpf
                        cliente.nome = nome
                        mensagem = f"200 OK\nHóspede {nome} cadastrado com sucesso!\n{self.gerenciador.mostrar_hospede()}"
                    except Exception as e:
                        mensagem = f"Erro- 500\nAo cadastrar hóspede: {str(e)}"

                
                elif comando[0] == "RESERVAR" and len(comando) >= 4:
                    # cpf, num_quarto, data_entrada, data_saida = comando[1], int(comando[2]), comando[3], comando[4]
                    _, num_quarto, data_entrada, data_saida = comando
                    num_quarto = int(num_quarto)
                    try:
                        # if cpf != cliente.cpf:
                        #     raise ErroDeReserva("(Não autorizado) CPF é de outro hóspede.")
                        
                        self.gerenciador.realizar_reserva(cliente.cpf, num_quarto, data_entrada, data_saida)
                        mensagem = f"200 OK\n Reserva confirmada para CPF {cliente.cpf}, Quarto {num_quarto}, de {data_entrada} a {data_saida}."
                    except ErroDeReserva as e:
                        mensagem = f"ERRO- 409\n {e.__str__()}"

                elif comando[0] == "CANCELAR" and len(comando) >= 3:
                    # cpf, num_quarto, data_entrada = comando[1], int(comando[2]), comando[3]
                    _, num_quarto, data_entrada = comando
                    num_quarto = int(num_quarto) # declarando pra nao dar indefinido
                    try:
                        # if cpf != cliente.cpf:
                        #     raise ErroDeReserva("(Não autorizado) CPF é de outro hóspede.")
                        self.gerenciador.cancelar_reserva(cliente.cpf, num_quarto, data_entrada)
                        mensagem = f"200 OK\n Reserva do Quarto {num_quarto} para CPF {cliente.cpf} cancelada."
                    except ErroDeReserva as e:
                        mensagem = f"ERRO- 404\n Reserva não encontrada: {str(e)}"
            
                elif comando[0] == "ADICIONAR" and len(comando)>=4:
                    _, num_quarto, preco, cama = comando
                    num_quarto = int(num_quarto)
                    self.gerenciador.adicionar_quarto(num_quarto,preco,cama)
                    mensagem = f'({self.gerenciador.mostrar_quartos()}'

                elif comando[0] == "CONSULTAR" and len(comando) >= 2:
                    # cpf = comando[1]
                    ano = int(comando[1])
                    usuario = self.gerenciador.buscar_usuario(cliente.cpf)
                    
                    try:
                        if not usuario:
                            raise ErroDeReserva("Hóspede não encontrado.")
                        
                        # if cpf != cliente.cpf:
                        #     raise ErroDeReserva("(Não autorizado) CPF é de outro hóspede.")
                        
                        reservas = self.gerenciador.consultar_reserva(cliente.cpf, ano)
                        if not reservas:
                            raise ErroDeReserva(f"Usuário {usuario.nome} (CPF: {cliente.cpf}) está cadastrado, mas não possui reservas.")
                        
                        mensagem = f"200 OK\n Reservas para {usuario.nome} (CPF: {cliente.cpf}):\n"
                        for reserva in reservas:
                            mensagem += f"- Quarto {reserva.quarto.num_quarto}, Entrada: {reserva.data_entrada}, Saída: {reserva.data_saida}\n"

                    except ErroDeReserva as e:
                        mensagem = f"ERRO- 404\n {str(e)}"

                elif comando[0] == "SAIR":
                    mensagem = "🔌 Conexão encerrada pelo cliente."
                    cliente.socket.send(mensagem.encode())
                    cliente.socket.close()
                    return

                cliente.socket.send(mensagem.encode())
        
            except Exception as e:
                cliente.socket.send(f"500| Erro interno: {str(e)}".encode())

if __name__ == "__main__":
    if len(sys.argv)>1:
        porta = int(sys.argv[1])
        Servidor(porta=porta).start()
    else:
        Servidor().start()
    
