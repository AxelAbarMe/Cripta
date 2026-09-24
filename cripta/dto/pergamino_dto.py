from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PergaminoDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int

    @staticmethod
    def desde_json(datos):
        return PergaminoDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
        )