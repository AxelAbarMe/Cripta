"""Jugador: actor controlado por la persona, con inventario y equipo."""
from cripta.modelo.actor import Actor
from cripta.modelo.inventario import Inventario


class Jugador(Actor):
    """Las estadísticas iniciales vienen siempre de la cripta (JugadorInicialDTO)."""
    def __init__(self, datos_iniciales, sala_actual: int, inventario_max: int):
        # datos_iniciales: JugadorInicialDTO
        super().__init__(
            nombre="Jugador",
            vida_max=datos_iniciales.vida_max,
            ataque=datos_iniciales.ataque,
            defensa=datos_iniciales.defensa,
            velocidad=datos_iniciales.velocidad,
            sala_actual=sala_actual,
        )
        self.inventario = Inventario(capacidad_max=inventario_max)

    @property
    def ataque_efectivo(self) -> int:
        # Suma el bonus del arma equipada, si hay una
        arma = self.inventario.arma_equipada
        return self.ataque_base + (arma.ficha.ataque_bonus if arma else 0)

    @property
    def defensa_efectiva(self) -> int:
        # Suma el bonus de la armadura equipada, si hay una
        armadura = self.inventario.armadura_equipada
        return self.defensa_base + (armadura.ficha.defensa_bonus if armadura else 0)
