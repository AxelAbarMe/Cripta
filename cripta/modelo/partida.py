"""Partida: el motor del juego (docs/CONTRATO_PARTIDA.md).

No conoce HTTP, archivos ni la vista: recibe sus dependencias ya construidas.
El jugador y los enemigos son eventos del mismo reloj virtual; el orden sale solo de
(tiempo, secuencia). Toda la aleatoriedad sale de una única random.Random(semilla).
"""
import random

from cripta.constantes import COSTO_ATACAR, COSTO_ESPERAR, COSTO_MOVER, TRAMPA_REARME_DEFAULT
from cripta.modelo import combate
from cripta.modelo.bitacora_mensajes import BitacoraMensajes
from cripta.modelo.comportamiento_enemigo import decidir_accion_enemigo
from cripta.modelo.efectos import EfectoTrampa
from cripta.modelo.historial_retroceso import HistorialRetroceso
from cripta.modelo.jugador import Jugador
from cripta.modelo.reloj import RelojEventos, calcular_intervalo
from cripta.modelo.resultado_partida import (
    EnemigoVista,
    ResultadoAccion,
    ResumenPuntaje,
    SalidaVista,
    TrampaVista,
    VistaPartida,
)

EN_CURSO = "en_curso"
VICTORIA = "victoria"
DERROTA = "derrota"


