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

    def __eq__(self, outro: "Cliente") -> bool:
        return self.cpf == outro.cpf

    def esta_logado(self) -> bool:
        """Verifica se o usuário está logado."""
        return self.nome != "" and self.cpf != ""

class Servidor:
    def __init__(self, host='0.0.0.0', porta=12345):
        self.host = host
        self.porta = porta
        self.gerenciador = GerenciadorReservas()
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: list[Cliente] = []

    def start(self):
        """Inicia o servidor."""
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
        """Para o servidor."""
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
        """Lida com clientes em thread."""
        while True:
            try:
                dados = cliente.socket.recv(1024).decode().strip("\r\n")
            except ConnectionAbortedError:
                break

            if not dados:
                break

            try:
                comando = dados.split("|")
                if not comando:
                    continue

                resposta = "400| Comando inválido"

                if comando[0] == "CADASTRAR" and len(comando) == 5:
                    _, cpf, nome, telefone, senha = comando
                    try:
                        if cliente.esta_logado():
                            resposta ='400'
                            # raise ErroDeReserva("Você já está cadastrado.")

                        self.gerenciador.add_hospede(cpf, nome, telefone, senha)
                        cliente.cpf = cpf
                        cliente.nome = nome
                        resposta = f"200"
                    except Exception as e:
                        resposta = f"400" 
                        print(self.gerenciador.mostrar_hospede())
                    

                elif comando[0] == "LOGIN" and len(comando) == 3:
                    _, cpf, senha = comando
                    hospede = self.gerenciador.buscar_usuario(cpf)
                    try:
                        if cliente.esta_logado():
                           resposta = f'400'

                        if not hospede or hospede.senha != senha:
                            raise ErroDeReserva("CPF ou senha errados.")

                        cliente.nome = hospede.nome
                        cliente.cpf = cpf
                        resposta = f"200"
                    except Exception as e:
                        resposta = f"401"

                elif comando[0] == "RESERVAR" and len(comando) == 4:
                    if not cliente.esta_logado():
                        resposta = "401"
                    else:
                        _, num_quarto, data_entrada, data_saida = comando
                        try:
                            self.gerenciador.realizar_reserva(cliente.cpf, int(num_quarto), data_entrada, data_saida)
                            resposta = f"201"
                        except ErroDeReserva as e:
                            resposta = f"409| {str(e)}"

                elif comando[0] == "CANCELAR" and len(comando) >= 3:
                    # cpf, num_quarto, data_entrada = comando[1], int(comando[2]), comando[3]
                    _, num_quarto, data_entrada = comando
                    try:
                        if not isinstance(int(num_quarto),int):
                            raise ErroDeReserva('quarto invalido')
                    except Exception as e:
                            raise ErroDeReserva('quarto invalido')
                    
                    print('testando')
                    num_quarto = int(num_quarto) # declarando pra nao dar indefinido
                    try:
                        if not cliente.esta_logado():
                            raise ErroDeReserva("É necessário fazer login.")
                    
                        self.gerenciador.cancelar_reserva(cliente.cpf, num_quarto, data_entrada)
                    
                        resposta = f"200| Reserva do Quarto {num_quarto} para CPF {cliente.cpf} cancelada."
                    except ErroDeReserva as e:
                        resposta = f"400| {str(e)}"

                        

                elif comando[0] == "CONSULTAR" and len(comando) >= 2:
                    # cpf = comando[1]
                    ano = int(comando[1])
                    usuario = self.gerenciador.buscar_usuario(cliente.cpf)
                    
                    try:
                        if not cliente.esta_logado():
                            raise ErroDeReserva("É necessário fazer login.")
                        
                        if not usuario:
                            raise ErroDeReserva("Hóspede não encontrado.")
                        
                        reservas = self.gerenciador.consultar_reserva(cliente.cpf, ano)
                        if not reservas:
                            raise ErroDeReserva(f"Usuário {usuario.nome} (CPF: {cliente.cpf}) está cadastrado, mas não possui reservas.")
                        
                    
            
                        resposta = f"200| Reservas para {usuario.nome} (CPF: {cliente.cpf}):\n"
                        for reserva in reservas:
                            resposta += f"- Quarto {reserva.quarto.num_quarto}, Entrada: {reserva.data_entrada}, Saída: {reserva.data_saida}\n"
                        
                    except ErroDeReserva as e:
                        resposta  = f"400| Reserva não encontrada"

                        mensagem = str(e.args[0])

                elif comando[0] == "ADICIONAR" and len(comando)>=4:
                    _, num_quarto, preco, cama = comando
                    num_quarto = int(num_quarto)
                    self.gerenciador.adicionar_quarto(num_quarto,preco,cama)
                    resposta = f'({self.gerenciador.mostrar_quartos()}'

                elif comando[0] == "LISTAR":
                    resposta = f"200| {self.gerenciador.mostrar_quartos()}"

                elif comando[0] == "SAIR":
                    resposta = "200| Conexão encerrada pelo cliente."
                    cliente.socket.send(resposta.encode())
                    cliente.socket.close()
                    self.clients.remove(cliente)
                    return

                cliente.socket.send(resposta.encode())

            except Exception as e:
                cliente.socket.send(f"500| Erro interno: {str(e)}".encode())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        porta = int(sys.argv[1])
        Servidor(porta=porta).start()
    else:
        Servidor().start()
