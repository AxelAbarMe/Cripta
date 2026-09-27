class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None  # Puntero al siguiente nodo

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None  # Puntero al primer nodo de la lista

    def agregar(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.cabeza is None:  # Lista vacía
            self.cabeza = nuevo_nodo
            return
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo_nodo

    def eliminar(self, valor):
        if self.cabeza is None:  # Lista vacía
            return
        if self.cabeza.valor == valor:  # Eliminar la cabeza
            self.cabeza = self.cabeza.siguiente
            return
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.valor != valor:
            actual = actual.siguiente
        if actual.siguiente:  # Nodo encontrado
            actual.siguiente = actual.siguiente.siguiente

    def buscar(self, valor):
        actual = self.cabeza
        while actual:
            if actual.valor == valor:
                return True
            actual = actual.siguiente
        return False