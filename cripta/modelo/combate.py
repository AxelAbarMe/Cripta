import random

from cripta.constantes import RAND_MAX, RAND_MIN, DANO_MIN;

def calcular_daño(atacante, defensor, azar: random.Random) -> int:
    """daño = max(1, ataque + azar.randint(0,4) - defensa). `azar` debe ser la
    random.Random(semilla) propia del modelo, nunca el generador global (§2.6).
    """
    daño = atacante.ataque_efectivo + azar.randint(RAND_MIN, RAND_MAX) - defensor.defensa_efectiva
    return max(DANO_MIN, daño)


def atacar(atacante, defensor, azar: random.Random) -> int:
    """Calcula el daño, se lo aplica al defensor y devuelve cuánto recibió."""
    daño = calcular_daño(atacante, defensor, azar)
    defensor.recibir_daño(daño)
    return daño
