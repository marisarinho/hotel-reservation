from listaEnc import Lista
import socket
import json


class User:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def __eq__(self, other: "User") -> bool:
        return self.cpf == other.cpf

    def __lt__(self, other: "User") -> bool:
        return self.cpf < other.cpf
    
    def __str__(self) -> str:
        return json.dumps(self.__dict__)

class Cliente:

    def __init__(self):
        self.host = socket.gethostname()
        self.porta = 10000
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lista_reservas = Lista()

    def start(self):
        self.cliente_socket.connect((self.host, self.porta))

        while True:
            usuario = User("mariana", "283718371", "817382123")
            print(usuario)
            self.cliente_socket.send(f"teste__{str(usuario)}".encode())
            print("\nOpções:")
            print("""
                    CHECK <numeroDoQuarto>
                    RESERVE <numeroDoQuarto> <nome>
                    CANCEL <numeroDoQuarto>
                    LIST
                    QUIT
            """)
            opcao =  input("> ").strip().upper()
            comandos = opcao.split()

            if not comandos:
                print("Comando inválido. Tente novamente.")
                continue

            self.cliente_socket.send(f"HRCP {opcao}".encode())
            resposta = self.cliente_socket.recv(1024).decode()
            print(f"[Servidor]: {resposta}")

            if comandos[0] == "RESERVE" and resposta.startswith("20 OK"):
                self.lista_reservas.append(comandos[1])  # Adiciona o quarto na lista local

            elif comandos[0] == "CANCEL" and resposta.startswith("20 OK"):
                self.lista_reservas.remover(comandos[1])  # Remove o quarto da lista local

            elif comandos[0] == "QUIT":
                self.cliente_socket.close()
                break

if __name__ == '__main__':
    Cliente().start()