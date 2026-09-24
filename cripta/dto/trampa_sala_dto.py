from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TrampaSalaDTO:
    instancia: str
    tipo: str
 
    @staticmethod
    def desde_json(datos):
        return TrampaSalaDTO(
            instancia=datos["instancia"],
            tipo=datos["tipo"],
        )