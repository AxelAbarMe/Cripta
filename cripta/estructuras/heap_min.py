class HeapMinimo:
    def __init__(self):
        self.heap = []

    def insertar(self, valor):
        self.heap.append(valor)
        self._flotar(len(self.heap) - 1)

    def eliminar_minimo(self):
        if not self.heap:
            return None
        minimo = self.heap[0]
        ultimo = self.heap.pop()
        if self.heap:
            self.heap[0] = ultimo
            self._hundir(0)
        return minimo

    def _flotar(self, indice):
        while indice > 0:
            padre = (indice - 1) // 2
            if self.heap[indice] < self.heap[padre]:
                self.heap[indice], self.heap[padre] = self.heap[padre], self.heap[indice]
                indice = padre
            else:
                break

    def _hundir(self, indice):
        n = len(self.heap)
        while True:
            hijo_izq = 2 * indice + 1
            hijo_der = 2 * indice + 2
            menor = indice

            if hijo_izq < n and self.heap[hijo_izq] < self.heap[menor]:
                menor = hijo_izq
            if hijo_der < n and self.heap[hijo_der] < self.heap[menor]:
                menor = hijo_der

            if menor == indice:
                break

            self.heap[indice], self.heap[menor] = self.heap[menor], self.heap[indice]
            indice = menor