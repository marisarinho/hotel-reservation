def listaquarto(string):
    string = string.strip(":")
    separaconjuntos = string.split(":")
    cont = 0
    for quarto in separaconjuntos:
        info = quarto.split("-")
        cont += 1
        print(f'Quarto: {info[0]}, Preço: {info[1]}, Cama:{info[2]} \n')