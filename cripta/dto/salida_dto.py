from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SalidaDTO:
    sala_destino: int
    cerrada: bool
    llave: str | None
    cierre_automatico: int | None
    costo: int | None = None  # None: este lado no lo declara (CriptaMapa aplica el 100 por defecto)

    @staticmethod
    def desde_json(datos):
        costo = datos.get("costo")
        if costo is not None and (isinstance(costo, bool) or not isinstance(costo, int) or costo < 1):
            raise ValueError(f"costo inválido ({costo!r}) en la salida hacia la sala {datos['sala']}: "
                             f"debe ser un entero >= 1")
        return SalidaDTO(
            sala_destino=datos["sala"],
            cerrada=bool(datos.get("cerrada")),  # un null del JSON queda como False, no como None
            llave=datos.get("llave"),
            cierre_automatico=datos.get("cierre_automatico"),
            costo=costo,
        )