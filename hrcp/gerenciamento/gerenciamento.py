from hrcp.estruturasDeDados.avl import AVLTree
from hrcp.estruturasDeDados.hashTable import HashTable
from hrcp.estruturasDeDados.fila import Fila
from hrcp.gerenciamento.user import User
from hrcp.gerenciamento.reserva import Reserva
from hrcp.gerenciamento.quarto import Quarto


class GerenciadorReservas:
    def __init__(self):
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
        """Cancela uma reserva X relacionada ao CPF passado"""
        pass


    def consultar_reserva(self, cpf):
        """
        Consulta todas as reservas associadas a um CPF na árvore AVL de reservas
        e na tabela de hash de usuários.
        """
        usuario_encontrado = self.hash_usuarios.get(cpf)  
        if not usuario_encontrado:
            return f"Nenhum usuário encontrado com o CPF {cpf}."
        
        reserva_achada = self.arvore_avl_reservas.buscar_reservas_por_cpf(usuario_encontrado)  

        if reserva_achada:  
            for r in reserva_achada:
                print(f'Quarto: {r.numero_quarto}, Período: {r.periodo_reservado}')
        else:
            print(f'Nenhuma reserva encontrada para o CPF {cpf}.')



    def listar(self, hash_quartos):
        """Lista todos os quartos(disponiveis ou nao)
            A listagem é feita usando uma fila, mostrando 5 quartos por vez"""
        pass