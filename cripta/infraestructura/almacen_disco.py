"""AlmacenDiscoArchivos: implementa AlmacenDiscoPuerto guardando cada clave como un
archivo dentro de un directorio. Es la única pieza que toca el sistema de archivos
para la caché persistente (§4.4); el resto del programa habla con el puerto."""
import os
from pathlib import Path


class AlmacenDiscoArchivos:
    def __init__(self, directorio):
        self._directorio = Path(directorio)
        self._directorio.mkdir(parents=True, exist_ok=True)

    def _ruta(self, clave: str) -> Path:
        # Solo letras, dígitos y "-_." : evita que una clave (que puede venir de
        # ids del servidor) escape del directorio con "/" o "..".
        nombre = "".join(c if (c.isalnum() or c in "-_.") else "_" for c in clave)
        return self._directorio / nombre

    def leer(self, clave: str) -> bytes | None:
        try:
            return self._ruta(clave).read_bytes()
        except FileNotFoundError:
            return None

    def escribir(self, clave: str, datos: bytes) -> None:
        # Se escribe a un temporal y se renombra: si el programa se cierra a la
        # mitad, nunca queda un archivo a medio escribir con el nombre final.
        destino = self._ruta(clave)
        temporal = destino.with_name(destino.name + ".tmp")
        temporal.write_bytes(datos)
        os.replace(temporal, destino)

    def existe(self, clave: str) -> bool:
        return self._ruta(clave).is_file()