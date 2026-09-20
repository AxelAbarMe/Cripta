from dataclasses import dataclass

# el objeto "jugador" dentro de los datos generales de la cripta
@dataclass(frozen=True, slots=True)
class JugadorInicialDTO:
    vida_max: int
    ataque: int
    defensa: int
    velocidad: int

    @staticmethod
    def desde_json(datos):
        return JugadorInicialDTO(
            vida_max=datos["vida_max"],
            ataque=datos["ataque"],
            defensa=datos["defensa"],
            velocidad=datos["velocidad"],
        )