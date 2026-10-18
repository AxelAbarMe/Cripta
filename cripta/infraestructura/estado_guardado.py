"""Estado de una partida como DATOS PLANOS, listo para serializar (§4.10).

Es la "foto" que guardado_binario.py escribe y lee. El controlador (o quien arme el
guardado) convierte el modelo vivo a estas clases y viceversa; así el formato de
archivo no depende de clases del modelo ni de closures del reloj: la agenda se guarda
como EventoGuardado (tipo + sujeto + dos parámetros) y al cargar se reconstruyen las
acciones a partir de esos datos.

Incluye el estado interno de random.Random(semilla) para que, al continuar una
partida cargada, la secuencia de azar sea EXACTAMENTE la que habría seguido (§2.6).
"""
from dataclasses import dataclass

# Tipos de evento de la agenda (qué debe reconstruir el cargador)
EV_TURNO_ACTOR = 0        # sujeto = "jugador" o instancia del enemigo
EV_VENENO_PULSO = 1       # sujeto = víctima; a = daño por pulso; b = pulsos restantes
EV_REGENERACION = 2       # sujeto = enemigo; a = cantidad
EV_FIN_VELOCIDAD = 3      # sujeto = actor; a = cuánto sumó el efecto a la velocidad
EV_ANTORCHA_APAGAR = 4    # sujeto = instancia/objeto
EV_REARME_TRAMPA = 5      # sujeto = instancia de la trampa
EV_CIERRE_PUERTA = 6      # sujeto = id de sala como texto; a = índice de dirección (N,S,E,O = 0..3)


@dataclass(frozen=True, slots=True)
class ObjetoGuardado:
    instancia_id: str
    ficha_id: str
    equipado: bool


@dataclass(frozen=True, slots=True)
class JugadorGuardado:
    vida: int
    vida_max: int
    ataque: int
    defensa: int
    velocidad: int
    sala_actual: int
    tiempo_siguiente: int
    capacidad_inventario: int
    indice_cursor: int                       # posición del cursor en el inventario (-1 si vacío)
    objetos: tuple[ObjetoGuardado, ...]      # en el orden real del inventario


@dataclass(frozen=True, slots=True)
class EnemigoGuardado:
    instancia_id: str
    tipo: str
    vida: int
    activo: bool
    sala_actual: int
    tiempo_siguiente: int


@dataclass(frozen=True, slots=True)
class TrampaGuardada:
    instancia_id: str
    tipo: str
    armada: bool


@dataclass(frozen=True, slots=True)
class SalaGuardada:
    sala_id: int
    contenido_cargado: bool
    puertas_cerradas: tuple[bool, bool, bool, bool]   # N, S, E, O
    rastro: int                                        # instante de la última visita; -1 = nunca
    objetos_suelo: tuple[str, ...]
    trampas: tuple[TrampaGuardada, ...]
    enemigos: tuple[EnemigoGuardado, ...]              # dormidos y activos presentes en la sala


@dataclass(frozen=True, slots=True)
class EventoGuardado:
    tiempo: int
    secuencia: int
    tipo: int
    sujeto: str
    a: int
    b: int


@dataclass(frozen=True, slots=True)
class EstadoRNG:
    version: int
    estado: tuple[int, ...]
    gauss_next: float | None

    @staticmethod
    def desde_random(azar) -> "EstadoRNG":
        version, estado, gauss = azar.getstate()
        return EstadoRNG(version, tuple(estado), gauss)

    def aplicar_a(self, azar) -> None:
        azar.setstate((self.version, tuple(self.estado), self.gauss_next))


@dataclass(frozen=True, slots=True)
class EstadoPartida:
    cripta_id: str
    cripta_version: str
    catalogo_version: str
    semilla: int
    rng: EstadoRNG
    reloj_actual: int
    siguiente_secuencia: int
    acciones_jugador: int
    enemigos_derrotados: int
    jugador: JugadorGuardado
    salas: tuple[SalaGuardada, ...]
    eventos: tuple[EventoGuardado, ...]
    mensajes: tuple[str, ...]