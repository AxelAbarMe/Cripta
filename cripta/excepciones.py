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

class CriptaDatosNoEncontradosError(CriptaError):
    """No se encontró en disco el archivo esperado para una operación en modo --offline."""
    def __init__(self, operacion: str, ruta: str):
        self.operacion = operacion
        self.ruta = ruta
        super().__init__(f"No se encontró el archivo para «{operacion}»: {ruta}")

class CriptaLimiteError(CriptaError):
    """Excepción para errores de límite de solicitudes de la API de Cripta."""
    def __init__(self, presupuesto_max : int):
        self.presupuesto_max = presupuesto_max
        super().__init__(f"Se agotó el presupuesto de solicitudes: ({presupuesto_max}).")

class CriptaFormatoIncompatibleError(CriptaError):
    """El archivo de guardado no es de este programa o es de otra versión del formato (§4.10)."""
    def __init__(self, motivo: str):
        self.motivo = motivo
        super().__init__(f"Archivo de guardado incompatible: {motivo}")