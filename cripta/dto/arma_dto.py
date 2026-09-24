from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArmaDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int
    ataque_bonus : int

    @staticmethod
    def desde_json(datos):
        return ArmaDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
            ataque_bonus=datos["ataque_bonus"],
        )