"""HistorialRetroceso: pergamino de retroceso.

Por cada intervalo entre dos decisiones del jugador se guarda una Pila.
Deshacer un intervalo es sacar cada operación de su Pila y
ejecutarla en el mismo orden LIFO en que se registró: lo último que pasó en
ese intervalo se revierte primer.

Los intervalos en sí se guardan en una lista simple, acotada a
RETROCESO_MAX_ACCIONES. Como el límite es una constante fija y pequeña 
(5, nunca crece más allá de 6 elementos antes de recortar).
"""
from cripta.constantes import RETROCESO_MAX_ACCIONES
from cripta.estructuras.pila import Pila

class HistorialRetroceso:
    def __init__(self, maximo: int = RETROCESO_MAX_ACCIONES):
        self._maximo = maximo
        self._intervalos: list[Pila] = []
        self._intervalo_actual: Pila | None = None

    def iniciar_intervalo(self) -> None:
        """Se llama justo antes de ejecutar una acción del jugador: todo lo que
        pase después (la acción misma, reacciones enemigas, efectos) se
        registra en este intervalo hasta la siguiente decisión del jugador."""
        self._intervalo_actual = Pila()

    def registrar(self, deshacer) -> None:
        """`deshacer` Se llama una vez por cada cambio que ocurra dentro del
        intervalo actualmente abierto. Si no hay ningún intervalo abierto"""
        if self._intervalo_actual is not None:
            self._intervalo_actual.push(deshacer)

    def cerrar_intervalo(self) -> None:
        """Se llama justo antes de la siguiente decisión del jugador: el
        intervalo que se estaba armando queda completo y disponible para
        deshacerse. Si al cerrarlo ya hay más de `maximo` guardados, se
        descarta el más antiguo."""
        if self._intervalo_actual is None:
            return
        self._intervalos.append(self._intervalo_actual)
        if len(self._intervalos) > self._maximo:
            self._intervalos.pop(0)
        self._intervalo_actual = None

    def hay_intervalo_para_deshacer(self) -> bool:
        return len(self._intervalos) > 0

    def deshacer_ultimo_intervalo(self) -> int:
        """Aplica, en orden LIFO, todas las operaciones inversas del intervalo
        más reciente disponible. Devuelve cuántas operaciones se revirtieron (solo informativo).
        Si no hay intervalos para deshacer, devuelve 0.
        No forma parte de inicio/cierre de intervalos
        Manejo de pergamino de retroceso se hace fuera de esta clase.
        """
        if not self._intervalos:
            return 0
        intervalo = self._intervalos.pop()
        contador = 0
        while True:
            deshacer = intervalo.pop()
            if deshacer is None:
                break
            deshacer()
            contador += 1
        return contador

    def __len__(self) -> int:
        return len(self._intervalos)
