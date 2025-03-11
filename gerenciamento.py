from hashTable import HashTable
from user import User
from reserva import Reserva
from quarto import Quarto
from listaOrd import Lista
from function import gerar_quartos
from datetime import datetime

class GerenciadorReservas:

    def __init__(self):
        self.hash_usuarios = HashTable(capacity=50)
        self.hash_quartos = HashTable(capacity=25)
        self.lista_reservas = Lista()
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



    def cancelar_reserva(self, cpf, num_quarto, data_entrada, data_saida):
        if self.consultar_reserva(cpf):
            for reserva in self.lista_reserva:
                if reserva.num_quarto == num_quarto and reserva.data_entrada == data_entrada  and reserva.data_saida == data_saida:
                    lista_reserva.remove(reserva)
                    
                    return f"Reserva cancelada com sucesso para o quarto {num_quarto}."
                    break 
        return "Reserva não encontrada ou não corresponde aos critérios especificados."


    def consultar_reserva(self, cpf):
 
        usuario_encontrado = self.hash_usuarios.get(cpf)  
        if not usuario_encontrado:
            return f"Nenhum usuário encontrado com o CPF {cpf}."
        
        reservasEncontradas = 0
        
        stringFinal = f"Usuário: {usuario_encontrado.cpf}, Nome: {usuario_encontrado.nome}, Telefone: {usuario_encontrado.telefone}, Reservas: \n"
        
        for reserva in self.lista_reservas:
            if reserva.user.cpf == cpf:
                reservasEncontradas+=1
                stringFinal += f"Quarto: {reserva.quarto.num_quarto}, Data de entrada: {reserva.data_entrada}, Data de saída: {reserva.data_saida} \n"
                
        if reservasEncontradas == 0:
            return f"Usuário {cpf} não possui reservas."
        
        return stringFinal

