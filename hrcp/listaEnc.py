class No:
    def __init__(self, carga):
        self.carga = carga
        self.prox = None

class Controle:
    def __init__(self):
        self.head = None
        self.tail = None
        self.tamanho = 0

class Lista:
    def __init__(self):
        self.__head = Controle()

    def vazia(self):
        return self.__head.head is None

    def append(self, carga):
        novo = No(carga)
        if self.vazia():
            self.__head.head = self.__head.tail = novo
        else:
            self.__head.tail.prox = novo
            self.__head.tail = novo
        self.__head.tamanho += 1

    def remover(self, key):
        if self.vazia():
            return False

        cursor = self.__head.head
        anterior = None

        while cursor is not None:
            if cursor.carga == key:
                if anterior is None:
                    self.__head.head = cursor.prox
                else:
                    anterior.prox = cursor.prox

                if cursor == self.__head.tail:
                    self.__head.tail = anterior

                self.__head.tamanho -= 1
                return True

            anterior = cursor
            cursor = cursor.prox

        return False

    def __str__(self):
        s = '['
        cursor = self.__head.head
        while cursor:
            s += f'{cursor.carga}, '
            cursor = cursor.prox
        return s.rstrip(', ') + ']'
