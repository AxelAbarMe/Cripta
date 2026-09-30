"""Tabla de puntajes local: un registro por partida terminada."""
from dataclasses import dataclass

from cripta.estructuras.ordenamientos import Ordenamiento


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

    def ordenados_por_tiempo(self) -> tuple[Puntaje, ...]:
        # Menor tiempo_final primero. Se ordena una copia para no alterar el orden de registro.
        copia = [(p.tiempo_final, i, p) for i, p in enumerate(self._registros)]
        Ordenamiento(copia).merge_sort()
        return tuple(p for _, _, p in copia)

    def __len__(self) -> int:
        return len(self._registros)
