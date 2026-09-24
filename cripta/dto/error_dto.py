from dataclasses import dataclass

dataclass(frozen=True, slots=True)
class ErrorApiDTO:
    error: str

    @staticmethod
    def desde_json(datos):
        return ErrorApiDTO(error=datos["error"])

dataclass(frozen=True, slots=True)
class ErrorLimiteDTO:
    error: str
    reintentar_en : int

    @staticmethod
    def desde_json(datos):
        return ErrorLimiteDTO(
            error=datos["error"],
            reintentar_en=datos["reintentar_en"],
        )