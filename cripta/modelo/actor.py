"""Actor: comportamiento común a Jugador y Enemigo (vida, combate y reloj de acciones."""


class Actor:
    def __init__(self, nombre: str, vida_max: int, ataque: int, defensa: int, velocidad: int, sala_actual: int):
        if vida_max <= 0:
            raise ValueError("vida_max debe ser positivo")
        if velocidad <= 0:
            raise ValueError("velocidad debe ser positivo")
        self.nombre = nombre
        self.vida_max = vida_max
        self.vida = vida_max
        self.ataque_base = ataque
        self.defensa_base = defensa
        self.velocidad = velocidad
        self.sala_actual = sala_actual
        self.tiempo_siguiente = 0  # el reloj lo fija al activar al actor
        self.evento_pendiente = None

    def esta_vivo(self) -> bool:
        return self.vida > 0

    def recibir_daño(self, cantidad: int) -> None:
        # La vida nunca baja de 0
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo")
        self.vida = max(0, self.vida - cantidad)

    def curar(self, cantidad: int) -> None:
        # La vida nunca supera vida_max
        if cantidad < 0:
            raise ValueError("La curación no puede ser negativa")
        self.vida = min(self.vida_max, self.vida + cantidad)
        
    @property
    def ataque_efectivo(self) -> int:
        return self.ataque_base

    @property
    def defensa_efectiva(self) -> int:
        return self.defensa_base

