from dataclasses import dataclass

from cripta.dto.salida_dto import SalidaDTO

@dataclass(frozen=True, slots=True)
class SalaDTO:
    id: int
    nombre: str
    norte: SalidaDTO | None
    sur: SalidaDTO | None
    este: SalidaDTO | None
    oeste: SalidaDTO | None

    def salida(self, direccion):
        # Permite pedir la salida por letra: sala.salida("N")
        if direccion == "N":
            return self.norte
        if direccion == "S":
            return self.sur
        if direccion == "E":
            return self.este
        if direccion == "O":
            return self.oeste
        raise ValueError(f"Dirección inválida: {direccion}")

    @staticmethod
    def desde_json(datos):
        salidas = datos.get("salidas", {})
        return SalaDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            norte=_leer_salida(datos["id"], salidas, "N"),
            sur=_leer_salida(datos["id"], salidas, "S"),
            este=_leer_salida(datos["id"], salidas, "E"),
            oeste=_leer_salida(datos["id"], salidas, "O"),
        )


def _leer_salida(sala_id, salidas, direccion):
    # Si esa dirección no viene en el JSON, la sala no tiene salida por ahí
    if direccion not in salidas:
        return None
    try:
        return SalidaDTO.desde_json(salidas[direccion])
    except ValueError as error:
        raise ValueError(f"sala {sala_id}, dirección {direccion}: {error}") from error