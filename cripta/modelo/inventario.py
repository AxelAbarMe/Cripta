"""Inventario del jugador.

El orden real de los objetos vive en una ListaDobleEnlazada:
- recorrer adelante/atrás mueve un cursor por los nodos, en O(1) por paso;
- soltar el objeto que se está viendo es O(1): ya se tiene el nodo por el cursor,
  no hace falta buscarlo por posición;
- equipar mueve el nodo al frente en O(1) (mover_al_inicio);
- las vistas ordenadas (peso/valor/nombre) se calculan aparte, sobre una copia,
  así que nunca alteran el orden real.
"""
from cripta.estructuras.lista_doble_enlazada import ListaDobleEnlazada
from cripta.estructuras.ordenamientos import Ordenamiento


class InventarioLlenoError(Exception):
    """Se intentó recoger un objeto con el inventario lleno."""

class ObjetoInventario:
    """Una instancia concreta de un objeto en el inventario, con su ficha de catálogo."""

    # Mejor usar __slots__ para ahorrar memoria, ya que habrá muchos objetos en el inventario
    __slots__ = ("instancia_id", "ficha")

    def __init__(self, instancia_id: str, ficha):
        self.instancia_id = instancia_id
        self.ficha = ficha  # ArmaDTO / ArmaduraDTO / PocionDTO / AntidotoDTO / LlaveDTO / ...


class Inventario:
    def __init__(self, capacidad_max: int):
        self._capacidad_max = capacidad_max
        self._lista = ListaDobleEnlazada()
        self._cursor = None  # nodo que el jugador está "viendo" actualmente
        self.arma_equipada: ObjetoInventario | None = None
        self.armadura_equipada: ObjetoInventario | None = None

    def esta_lleno(self) -> bool:
        return len(self._lista) >= self._capacidad_max

    def __len__(self) -> int:
        return len(self._lista)

    def objeto_actual(self) -> ObjetoInventario | None:
        return self._cursor.data if self._cursor else None

    # --- recorrido ---
    def siguiente(self) -> ObjetoInventario | None:
        if self._cursor and self._cursor.next:
            self._cursor = self._cursor.next
        return self.objeto_actual()

    def anterior(self) -> ObjetoInventario | None:
        if self._cursor and self._cursor.prev:
            self._cursor = self._cursor.prev
        return self.objeto_actual()

    # --- recoger / soltar ---
    def recoger(self, objeto: ObjetoInventario) -> None:
        if self.esta_lleno():
            raise InventarioLlenoError("El inventario está lleno; debe soltar algo primero.")
        nodo = self._lista.agregar(objeto)
        self._cursor = nodo  # el jugador queda viendo lo que acaba de recoger

    def soltar_actual(self) -> ObjetoInventario | None:
        # El costo no depende de la posición: ya se tiene el nodo por el cursor
        if self._cursor is None:
            return None
        nodo = self._cursor
        objeto = nodo.data
        self._cursor = nodo.next or nodo.prev  # se lee ANTES de desconectar el nodo
        self._lista.eliminar_nodo(nodo)
        if objeto is self.arma_equipada:
            self.arma_equipada = None
        if objeto is self.armadura_equipada:
            self.armadura_equipada = None
        return objeto

    # --- equipar ---
    def equipar_actual(self) -> ObjetoInventario | None:
        if self._cursor is None:
            return None
        objeto = self._cursor.data
        clase = objeto.ficha.clase
        if clase == "arma":
            self.arma_equipada = objeto
        elif clase == "armadura":
            self.armadura_equipada = objeto
        else:
            return None  # solo arma/armadura se "equipan"
        self._lista.mover_al_inicio(self._cursor)
        return objeto

    # --- vistas ordenadas: no alteran el orden real ---
    def vista_ordenada(self, criterio: str) -> tuple[ObjetoInventario, ...]:
        extractor = self._extractor_de(criterio)
        copia = []
        nodo = self._lista.head
        indice = 0
        while nodo:
            # (clave, índice, objeto): el índice desempata claves iguales sin
            # tener que comparar los ObjetoInventario entre sí.
            copia.append((extractor(nodo.data), indice, nodo.data))
            indice += 1
            nodo = nodo.next
        Ordenamiento(copia).merge_sort()
        return tuple(objeto for _, _, objeto in copia)

    @staticmethod
    def _extractor_de(criterio: str):
        if criterio == "peso":
            return lambda o: o.ficha.peso
        if criterio == "valor":
            return lambda o: o.ficha.valor
        if criterio == "nombre":
            return lambda o: o.ficha.nombre
        raise ValueError(f"Criterio de orden desconocido: {criterio}")
