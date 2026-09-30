"""CriptaMapa: junta las páginas del esqueleto en un solo mapa navegable por id de sala
Usa VectorOrdenado: búsqueda por id en O(log n) por búsqueda binaria.
"""
from cripta.estructuras.vector import VectorOrdenado
from cripta.modelo.sala import Sala

class CriptaMapa:
    def __init__(self):
        self._salas = VectorOrdenado(clave=lambda sala: sala.id)

    def agregar_pagina(self, pagina_dto) -> None:
        # pagina_dto: PaginaEsqueletoDTO
        for sala_dto in pagina_dto.salas:
            self._salas.insertar(Sala(sala_dto))

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

    def __len__(self) -> int:
        return len(self._salas)

    def __contains__(self, sala_id: int) -> bool:
        return self._salas.contiene(sala_id)
