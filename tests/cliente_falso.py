"""Cliente en memoria para pruebas: mismo contrato que ClienteCripta, cuenta cada
solicitud y permite simular latencia y versiones. No toca red ni disco."""
import time

from cripta.dto.catalogo_dto import CatalogoDTO
from cripta.dto.contenido_salas_respuesta_dto import ContenidoSalaRespuestaDTO
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.cripta_resumen_dto import CriptaResumenDTO
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO
from cripta.dto.version_dto import VersionCatalogoDTO, VersionCriptaDTO
from cripta.infraestructura.lotes import validar_lote


class ClienteFalso:
    def __init__(self, fichas_json=(), contenido_json=(), paginas_json=(), general_json=None,
                 version_catalogo="cat-1", version_cripta="v1", latencia=0.0, latencias_por_llamada=None):
        self.fichas_json = list(fichas_json)
        self.contenido_json = list(contenido_json)
        self.paginas_json = list(paginas_json)
        self.general_json = general_json
        self.version_catalogo = version_catalogo
        self.version_cripta = version_cripta
        self.latencia = latencia
        self.latencias_por_llamada = latencias_por_llamada  # lista consumida en orden (para probar determinismo)
        self.llamadas = []  # (metodo, argumentos)

    def _registrar(self, metodo, arg=None):
        self.llamadas.append((metodo, arg))
        espera = self.latencia
        if self.latencias_por_llamada:
            espera = self.latencias_por_llamada[(len(self.llamadas) - 1) % len(self.latencias_por_llamada)]
        if espera:
            time.sleep(espera)

    def contar(self, metodo):
        return sum(1 for m, _ in self.llamadas if m == metodo)

    def listar_criptas(self):
        self._registrar("listar_criptas")
        # salas = total de salas de todas las páginas (no la cantidad de páginas)
        total_salas = sum(len(p["salas"]) for p in self.paginas_json)
        return (CriptaResumenDTO(id="c1", nombre="Prueba", salas=total_salas, dificultad=1),)

    def obtener_general(self, cripta_id):
        self._registrar("obtener_general", cripta_id)
        return CriptaGeneralDTO.desde_json(self.general_json)

    def obtener_version_cripta(self, cripta_id):
        self._registrar("obtener_version_cripta", cripta_id)
        return VersionCriptaDTO(id=cripta_id, version=self.version_cripta)

    def obtener_pagina_esqueleto(self, cripta_id, pagina):
        self._registrar("obtener_pagina_esqueleto", pagina)
        return PaginaEsqueletoDTO.desde_json(self.paginas_json[pagina - 1])

    def obtener_contenido(self, cripta_id, salas):
        # Mismas reglas de lote que los clientes reales: un lote inválido no cuenta como llamada
        validar_lote(salas, "salas")
        self._registrar("obtener_contenido", tuple(salas))
        elegidos = [c for c in self.contenido_json if c["sala"] in salas]
        return ContenidoSalaRespuestaDTO.desde_json({"contenido": elegidos})

    def obtener_catalogo(self, ids):
        validar_lote(ids, "ids de catálogo")
        self._registrar("obtener_catalogo", tuple(ids))
        return CatalogoDTO.desde_json({"entidades": [f for f in self.fichas_json if f["id"] in ids]})

    def obtener_version_catalogo(self):
        self._registrar("obtener_version_catalogo")
        return VersionCatalogoDTO(version=self.version_catalogo)