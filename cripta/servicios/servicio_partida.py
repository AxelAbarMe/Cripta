"""ServicioPartida: arma una partida a partir de un ClienteCripta y coordina su bitácora y su reporte (§4.11, §5.1).

Es el único que conoce a la vez el cliente, la caché de disco y el modelo; el controlador y el replay
solo hablan con él. Construye mapa, catálogo y precarga, crea la Partida y escribe en la bitácora
cada acción aceptada. No conoce la vista.
"""
import random

from cripta.constantes import CACHE_TAMANO_DEFAULT
from cripta.infraestructura.partida_log import EscritorBitacoraPartida
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from cripta.servicios.servicio_presupuesto import ServicioPresupuesto


class ServicioPartida:
    def __init__(self, cliente, contador, cache_disco=None, tamano_cache: int = CACHE_TAMANO_DEFAULT,
                 asincrono: bool = True):
        # `cliente` debe ser seguro entre hilos (ClienteGeneral) y `contador` el mismo que usa el cliente
        self._cliente = cliente
        self._contador = contador
        self._cache_disco = cache_disco
        self._tamano_cache = tamano_cache
        self._asincrono = asincrono
        self._partida = None
        self._catalogo = None
        self._precarga = None
        self._bitacora = None
        self.datos_generales = None      # CriptaGeneralDTO de la partida en curso
        self.version_catalogo = None
        self.semilla = None

    @property
    def partida(self) -> Partida:
        """Para consultas (vista, mensajes, inventario). Las acciones se ejecutan SIEMPRE con ejecutar()."""
        if self._partida is None:
            raise RuntimeError("No hay una partida en curso: llama a iniciar_nueva() primero.")
        return self._partida

    def listar_criptas(self):
        return self._cliente.listar_criptas()

    # -------------------------------------------------------------- crear
    def iniciar_nueva(self, cripta_id: str, semilla: int | None = None, ruta_bitacora: str | None = None) -> None:
        """Descarga lo básico de la cripta, arma el modelo y deja a la partida lista para la primera acción.
        Sin `ruta_bitacora` no se escribe bitácora (replay y bench)."""
        self.cerrar()
        general = self._cliente.obtener_general(cripta_id)
        self._contador.fijar_presupuesto_maximo(general.presupuesto_solicitudes)
        # La versión del catálogo no viene con la cripta: una sola solicitud, y se pasa ya conocida al catálogo
        version_catalogo = self._cliente.obtener_version_catalogo().version
        if semilla is None:
            semilla = random.SystemRandom().randrange(2 ** 32)   # la semilla queda en la bitácora y en el guardado

        mapa = CriptaMapa()
        self._catalogo = ServicioCatalogo(
            self._cliente, self._tamano_cache, self._cache_disco,
            fichas_en_uso=self._fichas_en_uso, version_catalogo=version_catalogo,
        )
        self._precarga = ServicioPrecarga(
            self._cliente, cripta_id, mapa, servicio_catalogo=self._catalogo, cache_disco=self._cache_disco,
            version_cripta=general.version, asincrono=self._asincrono,
        )
        try:
            self._precarga.cargar_esqueleto(general.paginas)
            self._partida = Partida(general, mapa, self._catalogo, self._precarga, semilla)
            self._partida.iniciar()
        except BaseException:
            self.cerrar()
            raise
        self.datos_generales, self.version_catalogo, self.semilla = general, version_catalogo, semilla
        if ruta_bitacora is not None:
            self._bitacora = EscritorBitacoraPartida(ruta_bitacora, {
                "id_cripta": general.id, "version_cripta": general.version,
                "version_catalogo": version_catalogo, "semilla": semilla,
            })

    def _fichas_en_uso(self) -> tuple[str, ...]:
        # El catálogo se crea antes que la partida y se lo pregunta a ella al desalojar (§4.4)
        return self._partida.fichas_en_uso() if self._partida is not None else ()

    # ------------------------------------------------------------ jugar
    def ejecutar(self, accion):
        """Ejecuta la acción y, si el modelo la acepta, la anota en la bitácora (también el pergamino:
        cambia el estado y el replay tiene que repetirlo). Las rechazadas no cambian nada y no se anotan.
        Si falla la infraestructura (CriptaApiError, CriptaLimiteError...) la partida queda como estaba."""
        resultado = self.partida.ejecutar_accion(accion)
        if resultado.aceptada and self._bitacora is not None:
            self._bitacora.registrar_accion(accion.a_dict())
        return resultado

    # ----------------------------------------------------------- reporte
    def reporte_final(self) -> str:
        """Lo que pide §5.1 al terminar: solicitudes, presupuesto, aciertos y fallos de caché."""
        lineas = [ServicioPresupuesto(self._contador).reporte_final()]
        if self._catalogo is not None:          # si el arranque falló antes de armarlos, solo se reporta el presupuesto
            lineas.append(self._catalogo.estadisticas.reporte())
        if self._precarga is not None:
            lineas.append(self._precarga.reporte())
        return "\n".join(lineas)

    def cerrar(self) -> None:
        """Detiene el hilo de precarga sin gastar más solicitudes. Se puede llamar varias veces."""
        if self._precarga is not None:
            self._precarga.cerrar()
        self._partida = None
        self._bitacora = None