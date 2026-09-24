from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnemigoDTO:
    id : str
    nombre : str
    clase : str
    vida_max : int
    ataque : int
    defensa : int
    velocidad : int
    comportamiento : str
    suelta : tuple[str, ...]

    @staticmethod
    def desde_json(datos):
        suelta = datos.get("suelta") or []
        return EnemigoDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            vida_max=datos["vida_max"],
            ataque=datos["ataque"],
            defensa=datos["defensa"],
            velocidad=datos["velocidad"],
            comportamiento=datos["comportamiento"],
            suelta=tuple(suelta),
        )