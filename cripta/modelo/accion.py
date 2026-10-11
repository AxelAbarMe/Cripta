"""Acción del jugador (docs/CONTRATO_PARTIDA.md, sección 3).

Una Accion es inmutable: un tipo y, según el tipo, un argumento. Se convierte a dict
para escribirla en la bitácora de la partida y se reconstruye desde él (replay).
"""
from dataclasses import dataclass

from cripta.constantes import (
    COSTO_ABRIR_PUERTA,
    COSTO_ATACAR,
    COSTO_EQUIPAR_OBJETO,
    COSTO_ESPERAR,
    COSTO_MOVER,
    COSTO_RECOGER_OBJETO,
    COSTO_SOLTAR_OBJETO,
    COSTO_USAR_OBJETO,
    DIRECCIONES,
)

# (tipo, nombre del argumento o None, costo base). Son solo 9 filas fijas: se recorre la tupla.
_TIPOS = (
    ("mover", "direccion", COSTO_MOVER),
    ("abrir", "direccion", COSTO_ABRIR_PUERTA),
    ("atacar", "instancia", COSTO_ATACAR),
    ("esperar", None, COSTO_ESPERAR),
    ("recoger", "ficha_id", COSTO_RECOGER_OBJETO),
    ("usar", "indice", COSTO_USAR_OBJETO),
    ("equipar", "indice", COSTO_EQUIPAR_OBJETO),
    ("soltar", "indice", COSTO_SOLTAR_OBJETO),
    ("pergamino", None, 0),   # no consume tiempo virtual (§2.11)
)


def _buscar_tipo(tipo):
    for nombre_tipo, nombre_argumento, costo in _TIPOS:
        if nombre_tipo == tipo:
            return nombre_argumento, costo
    raise ValueError(f"Tipo de acción desconocido: {tipo!r}")


@dataclass(frozen=True, slots=True)
class Accion:
    tipo: str
    argumento: str | int | None = None

    def __post_init__(self):
        nombre_argumento, _costo = _buscar_tipo(self.tipo)
        if nombre_argumento is None:
            if self.argumento is not None:
                raise ValueError(f"La acción {self.tipo!r} no lleva argumento")
            return
        if self.argumento is None:
            raise ValueError(f"La acción {self.tipo!r} necesita el argumento {nombre_argumento!r}")
        if nombre_argumento == "direccion" and self.argumento not in DIRECCIONES:
            raise ValueError(f"Dirección inválida: {self.argumento!r}")
        if nombre_argumento == "indice":
            if isinstance(self.argumento, bool) or not isinstance(self.argumento, int) or self.argumento < 0:
                raise ValueError(f"El índice debe ser un entero mayor o igual que 0: {self.argumento!r}")

    @property
    def costo_base(self) -> int:
        return _buscar_tipo(self.tipo)[1]

    def a_dict(self) -> dict:
        datos = {"tipo": self.tipo}
        nombre_argumento = _buscar_tipo(self.tipo)[0]
        if nombre_argumento is not None:
            datos[nombre_argumento] = self.argumento
        return datos

    @staticmethod
    def desde_dict(datos) -> "Accion":
        tipo = datos.get("tipo")
        nombre_argumento = _buscar_tipo(tipo)[0]
        if nombre_argumento is None:
            return Accion(tipo)
        return Accion(tipo, datos.get(nombre_argumento))