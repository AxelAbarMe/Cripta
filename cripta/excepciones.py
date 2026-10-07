class CriptaError(Exception):
    """Clase base para todas las excepciones de Cripta."""
    pass

# === RED / DISCO (Saul) ===
class CriptaApiError(CriptaError):
    """Excepción para errores de la API de Cripta."""
    def __init__(self, operacion: str, codigo: int | None, mensaje: str):
        # codigo es None cuando no hubo respuesta HTTP (sin conexión, timeout) o el problema
        # fue el contenido de la respuesta, no su código
        self.operacion = operacion
        self.codigo = codigo
        self.mensaje = mensaje
        if codigo is None:
            super().__init__(f"Error en {operacion}: {mensaje}")
        else:
            super().__init__(f"Error en {operacion} (HTTP {codigo}): {mensaje}")

class CriptaDatosNoEncontradosError(CriptaError):
    """No se encontró en disco el archivo esperado para una operación en modo --offline."""
    def __init__(self, operacion: str, ruta: str):
        self.operacion = operacion
        self.ruta = ruta
        super().__init__(f"No se encontró el archivo para «{operacion}»: {ruta}")

class CriptaDatosInvalidosError(CriptaError):
    """Un archivo de --offline existe, pero su contenido no es JSON o no tiene la forma esperada."""
    def __init__(self, operacion: str, ruta: str, detalle: str):
        self.operacion = operacion
        self.ruta = ruta
        self.detalle = detalle
        super().__init__(f"Datos inválidos para «{operacion}» en {ruta}: {detalle}")

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
        
# === MODELO (Isaac) ===