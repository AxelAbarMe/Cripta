"""Tabla de puntajes local: un registro por partida terminada."""
from dataclasses import dataclass

from cripta.estructuras.ordenamiento_selector import ordenar_auto


@dataclass(frozen=True, slots=True)
class Puntaje:
    """Una fila de la tabla: nombre del jugador, cripta jugada y resultado."""
    nombre_jugador: str
    cripta_id: str
    cripta_version: str
    acciones_jugador: int
    enemigos_derrotados: int
    tiempo_final: int


class TablaPuntajes:
    """Guarda los puntajes de la sesión y permite verlos ordenados."""

    def __init__(self):
        self._registros: list[Puntaje] = []  # almacenamiento contiguo de bajo nivel

    def agregar(self, puntaje: Puntaje) -> None:
        self._registros.append(puntaje)

    def registros(self) -> tuple[Puntaje, ...]:
        # En el orden en que se registraron: es el orden que se guarda en disco
        return tuple(self._registros)

    def ordenados_por_tiempo(self) -> tuple[Puntaje, ...]:
        # Menor tiempo_final primero. Se ordena una copia para no alterar el orden de registro.
        copia = [(p.tiempo_final, i, p) for i, p in enumerate(self._registros)]
        ordenar_auto(copia)  # el algoritmo se elige según tamaño y desorden (§4.9)
        return tuple(p for _, _, p in copia)

    def __len__(self) -> int:
        return len(self._registros)
