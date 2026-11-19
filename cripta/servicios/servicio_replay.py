'''ServicioReplay: reproduce una bitácora de partida (--replay, §4.11) sin vista ni interacción.
Reutiliza ServicioPartida con la semilla del encabezado; no escribe bitácora ni registra puntaje.
Con `hasta` reproduce el log completo y consulta ese instante con el mismo componente que `historia <t>`.
Si el log es parcial, las versiones difieren o una acción no se acepta, lo reporta en vez de reproducir en silencio.
Lee el log con infraestructura/partida_log.py y reconstruye cada acción con Accion.desde_dict().
'''
from dataclasses import dataclass
from pathlib import Path

from cripta.infraestructura.partida_log import LectorBitacoraPartida, diferencias_de_version
from cripta.modelo.accion import Accion
from cripta.modelo.linea_tiempo import ResumenHistorico
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
    historia: ResumenHistorico | None = None   # estado consultado con --hasta, igual que `historia <t>`
    instante: int | None = None        # instante consultado: --hasta, o el reloj final si lo supera
    termino_antes: bool = False        # True si la partida terminó antes del --hasta pedido
    hasta: int | None = None           # el --hasta pedido

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
        if self.historia is not None:
            lineas += self._lineas_de_historia()
        lineas.append(self.reporte)
        return "\n".join(lineas)

    def _lineas_de_historia(self) -> list[str]:
        # Texto plano de los siete grupos de FR-LIN-004, sin vista
        h = self.historia
        lineas = []
        if self.termino_antes:
            lineas.append(f"La partida terminó antes de t={self.hasta}: se consulta el reloj final.")
        lineas += [f"Historia t={self.instante}",
                   f"  Tiempo virtual: {h.tiempo}",
                   f"  Sala {h.sala_id}",
                   f"  Vida {h.vida}/{h.vida_max} | Ataque {h.ataque} | Defensa {h.defensa} | Velocidad {h.velocidad}",
                   "  Inventario: " + (", ".join(f"{o.ficha_id} ({o.instancia_id})" for o in h.inventario) or "vacío"),
                   "  Efectos: " + (", ".join(h.efectos_activos) or "ninguno"),
                   "  Enemigos: " + (", ".join(f"{e.etiqueta} PV {e.vida}/{e.vida_max}" for e in h.enemigos) or "ninguno"),
                   "  Mapa conocido:"]
        for sala in h.mapa_conocido:
            nombre = f"{sala.nombre} " if sala.nombre else ""
            lineas.append(f"    Sala {sala.id_sala}: {nombre}({sala.estado})")
            for s in sala.salidas:
                costo = "?" if s.costo is None else s.costo
                lineas.append(f"      {s.direccion}->{s.id_sala_destino} ({costo}) {s.estado_puerta}")
        return lineas


class ServicioReplay:
    def __init__(self, servicio_partida):
        self._servicio = servicio_partida

    def reproducir(self, ruta: str, hasta: int | None = None) -> ResultadoReplay:
        """Lanza CriptaBitacoraError si el log no existe o está dañado; los errores de red salen tal cual.
        Con `hasta` reproduce el log completo y consulta ese instante con el mismo componente que `historia <t>`
        (o el reloj final si `hasta` lo supera). Lanza ValueError si `hasta` no es un entero mayor o igual a 0."""
        if hasta is not None and (isinstance(hasta, bool) or not isinstance(hasta, int) or hasta < 0):
            raise ValueError(f"--hasta debe ser un entero mayor o igual a 0 y se recibió {hasta!r}.")
        lector = LectorBitacoraPartida(ruta)
        encabezado, acciones = lector.leer()
        numeros_linea = self._numeros_linea_acciones(ruta)
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
            return self._reproducir_acciones(cabecera, avisos, acciones, hasta, numeros_linea)
        finally:
            servicio.cerrar()

    def _reproducir_acciones(self, cabecera, avisos, acciones, hasta, numeros_linea) -> ResultadoReplay:
        servicio = self._servicio
        problemas = []
        pasos = []
        reproducidas = 0
        for indice, datos in enumerate(acciones):
            numero = numeros_linea[indice]
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
        historia = instante = None
        if hasta is not None and not problemas:
            reloj_final = servicio.partida.vista().tiempo
            instante = min(hasta, reloj_final)
            historia = servicio.partida.consultar_instante(instante)
        return ResultadoReplay(
            cabecera, not problemas, tuple(problemas), avisos, reproducidas, len(acciones),
            servicio.partida.desenlace(), servicio.partida.puntaje(), servicio.reporte_final(), tuple(pasos),
            historia, instante, hasta is not None and instante is not None and hasta > instante, hasta,
        )

    @staticmethod
    def _numeros_linea_acciones(ruta):
        numeros = []
        encontro_encabezado = False
        with Path(ruta).open(encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                if not linea.strip() or linea.lstrip().startswith("#"):
                    continue
                if not encontro_encabezado:
                    encontro_encabezado = True
                    continue
                numeros.append(numero)
        return numeros
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
