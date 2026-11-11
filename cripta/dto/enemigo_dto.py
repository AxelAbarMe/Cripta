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
    rango : int | None = None  # solo lo usa el cazador, None si no es válido

    @staticmethod
    def desde_json(datos):
        suelta = datos.get("suelta") or []
        rango = datos.get("rango")
        if isinstance(rango, bool) or not isinstance(rango, int) or rango < 1:
            rango = None  # nulo, ausente o inválido: no se lanza excepción (FR-TER-008)
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
            rango=rango,
        )