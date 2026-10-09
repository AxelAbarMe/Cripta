"""CacheDisco: persistencia versionada de fichas de catálogo, esqueleto y contenido
de criptas (§4.4). Sobrevive al cierre del programa.

Cómo se valida por versión sin descargar nada: la versión va DENTRO de la clave
("catalogo.<version>.<id>", "cripta.<id>.<version>.contenido.<sala>"). Si la
versión del servidor cambió, la clave nueva simplemente no existe y se trata como
"nunca se persistió" (fallo -> solicitud de red); los archivos de la versión vieja
quedan huérfanos sin molestar. Así no hace falta ningún proceso de invalidación
que recorra el disco.

Tolerante a archivos dañados: un JSON ilegible o incompleto se trata como fallo
de caché (se volverá a pedir), nunca como excepción que tumbe la partida.
"""
from cripta.dto.contenido_sala_dto import ContenidoSalaDTO
from cripta.dto.entidad_dto import entidad_desde_json
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.infraestructura.serializacion import (
    a_bytes, contenido_sala_a_json, desde_bytes, ficha_a_json, pagina_esqueleto_a_json,
)


class CacheDisco:
    def __init__(self, almacen):
        self._almacen = almacen  # cualquier AlmacenDiscoPuerto

    # ---- catálogo (versión global) ----
    @staticmethod
    def _clave_ficha(version_catalogo: str, ficha_id: str) -> str:
        return f"catalogo.{version_catalogo}.{ficha_id}.json"

    def existe_ficha(self, version_catalogo: str, ficha_id: str) -> bool:
        # Se lee el archivo en vez de solo ver si existe: un archivo dañado debe contar como
        # "no está", para que la ficha viaje en el próximo lote de red y no en una solicitud aparte.
        return self.leer_ficha(version_catalogo, ficha_id) is not None

    def leer_ficha(self, version_catalogo: str, ficha_id: str):
        return self._leer(self._clave_ficha(version_catalogo, ficha_id), entidad_desde_json)

    def guardar_ficha(self, version_catalogo: str, ficha) -> None:
        self._almacen.escribir(self._clave_ficha(version_catalogo, ficha.id), a_bytes(ficha_a_json(ficha)))

    # ---- esqueleto (versión de la cripta) ----
    @staticmethod
    def _clave_pagina(cripta_id: str, version: str, pagina: int) -> str:
        return f"cripta.{cripta_id}.{version}.salas.{pagina}.json"

    def leer_pagina(self, cripta_id: str, version: str, pagina: int):
        return self._leer(self._clave_pagina(cripta_id, version, pagina), PaginaEsqueletoDTO.desde_json)

    def guardar_pagina(self, cripta_id: str, version: str, pagina_dto) -> None:
        self._almacen.escribir(
            self._clave_pagina(cripta_id, version, pagina_dto.pagina),
            a_bytes(pagina_esqueleto_a_json(pagina_dto)),
        )

    # ---- contenido (versión de la cripta), una entrada por sala ----
    @staticmethod
    def _clave_contenido(cripta_id: str, version: str, sala_id: int) -> str:
        return f"cripta.{cripta_id}.{version}.contenido.{sala_id}.json"

    def existe_contenido(self, cripta_id: str, version: str, sala_id: int) -> bool:
        # Mismo criterio que existe_ficha: un archivo dañado cuenta como que no existe
        return self.leer_contenido_sala(cripta_id, version, sala_id) is not None

    def leer_contenido_sala(self, cripta_id: str, version: str, sala_id: int):
        return self._leer(self._clave_contenido(cripta_id, version, sala_id), ContenidoSalaDTO.desde_json)

    def guardar_contenido_sala(self, cripta_id: str, version: str, contenido_dto) -> None:
        self._almacen.escribir(
            self._clave_contenido(cripta_id, version, contenido_dto.id),
            a_bytes(contenido_sala_a_json(contenido_dto)),
        )

    def _leer(self, clave: str, construir):
        crudo = self._almacen.leer(clave)
        if crudo is None:
            return None
        try:
            return construir(desde_bytes(crudo))
        except (ValueError, KeyError, TypeError):
            return None  # archivo dañado: se trata como si no existiera