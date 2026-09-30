"""Sala: geometría fija del esqueleto (SalaDTO) + lo que cambia durante la partida. No programa eventos ni conoce el reloj; solo guarda estado."""
from cripta.modelo.trampa import Trampa


class EstadoPuertas:
    """Estado mutable de las hasta 4 puertas de una sala, inicializado desde el esqueleto"""

    def __init__(self, esqueleto):
        self.norte = self._cerrada_inicial(esqueleto.norte)
        self.sur = self._cerrada_inicial(esqueleto.sur)
        self.este = self._cerrada_inicial(esqueleto.este)
        self.oeste = self._cerrada_inicial(esqueleto.oeste)

    @staticmethod
    def _cerrada_inicial(salida) -> bool:
        return bool(salida and salida.cerrada)

    # Verifica puertas
    def esta_cerrada(self, direccion: str) -> bool:
        if direccion == "N":
            return self.norte
        if direccion == "S":
            return self.sur
        if direccion == "E":
            return self.este
        if direccion == "O":
            return self.oeste
        raise ValueError(f"Dirección inválida: {direccion}")

    def abrir(self, direccion: str) -> None:
        self._fijar(direccion, cerrada=False)

    def cerrar(self, direccion: str) -> None:
        self._fijar(direccion, cerrada=True)

    # Fija el estado de una puerta, usado por abrir() y cerrar()
    def _fijar(self, direccion: str, cerrada: bool) -> None:
        if direccion == "N":
            self.norte = cerrada
        elif direccion == "S":
            self.sur = cerrada
        elif direccion == "E":
            self.este = cerrada
        elif direccion == "O":
            self.oeste = cerrada
        else:
            raise ValueError(f"Dirección inválida: {direccion}")


class Sala:
    """Une el esqueleto estático de una sala con su estado mutable durante la partida."""

    def __init__(self, esqueleto):
        # esqueleto: SalaDTO
        self.esqueleto = esqueleto
        self.puertas = EstadoPuertas(esqueleto)
        self.contenido_cargado = False
        self.objetos_en_suelo: list[str] = []  # ids de catálogo;
        self.trampas: list[Trampa] = []
        self.enemigos_dormidos: list = []  # Enemigo aún no activados
        self.enemigos_activos: list = []   # Enemigo activos actualmente en esta sala
        self.rastro_ultima_visita: int | None = None  # instante del reloj virtual

    @property
    def id(self) -> int:
        return self.esqueleto.id

    def cargar_contenido(self, contenido_dto) -> None:
        # contenido_dto: ContenidoSalaDTO. Los enemigos se resuelven aparte (necesitan
        # su ficha de catálogo, que se pide por lotes en servicio_catalogo).
        self.objetos_en_suelo = list(contenido_dto.objetos)
        self.trampas = [Trampa(t.instancia, t.tipo) for t in contenido_dto.trampas]
        self.contenido_cargado = True

    def marcar_visita(self, tiempo_actual: int) -> None:
        # Se refresca en cada acción del jugador en esta sala
        self.rastro_ultima_visita = tiempo_actual

    def rastro_es_fresco(self, tiempo_actual: int, antiguedad_maxima: int) -> bool:
        # Una sala nunca visitada no sirve como rastro; una visitada hace mucho, tampoco
        if self.rastro_ultima_visita is None:
            return False
        return (tiempo_actual - self.rastro_ultima_visita) < antiguedad_maxima

    def agregar_objeto(self, id_catalogo: str) -> None:
        self.objetos_en_suelo.append(id_catalogo)

    def quitar_objeto(self, id_catalogo: str) -> bool:
        if id_catalogo in self.objetos_en_suelo:
            self.objetos_en_suelo.remove(id_catalogo)
            return True
        return False

    def activar_enemigos_dormidos(self) -> list:
        # Mueve todos los enemigos dormidos a activos y los devuelve; no calcula
        # sus tiempos de próxima acción, eso lo hace quien programa el reloj.
        activados = list(self.enemigos_dormidos)
        self.enemigos_activos.extend(activados)
        self.enemigos_dormidos.clear()
        return activados
