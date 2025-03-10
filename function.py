from quarto import Quarto


def gerar_quartos(hash_table, quantidade=20):
    for i in range(1, quantidade + 1):
        num_quarto = 100 + i
        preco = 150 + (i % 3) * 50  # Alterna preços automaticamente
        camas = (i % 3) + 1  # Alterna entre 1, 2 e 3 camas
        hash_table.insert(num_quarto, Quarto(num_quarto, preco, camas))
        #        