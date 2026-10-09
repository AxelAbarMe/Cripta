"""Bitácora de partida para --replay (§4.11).

Formato: una línea JSON por registro, en un archivo de solo anexado.
  - Línea 1: el encabezado, {"tipo": "encabezado", "id_cripta": ..., "version_cripta": ...,
    "version_catalogo": ..., "semilla": ...} (los cuatro campos que exige el enunciado, como mínimo).
  - Líneas siguientes: una por cada acción aceptada, exactamente como la da Accion.a_dict()
    (formato definido en docs/CONTRATO_PARTIDA.md), por ejemplo {"tipo": "mover", "direccion": "N"}.
Las líneas ya escritas nunca se reescriben. Los dict solo existen al convertir de/a JSON (§7).
"""
import json
from pathlib import Path

from cripta.excepciones import CriptaBitacoraError

CAMPOS_ENCABEZADO = ("id_cripta", "version_cripta", "version_catalogo", "semilla")


class EscritorBitacoraPartida:
    """Crea la bitácora de UNA partida: el encabezado en la primera línea y luego una línea por acción."""

    def __init__(self, ruta: str, encabezado: dict):
        faltantes = _campos_faltantes(encabezado)
        if faltantes:
            raise ValueError(f"Al encabezado de la bitácora le faltan los campos {faltantes}")
        self._ruta = Path(ruta)
        # Modo "w": cada partida empieza su propio archivo. Si la ruta ya tenía la bitácora de otra
        # partida, se reemplaza en vez de mezclar las acciones de las dos.
        with self._ruta.open("w", encoding="utf-8") as archivo:
            archivo.write(_a_linea({**encabezado, "tipo": "encabezado"}))

    def registrar_accion(self, accion: dict) -> None:
        # La línea es la acción tal cual (accion.a_dict()), sin mezclarla con otras claves.
        # Modo "a" (anexar) y se cierra enseguida: lo ya escrito nunca se toca.
        with self._ruta.open("a", encoding="utf-8") as archivo:
            archivo.write(_a_linea(accion))


class LectorBitacoraPartida:
    """Lee una bitácora para --replay y separa el encabezado de las acciones."""

    def __init__(self, ruta: str):
        self._ruta = Path(ruta)
        # True si la última línea quedó cortada (el programa se cerró mientras la escribía) y se ignoró
        self.ultima_linea_incompleta = False

    def leer(self) -> tuple[dict, tuple[dict, ...]]:
        ruta = str(self._ruta)
        if not self._ruta.is_file():
            raise CriptaBitacoraError(ruta, "el archivo no existe")
        with self._ruta.open(encoding="utf-8") as archivo:
            lineas = archivo.read().splitlines()

        self.ultima_linea_incompleta = False
        registros = []
        for numero, linea in enumerate(lineas, start=1):
            if not linea.strip():
                continue
            try:
                registros.append(json.loads(linea))
            except json.JSONDecodeError:
                if numero == len(lineas) and registros:
                    # Solo la última línea puede quedar a medio escribir: se ignora y se avisa
                    self.ultima_linea_incompleta = True
                    break
                raise CriptaBitacoraError(ruta, f"la línea {numero} no es JSON válido") from None

        if not registros:
            raise CriptaBitacoraError(ruta, "el archivo está vacío")
        encabezado = registros[0]
        if not isinstance(encabezado, dict) or encabezado.get("tipo") != "encabezado":
            raise CriptaBitacoraError(ruta, "la primera línea no es un encabezado")
        faltantes = _campos_faltantes(encabezado)
        if faltantes:
            raise CriptaBitacoraError(ruta, f"al encabezado le faltan los campos {faltantes}")
        acciones = registros[1:]
        for accion in acciones:
            if not isinstance(accion, dict) or "tipo" not in accion:
                raise CriptaBitacoraError(ruta, f"hay una acción sin 'tipo': {accion!r}")
        return encabezado, tuple(acciones)


def diferencias_de_version(encabezado: dict, version_cripta: str, version_catalogo: str) -> tuple[str, ...]:
    """Compara las versiones del log con las disponibles. Si devuelve algo, el replay no puede
    garantizar una reproducción fiel y debe reportarlo en vez de reproducir en silencio (§4.11)."""
    diferencias = []
    if encabezado["version_cripta"] != version_cripta:
        diferencias.append(f"versión de cripta: el log usa {encabezado['version_cripta']}, "
                           f"la disponible es {version_cripta}")
    if encabezado["version_catalogo"] != version_catalogo:
        diferencias.append(f"versión de catálogo: el log usa {encabezado['version_catalogo']}, "
                           f"la disponible es {version_catalogo}")
    return tuple(diferencias)


def _campos_faltantes(encabezado: dict) -> tuple[str, ...]:
    return tuple(campo for campo in CAMPOS_ENCABEZADO if campo not in encabezado)


def _a_linea(datos: dict) -> str:
    # Una sola llamada a write por línea completa, con su salto de línea al final
    return json.dumps(datos, ensure_ascii=False) + "\n"