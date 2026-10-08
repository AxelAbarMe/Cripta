"""Efectos temporales y del entorno: veneno, cambio de velocidad,
antorcha, regeneración, activación/rearme de trampas, y cierre automático de
puertas. Ninguno guarda su propia copia del reloj más allá de
la referencia necesaria para programar/cancelar.
"""
from cripta.constantes import (
    REGENERACION_ENEMIGO,
    TRAMPA_REARME_DEFAULT,
    VELOCIDAD_MINIMA,
    VENENO_DURACION,
    VENENO_INTERVALO,
)
from cripta.modelo.reloj import calcular_tiempo_reprogramado

class EfectoVeneno:
    """Aplica `daño_por_pulso` cada VENENO_INTERVALO unidades, durante
    VENENO_DURACION unidades desde que se aplicó. Un antídoto lo
    cancela antes de que se agoten los pulsos restantes; los pulsos ya
    aplicados no se revierten al cancelar
    """
    def __init__(self, reloj, objetivo, daño_por_pulso: int):
        self._reloj = reloj
        self._objetivo = objetivo
        self._daño_por_pulso = daño_por_pulso
        self._pulsos_restantes = VENENO_DURACION // VENENO_INTERVALO
        self._cancelado = False
        self.evento_actual = None

    def iniciar(self) -> None:
        # Un veneno nuevo reemplaza al anterior y reinicia la duración (no se acumula)
        anterior = self._objetivo.veneno_activo
        if anterior is not None:
            anterior.cancelar()
        self._objetivo.veneno_activo = self
        self._siguiente_pulso()

    def cancelar(self) -> None:
        self._cancelado = True
        if self.evento_actual is not None:
            self._reloj.cancelar(self.evento_actual)
        self._liberar()

    def _liberar(self) -> None:
        if self._objetivo.veneno_activo is self:
            self._objetivo.veneno_activo = None

    def _siguiente_pulso(self) -> None:
        if self._cancelado or self._pulsos_restantes <= 0:
            self._liberar()
            return
        # Cada pulso se programa VENENO_INTERVALO unidades después del anterior (el primero, tras aplicar el veneno).
        self.evento_actual = self._reloj.programar_en(
            VENENO_INTERVALO, self._aplicar_pulso, descripcion="veneno: pulso"
        )

    # El pulso se aplica solo si el efecto no fue cancelado y el objetivo sigue vivo. Luego se programa el siguiente pulso.
    def _aplicar_pulso(self) -> None:
        if self._cancelado or not self._objetivo.esta_vivo():
            self._liberar()
            return
        self._objetivo.recibir_daño(self._daño_por_pulso)
        self._pulsos_restantes -= 1
        self._siguiente_pulso()


class EfectoCambioVelocidad:
    """Modifica temporalmente la velocidad de un actor y reajusta su próxima acción ya programada."""

    def __init__(self, reloj, actor, modificador_velocidad: int, duracion: int):
        self._reloj = reloj
        self._actor = actor
        self._modificador = modificador_velocidad
        self._duracion = duracion
        self._cambio_aplicado = 0   # cuánto cambió realmente la velocidad (menos si se acotó al mínimo)
        self.evento_fin = None

    def aplicar(self) -> None:
        velocidad_anterior = self._actor.velocidad
        velocidad_nueva = max(VELOCIDAD_MINIMA, velocidad_anterior + self._modificador)
        self._cambio_aplicado = velocidad_nueva - velocidad_anterior
        self._reescalar_a(velocidad_nueva)
        self._actor.velocidad = velocidad_nueva
        self.evento_fin = self._reloj.programar_en(self._duracion, self._terminar, "fin de cambio de velocidad")

    def _terminar(self) -> None:
        # Se resta lo que este efecto sumó, así varios efectos solapados no se pisan entre sí
        velocidad_nueva = max(VELOCIDAD_MINIMA, self._actor.velocidad - self._cambio_aplicado)
        self._reescalar_a(velocidad_nueva)
        self._actor.velocidad = velocidad_nueva

    def _reescalar_a(self, velocidad_nueva: int) -> None:
        evento = getattr(self._actor, "evento_pendiente", None) # Forma segura de recuperar el evento pendiente, aunque no exista el atributo (ej. si el actor murió y se borró).
        if evento is None or evento.cancelado:
            return  # el actor no tiene una acción pendiente que reajustar (ej. murió)
        nuevo_tiempo = calcular_tiempo_reprogramado(
            evento.tiempo, self._reloj.tiempo_actual, self._actor.velocidad, velocidad_nueva,
        )
        # Reprograma el evento pendiente del actor con el nuevo tiempo calculado según la nueva velocidad.
        self._actor.evento_pendiente = self._reloj.reprogramar(evento, nuevo_tiempo)


