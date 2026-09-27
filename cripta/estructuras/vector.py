from cripta.estructuras.ordenamientos import insertion_sort

class VectorOrdenado:
    def __init__(self, elementos=None):
        self.elementos = elementos if elementos is not None else []

    def ordenar_insercion(self):
        insertion_sort(self.elementos)

    def get_elementos(self):
        return self.elementos

    def insertar(self, valor):
        self.elementos.append(valor)
        self.ordenar_insercion()