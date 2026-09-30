from typing import Protocol, runtime_checkable

from cripta.dto.cripta_resumen_dto import CriptaResumenDTO
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.version_dto import VersionCriptaDTO
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.contenido_salas_respuesta_dto import ContenidoSalaRespuestaDTO
from cripta.dto.catalogo_dto import CatalogoDTO
from cripta.dto.version_dto import VersionCatalogoDTO

@runtime_checkable
class ClienteCripta(Protocol):

    def listar_criptas(self) -> tuple[CriptaResumenDTO, ...]:
        """GET /criptas"""
        ...
 
    def obtener_general(self, cripta_id: str) -> CriptaGeneralDTO:
        """GET /criptas/{cripta_id}"""
        ...
 
    def obtener_version_cripta(self, cripta_id: str) -> VersionCriptaDTO:
        """GET /criptas/{cripta_id}/version"""
        ...
 
    def obtener_pagina_esqueleto(self, cripta_id: str, pagina: int) -> PaginaEsqueletoDTO:
        """GET /criptas/{cripta_id}/salas?pagina=n"""
        ...
 
    def obtener_contenido(self, cripta_id: str, salas: list[int]) -> ContenidoSalaRespuestaDTO:
        """GET /criptas/{cripta_id}/contenido?salas=... (hasta 10 ids)"""
        ...
 
    def obtener_catalogo(self, ids: list[str]) -> CatalogoDTO:
        """GET /catalogo?ids=... (hasta 10 ids)"""
        ...
 
    def obtener_version_catalogo(self) -> VersionCatalogoDTO:
        """GET /catalogo/version"""
        ...

@runtime_checkable
class AlmacenDiscoPuerto(Protocol):
 
    def leer(self, clave: str) -> bytes | None:
        """Devuelve los bytes guardados bajo `clave`, o None si no existen."""
        ...
 
    def escribir(self, clave: str, datos: bytes) -> None:
        """Guarda `datos` bajo `clave`, sobrescribiendo si ya existía."""
        ...
 
    def existe(self, clave: str) -> bool:
        """True si hay algo guardado bajo `clave`, sin leer su contenido."""
        ...