from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class LlaveDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int
    abre : str | None

    @staticmethod
    def desde_json(datos):
        return LlaveDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
            abre=datos.get("abre"),
        )