"""RelojEventos: reloj virtual + agenda de eventos ordenada por (tiempo, secuencia)
"""
from cripta.constantes import VELOCIDAD_INTERVALO
from cripta.estructuras.heap_min import HeapMinimo


def calcular_intervalo(costo: int, velocidad: int) -> int:
    """intervalo = max(1, costo * 100 // velocidad)."""
    return max(1, costo * VELOCIDAD_INTERVALO // velocidad)

def calcular_tiempo_reprogramado(tiempo_siguiente: int, tiempo_actual: int, velocidad_anterior: int, velocidad_nueva: int) -> int:
    """Si un efecto cambia la velocidad de un actor que ya tiene una acción
    programada, el tiempo restante se reescala. Devuelve el nuevo tiempo_siguiente ABSOLUTO (no el intervalo)."""
    restante = tiempo_siguiente - tiempo_actual
    restante_nuevo = max(1, restante * velocidad_anterior // velocidad_nueva)
    return tiempo_actual + restante_nuevo


class EventoProgramado:
    """Un evento agendado en el RelojEventos, con tiempo absoluto y secuencia para desempatar.
    Se puede cancelar (sin sacarlo del heap) y reprogramar (cancelando el viejo y creando uno nuevo)."""
    def __init__(self, tiempo: int, secuencia: int, accion, descripcion: str = ""):
        self.tiempo = tiempo
        self.secuencia = secuencia
        self.accion = accion
        self.descripcion = descripcion
        self.cancelado = False

    def __lt__(self, otro: "EventoProgramado") -> bool:
        return (self.tiempo, self.secuencia) < (otro.tiempo, otro.secuencia)

    def __repr__(self) -> str:
        estado = "cancelado" if self.cancelado else "vigente"
        return f"EventoProgramado(t={self.tiempo}, seq={self.secuencia}, {estado}, {self.descripcion!r})"


class RelojEventos:
    """Reloj virtual (arranca en 0) + agenda de eventos sobre un HeapMinimo.
      - cancelar(evento) solo pone evento.cancelado = True; el heap no se toca.
      - reprogramar(evento, nuevo_tiempo) cancela el evento viejo y agenda uno nuevo con secuencia nueva
    ejecutar_siguiente() descarta cualquier evento cancelado que salga primero
    del heap y sigue extrayendo hasta encontrar uno vigente (o vaciar la
    agenda).

    La muerte de un actor NO se maneja cancelando uno por uno sus eventos
    futuros. El turno de un actor debe empezar comprobando `actor.esta_vivo()` y no hacer nada si ya murió.
    El evento igual se extrae del heap y el reloj avanza a su tiempo, pero la
    acción en sí se "descarta".
    """

    def __init__(self):
        self._heap = HeapMinimo()
        self._reloj_actual = 0
        self._siguiente_secuencia = 0

    @property
    def tiempo_actual(self) -> int:
        return self._reloj_actual

    def programar(self, tiempo: int, accion, descripcion: str = "") -> EventoProgramado:
        """Devuelve el EventoProgramado, necesario para poder cancelarlo o
        reprogramarlo más adelante."""
        evento = EventoProgramado(tiempo, self._siguiente_secuencia, accion, descripcion)
        self._siguiente_secuencia += 1
        self._heap.insertar(evento)
        return evento

    def programar_en(self, intervalo: int, accion, descripcion: str = "") -> EventoProgramado:
        """Atajo: programa `accion` `intervalo` unidades después del reloj actual."""
        return self.programar(self._reloj_actual + intervalo, accion, descripcion)

    def cancelar(self, evento: EventoProgramado) -> None:
        evento.cancelado = True

    def reprogramar(self, evento: EventoProgramado, nuevo_tiempo: int) -> EventoProgramado:
        self.cancelar(evento)
        return self.programar(nuevo_tiempo, evento.accion, evento.descripcion)

    def ejecutar_siguiente(self) -> EventoProgramado | None:
        """Un paso del bucle principal: obtiene el evento VIGENTE con
        menor (tiempo, secuencia), avanza el reloj a su tiempo, lo ejecuta, y
        lo devuelve. None si no queda ningún evento vigente en la agenda."""
        while True:
            evento = self._heap.eliminar_minimo()
            if evento is None:
                return None
            if not evento.cancelado:
                break
        self._reloj_actual = evento.tiempo
        evento.accion()
        return evento

    def esta_vacia(self) -> bool:
        return len(self._heap.heap) == 0
