"""ServicioResolubilidad: coordina obtencion de datos y verificacion causal.
Obtiene general, esqueleto paginado y llaves respetando presupuesto y cache.
Construye CriptaMapa e invoca VerificadorResolubilidad.
"""
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.resolubilidad import ResultadoResolubilidad, VerificadorResolubilidad


class ServicioResolubilidad:
    """Coordina la obtencion de datos, gestion de cache, presupuesto y verificacion."""

    def __init__(self, cliente, contador, cache_disco=None):
        self._cliente = cliente
        self._contador = contador
        self._cache_disco = cache_disco

    def verificar(self, id_cripta: str, general=None, mapa=None) -> ResultadoResolubilidad:
        """Descarga o lee esqueleto y llaves, arma el mapa y retorna el diagnostico.
        Si vienen general y mapa ya armados, no los vuelve a pedir."""
        if general is None:
            general = self._cliente.obtener_general(id_cripta)
            if self._contador is not None:
                self._contador.fijar_presupuesto_maximo(general.presupuesto_solicitudes)

        if mapa is None:
            mapa = CriptaMapa()
            for pagina in range(1, general.paginas + 1):
                dto = None
                if self._cache_disco is not None:
                    dto = self._cache_disco.leer_pagina(id_cripta, general.version, pagina)
                if dto is None:
                    dto = self._cliente.obtener_pagina_esqueleto(id_cripta, pagina)
                    if self._cache_disco is not None:
                        self._cache_disco.guardar_pagina(id_cripta, general.version, dto)
                mapa.agregar_pagina(dto)

            mapa.sincronizar_puertas()

        llaves = None
        if self._cache_disco is not None:
            llaves = self._cache_disco.leer_llaves(id_cripta, general.version)
        if llaves is None:
            llaves = self._cliente.obtener_llaves(id_cripta)
            if self._cache_disco is not None:
                self._cache_disco.guardar_llaves(id_cripta, general.version, llaves)

        ubicaciones = tuple(llaves) if llaves else ()
        verificador = VerificadorResolubilidad(
            mapa=mapa,
            sala_inicial=general.sala_inicial,
            sala_salida=general.sala_salida,
            llave_salida=general.llave_salida,
            llaves_ubicaciones=ubicaciones,
        )
        return verificador.verificar()
