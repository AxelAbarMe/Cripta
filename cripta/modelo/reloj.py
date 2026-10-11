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
    def __init__(self, tiempo: int, secuencia: int, accion, descripcion: str = "", datos=None):
        self.tiempo = tiempo
        self.secuencia = secuencia
        self.accion = accion
        self.descripcion = descripcion
        self.datos = datos   # (tipo, sujeto, a, b) para guardar la partida; ver estado_guardado.py
        self.cancelado = False
        self.ejecutado = False
        self.en_agenda = True

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
    # Función(inversa) que asigna quien arma el retroceso. El reloj es la parte más caliente del juego,
    # así que registra de forma explícita (un solo "if" por operación) y no con Reversible.
    registrador = None
    
    def __init__(self):
        self._heap = HeapMinimo()
        self._reloj_actual = 0
        self._siguiente_secuencia = 0
        self._vigentes = 0   # eventos que aún pueden ejecutarse (no cancelados ni ejecutados)

    @property
    def tiempo_actual(self) -> int:
        return self._reloj_actual

    def programar(self, tiempo: int, accion, descripcion: str = "", datos=None) -> EventoProgramado:
        """Devuelve el EventoProgramado, necesario para poder cancelarlo o
        reprogramarlo más adelante."""
        
        if tiempo < self._reloj_actual:
            raise ValueError(
                f"No se puede programar un evento en el pasado "
                f"(tiempo {tiempo}, reloj en {self._reloj_actual})."
            )
            
        evento = EventoProgramado(tiempo, self._siguiente_secuencia, accion, descripcion, datos)
        self._siguiente_secuencia += 1
        self._heap.insertar(evento)
        self._vigentes += 1
        if self.registrador is not None:
            self.registrador(lambda: self._deshacer_programar(evento))
        return evento

    def programar_en(self, intervalo: int, accion, descripcion: str = "", datos=None) -> EventoProgramado:
        """Atajo: programa `accion` `intervalo` unidades después del reloj actual."""
        return self.programar(self._reloj_actual + intervalo, accion, descripcion, datos)

    def cancelar(self, evento: EventoProgramado) -> None:
        if not evento.cancelado and not evento.ejecutado:
            self._vigentes -= 1
            if self.registrador is not None:
                self.registrador(lambda: self.restituir(evento))
        evento.cancelado = True

    def reprogramar(self, evento: EventoProgramado, nuevo_tiempo: int) -> EventoProgramado:
        # Se agenda primero el nuevo: si el tiempo es inválido, el viejo no queda cancelado a medias
        nuevo = self.programar(nuevo_tiempo, evento.accion, evento.descripcion, evento.datos)
        self.cancelar(evento)
        return nuevo

    def ejecutar_siguiente(self) -> EventoProgramado | None:
        """Un paso del bucle principal: obtiene el evento VIGENTE con
        menor (tiempo, secuencia), avanza el reloj a su tiempo, lo ejecuta, y
        lo devuelve. None si no queda ningún evento vigente en la agenda."""
        while True:
            evento = self._heap.eliminar_minimo()
            if evento is None:
                return None
            evento.en_agenda = False 
            if not evento.cancelado:
                break
        evento.ejecutado = True               
        self._vigentes -= 1 
        if self.registrador is not None:
            tiempo_anterior = self._reloj_actual
            self.registrador(lambda: self._deshacer_ejecutar(evento, tiempo_anterior))
        self._reloj_actual = evento.tiempo
        evento.accion()
        return evento

    def eventos_vigentes(self) -> tuple:
        """Los eventos que aún pueden ejecutarse (sin los cancelados), sin orden garantizado:
        cada uno trae su (tiempo, secuencia). Sirve para guardar la partida."""
        return tuple(e for e in self._heap.heap if not e.cancelado)

    def esta_vacia(self) -> bool:
        """True si no queda ningún evento vigente (los cancelados no cuentan)."""
        return self._vigentes == 0
    
    @property
    def siguiente_secuencia(self) -> int:
        return self._siguiente_secuencia

    def restaurar(self, tiempo_actual: int, siguiente_secuencia: int) -> None:
        """Deja el reloj y el contador de secuencia como estaban (retroceso y carga de partida)."""
        self._reloj_actual = tiempo_actual
        self._siguiente_secuencia = siguiente_secuencia

    def _deshacer_programar(self, evento: EventoProgramado) -> None:
        self.cancelar(evento)
        self._siguiente_secuencia = evento.secuencia   # la secuencia vuelve a ser la que se reservó

    def _deshacer_ejecutar(self, evento: EventoProgramado, tiempo_anterior: int) -> None:
        self.restituir(evento)
        self._reloj_actual = tiempo_anterior

    def restituir(self, evento: EventoProgramado) -> None:
        """Inverso de cancelar o ejecutar: deja el evento vigente con su mismo (tiempo, secuencia)."""
        if not evento.cancelado and not evento.ejecutado:
            return
        evento.cancelado = False
        evento.ejecutado = False
        if not evento.en_agenda:      # ya había salido del heap: se vuelve a insertar
            self._heap.insertar(evento)
            evento.en_agenda = True
        self._vigentes += 1

    def programar_con_secuencia(self, tiempo: int, secuencia: int, accion, descripcion: str = "", datos=None) -> EventoProgramado:
        """Agenda un evento con una secuencia ya conocida (reconstruir una partida guardada).
        Después hay que llamar a restaurar() para fijar el contador."""
        evento = EventoProgramado(tiempo, secuencia, accion, descripcion, datos)
        self._heap.insertar(evento)
        self._vigentes += 1
        return evento
