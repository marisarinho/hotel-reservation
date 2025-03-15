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
        mensagem += "\r\n"  # Adiciona o terminador correto
        self.cliente_socket.send(mensagem.encode())  
        resposta = self.cliente_socket.recv(1024).decode()

        partes = resposta.split("|", 1)
        if len(partes) == 2:
            codigo, mensagem = partes
          
            print("\n📩 Resposta do servidor:\n" + mensagem)
        else:
            print("\n⚠ Erro inesperado no formato da resposta.")



    def fechar_conexao(self):
        self.cliente_socket.close()

    def menu(self):
        while True:
            print("\n--- Sistema de Reservas ---")
            print("1. Fazer reserva")
            print("2. Cancelar reserva")
            print("3. Consultar reserva por CPF")
            print("4. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                cpf = input("Digite seu CPF: ")
                num_quarto = input("Número do quarto: ")
                data_entrada = input("Data de entrada (ex: 2025-03-15):")
                data_saida = input("Data de saida (ex: 2025-03-15):")
                self.enviar_requisicao(f"RESERVAR {cpf} {num_quarto} {data_entrada} {data_saida}")

            elif opcao == "2":
                cpf = input("Digite seu CPF: ")
                num_quarto = input("Número do quarto para cancelar: ")
                data_entrada = input("Data de entrada (ex: 2025-03-15):")
                data_saida = input("Data de saida (ex: 2025-03-15):")
                self.enviar_requisicao(f"CANCELAR {cpf} {num_quarto} {data_entrada} {data_saida}")

        
            elif opcao == "3":
                cpf = input("Digite seu CPF: ")
                self.enviar_requisicao(f"CONSULTAR {cpf}")

            elif opcao == "4":
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
