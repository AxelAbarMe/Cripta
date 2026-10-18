import time
import uuid
 
import requests

from cripta.constantes import MAX_REINTENTOS_429
from cripta.dto.contenido_sala_respuesta_dto import ContenidoSalaRespuestaDTO
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.cripta_resumen_dto import CriptaResumenDTO
from cripta.dto.catalogo_dto import CatalogoDTO
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.version_dto import VersionCatalogoDTO, VersionCriptaDTO
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.excepciones import CriptaApiError, CriptaLimiteError
from cripta.infraestructura.lotes import validar_lote

BASE_URL = "https://cripta-api.kad06a0zhgs84.us-east-2.cs.amazonlightsail.com/v1"
TIEMPO_ESPERA_SEGUNDOS = 10

class ClienteHttp:
    def __init__(self, contador: ContadorSolicitudes, base_url: str = BASE_URL):
        self._contador = contador
        self._base_url = base_url
        self._client_id = str(uuid.uuid4())  # una sola vez por ejecucion
        self._headers = {"X-Cripta-Client-Id": self._client_id}

    @property
    def client_id(self):
        return self._client_id

    def _get(self, ruta: str, operacion: str, parametros: dict | None = None) -> dict:
        reintentos = 0
        while True:
            # El presupuesto se revisa antes de CADA intento, tambien antes de un reintento por 429 (§5.1)
            if self._contador.restantes < 1:
                raise CriptaLimiteError(self._contador.presupuesto_maximo)
            self._contador.registrar_solicitud()

            respuesta = self._enviar(ruta, operacion, parametros)

            if respuesta.status_code == 200:
                return self._leer_json(respuesta, operacion)

            if respuesta.status_code == 429:
                if reintentos >= MAX_REINTENTOS_429:
                    raise CriptaApiError(
                        operacion=operacion,
                        codigo=429,
                        mensaje=f"límite de frecuencia excedido {reintentos + 1} veces seguidas",
                    )
                reintentos += 1
                time.sleep(self._segundos_de_espera(respuesta))  # tiempo real: no toca el reloj virtual
                continue

            raise CriptaApiError(
                operacion=operacion,
                codigo=respuesta.status_code,
                mensaje=self._mensaje_de_error(respuesta),
            )

    def _enviar(self, ruta: str, operacion: str, parametros: dict | None):
        # Hace la solicitud y convierte cualquier error de red en CriptaApiError con contexto (§3.1)
        try:
            return requests.get(
                self._base_url + ruta,
                headers=self._headers,
                params=parametros,
                timeout=TIEMPO_ESPERA_SEGUNDOS,
            )
        except requests.Timeout as error:
            raise CriptaApiError(
                operacion=operacion,
                codigo=None,
                mensaje=f"el servidor no respondió en {TIEMPO_ESPERA_SEGUNDOS} s",
            ) from error
        except requests.ConnectionError as error:
            raise CriptaApiError(
                operacion=operacion,
                codigo=None,
                mensaje="no se pudo conectar con el servidor",
            ) from error
        except requests.RequestException as error:
            raise CriptaApiError(
                operacion=operacion,
                codigo=None,
                mensaje=f"error de red ({type(error).__name__})",
            ) from error

    @staticmethod
    def _segundos_de_espera(respuesta) -> int:
        # Lee "reintentar_en" del 429 (si falta o no es válido, espera 1 segundo)
        try:
            segundos = respuesta.json().get("reintentar_en", 1)
        except (ValueError, AttributeError):
            return 1
        if isinstance(segundos, int) and segundos >= 1: # revisa si segundos es int y si es mayor o igual que 1
            return segundos
        return 1
 
    @staticmethod
    def _mensaje_de_error(respuesta) -> str:
        try:
            return respuesta.json().get("error", respuesta.text)
        except ValueError:
            return respuesta.text or "(sin cuerpo de error)"

    @staticmethod
    def _leer_json(respuesta, operacion: str):
        # Un 200 cuyo cuerpo no es JSON (por ejemplo una página HTML de un proxy) no debe devolver un mensaje de error de JSON
        try:
            return respuesta.json()
        except ValueError as error:
            raise CriptaApiError(operacion=operacion, codigo=respuesta.status_code,
                                 mensaje="la respuesta no es JSON válido") from error

    @staticmethod
    def _convertir(operacion: str, conversor, datos):
        # Convierte el JSON en DTOs. Si falta un campo (KeyError), llega un tipo inesperado
        # (TypeError) o un valor inválido (ValueError), se reporta con la operación que falló.
        try:
            return conversor(datos)
        except (KeyError, TypeError, ValueError) as error:
            raise CriptaApiError(operacion=operacion, codigo=None,
                                 mensaje=f"la respuesta no tiene el formato esperado "
                                         f"({type(error).__name__}: {error})") from error

    def listar_criptas(self) -> tuple[CriptaResumenDTO, ...]:
        # GET /criptas: lista de criptas publicadas, cada una como resumen (id, nombre, salas, dificultad)
        operacion = "listar criptas"
        datos = self._get("/criptas", operacion)
        return self._convertir(operacion, CriptaResumenDTO.lista_desde_json, datos)

    def obtener_general(self, cripta_id: str) -> CriptaGeneralDTO:
        # GET /criptas/{id}: datos generales de una cripta (sala inicial y de salida, presupuesto,
        # tamaño del inventario, estadísticas iniciales del jugador, etc)
        operacion = f"datos generales de {cripta_id}"
        datos = self._get(f"/criptas/{cripta_id}", operacion)
        return self._convertir(operacion, CriptaGeneralDTO.desde_json, datos)

    def obtener_version_cripta(self, cripta_id: str) -> VersionCriptaDTO:
        # GET /criptas/{id}/version: versión actual de la cripta. Sirve para saber si lo guardado
        # en disco sigue siendo válido o hay que volver a pedirlo
        operacion = f"versión de {cripta_id}"
        datos = self._get(f"/criptas/{cripta_id}/version", operacion)
        return self._convertir(operacion, VersionCriptaDTO.desde_json, datos)

    def obtener_pagina_esqueleto(self, cripta_id: str, pagina: int) -> PaginaEsqueletoDTO:
        # GET /criptas/{id}/salas?pagina=N: una página del esqueleto (salas con sus salidas y puertas)
        # Las páginas empiezan en 1
        operacion = f"esqueleto de {cripta_id} (página {pagina})"
        datos = self._get(f"/criptas/{cripta_id}/salas", operacion, parametros={"pagina": pagina})
        return self._convertir(operacion, PaginaEsqueletoDTO.desde_json, datos)

    def obtener_contenido(self, cripta_id: str, salas: list[int]) -> ContenidoSalaRespuestaDTO:
        # GET /criptas/{id}/contenido?salas=1,2,3: enemigos, objetos y trampas de un lote de salas
        # El lote se valida antes (1 a 10 salas distintas) para no gastar una solicitud que el servidor rechazaría
        validar_lote(salas, "salas")
        parametro = ",".join(str(s) for s in salas)
        operacion = f"contenido de {cripta_id} (salas {parametro})"
        datos = self._get(f"/criptas/{cripta_id}/contenido", operacion, parametros={"salas": parametro})
        return self._convertir(operacion, ContenidoSalaRespuestaDTO.desde_json, datos)

    def obtener_catalogo(self, ids: list[str]) -> CatalogoDTO:
        # GET /catalogo?ids=a,b,c: fichas técnicas (enemigos, objetos, trampas) de un lote de ids
        # Mismo control de lote que en obtener_contenido
        validar_lote(ids, "ids de catálogo")
        parametro = ",".join(ids)
        operacion = f"catálogo (ids {parametro})"
        datos = self._get("/catalogo", operacion, parametros={"ids": parametro})
        return self._convertir(operacion, CatalogoDTO.desde_json, datos)

    def obtener_version_catalogo(self) -> VersionCatalogoDTO:
        # GET /catalogo/version: versión actual del catálogo. Si cambió, las fichas guardadas
        # en la caché de disco ya no sirven
        operacion = "versión de catálogo"
        datos = self._get("/catalogo/version", operacion)
        return self._convertir(operacion, VersionCatalogoDTO.desde_json, datos)