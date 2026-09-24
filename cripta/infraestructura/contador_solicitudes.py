class ContadorSolicitudes:

    def __init__(self, presupuesto_maximo: int):
        self._presupuesto_maximo = presupuesto_maximo
        self._realizadas = 0

    @property
    def presupuesto_maximo(self) -> int:
        return self._presupuesto_maximo

    @property
    def realizadas(self) -> int:
        return self._realizadas

    @property
    def restantes(self) -> int:
        return max(0, self._presupuesto_maximo - self._realizadas)
    
    def registrar_solicitud(self) -> None:
        self._realizadas += 1

    def reporte(self) -> str:
        return (f"Solicitudes realizadas: {self._realizadas}, Presupuesto máximo: {self._presupuesto_maximo}, Restantes: {self.restantes}")
