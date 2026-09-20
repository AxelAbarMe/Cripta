from dataclasses import dataclass

from cripta.dto.sala_dto import SalaDTO


# GET /criptas/{id}/salas?pagina=n
@dataclass(frozen=True, slots=True)
class PaginaEsqueletoDTO:
    pagina: int
    total_paginas: int
    salas: tuple[SalaDTO, ...]

    @staticmethod
    def desde_json(datos):
        return PaginaEsqueletoDTO(
            pagina=datos["pagina"],
            total_paginas=datos["total_paginas"],
            salas=tuple(SalaDTO.desde_json(s) for s in datos["salas"]),
        )