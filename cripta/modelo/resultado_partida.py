"""Datos de salida de Partida (docs/CONTRATO_PARTIDA.md, secciones 4 y 5).

Todo es inmutable: la vista y el controlador solo leen estos objetos, nunca el modelo vivo.
"""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResultadoAccion:
    aceptada: bool
    motivo_rechazo: str | None
    mensajes: tuple[str, ...]
    desenlace: str          # "en_curso", "victoria" o "derrota"
    tiempo: int             # reloj virtual al terminar


@dataclass(frozen=True, slots=True)
class SalidaVista:
    direccion: str          # "N", "S", "E" u "O"
    destino: int
    cerrada: bool


@dataclass(frozen=True, slots=True)
class EnemigoVista:
    etiqueta: str           # por ejemplo "Rata gigante [e-201]"
    instancia: str
    vida: int
    vida_max: int


@dataclass(frozen=True, slots=True)
class TrampaVista:
    nombre: str
    armada: bool


@dataclass(frozen=True, slots=True)
class VistaPartida:
    sala_id: int
    sala_nombre: str
    salidas: tuple[SalidaVista, ...]
    enemigos: tuple[EnemigoVista, ...]
    objetos_suelo: tuple[str, ...]          # nombres
    trampas: tuple[TrampaVista, ...]
    vida: int
    vida_max: int
    ataque: int
    defensa: int
    velocidad: int
    efectos_activos: tuple[str, ...]
    objeto_actual: str | None               # nombre del objeto que el cursor está viendo
    objeto_actual_indice: int | None        # su posición en el orden real (0 = el primero)
    inventario_cantidad: int
    inventario_capacidad: int
    arma_equipada: str | None
    armadura_equipada: str | None
    tiempo: int
    desenlace: str


@dataclass(frozen=True, slots=True)
class ResumenPuntaje:
    """Lo que Partida sabe de su puntaje; el controlador le agrega el nombre y la versión de la cripta."""
    acciones_jugador: int
    enemigos_derrotados: int
    tiempo_final: int