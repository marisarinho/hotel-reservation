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
        self.__hash_hospedes: HashTable[str, Hospede] = HashTable() # chave<cpf> : value <objeto Hospede>
        self.__hash_quartos: HashTable[str, Quarto] = HashTable() # chave<numero_quarto> : value <objeto Quarto>
        #lista tb vai ficar privado provavelmtente
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
            if num_quarto in self.__hash_quartos:
                raise ErroDeReserva(f" O quarto {num_quarto} já existe.") 
            
            novo_quarto = Quarto(num_quarto, preco, camas)
            self.__hash_quartos[num_quarto] = novo_quarto
            #return f"Quarto {num_quarto} adicionado com sucesso."

    # def mostrar_quartos(self):
    #     """Retorna a hashtable com os quartos."""
    #     return self.__hash_quartos
    
    def mostrar_quartos(self):
        print("Quartos cadastrados:")
        for chave, valor in self.__hash_quartos.items():  # Se for um dicionário
            print(f"Quarto {chave}: {valor}")

    def mostrar_hospede(self):
        hospedes_lista = "Hospedes cadastrados:\n"
        for chave, valor in self.__hash_hospedes.items():  # Se for um dicionário
            hospedes_lista += f"Hóspede {chave}: {valor}\n"
        return hospedes_lista

    
    # def cancelar_reserva(self, cpf:str, num_quarto:int, data_entrada:datetime, data_saida:datetime):
    #     '''
    #     Método que cancela uma reserva existente no período especificado.

    #     Parâmetros
    #     -----------
    #     cpf (str): O CPF do hóspede que realizou a reserva.
    #     num_quarto (int): O número do quarto reservado.
    #     data_entrada (datetime): Data de início da reserva no formato aaaa-mm-dd.
    #     data_saida (datetime): Data de término da reserva no formato aaaa-mm-dd.

    #     Retorno
    #     ------------
    #     nada eu acho

    #     Raises
    #     -------------
    #     ErroDeReserva: Exceção levantada quando o hóspede não possui reservas ou os
    #     dados fornecidos estão incorretos.
    #     '''
    #     data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d")
    #     data_saida = datetime.strptime(data_saida, "%Y-%m-%d")

    #     with lock:  
    #         reservas_usuario = self.consultar_reserva(cpf)
    #         for reserva in reservas_usuario:
    #             if (reserva.__quarto[num_quarto] == num_quarto and
    #                 reserva.__data_entrada == data_entrada and
    #                 reserva.__data_saida == data_saida):
    #                 self.lista_reservas.remover(self.lista_reservas.busca(reserva))  
    #                 self.__hash_quartos[num_quarto]

    #         return "Reserva não encontrada ou dados incorretos."


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
            return self.__hash_hospedes[cpf]  
        except KeyError:
            return None
        
    def get_ano(self):
        # Extraindo o ano da data no formato 'DD/MM/YYYY'
        return self.__data_entrada.split("/")[0]
    
    def consultar_reservas(self, ano: int, cpf: str) -> List[Reserva]:
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
            if reserva.get_ano() == ano and reserva.cpf == cpf
        ]
        return reservas_filtradas


    def validar_cpf(self, cpf: str):
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11:
            raise ErroDeReserva("CPF inválido! Deve conter exatamente 11 dígitos numéricos.")
        if cpf == cpf[0] * 11:
            raise ErroDeReserva("CPF inválido! Não pode conter todos os dígitos iguais.")

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        digito1 = 0 if resto == 10 else resto

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        digito2 = 0 if resto == 10 else resto

        if int(cpf[9]) != digito1 or int(cpf[10]) != digito2:
            # print(f"Erro: CPF {cpf} com dígitos verificadores inválidos.") #testando
            raise ErroDeReserva("CPF inválido! Dígitos verificadores não conferem.")

        return True
    
    def add_hospede(self, cpf: str, nome: str, telefone: str):
        """
        Método para adicionar um hóspede ao sistema.

        Parâmetros:
        -----------
        cpf (str): CPF do hóspede.
        nome (str): Nome do hóspede.
        telefone (str): Telefone do hóspede.

        Retorno:
        ------------
        str: Mensagem confirmando o cadastro do hóspede.
        """

        try:
            # Validações
            #uma ou duas underlines?
            #self.__validar_cpf(cpf)5
            self.validar_cpf(cpf)
            # Verifica se o CPF já está cadastrado
            if cpf in self.__hash_hospedes:
                raise ErroDeReserva("Hóspede já cadastrado.")
            novo_hospede = Hospede(nome, cpf, telefone)
            self.__hash_hospedes[cpf] = novo_hospede


        except ErroDeReserva as e:
            return str(e) 
    