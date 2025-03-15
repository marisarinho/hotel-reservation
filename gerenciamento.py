from hashTable import HashTable
from hospede import Hospede
from reserva import Reserva
from listaOrd import Lista
from function import gerar_quartos
from datetime import datetime
from typing import Optional,List  #ideia pra trazer melhor a documentaçao?
from quarto import Quarto
from exception import ErroDeReserva,validar_numero_quarto
from tratarCorrida import lock
class GerenciadorReservas:

    def __init__(self):
        # Se der erro foi aqui (especificando os tipos)
        self.__hash_hospedes: HashTable[str, Hospede] = HashTable(capacity=50) # chave<cpf> : value <objeto Hospede>
        self.__hash_quartos: HashTable[str, Quarto] = HashTable(capacity=25) # chave<numero_quarto> : value <objeto Quarto>
        self.lista_reservas: Lista[Reserva] = Lista()  # Lista ordenada para armazenar as reservas. A chave da reserva é a data de entrada
        gerar_quartos(self.__hash_quartos)  

    def realizar_reserva(self, cpf:str, num_quarto:int, data_entrada:datetime, data_saida:datetime):
        '''
        Método que realiza a reserva de um quarto no período especificado.

        Parametros
        -----------
        cpf (str): o CPF do hóspede que está reservando o quarto
        num_quarto (int):
        data_entrada (datetime): Data de inicio da reserva no formato aaaa-mm-dd

        Retorno
        ------------
        dizer o que retorna

        Raises
        -------------
        ErroDeReserva: uma exceção quando o hospede não existir 
        '''
        with lock:
            try:
                hospede = self.__hash_hospedes[cpf]
                data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d")
                data_saida = datetime.strptime(data_saida, "%Y-%m-%d")  
                quarto = self.__hash_quartos[num_quarto]
            except KeyError: # aqui temos uma exceção se a chave cpf não estive na hash de hospede
                raise ErroDeReserva(f' Hospede de cpf {cpf} não cadastrado')
            except ValueError as ve:
                raise ErroDeReserva(ve.__str__())

        
            nova_reserva = Reserva(quarto, data_entrada, data_saida, hospede)        
        
            for reserva in self.lista_reservas:
                if reserva.get_quarto() == nova_reserva.get_quarto():
                    if not (data_saida <= reserva.get_data_entrada() or data_entrada >= reserva.get_data_saida()):
                        raise ErroDeReserva(
                            f"O quarto {num_quarto} já está reservado de {reserva.get_data_entrada()} a {reserva.get_data_saida()}.")
            self.lista_reservas.inserir(nova_reserva)
            print(self.lista_reservas)
        

    
    def cancelar_reserva(self, cpf:str, num_quarto:int, data_entrada:datetime, data_saida:datetime):
        '''
        Método que cancela uma reserva existente no período especificado.

        Parâmetros
        -----------
        cpf (str): O CPF do hóspede que realizou a reserva.
        num_quarto (int): O número do quarto reservado.
        data_entrada (datetime): Data de início da reserva no formato aaaa-mm-dd.
        data_saida (datetime): Data de término da reserva no formato aaaa-mm-dd.

        Retorno
        ------------
        nada eu acho

        Raises
        -------------
        ErroDeReserva: Exceção levantada quando o hóspede não possui reservas ou os
        dados fornecidos estão incorretos.
        '''
        data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d")
        data_saida = datetime.strptime(data_saida, "%Y-%m-%d")

        with lock:  
            reservas_usuario = self.consultar_reserva(cpf)
            for reserva in reservas_usuario:
                if (reserva.__quarto.get_num_quarto() == num_quarto and
                    reserva.__data_entrada == data_entrada and
                    reserva.__data_saida == data_saida):
                    self.lista_reservas.remover(self.lista_reservas.busca(reserva))  
                    self.__hash_quartos.get(num_quarto).set_disponibilidade(True) 
                    return f"Reserva do quarto {num_quarto} cancelada com sucesso."
            return "Reserva não encontrada ou dados incorretos."


    def buscar_usuario(self, cpf:str) -> Optional[Hospede]: # Optional -> None ou [valor]
        '''
        Método que busca um hóspede pelo CPF.

        Parâmetros
        -----------
        cpf (str): O CPF do hóspede.

        Retorno
        ------------
        Optional[Hospede]: Retorna o objeto Hospede se encontrado, senão retorna None.
        '''
        
        try:
            return self.__hash_hospedes.get(cpf)  
        except KeyError:
            return None
        
    def consultar_reserva(self, cpf:str) -> List[Reserva]:
        '''
        Método que consulta todas as reservas associadas a um determinado CPF.

        Parâmetros
        -----------
        cpf (str): O CPF do hóspede cujas reservas serão consultadas.

        Retorno
        ------------
        List[Reserva]: Lista contendo todas as reservas do hóspede. 
        Se não houver reservas, retorna uma lista vazia.

        Raises
        -------------
        Nenhuma exceção é levantada. Se o hóspede não for encontrado, uma lista vazia será retornada.
        '''
        usuario_encontrado = self.buscar_usuario(cpf)
        if not usuario_encontrado:
            return []
        with lock:        
            reservas = []   
            for reserva in self.lista_reservas:
                if reserva.user.cpf == cpf:
                    reservas.append(reserva)
            return reservas

    def add_hospode(self,cpf) :
        pass       