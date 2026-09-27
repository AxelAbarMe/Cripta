from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TrampaDTO:
    id : str
    nombre : str
    clase : str
    daño : int
    rearme : int

    @staticmethod
    def desde_json(datos):
        return TrampaDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            daño=datos["daño"],
            rearme=datos.get("rearme"),
        )