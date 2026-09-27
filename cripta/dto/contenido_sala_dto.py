from dataclasses import dataclass

from cripta.dto.enemigo_sala_dto import EnemigoSalaDTO
from cripta.dto.trampa_sala_dto import TrampaSalaDTO



@dataclass(frozen=True, slots=True)
class ContenidoSalaDTO:
    id: int
    enemigos: tuple[EnemigoSalaDTO, ...]
    objetos: tuple[str, ...]
    trampas: tuple[TrampaSalaDTO, ...]

    @staticmethod
    def desde_json(datos):
        enemigos = datos.get("enemigos", [])
        objetos = datos.get("objetos", [])
        trampas = datos.get("trampas", [])
        return ContenidoSalaDTO(
            id=datos["sala"],
            enemigos=tuple(EnemigoSalaDTO.desde_json(e) for e in enemigos),
            objetos=tuple(objetos),
            trampas=tuple(TrampaSalaDTO.desde_json(t) for t in trampas),
        )