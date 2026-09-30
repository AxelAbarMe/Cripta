"""ServicioPresupuesto: política sobre el presupuesto de solicitudes de una partida."""
from cripta.excepciones import CriptaLimiteError
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes


class ServicioPresupuesto:
    """Envuelve el ContadorSolicitudes con la política de no gastar más de lo que queda."""

    def __init__(self, contador: ContadorSolicitudes):
        self._contador = contador

    def verificar_disponible(self, cuantas: int = 1) -> None:
        # Se llama ANTES de hacer una solicitud real, para no arriesgarse a
        # gastar presupuesto en un lote que de todos modos no íbamos a poder completar.
        if self._contador.restantes < cuantas:
            raise CriptaLimiteError(self._contador.presupuesto_maximo)

    @property
    def restantes(self) -> int:
        return self._contador.restantes

    def reporte_final(self) -> str:
        return self._contador.reporte()
