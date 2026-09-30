"""Bitácora en pantalla: solo los últimos N mensajes, con memoria constante."""
from cripta.constantes import BITACORA_MAX_MENSAJES
from cripta.estructuras.cola_circular import ColaCircular

class BitacoraMensajes:
    def __init__(self, capacidad: int = BITACORA_MAX_MENSAJES):
        self._cola = ColaCircular(capacidad)

    def agregar(self, mensaje: str) -> None:
        self._cola.enqueue(mensaje)

    def mensajes(self) -> tuple[str, ...]:
        # Del más antiguo al más reciente
        return self._cola.elementos()

    def __len__(self) -> int:
        return len(self._cola)