from cripta.estructuras.ordenamientos import Ordenamiento


class VectorOrdenado:
    """Vector que se mantiene ordenado por una clave, para poder buscar
    por búsqueda binaria (O(log n)) en vez de recorrerlo completo (O(n)).
    Reutiliza Ordenamiento.insertion_sort() de estructuras/ordenamientos.py

    `clave` es una función que extrae el valor comparable de cada
    elemento. Se guarda internamente como (clave(elemento), elemento): así el ordenamiento y la búsqueda
    comparan tuplas, y Python solo mira el segundo valor (el elemento) si dos claves son iguales
    """

    def __init__(self, clave=lambda elemento: elemento):
        self._clave = clave
        self._pares = []  # cada entrada: (clave(elemento), elemento)

    def insertar(self, elemento):
        self._pares.append((self._clave(elemento), elemento))
        Ordenamiento(self._pares).insertion_sort()

    def buscar(self, valor_clave):
        """Búsqueda binaria por clave. Devuelve el elemento o None si no está."""
        indice = self._indice_de(valor_clave)
        return self._pares[indice][1] if indice is not None else None

    def contiene(self, valor_clave) -> bool:
        return self._indice_de(valor_clave) is not None

    def eliminar(self, valor_clave) -> bool:
        indice = self._indice_de(valor_clave)
        if indice is None:
            return False
        del self._pares[indice]
        return True

    def elementos(self):
        return tuple(par[1] for par in self._pares)

    def __len__(self):
        return len(self._pares)

    def _indice_de(self, valor_clave):
        # Búsqueda binaria manual
        bajo, alto = 0, len(self._pares) - 1
        while bajo <= alto:
            medio = (bajo + alto) // 2
            clave_medio = self._pares[medio][0]
            if clave_medio == valor_clave:
                return medio
            if clave_medio < valor_clave:
                bajo = medio + 1
            else:
                alto = medio - 1
        return None