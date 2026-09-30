"""Bitácora de partida para --replay

Formato: una línea JSON por registro. La primera línea es siempre el encabezado
(id de cripta, versión de cripta, versión de catálogo y semilla, como mínimo);
las siguientes son, en orden, las acciones del jugador. Nunca se reescriben líneas
ya escritas, solo se agregan nuevas.
"""
import json
from pathlib import Path


class EscritorBitacoraPartida:
    """Escribe el encabezado una sola vez y, luego, una línea por cada acción del jugador."""

    def __init__(self, ruta: str, encabezado: dict):
        self._ruta = Path(ruta)
        if not self._ruta.exists():
            with self._ruta.open("w", encoding="utf-8") as archivo:
                archivo.write(json.dumps({"tipo": "encabezado", **encabezado}, ensure_ascii=False) + "\n")

    def registrar_accion(self, accion: dict) -> None:
        # Abre y cierra de inmediato: una caída a mitad de partida no deja el archivo a medio escribir ni corrompe lo ya registrado.
        with self._ruta.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps({"tipo": "accion", **accion}, ensure_ascii=False) + "\n")


class LectorBitacoraPartida:
    """Lee un archivo de bitácora para --replay, separando el encabezado de las acciones."""

    def __init__(self, ruta: str):
        self._ruta = Path(ruta)

    def leer(self) -> tuple[dict, tuple[dict, ...]]:
        with self._ruta.open(encoding="utf-8") as archivo:
            lineas = [json.loads(linea) for linea in archivo if linea.strip()]
        if not lineas or lineas[0].get("tipo") != "encabezado":
            raise ValueError(f"«{self._ruta}» no tiene un encabezado válido de bitácora de partida.")
        encabezado = lineas[0]
        acciones = tuple(linea for linea in lineas[1:] if linea.get("tipo") == "accion")
        return encabezado, acciones
