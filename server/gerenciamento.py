from estruturas.hashTable import HashTable
from hospede import Hospede
from reserva import Reserva
from estruturas.listaOrd import Lista
from function import gerar_quartos
from datetime import datetime
from typing import Optional,List 
from quarto import Quarto
from exception import ErroDeReserva
from tratarCorrida import lock

class GerenciadorReservas:

    def __init__(self):
        # Se der erro foi aqui (especificando os tipos)
        self.__hospedes: HashTable[str, Hospede] = HashTable() # chave<cpf> : value <objeto Hospede>
        self.__quartos: HashTable[str, Quarto] = HashTable() # chave<numero_quarto> : value <objeto Quarto>
        #lista tb vai ficar privado provavelmtente
        self.__reservas: Lista[Reserva] = Lista()  # Lista ordenada para armazenar as reservas. A chave da reserva é a data de entrada
        gerar_quartos(self.__quartos)

    def realizar_reserva(self, cpf:str, num_quarto:int, data_entrada: str, data_saida: str):
        '''
        Método que realiza a reserva de um quarto no período especificado.

        Parametros
        -----------
        cpf (str): o CPF do hóspede que está reservando o quarto
        num_quarto (int):
        data_entrada (str): Data de inicio da reserva no formato dd/mm/aaaa
        data_saida (str): Data de saida da reserva no formato dd/mm/aaaa

        Retorno
        ------------
        dizer o que retorna

        Raises
        -------------
        ErroDeReserva: uma exceção quando o hospede não existir 
        '''
        with lock:
            hospede = self.buscar_usuario(cpf)
            if not hospede:
                raise ErroDeReserva(f'Hospede de cpf {cpf} não cadastrado')
            
            try:
                data_entrada = datetime.strptime(data_entrada, "%d/%m/%Y")
                data_saida = datetime.strptime(data_saida, "%d/%m/%Y")  
            except ValueError:
                raise ErroDeReserva("Formato inválido!")
            
            #MARK:realizar reserva 
            """ 
            Quando quarto nao é encontrado acaba caindo no 
            mesmo erro de Hospede de cpf {cpf} não cadastrado
            """
            
            try:
                quarto = self.__quartos[num_quarto] 
            except KeyError: # aqui temos uma exceção se a chave cpf não estive na hash de hospede
                raise ErroDeReserva(f'Quarto {num_quarto} não cadastrado')
  
            nova_reserva = Reserva(quarto, data_entrada, data_saida, hospede)        
        
            for reserva in self.__reservas:
                reserva: Reserva
                if reserva.quarto == nova_reserva.quarto:
                    if not (data_saida < reserva.data_entrada or data_entrada > reserva.data_saida):
                        raise ErroDeReserva(
                            f"O quarto {num_quarto} já está reservado de {reserva.data_entrada} a {reserva.data_saida}.")
            self.__reservas.inserir(nova_reserva)
        
    def adicionar_quarto(self, num_quarto: int, preco: float, camas: int):
        """
        Método para adicionar um novo quarto manualmente.

        Parâmetros:
        -----------
        num_quarto (int): Número do quarto a ser adicionado.
        preco (float): Preço da diária do quarto.
        camas (int): Quantidade de camas no quarto.

        Retorno:
        ------------
        str: Mensagem confirmando a adição do quarto.
        """
        with lock:
            if num_quarto in self.__quartos:
                raise ErroDeReserva(f"O quarto {num_quarto} já existe.") 
            
            novo_quarto = Quarto(num_quarto, preco, camas)
            self.__quartos[num_quarto] = novo_quarto
            #return f"Quarto {num_quarto} adicionado com sucesso."

    # def mostrar_quartos(self):
    #     """Retorna a hashtable com os quartos."""
    #     return self.__hash_quartos
    
    def mostrar_quartos(self):
        print("Quartos cadastrados:")
        for chave, valor in self.__quartos.items():  # Se for um dicionário
            print(f"Quarto {chave}: {valor}")

    def mostrar_hospede(self):
        hospedes_lista = "Hospedes cadastrados:\n"
        for chave, valor in self.__hospedes.items():  # Se for um dicionário
            hospedes_lista += f"Hóspede {chave}: {valor}\n"
        return hospedes_lista

    
    def cancelar_reserva(self, cpf:str, num_quarto:int, data_entrada:datetime):
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
        data_entrada = datetime.strptime(data_entrada, "%d/%m/%Y")

        with lock:  
            reservas_usuario = self.consultar_reserva(cpf, data_entrada.year)
            for reserva in reservas_usuario:
                if reserva.quarto.num_quarto == num_quarto and reserva.data_entrada == data_entrada:
                    self.__reservas.remover(self.__reservas.busca(reserva))  
                    return
                
            raise ErroDeReserva("Reserva não encontrada ou dados incorretos.")


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
            return self.__hospedes[cpf]  
        except KeyError:
            return None
        
    def consultar_reserva(self, cpf: str, ano: int) -> List[Reserva]:
        '''
        Método que consulta todas as reservas associadas a um determinado CPF em um ano específico.
 
        Parâmetros
        -----------
        cpf (str): O CPF do hóspede cujas reservas serão consultadas.
        ano (int): O ano em que as reservas devem ser filtradas.

        Retorno
        ------------
        List[Reserva]: Lista contendo todas as reservas do hóspede no ano especificado.
        Se não houver reservas, retorna uma lista vazia.

        Raises
        -------------
        Nenhuma exceção é levantada. Se o hóspede não for encontrado, uma lista vazia será retornada.
        '''
        
        # Filtra as reservas pelo ano e CPF
        reservas_filtradas = [
            reserva for reserva in self.__reservas 
            if reserva.ano == ano and reserva.hospede.cpf == cpf
        ]
        return reservas_filtradas


    def add_hospede(self, cpf: str, nome: str, telefone: str) -> None:
        """
        Método para adicionar um hóspede ao sistema.

        Parâmetros:
        -----------
        cpf (str): CPF do hóspede.
        nome (str): Nome do hóspede.
        telefone (str): Telefone do hóspede.

        Retorno:
        ------------
        None
        """

        if self.buscar_usuario(cpf) is not None:
            raise ErroDeReserva("Hóspede já cadastrado.")
        
        novo_hospede = Hospede(nome, cpf, telefone)
        self.__hospedes[cpf] = novo_hospede
        print(f"Hospede {nome}, cpf: {cpf}, cadastrado com sucesso!")
    