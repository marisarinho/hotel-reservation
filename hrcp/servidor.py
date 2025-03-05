import socket
import threading
from avl import AVLTree
from hashTable import HashTable
from fila import Fila
from datetime import datetime

class User:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def __str__(self):
        return f"{self.nome} {self.cpf} {self.telefone}"
        
class Quarto:
    def __init__(self, num_quarto, preco, camas):
        self.num_quarto = num_quarto
        self.disponibilidade = True
        self.preco = preco
        self.camas = camas

    @staticmethod
    def gerar_quartos(hash_table, quantidade=20):
        for i in range(1, quantidade + 1):
            num_quarto = 100 + i
            preco = 150 + (i % 3) * 50  # Alterna preços automaticamente
            camas = (i % 3) + 1  # Alterna entre 1, 2 e 3 camas
            hash_table.insert(num_quarto, Quarto(num_quarto, preco, camas))
            # fila_reservas.enfileirar(Quarto)

class Reserva:
    def __init__(self, quarto: Quarto, periodo, user: User):
        self.quarto = quarto
        self.periodo = periodo
        self.user = user

    def __lt__(self, other):
        return self.periodo < other.periodo
    
    def __eq__(self, other):
        return self.periodo == other.periodo
    
    def __str__(self):
        return f"Reserva(quarto={self.quarto}, periodo={self.periodo}, user={self.user})"
    
    def __repr__(self):
        return self.__str__()
    
    def periodo_conflita(self, outra_reserva):
      return not (self.periodo_fim < outra_reserva.periodo_inicio or self.periodo_inicio > outra_reserva.periodo_fim)

class Servidor:

    def __init__(self, host='localhost', porta=12345):
        self.host = host
        self.porta = porta
        self.hash_usuarios = HashTable(capacity=50)
        self.hash_quartos = HashTable(capacity=25)
        self.arvore_avl_reservas = AVLTree()
        self.fila_reservas = Fila()
        Quarto.gerar_quartos(self.hash_quartos)  # Corrigido: agora passa um instância



   
    def realizar_reserva(self, cpf, num_quarto, periodo): 
        periodo_inicio, periodo_fim = periodo.split("-")
        periodo_tupla = (periodo_inicio, periodo_fim)
        
        # Buscando o usuário
        usuario = None
        try:
            usuario = self.hash_usuarios.get(cpf)
        except KeyError as e:
            print("Usuário não encontrado", e)
        if usuario is None:
            usuario = User(nome="Usuário Padrão", cpf=cpf, telefone="0000-0000")
            self.hash_usuarios.insert(cpf, usuario)

        # Buscando o quarto
        quarto = None
        try:
            quarto = self.hash_quartos.get(num_quarto)
        except KeyError as e:
            print("Quarto não encontrado", e)
        if quarto is None:
            raise ValueError("Quarto não encontrado!")

        # Criando a reserva
        reserva = Reserva(quarto, periodo_tupla, usuario)

       
        reservas_existentes = self.arvore_avl_reservas.search_all(reserva) 
        for r in reservas_existentes:
            if r.quarto == reserva.quarto:  
                if reserva.periodo_conflita(reserva):  
                    raise ValueError(f"O quarto {num_quarto} já está reservado para o período solicitado!")

        self.arvore_avl_reservas.add(reserva)
        quarto.disponibilidade = False  

        print(self.arvore_avl_reservas)
        
        return f"Reserva realizada com sucesso para o quarto {num_quarto}!"



    def cancelar_reserva(self, cpf, num_quarto, periodo):

        reservas_usuario = self.consultar_reserva(cpf)
        periodo_inicio, periodo_fim = periodo.split("-")
        periodo_tupla = (periodo_inicio, periodo_fim)

        if reservas_usuario:
            for r in self.arvore_avl_reservas:
                if r.user.cpf == cpf and r.quarto.num_quarto == num_quarto and r.periodo == periodo_tupla:
                    self.arvore_avl_reservas.delete(r)
                    quarto = self.hash_quartos.get(num_quarto)
                    if quarto:
                        quarto.disponibilidade = True
                    
                    return f"Reserva do quarto {num_quarto} para o período {periodo} cancelada com sucesso."
        
        return f"Nenhuma reserva encontrada para o CPF {cpf} no quarto {num_quarto} para o período {periodo}."
        # reservas = [r for r in self.arvore_avl_reservas if r.user.cpf == cpf]
        # if reservas:
        #     return [f"Quarto {r.quarto.num_quarto} reservado de {r.periodo[0]} até {r.periodo[1]}" for r in reservas]
            # return ["Não há reservas para este CPF."]



    def consultar_reserva(self, cpf):
        """
        Consulta todas as reservas associadas a um CPF na árvore AVL de reservas.
        """
        usuario_encontrado = self.hash_usuarios.search(cpf)
        if not usuario_encontrado:
            return f"Nenhum usuário encontrado com o CPF {cpf}."
        peguei_usuario = self.hash_usuarios.get(cpf)
        reserva_achada = self.buscar_reservas_por_cpf(peguei_usuario.cpf)
        for r in reserva_achada:
            print(f'quarto{r.num_quarto}, periodo{r.periodo}')
            
        
        
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
                dados = conexao.recv(1024).decode()
                if not dados:
                    break

                dados = dados.strip("\r\n")
                
                comando = dados.split()
                resposta = "Comando inválido."

                if comando[0] == "RESERVAR" and len(comando) >= 4:
                    cpf, num_quarto, periodo = comando[1], int(comando[2]), comando[3]
                    resposta = self.realizar_reserva(cpf, num_quarto, periodo)
                
                elif comando[0] == "CANCELAR" and len(comando) >= 3:
                    cpf, num_quarto, periodo = comando[1], int(comando[2]), comando[3]
                    resposta = self.cancelar_reserva(cpf, num_quarto, periodo)
                elif comando[0] == "CONSULTAR" and len(comando) >= 1:
                    cpf = comando[1]
                    resposta = "\n".join(self.consultar_reserva(cpf))

                elif comando[0] == "LISTAR" and len(comando)>=1:
                    reposta = self.listar_quartos(fila_reservas)
                elif comando[0] == "SAIR":
                    conexao.close()
                    return
                
                conexao.send(resposta.encode())
            except Exception as e:
                conexao.send(f"Erro: {str(e)}".encode())



if __name__ == "__main__":
    porta = int(input("Digite a porta para o servidor: ")) 
    Servidor(porta=porta).start()
