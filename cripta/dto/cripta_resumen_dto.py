from dataclasses import dataclass


# GET /criptas -> un elemento de la lista "criptas"
@dataclass(frozen=True, slots=True)
class CriptaResumenDTO:
    id: str
    nombre: str
    salas: int
    dificultad: int

    @staticmethod
    def desde_json(datos):
        return CriptaResumenDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            salas=datos["salas"],
            dificultad=datos["dificultad"],
        )

    @staticmethod
    def lista_desde_json(datos):
        # GET /criptas devuelve {"criptas": [...]}: convierte cada elemento de esa lista en un resumen
        return tuple(CriptaResumenDTO.desde_json(c) for c in datos["criptas"])