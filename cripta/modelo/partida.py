"""Partida: el motor del juego (docs/CONTRATO_PARTIDA.md).

No conoce HTTP, archivos ni la vista: recibe sus dependencias ya construidas.
El jugador y los enemigos son eventos del mismo reloj virtual; el orden sale solo de
(tiempo, secuencia). Toda la aleatoriedad sale de una única random.Random(semilla).
"""
import random
from contextlib import nullcontext

from cripta.constantes import COSTO_ATACAR, COSTO_ESPERAR, COSTO_MOVER, DIRECCIONES, TRAMPA_REARME_DEFAULT
from cripta.estructuras.vector import VectorOrdenado
from cripta.excepciones import CriptaFormatoIncompatibleError

from cripta.infraestructura.estado_guardado import (
    EV_ANTORCHA_APAGAR,
    EV_CIERRE_PUERTA,
    EV_FIN_VELOCIDAD,
    EV_REARME_TRAMPA,
    EV_TURNO_ACTOR,
    EV_VENENO_PULSO,
)
from cripta.modelo import combate
from cripta.modelo.bitacora_mensajes import BitacoraMensajes
from cripta.modelo.comportamiento_enemigo import decidir_accion_enemigo

from cripta.modelo.efectos import (
    EfectoAntorcha,
    EfectoCambioVelocidad,
    EfectoCierrePuerta,
    EfectoTrampa,
    EfectoVeneno,
)
from cripta.modelo.historial_retroceso import HistorialRetroceso
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.jugador import Jugador

from cripta.modelo.persistencia_modelo import (
    crear_estado,
    restaurar_jugador,
    restaurar_sala,
    siguiente_instancia_tras,
)
from cripta.modelo.reloj import RelojEventos, calcular_intervalo

