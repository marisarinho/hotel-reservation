from quarto import Quarto
from estruturas.hashTable import HashTable

def gerar_quartos(hash_table: HashTable, quantidade: int=12) -> None:
    """ 
    Função para gerar quartos em uma hashtable

    Parâmetros
    -----------
    hash_table (HashTable): A hashtable dos quartos.
    quantidade (int): Quantidade de quartos a ser gerado.

    Retorno
    ------------
    None
    
    Raises
    -------------
    Nenhuma exceção é levantada.
    """
    
    for i in range(1, quantidade + 1):
        num_quarto = 100 + i
        preco = 150 + (i % 3) * 50  # Alterna preços automaticamente
        camas = (i % 3) + 1  # Alterna entre 1, 2 e 3 camas
        hash_table.put(num_quarto, Quarto(num_quarto, preco, camas))           