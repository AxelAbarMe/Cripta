"""Decisión de un enemigo en su turno (§2.8).

Este módulo solo DECIDE qué hace el enemigo; ejecutar la acción (atacar, moverse o
esperar, las tres de costo 100) y reprogramar su siguiente turno lo hace el motor.
La decisión es una pareja (tipo, direccion): ("atacar", None), ("mover", "N") o ("esperar", None).
"""
from cripta.constantes import RASTRO_ANTIGUEDAD_MAX


def decidir_accion_enemigo(enemigo, sala_jugador_id: int, mapa, azar, tiempo_actual: int):
    """Si comparte sala con el jugador ataca; si no, aplica su comportamiento."""
    if enemigo.sala_actual == sala_jugador_id:
        return ("atacar", None)
    if enemigo.comportamiento == "errante":
        return _decidir_errante(enemigo, mapa, azar)
    if enemigo.comportamiento == "rastreador":
        return _decidir_rastreador(enemigo, mapa, tiempo_actual)
    return ("esperar", None)   # guardián: nunca abandona su sala


def _decidir_errante(enemigo, mapa, azar):
    """Elige al azar una salida abierta y transitable; si no hay ninguna, espera.
    Consume exactamente una llamada al generador cuando hay al menos una salida."""
    abiertas = [direccion for direccion, _destino in mapa.vecinos(enemigo.sala_actual)
                if mapa.puerta_transitable(enemigo.sala_actual, direccion)]
    if not abiertas:
        return ("esperar", None)
    return ("mover", abiertas[azar.randint(0, len(abiertas) - 1)])


def _decidir_rastreador(enemigo, mapa, tiempo_actual: int):
    """Sigue el rastro fresco más reciente entre las salas vecinas accesibles (§2.9).
    Con rastros iguales gana la sala de menor id. Mira como mucho 4 salidas."""
    mejor = None   # (rastro, id_sala, direccion)
    for direccion, destino in mapa.vecinos(enemigo.sala_actual):
        if not mapa.puerta_transitable(enemigo.sala_actual, direccion):
            continue
        sala = mapa.obtener(destino)
        if sala is None or not sala.rastro_es_fresco(tiempo_actual, RASTRO_ANTIGUEDAD_MAX):
            continue
        rastro = sala.rastro_ultima_visita
        if mejor is None or rastro > mejor[0] or (rastro == mejor[0] and destino < mejor[1]):
            mejor = (rastro, destino, direccion)
    if mejor is None:
        return ("esperar", None)
    return ("mover", mejor[2])