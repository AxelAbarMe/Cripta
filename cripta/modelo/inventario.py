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

import unicodedata
from cripta.estructuras.ordenamiento_selector import ordenar_auto
from cripta.modelo.reversible import Reversible


def _normalizar_nombre(texto: str) -> str:
    """Minúsculas y sin tildes, para que 'Ábaco' quede junto a 'abeja'."""
    descompuesto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")

class InventarioLlenoError(Exception):
    """Se intentó recoger un objeto con el inventario lleno."""

class ObjetoInventario:
    """Una instancia concreta de un objeto en el inventario, con su ficha de catálogo."""

    # Mejor usar __slots__ para ahorrar memoria, ya que habrá muchos objetos en el inventario
    __slots__ = ("instancia_id", "ficha")

    def __init__(self, instancia_id: str, ficha):
        self.instancia_id = instancia_id
        self.ficha = ficha  # ArmaDTO / ArmaduraDTO / PocionDTO / AntidotoDTO / LlaveDTO / ...


class Inventario(Reversible):
    _no_reversibles = ("_cursor",)   # el cursor es de la interfaz, no del estado del juego
    
    def __init__(self, capacidad_max: int):
        self._capacidad_max = capacidad_max
        self._lista = ListaDobleEnlazada()
        self._cursor = None  # nodo que el jugador está "viendo" actualmente
        self.arma_equipada: ObjetoInventario | None = None
        self.armadura_equipada: ObjetoInventario | None = None

    @property
    def capacidad_max(self) -> int:
        return self._capacidad_max

    def esta_lleno(self) -> bool:
        return len(self._lista) >= self._capacidad_max

    def __len__(self) -> int:
        return len(self._lista)

    def objeto_actual(self) -> ObjetoInventario | None:
        return self._cursor.data if self._cursor else None

    # --- recorrido ---
    def siguiente(self):
        if self._cursor:
            self._cursor = self._cursor.next or self._lista.head   # del último pasa al primero
        return self.objeto_actual()

    def anterior(self):
        if self._cursor:
            self._cursor = self._cursor.prev or self._lista.tail   # del primero pasa al último
        return self.objeto_actual()
    
    def ir_a_posicion(self, indice: int) -> ObjetoInventario | None:
        """Pone el cursor en la posición `indice` del orden real (0 = el primero).
        Devuelve el objeto, o None si esa posición no existe. Cuesta O(n) con n <= inventario_max."""
        if indice < 0:
            return None
        nodo = self._lista.head
        while nodo is not None and indice > 0:
            nodo = nodo.next
            indice -= 1
        if nodo is None:
            return None
        self._cursor = nodo
        return nodo.data


    def posicion_actual(self) -> int | None:
        """Posición (0 = el primero) del objeto que el cursor está viendo, o None si no hay."""
        nodo = self._lista.head
        indice = 0
        while nodo is not None:
            if nodo is self._cursor:
                return indice
            nodo = nodo.next
            indice += 1
        return None


    # --- recoger / soltar ---
    def recoger(self, objeto: ObjetoInventario) -> None:
        if self.esta_lleno():
            raise InventarioLlenoError("El inventario está lleno; debe soltar algo primero.")
        nodo = self._lista.agregar(objeto)
        self._registrar_inversa(lambda: self._deshacer_recoger(objeto))
        self._cursor = nodo  # el jugador queda viendo lo que acaba de recoger

    def soltar_actual(self) -> ObjetoInventario | None:
        # El costo no depende de la posición: ya se tiene el nodo por el cursor
        if self._cursor is None:
            return None
        nodo = self._cursor
        objeto = nodo.data
        self._cursor = nodo.next or nodo.prev  # se lee ANTES de desconectar el nodo
        prefijo = self._prefijo_de(nodo)
        self._lista.eliminar_nodo(nodo)
        self._registrar_inversa(lambda: self._reponer_en_su_posicion(objeto, prefijo))
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
        prefijo = self._prefijo_de(self._cursor)
        self._lista.mover_al_inicio(self._cursor)
        self._registrar_inversa(lambda: self._deshacer_equipar(prefijo))
        return objeto


    # --- consultas por clase y fichas en uso ---
    def contar_clase(self, clase: str) -> int:
        cantidad = 0
        nodo = self._lista.head
        while nodo is not None:
            if nodo.data.ficha.clase == clase:
                cantidad += 1
            nodo = nodo.next
        return cantidad

    def cantidad_pergaminos(self) -> int:
        return self.contar_clase("pergamino_retroceso")

    def quitar_primero_de_clase(self, clase: str) -> ObjetoInventario | None:
        """Quita y devuelve el primer objeto de esa clase (por ejemplo, el pergamino que se usa).
        Devuelve None si no hay ninguno."""
        nodo = self._lista.head
        while nodo is not None and nodo.data.ficha.clase != clase:
            nodo = nodo.next
        if nodo is None:
            return None
        if nodo is self._cursor:
            self._cursor = nodo.next or nodo.prev   # se lee ANTES de desconectar el nodo
        objeto = nodo.data
        prefijo = self._prefijo_de(nodo)
        self._lista.eliminar_nodo(nodo)
        self._registrar_inversa(lambda: self._reponer_en_su_posicion(objeto, prefijo))
        return objeto


    def objetos_en_orden(self) -> tuple:
        """Los objetos en el orden real del inventario (el primero es el que está al frente)."""
        objetos = []
        nodo = self._lista.head
        while nodo is not None:
            objetos.append(nodo.data)
            nodo = nodo.next
        return tuple(objetos)


    def fichas_en_uso(self) -> tuple[str, ...]:
        """Ids de catálogo de los objetos del inventario (no se pueden liberar de la caché, §4.4)."""
        ids = []
        nodo = self._lista.head
        while nodo is not None:
            ids.append(nodo.data.ficha.id)
            nodo = nodo.next
        return tuple(ids)


    # --- inversas de los cambios (retroceso, §2.11) ---
    # Las inversas buscan el nodo por su OBJETO y no por el nodo guardado: al reponer un objeto
    # se crea un nodo nuevo, así que una referencia a un nodo viejo ya no sirve.
    def _nodo_de(self, objeto):
        actual = self._lista.head
        while actual is not None and actual.data is not objeto:
            actual = actual.next
        return actual

    def _prefijo_de(self, nodo) -> tuple:
        """Los objetos que van antes de `nodo` en el orden real."""
        prefijo = []
        actual = self._lista.head
        while actual is not None and actual is not nodo:
            prefijo.append(actual.data)
            actual = actual.next
        return tuple(prefijo)

    def _deshacer_recoger(self, objeto) -> None:
        nodo = self._nodo_de(objeto)
        if nodo is None:   # ya no está (por ejemplo, un pergamino, que el retroceso no toca)
            return
        self._cursor = nodo.prev or nodo.next
        self._lista.eliminar_nodo(nodo)

    def _reponer_en_su_posicion(self, objeto, prefijo) -> None:
        nuevo = self._lista.agregar_inicio(objeto)
        self._deshacer_equipar(prefijo)
        self._cursor = nuevo

    def _deshacer_equipar(self, prefijo) -> None:
        for previo in reversed(prefijo):   # devuelve al frente los que iban antes, del más cercano al más lejano
            nodo = self._nodo_de(previo)
            if nodo is not None:           # un pergamino quitado o soltado no se restaura (§2.11)
                self._lista.mover_al_inicio(nodo)


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
        ordenar_auto(copia)
        return tuple(objeto for _, _, objeto in copia)

    @staticmethod
    def _extractor_de(criterio: str):
        if criterio == "peso":
            return lambda o: o.ficha.peso
        if criterio == "valor":
            return lambda o: o.ficha.valor
        if criterio == "nombre":
            return lambda o: _normalizar_nombre(o.ficha.nombre)
        raise ValueError(f"Criterio de orden desconocido: {criterio}")
