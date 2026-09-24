from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AntorchaDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int
    duracion : int

    @staticmethod
    def desde_json(datos):
        return AntorchaDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
            duracion=datos["duracion"],
        )