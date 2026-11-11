from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LlaveUbicacionDTO:
    id: str
    sala: int
    enemigo: str | None = None  # None: la llave está en el suelo de la sala

    @staticmethod
    def desde_json(datos):
        for campo in ("id", "sala"):
            if datos.get(campo) is None:
                raise ValueError(f"llave sin el campo «{campo}»: {datos!r}")
        if not isinstance(datos["id"], str) or datos["id"] == "":
            raise ValueError(f"llave con «id» vacío o no válido: {datos['id']!r}")
        sala = datos["sala"]
        if isinstance(sala, bool) or not isinstance(sala, int) or sala < 1:
            raise ValueError(f"llave «{datos['id']}» con «sala» inválida ({sala!r}): debe ser un entero >= 1")
        return LlaveUbicacionDTO(id=datos["id"], sala=sala, enemigo=datos.get("enemigo"))
