import socket
import sys

class Cliente:
    def __init__(self, host='127.0.0.1', porta=12345):
        self.host = host
        self.porta = porta

    def conectar(self):
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect((self.host, self.porta))

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
                self.enviar_requisicao(f"CADASTRAR {cpf} {nome} {telefone} {senha}")
            
            elif opcao == "2":
                cpf = input("Digite seu CPF: ").strip()
                senha = input("Digite a senha: ").strip()
                self.enviar_requisicao(f"LOGIN {cpf} {senha}")
            
            elif opcao == "3":
                """ 
                Fazer verificaçoes no cliente (nao exclui as do servidor)
                """
                # cpf = input("Digite seu CPF: ")
                data_entrada = input("Data de entrada (ex: 15/03/2025): ").strip()
                data_saida = input("Data de saída (ex: 16/03/2025): ").strip()
                num_quarto = input("Número do quarto: ").strip()
                # self.enviar_requisicao(f"RESERVAR {cpf} {num_quarto} {data_entrada} {data_saida}")
                self.enviar_requisicao(f"RESERVAR {num_quarto} {data_entrada} {data_saida}")

            elif opcao == "4":
                # cpf = input("Digite seu CPF: ")
                data_entrada = input("Data de entrada (ex: 15/03/2025): ").strip()
                num_quarto = input("Número do quarto para cancelar: ").strip()
                # self.enviar_requisicao(f"CANCELAR {cpf} {num_quarto} {data_entrada}")
                self.enviar_requisicao(f"CANCELAR {num_quarto} {data_entrada}")

            elif opcao == "5":
                # cpf = input("Digite seu CPF: ")
                ano = input("Digite o ano da reserva: ").strip()
                self.enviar_requisicao(f"CONSULTAR {ano}")
                # self.enviar_requisicao(f"CONSULTAR {cpf} {ano}")
            elif opcao == "6":
                self.enviar_requisicao(f'LISTAR')

            elif opcao == "7":
                num_quarto = input('Qual o numero do quarto que dejesa adicionar: ')
                preco = input('Valor do quarto: ') 
                cama =  input('Quantidade de camas: ')
                self.enviar_requisicao(f'ADICIONAR {num_quarto} {preco} {cama}')

            elif opcao == "8":
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
