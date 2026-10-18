"""ServicioPartida: arma una partida a partir de un ClienteCripta y coordina su bitácora y su reporte (§4.11, §5.1).

Es el único que conoce a la vez el cliente, la caché de disco y el modelo; el controlador y el replay
solo hablan con él. Construye mapa, catálogo y precarga, crea la Partida y escribe en la bitácora
cada acción aceptada. No conoce la vista.
"""
import random
import shutil
from pathlib import Path

from cripta.constantes import CACHE_TAMANO_DEFAULT
from cripta.excepciones import CriptaBitacoraError, CriptaFormatoIncompatibleError
from cripta.infraestructura.guardado_binario import GuardadoBinario
from cripta.infraestructura.partida_log import CAMPOS_ENCABEZADO, EscritorBitacoraPartida, LectorBitacoraPartida
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.partida import Partida
from cripta.modelo.puntajes import Puntaje
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from cripta.servicios.servicio_presupuesto import ServicioPresupuesto


class ServicioPartida:
    def __init__(self, cliente, contador, cache_disco=None, tamano_cache: int = CACHE_TAMANO_DEFAULT,
                 asincrono: bool = True, repositorio_puntajes=None):
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
        self._repositorio_puntajes = repositorio_puntajes     # RepositorioPuntajes o None (sin tabla de puntajes)
        self._ruta_bitacora = None
        self._puntaje_registrado = False
        self.bitacora_completa = True    # False si se cargó un guardado cuya bitácora no estaba: no es reproducible

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
        self._contador.reiniciar()
        general, version_catalogo = self._datos_basicos(cripta_id)
        if semilla is None:
            semilla = random.SystemRandom().randrange(2 ** 32)   # la semilla queda en la bitácora y en el guardado
        try:
            mapa = self._armar(general, version_catalogo)
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
            self._ruta_bitacora = ruta_bitacora

    def _datos_basicos(self, cripta_id: str):
        general = self._cliente.obtener_general(cripta_id)
        self._contador.fijar_presupuesto_maximo(general.presupuesto_solicitudes)
        # La versión del catálogo no viene con la cripta: una sola solicitud, y se pasa ya conocida al catálogo
        return general, self._cliente.obtener_version_catalogo().version

    def _armar(self, general, version_catalogo: str) -> CriptaMapa:
        """Crea mapa, catálogo y precarga y carga el esqueleto completo (sirve para una partida nueva y para cargar)."""
        mapa = CriptaMapa()
        self._catalogo = ServicioCatalogo(
            self._cliente, self._tamano_cache, self._cache_disco,
            fichas_en_uso=self._fichas_en_uso, version_catalogo=version_catalogo,
        )
        self._precarga = ServicioPrecarga(
            self._cliente, general.id, mapa, servicio_catalogo=self._catalogo, cache_disco=self._cache_disco,
            version_cripta=general.version, asincrono=self._asincrono,
        )
        self._precarga.cargar_esqueleto(general.paginas)
        return mapa

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
        self._ruta_bitacora = None
        self._puntaje_registrado = False
        self.bitacora_completa = True

    # ------------------------------------------------------- guardar y cargar
    def guardar(self, ruta) -> None:
        """Guarda la partida en `ruta` (§4.10) y, junto a ella, una copia de la bitácora hasta este instante
        (`ruta` + ".log"). El guardado lleva consigo la historia que lo produjo: al cargarlo, la bitácora se
        restaura tal como estaba y la partida sigue en esa misma bitácora, sin acciones de una rama abandonada."""
        estado = self.partida.a_estado_guardado(self.version_catalogo)   # RuntimeError si ya terminó
        GuardadoBinario().guardar(ruta, estado)
        copia = _bitacora_del_guardado(ruta)
        if self._ruta_bitacora is not None:
            shutil.copyfile(self._ruta_bitacora, copia)   # la bitácora se cierra tras cada línea: la copia está completa
        elif copia.exists():
            copia.unlink()    # una copia vieja de otra historia no debe confundirse con la de este guardado

    def cargar(self, ruta, ruta_bitacora: str | None = None) -> None:
        """Reemplaza la partida en curso por la guardada en `ruta`. Si algo falla antes de empezar a armar
        (archivo ausente o de otro formato, cripta o catálogo de otra versión), la partida en curso no se toca."""
        estado = GuardadoBinario().cargar(ruta)     # FileNotFoundError, o CriptaFormatoIncompatibleError
        general, version_catalogo = self._datos_basicos(estado.cripta_id)
        if version_catalogo != estado.catalogo_version:
            raise CriptaFormatoIncompatibleError(
                f"La partida se guardó con el catálogo {estado.catalogo_version} y el disponible es "
                f"{version_catalogo}: las fichas pudieron cambiar, no se puede garantizar una carga fiel."
            )
        self.cerrar()
        try:
            mapa = self._armar(general, version_catalogo)
            self._partida = Partida.desde_estado_guardado(estado, general, mapa, self._catalogo, self._precarga)
            self.datos_generales, self.version_catalogo, self.semilla = general, version_catalogo, estado.semilla
            if ruta_bitacora is not None:
                self._restaurar_bitacora(estado, ruta, ruta_bitacora)
        except BaseException:
            self.cerrar()
            raise

    def _restaurar_bitacora(self, estado, ruta_guardado, ruta_bitacora: str) -> None:
        encabezado = {
            "id_cripta": estado.cripta_id, "version_cripta": estado.cripta_version,
            "version_catalogo": estado.catalogo_version, "semilla": estado.semilla,
        }
        copia = _bitacora_del_guardado(ruta_guardado)
        acciones = ()
        if copia.is_file():
            leido, acciones = LectorBitacoraPartida(str(copia)).leer()
            if any(leido[campo] != encabezado[campo] for campo in CAMPOS_ENCABEZADO):
                raise CriptaBitacoraError(str(copia), "no corresponde a este guardado")
            encabezado = {campo: valor for campo, valor in leido.items() if campo != "tipo"}
            self.bitacora_completa = not leido.get("parcial", False)
        else:
            # Sin la copia, la bitácora empieza en el guardado: no incluye lo anterior y no se puede reproducir
            encabezado["parcial"] = True
            self.bitacora_completa = False
        self._bitacora = EscritorBitacoraPartida(ruta_bitacora, encabezado)
        for accion in acciones:
            self._bitacora.registrar_accion(accion)
        self._ruta_bitacora = ruta_bitacora

    # ----------------------------------------------------- puntaje y ranking
    def registrar_puntaje(self, nombre_jugador: str) -> tuple[Puntaje, ...]:
        """Al terminar la partida (victoria o derrota): guarda el puntaje en la tabla local (§2.12) y devuelve
        el ranking de esta cripta. Se puede registrar una sola vez por partida."""
        if self._repositorio_puntajes is None:
            raise RuntimeError("Este servicio no tiene una tabla de puntajes configurada.")
        if not nombre_jugador.strip():
            raise ValueError("El nombre del jugador no puede estar vacío.")
        partida = self.partida
        if partida.desenlace() == "en_curso":
            raise RuntimeError("La partida sigue en curso: el puntaje se registra al terminar.")
        if self._puntaje_registrado:
            raise RuntimeError("El puntaje de esta partida ya se registró.")
        resumen = partida.puntaje()
        tabla = self._repositorio_puntajes.registrar(Puntaje(
            nombre_jugador.strip(), self.datos_generales.id, self.datos_generales.version,
            resumen.acciones_jugador, resumen.enemigos_derrotados, resumen.tiempo_final, resumen.victoria,
        ))
        self._puntaje_registrado = True
        return tabla.ranking(self.datos_generales.id, self.datos_generales.version)

    def ranking(self) -> tuple[Puntaje, ...]:
        """Los puntajes guardados de la cripta (e idéntica versión) de la partida en curso."""
        if self._repositorio_puntajes is None:
            raise RuntimeError("Este servicio no tiene una tabla de puntajes configurada.")
        tabla = self._repositorio_puntajes.cargar()
        return tabla.ranking(self.datos_generales.id, self.datos_generales.version) 


def _bitacora_del_guardado(ruta_guardado) -> Path:
    return Path(str(ruta_guardado) + ".log")