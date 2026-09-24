class CriptaError(Exception):
    """Clase base para todas las excepciones de Cripta."""
    pass

class CriptaApiError(CriptaError):
    """Excepción para errores de la API de Cripta."""
    def __init__(self, operacion : str, codigo : int, mensaje : str):
        self.operacion = operacion
        self.codigo = codigo
        self.mensaje = mensaje
        super().__init__(f"Error en {operacion}: {codigo} - {mensaje}")

class CriptaLimiteError(CriptaError):
    """Excepción para errores de límite de solicitudes de la API de Cripta."""
    def __init__(self, presupuesto_max : int):
        self.presupuesto_max = presupuesto_max
        super().__init__(f"Se agotó el presupuesto de solicitudes: ({presupuesto_max}).")