from dataclasses import dataclass

from cripta.dto.jugador_inicial_dto import JugadorInicialDTO


# GET /criptas/{id}
@dataclass(frozen=True, slots=True)
class CriptaGeneralDTO:
    id: str
    version: str
    salas_total: int
    paginas: int
    salas_por_pagina: int
    sala_inicial: int
    sala_salida: int
    llave_salida: str
    presupuesto_solicitudes: int
    inventario_max: int
    jugador: JugadorInicialDTO

    @staticmethod
    def desde_json(datos):
        return CriptaGeneralDTO(
            id=datos["id"],
            version=datos["version"],
            salas_total=datos["salas_total"],
            paginas=datos["paginas"],
            salas_por_pagina=datos["salas_por_pagina"],
            sala_inicial=datos["sala_inicial"],
            sala_salida=datos["sala_salida"],
            llave_salida=datos["llave_salida"],
            presupuesto_solicitudes=datos["presupuesto_solicitudes"],
            inventario_max=datos["inventario_max"],
            jugador=JugadorInicialDTO.desde_json(datos["jugador"]),
        )