class Partida:
    def __init__(self, datos_generales, mapa, servicio_catalogo, servicio_precarga, semilla: int):
        self._datos = datos_generales            # CriptaGeneralDTO
        self._mapa = mapa
        self._catalogo = servicio_catalogo
        self._precarga = servicio_precarga
        self._semilla = semilla
        self._azar = random.Random(semilla)      # única fuente de azar de la partida
        self._reloj = RelojEventos()
        self._jugador = Jugador(datos_generales.jugador, datos_generales.sala_inicial, datos_generales.inventario_max)
        self._bitacora = BitacoraMensajes()
        self._historial = HistorialRetroceso()   # se conecta en el retroceso 
        self._desenlace = EN_CURSO
        self._acciones_ejecutadas = 0
        self._enemigos_derrotados = 0
        self._turno_listo = False                # True cuando el jugador puede decidir
        self._mensajes_nuevos: list[str] = []
        self._iniciada = False

    # ------------------------------------------------------------------ inicio
    def iniciar(self) -> None:
        """§2.4: contenido de la sala inicial, rastro en tiempo 0, enemigos activados y
        primera acción del jugador en tiempo 0."""
        if self._iniciada:
            raise RuntimeError("La partida ya fue iniciada.")
        self._iniciada = True
        sala = self._precarga.preparar_sala(self._datos.sala_inicial)
        self._precarga.precargar_desde(self._datos.sala_inicial)
        sala.marcar_visita(0)
        self._activar_enemigos_de(sala)
        self._reloj.programar(0, self._marcar_turno_jugador, "turno del jugador")
        self._avanzar_hasta_turno_jugador()
        self._mensajes_nuevos = []

    # --------------------------------------------------------- ciclo de eventos
    def _marcar_turno_jugador(self) -> None:
        self._turno_listo = True

    def _avanzar_hasta_turno_jugador(self) -> None:
        """Ejecuta eventos (enemigos, efectos) hasta que le toque decidir al jugador."""
        while not self._turno_listo and self._desenlace == EN_CURSO:
            if self._reloj.ejecutar_siguiente() is None:
                break

    def _terminar_accion_jugador(self, costo: int) -> None:
        self._acciones_ejecutadas += 1
        self._turno_listo = False
        intervalo = calcular_intervalo(costo, self._jugador.velocidad)
        self._jugador.tiempo_siguiente = self._reloj.tiempo_actual + intervalo
        self._reloj.programar(self._jugador.tiempo_siguiente, self._marcar_turno_jugador, "turno del jugador")
        self._avanzar_hasta_turno_jugador()

    # --------------------------------------------------------------- enemigos
    def _activar_enemigos_de(self, sala) -> None:
        # Los dormidos ya vienen en orden ascendente de instancia: reciben secuencias deterministas
        for enemigo in sala.activar_enemigos_dormidos():
            enemigo.activar()
            self._programar_turno_enemigo(enemigo, COSTO_MOVER)

    def _programar_turno_enemigo(self, enemigo, costo: int) -> None:
        intervalo = calcular_intervalo(costo, enemigo.velocidad)
        enemigo.tiempo_siguiente = self._reloj.tiempo_actual + intervalo
        enemigo.evento_pendiente = self._reloj.programar(
            enemigo.tiempo_siguiente, lambda e=enemigo: self._turno_enemigo(e), f"turno de {enemigo.instancia_id}"
        )

    def _turno_enemigo(self, enemigo) -> None:
        if not enemigo.esta_vivo() or self._desenlace != EN_CURSO:
            return
        tipo, direccion = decidir_accion_enemigo(
            enemigo, self._jugador.sala_actual, self._mapa, self._azar, self._reloj.tiempo_actual
        )
        if tipo == "atacar":
            daño = combate.atacar(enemigo, self._jugador, self._azar)
            self._decir(f"{self._etiqueta(enemigo)} te ataca y te hace {daño} de daño.")
            if not self._jugador.esta_vivo():
                self._desenlace = DERROTA
                self._decir("Has muerto.")
                return
            costo = COSTO_ATACAR
        elif tipo == "mover":
            self._mover_enemigo(enemigo, direccion)
            costo = COSTO_MOVER
        else:
            costo = COSTO_ESPERAR
        self._programar_turno_enemigo(enemigo, costo)

    def _mover_enemigo(self, enemigo, direccion: str) -> None:
        origen = self._mapa.obtener(enemigo.sala_actual)
        destino_id = origen.esqueleto.salida(direccion).sala_destino
        destino = self._mapa.obtener(destino_id)
        origen.enemigos_activos.remove(enemigo)
        destino.enemigos_activos.append(enemigo)   # permanece activo aunque el jugador no haya entrado
        enemigo.sala_actual = destino_id

    # ------------------------------------------------------------- acciones
    def ejecutar_accion(self, accion) -> ResultadoAccion:
        self._mensajes_nuevos = []
        if not self._iniciada:
            raise RuntimeError("Hay que llamar a iniciar() antes de ejecutar acciones.")
        if self._desenlace != EN_CURSO:
            return self._rechazar("La partida ya terminó.")
        if accion.tipo == "esperar":
            return self._esperar(accion)
        if accion.tipo == "mover":
            return self._mover(accion)
        if accion.tipo == "abrir":
            return self._abrir(accion)
        return self._rechazar(f"La acción '{accion.tipo}' todavía no está implementada.")

    def _esperar(self, accion) -> ResultadoAccion:
        self._sala_actual().marcar_visita(self._reloj.tiempo_actual)   # el rastro se refresca en cada acción
        self._decir("Esperas.")
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()


    def _mover(self, accion) -> ResultadoAccion:
        sala = self._sala_actual()
        direccion = accion.argumento
        salida = sala.esqueleto.salida(direccion)
        if salida is None:
            return self._rechazar(f"No hay salida hacia el {direccion}.")
        if not self._mapa.puerta_transitable(sala.id, direccion):
            return self._rechazar("La puerta está cerrada.")
        # El contenido de la sala destino debe estar en memoria antes de confirmar el movimiento 
        # Si todavía no llegó, esta llamada espera: la espera real no mueve el reloj virtual.
        destino = self._precarga.preparar_sala(salida.sala_destino)
        tiempo = self._reloj.tiempo_actual
        sala.marcar_visita(tiempo)
        self._jugador.sala_actual = destino.id
        destino.marcar_visita(tiempo)   # el rastro de la sala destino es el instante en que se entra
        self._decir(f"Entras a {destino.esqueleto.nombre}.")
        self._activar_enemigos_de(destino)
        self._precarga.precargar_desde(destino.id)
        self._activar_trampas_de(destino)   # antes de procesar el siguiente evento del reloj 
        if self._jugador.esta_vivo() and destino.id == self._datos.sala_salida:
            self._desenlace = VICTORIA
            self._decir("¡Has llegado a la salida! Ganas la partida.")
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    def _activar_trampas_de(self, sala) -> None:
        for trampa in sala.trampas:
            if not self._jugador.esta_vivo():
                break
            ficha = self._catalogo.obtener(trampa.tipo_catalogo)
            rearme = ficha.rearme if ficha.rearme is not None else TRAMPA_REARME_DEFAULT

            def aplicar(ficha=ficha):
                # Decisión: el daño de la trampa es fijo (no pasa por la defensa ni consume azar)
                self._jugador.recibir_daño(ficha.daño)
                self._decir(f"Pisas {ficha.nombre} y recibes {ficha.daño} de daño.")

            EfectoTrampa(self._reloj, trampa, rearme).activar(aplicar)
        if not self._jugador.esta_vivo():
            self._desenlace = DERROTA
            self._decir("Has muerto.")

    def _abrir(self, accion) -> ResultadoAccion:
        sala = self._sala_actual()
        direccion = accion.argumento
        if sala.esqueleto.salida(direccion) is None:
            return self._rechazar(f"No hay salida hacia el {direccion}.")
        if self._mapa.puerta_transitable(sala.id, direccion):
            return self._rechazar("La puerta ya está abierta.")
        # La llave y el cierre automático el API solo los marca en uno de los dos lados de la puerta
        llave, cierre = self._mapa.datos_de_puerta(sala.id, direccion)
        if llave is None:
            return self._rechazar("Esta puerta no tiene cerradura.")
        if llave not in self._jugador.inventario.fichas_en_uso():   # la llave coincide con el id de su ficha
            return self._rechazar("No tienes la llave de esta puerta.")
        sala.marcar_visita(self._reloj.tiempo_actual)
        self._mapa.abrir_puerta(sala.id, direccion)
        self._decir(f"Abres la puerta hacia el {direccion}.")
        if cierre is not None:
            self._reloj.programar_en(
                cierre, lambda s=sala.id, d=direccion: self._cerrar_puerta_automatica(s, d), "cierre automático de puerta"
            )
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    def _cerrar_puerta_automatica(self, sala_id: int, direccion: str) -> None:
        # Cierra los dos lados; quien ya cruzó se queda donde está (solo se impide volver a atravesar)
        self._mapa.cerrar_puerta(sala_id, direccion)
        self._decir("Una puerta se cierra sola.")


    def _rechazar(self, motivo: str) -> ResultadoAccion:
        self._decir(motivo)
        return ResultadoAccion(False, motivo, tuple(self._mensajes_nuevos), self._desenlace, self._reloj.tiempo_actual)

    def _aceptar(self) -> ResultadoAccion:
        return ResultadoAccion(True, None, tuple(self._mensajes_nuevos), self._desenlace, self._reloj.tiempo_actual)

    # ------------------------------------------------------------- consultas
    def desenlace(self) -> str:
        return self._desenlace

    def mensajes(self) -> tuple[str, ...]:
        return self._bitacora.mensajes()

    def puntaje(self) -> ResumenPuntaje:
        return ResumenPuntaje(self._acciones_ejecutadas, self._enemigos_derrotados, self._reloj.tiempo_actual)

    def inventario_siguiente(self):
        return self._jugador.inventario.siguiente()

    def inventario_anterior(self):
        return self._jugador.inventario.anterior()

    def inventario_ordenado(self, criterio: str):
        return self._jugador.inventario.vista_ordenada(criterio)

    def vista(self) -> VistaPartida:
        sala = self._sala_actual()
        salidas = tuple(
            SalidaVista(direccion, destino, not self._mapa.puerta_transitable(sala.id, direccion))
            for direccion, destino in self._mapa.vecinos(sala.id)
        )
        enemigos = tuple(
            EnemigoVista(self._etiqueta(e), e.instancia_id, e.vida, e.vida_max)
            for e in sala.enemigos_activos if e.esta_vivo()
        )
        objetos = tuple(f.nombre for f in self._catalogo.obtener_varias(sala.objetos_en_suelo)) if sala.objetos_en_suelo else ()
        trampas = tuple(
            TrampaVista(self._catalogo.obtener(t.tipo_catalogo).nombre, t.armada) for t in sala.trampas
        )
        jugador = self._jugador
        inventario = jugador.inventario
        actual = inventario.objeto_actual()
        efectos = ("Veneno",) if jugador.veneno_activo is not None else ()
        return VistaPartida(
            sala_id=sala.id,
            sala_nombre=sala.esqueleto.nombre,
            salidas=salidas,
            enemigos=enemigos,
            objetos_suelo=objetos,
            trampas=trampas,
            vida=jugador.vida,
            vida_max=jugador.vida_max,
            ataque=jugador.ataque_efectivo,
            defensa=jugador.defensa_efectiva,
            velocidad=jugador.velocidad,
            efectos_activos=efectos,
            objeto_actual=actual.ficha.nombre if actual else None,
            inventario_cantidad=len(inventario),
            inventario_capacidad=self._datos.inventario_max,
            arma_equipada=inventario.arma_equipada.ficha.nombre if inventario.arma_equipada else None,
            armadura_equipada=inventario.armadura_equipada.ficha.nombre if inventario.armadura_equipada else None,
            tiempo=self._reloj.tiempo_actual,
            desenlace=self._desenlace,
        )

    # ------------------------------------------------------------- auxiliares
    def _sala_actual(self):
        return self._mapa.obtener(self._jugador.sala_actual)

    @staticmethod
    def _etiqueta(enemigo) -> str:
        return f"{enemigo.nombre} [{enemigo.instancia_id}]"

    def _decir(self, texto: str) -> None:
        self._bitacora.agregar(texto)
        self._mensajes_nuevos.append(texto)