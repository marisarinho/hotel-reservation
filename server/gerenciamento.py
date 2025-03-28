from estruturas.hashTable import HashTable
from hospede import Hospede
from reserva import Reserva
from estruturas.listaOrd import Lista
from gerar_quartos import gerar_quartos
from datetime import datetime
from typing import Optional, List
from quarto import Quarto
from exception import ErroDeReserva
from tratarCorrida import lock


class GerenciadorReservas:

    def __init__(self):
        self.__hospedes: HashTable[str, Hospede] = (
            HashTable()
        )  # chave<cpf> : value <objeto Hospede>
        self.__quartos: HashTable[str, Quarto] = (
            HashTable()
        )  # chave<numero_quarto> : value <objeto Quarto>
        self.__reservas: Lista[Reserva] = (
            Lista()
        )  # Lista ordenada para armazenar as reservas. A chave da reserva é a data de entrada
        gerar_quartos(self.__quartos)

    def realizar_reserva(
        self, cpf: str, num_quarto: int, data_entrada: str, data_saida: str
    ) -> None:
        """
        Método que realiza a reserva de um quarto no período especificado.

        Parametros
        -----------
        cpf (str): o CPF do hóspede que está reservando o quarto
        num_quarto (int):
        data_entrada (str): Data de inicio da reserva no formato dd/mm/aaaa
        data_saida (str): Data de saida da reserva no formato dd/mm/aaaa

        Retorno
        ------------
        None

        Raises
        -------------
        ErroDeReserva: uma exceção quando o hospede não existir
        """
        with lock:
            hospede = self.buscar_usuario(cpf)
            if not hospede:
                raise ErroDeReserva(f"422| Hospede não encontrado")

            try:
                data_entrada = datetime.strptime(data_entrada, "%d/%m/%Y")
                data_saida = datetime.strptime(data_saida, "%d/%m/%Y")
            except ValueError:
                raise ErroDeReserva("423| Formato de data inválido!")

            try:
                quarto = self.__quartos[num_quarto]
            except (
                KeyError
            ):  
                raise ErroDeReserva(f"424| Quarto não cadastrado")

            nova_reserva = Reserva(quarto, data_entrada, data_saida, hospede)

            for reserva in self.__reservas:
                reserva: Reserva
                if reserva.quarto == nova_reserva.quarto:
                    if not (
                        data_saida < reserva.data_entrada
                        or data_entrada > reserva.data_saida
                    ):
                        raise ErroDeReserva(f"425| O quarto já reservado.")
            self.__reservas.inserir(nova_reserva)

    def add_hospede(self, cpf: str, nome: str, telefone: str, senha: str) -> None:
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
            raise ErroDeReserva("402| Hóspede com o mesmo CPF já cadastrado.")

        if nome:
            for char in nome:
                if char in "123456789":
                    raise ErroDeReserva("403| Nome com formato inválido.")

        if not telefone.isdigit() or len(telefone) != 11:
            raise ErroDeReserva("403| Telefone com formato inválido.")

        novo_hospede = Hospede(nome, cpf, telefone, senha)
        self.__hospedes[cpf] = novo_hospede

    def adicionar_quarto(self, num_quarto: int, preco: float, camas: int) -> None:
        """
        Método para adicionar um novo quarto manualmente.

        Parâmetros:
        -----------
        num_quarto (int): Número do quarto a ser adicionado.
        preco (float): Preço da diária do quarto.
        camas (int): Quantidade de camas no quarto.

        Retorno:
        ------------
        None

        Raises
        -------------
        ErroDeReserva: uma exceção quando o quarto já existir
        """
        with lock:
            if num_quarto in self.__quartos:
                raise ErroDeReserva(f"451| O quarto já existe.")

            novo_quarto = Quarto(num_quarto, preco, camas)
            self.__quartos[num_quarto] = novo_quarto

    def mostrar_quartos(self):
        mensagem = "listar quartos cadastrados:\n"
        for chave, valor in self.__quartos.items():
            mensagem += f"Quarto {chave}: Nº {valor.num_quarto}, Preço: R${valor.preco}, Cama: {valor.camas}\n"
        return mensagem

    def mostrar_hospede(self):
        hospedes_lista = "Hospedes cadastrados:\n"
        for chave, valor in self.__hospedes.items(): 
            hospedes_lista += f"Hóspede {chave}: {valor}\n"
        return hospedes_lista

    def cancelar_reserva(self, cpf: str, num_quarto: int, data_entrada: datetime):
        """
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
        """

        try:
            data_entrada = datetime.strptime(data_entrada, "%d/%m/%Y")
        except ValueError:
            raise ErroDeReserva("433| Formato inválido!")

        try:
            self.__quartos[num_quarto]
        except KeyError:
            raise ErroDeReserva(f"432| Reserva não encontrada")

        reservas_usuario = self.consultar_reserva(cpf, data_entrada.year)
        if len(reservas_usuario) == 0:
            raise ErroDeReserva(f"432| Reserva não encontrada")

        with lock:

            for reserva in reservas_usuario:
                if (
                    reserva.quarto.num_quarto == num_quarto
                    and reserva.data_entrada == data_entrada
                ):
                    self.__reservas.remover(self.__reservas.busca(reserva))
                    return

                raise ErroDeReserva("432| Reserva não encontrada")

    def buscar_usuario(
        self, cpf: str
    ) -> Optional[Hospede]:  # Optional -> None ou [valor]
        """
        Método que busca um hóspede pelo CPF.

        Parâmetros
        -----------
        cpf (str): O CPF do hóspede.

        Retorno
        ------------
        Optional[Hospede]: Retorna o objeto Hospede se encontrado, senão retorna None.
        """

        try:
            return self.__hospedes[cpf]
        except KeyError:
            return None

    def consultar_reserva(self, cpf: str, ano: int) -> List[Reserva]:
        """
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
        """

        # Filtra as reservas pelo ano e CPF
        reservas_filtradas = [
            reserva
            for reserva in self.__reservas
            if reserva.ano == ano and reserva.hospede.cpf == cpf
        ]
        return reservas_filtradas
