from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class EnemigoSalaDTO:
    instancia: str
    tipo: str
    vida: int | None 
 
    @staticmethod
    def desde_json(datos):
        return EnemigoSalaDTO(
            instancia=datos["instancia"],
            tipo=datos["tipo"],
            vida=datos.get("vida"),
        )