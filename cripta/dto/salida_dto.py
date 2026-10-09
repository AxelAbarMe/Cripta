from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SalidaDTO:
    sala_destino: int
    cerrada: bool
    llave: str | None
    cierre_automatico: int | None

    @staticmethod
    def desde_json(datos):
        return SalidaDTO(
            sala_destino=datos["sala"],
            cerrada=bool(datos.get("cerrada")),  # un null del JSON queda como False, no como None
            llave=datos.get("llave"),
            cierre_automatico=datos.get("cierre_automatico"),
        )