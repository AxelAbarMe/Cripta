"""Cliente offline: implementa el mismo contrato que ClienteHttp,
 pero lee desde disco en vez de hacer peticiones HTTP (--offline).
 El modelo y los servicios no distinguen cuál de los dos reciben: 
 ambos exponen los mismos métodos y devuelven los mismos DTOs.

Convención de archivos (confirmada con el API real; detalle en docs/FORMATO_OFFLINE.md):

    <raiz>/criptas.json                     misma forma que GET /criptas
    <raiz>/<cripta_id>/general.json         misma forma que GET /criptas/<id>
    <raiz>/<cripta_id>/version.json         misma forma que GET /criptas/<id>/version
    <raiz>/<cripta_id>/salas/pagina_N.json  misma forma que GET /criptas/<id>/salas?pagina=N
    <raiz>/<cripta_id>/contenido/S.json     un elemento de la lista "contenido" del lote, para la sala S
    <raiz>/catalogo/version.json            misma forma que GET /catalogo/version
    <raiz>/catalogo/ID.json                 una sola ficha, igual a la respuesta de GET /catalogo/<id>

Se lee un archivo por sala/id de catálogo (en vez de un archivo por lote exacto) para no
depender de qué combinación de ids pida cada partida; así cualquier subconjunto de hasta
10 elementos se arma leyendo varios archivos pequeños.

Ninguno de estos métodos cuenta como solicitud de red: por eso esta clase no recibe un ContadorSolicitudes.
"""
import json
from pathlib import Path

from cripta.dto.catalogo_dto import CatalogoDTO
from cripta.dto.contenido_sala_dto import ContenidoSalaDTO
from cripta.dto.contenido_sala_respuesta_dto import ContenidoSalaRespuestaDTO
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.cripta_resumen_dto import CriptaResumenDTO
from cripta.dto.entidad_dto import entidad_desde_json
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.version_dto import VersionCatalogoDTO, VersionCriptaDTO
from cripta.excepciones import CriptaDatosInvalidosError, CriptaDatosNoEncontradosError
from cripta.infraestructura.lotes import validar_lote


class ClienteOffline:
    """Misma interfaz pública que ClienteHttp, leyendo de `raiz_fixtures` en vez de la red."""

    def __init__(self, raiz_fixtures: str):
        # raiz_fixtures: carpeta donde están los archivos JSON que reemplazan al API
        self._raiz = Path(raiz_fixtures)

    def listar_criptas(self) -> tuple[CriptaResumenDTO, ...]:
        # Lee criptas.json: lista de criptas disponibles (como GET /criptas)
        return self._leer(self._raiz / "criptas.json", "listar criptas", CriptaResumenDTO.lista_desde_json)

    def obtener_general(self, cripta_id: str) -> CriptaGeneralDTO:
        # Lee <cripta>/general.json: datos generales de la cripta (como GET /criptas/{id})
        return self._leer(self._raiz / cripta_id / "general.json",
                          f"datos generales de {cripta_id}", CriptaGeneralDTO.desde_json)

    def obtener_version_cripta(self, cripta_id: str) -> VersionCriptaDTO:
        # Lee <cripta>/version.json: versión de la cripta (como GET /criptas/{id}/version)
        return self._leer(self._raiz / cripta_id / "version.json",
                          f"versión de {cripta_id}", VersionCriptaDTO.desde_json)

    def obtener_pagina_esqueleto(self, cripta_id: str, pagina: int) -> PaginaEsqueletoDTO:
        # Lee <cripta>/salas/pagina_N.json: una página del esqueleto (como GET /criptas/{id}/salas?pagina=N)
        return self._leer(self._raiz / cripta_id / "salas" / f"pagina_{pagina}.json",
                          f"esqueleto de {cripta_id} (página {pagina})", PaginaEsqueletoDTO.desde_json)

    def obtener_contenido(self, cripta_id: str, salas: list[int]) -> ContenidoSalaRespuestaDTO:
        # El API devuelve todas las salas del lote en una sola respuesta. Aquí hay un archivo por sala
        # (contenido/<sala>.json), así que se lee cada uno y se juntan en el mismo DTO que daría el API
        validar_lote(salas, "salas")
        entradas = []
        for sala_id in salas:
            ruta = self._raiz / cripta_id / "contenido" / f"{sala_id}.json"
            entradas.append(self._leer(ruta, f"contenido de la sala {sala_id} de {cripta_id}",
                                       ContenidoSalaDTO.desde_json))
        return ContenidoSalaRespuestaDTO(salas=tuple(entradas))

    def obtener_catalogo(self, ids: list[str]) -> CatalogoDTO:
        # Un archivo por id (catalogo/<id>.json). Cada archivo trae una sola ficha, sin la lista
        # {"entidades": [...]} de la respuesta por lote, es la forma en que responde GET /catalogo/{id}
        validar_lote(ids, "ids de catálogo")
        entidades = []
        for catalog_id in ids:
            ruta = self._raiz / "catalogo" / f"{catalog_id}.json"
            entidades.append(self._leer(ruta, f"ficha de catálogo {catalog_id}", entidad_desde_json))
        return CatalogoDTO(entidades=tuple(entidades))

    def obtener_version_catalogo(self) -> VersionCatalogoDTO:
        # Lee catalogo/version.json: versión del catálogo (como GET /catalogo/version)
        return self._leer(self._raiz / "catalogo" / "version.json",
                          "versión de catálogo", VersionCatalogoDTO.desde_json)

    @staticmethod
    def _leer(ruta: Path, operacion: str, conversor):
        # Lee el archivo y lo convierte en DTO. Tres fallas posibles, cada una con su error claro:
        # el archivo no existe, no es JSON, o es JSON pero no tiene la forma esperada
        if not ruta.is_file():
            raise CriptaDatosNoEncontradosError(operacion=operacion, ruta=str(ruta))
        with ruta.open(encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
            except json.JSONDecodeError as error:
                raise CriptaDatosInvalidosError(operacion, str(ruta),
                                                f"no es JSON válido (línea {error.lineno})") from error
        try:
            return conversor(datos)
        except (KeyError, TypeError, ValueError) as error:
            raise CriptaDatosInvalidosError(operacion, str(ruta),
                                            f"no tiene el formato esperado "
                                            f"({type(error).__name__}: {error})") from error