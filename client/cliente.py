import socket
import sys
from listaQuarto import listaquarto


class Cliente:
    def __init__(self, host="127.0.0.1", porta=12345):
        self.host = host
        self.porta = porta

    def conectar(self):
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect((self.host, self.porta))

    def fechar_conexao(self):
        self.cliente_socket.close()

    def enviar_requisicao(
        self, mensagem
    ):  # RESERVAR {num_quarto} {data_entrada} {data_saida}
        mensagem += "\r\n"
        self.cliente_socket.sendall(mensagem.encode())
        resposta = self.cliente_socket.recv(1024).decode()

        codigo, msg = resposta.split("|")
        if codigo.isdigit():
            codigo = int(codigo)
            if codigo in [401, 411]:
                print("Você já está logado.")
            elif codigo == 402:
                print("Este CPF já está em uso. Talvez você já tenha se cadastrado anteriormente.")
            elif codigo in [421, 431, 441]:
                print("Para usar esse recurso é necessário fazer login.")
            elif codigo in [403, 405]:
                print("Dados com formato inválido")
            else:
                print(msg.strip(" "))
        #     # Cadastro
        #     if codigo == 200:
        #         print("Hóspede cadastrado com sucesso")
        #     elif codigo == 401:
        #         print("Hóspede já está cadastrado.")
        #     elif codigo == 402:
        #         print("Telefone com formato inválido")
        #     elif codigo == 403:
        #         print('Cpf Inválido')

        #     # Login
        #     elif codigo == 211:
        #         print("Hóspede logado com sucesso!")
        #     elif codigo == 411:
        #         print("Hóspede já esta logado.")
        #     elif codigo == 412:
        #         print("Cpf ou senha incorretos.")
        #     elif codigo == 201:
        #         print("", msg.strip())
        #     elif codigo == 202:
        #         listaquarto(msg.strip())
        #     elif codigo == 400:
        #         print("Reserva não encontrada", msg.strip())
        #     elif codigo == 401:
        #         print("Acesso negado:", msg.strip())
        #     elif codigo == 409:
        #         print("Opção não é válida", msg.strip())
        #     elif codigo == 500:
        #         print("Erro interno do servidor:", msg.strip())
        #     else:
        #         print("Código desconhecido:", msg.strip())
        # else:
        #     print("Resposta do servidor:", resposta)

    def menu(self):
        while True:
            print("\n--- Sistema de Reservas ---")
            print("1. Cadastrar")
            print("2. Fazer login")
            print("3. Fazer reserva")
            print("4. Cancelar reserva")
            print("5. Consultar reserva por ano")
            print("6. Listar quartos")
            print("7. Adicionar quarto")
            print("8. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                cpf = input("Digite seu CPF: ").strip()
                nome = input("Digite seu nome: ").strip()
                telefone = input("Digite seu telefone: ").strip()
                senha = input("Digite a senha: ").strip()
                self.enviar_requisicao(f"CADASTRAR|{cpf}|{nome}|{telefone}|{senha}")

            elif opcao == "2":
                cpf = input("Digite seu CPF: ").strip()
                senha = input("Digite a senha: ").strip()
                self.enviar_requisicao(f"LOGIN|{cpf}|{senha}")

            elif opcao == "3":
                """
                Fazer verificaçoes no cliente (nao exclui as do servidor)
                """
                data_entrada = input("Data de entrada (ex: 15/03/2025): ").strip()
                data_saida = input("Data de saída (ex: 16/03/2025): ").strip()
                num_quarto = input("Número do quarto: ").strip()
                self.enviar_requisicao(
                    f"RESERVAR|{num_quarto}|{data_entrada}|{data_saida}"
                )

            elif opcao == "4":
                data_entrada = input("Data de entrada (ex: 15/03/2025): ").strip()
                num_quarto = input("Número do quarto para cancelar: ").strip()
                self.enviar_requisicao(f"CANCELAR|{num_quarto}|{data_entrada}")

            elif opcao == "5":
                # cpf = input("Digite seu CPF: ")
                ano = input("Digite o ano da reserva: ").strip()
                self.enviar_requisicao(f"CONSULTAR|{ano}")
                # self.enviar_requisicao(f"CONSULTAR {cpf} {ano}")
            elif opcao == "6":
                self.enviar_requisicao(f"LISTAR")

            elif opcao == "7":
                num_quarto = input("Qual o numero do quarto que dejesa adicionar: ")
                preco = input("Valor do quarto: ")
                cama = input("Quantidade de camas: ")
                self.enviar_requisicao(f"ADICIONAR|{num_quarto}|{preco}|{cama}")

            elif opcao == "8":
                print("Encerrando conexão...")
                self.enviar_requisicao("SAIR")
                self.fechar_conexao()
                break

            else:
                print("Opção inválida, tente novamente.")


if __name__ == "__main__":

    host = "127.0.0.1"
    porta = 12345

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        porta = int(sys.argv[2])

    cliente = Cliente(host=host, porta=porta)
    cliente.conectar()
    cliente.menu()
