"""CriptaMapa: junta las páginas del esqueleto en un solo mapa navegable por id de sala
Usa VectorOrdenado: búsqueda por id en O(log n) por búsqueda binaria.
"""
from cripta.estructuras.vector import VectorOrdenado
from cripta.modelo.sala import Sala
from cripta.constantes import direccion_opuesta

class CriptaMapa:
    def __init__(self):
        self._salas = VectorOrdenado(clave=lambda sala: sala.id)

    def agregar_pagina(self, pagina_dto) -> None:
        # pagina_dto: PaginaEsqueletoDTO
        for sala_dto in pagina_dto.salas:
            if self._salas.contiene(sala_dto.id):
                continue   # página repetida (por ejemplo, un reintento): se ignora
            self._salas.insertar(Sala(sala_dto))

    def todas_las_salas(self) -> tuple:
        """Todas las salas, en orden ascendente de id."""
        return self._salas.elementos()

    def obtener(self, sala_id: int) -> Sala | None:
        return self._salas.buscar(sala_id)

    def vecinos(self, sala_id: int) -> tuple[tuple[str, int], ...]:
        # [(direccion, id_sala_destino), ...] para las salidas que existen, abiertas o no
        sala = self.obtener(sala_id)
        if sala is None:
            raise ValueError(f"Sala {sala_id} no está en el mapa")
        resultado = []
        for direccion in ("N", "S", "E", "O"):
            salida = sala.esqueleto.salida(direccion)
            if salida is not None:
                resultado.append((direccion, salida.sala_destino))
        return tuple(resultado)



    def puerta_transitable(self, sala_id: int, direccion: str) -> bool:
        """True si existe la salida y su puerta está abierta."""
        sala = self.obtener(sala_id)
        if sala is None or sala.esqueleto.salida(direccion) is None:
            return False
        return not sala.puertas.esta_cerrada(direccion)


    def datos_de_puerta(self, sala_id: int, direccion: str) -> tuple[str | None, int | None]:
        """Devuelve (llave, cierre_automatico) de la puerta, mirando los dos lados:
        el API solo marca la llave y el cierre en uno de ellos (§2.1)."""
        sala = self.obtener(sala_id)
        salida = sala.esqueleto.salida(direccion) if sala is not None else None
        if salida is None:
            raise ValueError(f"La sala {sala_id} no tiene salida hacia {direccion}")
        llave, cierre = salida.llave, salida.cierre_automatico
        otra = self.obtener(salida.sala_destino)
        if otra is not None:
            salida_opuesta = otra.esqueleto.salida(direccion_opuesta(direccion))
            if salida_opuesta is not None:
                llave = llave if llave is not None else salida_opuesta.llave
                cierre = cierre if cierre is not None else salida_opuesta.cierre_automatico
        return llave, cierre


    def conectar_registrador(self, registrador) -> None:
        """Conecta el retroceso a todas las salas y a sus puertas."""
        for sala in self._salas.elementos():
            sala.registrador = registrador
            sala.puertas.registrador = registrador

    def abrir_puerta(self, sala_id: int, direccion: str) -> None:
        self._fijar_puerta(sala_id, direccion, cerrada=False)

    def cerrar_puerta(self, sala_id: int, direccion: str) -> None:
        self._fijar_puerta(sala_id, direccion, cerrada=True)

    def _fijar_puerta(self, sala_id: int, direccion: str, cerrada: bool) -> None:
        # Una salida conecta dos salas (§2.1): se cambia el estado de los dos lados
        sala = self.obtener(sala_id)
        salida = sala.esqueleto.salida(direccion) if sala is not None else None
        if salida is None:
            raise ValueError(f"La sala {sala_id} no tiene salida hacia {direccion}")
        lados = [(sala, direccion)]
        opuesta = direccion_opuesta(direccion)
        otra = self.obtener(salida.sala_destino)
        if otra is not None and otra.esqueleto.salida(opuesta) is not None:
            lados.append((otra, opuesta))
        for lado_sala, lado_direccion in lados:
            if cerrada:
                lado_sala.puertas.cerrar(lado_direccion)
            else:
                lado_sala.puertas.abrir(lado_direccion)

    def sincronizar_puertas(self) -> None:
        """Si un lado de una puerta está cerrado, queda cerrado en los dos.
        Se llama una vez, después de agregar todas las páginas del esqueleto."""
        for sala in self._salas.elementos():
            for direccion, destino in self.vecinos(sala.id):
                otra = self.obtener(destino)
                opuesta = direccion_opuesta(direccion)
                if otra is None or otra.esqueleto.salida(opuesta) is None:
                    continue
                if sala.puertas.esta_cerrada(direccion) or otra.puertas.esta_cerrada(opuesta):
                    sala.puertas.cerrar(direccion)
                    otra.puertas.cerrar(opuesta)


    def __len__(self) -> int:
        return len(self._salas)

    def __contains__(self, sala_id: int) -> bool:
        return self._salas.contiene(sala_id)
