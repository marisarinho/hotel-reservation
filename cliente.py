import socket
import sys

class Cliente:
    def __init__(self, host='127.0.0.1', porta=12345):
        self.host = host
        self.porta = porta

    def conectar(self):
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect((self.host, self.porta))

    # def enviar_requisicao(self, mensagem):
    #     self.cliente_socket.send(mensagem.encode())  # f"RESERVAR {cpf} {num_quarto} {periodo}"
    #     resposta = self.cliente_socket.recv(1024).decode()
    #     print("Resposta do servidor:", resposta)

    def enviar_requisicao(self, mensagem):
        mensagem += "\r\n" # Adiciona o terminador conforme exigido
        self.cliente_socket.send(mensagem.encode())  
        resposta = self.cliente_socket.recv(1024).decode()
        print("📩 Resposta do servidor:", resposta)

    def fechar_conexao(self):
        self.cliente_socket.close()

    def menu(self):
        while True:
            print("\n--- Sistema de Reservas ---")
            print("1. Cadastrar hóspede")
            print("2. Fazer reserva")
            print("3. Cancelar reserva")
            print("4. Consultar reserva por CPF")
            print("5. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                cpf = input("Digite seu CPF: ")
                nome = input("Digite seu nome: ")
                telefone = input("Digite seu telefone: ")
                self.enviar_requisicao(f"CADASTRAR {cpf} {nome} {telefone}")
            
            elif opcao == "2":
                cpf = input("Digite seu CPF: ")
                num_quarto = input("Número do quarto: ")
                data_entrada = input("Data de entrada (ex: 2025-03-15):")
                data_saida = input("Data de saída (ex: 2025-03-15):")
                self.enviar_requisicao(f"RESERVAR {cpf} {num_quarto} {data_entrada} {data_saida}")

            elif opcao == "3":
                cpf = input("Digite seu CPF: ")
                num_quarto = input("Número do quarto para cancelar: ")
                data_entrada = input("Data de entrada (ex: 2025-03-15):")
                data_saida = input("Data de saída (ex: 2025-03-15):")
                self.enviar_requisicao(f"CANCELAR {cpf} {num_quarto} {data_entrada} {data_saida}")

            elif opcao == "4":
                cpf = input("Digite seu CPF: ")
                ano = input("Digite o ano da reserva: ")
                self.enviar_requisicao(f"CONSULTAR {cpf} {ano}")

                
            elif opcao == "5":
                print("Encerrando conexão...")
                self.fechar_conexao()
                break

            else:
                print("Opção inválida, tente novamente.")


if __name__ == "__main__": 

    host = '127.0.0.1'
    porta = 12345  

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        porta = int(sys.argv[2])
    
    cliente = Cliente(host=host, porta=porta)
    cliente.conectar()
    cliente.menu()
