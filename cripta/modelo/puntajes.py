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
    victoria: bool


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

    def ranking(self, cripta_id: str, cripta_version: str) -> tuple[Puntaje, ...]:
        """Los puntajes de una cripta (su id y su versión): primero las victorias y después las derrotas;
        dentro de cada grupo, menor tiempo primero y, en un empate, el que se registró antes."""
        copia = [
            (0 if p.victoria else 1, p.tiempo_final, i, p)
            for i, p in enumerate(self._registros)
            if p.cripta_id == cripta_id and p.cripta_version == cripta_version
        ]
        ordenar_auto(copia)
        return tuple(p for _grupo, _tiempo, _i, p in copia)

    def __len__(self) -> int:
        return len(self._registros)


def _ordenar_por_resultado(puntajes) -> tuple[Puntaje, ...]:
    """Primero las victorias, de menor a mayor tiempo. Después las derrotas: más enemigos derrotados primero y,
    en un empate, más tiempo vivo primero. Un empate total conserva el orden de registro."""
    copia = [
        (0, p.tiempo_final, 0, i, p) if p.victoria else (1, -p.enemigos_derrotados, -p.tiempo_final, i, p)
        for i, p in enumerate(puntajes)
    ]
    ordenar_auto(copia)  # el índice `i` es único: la comparación nunca llega hasta el Puntaje
    return tuple(fila[-1] for fila in copia)
