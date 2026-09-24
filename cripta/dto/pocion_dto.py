from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PocionDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int
    cura : int | None
    modificador_velocidad : int | None
    duracion : int | None

    @staticmethod
    def desde_json(datos):
        return PocionDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
            cura=datos["cura"],
            modificador_velocidad=datos["modificador_velocidad"],
            duracion=datos["duracion"],
        )