"""Enemigo: instancia concreta de un tipo de catálogo colocada en una sala."""
from cripta.modelo.actor import Actor


class Enemigo(Actor):
    """Une una ficha de catálogo (EnemigoDTO, compartida entre instancias) con el estado
    propio de una instancia: vida actual, sala, si ya está activa, etc.
    """

    def __init__(self, instancia_id: str, ficha, sala_actual: int, vida_inicial: int | None = None):
        # Nota: EnemigoDTO. vida_inicial puede venir menor que vida_max
        super().__init__(
            nombre=ficha.nombre,
            vida_max=ficha.vida_max,
            ataque=ficha.ataque,
            defensa=ficha.defensa,
            velocidad=ficha.velocidad,
            sala_actual=sala_actual,
        )
        self.instancia_id = instancia_id
        self.tipo_catalogo = ficha.id
        self.comportamiento = ficha.comportamiento
        self.suelta = ficha.suelta
        self.activo = False  # se activa solo cuando el jugador entra a su sala

        if vida_inicial is not None:
            if vida_inicial < 0:
                raise ValueError("vida_inicial no puede ser negativa")
            self.vida = min(vida_inicial, self.vida_max)

    def activar(self) -> None:
        self.activo = True

    def etiqueta(self) -> str:
        # Presentación identificable de la instancia, por ejemplo "Rata gigante [e-201]"
        return f"{self.nombre} [{self.instancia_id}]"
