"""Cliente offline: implementa el mismo contrato que ClienteHttp,
 pero lee desde disco en vez de hacer peticiones HTTP (--offline).
 El modelo y los servicios no distinguen cuál de los dos reciben: 
 ambos exponen los mismos métodos y devuelven los mismos DTOs.

Convención de archivos usada aquí (PROVISIONAL):

    <raiz>/criptas.json                     misma forma que GET /criptas
    <raiz>/<cripta_id>/general.json         misma forma que GET /criptas/<id>
    <raiz>/<cripta_id>/version.json         misma forma que GET /criptas/<id>/version
    <raiz>/<cripta_id>/salas/pagina_N.json  misma forma que GET /criptas/<id>/salas?pagina=N
    <raiz>/<cripta_id>/contenido/S.json     una entrada RoomContentEntry para la sala S
    <raiz>/catalogo/version.json            misma forma que GET /catalogo/version
    <raiz>/catalogo/ID.json                 una ficha "desempaquetada", forma de GET /catalogo/<id>

Se lee un archivo por sala/id de catálogo (en vez de un archivo por lote exacto) para no
depender de qué combinación de ids pida cada partida; así cualquier subconjunto de hasta
10 elementos se arma leyendo varios archivos pequeños.

Ninguno de estos métodos cuenta como solicitud de red: por eso esta clase no recibe un ContadorSolicitudes.
"""
import json
from pathlib import Path

from cripta.dto.catalogo_dto import CatalogoDTO
from cripta.dto.contenido_sala_dto import ContenidoSalaDTO
from cripta.dto.contenido_salas_respuesta_dto import ContenidoSalaRespuestaDTO
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.cripta_resumen_dto import CriptaResumenDTO
from cripta.dto.entidad_dto import entidad_desde_json
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.version_dto import VersionCatalogoDTO, VersionCriptaDTO
from cripta.excepciones import CriptaDatosNoEncontradosError


class ClienteOffline:
    """Misma interfaz pública que ClienteHttp, leyendo de `raiz_fixtures` en vez de la red."""

    def __init__(self, raiz_fixtures: str):
        self._raiz = Path(raiz_fixtures)

    def listar_criptas(self) -> tuple[CriptaResumenDTO, ...]:
        datos = self._leer(self._raiz / "criptas.json", "listar criptas")
        return tuple(CriptaResumenDTO.desde_json(c) for c in datos["criptas"])

    def obtener_general(self, cripta_id: str) -> CriptaGeneralDTO:
        datos = self._leer(self._raiz / cripta_id / "general.json", f"datos generales de {cripta_id}")
        return CriptaGeneralDTO.desde_json(datos)

    def obtener_version_cripta(self, cripta_id: str) -> VersionCriptaDTO:
        datos = self._leer(self._raiz / cripta_id / "version.json", f"versión de {cripta_id}")
        return VersionCriptaDTO.desde_json(datos)

    def obtener_pagina_esqueleto(self, cripta_id: str, pagina: int) -> PaginaEsqueletoDTO:
        ruta = self._raiz / cripta_id / "salas" / f"pagina_{pagina}.json"
        datos = self._leer(ruta, f"esqueleto de {cripta_id} (página {pagina})")
        return PaginaEsqueletoDTO.desde_json(datos)

    def obtener_contenido(self, cripta_id: str, salas: list[int]) -> ContenidoSalaRespuestaDTO:
        # Un archivo por sala; se ensambla el mismo sobre "contenido" que devolvería el lote real
        entradas = []
        for sala_id in salas:
            ruta = self._raiz / cripta_id / "contenido" / f"{sala_id}.json"
            datos = self._leer(ruta, f"contenido de la sala {sala_id} de {cripta_id}")
            entradas.append(ContenidoSalaDTO.desde_json(datos))
        return ContenidoSalaRespuestaDTO(salas=tuple(entradas))

    def obtener_catalogo(self, ids: list[str]) -> CatalogoDTO:
        # Un archivo por id de catálogo, con la forma "desempaquetada" (como /catalogo/<id>)
        entidades = []
        for catalog_id in ids:
            ruta = self._raiz / "catalogo" / f"{catalog_id}.json"
            datos = self._leer(ruta, f"ficha de catálogo {catalog_id}")
            entidades.append(entidad_desde_json(datos))
        return CatalogoDTO(entidades=tuple(entidades))

    def obtener_version_catalogo(self) -> VersionCatalogoDTO:
        datos = self._leer(self._raiz / "catalogo" / "version.json", "versión de catálogo")
        return VersionCatalogoDTO.desde_json(datos)

    @staticmethod
    def _leer(ruta: Path, operacion: str) -> dict:
        if not ruta.is_file():
            raise CriptaDatosNoEncontradosError(operacion=operacion, ruta=str(ruta))
        with ruta.open(encoding="utf-8") as archivo:
            return json.load(archivo)
