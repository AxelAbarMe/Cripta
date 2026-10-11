from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TrampaDTO:
    id : str
    nombre : str
    clase : str
    daño : int
    rearme: int | None  # None = la ficha no lo trae. El modelo usa TRAMPA_REARME_DEFAULT (§2.10)

    @staticmethod
    def desde_json(datos):
        return TrampaDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            daño=datos["daño"],
            rearme=datos.get("rearme"),
        )