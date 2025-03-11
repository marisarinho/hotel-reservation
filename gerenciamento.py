from hashTable import HashTable
from user import User
from reserva import Reserva
from listaOrd import Lista
from function import gerar_quartos
from datetime import datetime
from typing import Optional  #ideia pra trazer melhor a documentaçao?
from quarto import Quarto

class GerenciadorReservas:

    def __init__(self):
        # Se der erro foi aqui (especificando os tipos)
        self.hash_usuarios: HashTable[str, User] = HashTable(capacity=50)
        self.hash_quartos: HashTable[str, Quarto] = HashTable(capacity=25)
        self.lista_reservas: Lista[Reserva] = Lista()  
        gerar_quartos(self.hash_quartos)  

    def realizar_reserva(self, cpf, num_quarto, data_entrada, data_saida):
        
        data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d")
        data_saida = datetime.strptime(data_saida, "%Y-%m-%d")
        
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

    
        nova_reserva = Reserva(quarto, data_entrada, data_saida, usuario)
        
       
        for reserva in self.lista_reservas:
            if reserva.quarto == nova_reserva.quarto:
                if not (data_saida <= reserva.data_entrada or data_entrada >= reserva.data_saida):
                    raise ValueError(f"O quarto {num_quarto} já está reservado de {reserva.data_entrada} a {reserva.data_saida}.")

        self.lista_reservas.inserir(nova_reserva)
        print(self.lista_reservas)
        quarto.disponibilidade = False  

        return f"Reserva realizada com sucesso para o quarto {num_quarto}!"
    
    def cancelar_reserva(self, cpf, quarto, data_entrada, data_saida):
        reservas_usuario = self.consultar_reserva(cpf)

        for reserva in reservas_usuario:
            if (reserva.quarto == quarto and
                reserva.data_entrada == datetime.strptime(data_entrada, "%Y-%m-%d") and
                reserva.data_saida == datetime.strptime(data_saida, "%Y-%m-%d")):
                
                self.lista_reservas.remover(reserva)  # Remove a reserva da lista ordenada
                self.hash_quartos.get(quarto).disponibilidade = True  # Libera o quarto
                return f"Reserva do quarto {quarto} cancelada com sucesso."

        return "Reserva não encontrada ou dados incorretos."

    
    
    
    # def cancelar_reserva(self, cpf, num_quarto):
    #     # verifica se o quarto existe
    #     try:
    #         quarto = self.hash_quartos.get(num_quarto)
    #     except KeyError:
    #         return f"Erro: Quarto {num_quarto} não encontrado."

    #     # procura pela reserva e remove se encontrar
    #     for reserva in self.lista_reservas:
    #         if reserva.user.cpf == cpf and reserva.quarto == quarto:
    #             self.lista_reservas.remover(reserva)
    #             quarto.disponibilidade = True  # Libera o quarto
    #             return f"Reserva do quarto {num_quarto} cancelada com sucesso."

    #     return "Erro: Reserva não encontrada."

    # def cancelar_reserva(self, cpf, num_quarto, data_entrada, data_saida):
    #     reserva_cancelar = 0
    #     for reserva in self.lista_reserva:
    #         if reserva.num_quarto == num_quarto and reserva.data_entrada == data_entrada and reserva.data_saida == data_saida:
    #                 self.lista_reserva.remove(reserva)
    #                 reserva_cancelar+=1
    #                 return f"Reserva cancelada com sucesso para o quarto {num_quarto}."
    #     if reserva_cancelar == 0:
    #         return "Reserva não encontrada ou não corresponde aos critérios especificados." 

    def buscar_usuario(self, cpf) -> Optional[User]: # Optional -> None ou [valor]
        try:
            return self.hash_usuarios.get(cpf)  
        except KeyError:
            return None
        
    def consultar_reserva(self, cpf) -> list[Reserva]:
        """
        Recebe o cpf como parametro e retorna as reservas,
        se não encontrado retornar uma lista vazia.
        """
        usuario_encontrado = self.buscar_usuario(cpf)
        if not usuario_encontrado:
            return []
        reservas = []   
        for reserva in self.lista_reservas:
            if reserva.user.cpf == cpf:
                reservas.append(reserva)
        return reservas

