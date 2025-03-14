from hashTable import HashTable
from user import User
from reserva import Reserva
from listaOrd import Lista
from function import gerar_quartos
from datetime import datetime
from typing import Optional  #ideia pra trazer melhor a documentaçao?
from quarto import Quarto
from exception import ErroDeReserva,validar_cpf,validar_numero_quarto,validar_datas
from tratarCorrida import lock
class GerenciadorReservas:

    def __init__(self):
        # Se der erro foi aqui (especificando os tipos)
        self.hash_usuarios: HashTable[str, User] = HashTable(capacity=50)
        self.hash_quartos: HashTable[str, Quarto] = HashTable(capacity=25)
        self.lista_reservas: Lista[Reserva] = Lista()  
        gerar_quartos(self.hash_quartos)  

    def realizar_reserva(self, cpf, num_quarto, data_entrada, data_saida):
        try:
                # Validações
                validar_cpf(cpf)
                validar_numero_quarto(num_quarto)
                data_entrada, data_saida = validar_datas(data_entrada, data_saida)

                data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d")
                data_saida = datetime.strptime(data_saida, "%Y-%m-%d")
                
                usuario = None
                usuario = self.hash_usuarios.get(cpf)
                if usuario is None:
                    usuario = User(nome="Usuário Padrão", cpf=cpf, telefone="0000-0000")
                    self.hash_usuarios.insert(cpf, usuario)

                # Buscando o quarto
                quarto = None
                if quarto is None:
                    resposta = ErroDeReserva("Quarto não encontrado")

                nova_reserva = Reserva(quarto, data_entrada, data_saida, usuario)
                
                for reserva in self.lista_reservas:
                    if reserva.quarto == nova_reserva.quarto:
                        if not (data_saida <= reserva.data_entrada or data_entrada >= reserva.data_saida):
                            resposta =  ErroDeReserva(f"O quarto {num_quarto} já está reservado de {reserva.data_entrada} a {reserva.data_saida}.")

                self.lista_reservas.inserir(nova_reserva)
                print(self.lista_reservas)
                quarto.disponibilidade = False  

                return f"Reserva realizada com sucesso para o quarto {num_quarto}!"
            
        except ErroDeReserva as e:
            return f"Erro ao realizar reserva: {e}"
    
    def cancelar_reserva(self, cpf, num_quarto, data_entrada, data_saida):
        data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d")
        data_saida = datetime.strptime(data_saida, "%Y-%m-%d")

        with lock:  
            reservas_usuario = self.consultar_reserva(cpf)
            for reserva in reservas_usuario:
                if (reserva.quarto.get_num_quarto() == num_quarto and
                    reserva.data_entrada == data_entrada and
                    reserva.data_saida == data_saida):
                    self.lista_reservas.remover(self.lista_reservas.busca(reserva))  
                    self.hash_quartos.get(num_quarto).set_disponibilidade(True) 
                    return f"Reserva do quarto {num_quarto} cancelada com sucesso."
            return "Reserva não encontrada ou dados incorretos."


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
        with lock:        
            reservas = []   
            for reserva in self.lista_reservas:
                if reserva.user.cpf == cpf:
                    reservas.append(reserva)
            return reservas