from cripta.modelo.resultado_partida import (
    EnemigoVista,
    ObjetoSueloVista,
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
        self._mapa.sincronizar_puertas()         # la puerta cerrada en un lado debe estarlo en los dos 
        self._catalogo = servicio_catalogo
        self._precarga = servicio_precarga
        self._semilla = semilla
        self._azar = random.Random(semilla)      # única fuente de azar de la partida
        self._reloj = RelojEventos()
        self._jugador = Jugador(datos_generales.jugador, datos_generales.sala_inicial, datos_generales.inventario_max)
        self._bitacora = BitacoraMensajes()
        self._historial = HistorialRetroceso()
        self._conectar_retroceso()
        self._desenlace = EN_CURSO
        self._acciones_ejecutadas = 0
        self._enemigos_derrotados = 0
        self._turno_listo = False                # True cuando el jugador puede decidir
        self._siguiente_instancia = 0            # para dar ids deterministas a los objetos recogidos
        self._antorcha_encendida = False
        self._salas_preparadas = VectorOrdenado()   # ids de las salas ya pobladas (el jugador llegó a ellas)
        self._mensajes_nuevos: list[str] = []
        self._iniciada = False



    def _conectar_retroceso(self) -> None:
        # Todo lo que cambia en el juego avisa a este historial cómo deshacerse (ver Reversible).
        # Los enemigos, trampas y efectos se conectan cuando se crean o activan.
        registrar = self._historial.registrar_cambio
        self._reloj.registrador = registrar
        self._jugador.registrador = registrar
        self._jugador.inventario.registrador = registrar
        self._mapa.conectar_registrador(registrar)

    def _con_retroceso(self, objeto):
        objeto.registrador = self._historial.registrar_cambio
        return objeto

    def _guardar_contadores(self) -> None:
        # Lo propio de la partida que no vive en otro objeto, incluido el estado del azar:
        # tras retroceder, repetir la misma acción da el mismo resultado (no se puede "volver a tirar")
        estado = (self._acciones_ejecutadas, self._enemigos_derrotados, self._antorcha_encendida,
                  self._siguiente_instancia, self._turno_listo, self._azar.getstate())
        self._historial.registrar_cambio(lambda: self._restaurar_contadores(estado))

    def _restaurar_contadores(self, estado) -> None:
        (self._acciones_ejecutadas, self._enemigos_derrotados, self._antorcha_encendida,
         self._siguiente_instancia, self._turno_listo, estado_azar) = estado
        self._azar.setstate(estado_azar)


    def _marcar_preparada(self, sala_id: int) -> None:
        if not self._salas_preparadas.contiene(sala_id):
            self._salas_preparadas.insertar(sala_id)

    # ---------------------------------------------------------------- guardado
    def a_estado_guardado(self, version_catalogo: str):
        """Convierte la partida a datos planos (EstadoPartida) para GuardadoBinario (§4.10).
        Solo se puede guardar cuando al jugador le toca decidir y la partida sigue en curso."""
        if not self._iniciada:
            raise RuntimeError("Hay que llamar a iniciar() antes de guardar.")
        if self._desenlace != EN_CURSO:
            raise RuntimeError("No se puede guardar una partida terminada.")
        return crear_estado(
            cripta_id=self._datos.id, cripta_version=self._datos.version, catalogo_version=version_catalogo,
            semilla=self._semilla, azar=self._azar, reloj=self._reloj, jugador=self._jugador, mapa=self._mapa,
            salas_preparadas=self._salas_preparadas, acciones_jugador=self._acciones_ejecutadas,
            enemigos_derrotados=self._enemigos_derrotados, mensajes=self._bitacora.mensajes(),
        )


    @classmethod
    def desde_estado_guardado(cls, estado, datos_generales, mapa, servicio_catalogo, servicio_precarga):
        """Reconstruye una partida guardada (§4.10). `mapa`, `servicio_catalogo` y `servicio_precarga`
        deben ser nuevos (con el esqueleto ya cargado). La partida queda lista para que el jugador decida.
        El historial de retroceso empieza vacío: el pergamino no deshace lo anterior al guardado."""
        if estado.cripta_id != datos_generales.id or estado.cripta_version != datos_generales.version:
            raise CriptaFormatoIncompatibleError(
                f"La partida es de {estado.cripta_id} (versión {estado.cripta_version}) y la cripta actual es "
                f"{datos_generales.id} (versión {datos_generales.version}): no se puede garantizar una carga fiel."
            )
        partida = cls(datos_generales, mapa, servicio_catalogo, servicio_precarga, estado.semilla)
        with partida._historial.sin_registrar():   # cargar no es una acción: nada de esto se podría deshacer
            partida._restaurar(estado)
        partida._precarga.precargar_desde(partida._jugador.sala_actual)
        return partida

    def _restaurar(self, estado) -> None:
        enemigos = VectorOrdenado(clave=lambda e: e.instancia_id)
        trampas = VectorOrdenado(clave=lambda t: t.instancia_id)
        for guardada in estado.salas:
            sala = self._mapa.obtener(guardada.sala_id)
            if sala is None:
                raise CriptaFormatoIncompatibleError(f"La partida guardada menciona la sala {guardada.sala_id}, que no existe.")
            restaurar_sala(sala, guardada, self._precarga, self._catalogo, enemigos, trampas)
            if guardada.contenido_cargado:
                self._marcar_preparada(sala.id)
        restaurar_jugador(self._jugador, estado.jugador, self._catalogo)
        for trampa in trampas.elementos():
            self._con_retroceso(trampa)
        for enemigo in enemigos.elementos():
            if enemigo.activo:
                self._con_retroceso(enemigo)
        self._restaurar_agenda(estado.eventos, enemigos, trampas)
        self._reloj.restaurar(estado.reloj_actual, estado.siguiente_secuencia)
        estado.rng.aplicar_a(self._azar)
        self._acciones_ejecutadas = estado.acciones_jugador
        self._enemigos_derrotados = estado.enemigos_derrotados
        for mensaje in estado.mensajes:
            self._bitacora.agregar(mensaje)
        self._siguiente_instancia = siguiente_instancia_tras(self._jugador.inventario)
        self._turno_listo = True                    # solo se guarda cuando al jugador le toca decidir
        self._mensajes_nuevos = []
        self._iniciada = True

    def _restaurar_agenda(self, eventos, enemigos, trampas) -> None:
        """Recrea las acciones del reloj (que son funciones) a partir de sus descriptores guardados."""
        for ev in eventos:
            datos = (ev.tipo, ev.sujeto, ev.a, ev.b)
            if ev.tipo == EV_TURNO_ACTOR:
                enemigo = enemigos.buscar(ev.sujeto)
                if enemigo is None:    # el turno del jugador nunca está pendiente al guardar
                    raise CriptaFormatoIncompatibleError(f"El turno pendiente de «{ev.sujeto}» no corresponde a ningún enemigo.")
                enemigo.evento_pendiente = self._reloj.programar_con_secuencia(
                    ev.tiempo, ev.secuencia, lambda e=enemigo: self._turno_enemigo(e),
                    f"turno de {enemigo.instancia_id}", datos,
                )
            elif ev.tipo == EV_VENENO_PULSO:
                efecto = EfectoVeneno(self._reloj, self._actor_de(ev.sujeto, enemigos), ev.a)
                self._con_retroceso(efecto).restaurar(ev.b, ev.tiempo, ev.secuencia)
            elif ev.tipo == EV_FIN_VELOCIDAD:
                efecto = EfectoCambioVelocidad(self._reloj, self._actor_de(ev.sujeto, enemigos), ev.a, 0)
                self._con_retroceso(efecto).restaurar(ev.a, ev.tiempo, ev.secuencia)
            elif ev.tipo == EV_ANTORCHA_APAGAR:
                self._antorcha_encendida = True
                EfectoAntorcha(self._reloj, 0, self._apagar_antorcha).restaurar(ev.tiempo, ev.secuencia)
            elif ev.tipo == EV_REARME_TRAMPA:
                trampa = trampas.buscar(ev.sujeto)
                if trampa is None:
                    raise CriptaFormatoIncompatibleError(f"El rearme pendiente de «{ev.sujeto}» no corresponde a ninguna trampa.")
                EfectoTrampa(self._reloj, trampa).restaurar_rearme(ev.tiempo, ev.secuencia)
            elif ev.tipo == EV_CIERRE_PUERTA:
                EfectoCierrePuerta(
                    self._reloj, self._mapa, int(ev.sujeto), DIRECCIONES[ev.a], 0, self._avisar_cierre_de_puerta
                ).restaurar(ev.tiempo, ev.secuencia)
            else:
                raise CriptaFormatoIncompatibleError(f"Tipo de evento desconocido en la agenda guardada: {ev.tipo}.")

    def _actor_de(self, sujeto: str, enemigos):
        if sujeto == "jugador":
            return self._jugador
        actor = enemigos.buscar(sujeto)
        if actor is None:
            raise CriptaFormatoIncompatibleError(f"La agenda guardada menciona a «{sujeto}», que no existe.")
        return actor


    # ------------------------------------------------------------------ inicio
    def iniciar(self) -> None:
        """§2.4: contenido de la sala inicial, rastro en tiempo 0, enemigos activados y
        primera acción del jugador en tiempo 0."""
        if self._iniciada:
            raise RuntimeError("La partida ya fue iniciada.")
        sala = self._precarga.preparar_sala(self._datos.sala_inicial)
        self._marcar_preparada(sala.id)
        self._precarga.precargar_desde(self._datos.sala_inicial)
        sala.marcar_visita(0)
        self._activar_enemigos_de(sala)
        self._reloj.programar(0, self._marcar_turno_jugador, "turno del jugador", datos=(EV_TURNO_ACTOR, "jugador", 0, 0))
        self._avanzar_hasta_turno_jugador()
        self._mensajes_nuevos = []
        self._iniciada = True

    # --------------------------------------------------------- ciclo de eventos
    def _marcar_turno_jugador(self) -> None:
        self._turno_listo = True
        self._jugador.evento_pendiente = None   # ya se ejecutó: no hay acción del jugador que reajustar

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
        self._jugador.evento_pendiente = self._reloj.programar(
            self._jugador.tiempo_siguiente, self._marcar_turno_jugador, "turno del jugador",
            datos=(EV_TURNO_ACTOR, "jugador", 0, 0),
        )
        self._avanzar_hasta_turno_jugador()
        self._historial.cerrar_intervalo()   # el intervalo llega hasta la siguiente decisión del jugador

    # --------------------------------------------------------------- enemigos
    def _activar_enemigos_de(self, sala) -> None:
        # Los dormidos ya vienen en orden ascendente de instancia: reciben secuencias deterministas
        for enemigo in sala.activar_enemigos_dormidos():
            self._con_retroceso(enemigo)
            enemigo.activar()
            self._programar_turno_enemigo(enemigo, COSTO_MOVER)

    def _programar_turno_enemigo(self, enemigo, costo: int) -> None:
        intervalo = calcular_intervalo(costo, enemigo.velocidad)
        enemigo.tiempo_siguiente = self._reloj.tiempo_actual + intervalo
        enemigo.evento_pendiente = self._reloj.programar(
            enemigo.tiempo_siguiente, lambda e=enemigo: self._turno_enemigo(e), f"turno de {enemigo.instancia_id}",
            datos=(EV_TURNO_ACTOR, enemigo.instancia_id, 0, 0),
        )

    def _turno_enemigo(self, enemigo) -> None:
        if not enemigo.esta_vivo() or self._desenlace != EN_CURSO:
            return
        tipo, direccion = decidir_accion_enemigo(
            enemigo, self._jugador.sala_actual, self._mapa, self._azar, self._reloj.tiempo_actual
        )
        if tipo == "atacar":
            daño = combate.atacar(enemigo, self._jugador, self._azar)
            self._decir(f"{enemigo.etiqueta()} te ataca y te hace {daño} de daño.")
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
        indice = origen.enemigos_activos.index(enemigo)
        origen.enemigos_activos.remove(enemigo)
        destino.enemigos_activos.append(enemigo)   # permanece activo aunque el jugador no haya entrado
        enemigo.sala_actual = destino_id

        def deshacer():
            destino.enemigos_activos.remove(enemigo)
            origen.enemigos_activos.insert(indice, enemigo)
        self._historial.registrar_cambio(deshacer)

    # ------------------------------------------------------------- acciones
    def ejecutar_accion(self, accion) -> ResultadoAccion:
        self._mensajes_nuevos = []
        if not self._iniciada:
            raise RuntimeError("Hay que llamar a iniciar() antes de ejecutar acciones.")
        if self._desenlace != EN_CURSO:
            return self._rechazar("La partida ya terminó.")
        if accion.tipo == "pergamino":
            return self._usar_pergamino()   # no es una acción del jugador: no abre intervalo en el historial
        self._historial.iniciar_intervalo()
        self._guardar_contadores()
        try:
            resultado = self._despachar(accion)
        except BaseException:
            self._historial.revertir_intervalo_actual()   # si la infraestructura falla a medias, no queda nada a medias
            raise
        if not resultado.aceptada:
            self._historial.descartar_intervalo_actual()   # una acción rechazada no cambia nada
        return resultado

    def _despachar(self, accion) -> ResultadoAccion:
        if accion.tipo == "esperar":
            return self._esperar(accion)
        if accion.tipo == "mover":
            return self._mover(accion)
        if accion.tipo == "abrir":
            return self._abrir(accion)
        if accion.tipo == "atacar":
            return self._atacar(accion)
        if accion.tipo == "recoger":
            return self._recoger(accion)
        if accion.tipo == "soltar":
            return self._soltar(accion)
        if accion.tipo == "equipar":
            return self._equipar(accion)
        if accion.tipo == "usar":
            return self._usar(accion)
        return self._rechazar(f"La acción '{accion.tipo}' todavía no está implementada.")

    def _usar_pergamino(self) -> ResultadoAccion:
        """§2.11: deshace la última acción del jugador (y todo lo que pasó hasta la siguiente decisión).
        No consume tiempo virtual. El pergamino se descuenta fuera del alcance de la reversión."""
        inventario = self._jugador.inventario
        if inventario.cantidad_pergaminos() == 0:
            return self._rechazar("No tienes ningún pergamino de retroceso.")
        if not self._historial.hay_intervalo_para_deshacer():
            return self._rechazar("No hay ninguna acción que deshacer.")
        self._historial.deshacer_ultimo_intervalo()
        with self._historial.sin_registrar():
            inventario.quitar_primero_de_clase("pergamino_retroceso")
        self._decir("Usas un pergamino de retroceso: el tiempo vuelve atrás.")
        return self._aceptar()

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
        # El contenido de la sala destino debe estar en memoria antes de confirmar el movimiento (§2.5).
        # Si todavía no llegó, esta llamada espera: la espera real no mueve el reloj virtual.
        with self._historial.sin_registrar():   # cargar contenido es infraestructura, no estado del juego
            destino = self._precarga.preparar_sala(salida.sala_destino)
        self._marcar_preparada(destino.id)
        tiempo = self._reloj.tiempo_actual
        sala.marcar_visita(tiempo)
        self._jugador.sala_actual = destino.id
        destino.marcar_visita(tiempo)   # el rastro de la sala destino es el instante en que se entra
        self._decir(f"Entras a {destino.esqueleto.nombre}.")
        self._activar_enemigos_de(destino)
        with self._historial.sin_registrar():
            self._precarga.precargar_desde(destino.id)
        self._activar_trampas_de(destino)   # antes de procesar el siguiente evento del reloj (§2.10)
        if (self._jugador.esta_vivo() and destino.id == self._datos.sala_salida and self._puerta_exige_llave_de_salida(sala.id, direccion)):
            self._desenlace = VICTORIA
            self._decir("¡Has llegado a la salida! Ganas la partida.")
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    def _puerta_exige_llave_de_salida(self, origen_id: int, direccion: str) -> bool:
        # 2.12: la puerta cruzada exige llave_salida; solo se cruza abierta y abrirla requirió esa llave
        llave, _cierre = self._mapa.datos_de_puerta(origen_id, direccion)
        return llave is not None and llave == self._datos.llave_salida

    def _activar_trampas_de(self, sala) -> None:
        for trampa in sala.trampas:
            if not self._jugador.esta_vivo():
                break
            ficha = self._catalogo.obtener(trampa.tipo_catalogo)
            rearme = ficha.rearme if ficha.rearme is not None else TRAMPA_REARME_DEFAULT
            self._con_retroceso(trampa)

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
            EfectoCierrePuerta(
                self._reloj, self._mapa, sala.id, direccion, cierre, self._avisar_cierre_de_puerta
            ).programar_cierre()
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()


    def _avisar_cierre_de_puerta(self) -> None:
        # El efecto cierra los dos lados; quien ya cruzó se queda donde está (solo se impide volver a atravesar)
        self._decir("Una puerta se cierra sola.")


    def _atacar(self, accion) -> ResultadoAccion:
        sala = self._sala_actual()
        enemigo = self._buscar_enemigo(sala, accion.argumento)
        if enemigo is None:
            return self._rechazar("Ese enemigo no está en esta sala.")
        sala.marcar_visita(self._reloj.tiempo_actual)
        daño = combate.atacar(self._jugador, enemigo, self._azar)
        self._decir(f"Atacas a {enemigo.etiqueta()} y le haces {daño} de daño.")
        if not enemigo.esta_vivo():
            self._matar_enemigo(enemigo, sala)
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    @staticmethod
    def _buscar_enemigo(sala, instancia: str):
        for enemigo in sala.enemigos_activos:
            if enemigo.instancia_id == instancia and enemigo.esta_vivo():
                return enemigo
        return None

    def _matar_enemigo(self, enemigo, sala) -> None:
        if enemigo.evento_pendiente is not None:
            self._reloj.cancelar(enemigo.evento_pendiente)   # sus eventos futuros ya no ocurren
        indice = sala.enemigos_activos.index(enemigo)
        sala.enemigos_activos.remove(enemigo)
        self._historial.registrar_cambio(lambda: sala.enemigos_activos.insert(indice, enemigo))
        self._enemigos_derrotados += 1
        self._decir(f"{enemigo.etiqueta()} muere.")
        if enemigo.suelta:
            for ficha_id in enemigo.suelta:
                sala.agregar_objeto(ficha_id)
            nombres = ", ".join(f.nombre for f in self._catalogo.obtener_varias(enemigo.suelta))
            self._decir(f"Deja caer: {nombres}.")

    def _recoger(self, accion) -> ResultadoAccion:
        sala = self._sala_actual()
        inventario = self._jugador.inventario
        ficha_id = accion.argumento
        if ficha_id not in sala.objetos_en_suelo:
            return self._rechazar("Ese objeto no está en el suelo.")
        if inventario.esta_lleno():
            return self._rechazar("El inventario está lleno; debes soltar algo primero.")
        sala.marcar_visita(self._reloj.tiempo_actual)
        ficha = self._catalogo.obtener(ficha_id)
        with self._sin_deshacer_si_es_pergamino(ficha):
            sala.quitar_objeto(ficha_id)
            inventario.recoger(ObjetoInventario(self._nueva_instancia(), ficha))
        self._decir(f"Recoges {ficha.nombre}.")
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    def _soltar(self, accion) -> ResultadoAccion:
        sala = self._sala_actual()
        inventario = self._jugador.inventario
        if inventario.ir_a_posicion(accion.argumento) is None:
            return self._rechazar("No hay ningún objeto en esa posición del inventario.")
        sala.marcar_visita(self._reloj.tiempo_actual)
        with self._sin_deshacer_si_es_pergamino(inventario.objeto_actual().ficha):
            objeto = inventario.soltar_actual()
            sala.agregar_objeto(objeto.ficha.id)
        self._decir(f"Sueltas {objeto.ficha.nombre}.")
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    def _equipar(self, accion) -> ResultadoAccion:
        inventario = self._jugador.inventario
        if inventario.ir_a_posicion(accion.argumento) is None:
            return self._rechazar("No hay ningún objeto en esa posición del inventario.")
        objeto = inventario.objeto_actual()
        if objeto.ficha.clase not in ("arma", "armadura"):
            return self._rechazar(f"{objeto.ficha.nombre} no se puede equipar.")
        self._sala_actual().marcar_visita(self._reloj.tiempo_actual)
        inventario.equipar_actual()   # lo mueve al frente del orden real
        self._decir(f"Equipas {objeto.ficha.nombre}.")
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    def _usar(self, accion) -> ResultadoAccion:
        inventario = self._jugador.inventario
        if inventario.ir_a_posicion(accion.argumento) is None:
            return self._rechazar("No hay ningún objeto en esa posición del inventario.")
        ficha = inventario.objeto_actual().ficha
        motivo = self._motivo_no_usable(ficha)
        if motivo is not None:
            return self._rechazar(motivo)
        self._sala_actual().marcar_visita(self._reloj.tiempo_actual)
        self._aplicar_uso(ficha)
        inventario.soltar_actual()   # se consume (no va al suelo)
        self._terminar_accion_jugador(accion.costo_base)
        return self._aceptar()

    def _motivo_no_usable(self, ficha) -> str | None:
        if ficha.clase == "pocion":
            return None
        if ficha.clase == "antorcha":
            return "Ya tienes una antorcha encendida." if self._antorcha_encendida else None
        if ficha.clase == "antidoto":
            return None if self._jugador.veneno_activo is not None else "No estás envenenado."
        if ficha.clase == "llave":
            return "La llave se usa al abrir una puerta."
        if ficha.clase == "pergamino_retroceso":
            return "El pergamino se usa con la acción de retroceso."
        if ficha.clase in ("arma", "armadura"):
            return f"{ficha.nombre} se equipa, no se usa."
        return f"{ficha.nombre} no se puede usar así."

    def _aplicar_uso(self, ficha) -> None:
        if ficha.clase == "pocion":
            if ficha.cura:
                self._jugador.curar(ficha.cura)   # nunca supera vida_max
                self._decir(f"Usas {ficha.nombre} y recuperas vida ({self._jugador.vida}/{self._jugador.vida_max}).")
            if ficha.modificador_velocidad:
                efecto = EfectoCambioVelocidad(self._reloj, self._jugador, ficha.modificador_velocidad, ficha.duracion)
                self._con_retroceso(efecto).aplicar()
                self._decir(f"Usas {ficha.nombre}: tu velocidad cambia durante {ficha.duracion} unidades.")
        elif ficha.clase == "antidoto":
            self._jugador.veneno_activo.cancelar()
            self._decir(f"Usas {ficha.nombre} y el veneno desaparece.")
        elif ficha.clase == "antorcha":
            self._antorcha_encendida = True
            EfectoAntorcha(self._reloj, ficha.duracion, self._apagar_antorcha).encender()
            self._decir(f"Enciendes {ficha.nombre}.")

    def _apagar_antorcha(self) -> None:
        self._antorcha_encendida = False
        self._decir("Tu antorcha se apaga.")

    def _sin_deshacer_si_es_pergamino(self, ficha):
        """Recoger o soltar un pergamino no se deshace con el retroceso (§2.11, Apéndice B)."""
        if ficha.clase == "pergamino_retroceso":
            return self._historial.sin_registrar()
        return nullcontext()

    def _nueva_instancia(self) -> str:
        self._siguiente_instancia += 1
        return f"i-{self._siguiente_instancia}"


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
        return ResumenPuntaje(
            self._acciones_ejecutadas, self._enemigos_derrotados, self._reloj.tiempo_actual, self._desenlace == VICTORIA
        )

    def fichas_en_uso(self) -> tuple[str, ...]:
        """Ids de ficha que la caché del catálogo no puede liberar (§4.4): objetos del inventario, objetos
        y trampas de la sala actual y enemigos vivos. Solo se consulta al desalojar, no en cada acceso."""
        sala = self._sala_actual()
        ids = list(self._jugador.inventario.fichas_en_uso())
        ids.extend(sala.objetos_en_suelo)
        ids.extend(t.tipo_catalogo for t in sala.trampas)
        ids.extend(e.tipo_catalogo for e in sala.enemigos_dormidos)   # los de la sala actual, aún sin activar
        for otra in self._mapa.todas_las_salas():
            ids.extend(e.tipo_catalogo for e in otra.enemigos_activos if e.esta_vivo())
        return tuple(ids)

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
            EnemigoVista(e.etiqueta(), e.instancia_id, e.vida, e.vida_max)
            for e in sala.enemigos_activos if e.esta_vivo()
        )
        objetos = tuple(ObjetoSueloVista(i, self._catalogo.obtener(i).nombre) for i in sala.objetos_en_suelo)
        trampas = tuple(
            TrampaVista(self._catalogo.obtener(t.tipo_catalogo).nombre, t.armada) for t in sala.trampas
        )
        jugador = self._jugador
        inventario = jugador.inventario
        actual = inventario.objeto_actual()
        efectos = (("Veneno",) if jugador.veneno_activo is not None else ()) + (("Antorcha",) if self._antorcha_encendida else ())
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
            objeto_actual_indice=inventario.posicion_actual(),
            inventario_cantidad=len(inventario),
            inventario_capacidad=self._datos.inventario_max,
            pergaminos=inventario.cantidad_pergaminos(),
            retrocesos_posibles=min(inventario.cantidad_pergaminos(), len(self._historial)),
            arma_equipada=inventario.arma_equipada.ficha.nombre if inventario.arma_equipada else None,
            armadura_equipada=inventario.armadura_equipada.ficha.nombre if inventario.armadura_equipada else None,
            tiempo=self._reloj.tiempo_actual,
            desenlace=self._desenlace,
        )

    # ------------------------------------------------------------- auxiliares
    def _sala_actual(self):
        return self._mapa.obtener(self._jugador.sala_actual)

    def _decir(self, texto: str) -> None:
        self._bitacora.agregar(texto)
        self._mensajes_nuevos.append(texto)