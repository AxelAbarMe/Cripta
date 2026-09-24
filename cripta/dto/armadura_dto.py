from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ArmaduraDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int
    defensa_bonus : int

    @staticmethod
    def desde_json(datos):
        return ArmaduraDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
            defensa_bonus=datos["defensa_bonus"],
        )