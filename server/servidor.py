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
    def __init__(self, host="0.0.0.0", porta=12345):
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
                thread_cliente = threading.Thread(
                    target=self.lidar_com_cliente, args=(cliente,)
                )
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
                command = "q"

            if command.strip().lower() == "q":
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

                if comando[0] == "CADASTRAR" and len(comando) >= 5:
                    _, cpf, nome, telefone, senha = comando
                    try:
                        if cliente.esta_logado():
                            resposta = "401| Já está logado"
                        else:
                            self.gerenciador.add_hospede(cpf, nome, telefone, senha)
                            cliente.cpf = cpf
                            cliente.nome = nome
                            resposta = f"211| cadastrar hóspede"
                    except Exception as e:
                        resposta = e.__str__()
                        print(self.gerenciador.mostrar_hospede())

                elif comando[0] == "LOGIN" and len(comando) == 3:
                    _, cpf, senha = comando
                    hospede = self.gerenciador.buscar_usuario(cpf)
                    try:
                        if cliente.esta_logado():
                            resposta = f"411| Já está logado"

                        elif not hospede or hospede.senha != senha:
                            raise ErroDeReserva("412| CPF ou senha errados.")
                        else:
                            cliente.nome = hospede.nome
                            cliente.cpf = cpf
                            resposta = f"211| efetuadar login"
                    except Exception as e:
                        resposta = e.__str__()

                elif comando[0] == "RESERVAR" and len(comando) == 4:
                    if not cliente.esta_logado():
                        resposta = f"421| Precisa estar logado"
                    else:
                        _, num_quarto, data_entrada, data_saida = comando
                        try:
                            self.gerenciador.realizar_reserva(
                                cliente.cpf, int(num_quarto), data_entrada, data_saida
                            )
                            resposta = "221| realizar reserva"
                        except ErroDeReserva as e:
                            resposta = e.__str__()

                elif comando[0] == "CANCELAR" and len(comando) >= 3:
                    _, num_quarto, data_entrada = comando

                    try:
                        if not cliente.esta_logado():
                            raise ErroDeReserva("431| Precisa estar logado.")

                        if not num_quarto.isdigit():
                            raise ErroDeReserva("432| Reserva não encontrada.")
                        num_quarto = int(num_quarto)

                        self.gerenciador.cancelar_reserva(
                            cliente.cpf, int(num_quarto), data_entrada
                        )

                        resposta = f"231| cancelar reserva"
                    except ErroDeReserva as e:
                        resposta = e.__str__()

                elif comando[0] == "CONSULTAR" and len(comando) >= 2:
                    ano = comando[1]
                    try:
                        if not cliente.esta_logado():
                            raise ErroDeReserva("441| Precisa estar logado.")

                        if not ano.isdigit():
                            raise ErroDeReserva("442| Reservas não encontradas.")

                        usuario = self.gerenciador.buscar_usuario(cliente.cpf)

                        if not usuario:
                            raise ErroDeReserva("443| Hóspede não encontrado.")

                        reservas = self.gerenciador.consultar_reserva(
                            cliente.cpf, int(ano)
                        )
                        if not reservas:
                            raise ErroDeReserva("442| Reservas não encontradas.")

                        resposta = f"241| "
                        for reserva in reservas:
                            resposta += f"- Quarto {reserva.quarto.num_quarto}, Entrada: {reserva.data_entrada}, Saída: {reserva.data_saida}\n"

                    except ErroDeReserva as e:
                        resposta = e.__str__()

                elif comando[0] == "ADICIONAR" and len(comando) >= 4:
                    _, num_quarto, preco, cama = comando
                    try:
                        if not num_quarto.isdigit():
                            raise ErroDeReserva("452| Formato inválido para quarto.")
                        
                        self.gerenciador.adicionar_quarto(int(num_quarto), preco, cama)
                        resposta = f"251| {self.gerenciador.mostrar_quartos()}"
                    except Exception as e:
                        resposta = e.__str__()


                elif comando[0] == "LISTAR":
                    resposta = f"261| {self.gerenciador.mostrar_quartos()}"

                elif comando[0] == "SAIR":
                    resposta = "271| Conexão encerrada pelo cliente."
                    try:
                        cliente.socket.sendall(resposta.encode())
                        cliente.socket.close()
                        self.clients.remove(cliente)
                    except Exception:
                        resposta = "471| Erro ao encerrar a conexão"
                    return

                cliente.socket.sendall(resposta.encode())

            except Exception as e:
                cliente.socket.sendall(f"500| Erro interno: {str(e)}".encode())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        porta = int(sys.argv[1])
        Servidor(porta=porta).start()
    else:
        Servidor().start()