class EfectoAntorcha:
    """Al encenderse, programa su apagado tras `duracion` unidades."""

    def __init__(self, reloj, duracion: int, al_apagar):
        self._reloj = reloj
        self._duracion = duracion
        self._al_apagar = al_apagar

    # Al encenderse, programa el apagado de la antorcha tras `duracion` unidades de tiempo, llamando a `al_apagar` cuando se apague.
    def encender(self) -> None:
        self._reloj.programar_en(self._duracion, self._al_apagar, "antorcha: apagar")


class EfectoRegeneracion:
    """Un enemigo con regeneración recupera `cantidad` cada
    REGENERACION_ENEMIGO, sin superar vida_max. Se detiene sola si el objetivo muere."""

    def __init__(self, reloj, objetivo, cantidad: int):
        self._reloj = reloj
        self._objetivo = objetivo
        self._cantidad = cantidad
        self._cancelado = False

    def iniciar(self) -> None:
        self._programar_siguiente()

    def cancelar(self) -> None:
        self._cancelado = True

    def _programar_siguiente(self) -> None:
        if self._cancelado:
            return
        self._reloj.programar_en(REGENERACION_ENEMIGO, self._aplicar, "regeneración")

    # El efecto se aplica solo si no fue cancelado y el objetivo sigue vivo. Luego se programa la siguiente regeneración.
    def _aplicar(self) -> None:
        if self._cancelado or not self._objetivo.esta_vivo():
            return
        self._objetivo.curar(self._cantidad)
        self._programar_siguiente()


class EfectoTrampa:
    """Al activarse (el jugador entra a la sala con la trampa armada), aplica
    su efecto, queda desarmada, y programa su rearme. Si ya estaba
    desarmada, activar() no hace nada."""

    def __init__(self, reloj, trampa, intervalo_rearme: int = TRAMPA_REARME_DEFAULT):
        self._reloj = reloj
        self._trampa = trampa
        self._intervalo_rearme = intervalo_rearme

    '''Activa la trampa si está armada, aplicando su efecto y programando su rearme 
    tras el intervalo indicado. Devuelve True si se activó, False si ya estaba desarmada.
    `aplicar_efecto` es una función que aplica el efecto de la trampa'''
    def activar(self, aplicar_efecto) -> bool:
        if not self._trampa.armada:
            return False
        aplicar_efecto()
        self._trampa.desarmar()
        self._reloj.programar_en(self._intervalo_rearme, self._trampa.rearmar, "trampa: rearme")
        return True


class EfectoCierrePuerta:
    """Programa el cierre automático de una puerta tras el intervalo indicado al abrirse."""

    def __init__(self, reloj, sala, direccion: str, intervalo: int):
        self._reloj = reloj
        self._sala = sala
        self._direccion = direccion
        self._intervalo = intervalo

    def programar_cierre(self) -> None:
        self._reloj.programar_en(self._intervalo, self._cerrar, "cierre automático de puerta")

    def _cerrar(self) -> None:
        self._sala.puertas.cerrar(self._direccion)
