"""BuscadorRutas: costo mínimo desde la sala del jugador hacia las salas que ve un cazador.
Una sola tabla plana indexada por id de sala se comparte entre todos los cazadores.
La cola de prioridad es HeapMinimo, sin bibliotecas de rutas ni de estructuras.
"""
from cripta.constantes import COSTO_ESPERAR
from cripta.estructuras.heap_min import HeapMinimo


class BuscadorRutas:
    def __init__(self):
        self._distancias: list[int | None] = []
        self._cerrados: list[bool] = []
        self._sala_objetivo: int | None = None
        self._rango_max_calculado = -1
        self._valido = False

    def invalidar(self) -> None:
        # La próxima consulta recalcula la tabla
        self._valido = False

    def calcular_o_reutilizar(self, mapa, sala_jugador_id: int, rango_max: int) -> None:
        # Recalcula si la tabla es inválida, es de otra sala o el rango pedido supera el calculado
        if self._valido and self._sala_objetivo == sala_jugador_id and rango_max <= self._rango_max_calculado:
            return
        self._calcular(mapa, sala_jugador_id, rango_max)

    def distancia(self, sala_id: int) -> int | None:
        # Distancia guardada para la sala o None si no fue alcanzada
        if sala_id < 0 or sala_id >= len(self._distancias):
            return None
        return self._distancias[sala_id]

    def decidir_paso(self, cazador, sala_jugador_id: int, mapa) -> tuple[str, str | None, int]:
        # Devuelve (accion, direccion, costo) con desempate por el menor id de sala vecina
        self.calcular_o_reutilizar(mapa, sala_jugador_id, cazador.rango)
        origen = cazador.sala_actual
        if not self._esta_cerrada(origen) or self._distancias[origen] > cazador.rango:
            return ("esperar", None, COSTO_ESPERAR)
        total = self._distancias[origen]
        mejor = None
        for direccion, destino in mapa.vecinos(origen):
            if not mapa.puerta_transitable(origen, direccion) or not self._esta_cerrada(destino):
                continue
            costo = mapa.costo_de_conexion(origen, direccion)
            if costo + self._distancias[destino] != total:
                continue
            if mejor is None or destino < mejor[0]:
                mejor = (destino, direccion, costo)
        if mejor is None:
            return ("esperar", None, COSTO_ESPERAR)
        return ("mover", mejor[1], mejor[2])

    def _esta_cerrada(self, sala_id: int) -> bool:
        # Verdadero si la sala ya tiene su distancia mínima definitiva
        return 0 <= sala_id < len(self._cerrados) and self._cerrados[sala_id]

    def _calcular(self, mapa, sala_jugador_id: int, rango_max: int) -> None:
        # Dijkstra desde el jugador por salidas abiertas con poda al superar rango_max
        salas = mapa.todas_las_salas()
        tamano = (salas[-1].id + 1) if len(salas) > 0 else 0
        self._distancias = [None] * tamano
        self._cerrados = [False] * tamano
        self._sala_objetivo = sala_jugador_id
        self._rango_max_calculado = rango_max
        self._valido = True
        if sala_jugador_id < 0 or sala_jugador_id >= tamano:
            return
        cola = HeapMinimo()
        self._distancias[sala_jugador_id] = 0
        cola.insertar((0, sala_jugador_id))
        while not cola.esta_vacio():
            distancia, sala = cola.eliminar_minimo()
            if distancia > rango_max:
                break
            if self._cerrados[sala]:
                continue
            self._cerrados[sala] = True
            self._relajar_vecinas(mapa, sala, distancia, cola)

    def _relajar_vecinas(self, mapa, sala: int, distancia: int, cola) -> None:
        # Mejora la distancia de cada vecina alcanzable por una salida abierta
        for direccion, destino in mapa.vecinos(sala):
            if not mapa.puerta_transitable(sala, direccion) or destino >= len(self._distancias):
                continue
            nueva = distancia + mapa.costo_de_conexion(sala, direccion)
            actual = self._distancias[destino]
            if not self._cerrados[destino] and (actual is None or nueva < actual):
                self._distancias[destino] = nueva
                cola.insertar((nueva, destino))
