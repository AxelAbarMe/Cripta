"""Estado conocido por el jugador sobre las salas y sus puertas."""
from dataclasses import dataclass

from cripta.modelo.reversible import Reversible


_DIRECCIONES = ("N", "S", "E", "O")
_OPUESTAS = ("S", "N", "O", "E")
_DESCONOCIDA = "desconocida"
_AVISTADA = "avistada"
_EXPLORADA = "explorada"
_NO_OBSERVADA = "no_observada"


@dataclass(frozen=True, slots=True)
class SalidaConocida:
    direccion: str
    id_sala_destino: int
    costo: int
    estado_puerta: str


@dataclass(frozen=True, slots=True)
class SalaConocida:
    id_sala: int
    estado: str
    nombre: str | None
    salidas: tuple[SalidaConocida, ...]


class ConocimientoJugador(Reversible):
    def __init__(self, mapa, sala_inicial: int):
        self.registrador = None
        if sala_inicial not in mapa:
            raise ValueError(f"La sala inicial {sala_inicial} no existe en el mapa")
        self._mapa = mapa
        self._estados = [_DESCONOCIDA] * (max(s.id for s in mapa.todas_las_salas()) + 1)
        self._puertas = [[_NO_OBSERVADA] * 4 for _ in self._estados]
        self._costos = [[None] * 4 for _ in self._estados]
        self._explorar(sala_inicial)

    def estado_de_sala(self, sala_id: int) -> str:
        if not self._id_valido(sala_id):
            return _DESCONOCIDA
        return self._estados[sala_id]

    def sala_conocida(self, sala_id: int) -> SalaConocida | None:
        if self.estado_de_sala(sala_id) != _EXPLORADA:
            return None
        sala = self._mapa.obtener(sala_id)
        salidas = []
        for direccion in _DIRECCIONES:
            salida = sala.esqueleto.salida(direccion)
            if salida is None:
                continue
            indice = _DIRECCIONES.index(direccion)
            estado = self._puertas[sala_id][indice]
            llave, cierre = self._mapa.datos_de_puerta(sala_id, direccion)
            opuesta = self._mapa.obtener(salida.sala_destino)
            salida_opuesta = (opuesta.esqueleto.salida(_OPUESTAS[indice])
                              if opuesta is not None else None)
            tiene_puerta_cerrada = salida.cerrada or (
                salida_opuesta is not None and salida_opuesta.cerrada
            )
            if llave is None and cierre is None and not tiene_puerta_cerrada:
                estado = "abierta"
            salidas.append(SalidaConocida(direccion, salida.sala_destino,
                                         self._costos[sala_id][indice], estado))
        return SalaConocida(sala_id, _EXPLORADA, sala.esqueleto.nombre, tuple(salidas))

    def observar_puerta(self, sala_id: int, direccion: str) -> None:
        indice = self._indice(sala_id, direccion)
        sala = self._mapa.obtener(sala_id)
        if sala is None or sala.esqueleto.salida(direccion) is None:
            raise ValueError(f"La sala {sala_id} no tiene salida hacia {direccion}")
        estado = "cerrada" if sala.puertas.esta_cerrada(direccion) else "abierta"
        self._fijar_celda(self._puertas, sala_id, indice, estado)
        salida = sala.esqueleto.salida(direccion)
        opuesta = self._mapa.obtener(salida.sala_destino)
        if opuesta is not None:
            direccion_opuesta = _OPUESTAS[indice]
            if opuesta.esqueleto.salida(direccion_opuesta) is not None:
                self._fijar_celda(self._puertas, salida.sala_destino,
                                  _DIRECCIONES.index(direccion_opuesta), estado)

    def estado_de_puerta(self, sala_id: int, direccion: str) -> str:
        indice = self._indice(sala_id, direccion)
        if not self._id_valido(sala_id):
            return _NO_OBSERVADA
        return self._puertas[sala_id][indice]

    def al_entrar(self, sala_id: int, antorcha_encendida: bool) -> None:
        if self._mapa.obtener(sala_id) is None:
            raise ValueError(f"La sala {sala_id} no existe en el mapa")
        self._explorar(sala_id)
        for direccion, destino in self._mapa.vecinos(sala_id):
            self.observar_puerta(sala_id, direccion)
            if antorcha_encendida:
                self._explorar(destino)

    def proyectar(self) -> tuple[SalaConocida, ...]:
        resultado = []
        for sala_id, estado in enumerate(self._estados):
            if estado == _EXPLORADA:
                resultado.append(self.sala_conocida(sala_id))
            elif estado == _AVISTADA:
                resultado.append(SalaConocida(sala_id, _AVISTADA, None, ()))
        return tuple(resultado)

    def exportar_celdas(self) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...], tuple[tuple[int | None, ...], ...]]:
        return tuple(self._estados), tuple(tuple(fila) for fila in self._puertas), tuple(
            tuple(fila) for fila in self._costos
        )

    def importar_celdas(self, celdas) -> None:
        estados, puertas, costos = celdas
        cantidad = len(self._estados)
        if (len(estados) != cantidad or len(puertas) != cantidad or len(costos) != cantidad
                or any(len(fila) != len(_DIRECCIONES) for fila in puertas)
                or any(len(fila) != len(_DIRECCIONES) for fila in costos)):
            raise ValueError("El tamaño de las celdas no coincide con el mapa")
        self._estados = list(estados)
        self._puertas = [list(fila) for fila in puertas]
        self._costos = [list(fila) for fila in costos]

    def _explorar(self, sala_id: int) -> None:
        if self.estado_de_sala(sala_id) == _EXPLORADA:
            return
        self._fijar_celda(self._estados, sala_id, None, _EXPLORADA)
        for direccion, destino in self._mapa.vecinos(sala_id):
            indice = _DIRECCIONES.index(direccion)
            self._fijar_celda(self._costos, sala_id, indice,
                              self._mapa.costo_de_conexion(sala_id, direccion))
            if self.estado_de_sala(destino) == _DESCONOCIDA:
                self._fijar_celda(self._estados, destino, None, _AVISTADA)

    def _fijar_celda(self, matriz, sala_id: int, indice, valor) -> None:
        if indice is None:
            anterior = matriz[sala_id]
            if anterior == valor:
                return
            self._registrar_inversa(lambda: matriz.__setitem__(sala_id, anterior))
            matriz[sala_id] = valor
            return
        anterior = matriz[sala_id][indice]
        if anterior == valor:
            return
        self._registrar_inversa(lambda: matriz[sala_id].__setitem__(indice, anterior))
        matriz[sala_id][indice] = valor

    def _id_valido(self, sala_id: int) -> bool:
        return isinstance(sala_id, int) and not isinstance(sala_id, bool) and 0 <= sala_id < len(self._estados)

    @staticmethod
    def _indice(sala_id: int, direccion: str) -> int:
        if direccion not in _DIRECCIONES:
            raise ValueError(f"Dirección inválida: {direccion}")
        return _DIRECCIONES.index(direccion)
