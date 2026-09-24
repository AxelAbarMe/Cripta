from dataclasses import dataclass

from cripta.dto.contenido_sala_dto import ContenidoSalaDTO

@dataclass(frozen=True, slots=True)
class ContenidoSalaRespuestaDTO:
    salas: tuple[ContenidoSalaDTO, ...]
 
    @staticmethod
    def desde_json(datos):
        return ContenidoSalaRespuestaDTO(
            salas=tuple(ContenidoSalaDTO.desde_json(s) for s in datos["contenido"]),
        )