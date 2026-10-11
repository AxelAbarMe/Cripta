from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class LlaveDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int
    abre: str | int | None  # informativo: la puerta se abre si su "llave" coincide con el id de esta ficha

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