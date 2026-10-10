"""HistorialRetroceso: pergamino de retroceso.

Por cada intervalo entre dos decisiones del jugador se guarda una Pila.
Deshacer un intervalo es sacar cada operación de su Pila y
ejecutarla en el mismo orden LIFO en que se registró: lo último que pasó en
ese intervalo se revierte primer.

Los intervalos en sí se guardan en una lista simple, acotada a
RETROCESO_MAX_ACCIONES. Como el límite es una constante fija y pequeña 
(5, nunca crece más allá de 6 elementos antes de recortar).
"""
from contextlib import contextmanager
from cripta.constantes import RETROCESO_MAX_ACCIONES
from cripta.excepciones import CriptaHistorialError
from cripta.estructuras.pila import Pila

class HistorialRetroceso:
    def __init__(self, maximo: int = RETROCESO_MAX_ACCIONES):
        self._maximo = maximo
        self._intervalos: list[Pila] = []
        self._intervalo_actual: Pila | None = None
        self._revirtiendo = False
        self._pausas = 0

    def iniciar_intervalo(self) -> None:
        """Se llama justo antes de ejecutar una acción del jugador: todo lo que
        pase después (la acción misma, reacciones enemigas, efectos) se
        registra en este intervalo hasta la siguiente decisión del jugador."""
        if self._intervalo_actual is not None:
            raise CriptaHistorialError("Ya hay un intervalo abierto: hay que cerrarlo antes de abrir otro.")
        self._intervalo_actual = Pila()

    def registrar(self, deshacer) -> None:
        """`deshacer` Se llama una vez por cada cambio que ocurra dentro del
        intervalo actualmente abierto. Si no hay ningún intervalo abierto"""
        if self._intervalo_actual is None:
            raise CriptaHistorialError("No hay un intervalo abierto: este cambio no se podría deshacer.")
        self._intervalo_actual.push(deshacer)

    def hay_intervalo_abierto(self) -> bool:
        return self._intervalo_actual is not None

    def descartar_intervalo_actual(self) -> None:
        """Abandona el intervalo abierto sin guardarlo (la acción fue rechazada y no cambió nada)."""
        self._intervalo_actual = None

    def registrar_cambio(self, deshacer) -> None:
        """Gancho para los objetos del modelo (ver Reversible): registra la inversa solo si hay un
        intervalo abierto y no se está revirtiendo ni en pausa. A diferencia de registrar(),
        no registrar aquí no es un error: hay cambios legítimos fuera de un intervalo."""
        if self._intervalo_actual is None or self._revirtiendo or self._pausas > 0:
            return
        self._intervalo_actual.push(deshacer)

    @contextmanager
    def sin_registrar(self):
        """Dentro del bloque los cambios no se registran (carga de contenido, pergaminos)."""
        self._pausas += 1
        try:
            yield
        finally:
            self._pausas -= 1

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
        self._revirtiendo = True   # revertir no debe registrar nuevas inversas
        try:
            while True:
                deshacer = intervalo.pop()
                if deshacer is None:
                    break
                deshacer()
                contador += 1
        finally:
            self._revirtiendo = False
        return contador

    def __len__(self) -> int:
        return len(self._intervalos)