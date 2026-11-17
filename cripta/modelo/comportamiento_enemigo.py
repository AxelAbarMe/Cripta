"""Decisión de un enemigo en su turno (§2.8).

Este módulo solo DECIDE qué hace el enemigo. Ejecutar la acción y reprogramar su siguiente turno
lo hace el motor (atacar y esperar cuestan 100, moverse cuesta lo que la salida atravesada).
La decisión es una pareja (tipo, direccion), por ejemplo ("mover", "N"). El cazador agrega el costo.
"""
from cripta.constantes import COSTO_ATACAR, COSTO_ESPERAR, RASTRO_ANTIGUEDAD_MAX


def decidir_accion_enemigo(enemigo, sala_jugador_id: int, mapa, azar, tiempo_actual: int, buscador=None):
    """Si comparte sala con el jugador ataca. Si no, aplica su comportamiento.
    El cazador devuelve una tripleta (tipo, direccion, costo), los demás una pareja."""
    if enemigo.comportamiento == "cazador":
        return _decidir_cazador(enemigo, sala_jugador_id, mapa, buscador)
    if enemigo.sala_actual == sala_jugador_id:
        return ("atacar", None)
    if enemigo.comportamiento == "errante":
        return _decidir_errante(enemigo, mapa, azar)
    if enemigo.comportamiento == "rastreador":
        return _decidir_rastreador(enemigo, mapa, tiempo_actual)
    return ("esperar", None)   # guardián: nunca abandona su sala


def _decidir_cazador(enemigo, sala_jugador_id: int, mapa, buscador):
    """Ataca si comparte sala. Sin rango o sin buscador espera. Si no, sigue la ruta de costo mínimo."""
    if enemigo.sala_actual == sala_jugador_id:
        return ("atacar", None, COSTO_ATACAR)
    if enemigo.rango is None or buscador is None:
        return ("esperar", None, COSTO_ESPERAR)
    return buscador.decidir_paso(enemigo, sala_jugador_id, mapa)


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