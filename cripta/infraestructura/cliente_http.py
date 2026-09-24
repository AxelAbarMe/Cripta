import time
import uuid
 
import requests
 
from cripta.dto.contenido_salas_respuesta_dto import ContenidoSalaRespuestaDTO
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.cripta_resumen_dto import CriptaResumenDTO
from cripta.dto.catalogo_dto import CatalogoDTO
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.version_dto import VersionCatalogoDTO, VersionCriptaDTO
from cripta.excepciones import CriptaApiError
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes

BASE_URL = "https://cripta-api.kad06a0zhgs84.us-east-2.cs.amazonlightsail.com/v1"
TIEMPO_ESPERA_SEGUNDOS = 10 
MAX_IDS_POR_LOTE = 10

class ClienteHttp:
    def __init__(self, contador: ContadorSolicitudes, base_url: str = BASE_URL):
        self._contador = contador
        self._base_url = base_url
        self._client_id = str(uuid.uuid4())  # una sola vez por ejecución
        self._headers = {"X-Cripta-Client-Id": self._client_id}

    @property
    def client_id(self):
        return self._client_id

    def _get(self, ruta: str, operacion: str, parametros: dict | None = None) -> dict:
        while True:
            self._contador.registrar_solicitud()
            respuesta = requests.get(
                self._base_url + ruta,
                headers=self._headers,
                params=parametros,
                timeout=TIEMPO_ESPERA_SEGUNDOS,
            )
 
            if respuesta.status_code == 200:
                return respuesta.json()
 
            if respuesta.status_code == 429:
                cuerpo = respuesta.json()
                reintentar_en = cuerpo.get("reintentar_en", 1)
                time.sleep(reintentar_en)  # tiempo real
                continue
 
            raise CriptaApiError(
                operacion=operacion,
                codigo=respuesta.status_code,
                mensaje=self._mensaje_de_error(respuesta),
            )
 
    @staticmethod
    def _mensaje_de_error(respuesta) -> str:
        try:
            return respuesta.json().get("error", respuesta.text)
        except ValueError:
            return respuesta.text or "(sin cuerpo de error)"
 

    def listar_criptas(self) -> tuple[CriptaResumenDTO, ...]:
        datos = self._get("/criptas", "listar criptas")
        return tuple(CriptaResumenDTO.desde_json(c) for c in datos["criptas"])
 
    def obtener_general(self, cripta_id: str) -> CriptaGeneralDTO:
        datos = self._get(f"/criptas/{cripta_id}", f"datos generales de {cripta_id}")
        return CriptaGeneralDTO.desde_json(datos)
 
    def obtener_version_cripta(self, cripta_id: str) -> VersionCriptaDTO:
        datos = self._get(f"/criptas/{cripta_id}/version", f"versión de {cripta_id}")
        return VersionCriptaDTO.desde_json(datos)
 
    def obtener_pagina_esqueleto(self, cripta_id: str, pagina: int) -> PaginaEsqueletoDTO:
        datos = self._get(
            f"/criptas/{cripta_id}/salas",
            f"esqueleto de {cripta_id} (página {pagina})",
            parametros={"pagina": pagina},
        )
        return PaginaEsqueletoDTO.desde_json(datos)
 
    def obtener_contenido(self, cripta_id: str, salas: list[int]) -> ContenidoSalaRespuestaDTO:
        self._validar_lote(salas, "salas")
        parametro = ",".join(str(s) for s in salas)
        datos = self._get(
            f"/criptas/{cripta_id}/contenido",
            f"contenido de {cripta_id} (salas {parametro})",
            parametros={"salas": parametro},
        )
        return ContenidoSalaRespuestaDTO.desde_json(datos)
 
    def obtener_catalogo(self, ids: list[str]) -> CatalogoDTO:
        self._validar_lote(ids, "ids de catálogo")
        parametro = ",".join(ids)
        datos = self._get(
            "/catalogo",
            f"catálogo (ids {parametro})",
            parametros={"ids": parametro},
        )
        return CatalogoDTO.desde_json(datos)
 
    def obtener_version_catalogo(self) -> VersionCatalogoDTO:
        datos = self._get("/catalogo/version", "versión de catálogo")
        return VersionCatalogoDTO.desde_json(datos)

    @staticmethod
    def _validar_lote(elementos: list, nombre_campo: str) -> None:
        # Lotes repetidos o vacios son rechazados antes de la llamada de red, para no desperdiciar solicitudes.
        if not elementos:
            raise ValueError(f"El lote de {nombre_campo} no puede estar vacío.")
        if len(elementos) > MAX_IDS_POR_LOTE:
            raise ValueError(
                f"El lote de {nombre_campo} admite hasta {MAX_IDS_POR_LOTE} "
                f"elementos, se recibieron {len(elementos)}."
            )
        if ClienteHttp._tiene_repetidos(elementos):
            raise ValueError(f"El lote de {nombre_campo} tiene elementos repetidos.")
 
    @staticmethod
    def _tiene_repetidos(elementos: list) -> bool:
        # Chequeo manual de repetidos para no depender de set() y mantener el orden de los elementos.
        for i in range(len(elementos)):
            for j in range(i + 1, len(elementos)):
                if elementos[i] == elementos[j]:
                    return True
        return False