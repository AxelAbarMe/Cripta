from dataclasses import dataclass

from cripta.dto.entidad_dto import EntidadDTO, entidad_desde_json

#GET /catalogo?ids=...
@dataclass(frozen=True, slots=True)
class CatalogoDTO:
    entidades : tuple[EntidadDTO, ...]

    @staticmethod
    def desde_json(datos):
        return CatalogoDTO(
            entidades=tuple(entidad_desde_json(e) for e in datos["entidades"]),
        )