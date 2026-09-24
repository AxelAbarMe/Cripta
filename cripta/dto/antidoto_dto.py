from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AntidotoDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int

    @staticmethod
    def desde_json(datos):
        return AntidotoDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
        )