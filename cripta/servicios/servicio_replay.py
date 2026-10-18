'''ServicioReplay: reproduce una bitácora de partida (--replay, §4.11) sin vista ni interacción.
Reutiliza ServicioPartida con la semilla del encabezado; no escribe bitácora ni registra puntaje.
Si el log es parcial, las versiones difieren o una acción no se acepta, lo reporta en vez de reproducir en silencio.
Lee el log con infraestructura/partida_log.py y reconstruye cada acción con Accion.desde_dict().
'''
from dataclasses import dataclass

from cripta.infraestructura.partida_log import LectorBitacoraPartida, diferencias_de_version
from cripta.modelo.accion import Accion
from cripta.modelo.resultado_partida import ResumenPuntaje


@dataclass(frozen=True, slots=True)
class ResultadoReplay:
    """Resultado de una reproducción: si fue fiel, qué la impidió o la desvió y el desenlace final."""
    cabecera: str                      # una línea con cripta, versiones y semilla del log
    fiel: bool                         # True solo si se reprodujo completa y sin divergencias
    problemas: tuple[str, ...]         # motivos por los que no se reprodujo o por los que divergió
    avisos: tuple[str, ...]            # advertencias que no impiden reproducir
    acciones_reproducidas: int
    acciones_en_log: int
    desenlace: str | None              # None si no se reprodujo
    puntaje: ResumenPuntaje | None
    reporte: str | None                # reporte_final() del servicio (5.1)
    pasos: tuple[str, ...] = ()        # una entrada por acción reproducida, con sus mensajes y el estado resultante

    def informe(self) -> str:
        # Texto plano para mostrar en consola
        lineas = [self.cabecera]
        lineas += [f"Aviso: {aviso}" for aviso in self.avisos]
        lineas += self.pasos
        lineas.append(f"Acciones reproducidas: {self.acciones_reproducidas} de {self.acciones_en_log}")
        lineas += [f"PROBLEMA: {problema}" for problema in self.problemas]
        if self.desenlace is None:
            lineas.append("No se puede garantizar una reproducción fiel: la partida no se reprodujo.")
            return "\n".join(lineas)
        p = self.puntaje
        lineas.append(f"Desenlace: {self.desenlace} | acciones del jugador: {p.acciones_jugador}, "
                      f"enemigos derrotados: {p.enemigos_derrotados}, tiempo final: {p.tiempo_final}")
        if self.problemas:
            lineas.append("La reproducción divergió del log: el resultado no es fiel.")
        lineas.append(self.reporte)
        return "\n".join(lineas)


class ServicioReplay:
    def __init__(self, servicio_partida):
        self._servicio = servicio_partida

    def reproducir(self, ruta: str) -> ResultadoReplay:
        """Lanza CriptaBitacoraError si el log no existe o está dañado; los errores de red salen tal cual."""
        lector = LectorBitacoraPartida(ruta)
        encabezado, acciones = lector.leer()
        cabecera = (f"Cripta {encabezado['id_cripta']} (versión {encabezado['version_cripta']}), "
                    f"catálogo {encabezado['version_catalogo']}, semilla {encabezado['semilla']}")
        avisos = ("la última línea del log estaba incompleta y se ignoró",) if lector.ultima_linea_incompleta else ()
        if encabezado.get("parcial", False):
            return self._sin_reproducir(cabecera, avisos, len(acciones), (
                "el log es parcial (la partida se cargó sin su bitácora anterior)",))

        servicio = self._servicio
        servicio.iniciar_nueva(encabezado["id_cripta"], encabezado["semilla"], None)   # sin bitácora ni puntaje
        try:
            diferencias = diferencias_de_version(encabezado, servicio.datos_generales.version, servicio.version_catalogo)
            if diferencias:
                return self._sin_reproducir(cabecera, avisos, len(acciones), diferencias)
            return self._reproducir_acciones(cabecera, avisos, acciones)
        finally:
            servicio.cerrar()

    def _reproducir_acciones(self, cabecera, avisos, acciones) -> ResultadoReplay:
        servicio = self._servicio
        problemas = []
        pasos = []
        reproducidas = 0
        for numero, datos in enumerate(acciones, start=2):   # número de línea del log: la 1 es el encabezado
            try:
                accion = Accion.desde_dict(datos)
                resultado = servicio.ejecutar(accion)
            except ValueError as error:
                problemas.append(f"línea {numero}: acción inválida ({error})")
                break
            if not resultado.aceptada:
                problemas.append(f"línea {numero}: la acción {datos} no se aceptó ({resultado.motivo_rechazo})")
                break
            reproducidas += 1
            pasos.append(self._describir_paso(reproducidas, accion, resultado))
        return ResultadoReplay(
            cabecera, not problemas, tuple(problemas), avisos, reproducidas, len(acciones),
            servicio.partida.desenlace(), servicio.partida.puntaje(), servicio.reporte_final(), tuple(pasos),
        )

    def _describir_paso(self, numero, accion, resultado) -> str:
        # Salida de solo lectura: texto plano, sin vista ni entrada del usuario (6)
        vista = self._servicio.partida.vista()
        argumento = "" if accion.argumento is None else f" {accion.argumento}"
        lineas = [f"[{numero}] {accion.tipo}{argumento} -> t={vista.tiempo}, sala {vista.sala_id} ({vista.sala_nombre}), "
                  f"vida {vista.vida}/{vista.vida_max}"]
        lineas += [f"      {mensaje}" for mensaje in resultado.mensajes]
        return "\n".join(lineas)

    @staticmethod
    def _sin_reproducir(cabecera, avisos, total, problemas) -> ResultadoReplay:
        return ResultadoReplay(cabecera, False, tuple(problemas), avisos, 0, total, None, None, None)